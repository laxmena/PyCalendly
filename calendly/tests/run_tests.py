import copy
import json
import unittest
from unittest.mock import MagicMock, patch

from calendly.calendly import CalendlyAPI
from calendly.exceptions import CalendlyOauth2Exception, CalendlyException
from calendly.utils import constants
from calendly.utils.api import CalendlyReq
from calendly.utils.oauth2 import CalendlyOauth2

# Init test objects
mock_token = 'mock_token'
calendly_client = CalendlyAPI(mock_token)
calendly_request = CalendlyReq(mock_token)
calendly_client.request = calendly_request


class TestCalendlyExceptions(unittest.TestCase):

    def test_CalendlyException(self):
        message = "SOME MESSAGE"
        details = [{}, {}, {}]

        exception = CalendlyException(message, details)
        self.assertEqual(exception.message, message)
        self.assertEqual(exception.details, details)

        with self.assertRaises(CalendlyException):
            raise exception

    def test_CalendlyOauth2Exception(self):
        message = "SOME MESSAGE"
        details = [{}, {}, {}]

        exception = CalendlyOauth2Exception(message, details)
        self.assertEqual(exception.message, message)
        self.assertEqual(exception.details, details)

        with self.assertRaises(CalendlyOauth2Exception):
            raise exception

class TestCalendlyReq(unittest.TestCase):

    def test_constructor(self):
        pass

    def test__get_oauth2_error_from_response(self):
        pass

    def test__get_api_error_from_response(self):
        pass

    def test__get_error_type_and_description_from_response(self):
        pass

    def test_process_request(self):
        pass

    def test_get(self):
        pass

    def test_post(self):
        pass

    def test_delete(self):
        pass

    def test_put(self):
        pass


# Set HTTP mock response class
class MockResponse(object):
    def __init__(self, content, status_code, headers=None):
        if isinstance(content, bytes):
            self.content = content
        else:
            self.content = content.encode('utf-8')
        self.status_code = status_code
        self.headers = headers or {}

    @property
    def text(self):
        return self.content.decode('utf-8')

    def json(self):
        return json.loads(self.content)


# Test endpoints
class TestEndpoints(unittest.TestCase):
    def test_create_webhook(self):
        # Arrange
        calendly_request.post = MagicMock(return_value=MockResponse('{}', 200))

        mock_url = 'mock_url'
        mock_scope = 'mock_scope'
        mock_organization = 'mock_organization'
        mock_signing_key = 'mock_signing_key'

        expected_payload = {
            'url': mock_url,
            'organization': mock_organization,
            'scope': mock_scope,
            'signing_key': mock_signing_key,
            'events': ['invitee.canceled', 'invitee.created']
        }

        # Act
        calendly_client.create_webhook(url=mock_url, scope=mock_scope, organization=mock_organization,
                                       signing_key=mock_signing_key)

        # Assert
        calendly_request.post.assert_called_once()
        calendly_request.post.assert_called_with(f'{constants.WEBHOOK}', expected_payload)

    def test_delete_webhook(self):
        # Arrange
        calendly_request.get = MagicMock(return_value=MockResponse('{}', 204))

        mock_uuid = 'mock_uuid'

        # Act
        calendly_client.get_webhook(mock_uuid)

        # Assert
        calendly_request.get.assert_called_once()
        calendly_request.get.assert_called_with(f'{constants.WEBHOOK}/{mock_uuid}')

    def test_get_event_details(self):
        # Arrange
        with open('./calendly/tests/get_event_details_response.json', 'r') as file:
            calendly_request.get = MagicMock(return_value=MockResponse(file.read(), 200))

        mock_uuid = 'mock_uuid'

        # Act
        response = calendly_client.get_event_details(mock_uuid)

        # Assert
        calendly_request.get.assert_called_once()
        calendly_request.get.assert_called_with(f'{constants.EVENTS}/{mock_uuid}')
        self.assertEqual(response['resource']['uri'], 'https://api.calendly.com/scheduled_events/MOCK_URI')

    def test_list_event_types(self):
        # Arrange
        with open('./calendly/tests/list_event_types_response.json', 'r') as file:
            calendly_request.get = MagicMock(return_value=MockResponse(file.read(), 200))

        mock_uuid = 'mock_uuid'
        expected_payload = {
            'count': 20,
            'user': 'mock_uuid'
        }

        # Act
        response = calendly_client.list_event_types(user_uri=mock_uuid)

        # Assert
        calendly_request.get.assert_called_once()
        calendly_request.get.assert_called_with(f'{constants.EVENT_TYPE}', expected_payload)
        self.assertEqual(response['collection'][0]['uri'], 'https://api.calendly.com/event_types/MOCK_URI')

    def test_list_events(self):
        # Arrange
        with open('./calendly/tests/list_events_response.json', 'r') as file:
            calendly_request.get = MagicMock(return_value=MockResponse(file.read(), 200))

        mock_uuid = 'mock_uuid'
        expected_payload = {
            'count': 20,
            'user': 'mock_uuid'
        }

        # Act
        response = calendly_client.list_events(user_uri=mock_uuid)

        # Assert
        calendly_request.get.assert_called_once()
        calendly_request.get.assert_called_with(f'{constants.EVENTS}', expected_payload)
        self.assertEqual(response['collection'][0]['uri'], 'https://api.calendly.com/scheduled_events/MOCK_URI')


# Test endpoints
class TestLogicalFunctions(unittest.TestCase):
    def test_get_all_items_with_pagination(self):
        # Arrange
        first_uri = 'https://api.calendly.com/event_types/A'
        second_uri = 'https://api.calendly.com/event_types/B'
        next_page_uri = 'https://api.calendly.com/uri_to_next_page'

        first_page = '{"collection": [{"uri": "' + first_uri + '"}],"pagination": {"next_page": "' + next_page_uri + '"}}'
        second_page = '{"collection": [{"uri": "' + second_uri + '"}],"pagination": {"next_page": null}}'

        calendly_client.list_event_types = MagicMock(return_value=json.loads(first_page))
        calendly_client.list_events = MagicMock(return_value=json.loads(first_page))

        # Return next page only for the correct "next_page" uri
        def handle_get_request(uri):
            if uri == next_page_uri:
                return MockResponse(second_page, 200)
            return MockResponse('Not Found', 400)

        calendly_request.get = MagicMock(side_effect=handle_get_request)

        # Act (testing both get_all_event_types & get_all_scheduled_events)
        event_types = calendly_client.get_all_event_types('mock_user_uri')
        scheduled_events = calendly_client.get_all_scheduled_events('mock_user_uri')

        # Assert
        self.assertEqual(len(event_types), 2)
        self.assertEqual(event_types[0]['uri'], first_uri)
        self.assertEqual(event_types[1]['uri'], second_uri)

        self.assertEqual(len(scheduled_events), 2)
        self.assertEqual(scheduled_events[0]['uri'], first_uri)
        self.assertEqual(scheduled_events[1]['uri'], second_uri)

    def test_convert_event_to_original_url_match_on_first_page(self):
        # Arrange
        with open('./calendly/tests/get_event_details_response.json', 'r') as file:
            calendly_client.get_event_details = MagicMock(return_value=json.loads(file.read()))

        with open('./calendly/tests/list_event_types_response.json', 'r') as file:
            calendly_client.list_event_types = MagicMock(return_value=json.loads(file.read()))

        mock_event_uri = 'mock_event_uri'
        mock_user_uri = 'mock_user_uri'

        # Act
        original_url = calendly_client.convert_event_to_original_url(mock_event_uri, mock_user_uri)

        # Assert
        self.assertEqual(original_url, 'https://calendly.com/acmesales')

    def test_convert_event_to_original_url_paging_required(self):
        # Arrange
        mock_event_uri = 'mock_event_uri'
        mock_user_uri = 'mock_user_uri'
        next_page_uri = 'https://api.calendly.com/uri_to_next_page'

        with open('./calendly/tests/get_event_details_response.json', 'r') as file:
            content = file.read()
            calendly_client.get_event_details = MagicMock(
                side_effect=lambda x: json.loads(content) if x == mock_event_uri else None)

        with open('./calendly/tests/list_event_types_response.json', 'r') as file:
            # Result won't be found in first page
            mock_first_page = json.loads(file.read())
            mock_first_page['collection'][0]['uri'] = 'NOT_THE_URI_WE_WERE_LOOKING_FOR'
            mock_first_page['pagination']['next_page'] = next_page_uri

            # Result will be found only on second page   
            mock_second_page = copy.deepcopy(mock_first_page)
            mock_second_page['collection'][0]['uri'] = 'https://api.calendly.com/event_types/MOCK_URI'
            mock_second_page['pagination']['next_page'] = 'null'

            calendly_client.list_event_types = MagicMock(return_value=mock_first_page)

            # Return next page only for the correct "next_page" uri
            def handle_get_request(uri):
                if uri == next_page_uri:
                    return MockResponse(json.dumps(mock_second_page), 200)
                return MockResponse('Not Found', 400)

            calendly_request.get = MagicMock(side_effect=handle_get_request)

        # Act
        original_url = calendly_client.convert_event_to_original_url(mock_event_uri, mock_user_uri)

        # Assert
        self.assertEqual(original_url, 'https://calendly.com/acmesales')


class TestCalendlyOauth2(unittest.TestCase):
    client_id = "ClientID123"
    client_secret = "Secret123"
    redirect_uri = "https://redirect.url"
    response_type = "response_type"

    def test_constructor(self):
        oauth2 = CalendlyOauth2(self.client_id, self.client_secret)

        self.assertEqual(oauth2.client_id, self.client_id)
        self.assertEqual(oauth2.client_secret, self.client_secret)

    def test_constructor_passing_redirect_uri(self):
        oauth2 = CalendlyOauth2(self.client_id, self.client_secret, redirect_uri=self.redirect_uri)

        self.assertEqual(oauth2.client_id, self.client_id)
        self.assertEqual(oauth2.client_secret, self.client_secret)
        self.assertEqual(oauth2.redirect_uri, self.redirect_uri)

    def test_constructor_passing_response_type(self):
        oauth2 = CalendlyOauth2(self.client_id, self.client_secret)
        self.assertEqual(oauth2.response_type, "code")

        oauth2 = CalendlyOauth2(self.client_id, self.client_secret, response_type=self.response_type)
        self.assertEqual(oauth2.response_type, self.response_type)

    def test_authorization_url(self):
        expected_url = f"{constants.OAUTH_AUTHORIZE_URL}?" \
                       f"client_id={self.client_id}&response_type=code&redirect_uri={self.redirect_uri}"

        oauth2 = CalendlyOauth2(
            self.client_id,
            self.client_secret
        )

        # redirect uri not provided
        with self.assertRaises(CalendlyOauth2Exception):
            _ = oauth2.authorization_url

        oauth2 = CalendlyOauth2(
            self.client_id,
            self.client_secret,
            redirect_uri=self.redirect_uri
        )

        self.assertEqual(oauth2.authorization_url, expected_url)

    def test_authorization_url_passing_response_type(self):
        expected_url = f"{constants.OAUTH_AUTHORIZE_URL}?" \
                       f"client_id={self.client_id}&response_type={self.response_type}&redirect_uri={self.redirect_uri}"

        oauth2 = CalendlyOauth2(
            self.client_id,
            self.client_secret,
            redirect_uri=self.redirect_uri,
            response_type=self.response_type
        )

        self.assertEqual(oauth2.authorization_url, expected_url)

    @patch("calendly.utils.oauth2.CalendlyReq.post")
    def test_send_post(self, post_mock):
        print("PASSING")
        args = (1,2,3)
        kwargs = {"some": "parameters"}
        response_mock = MockResponse('{}', 200)
        post_mock.return_value = response_mock

        oauth2 = CalendlyOauth2(self.client_id, self.client_secret)

        returned_response = oauth2.send_post(*args, **kwargs)
        self.assertEqual(response_mock, returned_response)
        post_mock.assert_called_with(*args, **kwargs)

        post_mock.reset_mock()
        post_mock.side_effect = CalendlyException()

        with self.assertRaises(CalendlyOauth2Exception):
            oauth2.send_post(*args, **kwargs)
        post_mock.assert_called_with(*args, **kwargs)

    @patch("calendly.utils.oauth2.CalendlyOauth2.send_post")
    def test_get_access_token(self, send_post_mock):
        code = "code123"
        expected_token_data = {"TOKEN": "DATA"}
        response_mock = MockResponse(json.dumps(expected_token_data), 200)

        send_post_mock.return_value = response_mock

        oauth2 = CalendlyOauth2(
            self.client_id,
            self.client_secret
        )

        # redirect url not provided
        with self.assertRaises(CalendlyOauth2Exception):
            oauth2.get_access_token(code)

        oauth2 = CalendlyOauth2(
            self.client_id,
            self.client_secret,
            redirect_uri=self.redirect_uri
        )

        expected_data = dict(
            grant_type="authorization_code",
            client_id=self.client_id,
            client_secret=self.client_secret,
            code=code,
            redirect_uri=self.redirect_uri
        )

        token_data = oauth2.get_access_token(code)
        self.assertDictEqual(token_data, expected_token_data)
        send_post_mock.assert_called_with(constants.OAUTH_TOKEN_URL, expected_data)

    @patch("calendly.utils.oauth2.CalendlyOauth2.send_post")
    def test_get_access_token_passing_grant_type(self, send_post_mock):
        code = "code123"
        grant_type = "TYPE"
        expected_token_data = {"TOKEN": "DATA"}
        response_mock = MockResponse(json.dumps(expected_token_data), 200)

        send_post_mock.return_value = response_mock

        oauth2 = CalendlyOauth2(
            self.client_id,
            self.client_secret,
            redirect_uri=self.redirect_uri
        )

        expected_data = dict(
            grant_type=grant_type,
            client_id=self.client_id,
            client_secret=self.client_secret,
            code=code,
            redirect_uri=self.redirect_uri
        )

        token_data = oauth2.get_access_token(code, grant_type)
        self.assertDictEqual(token_data, expected_token_data)
        send_post_mock.assert_called_with(constants.OAUTH_TOKEN_URL, expected_data)

    @patch("calendly.utils.oauth2.CalendlyOauth2.send_post")
    def test_revoke_access_token(self, send_post_mock):
        token = "TOKEN123"
        expected_token_data = {"TOKEN": "DATA"}
        response_mock = MockResponse(json.dumps(expected_token_data), 200)
        expected_data = dict(client_id=self.client_id, client_secret=self.client_secret, token=token)
        send_post_mock.return_value = response_mock

        oauth2 = CalendlyOauth2(
            self.client_id,
            self.client_secret,
            redirect_uri=self.redirect_uri
        )

        oauth2.revoke_access_token(token)
        send_post_mock.assert_called_with(constants.OAUTH_REVOKE_URL, expected_data)

    @patch("calendly.utils.oauth2.CalendlyOauth2.send_post")
    def test_refresh_access_token(self, send_post_mock):
        refresh_token = "TOKEN123"
        expected_token_data = {"TOKEN": "DATA"}
        response_mock = MockResponse(json.dumps(expected_token_data), 200)

        expected_data = dict(
            grant_type="refresh_token",
            client_id=self.client_id,
            client_secret=self.client_secret,
            refresh_token=refresh_token
        )

        send_post_mock.return_value = response_mock

        oauth2 = CalendlyOauth2(
            self.client_id,
            self.client_secret,
            redirect_uri=self.redirect_uri
        )

        oauth2.refresh_access_token(refresh_token)
        send_post_mock.assert_called_with(constants.OAUTH_TOKEN_URL, expected_data)

    @patch("calendly.utils.oauth2.CalendlyOauth2.send_post")
    def test_refresh_access_token_passing_grant_type(self, send_post_mock):
        grant_type = "grant_type"
        refresh_token = "TOKEN123"
        expected_token_data = {"TOKEN": "DATA"}
        response_mock = MockResponse(json.dumps(expected_token_data), 200)

        expected_data = dict(
            grant_type=grant_type,
            client_id=self.client_id,
            client_secret=self.client_secret,
            refresh_token=refresh_token
        )

        send_post_mock.return_value = response_mock

        oauth2 = CalendlyOauth2(
            self.client_id,
            self.client_secret,
            redirect_uri=self.redirect_uri
        )

        oauth2.refresh_access_token(refresh_token, grant_type)
        send_post_mock.assert_called_with(constants.OAUTH_TOKEN_URL, expected_data)

    @patch("calendly.utils.oauth2.CalendlyOauth2.send_post")
    def test_introspect_access_token(self, send_post_mock):
        token = "TOKEN123"
        expected_token_data = {"TOKEN": "DATA"}
        response_mock = MockResponse(json.dumps(expected_token_data), 200)

        expected_data = dict(
            client_id=self.client_id,
            client_secret=self.client_secret,
            token=token
        )

        send_post_mock.return_value = response_mock

        oauth2 = CalendlyOauth2(
            self.client_id,
            self.client_secret,
            redirect_uri=self.redirect_uri
        )

        oauth2.introspect_access_token(token)
        send_post_mock.assert_called_with(constants.OAUTH_INTROSPECT_URL, expected_data)


if __name__ == '__main__':
    unittest.main()
