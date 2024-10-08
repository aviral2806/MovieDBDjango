from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.contrib.auth.models import User

# Create your models here.
class WatchList(models.Model):
    title = models.CharField(max_length=32)
    storyline = models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    avg_rating = models.FloatField(default=0)
    number_rating = models.IntegerField(default=0)
    platform = models.ForeignKey("StreamPlatform",on_delete=models.CASCADE,related_name="watchlist",default="1")
    
    def __str__(self):
        return self.title
    
class StreamPlatform(models.Model):
    name = models.CharField(max_length=32)
    about = models.CharField(max_length=200)
    website = models.URLField(max_length=200)
    
    def __str__(self):
        return self.name
    
class Review(models.Model):
    review_user = models.ForeignKey(User,on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    description = models.TextField(max_length=200,null=True)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    watchlist = models.ForeignKey(WatchList,on_delete=models.CASCADE,related_name="reviews")
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.rating) + ' | ' + self.watchlist.title