class CalendlyException(Exception):
    """Errors corresponding to a misuse of Calendly API"""

    def __init__(self, message=None, details=None):
        self.message = message or ""
        self.details = details or []
        super(CalendlyException, self).__init__(f"{self.message} - {self.details}")

class CalendlyOauth2Exception(CalendlyException):
    """Errors corresponding to a misuse of CalendlyOauth2 API"""