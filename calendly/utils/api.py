from typing import MutableMapping
from calendly.exceptions import CalendlyOauth2Exception
import requests

__author__ = "laxmena <ConnectWith@laxmena.com>"
__license__ = "MIT"


class CalendlyReq(object):
    """
    Private class wrapping the Calendly API v2. Decodes responses from Calendly and returns it

    References
    ----------
    https://calendly.stoplight.io/docs/api-docs/
    """

    ERROR_TYPE_KEY = 'error'
    ERROR_DESCRIPTION_KEY = 'error_description'

    def __init__(self, token: str=None, headers: dict=None):
        """
        Constructor: Uses Bearer Token Authentication or custom headers.

        Parameters
        ----------
        token : str 
        headers : str
            Personal Access Token
        """

        if token and headers:
            raise CalendlyException("You can't pass both token and headers at the same time.")

        if token:
            headers = {'authorization': 'Bearer ' + token}

        self.headers = headers

    def _get_error_type_and_description_from_response(self, response):
        try:
            resp = response.json()
            return resp[self.ERROR_TYPE_KEY], resp[self.ERROR_DESCRIPTION_KEY]
        except (AttributeError, KeyError):
            return "error", "Unknown Error."

    def process_request(self, method: str, url: str, data: MutableMapping=None) -> requests.Response:
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
        kwargs = dict(json=data)

        if self.headers:
            kwargs.update(dict(headers=self.headers))

        response = request_method(url, **kwargs)

        if response.status_code > requests.codes.permanent_redirect:
            error_type, error_description = self._get_error_type_and_description_from_response(response)
            raise CalendlyException(f"{error_type}: {error_description}")

        return response

    def get(self, url: str, data: MutableMapping=None) -> requests.Response:
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

    def post(self, url: str, data: MutableMapping=None) -> requests.Response:
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

    def delete(self, url: str, data: MutableMapping=None) -> requests.Response:
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

    def put(self, url: str, data: MutableMapping=None) -> requests.Response:
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