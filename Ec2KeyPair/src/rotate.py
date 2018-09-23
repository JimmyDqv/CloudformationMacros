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
from common import create_failure
from create import create_and_store_key_pair
from delete import delete_key_pair


log = logging.getLogger('Macro-Ec2KeyPair-Rotate')
log.setLevel(logging.DEBUG)


def rotate_key_pair(event):
    log.debug(json.dumps(event, indent=2))
    params = get_params(event)
    key_name = get_parameter(params, 'Keyname', None)

    # Keyname is required.
    if key_name == None:
        return create_failure(event)
    
    delete_key_pair(event)
    return create_and_store_key_pair(event)
