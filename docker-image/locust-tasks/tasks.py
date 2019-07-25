#!/usr/bin/env python

# Copyright 2015 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import uuid
import pprint
import sseclient
import time
import resource
resource.setrlimit(resource.RLIMIT_NOFILE, (10240, 9223372036854775807))

from datetime import datetime
from locust import HttpLocust, TaskSet, task
from locust.events import request_success, request_failure
class MetricsTaskSet(TaskSet):
    _deviceid = None


    def with_requests(self, url):
        """Get a streaming response for the given event feed using requests."""
        import requests
        
        try:
            r = requests.get(url, stream=True)
            return r
        except requests.exceptions.RequestException as e:
                    print(e)
                    request_failure.fire()
                    
        

    def on_start(self):
        url = 'http://localhost:3000/connect'
        start_at = time.time()
        response = self.with_requests(url)  # or with_requests(url)
        client = sseclient.SSEClient(response)
        
        for event in client.events():
            start_at_click = time.time()
            end_at = time.time()
            data = json.loads(event.data)
            pprint.pprint(data)
            
            if 'lc' in data:
                response_time = int((end_at - start_at) * 1000)
                request_success.fire(
                                     request_type='Connection Received',
                                     name='test/sse/connect',
                                     response_time=response_time,
                                     response_length=len(event.data),
                                     )
            elif 'ts' in data:
                response_time_click = int((float(data['ts']) - start_at_click * 1000) * 1000)
                request_success.fire(
                                      request_type='Click received',
                                      name='sse/clickEvent',
                                     response_time=response_time_click,
                                     response_length=len(event.data),)
## check for lc and set success


class StreamTask(TaskSet):

    def on_start(self):
        print("Starting")
        messages = SSEClient('http://localhost:3000/connect')
        for msg in messages:
            print(msg)
	


class MetricsLocust(HttpLocust):
    task_set = MetricsTaskSet
