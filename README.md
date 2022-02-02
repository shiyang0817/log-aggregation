# lambda get sub dir from s3 bucket
```
import boto3
s3_r = boto3.resource('s3')
bucket_tmp = s3_r.Bucket('log-jan')
for o in bucket_tmp.objects.filter(Delimiter='/'):
    print("o.key: ", o.key)
```
>only the sub-dir that has object updates will be scanned and filtered. the sub-dir that does not have object updates will not be scanned and filtered.
