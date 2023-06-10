from ..models.models import Devices, OS, OS_devices, OS_version
from django.db.models import Q
import json

def getOSAll(id: int) -> dict:
    os_devices = list(OS_devices.objects.filter(devices_id=id).values_list('os_id__os_version_id', "devices_id"))

    os_all = []
    for os_device in os_devices:
        os_version_id = os_device[0]
        os_versions = list(
            OS_version.objects.filter(os_version_id=os_version_id)
            .values('os_version_id', 'version', 'date_start', 'date_end', 'os_id')
        )
        os_all.extend(os_versions)

    os_all_name = list(OS.objects.values('id_os', 'name'))
    os_data = {}

    for os_info in os_all:
        os_id = os_info['os_id']
        os_data[os_info['os_version_id']] = {
            'version': os_info['version'],
            'date_start': os_info['date_start'],
            'date_end': os_info['date_end'],
            'name': next((os_name['name'] for os_name in os_all_name if os_name['id_os'] == os_id), None)
        }

    return os_data

def getOSChart(id: int) -> dict:
    os_devices = list(OS_devices.objects.filter(devices_id=id).values_list('os_id__os_version_id', "devices_id"))

    os_all = []
    for os_device in os_devices:
        os_version_id = os_device[0]
        os_versions = list(
            OS_version.objects.filter(os_version_id=os_version_id)
            .values('os_version_id', 'version', 'date_start', 'date_end', 'os_id')
        )
        os_all.extend(os_versions)

    os_all_name = list(OS.objects.values('id_os', 'name'))
    os_data = {}

    for os_info in os_all:
        os_id = os_info['os_id']
        os_data[os_info['os_version_id']] = {
            
            "start": os_info['date_start'].year if os_info['date_start'] else None,
            "koniec": os_info['date_end'].year if os_info['date_end'] else None,
        }

    os_chart_json = json.dumps(os_data)
    return os_chart_json

