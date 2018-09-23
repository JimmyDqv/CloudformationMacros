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

log = logging.getLogger('Macro-Ec2KeyPair-Create')
log.setLevel(logging.DEBUG)

ec2_client = boto3.client('ec2')
s3_client = boto3.client('s3')

def create_and_store_key_pair(event):
    log.debug(json.dumps(event, indent=2))

    fragment = event['fragment']
    params = get_params(event)
    s3_bucket = get_parameter(params, 'S3Bucket', None)
    s3_key = get_parameter(params, 'S3Key', None)
    key_name = get_parameter(params, 'Keyname', None)
    
    if key_name == None:
        key_name = generate_name(20)

    if not does_key_pair_exists(key_name):
        response = ec2_client.create_key_pair(
            KeyName=key_name
        )
        store_key_material(response, s3_bucket, s3_key)

    fragment = key_name

    return {
        'requestId' : event['requestId'], 
        'status' : 'success', 
        'fragment' : fragment
    }


def store_key_material(create_response, s3_bucket, s3_key):
    key_material = create_response['KeyMaterial']

    s3_client.put_object(
        Bucket=s3_bucket,
        Key=s3_key,
        Body=key_material
    )


def does_key_pair_exists(name):
    try:
        ec2_client.describe_key_pairs(
            KeyNames=[
                name
            ]
        )

        return True
    except Exception as e:
        return False
    else:
        return False


def generate_name(size=12):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))
