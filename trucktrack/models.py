from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(default = None, null=True,max_length=100)
    city = models.CharField(max_length=100, default=None, blank=True, null=True)
    truck_tonnage = models.IntegerField(default=None, null=True, blank=True)

class Orders(models.Model):
    title =models.CharField(max_length = 100)
    text = models.TextField()
    sender = models.ForeignKey("Cities", on_delete=models.CASCADE, related_name ="departures" , default= None)
    receiver = models.ForeignKey("Cities", on_delete=models.CASCADE, related_name ="arrivals", default=None)
    bid = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    perform =models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, related_name="perform")
    visability = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add = True)
    tonnage=models.IntegerField()
    type=models.ForeignKey("Type", on_delete=models.CASCADE)
    find=models.BooleanField(default = True)

    def __str__(self):
        return f"From {self.sender} to {self.receiver} need to {self.title} with {self.bid} and {self.perform} and {self.visability} and {self.find}"

class Cities(models.Model):
    city = models.CharField(max_length = 100)

    def __str__(self):
        return f"The city name : {self.city}"
    
class Grade(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    grade = models.IntegerField()
    comentator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comentator")
    comment = models.CharField(max_length = 100)
    timestamp = models.DateTimeField(auto_now_add=True)


class Performers(models.Model):
    order = models.ForeignKey(Orders,on_delete=models.CASCADE)
    performer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.performer.id} on {self.order.id}"


class Type(models.Model):
    type = models.CharField(max_length=100)

class Chat(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name ="writer")
    message = models.CharField(max_length=100, null= True, blank=True)
    chat_number = models.ForeignKey("Chats", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.writer} have {self.message} and {self.chat_number}"

class Chats(models.Model):
    chat_id =models.ForeignKey(User, on_delete=models.CASCADE, related_name="chat_id")
    main_user = models.ForeignKey(User,on_delete=models.CASCADE, related_name ="main_user")
    second_user= models.ForeignKey(User,on_delete=models.CASCADE, related_name ="second_user")
    number = models.IntegerField()
    