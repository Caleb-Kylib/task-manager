from django.http import JsonResponse

def home(request):
    # provide the current year for the footer in the template
    return JsonResponse({
        "message": "Welcome to the Task Manager API",
        "status": "running"
    })
