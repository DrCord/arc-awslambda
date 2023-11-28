# AWSTelemetry/utility/Grafana Create JSON
Tool for using the metrics.json file to generate the Grafana configuration json file

## Usage
open the node.js file and replace the metrics variable with your metrics.json data, save, run `node node.js`, the output will be `telemetry_points.json`

## Requirements
Node.js

## TODO
Make the script work right when ingesting the metrics from a file instead of from a variable within the same file
