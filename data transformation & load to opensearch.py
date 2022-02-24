import boto3
import re
import requests
from requests_aws4auth import AWS4Auth
import time
from datetime import datetime

region = 'us-west-2' # e.g. us-west-1
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

host = 'https://search-jan2-jsuwsxlwenpntew53nwxoz74gy.us-west-2.es.amazonaws.com' # the OpenSearch Service domain, including https://
index = 'f_9'
type = '_doc'
url = host + '/' + index + '/' + type

headers = { "Content-Type": "application/json" }
s3 = boto3.client('s3')
s3_r = boto3.resource('s3')

# Lambda execution starts here
def lambda_handler(event, context):
    print("index: ", index)
    print("credentials.access_key: ", credentials.access_key)
    print("credentials.secret_key: ", credentials.secret_key)
    print("region: ",region)
    print("service: ", service)
    
    #bucket_tmp = s3_r.Bucket('log-jan')
    #for o in bucket_tmp.objects.filter(Delimiter='/'):
    #    print("o.key: ", o.key)

    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        
        print("key: ", key)
        
        obj = s3.get_object(Bucket=bucket, Key=key)
        body = obj['Body'].read()
        lines = body.splitlines()
        i=0

        #Match the regular expressions to each line and index the JSON
        for line in lines:

            print("line: ", line)
            line = line.decode("utf-8")
            li = line.split("||")
            remote_addr = li[0]
            http_x_forwarded_for = li[1]
            geoip_country_code = li[2]
            geoip_city = li[3]
            time_local = li[4]
            server_name = li[5]
            server_port = li[6]
            host = li[7]
            request = li[8]
            request_length = li[9]
            request_time = li[10]
            uid_set = li[11]
            uid_got = li[12]
            status = li[13]
            body_bytes_sent = li[14]
            bytes_sent = li[15]
            connection = li[16]
            connection_requests = li[17]
            http_user_agent = li[18]
            http_referer = li[19]
            upstream_addr = li[20]
            upstream_status = li[21]
            upstream_response_time = li[22]

            #ip = ip_pattern.search(line).group(1)
            # timestamp = time_pattern.search(line).group(1)
            # message = line

            # document = { "message": message }
            document = {'status': status, 'body_bytes_sent': body_bytes_sent, 'http_user_agent': http_user_agent, 'request_length': request_length, 'http_x_forwarded_for': http_x_forwarded_for, 'request': request, 'upstream_response_time': upstream_response_time, 'connection_requests': connection_requests, 'host': host, 'geoip_country_code': geoip_country_code, 'request_time': request_time, 'server_name': server_name, 'remote_addr': remote_addr, 'geoip_city': geoip_city, 'upstream_status': upstream_status, 'bytes_sent': bytes_sent, 'connection': connection, 'server_port': server_port, 'http_referer': http_referer, 'uid_set': uid_set, 'time_local': time_local, 'upstream_addr': upstream_addr, 'uid_got': uid_got}


            r = requests.post(url, auth=awsauth, json=document, headers=headers)