import requests

from drf_standardized_errors.handler import ExceptionHandler
from rest_framework.exceptions import APIException

from django.utils.translation import gettext_lazy as _


class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = _("Service temporarily unavailable, try again later.")
    default_code = "service_unavailable"


class CustomExceptionHandler(ExceptionHandler):
    def convert_known_exceptions(self, exc: Exception) -> Exception:
        if isinstance(exc, requests.Timeout):
            return ServiceUnavailable()
        return super().convert_known_exceptions(exc)
