from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # owner of the document will be able to View, Edit, and Delete the document
        # other user will only be able to view and edit if the document is shared with them
        # other user will be able to create his/her own document.
        edit_request = request.method == 'PUT'
        view_request = request.method == 'GET'

        view_or_edit_request = view_request or edit_request

        # if request.method in permissions.SAFE_METHODS:
        #     return True

        is_document_owner = obj.owner == request.user
        is_in_shared_list = request.user in obj.shared_with.all()

        if is_document_owner:
            return True
        if is_in_shared_list and view_or_edit_request:
            return True
        return False
