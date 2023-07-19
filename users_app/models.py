from django.db import models
from authentication.models import User
from .basemodel import BaseModel


class UserConnection(BaseModel):
    CHOICES = [
        ("PENDING", "pending"),
        ("ACCEPTED", "accepted"),
        ("DECLINED", "declined"),
    ]

    sender = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name="sender") 
    reciever = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name="reciever")
    connection_status = models.CharField(max_length=20, choices=CHOICES, default="PENDING")

    # def __str__(self):
    #     return self.sender.email

    def update(self, instance, validated_data):
        print(validated_data)
        # if instance.user.id == validated_data["user"].id:
        return super().update(instance, validated_data)
