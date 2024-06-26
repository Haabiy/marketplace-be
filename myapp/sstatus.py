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

from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
@api_view(['POST', 'PUT'])
def activate_source(request, source_id):
    try:
        source = SourceModel.objects.get(id=source_id)
        source.status = 'active'
        source.save()
        source_data = {
            "id": source.id,
            "title": source.country,
            "data_vendor": source.data_vendor,
            "panel": source.panel,
            "panel_group": source.panel_group,
            "scope_of_subscription": source.scope_of_subscription,
            "data_type": source.data_type,
            "granularity": source.granularity,
            "end_date": source.end_date,
            "current_update": source.current_update,
            "next_update": source.next_update,
            "created_by": source.created_by,
            "datadelivery_status": source.datadelivery_status,
            "status": source.status,
        }
        return Response({
            "message": "Source activated successfully",
            "source": source_data
        })
    except SourceModel.DoesNotExist:
        return Response({"error": "Source not found"}, status=404)
@csrf_exempt
@api_view(['POST', 'PUT'])
def deactivate_source(request, source_id):
    try:
        source = SourceModel.objects.get(id=source_id)
        source.status = 'inactive'
        source.save()
        source_data = {
            "id": source.id,
            "title": source.country,
            "data_vendor": source.data_vendor,
            "panel": source.panel,
            "panel_group": source.panel_group,
            "scope_of_subscription": source.scope_of_subscription,
            "data_type": source.data_type,
            "granularity": source.granularity,
            "end_date": source.end_date,
            "current_update": source.current_update,
            "next_update": source.next_update,
            "created_by": source.created_by,
            "datadelivery_status": source.datadelivery_status,
            "status": source.status,
        }
        return Response({
            "message": "Source deactivated successfully",
            "source": source_data
        })
    except SourceModel.DoesNotExist:
        return Response({"error": "Source not found"}, status=404)
@csrf_exempt
@api_view(['POST'])
def reactivate_source(request, source_id):
    try:
        source = SourceModel.objects.get(id=source_id)
        source.status = 'active'
        source.save()
        source_data = {
            "id": source.id,
            "title": source.country,
            "data_vendor": source.data_vendor,
            "panel": source.panel,
            "panel_group": source.panel_group,
            "scope_of_subscription": source.scope_of_subscription,
            "data_type": source.data_type,
            "granularity": source.granularity,
            "end_date": source.end_date,
            "current_update": source.current_update,
            "next_update": source.next_update,
            "created_by": source.created_by,
            "datadelivery_status": source.datadelivery_status,
            "status": source.status,
        }
        return Response({
            "message": "Source reactivated successfully",
            "source": source_data
        })
    except SourceModel.DoesNotExist:
        return Response({"error": "Source not found"}, status=404)

@csrf_exempt  
@api_view(['GET'])
def data_library(request):
    """
    API endpoint to summarize the status of sources created 30 days or earlier.

    Args:
        request: The HTTP request.

    Returns:
        Response: A JSON response containing the summary of source statuses.
    """
    now_utc = timezone.now()

    # Convert to 'Europe/Paris' timezone
    europe_paris_tz = timezone.get_current_timezone()
    now_paris = now_utc.astimezone(europe_paris_tz)

    # Calculate thirty days ago in 'Europe/Paris' timezone
    thirty_days_ago = now_paris - timedelta(days=30)
    #thirty_days_ago = timezone.now() - timedelta(days=30)

    getstatus = SourceModel.objects.all()
    today = now_paris.date()

    # Count the number of active, inactive, and total
    active_count = getstatus.filter(status='active', created_at__gt=thirty_days_ago).count()
    inactive_count = getstatus.filter(status='inactive', created_at__gt=thirty_days_ago).count()
    total_count = active_count + inactive_count

    # Count the number of scheduled, awaiting, and delayed sources
    received_count = getstatus.filter(current_update=today).count()
    awaiting_count = getstatus.filter(current_update__gt=today).count()
    delayed_count = getstatus.filter(current_update__lt=today).count()

    # Sample data for pending, in-progress, and completed counts
    pending_count = 12
    in_progress_count = 5
    completed_count = 4

    # Organize data into sections
    data = [
        {
            "section": "Data Library",
            "t1": "Created",
            "t2": "Activated",
            "t3": "Deactivated",
            "d1": 30,
            "d2": 30,
            "d3": 30,
            "s1": total_count,
            "s2": active_count,
            "s3": inactive_count
        },
        {
            "section": "Data Delivery",
            "t1": "Received",
            "t2": "Awaiting",
            "t3": "Delayed",
            "d1": 30,
            "d2": 30,
            "d3": 30,
            "s1": received_count,
            "s2": awaiting_count,
            "s3": delayed_count
        },
        {
            "section": "Data Update",
            "t1": "Pending",
            "t2": "In Progress",
            "t3": "Completed",
            "d1": 30,
            "d2": 30,
            "d3": 30,
            "s1": pending_count,
            "s2": in_progress_count,
            "s3": completed_count
        }
    ]

    return Response(data)