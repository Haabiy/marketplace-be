import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from datetime import timedelta
from .models import SourceModel

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

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.parsers import JSONParser

from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .serializers import SourceSerializer
from .models import SourceModel

from datetime import datetime


import json

class ActivationSourcesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'data_sources_updates'
        
        if self.channel_layer:
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.channel_layer:
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')
        source_id = data.get('source_id')
        print(data)
        if action == 'activate':
            response = await self.activate_source(source_id)
        elif action == 'deactivate':
            response = await self.deactivate_source(source_id)
        elif action == 'reactivate':
            response = await self.reactivate_source(source_id)
        
        await self.send(text_data=json.dumps(response))

    @database_sync_to_async
    def activate_source(self, source_id):
        try:
            source = SourceModel.objects.get(id=source_id)
            source.status = 'active'
            source.save()
            serializer = SourceSerializer(source)
            return {"message": "Source activated successfully", "source": serializer.data}
        except SourceModel.DoesNotExist:
            return {"error": "Source not found"}

    @database_sync_to_async
    def deactivate_source(self, source_id):
        try:
            source = SourceModel.objects.get(id=source_id)
            source.status = 'inactive'
            source.save()
            serializer = SourceSerializer(source)
            return {"message": "Source deactivated successfully", "source": serializer.data}
        except SourceModel.DoesNotExist:
            return {"error": "Source not found"}

    @database_sync_to_async
    def reactivate_source(self, source_id):
        try:
            source = SourceModel.objects.get(id=source_id)
            source.status = 'active'
            source.save()
            serializer = SourceSerializer(source)
            return {"message": "Source reactivated successfully", "source": serializer.data}
        except SourceModel.DoesNotExist:
            return {"error": "Source not found"}

class DataLibraryConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'data_library_updates'

        # Join group
        if self.channel_layer:
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()
            await self.fetch_data()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.channel_layer:
            # Leave group
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def fetch_data(self):
        data = await self.get_data()
        await self.send(text_data=json.dumps({
            'data': data
        }))

    @database_sync_to_async
    def get_data(self):
        now_utc = timezone.now()
        europe_paris_tz = timezone.get_current_timezone()
        now_paris = now_utc.astimezone(europe_paris_tz)
        thirty_days_ago = now_paris - timedelta(days=30)

        getstatus = SourceModel.objects.all()
        today = now_paris.date()

        active_count = getstatus.filter(status='active', created_at__gt=thirty_days_ago).count()
        inactive_count = getstatus.filter(status='inactive', created_at__gt=thirty_days_ago).count()
        total_count = active_count + inactive_count

        received_count = getstatus.filter(current_update=today).count()
        awaiting_count = getstatus.filter(current_update__gt=today).count()
        delayed_count = getstatus.filter(current_update__lt=today).count()

        pending_count = 12
        in_progress_count = 5
        completed_count = 5

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

        return data

    async def receive(self, text_data):
        pass

class DataSourcesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'data_sources_updates'

        if self.channel_layer:
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()
            await self.fetch_data_sources()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.channel_layer:
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def fetch_data_sources(self):
        data_sources = await self.get_data_sources()
        await self.send(text_data=json.dumps({
            'data': data_sources
        }))

    @database_sync_to_async
    def get_data_sources(self):
        source_models = SourceModel.objects.order_by('-created_at')
        serializer = SourceSerializer(source_models, many=True)
        return serializer.data

    async def receive(self, text_data):
        pass

class UpdateSourceConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        # Disconnect from the WebSocket
        pass

    async def receive(self, text_data):
        # Handle incoming WebSocket messages
        try:
            data = JSONParser().parse(text_data)
            source_id = data.get('id')
            source_data = data.get('data')

            # Fetch the source model instance
            try:
                source = SourceModel.objects.get(id=source_id)
            except SourceModel.DoesNotExist:
                await self.send_json({'error': 'Source not found'}, status_code=404)
                return

            # Update the source model based on the received data
            serializer = SourceSerializer(source, data=source_data, partial=True)
            if serializer.is_valid():
                print(source_data)
                serializer.save()
                await self.send_json(serializer.data, status_code=200)
            else:
                await self.send_json(serializer.errors, status_code=400)
        
        except Exception as e:
            await self.send_json({'error': str(e)}, status_code=500)
