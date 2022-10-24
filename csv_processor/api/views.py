from random import random
from rest_framework.views import APIView
from django.http import JsonResponse
import pandas as pd
from rest_framework import status
from .serializers import DocumentSerializer
from .models import Document
from rest_framework.parsers import MultiPartParser
import json
from .tasks import handle_uploaded_file
import uuid
from datetime import datetime


class DocumentView(APIView):

    parser_classes = (MultiPartParser,)
    def post(self,request,*args, **kwargs):
        try:
            serializer = DocumentSerializer(data=request.data)
            if serializer.is_valid() and request.FILES['inputFile'].name.endswith('.csv') and 'inputFile' in request.FILES:
                    document = Document()
                    document.save()
                    f=request.FILES['inputFile']
                    new_date = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
                    filePath = f'media/documents/{new_date}_{f.name}'
                    fileName = f.name
                    with open(filePath, 'wb+') as destination:
                        for chunk in f.chunks():
                            destination.write(chunk)
                    
                    handle_uploaded_file.delay(fileName,filePath,document.id,new_date)
                    return JsonResponse({
                        'taskId': document.id
                    }, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse({
                        'error': 'bad request',
                    }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({
                'error': str(e),
                
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def get_object(self, pk):
        try:
            return Document.objects.get(id=pk)
        except Document.DoesNotExist as e:
            raise e

    def get(self, request, pk, *args, **kwargs):
        try:
            doc_instance = self.get_object(pk)
            if not doc_instance:
                return JsonResponse(
                    {"error": 'document not found!'},
                    status=status.HTTP_404_NOT_FOUND
                )
            print('check')
            document = pd.read_csv(doc_instance.outputFile, sep=',')
            res = document.to_json(orient='records')
            parsed=json.loads(res)
            data = {
                'status': doc_instance.status,
                'inputFile': doc_instance.inputFile,
                'outputFile': doc_instance.outputFile,
                'data':parsed
            }
            return JsonResponse(data, status=status.HTTP_200_OK,safe=False)
        except Exception as e:
            return JsonResponse({
                'error': str(e)
            },status= status.HTTP_500_INTERNAL_SERVER_ERROR)

