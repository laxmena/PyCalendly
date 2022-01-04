from calendly.calendly import CalendlyReq, CalendlyAPI
from calendly.utils import constants
from unittest.mock import MagicMock
import unittest
import json
import copy

# Init test objects
mock_token = 'mock_token'
calendly_client = CalendlyAPI(mock_token)
calendly_request = CalendlyReq(mock_token)
calendly_client.request = calendly_request

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
        calendly_client.create_webhook(url=mock_url, scope=mock_scope, organization=mock_organization, signing_key=mock_signing_key)

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

        first_page = '{"collection": [{"uri": "'+first_uri+'"}],"pagination": {"next_page": "'+next_page_uri+'"}}'
        second_page = '{"collection": [{"uri": "'+second_uri+'"}],"pagination": {"next_page": null}}'

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
            calendly_client.get_event_details = MagicMock(side_effect=lambda x: json.loads(content) if x == mock_event_uri else None)
        
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

if __name__ == '__main__':
    unittest.main()