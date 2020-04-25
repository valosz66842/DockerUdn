import os

def utility(request):
    os_name=os.name
    if os_name == 'nt':
        base_url = 'http://127.0.0.1:8000/'
    elif os_name == 'posix':
        base_url = 'https://django.gcp.com/'
    return {'base_url': base_url}
