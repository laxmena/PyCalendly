import requests
import json

__author__ = "laxmena <ConnectWith@laxmena.com>"
__license__ = "MIT"


class CalendlyException(Exception):
    """Errors corresponding to a misuse of Calendly API"""


class CalendlyReq(object):
    """
    Private class wrapping the Calendly API v2. Decodes responses from Calendly and returns it

    References
    ----------
    https://calendly.stoplight.io/docs/api-docs/
    """

    def __init__(self, token):
        """
        Constructor. Uses Bearer Token Authentication.

        Parameters
        ----------
        token : str 
            Personal Access Token
        """
        self.headers = {'authorization': 'Bearer ' + token}

    def process_request(self, method, url, data=None):
        """
        Make requests to Calendly API by appending requried headers. 

        Parameters
        ----------
        method : str
            supported methods - get, post, delete, put
        url : str
            Calendly API URL
        data : dict, optional
            additional data to be passed to the API 
        """
        request_method = getattr(requests, method)
        return request_method(url, json=data, headers=self.headers)

    def get(self, url, data=None):
        """
        Send GET request to the Calendly URL.

        Parameters
        ----------
        url : str
            Calendly API URL
        data : dict, optional
            additional data to be passed to the API 
        """
        return self.process_request('get', url, data)

    def post(self, url, data=None):
        """
        Send POST request to the Calendly URL.

        Parameters
        ----------
        url : str
            Calendly API URL
        data : dict, optional
            additional data to be passed to the API 
        """
        return self.process_request('post', url, data)

    def delete(self, url, data=None):
        """
        Send DELETE request to the Calendly URL.

        Parameters
        ----------
        url : str
            Calendly API URL
        data : dict, optional
            additional data to be passed to the API 
        """
        return self.process_request('delete', url, data)

    def put(self, url, data=None):
        """
        Send PUT request to the Calendly URL.

        Parameters
        ----------
        url : str
            Calendly API URL
        data : dict, optional
            additional data to be passed to the API 
        """        
        return self.process_request('put', url, data)
