from rest_framework.permissions import BasePermission
from django.shortcuts import get_object_or_404
from .models import Listing, Image


class IsListingOwner(BasePermission):
    def has_permission(self, request, view):
        if 'id' in view.kwargs:
            listing = get_object_or_404(Listing, id=view.kwargs['id'])
            return listing.seller == request.user
        return True

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Listing):
            return obj.seller == request.user
        elif isinstance(obj, Image):
            return obj.listing.seller == request.user
        return False