from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from import_export.fields import Field
from .models import Shipment
from .models import AdminUpload
from .google_drive import upload_file_to_drive_obj


@admin.register(AdminUpload)
class AdminUploadAdmin(admin.ModelAdmin):
    list_display = ("file", "uploaded_at", "drive_file_link")
    readonly_fields = ("drive_file_id", "drive_file_link")

    # Set your Shared Drive folder and drive IDs here
    SHARED_DRIVE_FOLDER_ID = "1KmlipO7ZnG-q7pUM-nNFyOgzWopgCzvR"
    SHARED_DRIVE_ID = None  # Set this if you know your Shared Drive ID, else leave as None

    def save_model(self, request, obj, form, change):
        # Only upload if this is a new file or the file has changed
        if obj.file and not obj.drive_file_id:
            file_obj = obj.file.open("rb")
            file_id, file_link = upload_file_to_drive_obj(
                file_obj,
                obj.file.name,
                mimetype=getattr(obj.file.file, "content_type", None),
                folder_id=self.SHARED_DRIVE_FOLDER_ID,
                drive_id=self.SHARED_DRIVE_ID,
            )
            obj.drive_file_id = file_id
            obj.drive_file_link = file_link
            file_obj.close()
        super().save_model(request, obj, form, change)



class ShipmentResource(resources.ModelResource):
    """
    Resource class for import/export functionality.
    Defines how data should be imported/exported for Shipment model.
    """
    
    # Custom fields for better export/import experience
    duty_status_display = Field(column_name='duty_status_display')
    towing_status_display = Field(column_name='towing_status_display')
    freight_status_display = Field(column_name='freight_status_display')
    total_charges = Field(column_name='total_charges')
    
    class Meta:
        model = Shipment
        fields = (
            'id', 'bl_number', 'shipping_line', 'consignee', 'shipper',
            'eta', 'free_days', 'demurrage_days', 'duty_status',
            'duty_status_display', 'penalty_duty', 'container_no',
            'description', 'chassis_no', 'item_quantity', 'extra_charges',
            'towing_charge', 'towing_destination', 'towing_car_owner',
            'towing_status', 'towing_status_display', 'agent_assigned',
            'gate_out_date', 'supervisor_status', 'freight_payment',
            'freight_status', 'freight_status_display', 'total_charges',
            'created_at', 'updated_at'
        )
        export_order = fields
    
    def dehydrate_duty_status_display(self, shipment):
        """Export duty status as readable text"""
        return shipment.get_duty_status_display_custom()
    
    def dehydrate_towing_status_display(self, shipment):
        """Export towing status as readable text"""
        return shipment.get_towing_status_display_custom()
    
    def dehydrate_freight_status_display(self, shipment):
        """Export freight status as readable text"""
        return shipment.get_freight_status_display()
    
    def dehydrate_total_charges(self, shipment):
        """Export total charges calculation"""
        return shipment.total_charges()


@admin.register(Shipment)
class ShipmentAdmin(ImportExportModelAdmin):
    """
    Custom admin configuration for Shipment model.
    Provides Excel-like interface with search, filters, and bulk editing.
    """
    
    resource_class = ShipmentResource
    
    # List display - shows all important fields in tabular format (Excel-like)
    list_display = [
        'bl_number',
        'container_no', 
        'shipping_line',
        'consignee',
        'shipper',
        'eta',
        'free_days',
        'demurrage_days',
        'colored_duty_status',
        'penalty_duty',
        'chassis_no',
        'item_quantity',
        'extra_charges',
        'towing_charge',
        'towing_destination',
        'towing_car_owner',
        'colored_towing_status',
        'agent_assigned',
        'gate_out_date',
        'supervisor_status',
        'freight_payment',
        'colored_freight_status',
        'overdue_indicator',
        'updated_at',
        'duty_status',
        'freight_status',
        'towing_status',
    ]
    
    # Fields that can be edited directly from the list view (Excel-like editing)
    list_editable = [
        'duty_status',
        'freight_status',
        'gate_out_date',
        'agent_assigned',
        'supervisor_status',
        'towing_status',
        'penalty_duty',
        'extra_charges',
        'towing_charge',
        'freight_payment',
    ]
    
    # Search functionality
    search_fields = [
        'bl_number',
        'container_no',
        'chassis_no',
        'consignee',
        'shipper',
        'shipping_line',
        'agent_assigned',
    ]
    
    # Filter options in right sidebar
    list_filter = [
        'duty_status',
        'freight_status',
        'towing_status',
        'supervisor_status',
        'shipping_line',
        'agent_assigned',
        'eta',
        'gate_out_date',
        'created_at',
    ]
    
    # Date hierarchy for easy navigation
    date_hierarchy = 'eta'
    
    # Number of items per page
    list_per_page = 50
    list_max_show_all = 200
    
    # Ordering
    ordering = ['-updated_at']
    
    # Fields to display in the detailed form
    fieldsets = [
        ('Basic Information', {
            'fields': [
                ('bl_number', 'container_no'),
                ('shipping_line', 'chassis_no'),
                ('consignee', 'shipper'),
                'description',
            ],
            'classes': ['wide']
        }),
        ('Timeline & Dates', {
            'fields': [
                ('eta', 'gate_out_date'),
                ('free_days', 'demurrage_days'),
            ],
            'classes': ['wide']
        }),
        ('Financial Information', {
            'fields': [
                ('duty_status', 'penalty_duty'),
                ('freight_status', 'freight_payment'),
                'extra_charges',
            ],
            'classes': ['wide']
        }),
        ('Towing Information', {
            'fields': [
                ('towing_charge', 'towing_status'),
                'towing_destination',
                'towing_car_owner',
            ],
            'classes': ['wide']
        }),
        ('Management', {
            'fields': [
                ('agent_assigned', 'supervisor_status'),
                'item_quantity',
            ],
            'classes': ['wide']
        }),
        ('System Information', {
            'fields': [
                ('created_at', 'updated_at'),
            ],
            'classes': ['collapse', 'wide'],
            'description': 'Automatically managed timestamps'
        }),
    ]
    
    # Read-only fields
    readonly_fields = ['created_at', 'updated_at']
    
    # Custom methods for colored status display
    def colored_duty_status(self, obj):
        """Display duty status with color coding"""
        if obj.duty_status:
            return format_html(
                '<span style="color: green; font-weight: bold;">✓ Paid</span>'
            )
        else:
            return format_html(
                '<span style="color: red; font-weight: bold;">✗ Not Paid</span>'
            )
    colored_duty_status.short_description = 'Duty Status'
    colored_duty_status.admin_order_field = 'duty_status'
    
    def colored_towing_status(self, obj):
        """Display towing status with color coding"""
        if obj.towing_status:
            return format_html(
                '<span style="color: green; font-weight: bold;">✓ Paid</span>'
            )
        else:
            return format_html(
                '<span style="color: red; font-weight: bold;">✗ Not Paid</span>'
            )
    colored_towing_status.short_description = 'Towing Status'
    colored_towing_status.admin_order_field = 'towing_status'
    
    def colored_freight_status(self, obj):
        """Display freight status with color coding"""
        colors = {
            'paid': 'green',
            'not_paid': 'red',
            'pending': 'orange'
        }
        color = colors.get(obj.freight_status, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_freight_status_display()
        )
    colored_freight_status.short_description = 'Freight Status'
    colored_freight_status.admin_order_field = 'freight_status'
    
    def overdue_indicator(self, obj):
        """Show overdue status with visual indicator"""
        if obj.is_overdue():
            days = obj.days_overdue()
            return format_html(
                '<span style="color: red; font-weight: bold;">⚠️ {} days overdue</span>',
                days
            )
        else:
            return format_html(
                '<span style="color: green;">✓ On time</span>'
            )
    overdue_indicator.short_description = 'Status'
    overdue_indicator.admin_order_field = 'eta'
    
    # Custom actions
    actions = ['mark_duty_paid', 'mark_freight_paid', 'export_selected_shipments']
    
    def mark_duty_paid(self, request, queryset):
        """Bulk action to mark duty as paid"""
        updated = queryset.update(duty_status=True)
        self.message_user(
            request,
            f'{updated} shipments marked as duty paid.'
        )
    mark_duty_paid.short_description = 'Mark selected shipments duty as paid'
    
    def mark_freight_paid(self, request, queryset):
        """Bulk action to mark freight as paid"""
        updated = queryset.update(freight_status='paid')
        self.message_user(
            request,
            f'{updated} shipments marked as freight paid.'
        )
    mark_freight_paid.short_description = 'Mark selected shipments freight as paid'
    
    # Enhanced save method
    def save_model(self, request, obj, form, change):
        """Custom save logic"""
        super().save_model(request, obj, form, change)
    
    # Custom queryset for performance
    def get_queryset(self, request):
        """Optimize queryset for better performance"""
        return super().get_queryset(request).select_related()


# Customize admin site headers
admin.site.site_header = "Shipping Management System"
admin.site.site_title = "Shipping Admin"
admin.site.index_title = "Welcome to Shipping Management Dashboard"