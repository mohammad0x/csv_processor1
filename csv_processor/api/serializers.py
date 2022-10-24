from dataclasses import field, fields
from rest_framework import serializers

from api.models import Document

class DocumentSerializer(serializers.Serializer):
    inputFile = serializers.FileField(max_length= None)
    class Meta:
        model= Document
        fields= ['inputFile']