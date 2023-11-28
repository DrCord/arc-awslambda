import logging
import requests
import json
import grafana

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.user
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@arcimoto.runtime.handler
@arcimoto.user.require('grafana.group.write')
def provision_grafana_groups():
    global logger

    try:
        env = arcimoto.runtime.get_env()
        cursor = arcimoto.db.get_cursor()
        grafana_instance = grafana.Grafana()
        grafana_ip = arcimoto.runtime.get_secret(f'grafana.ip.{env}').get('ip', None)
        if grafana_ip is None:
            raise ArcimotoException(f'Unable to get grafana ip for ENV {env}')
        # upsert dashboard endpoint
        url = f'http://{grafana_ip}/api/dashboards/db'

        headers = grafana_instance.get_headers()

        # select all vehicles for provided group for overview dashboard creation
        query = (
            'SELECT id, name '
            'FROM vehicle_group '
            'ORDER BY name'
        )
        cursor.execute(query)
        groups = cursor.fetchall()

        if groups is None:
            raise ArcimotoNotFoundError('No groups found')

        # get color data
        with open('grafana_colors.json') as f:
            colors = json.load(f)

        color_palette = colors['groups_palette']

        # get groups dashboard specification
        with open('grafana_groups_dashboard.json') as f:
            groups_dashboard = json.load(f)

        # get groups panel specification
        with open('grafana_groups_panel_set.json') as f:
            groups_panel_set = json.load(f)

        # get url for server based on ENV
        url_base = f'https://telemetry.arcimoto.com' if env == 'prod' else f'https://{env}.telemetry.arcimoto.com'

        groups_dashboard = json.dumps(groups_dashboard)
        groups_dashboard = groups_dashboard.replace('replacetext_url_base', url_base)
        groups_dashboard = groups_dashboard.replace('replacetext_overview_dashboard', 'group_overview_dashboard')
        groups_dashboard = groups_dashboard.replace('replacetext_overview_title', 'Fleets Overview')

        # update groups dashboard if vehicle belongs to group
        groups_dashboard = json.loads(groups_dashboard)
        group_counter = 0
        x_offset = 0
        y_offset = 0
        color_counter = 0

        for group in groups:
            # exclude Arcimoto special group (id 1)
            if group[0] == 1:
                continue
            # new row every 8 vehicles
            if group_counter != 0:
                x_offset += 4  # to match width of overview panel
                if group_counter % 6 == 0:
                    x_offset = 0
                    y_offset += 9  # was 6 before adding group telemetry panels

            panel = json.dumps(groups_panel_set)
            panel = panel.replace('replacetext_url_base', url_base)
            panel = panel.replace('replacetext_uid_1', f'overview_{str(group[0])}')
            panel = panel.replace('replacetext_title_1', f'{group[1]}_{str(group[0])}')
            panel = panel.replace('replacetext_uid_2', f'group_telemetry_{str(group[0])}')
            panel = panel.replace('replacetext_title_2', env + '_' + group[1] + '_' + str(group[0]) + '_telemetry')
            panel = panel.replace('replacetext_name', group[1])
            panel = panel.replace('"replacetext_panel_id_1"', str(group_counter * 2 - 1))
            panel = panel.replace('"replacetext_panel_id_2"', str(group_counter * 2))

            color = color_palette[color_counter]
            color_counter += 1
            if color_counter >= len(color_palette):
                color_counter = 0
            panel = panel.replace('replacetext_color', color)
            panel = panel.replace('"replacetext_x_offset_1"', str(x_offset))
            panel = panel.replace('"replacetext_y_offset_1"', str(y_offset))
            panel = panel.replace('"replacetext_x_offset_2"', str(x_offset))
            panel = panel.replace('"replacetext_y_offset_2"', str(y_offset + 6))  # 6 to match height of overview panel

            panel = json.loads(panel)
            for item in panel:
                groups_dashboard['dashboard']['panels'].append(item)

            group_counter += 1

        # Upsert overview dashboard
        r = requests.post(url, data=json.dumps(groups_dashboard), json=None, headers=headers)

        return {}

    except Exception as e:
        raise ArcimotoException(f'provision_grafana_groups function failed: {e}')


lambda_handler = provision_grafana_groups
