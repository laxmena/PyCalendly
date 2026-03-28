# Changelog

All notable changes to PyCalendly will be documented here.

## [0.1.0] - 2026-03-27

### Added
- OAuth2 authentication support via new `CalendlyOauth2` class
- `get_access_token` — exchange authorization code for access token
- `revoke_access_token` — revoke a given access token
- `refresh_access_token` — refresh an existing access token
- `introspect_access_token` — retrieve details about a token
- `authorization_url` property for building the OAuth2 authorization URL
- Dedicated `CalendlyException` and `CalendlyOauth2Exception` exception classes in `exceptions.py`

### Changed
- **Breaking:** `CalendlyReq.process_request` now raises `CalendlyException` on HTTP 4xx/5xx responses instead of returning the raw response
- Renamed internal `utils/requests.py` to `utils/api.py` to avoid shadowing the `requests` package
- Mutable default argument in `create_webhook` changed from `list` to `tuple`
- Return type annotations corrected on `list_event_types`, `list_events`, `get_all_event_types`, `get_all_scheduled_events`

### Fixed
- Removed unnecessary parentheses in conditionals throughout `calendly.py`
- `user == None` replaced with `user is None`

## [0.0.1] - 2021-07-29

- Initial release
