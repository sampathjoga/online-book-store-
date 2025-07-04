# Create your models here.
from django.contrib.auth.models import User
from django.db import models    

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='books/')
    description = models.TextField()

    def __str__(self):
        return self.title

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.book.price * self.quantity
class Login(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    def __str__(self):
        return self.username+self.password
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered_at = models.DateTimeField(auto_now_add=True)
    items = models.ManyToManyField(CartItem)

    def total_cost(self):
        return sum(item.total_price() for item in self.items.all())
