# accounts/context_processors.py
from django.conf import settings
import os


def google_api_key(request):
    return {"GOOGLE_API_KEY": os.getenv("GOOGLE_API_KEY")}
