# Grafana Re-Provision Scripts

These scripts allow you to run all of a "level" of the grafana provisioning process:

- the fleet overviews
- the fleet views
- the VIN views

## Scripts

### grafana_reprovision_group_overviews

```python-cli
$ python3 ./utility/grafana_reprovision/grafana_reprovision_group_overviews.py [-h] --user USER -e {dev,staging,prod}

positional arguments:
  function              the name of the lambda function to allow

optional arguments:
  -h, --help                   show this help message and exit
  --user USER                  authenticate as a specific user before invoking
  -e, --env {dev,staging,prod} environment to use (default: dev)
```

### grafana_reprovision_vehicle_dashboards

```python-cli
$ python3 ./utility/grafana_reprovision/grafana_reprovision_vehicle_dashboards.py [-h] --user USER -e {dev,staging,prod}

positional arguments:
  function              the name of the lambda function to allow

optional arguments:
  -h, --help                   show this help message and exit
  --user USER                  authenticate as a specific user before invoking
  -e, --env {dev,staging,prod} environment to use (default: dev)
```

### grafana_reprovision_vehicle_groups

```python-cli
$ python3 ./utility/grafana_reprovision/grafana_reprovision_vehicle_groups.py [-h] --user USER -e {dev,staging,prod}

positional arguments:
  function              the name of the lambda function to allow

optional arguments:
  -h, --help                   show this help message and exit
  --user USER                  authenticate as a specific user before invoking
  -e, --env {dev,staging,prod} environment to use (default: dev)
```