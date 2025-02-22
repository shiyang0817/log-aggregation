# log-aggregation

quite a number of customers have their critical systems deployed on-premise, especially for those who are sensitive towards data security.
however, logs collected from those on-prem systems with large volumes and values dispered between countless records are usually less sensitive, and when it comes to cross geo-region aggregation scenario, it is much more efficient and cost-effective to store those logs on cloud to achieve the aggregated anaylsis, as cloud provides a cross region integrated platform with high scalability and durability.

this doc describes a log aggregation solution leveraging on aws cloud services. logs are initially generated by different geo-regions. Afterwards, these logs will be collected to the nearest aws regions, and then synced to a central region for further aggregation analysis. the processing steps are as follows.

## Tabel of Contents
- [1. on-prem logs transfered to nearest aws region](#1-on-prem-logs-transfered-to-nearest-aws-region)
   - [1.1 first, a client agent needs to be installed on customers on-prem enviroment. the agent is named as Kinesis Agent](#11-first-a-client-agent-needs-to-be-installed-on-customers-on-prem-enviroment-the-agent-is-named-as-kinesis-agent)
   - [1.2 Kinesis Data Streams + Kinesis Data Firhose pipeline](#12-kinesis-data-streams--kinesis-data-firhose-pipeline)
- [2. logs ingested and stored in different aws regions aggregation](#2-logs-ingested-and-stored-in-different-aws-regions-aggregation)
- [3. analyze those logs through aws opensearch](#3-analyze-those-logs-through-aws-opensearch)
- [4. set up index in aws opensearch](https://github.com/symeta/ES-Operation)
- [5. configure alerting through kibana console](#5-configure-alerting-through-kibana-console)
- [6. solution diagram](#4-solution-diagram)
- [7. related solution points: no.1 smallest authorization @edge](https://github.com/symeta/log-aggregation/tree/smallest-authorization-%40edge#smallest-authorization-edge)
- [8. related solution points: no.2 lambda get sub-dir from s3 bucket](https://github.com/symeta/log-aggregation/tree/lambda-get-sub-dir-from-s3-bucket#lambda-get-sub-dir-from-s3-bucket)

## 1. on-prem logs transfered to nearest aws region

### 1.1 first, a client agent needs to be installed on customers on-prem enviroment. the agent is named as Kinesis Agent
Please refer to the below link for further installation guidance:
   
https://docs.aws.amazon.com/streams/latest/dev/writing-with-agents.html
   
a sample of agent.json:　
```json
   {
      "kinesis.endpoint": "kinesis.ap-southeast-1.amazonaws.com", 
      "flows": [
                 {
                   "filePattern": "/tmp/app.log*",
                   "kinesisStream": "jan5-kds-sg"
                 }
       ]
    }
```

### 1.2 Kinesis Data Streams + Kinesis Data Firhose pipeline
the log data will be transferred through the KDS + KDF pipepline and finally stored in s3 bucket.
Please refer to the below link for further setup guidance:
   
https://docs.aws.amazon.com/firehose/latest/dev/writing-with-kinesis-streams.html
    
    
## 2. logs ingested and stored in different aws regions aggregation
the aggregation of logs stored in different regions are achieved leveraging on aws s3 cross region replication feature.
please refer to the below link for further guidance:
   
https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication-walkthrough1.html

## 3. analyze those logs through aws opensearch
the logs stored in s3 will be ingested into opensearch service domain for further analysis.
please refer to the lambda function explanation as the below link:
   
https://docs.aws.amazon.com/opensearch-service/latest/developerguide/integrations.html#integrations-s3-lambda
   
and the docs link below for detail packaging guidance:
   
https://docs.aws.amazon.com/lambda/latest/dg/python-package.html#python-package-create-package-no-dependency
   
the lambda function needs to be authenticated by opensearch cluster. the authentication role mapping guidance is as below:
   
https://docs.aws.amazon.com/opensearch-service/latest/developerguide/fgac.html#fgac-mapping

## 5. configure alerting through kibana console
* Key Step 1. access kibana console, click Anomaly Detection button in the left panel to create an anomaly detector :

![Anomaly detection  Dashboard](https://user-images.githubusercontent.com/97269758/155730566-20a58266-41f0-41a6-b38d-37660d00fb91.png)

![Open Distro for Elasticsearch](https://user-images.githubusercontent.com/97269758/155730612-7dcf7ef5-c8a7-4b4a-9371-f50aa06368ce.png)

* Key Step 2. add filter while creating the anomaly detector. this step is to configure the specific field that the detector watches:

![Add filter](https://user-images.githubusercontent.com/97269758/155730968-24e8177e-452e-43a1-aaa0-afce559cca05.png)

* Key Step 3. configure model. this step is to configure the Random Cut Forrest model to define how the anomaly event is defined and calculated.

![Configure model](https://user-images.githubusercontent.com/97269758/155731726-ba14b24e-3cc6-4d8b-b8cb-859cf8933b67.png)

for this case, we use count() as the aggregation method.

![Aggregation method](https://user-images.githubusercontent.com/97269758/155731770-9661a96b-289e-45a1-971c-b7bb77622b10.png)

* Key Step 4: switch back to the left panel and click the alerting button to create a monitor leveraging on the anomaly detector just created:

![Define monitor](https://user-images.githubusercontent.com/97269758/155731996-accb4b84-4429-401f-a7af-2123019e191e.png)

* Key Step 5: add a destination for the monitor: enabling the alerting to send out to email/sms/3rd party platform like dingding or feishu

![Amazon SNS](https://user-images.githubusercontent.com/97269758/155732568-0224c50a-b11f-4d3e-b9ad-529434c77237.png)

## 6. solution diagram
the solution diagram is shown as below:

assume that customer has on-prem system deployments at Singapore and Australia. Singapore will be the central hub for all logs. 
![Screen Shot 2022-01-07 at 12 48 17 PM](https://user-images.githubusercontent.com/97269758/148493379-3d8a64f6-8ca8-4d66-9662-33701b725a28.png)
