from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404

from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import QueryDict
import json

from .serializers import SourceSerializer
from .models import SourceModel

import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        print(body)
        username = body.get('username')
        password = body.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Authentication successful
            return JsonResponse({'message': 'Login successful...'})
        else:
            # Authentication failed
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
