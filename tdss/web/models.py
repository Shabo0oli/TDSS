from django.db import models

# Create your models here.



class Tweet(models.Model):
    Subject = models.CharField(max_length=200 , null=True , blank=True)
    Text = models.TextField()
    RetweetCount = models.IntegerField(default=0)
    FavoriteCount = models.IntegerField(default=0)
    FollowersCount = models.IntegerField(default=0)
    Date = models.DateField(null=True , blank=True)
    Source = models.CharField(max_length=200 , null=True , blank=True)
    Username = models.CharField(max_length=300 , null=True , blank=True)
    Location = models.CharField(max_length=300, null=True, blank=True)


class Featured(models.Model):
    Tweet = models.ForeignKey(Tweet , on_delete=models.CASCADE)
    Reliability = models.IntegerField(default=0)
    Popularity = models.IntegerField(default=0)
    Polarity = models.IntegerField(default=0)

class Plot(models.Model):
    Image = models.ImageField(upload_to='figures/')