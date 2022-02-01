# lambda get sub dir from s3 bucket
```
import boto3
s3_r = boto3.resource('s3')
bucket_tmp = s3_r.Bucket('log-jan')
for o in bucket_tmp.objects.filter(Delimiter='/'):
    print("o.key: ", o.key)
```
