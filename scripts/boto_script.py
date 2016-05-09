#!/usr/bin/python

import boto
import time
import sys
import os

from boto.ec2.connection import EC2Connection
from boto.ec2.regioninfo import RegionInfo

import boto.s3.connection

region = RegionInfo(name="melbourne", endpoint="nova.rc.nectar.org.au")
connection = boto.connect_ec2(aws_access_key_id="adf938e8df4841129a5ca7089ab6b0ee",
                    aws_secret_access_key="66f187d931f04af5805e899421bbfbef",
                    is_secure=True,
                    region=region,
                    validate_certs=False,
                    port=8773,
                    path="/services/Cloud")

# get the image ami
images = connection.get_all_images()
for idx,img in enumerate(images):
    if img.name.find("CentOS")>0:
        print ("id:%s name:%s" % (img.id,img.name))

reservations = connection.get_all_instances()
for idx,res in enumerate(reservations):
    print ("id:%s instances:%s" % (res.id,res.instances))



# Create instance here
# try:
#     res = connection.run_instances('ami-00003801',key_name='ubuntu',security_groups=['default','open'],instance_type='m1.medium',placement='melbourne-qh2')
#     instance = res.instances[0]
# except Exception as e:
#     if e.status == 413:
#         print ("Quota exceeded the limitation, please try to release some resources for instance" )
#         sys.exit(1)
# else:
#     while instance.update() != "running":
#         print("wait for the instance running") 
#         time.sleep(5)  # Run this in a green thread, ideally
#     print instance.ip_address
#     f = open('IP.txt','w')
#     f.write("[web]\n")
#     f.write(instance.ip_address+"\n")
#     f.close()

connection = boto.s3.connection.S3Connection(
          aws_access_key_id='adf938e8df4841129a5ca7089ab6b0ee',
          aws_secret_access_key='66f187d931f04af5805e899421bbfbef',
          port=8888,
          host='swift.rc.nectar.org.au',
          is_secure=True,
          validate_certs=False,
          calling_format=boto.s3.connection.OrdinaryCallingFormat()
        )

# buckets = connection.get_all_buckets()

container_name = "twitter_container"
try :
    b = connection.create_bucket(container_name)
except boto.exception.S3CreateError as e:
    if e.status == 409:
        print ("already exists the container: %s" % (container_name))
        pass 
except:
    print "Unexpected error:", sys.exc_info()[0]

b = connection.get_bucket('twitter_container', validate=False)
print b.name
