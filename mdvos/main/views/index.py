from django.shortcuts import render
import datetime

# Create your views here.
def home(request):
    context = {
        "now" : datetime.datetime.now()
    }
    request.session['next_page'] = request.get_full_path()
    return render(request, "index.html", context)