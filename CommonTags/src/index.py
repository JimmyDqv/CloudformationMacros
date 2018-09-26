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

log = logging.getLogger('Macro-CommonTags')
log.setLevel(logging.DEBUG)

# Load data about resources supporting tags.
# Do it outside of the handler to enable resuse.
RESOURCES_SUPPORTING_TAGS = []
with open('resources_supporting_tags.json') as f:
    RESOURCES_SUPPORTING_TAGS = json.load(f)


def handler(event, context):
    log.debug(json.dumps(event, indent=2))

    tags = get_parameters(event)
    if not tags:
        return create_failure(event)

    resources = get_resources(event)
    if resources == None:
        return create_failure(event)

    tag_resources(resources, tags)

    return {
        'requestId': event['requestId'],
        'status': 'success',
        'fragment': event['fragment']
    }


def tag_resources(resources, tags):
    for resource_key in resources:
        add_tags_to_resource(resources[resource_key], tags)


def add_tags_to_resource(resource, tags):
    if does_resource_support_tags(resource):
        resource_tags = resource['Properties'].get('Tags', [])
        for tag in tags:
            if not is_tag_already_specified(tag, resource_tags):
                tag_object = {
                    'Key': tag,
                    'Value': tags[tag]
                }
                resource_tags.append(tag_object)
        resource['Properties']['Tags'] = resource_tags


def is_tag_already_specified(tag, resource_tags):
    for tag_object in resource_tags:
        if tag_object['Key'] == tag:
            return True
    return False


# Check if a resource support Tags, since not all resources does that.
def does_resource_support_tags(resource):
    if 'Tags' in resource['Properties']:
        return True

    if resource['Type'] in RESOURCES_SUPPORTING_TAGS:
        return True

    return False


def get_parameters(event):
    if 'params' in event:
        return event['params']
    return {}


def get_resources(event):
    if 'Resources' in event['fragment']:
        return event['fragment']['Resources']
    return None


def create_failure(event):
    return {
        'requestId': event['requestId'],
        'status': 'failed',
        'fragment': event['fragment']
    }
