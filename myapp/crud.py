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

from .serializers import SourceSerializer
from .models import SourceModel

import logging

logger = logging.getLogger(__name__)

@csrf_exempt
@api_view(['POST'])
def add_new_source(request):
    if request.method == 'POST':
        if request.FILES:
            # Handle file uploads
            serializer = SourceSerializer(data = request.data, files=request.FILES)
        else:
            # Handle form-encoded data
            serializer = SourceSerializer(data=request.data)
            
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
@api_view(['GET'])
def data_sources(request):
    if request.method == 'GET':
        source_models = SourceModel.objects.order_by('-created_at') 
        serializer = SourceSerializer(source_models, many=True)
        data = serializer.data
        return Response(data)
    
@csrf_exempt
@api_view(['PUT', 'PATCH', 'POST'])
def update_source(request, id):
    try:
        source = SourceModel.objects.get(id=id)
        data = request.data.copy()
        # handles if the user chooses an empty next_update
        if 'next_update' in data and data['next_update'] in [None, 'undefined', '', 'unscheduled']:
            #data['next_update'] = '' or
            data['next_update'] = None 
    except SourceModel.DoesNotExist:
        return JsonResponse({"error": "Source not found"}, status=404)

    if request.method in ['PUT', 'POST']:
        serializer = SourceSerializer(source, data=data)
    elif request.method == 'PATCH':
        serializer = SourceSerializer(source, data=data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)
    else:
        logger.debug(f"Updated source: {serializer.data}")
        return Response(serializer.errors, status=400)

@csrf_exempt
@api_view(['DELETE', 'POST'])
def delete_source(request, id):
    if request.method in ['DELETE', 'POST']:
        delete_source = get_object_or_404(SourceModel, id=id)
        delete_source.delete()
        return JsonResponse({'message': 'Source deleted successfully'}, status=204)

