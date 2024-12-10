from django.contrib import admin
from .models import Service, Announcement, BlogPost, Donation, Branch, Daily_Devotional, Sermon, GeneralOverseerMessage
from django.utils import timezone

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'service_type', 'day', 'time', 'location')
    search_fields = ('title', 'service_type')
    list_filter = ('service_type', 'day')

class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_posted', 'is_active')
    search_fields = ['title']
    list_filter = ('date_posted', 'is_active')

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_posted', 'category')
    search_fields = ('title', 'author', 'category')
    list_filter = ('date_posted', 'category')

class DonationAdmin(admin.ModelAdmin):
    list_display = ('bank_name', 'account_name','bank_account')
    search_fields = ('bank_name', 'account_name')
    list_filter = ['bank_name']

class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'address', 'phone_number', 'email')
    search_fields = ['name', 'location']
    #readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Branch Information', {
            'fields': ('name', 'location', 'address', 'latitude', 'longitude')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone_number')
        }),
    )
class Daily_DevotionalAdmin(admin.ModelAdmin):
    list_display = ('bible_portion', 'date')
    
    # def save_model(self, request, obj, form, change):
    #     if not change:
    #         obj.created_at = timezone.now()
    #     obj.updated_at = timezone.now()
    #     super().save_model(request, obj, form, change)
class SermonAdmin(admin.ModelAdmin):
    list_display = ('title', 'preacher', 'date_preached', 'posted_by', 'created_at')
    search_fields = ('title', 'preacher', 'description')
    list_filter = ('date_preached', 'posted_by')
    date_hierarchy = 'date_preached'
    ordering = ['-date_preached']


class GeneralOverseerMessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_posted')
    search_fields = ('title', 'description')
    ordering = ['-date_posted']   


admin.site.register(Service, ServiceAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Donation, DonationAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.register(Daily_Devotional, Daily_DevotionalAdmin)
admin.site.register(Sermon, SermonAdmin)
admin.site.register(GeneralOverseerMessage, GeneralOverseerMessageAdmin)

# Register your models here.
