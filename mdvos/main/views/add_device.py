from django.shortcuts import render, redirect
from ..forms import AddDeviceForm, AddDeviceSpecsForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models.models import Specification, Specification_type, Devices


@login_required(login_url='login')
def add_device(request):
    if request.method == "POST":
        main_form = AddDeviceForm(request.POST, request.FILES)
        specs_form = AddDeviceSpecsForm(request.POST)
        
        if not (main_form.is_valid() and specs_form.is_valid()):
            return render(request, 'add_device.html', {'main_form':main_form, 'specs_form': specs_form})
        
        device = main_form.save()
        add_specs_to_device(specs_form.cleaned_data, device.id_device)

        messages.success(request, "Złożono propozycję dodania urządzenia.")
        return render(request, 'add_device.html', {'main_form': main_form, 'specs_form': specs_form})

            
    main_form = AddDeviceForm()
    specs_form = AddDeviceSpecsForm()
    return render(request, "add_device.html", {'main_form': main_form, 'specs_form': specs_form})


def add_specs_to_device(specs_data, device_id):

    cpu_spec = Specification(
        spec_type_id=Specification_type.objects.get(name='CPU'),
        value=specs_data['cpu'],
        devices_id=Devices.objects.get(id_device=device_id),
    )
    cpu_spec.save()

    ram_spec = Specification(
        spec_type_id=Specification_type.objects.get(name='RAM'),
        value=specs_data['ram'],
        devices_id=Devices.objects.get(id_device=device_id),
    )
    ram_spec.save()

    screen_size_spec = Specification(
        spec_type_id=Specification_type.objects.get(name='SIZE'),
        value=specs_data['screen_size'],
        devices_id=Devices.objects.get(id_device=device_id),
    )
    screen_size_spec.save()

    battery_spec = Specification(
        spec_type_id=Specification_type.objects.get(name='BATTERY'),
        value=specs_data['battery'],
        devices_id=Devices.objects.get(id_device=device_id),
    )
    battery_spec.save()

    disk_spec = Specification(
        spec_type_id=Specification_type.objects.get(name='DISC'),
        value=specs_data['disk_size'],
        devices_id=Devices.objects.get(id_device=device_id),
    )
    disk_spec.save()