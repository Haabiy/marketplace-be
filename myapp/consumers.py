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
from asgiref.sync import async_to_sync
import json, requests, os

from .signals import *

import boto3, logging
from dotenv import load_dotenv

load_dotenv()

#logger = logging.getLogger(__name__)

class DataLibraryConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'DataLibrary'

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
        received_count = getstatus.filter(datadelivery_status='received').count()
        awaiting_count = getstatus.filter(datadelivery_status='awaiting').count()
        delayed_count = getstatus.filter(datadelivery_status='delayed').count()

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
    async def handle_data_update(self, event):
        await self.fetch_data()

class ActivationSourcesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'ToggleVisibility'
        
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
        if action == 'activate':
            response = await self.activate_source(source_id)
        elif action == 'deactivate':
            response = await self.deactivate_source(source_id)
        elif action == 'reactivate':
            response = await self.reactivate_source(source_id)

        '''if self.channel_layer:
            await self.channel_layer.group_send(
                'DataLibrary',
                {
                    'type': 'handle_data_update',
                    'message': 'Update data library'
                }
            )

        await self.send(text_data=json.dumps(response))'''

    @database_sync_to_async
    def activate_source(self, source_id):
        try:
            source = SourceModel.objects.get(id=source_id)
            source.status = 'active'
            source.save()
            lib.send(sender=self.__class__, message="Update data library")
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
            lib.send(sender=self.__class__, message="Update data library")
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
            lib.send(sender=self.__class__, message="Update data library")
            serializer = SourceSerializer(source)
            return {"message": "Source reactivated successfully", "source": serializer.data}
        except SourceModel.DoesNotExist:
            return {"error": "Source not found"}


class DataSourcesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'DataSource'

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

    async def handle_data_update(self, event):
        await self.fetch_data_sources()

class FilterDataSourcesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'FilterDataSource'

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

    async def fetch_data_sources(self):
        await self.filter_data_sources()

    @database_sync_to_async
    def filter_data_sources(self, id):
        source = SourceModel.objects.get(id=id)
        #source_models = SourceModel.objects.order_by('-created_at')
        serializer = SourceSerializer(source)
        print(serializer.data)
        return serializer.data

    async def receive(self, text_data):
        # Parse incoming WebSocket message
        data = json.loads(text_data)
        action = data.get('action')
        print(data)
        if action == 'filter_by_id':
            source_id = data.get('id')
            if source_id:
                # Fetch data source by ID and send back the response
                data_source = await self.filter_data_sources(source_id)
                await self.send(text_data=json.dumps({
                    'status': 'success',
                    'data': data_source
                }))
            else:
                await self.send(text_data=json.dumps({
                    'status': 'error',
                    'message': 'ID not provided'
                }))

    async def handle_data_update(self, event):
        await self.fetch_data_sources()

class SourceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'CRUDSource'

        if self.channel_layer:
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()
            #await self.fetch_data_sources()
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
        formData = data.get('formData')
        if action == 'update_source':
            await self.update_source(source_id, formData)
        elif action == 'add_source':
            await self.add_source(formData)

        '''if self.channel_layer:
            await self.channel_layer.group_send(
                'DataLibrary',
                {
                    'type': 'handle_data_update',
                    'message': ({ "type": "update data sources"})
                }
            )
            await self.channel_layer.group_send(
                'DataSource',
                {
                    'type': 'handle_data_update',
                    'message': ({ "type": "update data sources"})
                }
            )
        await self.send(text_data=json.dumps(response))'''

    @database_sync_to_async
    def update_source(self, source_id, form_data):
        try:
            source = SourceModel.objects.get(id=source_id)
            if 'next_update' in form_data and form_data['next_update'] in [None, 'undefined', '', 'unscheduled']:
                form_data['next_update'] = None

            serializer = SourceSerializer(source, data=form_data, partial=True)
            
        except SourceModel.DoesNotExist:
            return {"status": "error", "message": "Source not found"}

        serializer = SourceSerializer(source, data=form_data)
        if serializer.is_valid():
            serializer.save()
            source_lib.send(sender=self.__class__, message="Update data library")
            return {"status": "success", "data": serializer.data}
        else:
            return {"status": "error", "errors": serializer.errors}

    @database_sync_to_async
    def add_source(self, form_data):
        form_data['next_update'] = None if(form_data['next_update']=='') else form_data['next_update']
        serializer = SourceSerializer(data=form_data)
        if serializer.is_valid():
            serializer.save()
            source_lib.send(sender=self.__class__, message="Update data library")
            print('serializer_data---:', serializer.data)
            return {"status": "success", "data": serializer.data}
        else:
            return {"status": "error", "errors": serializer.errors}
        
class EMRConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'EMR'
        
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
        try:
            data = json.loads(text_data)
            step = data.get('step')
            if step:
                result = await self.EMRRunner(step)
                await self.send(text_data=json.dumps(result))
            else:
                await self.send(text_data=json.dumps({'success': False, 'error': 'No step provided'}))
        except Exception as e:
            #logger.error(f"Error receiving data: {str(e)}")
            await self.send(text_data=json.dumps({'success': False, 'error': str(e)}))

    async def EMRRunner(self, step):
        try:
            s3_path = os.getenv("S3_PATH")
            EMR_CLUSTER_ID = os.getenv("EMR_CLUSTER_ID")
            AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
            AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
            AWS_REGION = os.getenv("AWS_REGION")

            emr_client = boto3.client(
                'emr',
                region_name=AWS_REGION,
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY
            )

            #logger.info("Initialized EMR client")

            step_config = {
                'Name': step,
                'ActionOnFailure': 'CONTINUE',
                'HadoopJarStep': {
                    'Jar': 'command-runner.jar',
                    'Args': [
                        'bash',
                        '-c',
                        'cd /home/hadoop/ && ' 
                        f'aws s3 sync {s3_path}/{step}/ /home/hadoop/{step}/ && '
                        f'cd /home/hadoop/{step} && '
                        'spark-submit --deploy-mode cluster --conf spark.pyspark.python=/home/hadoop/myenv/bin/python --py-files dependencies.py job.py '
                    ] 
                }
            }

            #logger.info(f"Adding step to EMR: {step_config}")

            # Add the step to the EMR cluster
            response = emr_client.add_job_flow_steps(
                JobFlowId=EMR_CLUSTER_ID,
                Steps=[step_config]
            )

            #logger.info(f"EMR step added: {response}")
            return {'success': True, 'step_id': response['StepIds'][0]}
        except Exception as e:
            #logger.error(f"Error running EMR step: {str(e)}")
            print(f"Error running EMR step: {str(e)}")
            return {'success': False, 'error': str(e)}