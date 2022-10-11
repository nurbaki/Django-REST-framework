from urllib import request
from rest_framework import permissions

class IsStaffPermission(permissions.IsAdminUser):
    # check permission:
    def has_permission(self, request, view):
        if request.auth:
        # is login:
            if request.method in permissions.SAFE_METHODS:
            # All member can view:
                return True
            else:
            # Only staff-member can run POST/PUT/DELETE:
                return bool(request.user.is_staff)
        # is not login:
        return False