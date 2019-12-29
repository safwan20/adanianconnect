from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model) : #one user is asscciated with one profile
    user =  models.OneToOneField(User,on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    image = models.ImageField(default='default.jpg',upload_to='profile_pics')
    tech =  models.TextField(default="None",max_length=10000,null=True)
    lang = models.CharField(default="None",max_length=10000,null=True)
    phone = models.CharField(default="None",max_length=50,null=True)
    link = models.CharField(default="",max_length=5000000,null=True)
    skills = models.TextField(default="None",max_length=5000000,null=True)
    lkes = models.ManyToManyField(User,related_name='likes',blank=True)
    sem = models.CharField(default="",max_length=50,null=True)
    book = models.ManyToManyField(User, related_name='book', blank=True)
    linkin = models.CharField(default="",max_length=5000000,null=True)
    stop = models.CharField(default="", max_length=5000000, null=True)


    def get_absolute_url(self,haj):
        return "/show/" + str(haj)


    def total_likes(self):
        return self.lkes.count()


    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)





class Message(models.Model) :
    id = models.AutoField(primary_key=True)
    to = models.CharField(max_length=50)
    froms = models.CharField(max_length=50)
    read = models.IntegerField(default=0)
    message = models.TextField(max_length=10000)



