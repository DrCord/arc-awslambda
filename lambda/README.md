# Lambdas

## AWS Runtime Configuration

All lambda functions should be configured with the following configuration within the AWS console. If you use the [lambda utility](../utility/lambda/README.md) to create the lambda, these settings will be configured correctly for you by default (for the Telemetry security zone).

- Runtime
  - Python 3.6
    - **NOTE**: The bundled [psycopg2](../dependencies/psycopg2.zip) package requires 3.6 exactly

- Network
  - Telemetry Zone
    - VPC:
      - vpc-c92dd3b1 (172.30.0.0/16) | telemetry
    - Subnets:
      - subnet-ddf88c96 (172.30.3.0/24) | us-west-2a, tel-nat-a
      - subnet-864309ff (172.30.4.0/24) | us-west-2b, tel-nat-b
      - subnet-4381a419 (172.30.5.0/24) | us-west-2c, tel-nat-c
    - Security Group:
      - sg-e6405396 (telemetry-security-group) | telemetry-security-group

- Role
  - Lambda functions are grouped into roles depending on their needs and their bundle. The configured role is referenced at runtime by the [arcimoto package](../dependencies/arcimoto/README.md), and informs other policy access. See [lambda_roles.md](../docs/lambda_roles.md) for details.

## Bundles

Lambdas are broken down into bundles to aid with deployment and organization:

- [alarms](./alarms/README.md)
  - Functions related to data/system observation and alerting
- [authorities](./authorities/README.md)
  - Authority Manager related functions
- [debug](./debug/README.md)
  - Administrative tools for internal use
- [firmware](./firmware/README.md)
  - Vehicle firmware version tracking and management
- [grafana](./grafana/README.md)
  - Grafana/visualization related functions
- [hologram](./hologram/README.md)
  - Cellular (hologram.io) related integration functions
- [notes](./notes/README.md)
  - Generalized note/tagging functions
- [recalls](./recalls/README.md)
  - Functions related to managing vehicle recall data
- [telemetry](./telemetry/README.md)
  - Functions related to configuring vehicle telemetry data feed
- [users](./users/README.md)
  - User Manager functionality, including group and permission management
- [utility](./utility/README.md)
  - Miscellaneous functions, including devops and maintenance
- [vehicles](./vehicles/README.md)
  - Core Vehicle Manager functionalty

## AWS Lambda Layers

Lambda layer allow you to bundle lambda dependencies directly in AWS. You can include a single dependency/library or many in a layer.

### Layers list

Existing custom layers that are available in our AWS infrastrucure.

| AWS layer name    | local depedency name | Includes                     |
|-------------------|----------------------|------------------------------|
| arcimoto-globals  | global_dependencies  | arcimoto, cerberus, psycopg2 |
| requests-extended | requests_extended    | requests_extended            |

### Creating a layer archive

1. You need a folder that you plan to zip to build the archive structure into and then drop your packages into. For python 3.6 the folder structure before you put in your package(s) would be: `{BASE_FOLDER_TO_ZIP}/lib/python3.6/site-packages`

2. Extract/copy the package(s) for your layer into `site-package` in the archive you created. There should be a folder named exactly what your package is named for each package included in your layer in `site-packages`.
    - For packages already working within our bundling system and included within our repo you should be able to move/extract the repo directly files to your layer archive.
    - When packaging a python package not included in our existing codebase you will need to build it on a host system that matches the labmda runtime (eg, centos) in order for any compiled code to run correctly. This is not an issue for pure python packages, but psycopg (for example) has a bunch of C code compiled into it, and the target system where the package is built is important.

3. Zip the `{BASE_FOLDER_TO_ZIP}` in the archive.

### Uploading the layer to AWS

Uploading the layer archive to AWS to create the AWS lambda layer has 2 possible methods: CLI or AWS console.

#### CLI

[AWS Documentation](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html#configuration-layers-manage)

#### AWS Console

1. Go to [AWS Lambda Layers (us-west-2)](https://us-west-2.console.aws.amazon.com/lambda/home?region=us-west-2#/layers)

2. Click "Create layer"

3. Give the layer a unique, machine-friendly name. We typically use kebob-case (lowercase with dashes as seperators).

4. Input any relevant info in the description, like the packages included.

5. Upload the zip archive you created for the layer

6. Choose compatible runtimes that you setup in the folder structure in the layer archive

7. Click "Create"

8. Note the layer name and version number for use in adding to our dependency system

### Making a layer available for use in our dependency system

The dependencies.json file has a top level item `layers`, adding an item to the layers section makes it available to use as a layer when building lambdas.

Example:

```json
"requests_extended": {
      "name": "requests-extended",
      "version": 1,
      "meta": {
        "contains": [
          "requests_extended"
        ]
      }
    }
```

### Using a layer within our dependency system

Adding a flag to the common dependency of `layer: true` will leave it out of the bundling process and once it has been added to the dependencies `layer` section as outlined in `Making a layer available for use in our dependency system` above will include it in the layers list attachment to the lambda once it has been created/updated.

## Arcimoto Lambda Template

The [example_lambda template](../docs/example_lambda.py) serves as a general example of how best to build a lambda which incorporates internal arcimoto functionality. Please see the [arcimoto package documentation](../dependencies/arcimoto/README.md) for details on standard lambda behaviors.

## IoT rules triggering lambda aliases

To attach an IoT rule to an alias of a lambda you must either:

- create the rule entirely from the lambda side by adding a new IoT rule as a trigger
- use boto to make the IoT rule

Either way you must attach it as a trigger from the lambda side in the lambda alias' "Designer" section in the AWS Console UI.
