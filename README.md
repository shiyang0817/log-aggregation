# smallest-authorization-@edge

Previously we discussed log aggregation solution. In this solution scenario, the log files are generated and initially stored in customer's IDC. In order to achieve log aggregation and analysis on cloud, these logs need to be ingested into cloud. It is essential to build a data pipeline between customer's IDC and  S3 @aws region. Kinesis agent deployed on-prem + Kinesis Data Stream instance + Kinesis Data Firehose instance together play as the data pipeline.

How to guarantee that the on-prem deployed Kinesis agent can only access to Kinesis Data Stream instance, with no permissions to other services is quite crucial from security perspective. This doc describes the solution on this very point.

The key conception of this solution is the STS assumeRole mechanism provided by aws IAM service. By applying the STS assumeRole feature, an IAM user could get itself adhered to a service role, and functions as the service role, meaning that the permissions the IAM user has is exactly the same as the service role. 

Leveraging on this feature, we set IAM User A who is a common IAM user, may possibly have many permissions and roles attached, IAM user B who is a special IAM user who does not have any permissions. We define a service role under IAM user A, the service role has just one permission policy, namely the AmazonKinesisFullAccess, to enable itself to manipulate Kinesis service. Then, we set IAM user B to assume this service role by configuring it in IAM user A's Trust Relationship tab. The json policy description file sample is as below:

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::<account id>:user/<IAM user B>"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}

Next, we acquire IAM user B's security credentials (the ak and sk) from the root user. And then amend the kinesis agent.json file is below:

{
   "kinesis.endpoint": "kinesis.<specific region name>.amazonaws.com", 
   "assumeRoleARN": "arn:aws:iam::<account id>:role/<IAM user B>",
   "awsAccessKeyId": "<the ak>",
   "awsSecretAccessKey": "<the sk>",
   "flows": [
              {
                 "filePattern": "/tmp/app.log*",
                 "kinesisStream": "<the KDS instance name>"
              }
   ]
}
  
Aftering finishing configuring the above, now the on-prem kinesis agent who now holds the security credentails of IAM user B, can get access to kinesis serivce intance created under IAM user A with the smallest authorization. the solution diagram is show as below.
<img width="1159" alt="Screen Shot 2022-01-17 at 6 21 30 PM" src="https://user-images.githubusercontent.com/97269758/149751843-03e46941-d42c-4e25-be11-30ef5e8b4c33.png">

