# Set all lambda timeouts

## Usage

Run `aws lambda list-functions --max-items 1000 > functions.json` from this directory to update the json file, then run `node index.js 30` to set the timeout for all lambdas to 30 seconds.