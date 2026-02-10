from django.db import models
import uuid
from django_countries.fields import CountryField
from geopy.geocoders import Nominatim

# Create your models here.
# shipments/models.py

import random
import string

def generate_tracking_number():
    from .models import Shipment
    while True:
        digits = ''.join(random.choices(string.digits, k=8))
        new_number = f"ED{digits}-US"
        if not Shipment.objects.filter(tracking_number=new_number).exists():
            return new_number

class Shipment(models.Model):
    # CHOICES
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_transit', 'In Transit'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('on_hold', 'On Hold'),
        ('cancelled', 'Cancelled'),
    ]
    
    TYPE_CHOICES = [
        ('air_freight', 'Air Freight'),
        ('truckload', 'Truckload'),
        ('international_shipping', 'International Shipping'),
        ('van_move', 'Van Move'),
        ('office_pickup', 'Office Pickup'),
    ]
    
    MODE_CHOICES = [
        ('sea', 'Sea'),
        ('land', 'Land'),
        ('air', 'Air'),
    ]
    
    PAYMENT_CHOICES = [
        ('cash', 'Cash'),
        ('cheque', 'Cheque'),
        ('bac', 'BAC'),
        ('paypal', 'PayPal'),
        ('zelle', 'Zelle'),
        ('crypto', 'Crypto'),
    ]
    
    CARRIER_CHOICES = [
        ('dhl', 'DHL'),
        ('fedex', 'FedEx'),
        ('global_express', 'Global Express Logistics'),
        ('usps', 'USPS'),
    ]

    # SHIPPER DETAILS
    shipper_name = models.CharField(max_length=100)
    shipper_phone = models.CharField(max_length=20)
    shipper_address = models.CharField(max_length=255)
    shipper_email = models.EmailField()

    # RECEIVER DETAILS
    receiver_name = models.CharField(max_length=100)
    receiver_phone = models.CharField(max_length=20)
    receiver_address = models.CharField(max_length=255)
    receiver_email = models.EmailField()

    # SHIPMENT DETAILS
    tracking_number = models.CharField(max_length=20, unique=True, default=generate_tracking_number)
    type_of_shipment = models.CharField(max_length=50, choices=TYPE_CHOICES, blank=True, null=True)
    weight = models.CharField(max_length=50, blank=True, null=True)
    product = models.CharField(max_length=100, blank=True, null=True)
    payment_mode = models.CharField(max_length=50, choices=PAYMENT_CHOICES, blank=True, null=True)
    carrier = models.CharField(max_length=100, choices=CARRIER_CHOICES, blank=True, null=True)
    departure_time = models.TimeField(blank=True, null=True)
    destination = models.CharField(max_length=200, blank=True, null=True)
    pickup_time = models.TimeField(blank=True, null=True)
    
    courier = models.CharField(max_length=100, blank=True, null=True)
    mode = models.CharField(max_length=50, choices=MODE_CHOICES, blank=True, null=True)
    quantity = models.CharField(max_length=50, blank=True, null=True)
    total_freight = models.CharField(max_length=50, blank=True, null=True)
    carrier_ref_no = models.CharField(max_length=100, blank=True, null=True)
    origin = models.CharField(max_length=200, blank=True, null=True)
    pickup_date = models.DateField(blank=True, null=True)
    expected_delivery_date = models.DateField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    # STATUS
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    current_status_date = models.DateField(blank=True, null=True)
    current_status_time = models.TimeField(blank=True, null=True)
    current_location = models.CharField(max_length=255, blank=True, null=True)
    
    # Internal for map (hidden from form)
    current_lat = models.FloatField(blank=True, null=True)
    current_lng = models.FloatField(blank=True, null=True)
    origin_lat = models.FloatField(blank=True, null=True)
    origin_lng = models.FloatField(blank=True, null=True)
    dest_lat = models.FloatField(blank=True, null=True)
    dest_lng = models.FloatField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Geocoding logic
        geolocator = Nominatim(user_agent="courier_tracking_app")
        
        # Geocode current location
        if self.current_location:
            try:
                location = geolocator.geocode(self.current_location)
                if location:
                    self.current_lat = location.latitude
                    self.current_lng = location.longitude
            except:
                pass
        
        # Geocode origin
        if self.origin and not self.origin_lat:
            try:
                location = geolocator.geocode(self.origin)
                if location:
                    self.origin_lat = location.latitude
                    self.origin_lng = location.longitude
            except:
                pass

        # Geocode destination
        if self.destination and not self.dest_lat:
            try:
                location = geolocator.geocode(self.destination)
                if location:
                    self.dest_lat = location.latitude
                    self.dest_lng = location.longitude
            except:
                pass
                
        super().save(*args, **kwargs)

    @property
    def hours_left(self):
        """Estimate hours left based on distance between current location and destination"""
        if self.current_lat and self.current_lng and self.dest_lat and self.dest_lng:
            from geopy.distance import geodesic
            current = (self.current_lat, self.current_lng)
            destination = (self.dest_lat, self.dest_lng)
            distance_km = geodesic(current, destination).km
            
            # Assume average speed based on mode
            # Air: 800 km/h, Land: 80 km/h, Sea: 40 km/h
            speed = 80 # Default land
            if self.mode == 'air': speed = 800
            elif self.mode == 'sea': speed = 40
            
            hours = distance_km / speed
            # Add some overhead for processing/stops (20%)
            total_hours = hours * 1.2
            return round(total_hours, 1)
        return None

    def __str__(self):
        return f"{self.tracking_number} - {self.receiver_name}"

    @property
    def total_volumetric(self):
        total = 0
        for pkg in self.packages.all():
            total += (pkg.qty * pkg.length * pkg.width * pkg.height) / 5000
        return round(total, 2)

    @property
    def total_volume(self):
        total = 0
        for pkg in self.packages.all():
            total += (pkg.qty * pkg.length * pkg.width * pkg.height) / 1000000 # in cu. m.
        return round(total, 3)

    @property
    def total_actual_weight(self):
        total = sum(pkg.qty * pkg.weight for pkg in self.packages.all())
        return round(total, 2)

class Package(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name='packages')
    qty = models.IntegerField(default=1)
    piece_type = models.CharField(max_length=50, blank=True, null=True) # e.g. Carton
    description = models.TextField(blank=True, null=True)
    length = models.FloatField(default=0.0, verbose_name="Length(cm)")
    width = models.FloatField(default=0.0, verbose_name="Width(cm)")
    height = models.FloatField(default=0.0, verbose_name="Height(cm)")
    weight = models.FloatField(default=0.0, verbose_name="Weight(kg)")

    def __str__(self):
        return f"Package for {self.shipment.tracking_number}"

class ShipmentUpdate(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name='updates')
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    location = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    updated_by = models.CharField(max_length=100, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.shipment.tracking_number} - {self.status}"

class SupportMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"
