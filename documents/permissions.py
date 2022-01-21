import functools
import time
from rest_framework import permissions


class ConditionsPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        """" owner of the document will be able to View, Edit, and Delete the document
        collaborator will only be able to view and edit if the document is shared with them
        collaborator is forbidden to delete the owner created file
        collaborator will be able to create his/her own document.
        """
        edit_request = request.method == 'PUT'
        view_request = request.method == 'GET'
        delete_request = request.method == 'DELETE'

        view_edit_or_delete_request = view_request or edit_request or delete_request
        view_or_edit_request = view_request or edit_request

        # if request.method in permissions.SAFE_METHODS:
        #     return True

        is_document_owner = obj.owner == request.user
        is_in_shared_list = request.user in obj.shared_with.all()
        is_owner_editing = obj.owner == request.user and request.user in obj.current_editors.all()
        if is_document_owner:
            return True
        if is_in_shared_list and request.method == 'DELETE':
            return False
        if is_in_shared_list and view_edit_or_delete_request and is_owner_editing:
            return True
        if is_in_shared_list and view_or_edit_request:
            return True
        return False


def collaborator_throttle(f):
    """
    simple delay throttle to delay the collaborator requests in atomic db update
    """
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        time.sleep(1)
        return f(*args, **kwargs)
    return wrapper

