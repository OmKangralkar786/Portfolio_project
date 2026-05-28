from django.db import models
from django.contrib.auth.models import User

class Portfolio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    projects = models.TextField(blank=True)
    school = models.CharField(max_length=200, blank=True)
    college = models.CharField(max_length=200, blank=True)
    linkedin_url = models.URLField(max_length=255, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    puc_marks = models.FileField(upload_to='puc_marks/', blank=True, null=True)
    certificates = models.FileField(upload_to='certificates/', blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)

    def __str__(self):
        return self.full_name

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user.username}"

class Company(models.Model):
    name = models.CharField(max_length=255)  # ✅ Correct field name
    required_skills = models.TextField()
    experience = models.CharField(max_length=50)
    address = models.TextField()
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name
