from .api import CalendlyReq
from .constants import OAUTH_AUTHORIZE_URL, OAUTH_TOKEN_URL, OAUTH_REVOKE_URL, OAUTH_INTROSPECT_URL
from calendly.exceptions import CalendlyOauth2Exception

__author__ = "luis <luiscastillocr@gmail.com>"
__license__ = "MIT"

REDIRECT_URI_EXCEPTION_TEXT = "You must pass the redirect_uri in the CalendlyOauth2 instantiation."

class CalendlyOauth2(object):
    """
    Private class wrapping the Calendly Oauth2 Api

    References
    ----------
    https://developer.calendly.com/how-to-authenticate-with-oauth

    """

    client_id = None
    client_secret = None
    redirect_uri = None
    response_type = None

    def __init__(self, client_id: str, client_secret: str, redirect_uri: str=None, response_type: str=None):
        """
        Constructor. client_id, client_secret, optionally you can pass the redirect_uri and response type

        Parameters
        ----------
        client_id : str
        client_secret : str
        redirect_uri : str
        response_type : str
        """
        self.request = CalendlyReq()
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.response_type = response_type or "code"

    @property
    def authorization_url(self):
        if not self.redirect_uri:
            raise CalendlyOauth2Exception(REDIRECT_URI_EXCEPTION_TEXT)

        return f"{OAUTH_AUTHORIZE_URL}?client_id={self.client_id}&response_type={self.response_type}&redirect_uri={self.redirect_uri}"

    def get_access_token(self, code: str, grant_type: str=None):

        if not self.redirect_uri:
            raise CalendlyOauth2Exception(REDIRECT_URI_EXCEPTION_TEXT)

        data = dict(
            grant_type=grant_type or "authorization_code",
            client_id=self.client_id,
            client_secret=self.client_secret,
            code=code,
            redirect_uri=self.redirect_uri
        )

        response = self.request.post(OAUTH_TOKEN_URL, data)
        return response.json()

    def revoke_access_token(self, token: str):
        data = dict(
            client_id=self.client_id,
            client_secret=self.client_secret,
            token=token
        )

        response = self.request.post(OAUTH_REVOKE_URL, data)
        return response.json()

    def refresh_access_token(self, refresh_token: str, grant_type: str=None):
        data = dict(
            grant_type=grant_type or "refresh_token",
            client_id=self.client_id,
            client_secret=self.client_secret,
            refresh_token=refresh_token
        )

        response = self.request.post(OAUTH_TOKEN_URL, data)
        return response.json()

    def introspect_access_token(self, token: str):
        data = dict(
            client_id=self.client_id,
            client_secret=self.client_secret,
            token=token
        )

        response = self.request.post(OAUTH_INTROSPECT_URL, data)
        return response.json()


