import json
import logging

import requests


logger = logging.getLogger(__name__)


class MockServerClient(object):
    DEFAULT_RESPONSE_HEADERS = [
        {"name": "Content-Type", "values": ["application/json; charset=utf-8"]},
        {"name": "Cache-Control", "values": ["no-cache, no-store"]}
    ]

    def __init__(self, url):
        self.url = url

    def _put(self, endpoint, json=None):
        response = requests.put(
            self.url + endpoint,
            json=json,
        )
        return response

    def create_response_matcher(self, path):
        return {
            'method': "",
            'path': path,
            'body': "",
            'headers': [],
            'cookies': [],
            'queryStringParameters': []
        }

    def create_expectation(self, path, responseBody, statusCode):
        return {
            'httpRequest': self.create_response_matcher(path),
            'httpResponse': {
                'statusCode': statusCode or 200,
                'body': json.dumps(responseBody),
                'cookies': [],
                'headers': self.DEFAULT_RESPONSE_HEADERS,
                'delay': {
                    'timeUnit': "MICROSECONDS",
                    'value': 0
                }
            },
            'times': {
                'remainingTimes': 1,
                'unlimited': False
            }
        }

    def mock_any_response(self, expectation):
        """Setup an expectation in the MockServer by specifying an expectation object.

        For example:
           mockServerClient("localhost", 1080).mockAnyResponse(
               {
                   'httpRequest': {
                       'path': '/somePath',
                       'body': {
                           'type': "STRING",
                           'value': 'someBody'
                       }
                   },
                   'httpResponse': {
                       'statusCode': 200,
                       'body': Base64.encode(JSON.stringify({ name: 'first_body' })),
                       'delay': {
                           'timeUnit': 'MILLISECONDS',
                           'value': 250
                       }
                   },
                   'times': {
                       'remainingTimes': 1,
                       'unlimited': false
                   }
               }
           );

        Args:
            expectation the expectation to setup on the MockServer
        """
        return self._put("/expectation", expectation)

    def mock_simple_response(self, path, responseBody, statusCode):
        """Setup an expectation in the MockServer without having to specify the full
        expectation object.

        for example:
            mockServerClient("localhost", 1080).mockSimpleResponse(
                '/somePath', { name: 'value' }, 203);

        Args:
             path: the path to match requests against
             responseBody: the response body to return if a request matches
             statusCode: the response code to return if a request matches
        """
        return self.mock_any_response(self.create_expectation(path, responseBody, statusCode))

    def verify(self, request, count=None, exact=None):
        """Verify a request has been sent.

        For example:

           expect(client.verify(
               request={
                   'method': 'POST',
                   'path': '/somePath'
               }
           )).toBeTruthy();

        Args:
            request: the http request that must be matched for this verification to pass
            count: the number of times this request must be matched
            exact: true if the count is matched as "equal to" or false if the count
                is matched as "greater than or equal to"
        """
        count = 1 if count is None else count
        resp = self._put("/verify", {
            "httpRequest": request,
            "times": {
                "count": count,
                "exact": exact
            }})
        if resp.status_code == 202:
            return self
        else:
            logger.error(resp.content)
            raise Exception('Failed to verify')

    def reset(self):
        """Reset MockServer by clearing all expectations"""
        return self._put("/reset")
