from django.shortcuts import render, get_object_or_404, redirect
from .models import Service, Announcement, Donation, BlogPost, Branch, Daily_Devotional, Sermon, GeneralOverseerMessage
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import ContactForm, PaymentForm
from django.http import HttpResponse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from django.http import HttpResponse
from io import BytesIO
import os
import qrcode
import folium
import json
import requests
import random



def home(request):

    daily_devotional = Daily_Devotional.objects.all()
    announcement = Announcement.objects.all()
    return render(request, 'church/home.html', {'announcement': announcement, 'daily_devotional': daily_devotional})
    
# views.py


def branches_view(request):
    # Query all branches from the database
    branches = Branch.objects.all()

    # Create a base map centered at a default location (change the location to your needs)
    m = folium.Map(location=[0, 0], zoom_start=2)

    # Loop through branches and add markers for each branch
    for branch in branches:
        folium.Marker(
            location=[branch.latitude, branch.longitude],
            popup=f"<b>{branch.name}</b><br>{branch.address}",
            icon=folium.Icon(color="red", icon="info-sign"),
        ).add_to(m)

    # Save the generated map to an HTML string
    map_html = m._repr_html_()

    # Pass branches and the map to the template
    return render(request, 'church/branch_list.html', {'branches': branches, 'map': map_html})


def about_us(request):
    return render(request, 'church/about_us.html')


# views.py

def simple_mail(request):
    send_mail(subject='That is your subject',
               message='That is your message body',
               from_email='hello@demomailtrap.com', 
               recipient_list=['edidiongeka54@gmail.com'])

    return HttpResponse ('message sent')


def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Get the data from the form
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Build the full email message
            full_message = f"Message from {name} ({email}):\n\n{message}"

            # Send the email
            send_mail(
                subject=f"Message from {name} via Contact Form",
                message=full_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['edidiongeka54@gmail.com'],
                fail_silently=False,
            )

            # Set a session variable to allow access to the thank-you page
            request.session['form_submitted'] = True

            # Redirect to the thank-you page
            return redirect('contact-thanks')
    else:
        form = ContactForm()

    return render(request, 'church/contact_us.html', {'form': form})


def contact_thanks(request):
    """View to render the Thank You page after successful form submission."""
    # Ensure the user came from the contact_us page via a successful form submission
    if not request.session.get('form_submitted'):
        return redirect('contact')  # Redirect back to the contact form if accessed improperly

    # Clear the session variable to prevent revisits
    del request.session['form_submitted']

    return render(request, 'church/contact_thanks.html')


def services(request):
    services = Service.objects.all().order_by('service_type', 'time')  # Ordering services by type and time
    return render(request, 'church/service.html', {'services': services})

def blog_post(request):
    # Query all blog posts ordered by date (latest first)
    posts = BlogPost.objects.all().order_by('-date_posted')
    
    # Set up pagination
    paginator = Paginator(posts, 6)  # 6 posts per page
    page_number = request.GET.get('page')  # Get the page number from the request
    page_obj = paginator.get_page(page_number)  # Get the page object for the current page
    
    # Render the template with the context
    context = {
        'page_obj': page_obj,  # Pass the page object to the template
    }
    return render(request, 'church/blog_post.html', context)

def blog_post_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    return render(request, 'church/blog_post_detail.html', {'post': post})

def sermon_list(request):
    sermons = Sermon.objects.all().order_by('-date_preached')
    
    # Set up pagination
    paginator = Paginator(sermons, 9)  # 9 posts per page
    page_number = request.GET.get('page')  # Get the page number from the request
    page_obj = paginator.get_page(page_number)  # Get the page object for the current page
    
    # Render the template with the context
    context = {
        'page_obj': page_obj,  # Pass the page object to the template
    }
    return render(request, 'church/sermon_list.html', context)


def sermon_detail(request, slug):
    # Get the specific sermon by its ID
    sermon = get_object_or_404(Sermon, slug=slug)

    # Fetch other sermons by the same preacher, excluding the current sermon
    related_sermons = Sermon.objects.filter(preacher=sermon.preacher).exclude(slug=slug)

    # Shuffle the related sermons to show random ones
    related_sermons_list = list(related_sermons)  # Convert queryset to a list
    random.shuffle(related_sermons_list)

    # Limit the related sermons to 4
    related_sermons = related_sermons_list[:4]

    # Render the sermon detail template with the sermon and related sermons
    return render(request, 'church/sermon_detail.html', {
        'sermon': sermon,
        'related_sermons': related_sermons,
    })

def overseer_message(request):
    message = GeneralOverseerMessage.objects.last()  # Get the latest message
    return render(request, 'church/overseer_message.html', {'message': message})

# views.py

def initialize_payment(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        amount = int(request.POST.get('amount')) * 100  # Convert to kobo (NGN currency)

        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json',
        }
        data = {
            'email': email,
            'amount': amount,
            'metadata': {
                'name': name
            }
        }

        url = 'https://api.paystack.co/transaction/initialize'
        response = requests.post(url, headers=headers, json=data)
        response_data = response.json()

        if response_data['status']:
            payment_url = response_data['data']['authorization_url']
            return redirect(payment_url)
        else:
            # Handle errors
            return JsonResponse({'error': 'Error initializing payment'}, status=500)

    return render(request, 'church/donation.html')

# views.py
@csrf_exempt
def verify_payment(request, reference):
    # Build the URL to verify the payment status
    url = f'https://api.paystack.co/transaction/verify/{reference}'
    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
    }

    # Make the request to Paystack to verify the transaction
    response = requests.get(url, headers=headers)
    response_data = response.json()

    if response_data['status'] and response_data['data']['status'] == 'success':
        # Payment is successful, perform any necessary actions (e.g., updating orders, sending receipts)

        # Redirect to the 'donate' page (or homepage) after successful payment
        return redirect('donate')  # Replace 'donate' with the correct URL name or view name

    else:
        # Handle unsuccessful payment
        messages.error(request, 'Payment verification failed. Please try again.')
        return JsonResponse({'error': 'Payment verification failed.'}, status=400)

def save_website_qr_code(request):
    # Your website URL (replace this with your actual domain name when available)
    website_url = "http://127.0.0.1:8000"

    # Generate the QR code
    qr = qrcode.make(website_url)

    # Save the QR code to a directory under MEDIA_ROOT
    qr_directory = os.path.join(settings.MEDIA_ROOT, 'website_qrcodes')
    os.makedirs(qr_directory, exist_ok=True)  # Ensure the directory exists
    qr_filename = "website_qr.png"
    qr_path = os.path.join(qr_directory, qr_filename)
    qr.save(qr_path)

    # Optionally return the saved file as a response
    with open(qr_path, "rb") as qr_file:
        return HttpResponse(qr_file.read(), content_type="image/png") 
