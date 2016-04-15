"""
CS1951A Final Project
Brown University
Spring 2016

Vann, Steffani, JJ, Chaitu

Scrapers
"""

import requests


class CustomRequest(object):
    read_timeout = 10.0
    connect_timeout = 10.0

    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers

        # setup session
        self.session = requests.Session()
        self.session.mount("http://", requests.adapters.HTTPAdapter
                           (max_retries=3))
        self.session.mount("https://", requests.adapters.HTTPAdapter
                           (max_retries=3))

    def get_request(self, modifier="", params={}):
        try:
            response = self.session.get(self.base_url+modifier,
                                        params=params,
                                        headers=self.headers,
                                        timeout=(self.connect_timeout,
                                                 self.read_timeout))
        except requests.exceptions.ConnectTimeout as c:
            print "Waited too long to connect:", c.message
        except requests.exceptions.ReadTimeout as r:
            print "Waited too long between bytes:", r.message

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as h:
            print "HTTPError:", h.message

        return response
