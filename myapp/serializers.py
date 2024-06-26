from rest_framework import serializers
from .models import SourceModel

class SourceSerializer(serializers.ModelSerializer):
    next_status = serializers.CharField(read_only=True)
    class Meta:
        model = SourceModel
        fields = '__all__' # or list using []