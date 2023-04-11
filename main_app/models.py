from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Toy(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('toy_detail', kwargs={'pk': self.id})

class Cat(models.Model):
    name = models.CharField(max_length=100) # varchar datatype
    breed = models.CharField(max_length=100)
    description = models.TextField(max_length=250) # text datatype
    age = models.IntegerField(default=0)
    toys = models.ManyToManyField(Toy)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('cat_detail', kwargs={'cat_id': self.id})
    
class Feeding(models.Model):
    MEALS = (
        ('B', 'Breakfast'),
        ('L', 'Lunch'),
        ('D', 'Dinner'),
    )
    date = models.DateField()
    meal = models.CharField(max_length=1, choices=MEALS, default=MEALS[0][0])
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.get_meal_display()} on {self.date}'
        # NOTE: when a field has a choices kw arg we can use the get_<fieldname>_display()
        # method to display the human friendly version of the single character value
        # https://docs.djangoproject.com/en/4.1/ref/models/fields/

    class Meta:
        ordering = ['-date']

class Photo(models.Model):
    url = models.CharField(max_length=200)
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)

    def __str__(self):
        return f'Photo for cat_id: {self.cat_id} @{self.url}'
    