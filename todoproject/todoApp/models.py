from django.db import models
from django.utils import timezone
from django.utils.text import slugify

# Create your models here.
class userModel(models.Model):
    firstname=models.CharField(max_length=30)
    lastname=models.CharField(max_length=30)
    username=models.CharField(max_length=30)
    password=models.CharField(max_length=30)
    phone=models.IntegerField()
    email=models.EmailField()
    slug=models.SlugField(default='',null=False)

    def save(self, *args, **kwargs):
        # Auto-generate slug from firstname and lastname
        self.slug = slugify(self.firstname + '-' + self.lastname)
        super(userModel, self).save(*args, **kwargs)

class task(models.Model):
    user=models.ForeignKey(userModel,on_delete=models.CASCADE)
    title=models.CharField(max_length=30)
    description=models.TextField()
    date=models.DateField(default=timezone.now)


    


