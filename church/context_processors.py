from django.utils import timezone
from .models import BlogPost, Sermon
from datetime import date

def navbar_context(request):
    today = timezone.now().date()
    blog_post_today_count = BlogPost.objects.filter(date_posted=today).count()
    return {'blog_post_today_count': blog_post_today_count}


def sermon_context(request):
    today = date.today()
    sermon_today_count = Sermon.objects.filter(created_at__gte=today).count() 
    return {'sermon_today_count': sermon_today_count}
