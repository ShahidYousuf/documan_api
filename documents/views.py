from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from .models import Document
from .serializers import DocumentSerializer
from .permissions import ConditionsPermission


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all().order_by('-modified_on')
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated, ConditionsPermission]

    def retrieve(self, request, *args, **kwargs):
        return super(DocumentViewSet, self).retrieve(request, *args, **kwargs)


