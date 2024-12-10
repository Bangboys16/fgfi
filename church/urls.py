from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about_us, name='about'),
    path('branches/', views.branches_view, name='branches'),
    path('contact/', views.contact_us, name='contact'),
    path('contact-thanks/', views.contact_thanks, name='contact-thanks'),
    path('donate/', views.initialize_payment, name='donate'),
    path('verify-payment/<str:reference>/', views.verify_payment, name='verify-payment'),
    path('service/', views.services, name='service'),
    path('blogpost/', views.blog_post, name='blogpost'),
    path('sermons/', views.sermon_list, name='sermons'),
    path('sermon-detail/<slug:slug>/', views.sermon_detail, name='sermon-detail'),
    path('overseer-message/', views.overseer_message, name='overseer-message'),
    path('simple/', views.simple_mail, name='simple'), 
    path('post-detail/<slug:slug>/', views.blog_post_detail, name='post-detail'),
    path('save-website-qr/', views.save_website_qr_code, name='save-website-qr'),
]