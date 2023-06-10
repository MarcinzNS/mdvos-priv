from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from ..services.devices import *
from ..services.os import *
from ..forms import CommentForm, UnderCommentForm, AddDeviceForm, AddDeviceSpecsForm, ChangeDevicePhotoForm
from main.models.models import Devices, Specification, Specification_type

from django.shortcuts import render
from django.contrib import messages




import math

def devices(request, category="NOT", sort_by="NOT", how_many_item_on_page=5, page=1,):
    context = {
        "sidebar": {
            "brand": ["Xiaomi", "Samsung", "Apple", "Motorola"],
            "ram": [6, 8, 12, 16, 18],
            "sort_by": {"Sortuj wg daty": "premier", "Sortuj po nazwie": "brand", "Sortuj po nazwie modelu": "model"}
        }
    } 
    brand_filter = []
    ram_filter = []
    urlEnd = ""
    if request.method == "GET":
        urlEnd = GETtoURL(request.GET)
        brand_filter = [brand_name for brand_name in context["sidebar"]["brand"] if request.GET.get(brand_name, False)]
        ram_filter = [ram_value for ram_value in context["sidebar"]["ram"] if request.GET.get(f"ram{ram_value}", False)]

    data = getDevicesDataForPage(category, sort_by, how_many_item_on_page, page, brand_filter, ram_filter)
    
    how_many_pages = math.ceil(data["how_many_results"]/how_many_item_on_page)
    
    context |= {
        "data": data["data"],
        "how_many_pages": [i+1 for i in range(how_many_pages)],
        "show_arrow": [page >= 2, page+1 <= how_many_pages],
        "page": {
            "previous": page-1,
            "next": page+1,
            "show_pages_controler": how_many_pages > 1
        },
        "how_many_item_on_page": how_many_item_on_page,
        "filters": {
            "brand": brand_filter, 
            "ram": ram_filter
        },
        "urlEnd": urlEnd
    }
    if category != "NOT": context |= {"category":category}
    if sort_by != "NOT": context |= {"sort_by":sort_by}
    
    request.session['next_page'] = request.get_full_path()
    
    return render(request, "devices.html", context)

def followed_list(request, category="NOT", sort_by="NOT", how_many_item_on_page=5, page=1,):
   
    context = {
        "sidebar": {
            "brand": ["Xiaomi", "Samsung", "Apple", "Motorola"],
            "ram": [6, 8, 12, 16, 18],
            "sort_by": {"Sortuj wg daty": "premier", "Sortuj po nazwie": "brand", "Sortuj po nazwie modelu": "model"}
        }
    } 
    brand_filter = []
    ram_filter = []
    urlEnd = ""
    if request.method == "GET":
        urlEnd = GETtoURL(request.GET)
        brand_filter = [brand_name for brand_name in context["sidebar"]["brand"] if request.GET.get(brand_name, False)]
        ram_filter = [ram_value for ram_value in context["sidebar"]["ram"] if request.GET.get(f"ram{ram_value}", False)]

    data = getDevicesDataForPage(category, sort_by, how_many_item_on_page, page, brand_filter, ram_filter)
    
    how_many_pages = math.ceil(data["how_many_results"]/how_many_item_on_page)
    
    context |= {
        "data": data["data"],
        "how_many_pages": [i+1 for i in range(how_many_pages)],
        "show_arrow": [page >= 2, page+1 <= how_many_pages],
        "page": {
            "previous": page-1,
            "next": page+1,
            "show_pages_controler": how_many_pages > 1
        },
        "how_many_item_on_page": how_many_item_on_page,
        "filters": {
            "brand": brand_filter, 
            "ram": ram_filter
        },
        "urlEnd": urlEnd
    }
    if category != "NOT": context |= {"category":category}
    if sort_by != "NOT": context |= {"sort_by":sort_by}
    
    request.session['next_page'] = request.get_full_path()
        
    return render(request, "followed.html", context)


def GETtoURL(getDict):
    url = "?"
    for key in getDict:
        url += f"{key}={getDict[key]}&"
    return url[:-1]


def one_device(request, id):

    main_edit_device_form = AddDeviceForm(initial={
            'brand': Devices.objects.get(id_device=id).brand,
            'model': Devices.objects.get(id_device=id).model,
            'device_type': Devices.objects.get(id_device=id).device_type,
            'release_date': Devices.objects.get(id_device=id).premier,
        }
    )

    specs_edit_device_form = AddDeviceSpecsForm(initial={
            'cpu': Specification.objects.get(devices_id=id, spec_type_id=Specification_type.objects.get(name="CPU")),
            'ram': Specification.objects.get(devices_id=id, spec_type_id=Specification_type.objects.get(name="RAM")),
            'screen_size': Specification.objects.get(devices_id=id, spec_type_id=Specification_type.objects.get(name="SIZE")),
            'battery': Specification.objects.get(devices_id=id, spec_type_id=Specification_type.objects.get(name="BATTERY")),
            'disk_size': Specification.objects.get(devices_id=id, spec_type_id=Specification_type.objects.get(name="DISC")),
        }
    )

    edit_image_form = ChangeDevicePhotoForm(initial={'image': Devices.objects.get(id_device=id).image})

    context = {
        "device" : getDeviceData(id),
        "specification" : getSpecificationData(id),
        "OS_ALL" : getOSAll(id),
        "like": getDeviceLike(request, id),
        'comments': getCommentsWithUnderComments(id),
        "OS_chart": getOSChart(id),
        "main_comment_form": CommentForm(),
        "under_comment_form":UnderCommentForm(),
        "main_edit_device_form": main_edit_device_form,
        "specs_edit_device_form": specs_edit_device_form,
        'edit_image_form': edit_image_form,
    }

    request.session['next_page'] = request.get_full_path()
    
    return render(request, "device.html", context)



@login_required(login_url='login')
def add_MainComment(request, device_id):
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        print(form)
        if form.is_valid():

            form.save(device_id, request)
            messages.success(request, "Pomyślnie dodany do bazy danych.")

        else:
            messages.error(request,form.errors)
            
            
    else:   
        print(form.errors)
        
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required(login_url='login')
def add_UnderComment(request, device_id, main_comment_id):
    form = UnderCommentForm()
    if request.method == 'POST':
        form = UnderCommentForm(request.POST)
        print(form)
        if form.is_valid():

            form.save(device_id, request, main_comment_id)
            messages.success(request, "Pomyślnie dodany do bazy danych.")

        else:
            messages.error(request,form.errors)
            
            
    else:   
        print(form.errors)
        
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
    
    
    
    


