import logging
import json
import requests
import re

import arcimoto.runtime
from arcimoto.exceptions import *

logging.basicConfig()


class Grafana:
    # logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    f = None

    # attributes
    with open('grafana_config.json') as f:
        grafana_config = json.load(f)

    # get telemetry points data
    with open('grafana_telemetry_points.json') as f:
        grafana_telemetry_points = json.load(f)

    env = 'dev'
    group_folder = None
    vin_folder = None
    datasource = None
    panel_id_counter = 1
    url_base = None

    # Grafana URLs
    grafana_ip = None
    UPSERT_URL = None
    FOLDER_URL = None

    # init grafana instance
    def __init__(self):
        self.env = arcimoto.runtime.get_env()

        self.vin_folder = self.grafana_config['folders'][self.env]['vin']['id']
        self.group_folder = self.grafana_config['folders'][self.env]['fleet']['id']
        self.datasource = self.grafana_config['datasources'][self.env]['name']

        # Grafana URLs
        self.grafana_ip = arcimoto.runtime.get_secret(f'grafana.ip.{self.env}').get('ip', None)
        if self.grafana_ip is None:
            raise ArcimotoException(f'Unable to get grafana ip for ENV {self.env}')
        self.UPSERT_URL = f'http://{self.grafana_ip}/api/dashboards/db'
        self.FOLDER_URL = f'http://{self.grafana_ip}/api/folders'

        # get url for server based on ENV
        self.url_base = f'https://telemetry.arcimoto.com' if self.env == 'prod' else f'https://{self.env}.telemetry.arcimoto.com'

    def get_headers(self):
        # get grafana secret
        grafanasecret = arcimoto.runtime.get_secret('grafana.api')

        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + str(grafanasecret['api_key'])
        }

    def publish_dashboard(self, vin, folder_id, telemetry_points, show_gps=False):
        headers = self.get_headers()

        dashboard_json = self.prepare_vehicle_dashboard(vin, folder_id, telemetry_points, show_gps=show_gps)

        # upsert dashboad
        r = requests.post(self.UPSERT_URL, data=json.dumps(dashboard_json), json=None, headers=headers)
        self.logger.debug(r.content)
        return {}

    def prepare_vehicle_dashboard(self, vin, folder_id, telemetry_points, show_gps=False):
        # load dashboard and footer from JSON config files
        try:
            with open('grafana_vin_dashboard.json') as f:
                grafana_vin_dashboard = json.load(f)
        except Exception as e:
            raise ArcimotoAlertException(f'Unable to load main dashboard JSON for Grafana dashboard provision for VIN {vin}: {e}')

        try:
            with open('grafana_vin_dashboard_footer.json') as f:
                grafana_vin_dashboard_footer = json.load(f)
        except Exception as e:
            raise ArcimotoAlertException(f'Unable to load footer JSON for Grafana dashboard provision for VIN {vin}: {e}')

        # search and replace within dashboard
        try:
            dash = json.dumps(grafana_vin_dashboard)
            dash = dash.replace('replacetext_vin', vin)
            dash = dash.replace('"replacetext_folder_id"', str(folder_id))
            dash = dash.replace('replacetext_datasource', self.datasource)
            dashboard_json = json.loads(dash)
        except Exception as e:
            raise ArcimotoAlertException(f'Unable to assemble dynamic panels for Grafana dashboard provision for VIN {vin}: {e}')

        current_x = 0
        current_y = 44  # after the 4 rows of dynamic panels each at height 8, and one row at height 12
        last_height = 8
        self.panel_id_counter = 6  # 6 dynamic panels

        try:
            for telemetry_point in telemetry_points:
                # skip not configured telemetry points
                if telemetry_point not in self.grafana_telemetry_points:
                    self.logger.debug(f'Error: the telemetry point {telemetry_point} is not configured in grafana_telemetry_points.json')
                    continue
                # skip fault points, they show in the footer fault panels section already
                if 'fault' in telemetry_point:
                    self.logger.info(f'Telemetry point {telemetry_point} skipped for line graphs because it is included in the fault panels.')
                    continue
                # skip gps_altitude, only relevant on GPS worldmap panel, which is not currently deployed
                if 'gps' in telemetry_point:
                    self.logger.info(f'Telemetry point {telemetry_point} skipped for line graphs because it is GPS related.')
                    continue

                point_data = self.grafana_telemetry_points[telemetry_point]
                # default values, consider if these should be dynamic
                point_data['attribute_name'] = telemetry_point
                point_data['width'] = 12
                point_data['height'] = 12
                point_data['ds_period'] = '30m'  # 30 minute period for downsampling
                self.logger.debug(telemetry_point)

                # handle different types of graphs
                if point_data['type'] == 'line_graph':
                    # load config from JSON file
                    json_filename = 'grafana_line_graph.json'
                elif point_data['type'] == 'worldmap' and show_gps:
                    json_filename = 'grafana_worldmap_graph.json'

                # handle stuff that happens on all graph types
                if point_data['type'] == 'line_graph' or (point_data['type'] == 'worldmap' and show_gps):
                    with open(json_filename) as f:
                        graph = json.load(f)
                    replacements_array = [{'original': 'DYNAMIC_TITLE', 'changed': point_data['title']}]
                    graph = self.perform_replacements(graph, replacements_array)
                    # height, width and position of the panel
                    current_x, current_y, last_height, graph = self.set_panel_x_y(point_data, graph, current_x, current_y, last_height)

                    # refine differnet types of graphs
                    if point_data['type'] == 'line_graph':
                        if telemetry_point == 'odometer':
                            graph['fieldConfig']['defaults']['decimals'] = 2
                            graph['fieldConfig']['defaults']['unit'] = 'none'
                        # dynamic query aliases
                        replacements_array = [{'original': 'DYNAMIC_QUERY_ALIAS_1', 'changed': telemetry_point}]
                        graph = self.perform_replacements(graph, replacements_array)
                        replacements_array = [{'original': 'DYNAMIC_QUERY_ALIAS_2', 'changed': telemetry_point}]
                        graph = self.perform_replacements(graph, replacements_array)
                        # dynamic ylabel
                        replacements_array = [{'original': 'DYNAMIC_YLABEL', 'changed': point_data['ylabel']}]
                        graph = self.perform_replacements(graph, replacements_array)
                        # Add a series for each series element
                        series_overrides_element = list(map(lambda x: {'alias': x['title'], 'color': x['color']}, [point_data]))
                        graph['seriesOverrides'] = series_overrides_element
                        # queries
                        replacements_array = [{'original': 'DYNAMIC_QUERY_1', 'changed': self.prepare_query([point_data], vin)}]
                        graph = self.perform_replacements(graph, replacements_array)
                        replacements_array = [{'original': 'DYNAMIC_RAW_SQL_1', 'changed': self.prepare_raw_sql([point_data], vin,)}]
                        graph = self.perform_replacements(graph, replacements_array)
                        replacements_array = [{'original': 'DYNAMIC_QUERY_2', 'changed': self.prepare_query([point_data], vin, downsampled=True)}]
                        graph = self.perform_replacements(graph, replacements_array)
                        replacements_array = [{'original': 'DYNAMIC_RAW_SQL_2', 'changed': self.prepare_raw_sql([point_data], vin, downsampled=True)}]
                        graph = self.perform_replacements(graph, replacements_array)
                        replacements_array = [{'original': 'DYNAMIC_DATASOURCE', 'changed': self.datasource}]
                        graph = self.perform_replacements(graph, replacements_array)
                    elif point_data['type'] == 'worldmap' and show_gps:
                        # queries
                        replacements_array = [{'original': 'DYNAMIC_GPS_QUERY', 'changed': self.prepare_gps_query([point_data], vin)}]
                        graph = self.perform_replacements(graph, replacements_array)
                        replacements_array = [{'original': 'DYNAMIC_DATASOURCE', 'changed': self.datasource}]
                        graph = self.perform_replacements(graph, replacements_array)
                        replacements_array = [{'original': 'DYNAMIC_VIN', 'changed': vin}]
                        graph = self.perform_replacements(graph, replacements_array)

                    # set id and append to list of panels
                    graph['id'] = int(self.panelIdReplace(1))
                    dashboard_json['dashboard']['panels'].append(graph)
        except Exception as e:
            raise ArcimotoAlertException(f'Unable to assemble telemetry point panels for Grafana dashboard provision for VIN {vin}: {e}')

        try:
            # prepare footer
            footer = json.dumps(grafana_vin_dashboard_footer)
            footer = footer.replace('replacetext_datasource', self.datasource)
            footer = footer.replace('"replacetext_x1"', str(0))
            footer = footer.replace('"replacetext_x2"', str(12))
            footer = footer.replace('"replacetext_y1"', str(current_y + 12))
            footer = footer.replace('"replacetext_y2"', str(current_y + 24))
            footer = re.sub('"replacetext_panel_id"', self.panelIdReplace, footer)
            footer_json = json.loads(footer)

            # append final panels
            for item in footer_json:
                dashboard_json['dashboard']['panels'].append(item)
        except Exception as e:
            raise ArcimotoAlertException(f'Unable to assemble footer for Grafana dashboard provision for VIN {vin}: {e}')

        return dashboard_json

    def provision_grafana_group_overview(self, group, vehicles):
        '''
        Purpose:
            create group overview dashboard and deploy to Grafana
        Inputs:
            group: group id
            vehicles: list of vins
            vehicles_meta: corresponding list of vehicle meta data
        '''
        try:
            headers = self.get_headers()

            # get overview dashboard specification
            with open('grafana_overview_dashboard.json') as f:
                overview_dashboard = json.load(f)

            # get overview dashboard header specification
            with open('grafana_overview_header_panel.json') as f:
                overview_header_panel = json.load(f)

            # get overview panel specification
            with open('grafana_overview_vin_panel_set.json') as f:
                overview_vin_panel_set = json.load(f)

            # reset panel id counter
            self.panel_id_counter = 1

            # header offset
            header_offset = 2  # should be consistent with contents of overview_header_panel

            # update overview dashboard if vehicle belongs to group
            overview_dashboard_mod = json.dumps(overview_dashboard)
            overview_dashboard_mod = overview_dashboard_mod.replace('replacetext_overview_uid', f'overview_{str(group[0])}')
            overview_dashboard_mod = overview_dashboard_mod.replace('replacetext_overview_title', f'{group[1]} [{str(group[0])}] - Overview')
            overview_dashboard_mod = overview_dashboard_mod.replace('"replacetext_folder_id"', str(self.group_folder))
            overview_dashboard_mod = json.loads(overview_dashboard_mod)

            # append header panel
            overview_header_panel_mod = json.dumps(overview_header_panel)
            overview_header_panel = json.loads(overview_header_panel_mod)
            for item in overview_header_panel:
                item_mod = json.dumps(item)
                item_mod = re.sub('"replacetext_panel_id"', self.panelIdReplace, item_mod)
                item_mod = json.loads(item_mod)
                overview_dashboard_mod['dashboard']['panels'].append(item_mod)

            vehicle_counter = 0
            x_offset = 0
            y_offset = header_offset
            panel_height = 4
            panel_width = 4
            num_panels = 4  # number of panels per vehicle, arranged in a column
            num_panels_wide = int(24 / panel_width)

            for vehicle in vehicles:
                # new row every 24/panel_width vehicles
                vin = vehicle[0]
                if (vehicle_counter % num_panels_wide == 0 and vehicle_counter != 0):
                    x_offset = 0
                    y_offset += panel_height * num_panels + 1

                # perform replacements
                panel = json.dumps(overview_vin_panel_set)
                panel = panel.replace('replacetext_url_base', self.url_base)
                panel = panel.replace('replacetext_vin', vin)
                panel = panel.replace('replacetext_datasource', self.datasource)
                panel = panel.replace('"replace_panel_height"', str(panel_height), num_panels)
                panel = panel.replace('"replace_panel_width"', str(panel_width), num_panels)
                panel = panel.replace('"replaceval_0"', str(y_offset))
                panel = panel.replace('"replaceval_4"', str(4 + y_offset))
                panel = panel.replace('"replaceval_8"', str(8 + y_offset))
                panel = panel.replace('"replaceval_10"', str(10 + y_offset))
                panel = panel.replace('"replaceval_12"', str(12 + y_offset))
                panel = panel.replace('"replaceval_14"', str(14 + y_offset))
                panel = panel.replace('"replaceval_16"', str(16 + y_offset))
                panel = re.sub('"replacetext_panel_id"', self.panelIdReplace, panel)
                panel = panel.replace('"replace_x_column"', str(x_offset))

                # attach panel items to overview dashboard
                panel = json.loads(panel)
                for item in panel:
                    overview_dashboard_mod['dashboard']['panels'].append(item)
                x_offset += panel_width
                vehicle_counter += 1

            # handle no vehicles in group
            if len(vehicles) == 0:
                item = {
                    "content": "<h3>No Vehicles in Fleet</h3>",
                    "gridPos": {
                        "h": 2,
                        "w": 24,
                        "x": 0,
                        "y": 0
                    },
                    "id": 1,
                    "links": [],
                    "mode": "html",
                    "title": "",
                    "transparent": True,
                    "type": "text"
                }
                overview_dashboard_mod['dashboard']['panels'].append(item)

            # upsert overview dashboard
            r = requests.post(self.UPSERT_URL, data=json.dumps(overview_dashboard_mod), json=None, headers=headers)

            self.logger.debug(r.content)
            return {}

        except Exception as e:
            raise ArcimotoException(f'provision_grafana_group_overview function failed: {e}')

    def provision_grafana_group_telemetry(self, group, vehicles):
        '''
        Purpose:
            create group telemetry dashboard and deploy to Grafana
        Inputs:
            group: group id
            vehicles: list of vins
            vehicles_meta: corresponding list of vehicle meta data
        '''
        try:
            headers = self.get_headers()

            # get overview dashboard specification
            with open('grafana_group_telemetry_dashboard.json') as f:
                group_telemetry_dashboard = json.load(f)

            # get overview dashboard header specification
            with open('grafana_overview_header_panel.json') as f:
                overview_header_panel = json.load(f)

            # get overview panel specification
            with open('grafana_group_telemetry_panel_set.json') as f:
                group_telemetry_panel_set = json.load(f)

            # reset panel id counter
            self.panel_id_counter = 1

            # header offset
            header_offset = 2  # should be consistent with contents of overview_header_panel

            # update group telemetry dashboard if vehicle belongs to group
            num_variables = 4  # number of variables in group_telemetry dashboard
            group_telemetry_dashboard_mod = json.dumps(group_telemetry_dashboard)
            group_telemetry_dashboard_mod = group_telemetry_dashboard_mod.replace('replacetext_overview_uid', f'group_telemetry_{str(group[0])}')
            group_telemetry_dashboard_mod = group_telemetry_dashboard_mod.replace('replacetext_overview_title', f'{group[1]} [{str(group[0])}] - Telemetry')
            group_telemetry_dashboard_mod = group_telemetry_dashboard_mod.replace('"replacetext_folder_id"', str(self.group_folder))
            group_telemetry_dashboard_mod = group_telemetry_dashboard_mod.replace('replacetext_datasource', str(self.datasource), num_variables)
            group_telemetry_dashboard_mod = json.loads(group_telemetry_dashboard_mod)

            # append header panel
            overview_header_panel_mod = json.dumps(overview_header_panel)
            overview_header_panel = json.loads(overview_header_panel_mod)
            for item in overview_header_panel:
                item_mod = json.dumps(item)
                item_mod = item_mod.replace('replacetext_url_base', self.url_base)
                item_mod = re.sub('"replacetext_panel_id"', self.panelIdReplace, item_mod)
                item_mod = json.loads(item_mod)
                group_telemetry_dashboard_mod['dashboard']['panels'].append(item_mod)

            y_offset = header_offset
            num_panels = 2  # number of panels per vehicle, arranged in a row
            panel_height = 8
            panel_width = int(24 / num_panels)

            for vehicle in vehicles:
                vin = vehicle[0]

                # perform replacements
                panel = json.dumps(group_telemetry_panel_set)
                panel = panel.replace('replacetext_vin', vin)
                panel = panel.replace('replacetext_datasource', self.datasource)
                panel = panel.replace('"replace_panel_height"', str(panel_height), num_panels)
                panel = panel.replace('"replace_panel_width"', str(panel_width), num_panels)
                panel = re.sub('"replacetext_panel_id"', self.panelIdReplace, panel)

                # attach panel items to group_telemetry dashboard
                panel = json.loads(panel)
                x_offset = 0
                for item in panel:
                    item['gridPos']['x'] = x_offset
                    item['gridPos']['y'] = y_offset
                    group_telemetry_dashboard_mod['dashboard']['panels'].append(item)
                    x_offset += panel_width
                y_offset += panel_height

            # handle no vehicles in group
            if len(vehicles) == 0:
                item = {
                    "content": "<h3>No Vehicles in Fleet</h3>",
                    "gridPos": {
                        "h": 2,
                        "w": 24,
                        "x": 0,
                        "y": 0
                    },
                    "id": 1,
                    "links": [],
                    "mode": "html",
                    "title": "",
                    "transparent": True,
                    "type": "text"
                }
                group_telemetry_dashboard_mod['dashboard']['panels'].append(item)

            # upsert overview dashboard
            r = requests.post(self.UPSERT_URL, data=json.dumps(group_telemetry_dashboard_mod), json=None, headers=headers)

            self.logger.debug(r.content)
            return {}

        except Exception as e:
            raise ArcimotoException(f'provision_grafana_group_telemetry function failed: {e}')

    def panelIdReplace(self, m):
        self.panel_id_counter += 1
        return str(self.panel_id_counter)

    def perform_replacements(self, json_object, replace_array, count=1):
        try:
            str_json = json.dumps(json_object)
        except Exception as e:
            raise ArcimotoAlertException(f'Unable to dump JSON from {json_object}: {e}')

        try:
            for replacement in replace_array:
                str_json = str_json.replace(replacement['original'], str(replacement['changed']), count)
        except Exception as e:
            raise ArcimotoAlertException(f'Unable to make replacements in JSON string, replace_array {replace_array}, str_json {str_json}: {e}')

        try:
            json_output = json.loads(str_json)
        except Exception as e:
            raise ArcimotoAlertException(f'Unable to parse valid JSON from replaced JSON string, str_json {str_json}: {e}')

        return json_output

    def set_panel_x_y(self, panel_item, graph, current_x, current_y, last_height):
        height = panel_item['height']
        width = panel_item['width']
        if (current_x + width) <= 24:
            x_position = current_x
            y_position = current_y
            next_x = current_x + width
            next_y = current_y
        else:
            x_position = 0
            y_position = current_y + last_height
            next_x = x_position + width
            next_y = y_position
        graph['gridPos']['h'] = height
        graph['gridPos']['w'] = width
        graph['gridPos']['y'] = y_position
        graph['gridPos']['x'] = x_position

        return next_x, next_y, height, graph

    def prepare_raw_sql(self, data_array, vin, downsampled=False):
        data_operations = list(map(lambda x: x['operator'], data_array))
        data_operations = list(set(data_operations))
        arguments_string = ', '.join(list(map(lambda x: '{0}(*)'.format(x), data_operations)))
        if downsampled:
            measurement = '\\\"365d\\\".\\\"telemetry\\\"'
            time_window = 'AND time < now()-30d'
        else:
            measurement = '\\\"telemetry\\\"'
            time_window = ''
        return "SELECT {0} FROM {1} WHERE $timeFilter {2} AND \\\"vin\\\"='{3}' GROUP BY time($__interval) fill(null)".format(arguments_string, measurement, time_window, vin)

    def prepare_query(self, data_array, vin, downsampled=False):
        try:
            data = data_array[0]
        except Exception as e:
            raise ArcimotoAlertException(f'Unable to get data from data_array for Grafana dashboard provision for VIN {vin}, data_array {data_array}: {e}')

        try:
            offset = data.get('offset', '')
        except Exception as e:
            raise ArcimotoAlertException(f'Unable to get data values from data for Grafana dashboard provision for VIN {vin}, data {data}: {e}')

        if downsampled:
            arguments_string = ', '.join(list(map(lambda x: '{0}({2}_{1}){4} as {1}_{3}'.format(x['operator'], x['attribute_name'], x['downsample'], x['ds_period'], offset), data_array)))
            measurement = '\\\"365d\\\".\\\"telemetry\\\"'
            time_window = 'AND time < now()-30d'
        else:
            arguments_string = ', '.join(list(map(lambda x: '{0}({1}){2} as {1}'.format(x['operator'], x['attribute_name'], offset), data_array)))
            measurement = '\\\"telemetry\\\"'
            time_window = ''
        return "SELECT {0} FROM {1} WHERE $timeFilter {2} AND \\\"vin\\\"='{3}' GROUP BY time($__interval) fill(null)".format(arguments_string, measurement, time_window, vin)

    def prepare_gps_query(self, data_array, vin, downsampled=False):
        if downsampled:
            # untested!  (We are not deploying the worldmap panel on provision at the moment)
            arguments_string = ', '.join(list(map(lambda x: "{0}(\\\"{4}_{1}\\\") AS \\\"metric_{5}\\\", {0}(\\\"{4}_{2}\\\") AS \\\"latitude_{5}\\\", {0}(\\\"{4}_{3}\\\") AS \\\"longitude_{5}\\\"".format(x['operator'], x['metric'], x['latitude'], x['longitude'], x['downsample'], x['ds_period']), data_array)))
            measurement = '\\\"365d\\\".\\\"telemetry\\\"'
            time_window = 'AND time < now()-30d'
        else:
            arguments_string = ', '.join(list(map(lambda x: "{0}(\\\"{1}\\\") AS \\\"metric\\\", {0}(\\\"{2}\\\") AS \\\"latitude\\\", {0}(\\\"{3}\\\") AS \\\"longitude\\\"".format(x['operator'], x['metric'], x['latitude'], x['longitude']), data_array)))
            measurement = '\\\"telemetry\\\"'
            time_window = ''
        return "SELECT {0} FROM {1} WHERE $timeFilter {2} AND \\\"vin\\\"='{3}' GROUP BY time(1m) fill({4})".format(arguments_string, measurement, time_window, vin, data_array[0]['fill'])

    def list_folders(self):
        headers = self.get_headers()

        # list folders
        r = requests.get(self.FOLDER_URL, data=None, json=None, headers=headers)
        self.logger.debug(r.content)
        return {}
