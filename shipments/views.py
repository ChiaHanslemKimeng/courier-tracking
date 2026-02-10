from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Shipment, SupportMessage

def track_shipment(request):
    shipment = None
    error = None

    if request.method == 'POST':
        tracking_number = request.POST.get('tracking_number')
        try:
            shipment = Shipment.objects.get(tracking_number=tracking_number)
        except Shipment.DoesNotExist:
            error = "Tracking number not found."

    return render(request, 'track.html', {
        'shipment': shipment,
        'error': error
    })

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Save to database (Messaging Center)
        SupportMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        
        full_message = f"Message from {name} ({email}):\n\n{message}"
        
        try:
            send_mail(
                subject=f"Contact Form: {subject}",
                message=full_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            messages.success(request, "Your message has been sent successfully! Our team will review it and get back to you shortly.")
        except Exception as e:
            # We still show success if database save worked but email failed
            messages.success(request, "Your message has been received! Our team will get back to you shortly.")
            
        return redirect('contact')
        
    return render(request, 'contact.html')

def services(request):
    return render(request, 'services.html')

from django.shortcuts import render, redirect, get_object_or_404

# Define blog posts outside for reuse in both views
BLOG_POSTS = [
    {
        'id': 1,
        'title': 'Future of Logistics',
        'date': 'Feb 1, 2026',
        'excerpt': 'How AI and automated drone delivery are redefining the shipping landscape for the next decade.',
        'image_url': 'https://images.unsplash.com/photo-1580674285054-bed31e145f59?auto=format&fit=crop&q=80&w=800',
        'content': """
            The logistics industry is standing on the brink of a revolution. As we move further into 2026, the integration of Artificial Intelligence (AI) and automated systems is no longer a luxury but a necessity for survival. 
            
            At Global Express Logistics, we are pioneering the use of machine learning algorithms to predict demand surges and optimize delivery routes in real-time. This not only reduces fuel consumption but also ensures that shipments reach their destinations faster than ever before.
            
            Autonomous drones are another major player. While still facing regulatory hurdles in some regions, drone delivery is proving to be a game-changer for 'last-mile' connectivity in remote areas. We expect to see a 300% increase in autonomous delivery operations over the next five years.
        """
    },
    {
        'id': 2,
        'title': 'The Last Mile Challenge',
        'date': 'Jan 25, 2026',
        'excerpt': 'Exploring innovative urban localized hubs to solve the efficiency gap in the final stage of delivery.',
        'image_url': 'https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?auto=format&fit=crop&q=80&w=800',
        'content': """
            The 'last mile' has always been the most expensive and complex part of the delivery journey. With urban populations growing, traditional delivery vans are finding it harder to navigate congested streets.
            
            Our solution at Global Express Logistics involve creating localized micro-fulfillment hubs. These hubs act as staging areas where larger shipments are broken down and delivered using smaller, more agile electric vehicles and e-bikes.
            
            This localized approach reduces the time a package stays in transit within the city and significantly lowers our carbon footprint. Innovation in the last mile is not just about speed; it's about smart urban integration.
        """
    },
    {
        'id': 3,
        'title': 'Sustainable Shipping',
        'date': 'Jan 15, 2026',
        'excerpt': 'Our commitment to carbon-neutral transport and eco-friendly packaging solutions for a greener planet.',
        'image_url': 'https://images.unsplash.com/photo-1578575437130-527eed3abbec?auto=format&fit=crop&q=80&w=800',
        'content': """
            Sustainability is at the core of our operations at Global Express Logistics. We recognize that the transportation industry is a major contributor to global emissions, and we are committed to being part of the solution.
            
            Our 'Green Global' initiative aims for total carbon neutrality by 2035. This involves transitioning our entire fleet to electric or hydrogen-powered vehicles and investing in carbon offset programs.
            
            Beyond the vehicles, we are also re-engineering our packaging. Our new biodegradable shipping materials are made from recycled plant fibers, ensuring that your shipments are protected without harming the environment.
        """
    },
    {
        'id': 4,
        'title': 'Global Supply Chain Resilience',
        'date': 'Jan 10, 2026',
        'excerpt': 'Strategies for building robust logistics networks that can withstand global disruptions and economic shifts.',
        'image_url': 'https://images.unsplash.com/photo-1521737604893-d14cc237f11d?auto=format&fit=crop&q=80&w=800',
        'content': """
            Recent global events have exposed the vulnerabilities in traditional supply chains. At Global Express Logistics, we believe that resilience is the primary metric of a modern logistics provider.
            
            Building resilience means diversifying routes and modes of transport. We use advanced data analytics to monitor global geopolitical and environmental risks, allowing us to pivot operations before disruptions occur.
            
            Collaboration is also key. By building strong partnerships with local carriers and infrastructure providers across 120+ countries, we ensure that our network remains flexible and reliable even under pressure.
        """
    },
    {
        'id': 5,
        'title': 'The Rise of E-commerce Logistics',
        'date': 'Jan 5, 2026',
        'excerpt': 'How the explosion of online shopping has forced the courier industry to adapt and scale at unprecedented speeds.',
        'image_url': 'https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?auto=format&fit=crop&q=80&w=800',
        'content': """
            The e-commerce boom of the last few years has permanently changed consumer expectations. 'Next-day delivery' is the new standard, and logistics companies must adapt or be left behind.
            
            Global Express Logistics has invested heavily in automated sorting centers that can handle millions of packages every day with 99.9% accuracy. These centers are the heartbeat of our e-commerce support system.
            
            We are also providing our merchants with deeper integration into our APIs, allowing them to offer their customers real-time tracking and flexible delivery options directly from their storefronts.
        """
    },
    {
        'id': 6,
        'title': 'Cold Chain Innovations',
        'date': 'Dec 28, 2025',
        'excerpt': 'The technology behind transporting temperature-sensitive goods like pharmaceuticals and fresh produce.',
        'image_url': 'https://images.unsplash.com/photo-1513106580091-1d82408b8cd6?auto=format&fit=crop&q=80&w=800',
        'content': """
            Transporting vaccines, medicines, and fresh food requires more than just a fast truck—it requires a precise, climate-controlled environment. This is the world of 'Cold Chain' logistics.
            
            Our specialized cold chain units at Global Express Logistics are equipped with IoT sensors that provide constant temperature and humidity monitoring. Any deviation triggers an immediate alert to our monitoring team.
            
            With the global demand for temperature-sensitive pharmaceuticals on the rise, we are expanding our cold storage facilities at major international airports to ensure seamless, safe transfers of life-saving goods.
        """
    },
]

def blog(request):
    return render(request, 'blog.html', {'posts': BLOG_POSTS})

def blog_detail(request, post_id):
    post = next((p for p in BLOG_POSTS if p['id'] == post_id), None)
    if not post:
        return redirect('blog')
    return render(request, 'blog_detail.html', {'post': post})


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid credentials. Please try again.")
            
    return render(request, 'login.html')

@login_required(login_url='admin_login')
def admin_dashboard(request):
    return render(request, 'dashboard.html')

def admin_logout(request):
    logout(request)
    messages.success(request, "Terminated session successfully. You are now logged out.")
    return redirect('admin_login')
