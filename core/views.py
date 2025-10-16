from django.shortcuts import render
from datetime import datetime

def home(request):
    # provide the current year for the footer in the template
    return render(request, 'home.html', {'year': datetime.utcnow().year})
