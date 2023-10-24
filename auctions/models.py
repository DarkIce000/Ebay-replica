from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser): 
    pass


class list_items(models.Model):
    id = models.AutoField(primary_key=True)
    product_title = models.CharField(max_length=64)
    description = models.CharField(max_length=500)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    imageUrl = models.CharField(max_length=1000)
    active_status = models.BooleanField(default=True)
    #done

class comments(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ManyToManyField(list_items, blank=True) 
    comment = models.CharField(max_length=300)
    #done  
     
class watchlist(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ManyToManyField(list_items, blank=True)
    #done 

class bid(models.Model):
    product_id = models.ForeignKey(list_items, on_delete=models.CASCADE)
    default_bid = models.IntegerField()
    last_bid = models.IntegerField()
    last_bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="last_bidder") 
    #done

class categories(models.Model):
    category_title = models.CharField(max_length=50, primary_key=True)
    product_id = models.ManyToManyField(list_items, blank=True)
    #done
