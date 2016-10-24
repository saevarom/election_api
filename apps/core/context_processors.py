from django.conf import settings

fb_app_id = getattr(settings, 'FB_APP_ID', '')


def fb_app_id(request):
    return {
        'FB_APP_ID': fb_app_id,
    }