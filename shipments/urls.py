from django.urls import path
from . import views

app_name = 'shipments'

urlpatterns = [
    # Home page with tracking interface
    path('', views.TrackingHomeView.as_view(), name='tracking_home'),
    
    # AJAX endpoint for shipment tracking
    path('api/track/', views.track_shipment, name='track_shipment'),
    
    # Detailed shipment view
    path('shipment/<str:tracking_number>/', views.shipment_detail_view, name='shipment_detail'),
    
    # API endpoint for external integrations
    path('api/status/', views.api_shipment_status, name='api_status'),
    
    # Debug CSRF token view
    path('debug/csrf/', views.debug_csrf_token, name='debug_csrf_token'),
]