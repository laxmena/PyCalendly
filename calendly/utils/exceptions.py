class CalendlyException(Exception):
    """Errors corresponding to a misuse of Calendly API"""

class CalendlyOauth2Exception(CalendlyException):
    """Errors corresponding to a misuse of CalendlyOauth2 API"""