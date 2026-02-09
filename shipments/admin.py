from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Shipment
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    def has_delete_permission(self, request, obj=None):
        # Only superusers can delete users
        return request.user.is_superuser

from .models import Shipment, Package, ShipmentUpdate

class PackageInline(admin.TabularInline):
    model = Package
    extra = 1

class ShipmentUpdateInline(admin.TabularInline):
    model = ShipmentUpdate
    extra = 1

@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('tracking_number', 'shipper_name', 'receiver_name', 'status', 'created_at')
    list_filter = ('status', 'type_of_shipment', 'mode')
    search_fields = ('tracking_number', 'shipper_name', 'receiver_name', 'shipper_email', 'receiver_email')
    
    inlines = [PackageInline, ShipmentUpdateInline]
    
    # Clean, organized layout
    exclude = ('current_lat', 'current_lng')
    
    fieldsets = (
        ("LOGISTICS IDENTITY", {
            "fields": ("tracking_number",),
            "classes": ("wide",),
        }),
        ("PARTICIPANTS", {
            "fields": (
                ("shipper_name", "receiver_name"),
                ("shipper_phone", "receiver_phone"),
                ("shipper_email", "receiver_email"),
                ("shipper_address", "receiver_address"),
            ),
        }),
        ("LOGISTICS & FREIGHT", {
            "fields": (
                ("type_of_shipment", "mode"),
                ("carrier", "weight"),
                ("product", "quantity"),
                ("payment_mode", "total_freight"),
                ("carrier_ref_no", "courier"),
            )
        }),
        ("ROUTING & TIMELINE", {
            "fields": (
                ("origin", "destination"),
                ("departure_time", "pickup_time"),
                ("pickup_date", "expected_delivery_date"),
            )
        }),
        ("MANIFEST STATUS", {
            "fields": (
                "status",
                ("current_location", "current_status_date", "current_status_time"),
                "comments",
            )
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields
