# The MIT License (MIT)
#
# Copyright (C) 2018 Jimmy Dahlqvist
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy,
# modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software
# is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
# IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import json
import logging
import string
import random
import boto3
from common import get_params
from common import get_parameter

log = logging.getLogger('Macro-Ec2KeyPair-Delete')
log.setLevel(logging.DEBUG)

ec2_client = boto3.client('ec2')
s3_client = boto3.client('s3')

def delete_key_pair(event):
    log.debug(json.dumps(event, indent=2))

    params = get_params(event)
    s3_bucket = get_parameter(params, 'S3Bucket', None)
    s3_key = get_parameter(params, 'S3Key', None)
    key_name = get_parameter(params, 'Keyname', None)

    log.debug('Delete EC2 key pair:')
    response = ec2_client.delete_key_pair(
        KeyName=key_name
    )
    log.debug(json.dumps(response, indent=2))

    log.debug('Delete S3 pem file')
    response = s3_client.delete_object(
        Bucket=s3_bucket,
        Key=s3_key
    )
    log.debug(json.dumps(response, indent=2))