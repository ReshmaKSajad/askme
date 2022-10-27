from django.db import models
from django.contrib.auth.models import User,AbstractUser

class MyUser(AbstractUser):
    phone = models.CharField(max_length=200)
    profile_pic = models.ImageField(upload_to="profilepics",null=True)


class Questions(models.Model):
    question = models.CharField(max_length=500)
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE)
    image = models.ImageField(null=True,upload_to="Q-images",blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default = True)

    def __str__(self):
        return self.question


class Answers(models.Model):
    question = models.ForeignKey(Questions,on_delete=models.CASCADE)
    answer = models.CharField(max_length=500)
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE)
    upvote = models.ManyToManyField(MyUser,related_name="support")
    image = models.ImageField(upload_to="A-images",null=True)
    posted_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.answer