from django.shortcuts import render
import datetime

# Create your views here.
def error404(request):
    context = {
        "now" : datetime.datetime.now()
    }
    return render(request, "404.html", context)

def error503(request):
    context = {
        "now" : datetime.datetime.now()
    }
    return render(request, "503.html", context)