from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser): 
    pass


class bid(models.Model):
    last_bid = models.IntegerField()
    last_bidder = models.OneToOneField(User, on_delete=models.CASCADE, related_name="last_bidder") 
    #done

class comment(models.Model):
    title = models.CharField(max_length=70)
    msg = models.CharField(max_length=300)

    def __str__(self):
        return f"title: {self.title} message : {self.msg}" 
    #done

class list_item(models.Model):
    product_title = models.CharField(max_length=64)
    description = models.CharField(max_length=500)
    seller = models.OneToOneField(User, on_delete=models.CASCADE)
    imageUrl = models.CharField(max_length=1000, blank=True)
    initialBid = models.IntegerField(default=0)
    bid = models.OneToOneField(bid, on_delete=models.CASCADE, blank=True, null=True)
    comments = models.ForeignKey(comment, on_delete=models.CASCADE, blank=True, null=True)
    active_status = models.BooleanField(default=True) 
    #done  
     
class watchlist(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True)
    product_id = models.ForeignKey(list_item, on_delete=models.CASCADE)
    #done 

class category(models.Model):
    category_title = models.CharField(max_length=50, primary_key=True, blank=False)
    product_id = models.ManyToManyField(list_item)
    #done
