# shipments/urls.py
from django.urls import path
from .views import track_shipment, home, about, contact, services, blog, blog_detail, admin_login, admin_dashboard, admin_logout

urlpatterns = [
    path('', home, name='home'),
    path('track/', track_shipment, name='track'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('services/', services, name='services'),
    path('blog/', blog, name='blog'),
    path('blog/<int:post_id>/', blog_detail, name='blog_detail'),
    path('admin/login/', admin_login, name='admin_login'),
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin/logout/', admin_logout, name='admin_logout'),
]
