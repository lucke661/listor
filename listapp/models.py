from django.db import models

class Lista(models.Model):
    listname = models.CharField(max_length=255)
    cuser = models.ForeignKey(User, on_delete= models.CASCADE)
    cdate = models.DateTimeField(default=timezone.now)