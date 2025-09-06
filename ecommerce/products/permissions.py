from rest_framework.permissions import BasePermission, SAFE_METHODS

class ProductPermissions(BasePermission):
    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        # All actions require authentication
        if not request.user.is_authenticated:
            return False
            
        # Authenticated users can read
        if request.method in SAFE_METHODS:
            return True

        # Only sellers can create products
        if request.method == "POST":
            return request.user.role == "SELLER"

        # Updates/deletes checked per object later
        return True

    def has_object_permission(self, request, view, obj):
        # All actions require authentication (checked in has_permission)
        if not request.user.is_authenticated:
            return False
            
        # Authenticated users can read
        if request.method in SAFE_METHODS:
            return True

        # Admin can update/delete any product
        if request.user.role == "admin" and request.method in ["PUT", "DELETE"]:
            return True

        # Seller can update/delete only their own products
        if request.user.role == "SELLER" and obj.seller == request.user:
            return True

        return False