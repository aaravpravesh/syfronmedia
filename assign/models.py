from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

# Always get the active user model
User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics/')
    resume = models.FileField(upload_to="Resumes/", default='default_resume.pdf')
    mobile = models.CharField(unique=True, null=True, blank=True)
    skills = models.TextField(max_length=500, null=True, blank=True)
    experience = models.TextField(max_length=500,null=True, blank=True)
    qualification = models.CharField(max_length=50,null=True, blank=True)    
    fname = models.CharField(max_length=20, null=True, blank=True)
    mname = models.CharField(max_length=20, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)


    def __str__(self):
        return f"{self.user.username}'s Profile"


class Assignment(models.Model):
    day = models.PositiveIntegerField()
    embedded_code = models.TextField(help_text="Paste YouTube iframe embed code here")

    def __str__(self):
        return f"Assignment Day {self.day}"


class Submission(models.Model):
    STATUS_CHOICES = [
        (0, 'Not Submitted'),
        (1, 'Submitted'),
    ]

    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name="submissions")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submissions")
    your_html_code = models.TextField(blank=True, null=True)
    your_css_code = models.TextField(blank=True, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)

    class Meta:
        unique_together = ('assignment', 'user')  # Prevent duplicate submissions per assignment-user

    def __str__(self):
        return f"{self.user.username} - Day {self.assignment.day}"
    

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"