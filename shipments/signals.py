from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import os
from .models import Shipment

@receiver(post_save, sender=Shipment)
def send_tracking_email(sender, instance, created, **kwargs):
    if created:
        subject = "Your Shipment Tracking Number - Global Express Logistics"
        
        # HTML Content
        html_content = f"""
        <html>
            <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #333; line-height: 1.6;">
                <div style="max-width: 600px; margin: 20px auto; padding: 40px; border: 1px solid #e0e0e0; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
                    <div style="text-align: center; margin-bottom: 30px;">
                        <img src="cid:logo" alt="Global Express Logistics" style="max-width: 180px;">
                    </div>
                    
                    <h2 style="color: #0d6efd; text-align: center; margin-bottom: 25px;">Shipment Confirmation</h2>
                    
                    <p>Dear {instance.receiver_name or 'Valued Customer'},</p>
                    
                    <p>We are pleased to inform you that your shipment has been successfully registered with <strong>Global Express Logistics</strong>.</p>
                    
                    <div style="background: #f8fafc; padding: 25px; border-radius: 10px; border-left: 4px solid #0d6efd; margin: 25px 0;">
                        <p style="margin: 0; font-size: 1.1em;"><strong>Tracking Number:</strong> <span style="color: #0d6efd;">{instance.tracking_number}</span></p>
                        <p style="margin: 10px 0 0 0; color: #64748b;"><strong>Current Status:</strong> Customs status updated.</p>
                    </div>
                    
                    <p>You can monitor your shipment's progress in real-time by clicking the button below:</p>
                    
                    <div style="text-align: center; margin: 35px 0;">
                        <a href="http://127.0.0.1:8000/" style="background: #0d6efd; color: #ffffff; padding: 14px 30px; text-decoration: none; border-radius: 8px; font-weight: bold; display: inline-block;">Track Shipment</a>
                    </div>
                    
                    <p style="font-size: 0.95em;">We hope this meets with your approval. Please do not hesitate to reach out if we can be of any further assistance.</p>
                    
                    <hr style="border: 0; border-top: 1px solid #edf2f7; margin: 35px 0;">
                    
                    <div style="color: #64748b; font-size: 0.9em;">
                        <p style="margin-bottom: 5px;">Yours sincerely,</p>
                        <p style="margin-top: 0; font-weight: bold; color: #1e293b;">Global Express Logistics Team</p>
                    </div>
                </div>
                <div style="text-align: center; font-size: 0.8em; color: #94a3b8; margin-top: 20px;">
                    &copy; 2026 Global Express Logistics. All rights reserved.
                </div>
            </body>
        </html>
        """
        
        text_content = strip_tags(html_content)
        
        email = EmailMultiAlternatives(
            subject,
            text_content,
            settings.DEFAULT_FROM_EMAIL,
            [instance.receiver_email]
        )
        email.attach_alternative(html_content, "text/html")
        
        # Attach Logo for CID embedding
        logo_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'logo.png')
        if os.path.exists(logo_path):
            with open(logo_path, 'rb') as f:
                from email.mime.image import MIMEImage
                msg_img = MIMEImage(f.read())
                msg_img.add_header('Content-ID', '<logo>')
                msg_img.add_header('Content-Disposition', 'inline', filename='logo.png')
                email.attach(msg_img)
        
        email.send(fail_silently=False)
