#!/usr/bin/env node
var program = require('commander')
var AWS = require('aws-sdk')
const lambda = new AWS.Lambda({ region: 'us-west-2' })
var awsFunctions = require('./functions.json')

program
  .arguments('<timeout>')
  .action(function(timeout) {
    var functions = awsFunctions.Functions
    for (var i = 0; i < functions.length; i++) {
      var functionName = functions[i].FunctionName
      /* This operation updates a Lambda function's configuration */
      var params = {
        FunctionName: functionName,
        Timeout: timeout,
      }
      lambda.updateFunctionConfiguration(params, function(err, data) {
        if (err) console.log(err, err.stack)
        // an error occurred
        else console.log(data) // successful response
      })
    }
  })
  .parse(process.argv)
