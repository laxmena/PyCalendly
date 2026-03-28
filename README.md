# PyCalendly
<a href="https://codeclimate.com/github/laxmena/PyCalendly/maintainability"><img src="https://api.codeclimate.com/v1/badges/12cadf4283a14dbb59eb/maintainability" /></a> [![CircleCI](https://circleci.com/gh/laxmena/PyCalendly/tree/main.svg?style=svg)](https://circleci.com/gh/laxmena/PyCalendly/tree/main)[![Downloads](https://pepy.tech/badge/pycalendly)](https://pepy.tech/project/pycalendly)

Python package to use [Calendly](https://calendly.com/) [API-v2](https://calendly.stoplight.io/docs/api-docs/docs/C-API-Conventions.md).

## Installation
Install with `pip`
```
$ pip install PyCalendly
```
## Usage
### Getting Started
See [Getting Started with Calendly API](https://developer.calendly.com/getting-started) and get a Personal Access token.

```
from calendly import CalendlyAPI
api_key = "<Personal Access Token>"
calendly = CalendlyAPI(api_key)
```
### Webhooks
- `create_webhook` - Create new Webhook subscription
- `list_webhooks` - List available Webhook subscriptions
- `delete_webhook` - Delete a previously subscribed webhook
- `get_webhook` - Get information about a specific webhook

### User
- `about` - Basic information about the current user

### Events
- `event_types` - Returns all event types associated with the event
- `get_event_type` - Get type associated with the specific event
- `list_events` - Returns available list of events
- `get_event_invitee` - Returns invitee information associated with the event
- `get_event_details` - Get information about the event
- `list_event_invitees` - Get all invitees for a event

### Oauth2
Getting started with [Calendly Oauth2 API](https://developer.calendly.com/api-docs/YXBpOjU5MTQwNw-o-auth-2-0) .
```
from calendly import CalendlyOauth2

client_id = "<client_id>"
client_secret = "<client_secret>"
redirect_uri = "<redirect_uri>"

oauth2 = CalendlyOauth2(
    client_id,
    client_secret,
    redirect_uri
)
```

### Methods
- `authorization_url` - Returns the formatted authorization URL
- `get_access_token` - Send a request to obtain the given access token
- `revoke_access_token` - Send a request to revoke the given access token
- `refresh_access_token` - Send a request to refresh the given access token
- `introspect_access_token` - Send a request to bring details about the given access token

## Issues
Feel free to submit issues and enhancement requests.
## Contributing
In general, we follow the "fork-and-pull" Git workflow.

1. Fork the repo on GitHub
2. Clone the project to your own machine
3. Commit changes to your own branch
4. Push your work back up to your fork
5. Submit a Pull request so that we can review your changes
NOTE: Be sure to merge the latest from "upstream" before making a pull request!

## Licensing
```
MIT License

Copyright (c) 2021 laxmena

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
### Citations:
Following modules are used as reference to build this package
- [Calendly-Python](https://github.com/kevteg/calendly-python)
- [PyCap](https://github.com/redcap-tools/PyCap)

![Visitor](https://visitor-badge.laobi.icu/badge?page_id=laxmena.PyCalendly)
