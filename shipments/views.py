from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db import models
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from .models import Shipment
import json
import logging
import re
from django.middleware.csrf import get_token

logger = logging.getLogger(__name__)


class TrackingHomeView(TemplateView):
    """
    Home page view for client shipment tracking.
    Displays the search interface for clients to track their shipments.
    """
    template_name = 'shipments/tracking_home.html'
    
    def get_context_data(self, **kwargs):
        """Add additional context data to the template"""
        context = super().get_context_data(**kwargs)
        context['total_shipments'] = Shipment.objects.count()
        context['recent_arrivals'] = Shipment.objects.filter(
            gate_out_date__isnull=False
        ).order_by('-gate_out_date')[:5]
        return context


@csrf_exempt  # Temporarily disable CSRF for debugging
def track_shipment(request):
    """
    API endpoint for tracking shipments.
    Accepts POST requests with tracking number and returns shipment details.
    """
    if request.method == 'POST':
        try:
            # Log CSRF token for debugging
            csrf_token = request.META.get('CSRF_COOKIE', 'Not Found')
            logger.debug(f"CSRF Token: {csrf_token}")

            # Get tracking number from POST data
            data = json.loads(request.body)
            tracking_number = data.get('tracking_number', '').strip()

            if not tracking_number:
                return JsonResponse({
                    'success': False,
                    'message': 'Please enter a tracking number'
                }, status=400)

            # Validate tracking number (letters and numbers only)
            if not re.match(r'^[a-zA-Z0-9]+$', tracking_number):
                return JsonResponse({
                    'success': False,
                    'message': 'Tracking number must contain only letters and numbers.'
                }, status=400)

            # Search for shipment by BL number, container number, or chassis number
            shipment = None
            try:
                shipment = Shipment.objects.get(
                    models.Q(bl_number__iexact=tracking_number) |
                    models.Q(container_no__iexact=tracking_number) |
                    models.Q(chassis_no__iexact=tracking_number)
                )
            except Shipment.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'Shipment not found. Please check your tracking number and try again.'
                }, status=404)

            # Prepare shipment data for response
            shipment_data = {
                'bl_number': shipment.bl_number,
                'container_no': shipment.container_no,
                'chassis_no': shipment.chassis_no or 'N/A',
                'shipping_line': shipment.shipping_line,
                'consignee': shipment.consignee,
                'shipper': shipment.shipper,
                'eta': shipment.eta.strftime('%B %d, %Y') if shipment.eta else 'N/A',
                'gate_out_date': shipment.gate_out_date.strftime('%B %d, %Y') if shipment.gate_out_date else 'Not yet delivered',
                'duty_status': 'Paid' if shipment.duty_status else 'Not Paid',
                'freight_status': shipment.get_freight_status_display(),
                'free_days': shipment.free_days,
                'demurrage_days': shipment.demurrage_days,
                'agent_assigned': shipment.agent_assigned or 'Not assigned',
                'supervisor_status': shipment.get_supervisor_status_display(),
                'description': shipment.description or 'No description available',
                'is_overdue': shipment.is_overdue(),
                'days_overdue': shipment.days_overdue() if shipment.is_overdue() else 0,
                'status_color': 'success' if shipment.gate_out_date else ('danger' if shipment.is_overdue() else 'warning')
            }

            return JsonResponse({
                'success': True,
                'shipment': shipment_data
            })

        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Invalid request format'
            }, status=400)
        except Exception as e:
            logger.error(f"Error in track_shipment: {e}")
            return JsonResponse({
                'success': False,
                'message': 'An error occurred while processing your request'
            }, status=500)

    # If not POST request, return method not allowed
    return JsonResponse({
        'success': False,
        'message': 'Method not allowed'
    }, status=405)


def shipment_detail_view(request, tracking_number):
    """
    Detailed view for a specific shipment.
    Can be accessed via direct URL with tracking number.
    """
    # Search for shipment by any of the three tracking fields
    shipment = get_object_or_404(
        Shipment,
        models.Q(bl_number__iexact=tracking_number) |
        models.Q(container_no__iexact=tracking_number) |
        models.Q(chassis_no__iexact=tracking_number)
    )
    
    context = {
        'shipment': shipment,
        'tracking_number': tracking_number
    }
    
    return render(request, 'shipments/shipment_detail.html', context)


def api_shipment_status(request):
    """
    API endpoint for getting shipment status.
    Returns JSON data for integration with other systems.
    """
    tracking_number = request.GET.get('tracking_number')
    
    if not tracking_number:
        return JsonResponse({
            'error': 'tracking_number parameter is required'
        }, status=400)
    
    try:
        shipment = Shipment.objects.get(
            models.Q(bl_number__iexact=tracking_number) |
            models.Q(container_no__iexact=tracking_number) |
            models.Q(chassis_no__iexact=tracking_number)
        )
        
        return JsonResponse({
            'bl_number': shipment.bl_number,
            'container_no': shipment.container_no,
            'status': 'delivered' if shipment.gate_out_date else 'in_transit',
            'eta': shipment.eta.isoformat() if shipment.eta else None,
            'gate_out_date': shipment.gate_out_date.isoformat() if shipment.gate_out_date else None,
            'duty_paid': shipment.duty_status,
            'freight_status': shipment.freight_status,
            'agent': shipment.agent_assigned
        })
        
    except Shipment.DoesNotExist:
        return JsonResponse({
            'error': 'Shipment not found'
        }, status=404)


def debug_csrf_token(request):
    """
    Temporary debug view to return the CSRF token.
    """
    csrf_token = get_token(request)
    return JsonResponse({
        'csrf_token': csrf_token
    })