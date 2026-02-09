# Global Express Logistics - Courier & Tracking System

![Project Banner](https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?auto=format&fit=crop&q=80&w=1200)

A premium, full-stack logistics management platform built with Django. This system handles everything from shipment registration and real-time tracking to automated email notifications and professional customer engagement.

## 🚀 Key Features

- **Real-Time Shipment Tracking**: Visual tracking interface with Leaflet/OSM map integration and automated status updates.
- **Dynamic Admin Dashboard**: Powered by `django-jazzmin`, featuring a streamlined UI for managing complex logistics data.
- **Interactive UX**: Smooth entrance animations using `Animate.css` and `AOS` (Animate on Scroll).
- **Social Proof**: Integrated testimonial carousel and customer engagement sections.
- **Automated Communication**: HTML-formatted tracking emails with embedded branding (Logo/CID).
- **Professional Blog**: Full-featured blog with unique imagery and detail views for industry insights.

## 🛠️ Technology Stack

- **Backend**: Django (Python)
- **Frontend**: Bootstrap 5, Vanilla CSS, JavaScript
- **Animations**: AOS.js, Animate.css
- **Maps**: Leaflet / OpenStreetMap
- **Admin**: Django-Jazzmin
- **Email**: Django.core.mail (SMTP integration)

## 📦 Local Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ChiaHanslemKimeng/courier-tracking.git
   cd courier-tracking
   ```

2. **Set up virtual environment**:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1  # Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Start the server**:
   ```bash
   python manage.py runserver
   ```

## 🌐 Deployment

This project is configured for seamless deployment to **PythonAnywhere**. Detailed instructions can be found in the [Deployment Guide](./deployment_guide.md).

---
*Delivering excellence through technology.*
