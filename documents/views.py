from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from .models import Document
from .serializers import DocumentSerializer
from .permissions import IsOwnerOrReadOnly


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all().order_by('-created_on')
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]




    # def get_queryset(self):
    #     documents = [self.request.user.documents, self.request.user.shared_documents]
    #     return documents

