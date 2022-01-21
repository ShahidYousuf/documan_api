import datetime

from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Document
from .serializers import DocumentSerializer
from .permissions import ConditionsPermission


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all().order_by('-modified_on')
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated, ConditionsPermission]

    def retrieve(self, request, *args, **kwargs):
        return super(DocumentViewSet, self).retrieve(request, *args, **kwargs)

    @action(detail=True, methods=['get', 'retrieve'])
    def download(self, request, pk=None):
        document = self.get_object()
        url = request.build_absolute_uri(document.doc_file.url)
        owner_editing = document.owner in document.current_editors.all()
        is_collaborator = request.user in document.shared_with.all() and request.user != document.owner
        if is_collaborator and owner_editing:
            return Response({'status': 'Cannot download, owner is currently editing the document'}, status=status.HTTP_403_FORBIDDEN)
        role = "OWNER" if document.owner == request.user else "COLLABORATOR"
        date = datetime.datetime.now()
        path = str(settings.BASE_DIR) + document.doc_file.url
        log_text = f"\n{date} --- DOWNLOAD by {role} -- {request.user.username}\n"
        with open(path, 'a') as f:
            f.write(log_text)
        return Response({
            'download': url,
            'status': 'Click the link above to download the document.'
        })



