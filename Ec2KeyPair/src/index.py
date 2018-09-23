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
from common import get_params
from common import get_parameter
from common import create_failure
from create import create_and_store_key_pair
from rotate import rotate_key_pair

log = logging.getLogger('Macro-Ec2KeyPair')
log.setLevel(logging.DEBUG)


def handler(event, context):
    log.debug(json.dumps(event, indent=2))

    params = get_params(event)
    operation = get_parameter(params, 'Operation', None)
    s3_bucket = get_parameter(params, 'S3Bucket', None)
    s3_key = get_parameter(params, 'S3Key', None)

    # Operation, S3Bucket and S3Key are always required!
    if operation == None or s3_bucket == None or s3_key == None:
        return create_failure(event)

    if operation == 'CREATE':
        return create_and_store_key_pair(event)
    elif operation == 'ROTATE':
        return rotate_key_pair(event)

    return create_failure(event)


