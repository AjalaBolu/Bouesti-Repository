from django.db import models
from django.contrib.auth.models import User
import uuid

class Journal(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    pdf_file = models.FileField(upload_to='journals/')
    upload_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='journals')  # ✅ make sure this exists


    # 🆕 Additional metadata fields
    abstract = models.TextField(blank=True, null=True)
    keywords = models.CharField(max_length=255, blank=True, null=True)
    doi = models.CharField(max_length=100, unique=True, blank=True, null=True)
    supervisor = models.CharField(max_length=100, blank=True, null=True)
    year = models.PositiveIntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.doi:
            self.doi = f"10.1234/{uuid.uuid4().hex[:8]}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
