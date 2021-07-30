from json import JSONDecodeError
from calendly.utils.constants import WEBHOOK, USERS, ME, EVENT_TYPE, DATA_COMPLIANCE
from calendly.utils.constants import EVENTS, WEBHOOK_SUBSCRIPTIONS, SCHEDULING_LINKS
from calendly.utils.constants import ORGANIZATIONS, ORGANIZATION_MEMBERSHIPS

from calendly.utils.requests import CalendlyReq, CalendlyException


class Calendly(object):

    event_types_def = {
        "canceled": "invitee.canceled",
        "created": "invitee.created"
    }

    def __init__(self, api_key):
        """
        Constructor

        Args:
            api_key (str): Calendly Personal Access Token
        """
        self.request = CalendlyReq(api_key)

    def create_webhook(self, url, scope, organization, user=None, event_types=["canceled", "created"]):
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
                'scope': scope}

        if(scope == 'user'):
            if(user == None):
                raise CalendlyException
            data['user'] = user

        response = self.request.post(WEBHOOK, data)
        return response.json()

    def list_webhooks(self, organization, scope, user=None, count=20, sort=None):
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

        if(sort != None):
            data['sort'] = sort

        if(scope == 'user'):
            if(user == None):
                raise CalendlyException
            data['user'] = user

        response = self.request.get(WEBHOOK, data)
        return response.json()

    def delete_webhook(self, id):
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
        except JSONDecodeError:
            json_response = {}
        dict_response.update(json_response)
        return dict_response

    def get_webhook(self, uuid):
        """
        Get a Webhook Subscription for an Organization or User with specified UUID.

        Args:
            uuid (str): Webhook uuid

        Returns:
            dict: Json decoded response from Calenderly API for Get webhook action.
        """
        response = self.request.get(f'{WEBHOOK}/{uuid}')
        return response.json()

    def about(self):
        """
        Returns basic information about the user account.

        Returns:
            dict: Json decoded response about the basic information about the user.
        """
        response = self.request.get(ME)
        return response.json()

    def event_types(self, count="20", organization=None, page_token=None, sort=None, user=None):
        """
        Returns all Event Types associated with a specified user.

        Args:
            count (str, optional): Number of rows to return. Defaults to "20".
            organization (str, optional): View available personal, team and organization events type assosicated with the organization's URI. Defaults to None.
            page_token (str, optional): Toke to pass the next portion of the collection. Defaults to None.
            sort (str, optional): Order results by specified field and direction. Defaults to None.
            user (str, optional): user's URI. Defaults to None.

        Returns:
            dict: json decoded response with list of event types
        """
        data = {"count": count}
        if(organization):
            data['organization'] = organization
        if(page_token):
            data['page_token'] = page_token
        if(sort):
            data['sort'] = sort
        if(user):
            data['user'] = user
        response = self.request.get(EVENT_TYPE, data)
        return response.json()

    def get_event_type(self, uuid):
        """Returns event type associated with the specified UUID

        Args:
            uuid (str): Event UUID

        Returns:
            dict: json decoded response with information about the event
        """
        data = {"uuid": uuid}
        response = self.request.get(f'{EVENT_TYPE}/' + uuid, data)
        return response.json()

    def list_events(self, count="20", organization=None, sort=None, user=None, status=None):
        """
        Returns a List of Events

        Args:
            count (str, optional): Number of rows to return. Defaults to "20".
            organization (str, optional): Organization URI. Defaults to None.
            sort (str, optional): comma seperated list of {field}:{direction} values. Defaults to None.
            user (str, optional): User URI. Defaults to None.
            status (str, optional): 'active' or 'canceled'. Defaults to None.

        Returns:
            dict: json decoded response of list of events.
        """
        data = {'count': count}
        if(organization):
            data['organization'] = organization
        if(sort):
            data['sort'] = sort
        if(user):
            data['user'] = user
        if(status):
            data['status'] = status
        response = self.request.get(EVENTS, data)
        return response.json()

    def get_event_invitee(self, event_uuid, invitee_uuid):
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

    def get_event_details(self, uuid):
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

    def list_event_invitees(self, uuid):
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
