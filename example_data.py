#!/usr/bin/env python
"""
Script to populate the database with sample shipping data.
Run with: python manage.py shell < example_data.py
"""

from shipments.models import Shipment
from django.utils import timezone
from datetime import date, timedelta
import random

# Sample data for creating test shipments
sample_data = [
    {
        'bl_number': 'BL2024001',
        'container_no': 'CONT001',
        'chassis_no': 'CH001',
        'shipping_line': 'Maersk Line',
        'consignee': 'ABC Trading Company',
        'shipper': 'Global Exports Inc.',
        'eta': date.today() + timedelta(days=5),
        'free_days': 7,
        'demurrage_days': 2,
        'duty_status': True,
        'penalty_duty': 1500.00,
        'description': 'Electronics and computer components',
        'item_quantity': 250,
        'extra_charges': 500.00,
        'towing_charge': 200.00,
        'towing_destination': 'Warehouse District A',
        'towing_car_owner': 'Express Logistics',
        'towing_status': True,
        'agent_assigned': 'John Smith',
        'supervisor_status': 'approved',
        'freight_payment': 3500.00,
        'freight_status': 'paid'
    },
    {
        'bl_number': 'BL2024002',
        'container_no': 'CONT002',
        'chassis_no': 'CH002',
        'shipping_line': 'MSC',
        'consignee': 'XYZ Manufacturing',
        'shipper': 'Industrial Suppliers Ltd',
        'eta': date.today() + timedelta(days=10),
        'free_days': 5,
        'demurrage_days': 0,
        'duty_status': False,
        'penalty_duty': 0.00,
        'description': 'Raw materials for manufacturing',
        'item_quantity': 500,
        'extra_charges': 750.00,
        'towing_charge': 300.00,
        'towing_destination': 'Industrial Zone B',
        'towing_car_owner': 'Heavy Haul Transport',
        'towing_status': False,
        'agent_assigned': 'Sarah Johnson',
        'supervisor_status': 'pending',
        'freight_payment': 4200.00,
        'freight_status': 'pending'
    },
    {
        'bl_number': 'BL2024003',
        'container_no': 'CONT003',
        'chassis_no': 'CH003',
        'shipping_line': 'COSCO',
        'consignee': 'Retail Chain Corp',
        'shipper': 'Fashion Imports',
        'eta': date.today() - timedelta(days=3),
        'gate_out_date': date.today() - timedelta(days=1),
        'free_days': 10,
        'demurrage_days': 3,
        'duty_status': True,
        'penalty_duty': 800.00,
        'description': 'Clothing and textiles',
        'item_quantity': 1000,
        'extra_charges': 300.00,
        'towing_charge': 150.00,
        'towing_destination': 'Distribution Center C',
        'towing_car_owner': 'City Transport',
        'towing_status': True,
        'agent_assigned': 'Mike Davis',
        'supervisor_status': 'completed',
        'freight_payment': 2800.00,
        'freight_status': 'paid'
    },
    {
        'bl_number': 'BL2024004',
        'container_no': 'CONT004',
        'chassis_no': 'CH004',
        'shipping_line': 'Evergreen',
        'consignee': 'Food Distributors Inc',
        'shipper': 'Agricultural Exports Co',
        'eta': date.today() + timedelta(days=15),
        'free_days': 3,
        'demurrage_days': 0,
        'duty_status': False,
        'penalty_duty': 0.00,
        'description': 'Canned goods and preserved foods',
        'item_quantity': 800,
        'extra_charges': 400.00,
        'towing_charge': 250.00,
        'towing_destination': 'Cold Storage Facility',
        'towing_car_owner': 'Refrigerated Transport',
        'towing_status': False,
        'agent_assigned': 'Lisa Wilson',
        'supervisor_status': 'in_progress',
        'freight_payment': 3200.00,
        'freight_status': 'not_paid'
    },
    {
        'bl_number': 'BL2024005',
        'container_no': 'CONT005',
        'chassis_no': None,
        'shipping_line': 'CMA CGM',
        'consignee': 'Auto Parts Direct',
        'shipper': 'Automotive Components Ltd',
        'eta': date.today() + timedelta(days=7),
        'free_days': 5,
        'demurrage_days': 1,
        'duty_status': True,
        'penalty_duty': 1200.00,
        'description': 'Car parts and automotive accessories',
        'item_quantity': 300,
        'extra_charges': 600.00,
        'towing_charge': 180.00,
        'towing_destination': 'Auto Service Center',
        'towing_car_owner': 'Automotive Logistics',
        'towing_status': True,
        'agent_assigned': 'Robert Brown',
        'supervisor_status': 'approved',
        'freight_payment': 3800.00,
        'freight_status': 'paid'
    }
]

# Create sample shipments
print("Creating sample shipments...")

for data in sample_data:
    shipment, created = Shipment.objects.get_or_create(
        bl_number=data['bl_number'],
        defaults=data
    )
    
    if created:
        print(f"Created shipment: {shipment.bl_number}")
    else:
        print(f"Shipment already exists: {shipment.bl_number}")

print(f"Database now contains {Shipment.objects.count()} shipments.")
print("\nSample tracking numbers you can use:")
for data in sample_data:
    print(f"- BL Number: {data['bl_number']}")
    print(f"  Container: {data['container_no']}")
    if data.get('chassis_no'):
        print(f"  Chassis: {data['chassis_no']}")
    print()