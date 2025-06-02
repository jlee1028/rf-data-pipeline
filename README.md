This example pipeline reads RF data from from s3, identifies signals where CPU spikes took place, and writes them to a separate s3 location.

**Prerequisites**
* Python3.9+
* AWS lambda and s3

## Architecture

* The lambda function is triggered by an s3 event in our s3 bucket where the object key is prefixed with "input/"
* The bucket name and object key are parsed out of the event data and the file is read into memory as a pandas dataframe
* The records where CPU spikes take place are isolated and written to a new csv file with a "cpu_spike/" prefix

## AWS Setup
* Create lambda function
* Create s3 bucket
* Add relevant permissions to the lambda's execution role
* Create the trigger in the lambda console
* Deploy the function
* Upload a file to the s3 bucket, check the CloudWatch logs
