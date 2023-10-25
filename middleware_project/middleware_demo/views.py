from django.shortcuts import render
import logging
# Create your views here.
from django.http import JsonResponse, HttpResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from .models import StatisticsLog  


# Sample view function that demonstrates authentication middleware
def protected_view(request):
    if request.user.is_authenticated:
        return JsonResponse({"message": "Authenticated user can access this view."})
    else:
        return JsonResponse({"message": "Authentication required."}, status=401)

# Sample view function that demonstrates request/response modification middleware
def custom_headers_view(request):
    response = JsonResponse({"message": "This response has custom headers."})
    response['X-Custom-Header'] = 'Custom-Value'
    return response

# Sample view function that demonstrates error handling middleware
def error_handling_view(request):
    # Simulate an error (e.g., division by zero)
    try:
        result = 1 / 0
        return JsonResponse({"result": result})
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return HttpResponseServerError(f"An error occurred: {str(e)}")

# Sample view function that demonstrates rate limiting middleware
@csrf_exempt  # Disable CSRF protection for this view (use with caution)
@never_cache  # Prevent caching of this view
def rate_limited_view(request):
    return JsonResponse({"message": "This view has rate limiting applied."})



def statistics_view(request):
    # Retrieve statistics data from the database
    statistics_data = StatisticsLog.objects.all()

    return render(request, 'statistics.html', {'statistics_data': statistics_data})



def get_statistics(request):
    # Retrieve statistics data from the database
    statistics_data = StatisticsLog.objects.all().values()

    # Convert the data to a list and create a JSON response
    data_list = list(statistics_data)
    return JsonResponse(data_list, safe=False)
