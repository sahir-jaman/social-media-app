from django.db import models
from authentication.models import User
from users_app.basemodel import BaseModel

# Create your models here.
class Post(BaseModel):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, null=True, blank=True)
    uploaded_photo = models.ImageField(upload_to='images', null=True, blank = True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

class PostLike(BaseModel):
    post = models.ForeignKey(Post, null=False, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("post", "user"), )

class PostComment(BaseModel):
    comment = models.CharField(max_length=264)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, null=False, on_delete=models.CASCADE)
