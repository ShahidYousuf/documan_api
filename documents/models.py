from django.db import models
from django.contrib.auth.models import User


class Document(models.Model):
    """
    model for representing a document
    shared_with and current_editors are indirectly used for document states.
    """
    DOCUMENT_STATUS_CHOICES = (
        ('open', 'Open'),
        ('closed', 'Closed'),
    )
    name = models.CharField(max_length=150, null=True, blank=True)
    doc_file = models.FileField(upload_to='uploads/')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    shared_with = models.ManyToManyField(User, null=True, blank=True, related_name='shared_documents')
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified_on = models.DateTimeField(auto_now=True, null=True, blank=True)
    status = models.CharField(max_length=30, choices=DOCUMENT_STATUS_CHOICES)
    current_editors = models.ManyToManyField(User, blank=True, related_name='current_editing_documents')

    def __str__(self):
        return self.name




