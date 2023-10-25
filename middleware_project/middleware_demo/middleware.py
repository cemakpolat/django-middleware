# middleware_demo/middleware.py
import logging
from django.http import HttpResponseServerError, HttpResponseForbidden, HttpResponse
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from datetime import datetime
from .models import StatisticsLog
import requests

class CustomHeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Modify the request object (e.g., add custom headers)
        request_header = request.META
        logging.info(f"Log request: {str(request_header)}")

        response = self.get_response(request)
        # Modify the response object (e.g., add custom headers)
        response['Custom-Response-Header'] = 'Custom-Response-Value'
           # Access response headers
        for header, value in response.items():
            # You can log or process each response header here
            logging.info(f'Response Header: {header} = {value}')

        logging.info(f"Log response: {str(response.content)}")
        return response

class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        logging.info(f"Log request: {str(request)}")
        logging.info(f"Log response: {str(response)}")
        return response

class ErrorHandlingMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        response = self.get_response(request)
        if response.status_code == 500:
            response = HttpResponseServerError("System cannot be accessed", content_type="text/plain", status=500)
    
        return response



class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define the rate limit values (requests per minute)
        
        if "rate-limited" in request.get_full_path():

            rate_limit = 5  # Adjust as needed
            rate_limit_key = f'ratelimit:{request.user.id}'  # Use user ID as the key

            request_count = cache.get(rate_limit_key, 0)
            print(request_count, rate_limit)
            if request_count >= rate_limit:
                # User has exceeded the rate limit
                return HttpResponseForbidden("Rate limit exceeded")

            # Increment the request count
            request_count += 1
            cache.set(rate_limit_key, request_count, 60)  # Store count for 1 minute

        response = self.get_response(request)
        return response


class CustomAuthHeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        if "/app/statistics/json/" in request.META['PATH_INFO']:
            if "HTTP_AUTHORIZATION" in request.META:
                print("authorize message")
                api_response = requests.get('http://auth_service:5000/canBeAuthorized', headers={'Authorization': request.META.get('HTTP_AUTHORIZATION')})

                if api_response.status_code == 200 and api_response.json().get('message') == "ok":
                    response = self.get_response(request)
                else:
                    # Authentication failed
                    response = HttpResponse("User authorization failed", status=401)
            else:
                # Authentication failed
                response = HttpResponse("User authorization failed", status=401)
        else:
            response = self.get_response(request)
        return response

class StatisticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Capture statistics
        start_time = datetime.now()

        response = self.get_response(request)

        end_time = datetime.now()
        response_time = end_time - start_time

        # Store statistics in the database
        try:
            StatisticsLog.objects.create(
                request_path=request.path,
                ip_address=request.META['REMOTE_ADDR'],
                response_time=response_time.total_seconds()
            )
        except Exception:
            pass
            # logging.error("User statistic couldn't be saved!")

        return response


