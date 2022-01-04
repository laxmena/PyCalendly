from calendly.utils.constants import WEBHOOK, EVENTS, ME, EVENT_TYPE
from calendly.utils.requests import CalendlyReq, CalendlyException
from typing import List, MutableMapping
import json 

class CalendlyAPI(object):

    event_types_def = {
        "canceled": "invitee.canceled",
        "created": "invitee.created"
    }

    def __init__(self, token: str):
        """
        Constructor. Uses Bearer Token for Authentication.

        Parameters
        ----------
        token : str 
            Personal Access Token
        """
        self.request = CalendlyReq(token)

    def create_webhook(self, url: str, scope: str, organization: str, signing_key: str=None, user: str=None, event_types: List[str]=["canceled", "created"]) -> MutableMapping:
        """
        Create a Webhook Subscription

        Args:
            url (str): Webhook URL
            scope (str): Either "organization" or "user"
            organization (str): Unique reference to the organization that the webhook will be tied to
            user (str, optional): If scope is set to "user", then user reference is required.
            event_types (list, optional): List of user events to subscribe to. Defaults to ["canceled", "created"].

        Returns:
            response: dict
                json-decoded response from Calendly API 
        """
        events = [self.event_types_def[event_type]
                  for event_type in event_types]
        data = {'url': url,
                'events': events,
                'organization': organization,
                'scope': scope,
                'signing_key': signing_key}

        if (scope == 'user'):
            if (user == None):
                raise CalendlyException
            data['user'] = user

        response = self.request.post(WEBHOOK, data)
        return response.json()

    def list_webhooks(self, organization: str, scope: str, user: str=None, count: int=20, sort: str=None) -> List[MutableMapping]:
        """ 
        Get a List of Webhook subscriptions for an Organization or User with a UUID.
        Reference:
        https://calendly.stoplight.io/docs/api-docs/reference/calendly-api/openapi.yaml/paths/~1webhook_subscriptions/get

        Args:
            organization (str): Unique reference to the organization that the webhook will be tied to
            scope (str): Either "organization" or "user"
            count (int, optional): Number of rows to return. Defaults to 20.
            sort (str, optional): Order results by specific field and direction. Defaults to None.
                Accepts comma-seperated list of {field}:{direction} values.
                Supported fields are: created_at, Sort direction is specified as: asc, desc
            user (str, optional): If scope is set to "user", then user reference is required.

        Raises:
            CalendlyException: [description]

        Returns:
            dict: Json decoded response for Get Webhook request.
        """
        data = {'organization': organization,
                'scope': scope,
                'count': count}

        if (sort != None):
            data['sort'] = sort

        if (scope == 'user'):
            if (user == None):
                raise CalendlyException
            data['user'] = user

        response = self.request.get(WEBHOOK, data)
        return response.json()

    def delete_webhook(self, id: str) -> MutableMapping:
        """
        Delete a Webhook subscription for an Organization or User with a specified UUID.

        Args:
            id (str): Webhook UUID

        Returns:
            dict: Calenderly API response for delete webhook action.
        """
        dict_response = {'success': True}
        response = self.request.delete(f'{WEBHOOK}/{id}')
        dict_response['success'] = response.status_code == 200
        try:
            json_response = response.json()
        except json.JSONDecodeError:
            json_response = {}
        dict_response.update(json_response)
        return dict_response

    def get_webhook(self, uuid: str) -> MutableMapping:
        """
        Get a Webhook Subscription for an Organization or User with specified UUID.

        Args:
            uuid (str): Webhook uuid

        Returns:
            dict: Json decoded response from Calenderly API for Get webhook action.
        """
        response = self.request.get(f'{WEBHOOK}/{uuid}')
        return response.json()

    def about(self) -> MutableMapping:
        """
        Returns basic information about the user account.

        Returns:
            dict: Json decoded response about the basic information about the user.
        """
        response = self.request.get(ME)
        return response.json()

    def list_event_types(self, count: int=20, organization: str=None, page_token: str=None, sort: str=None, user_uri: str=None) -> List[MutableMapping]:
        """
        Returns all Event Types associated with a specified user.

        Args:
            count (str, optional): Number of rows to return. Defaults to "20".
            organization (str, optional): View available personal, team and organization events type assosicated with the organization's URI. Defaults to None.
            page_token (str, optional): Toke to pass the next portion of the collection. Defaults to None.
            sort (str, optional): Order results by specified field and direction. Defaults to None.
            user_uri (str, optional): user's URI. Defaults to None.

        Returns:
            dict: json decoded response with list of event types
        """
        data = {"count": count}
        if (organization):
            data['organization'] = organization
        if (page_token):
            data['page_token'] = page_token
        if (sort):
            data['sort'] = sort
        if (user_uri):
            data['user'] = user_uri
        response = self.request.get(EVENT_TYPE, data)
        return response.json()

    def get_event_type(self, uuid: str) -> MutableMapping:
        """Returns event type associated with the specified UUID

        Args:
            uuid (str): Event UUID

        Returns:
            dict: json decoded response with information about the event
        """
        data = {"uuid": uuid}
        response = self.request.get(f'{EVENT_TYPE}/' + uuid, data)
        return response.json()

    def list_events(self, count: int=20, organization: str=None, sort: str=None, user_uri: str=None, status: str=None) -> List[MutableMapping]:
        """
        Returns a List of Events

        Args:
            count (str, optional): Number of rows to return. Defaults to "20".
            organization (str, optional): Organization URI. Defaults to None.
            sort (str, optional): comma seperated list of {field}:{direction} values. Defaults to None.
            user_uri (str, optional): User URI. Defaults to None.
            status (str, optional): 'active' or 'canceled'. Defaults to None.

        Returns:
            dict: json decoded response of list of events.
        """
        data = {'count': count}
        if (organization):
            data['organization'] = organization
        if (sort):
            data['sort'] = sort
        if (user_uri):
            data['user'] = user_uri
        if (status):
            data['status'] = status
        response = self.request.get(EVENTS, data)
        return response.json()

    def get_event_invitee(self, event_uuid: str, invitee_uuid: str) -> MutableMapping:
        """
        Returns information about an invitee associated with a URI

        Args:
            event_uuid (str): Event's unique identifier
            invitee_uuid (str): Invitee's unique identifier

        Returns:
            dict: json decoded response about invitee information
        """
        url = f'{EVENTS}/' + event_uuid + '/invitees/' + invitee_uuid
        response = self.request.get(url)
        return response.json()

    def get_event_details(self, uuid: str) -> MutableMapping:
        """
        Get information about an Event associated with a URI.

        Args:
            uuid (str): Event's unique identifier

        Returns:
            dict: json decoded response
        """
        url = f'{EVENTS}/' + uuid
        response = self.request.get(url)
        return response.json()

    def list_event_invitees(self, uuid: str) -> List[MutableMapping]:
        """
        Returns a list of Invitees for an Event.

        Args:
            uuid (str): Event's unique identifier.

        Returns:
            dict: json decoded response
        """
        url = f'{EVENTS}/' + uuid + '/invitees'
        response = self.request.get(url)
        return response.json()

    def get_all_event_types(self, user_uri: str) -> List[str]:
        """
        Get all event types by recursively crawling on all result pages.

        Args:
            user_uri (str, optional): User URI.

        Returns:
            list: json event type objects
        """
        first = self.list_event_types(user_uri=user_uri, count=100)
        next_page = first['pagination']['next_page']
        
        data = first['collection']

        while (next_page):
            page = self.request.get(next_page).json()
            data += page['collection']
            next_page = page['pagination']['next_page']
        
        return data

    def get_all_scheduled_events(self, user_uri: str) -> List[str]:
        """
        Get all scheduled events by recursively crawling on all result pages.

        Args:
            user_uri (str, optional): User URI.

        Returns:
            list: json scheduled event objects
        """
        first = self.list_events(user_uri=user_uri, count=100)
        next_page = first['pagination']['next_page']
        
        data = first['collection']

        while (next_page):
            page = self.request.get(next_page).json()
            data += page['collection']
            next_page = page['pagination']['next_page']
        
        return data

    def convert_event_to_original_url(self, event_uri: str, user_uri: str) -> str:
        """
        Convert event url from calendly's inner API convention to the original public url of the event.

        Args:
            event_uri (str): Event URI.
            user_uri (str, optional): User URI.

        Returns:
            string: the public convention of the event's url
        """
        event_type_uri = self.get_event_details(event_uri)['resource']['event_type']
        page = self.list_event_types(user_uri=user_uri)

        while True:
            filtered_result = next(filter(lambda event: event['uri'] == event_type_uri, page['collection']), None)
            if filtered_result:
                return filtered_result['scheduling_url']

            next_page = page['pagination']['next_page']
            if not next_page:
                break
            page = self.request.get(next_page).json()
        return
        