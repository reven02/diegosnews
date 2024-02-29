from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User 

# Create your models here.

class Story(models.Model):
    headline = models.CharField(max_length=64)
    category = models.CharField(max_length=8, choices={'pol': 'Politics', 'art': 'Art', 'tech': 'Tech', 'trivia': 'Trivia'})
    region = models.CharField(max_length=8, choices={'uk': 'United Kingdom', 'eu': 'Europe', 'w': 'World'})
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    details = models.CharField(max_length=128)

    def __str__(self):
        return self.headline
    
    def serialize(self):
        return {
            'key': self.pk,
            'headline': self.headline,
            'category': self.category,
            'region': self.region,
            'author': self.author.first_name,
            'date': self.date.strftime('%d/%m/%Y'),
            'details': self.details,   
        }

