var request = require('request');
const url = 'http://172.30.0.203/telegraf'
const vin_data = require('./vin_data_1.json')
var argv = require('minimist')(process.argv.slice(2));

args = {}
args.num_seconds = argv.num_seconds || 5
args.year = argv.year || 2019
args.month = argv.month || 1
args.day = argv.day || 1
args.hour = argv.hour || 0
args.minute = argv.minute || 0
args.second = argv.second || 0

let runstart = new Date();

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function insertData(){

    vin_count = vin_data.length;
    for (x=0; x<args.num_seconds; x++){
        //console.log("vin data", vin_data);
        currentSecond = new Date();

        for (vv=0; vv<vin_data.length; vv++){
            //console.log(vin_data[vv]);
            let telegraf_json = {"vin": vin_data[vv].vin, "group": "stress01", "timestamp": currentSecond.getTime(), "speed": Math.floor(Math.random() * 100), "steering_angle":Math.floor(Math.random() * 100), "tempdata": true}
            //console.log(telegraf_json)
            //await sleep(1);
            request.post({
                uri: url,
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(telegraf_json)
            });
        }
        sleep(1000); //wait a second and process next batch
        console.log(currentSecond + ": inserted "+vin_count+" records", )
    }
}

insertData().then(result => {
    let runend = new Date()
    duration_in_ms = runend.getTime() - runstart.getTime()                        
    console.log("duration_in_ms: "+duration_in_ms)
})



