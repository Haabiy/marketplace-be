from django.urls import re_path
from .consumers import *

websocket_urlpatterns = [
    re_path(r'ws/data_library/$', DataLibraryConsumer.as_asgi()),
    re_path(r'ws/read_source/', DataSourcesConsumer.as_asgi()),
    re_path(r'ws/update_source/', UpdateSourceConsumer.as_asgi()), 
    re_path(r'ws/data_source_activation/', ActivationSourcesConsumer.as_asgi()), 
]
