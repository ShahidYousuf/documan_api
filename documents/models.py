from django.db import models
from django.contrib.auth.models import User


class Document(models.Model):
    DOCUMENT_STATUS_CHOICES = (
        ('open', 'Open'),
        ('closed', 'Closed'),
    )
    name = models.CharField(max_length=150, null=True, blank=True)
    doc_file = models.FileField(upload_to='uploads/')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    shared_with = models.ManyToManyField(User, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified_on = models.DateTimeField(auto_now=True, null=True, blank=True)
    status = models.CharField(max_length=30, choices=DOCUMENT_STATUS_CHOICES)

    def __str__(self):
        return self.name



