from rest_framework import serializers
from post_app.models import Post, PostComment, PostLike
from authentication.models import User


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ["uid", "updated_at"]

    # user = serializers.PrimaryKeyRelatedField(read_only=True)
    # post = serializers.PrimaryKeyRelatedField(read_only=True)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = "__all__"

    comment = serializers.CharField(max_length=264)
    user = serializers.CharField(default=serializers.CurrentUserDefault())
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    def save(self, **kwargs):
        print(kwargs)
        self.post = kwargs["post"]
        return super().save(**kwargs)


class PostSerializer(serializers.ModelSerializer):
    # search = serializers.CharField()

    class Meta:
        model = Post
        fields = [
            "uid",
            "title",
            "description",
            "uploaded_photo",
            "user",
            "created_at",
            "updated_at",
        ]

    title = serializers.CharField()
    description = serializers.CharField()
    user = serializers.CharField(default=serializers.CurrentUserDefault())

    def update(self, instance, validated_data):
        print(validated_data)
        # if instance.user.id == validated_data["user"].id:
        return super().update(instance, validated_data)
