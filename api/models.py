import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django_countries.fields import CountryField
from django_filters.rest_framework import FilterSet, CharFilter, NumberFilter
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    USER_CHOICES = [
        ('admin', 'Admin'),
        ('farmer', 'Farmer'),
    ]

    user_type = models.CharField(max_length=10,choices=USER_CHOICES, default='farmer')

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name='api_user_groups',  # Change 'api_user_groups' to your preference
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='api_user_permissions',  # Change 'api_user_permissions' to your preference
    )


class Farmer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name =  models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    country = CountryField()

    def __str__(self):
        return self.name if self.name else self.user.username

class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    
    def __str__(self):
        return self.user.username
    
class OTP(models.Model):
    user = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    timestamp = models.DateTimeField(auto_now_add=True)

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.CharField(max_length=255)
    author = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    publication_datetime = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=50, choices=[('innovation', 'Innovation'), ('market_trends', 'Market Trends'), ('custom', 'Custom')])

class AgricKnowledge(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField

    def __str__(self):
        return self.title


class ProduceListing(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    produce_type = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='produce_images/', blank=True)

    def __str__(self):
        return f"{self.produce_type} - {self.farmer.username}"

class ProduceListingFilter(FilterSet):
    produce_type = CharFilter(field_name='produce_type', lookup_expr='icontains')
    location = CharFilter(field_name='farmer__location', lookup_expr='icontains')
    price_min = NumberFilter(field_name='price', lookup_expr='gte')
    price_max = NumberFilter(field_name='price', lookup_expr='lte')


class ChatMessage(models.Model):
    sender = models.CharField(max_length=255)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    conversation_id = models.UUIDField(default=uuid.uuid4)

class Complaint(models.Model):
    user = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.subject} - {self.farmer.username}"
    
class AdminReply(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply to {self.complaint.subject}"
    
class FarmerReply(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply to {self.complaint.subject}"