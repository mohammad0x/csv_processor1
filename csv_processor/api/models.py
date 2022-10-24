from django.db import models

class Document(models.Model):
   inputFile = models.CharField(max_length=100, blank=True, null= False)
   outputFile = models.CharField(max_length=200, blank=True, null=False)
   status = models.CharField(max_length=10,blank=False, null=False,default='processing')
   timestamp = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True)
