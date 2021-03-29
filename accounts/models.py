from django.contrib import auth
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):

    DEPARTMENT = (
        (
        ('IT', (
            ('Reports & Data Analyst', 'Reports & Data Analyst'),
            ('End User Support', 'End User Support'),
            ('IT Manager', 'IT Manager'),
            ('IT Supervisor', 'IT Supervisor'),
        )),
        ('Sales', (
            ('Sales Supervisor', 'Sales Supervisor'),
            ('Operational Manager', 'Operational Manager'),
            ('Seller', 'Seller'),
            ('Key Accounts Executive', 'Key Accounts Executive'),
            ('PSG', 'PSG'),
        )),
        ('HR', (
            ('HR Manager', 'HR Manager'),
            ('HR Supervisor', 'HR Supervisor'),
            ('HR Staff', 'HR Staff'),
        )),
    )
    )

    ASSIGNED_SITE = (
        ('RGPI Pasig', 'RGPI Pasig'),
        ('RGPI Calamba', 'RGPI Calamba'),
        ('RGPI Silang', 'RGPI Silang'),
        ('RGPI Sta. Cruz', 'RGPI Sta. Cruz'),
        ('RGPI Sta. Lipa', 'RGPI Sta. Lipa'),
        ('RGPI Sta. Balayan', 'RGPI Sta. Balayan'),
        ('RGPI Sta. Antipolo', 'RGPI Sta. Antipolo'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(max_length=100, blank=True)
    address = models.TextField(max_length=100, blank=True)
    contact_no = models.TextField(max_length=20, blank=True)
    site = models.CharField(max_length=30,choices=ASSIGNED_SITE, default="-------------")
    department = models.CharField(max_length=30,choices=DEPARTMENT, default="-------------")
    image = models.ImageField(null=True,blank = True, upload_to = 'profile_pics/', default= 'default.jpg')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


