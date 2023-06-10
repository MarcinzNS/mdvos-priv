from django.shortcuts import render
import datetime

def os(request):
    context = {
        "now" : datetime.datetime.now()
    }
    return render(request, "os.html", context)