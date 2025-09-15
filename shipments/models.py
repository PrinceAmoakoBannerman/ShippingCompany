from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone


class AdminUpload(models.Model):
    file = models.FileField(upload_to='uploads/')
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    drive_file_id = models.CharField(max_length=128, blank=True, null=True)
    drive_file_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.file.name

class Shipment(models.Model):
    """
    Shipment model representing a shipping container/cargo record.
    Contains all fields needed for tracking shipments from origin to destination.
    """
    
    # Freight Status Choices
    FREIGHT_STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('not_paid', 'Not Paid'),
        ('pending', 'Pending'),
    ]
    
    # Supervisor Status Choices
    SUPERVISOR_STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    # Primary identification fields
    bl_number = models.CharField(
        max_length=50, 
        unique=True, 
        verbose_name='BL Number',
        help_text='Bill of Lading Number - unique identifier for the shipment'
    )
    
    container_no = models.CharField(
        max_length=50,
        verbose_name='Container Number',
        help_text='Container identification number',
        db_index=True
    )
    
    chassis_no = models.CharField(
        max_length=50,
        verbose_name='Chassis Number',
        help_text='Chassis number for tracking',
        blank=True,
        null=True,
        db_index=True
    )
    
    # Shipping details
    shipping_line = models.CharField(
        max_length=100,
        verbose_name='Shipping Line',
        help_text='Name of the shipping company'
    )
    
    consignee = models.CharField(
        max_length=200,
        verbose_name='Consignee',
        help_text='Recipient of the shipment'
    )
    
    shipper = models.CharField(
        max_length=200,
        verbose_name='Shipper',
        help_text='Sender of the shipment'
    )
    
    # Date and timeline fields
    eta = models.DateField(
        verbose_name='ETA (Expected Time of Arrival)',
        help_text='Expected arrival date at destination'
    )
    
    gate_out_date = models.DateField(
        verbose_name='Gate Out Date',
        blank=True,
        null=True,
        help_text='Date when container left the port/facility'
    )
    
    # Demurrage and free days
    free_days = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Free Days',
        help_text='Number of free storage days at port'
    )
    
    demurrage_days = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Demurrage Days',
        help_text='Number of days exceeding free period'
    )
    
    # Financial fields
    duty_status = models.BooleanField(
        default=False,
        verbose_name='Duty Status',
        help_text='Check if duty has been paid'
    )
    
    penalty_duty = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
        verbose_name='Penalty Duty Amount',
        help_text='Amount of penalty duty charges'
    )
    
    extra_charges = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
        verbose_name='Extra Charges at Port',
        help_text='Additional charges incurred at the port'
    )
    
    freight_payment = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
        verbose_name='Freight Payment Amount',
        help_text='Amount paid for freight services'
    )
    
    freight_status = models.CharField(
        max_length=20,
        choices=FREIGHT_STATUS_CHOICES,
        default='pending',
        verbose_name='Freight Payment Status',
        help_text='Current status of freight payment'
    )
    
    # Towing information
    towing_charge = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name='Towing Charge',
        help_text='Cost for towing services'
    )
    
    towing_destination = models.CharField(
        max_length=200,
        verbose_name='Towing Destination',
        blank=True,
        help_text='Final destination for towing'
    )
    
    towing_car_owner = models.CharField(
        max_length=200,
        verbose_name='Towing Car Owner',
        blank=True,
        help_text='Owner of the towing vehicle'
    )
    
    towing_status = models.BooleanField(
        default=False,
        verbose_name='Towing Payment Status',
        help_text='Check if towing charges have been paid'
    )
    
    # Cargo details
    description = models.TextField(
        verbose_name='Cargo Description',
        help_text='Detailed description of the shipment contents',
        blank=True
    )
    
    item_quantity = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name='Item Quantity',
        help_text='Number of items in the shipment'
    )
    
    # Management fields
    agent_assigned = models.CharField(
        max_length=100,
        verbose_name='Assigned Agent',
        help_text='Agent responsible for handling this shipment',
        blank=True
    )
    
    supervisor_status = models.CharField(
        max_length=20,
        choices=SUPERVISOR_STATUS_CHOICES,
        default='pending',
        verbose_name='Supervisor Status',
        help_text='Current supervisor review status'
    )
    
    # Timestamp fields
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created At'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Last Updated'
    )
    
    class Meta:
        verbose_name = 'Shipment'
        verbose_name_plural = 'Shipments'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['bl_number']),
            models.Index(fields=['container_no']),
            models.Index(fields=['chassis_no']),
            models.Index(fields=['shipping_line']),
            models.Index(fields=['agent_assigned']),
            models.Index(fields=['eta']),
        ]
    
    def __str__(self):
        return f"{self.bl_number} - {self.container_no}"
    
    def get_duty_status_display_custom(self):
        """Custom display for duty status"""
        return "Paid" if self.duty_status else "Not Paid"
    
    def get_towing_status_display_custom(self):
        """Custom display for towing status"""
        return "Paid" if self.towing_status else "Not Paid"
    
    def is_overdue(self):
        """Check if shipment is overdue based on ETA"""
        if self.gate_out_date:
            return False  # Already delivered
        return timezone.now().date() > self.eta
    
    def days_overdue(self):
        """Calculate how many days overdue"""
        if not self.is_overdue():
            return 0
        return (timezone.now().date() - self.eta).days
    
    def total_port_charges(self):
        """Calculate total charges at port"""
        return self.penalty_duty + self.extra_charges
    
    def total_charges(self):
        """Calculate total all charges"""
        return self.penalty_duty + self.extra_charges + self.towing_charge + self.freight_payment