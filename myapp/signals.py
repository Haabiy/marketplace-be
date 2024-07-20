# signals.py
from django.dispatch import Signal, receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

crud,lib, source, toggle, source_lib = (Signal() for i in range(5))

@receiver(crud)
def CRUDSourceSignal(sender, **kwargs):
    channel_layer = get_channel_layer()
    message = kwargs['message']

    async_to_sync(channel_layer.group_send)(
        'CRUDSource',
        {
            'type': 'handle_data_update',
            'message': message
        }
    )

@receiver(lib)
def DataLibrarySignal(sender, **kwargs):
    channel_layer = get_channel_layer()
    message = kwargs['message']

    async_to_sync(channel_layer.group_send)(
        'DataLibrary',
        {
            'type': 'handle_data_update',
            'message': message
        }
    )

@receiver(source)
def DataSourceSignal(sender, **kwargs):
    channel_layer = get_channel_layer()
    message = kwargs['message']

    async_to_sync(channel_layer.group_send)(
        'DataSource',
        {
            'type': 'handle_data_update',
            'message': message
        }
    )

@receiver(lib)
def DataLibrarySignal(sender, **kwargs):
    channel_layer = get_channel_layer()
    message = kwargs['message']

    async_to_sync(channel_layer.group_send)(
        'DataLibrary',
        {
            'type': 'handle_data_update',
            'message': message
        }
    )

@receiver(source_lib)
def DataSource_DataLibSignal(sender, **kwargs):
    channel_layer = get_channel_layer()
    message = kwargs['message']

    async_to_sync(channel_layer.group_send)(
        'DataSource',
        {
            'type': 'handle_data_update',
            'message': message
        }
    )

    async_to_sync(channel_layer.group_send)(
        'DataLibrary',
        {
            'type': 'handle_data_update',
            'message': message
        }
    )

@receiver(toggle)
def ToggleVisibilitySignal(sender, **kwargs):
    channel_layer = get_channel_layer()
    message = kwargs['message']

    async_to_sync(channel_layer.group_send)(
        'ToggleVisibility',
        {
            'type': 'handle_data_update',
            'message': message
        }
    )
