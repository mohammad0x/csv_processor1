from time import sleep
from celery import shared_task
import pandas as pd
from .models import Document

@shared_task()
def handle_uploaded_file(fileName,filePath,taskId,new_date):
    try:
        newFilePath = f'media/documents/output_{new_date}_{fileName}'
        df= pd.read_csv(filePath)
        df2=df.groupby(['Song', 'Date'], as_index=False)['Number of Plays'].sum()
        df2.columns = ['Song', 'Date', 'Total Number of Plays for Date']
        df2.to_csv(newFilePath,index= False)
        print('hello')
        document = Document.objects.get(id=taskId)
        document.inputFile = filePath
        document.outputFile = newFilePath
        document.status = 'done'
        document.save()
    except Exception as e:
        document = Document.objects.get(id=taskId)
        document.inputFile = filePath
        document.outputFile = str(e)
        document.status = 'failed'
        document.save()
