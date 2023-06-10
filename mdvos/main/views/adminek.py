from django.shortcuts import render
import datetime

# Create your views here.
def adminek(request):
    context = {
        "now" : datetime.datetime.now()
    }
    return render(request, "admin.html", context)