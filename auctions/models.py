from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser): 
    pass


class list_item(models.Model):
    product_title = models.CharField(max_length=64)
    description = models.CharField(max_length=500)
    seller = models.OneToOneField(User, on_delete=models.CASCADE)
    imageUrl = models.CharField(max_length=1000)
    active_status = models.BooleanField(default=True)
    
    def __str__(self):
        return f"({self.product_title}): {self.description}; seller: {self.seller}; url:{self.imageUrl}"
         
class comment(models.Model):
    product_id = models.ForeignKey(list_item, on_delete=models.CASCADE) 
    comment = models.CharField(max_length=300)
    #done  
     
class watchlist(models.Model):
    userId = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    product_id = models.ForeignKey(list_item, on_delete=models.CASCADE)
    #done 

class bid(models.Model):
    product_id = models.OneToOneField(list_item, on_delete=models.CASCADE, primary_key=True)
    default_bid = models.IntegerField()
    last_bid = models.IntegerField()
    last_bidder = models.OneToOneField(User, on_delete=models.CASCADE, related_name="last_bidder") 
    #done

class category(models.Model):
    category_title = models.CharField(max_length=50, primary_key=True, blank=False)
    product_id = models.ForeignKey(list_item, on_delete=models.CASCADE)
    #done
