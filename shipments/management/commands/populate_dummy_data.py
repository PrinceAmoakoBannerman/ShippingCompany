from django.core.management.base import BaseCommand
from shipments.models import Shipment
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Populate the database with dummy shipment data'

    def handle(self, *args, **kwargs):
        Shipment.objects.all().delete()  # Clear existing data

        dummy_shipments = [
            Shipment(
                bl_number=f"BL000{i}",
                container_no=f"CONT000{i}",
                shipping_line="Maersk",
                consignee="Consignee {i}",
                shipper="Shipper {i}",
                eta=datetime.now() + timedelta(days=i),
                free_days=5,
                demurrage_days=i,
                duty_status="Pending",
                penalty_duty=100 * i,
                chassis_no=f"CHASSIS000{i}",
                item_quantity=10 * i,
                extra_charges=50 * i,
                towing_charge=200 * i,
                towing_destination=f"Destination {i}",
                towing_car_owner=f"Owner {i}",
                towing_status="Not Started",
                agent_assigned=f"Agent {i}",
                gate_out_date=datetime.now() + timedelta(days=i),
                supervisor_status="Pending",
                freight_payment=500 * i,
                freight_status="Unpaid",
                overdue_indicator=False,
                updated_at=datetime.now()
            ) for i in range(1, 11)
        ]

        Shipment.objects.bulk_create(dummy_shipments)
        self.stdout.write(self.style.SUCCESS('Successfully populated dummy shipment data.'))
