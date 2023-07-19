from rest_framework import serializers

from authentication.models import User
from users_app.models import UserConnection


class PrivateUserProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "uid",
            "email",
            "name",
            "profile_picture",
            "bio",
            "is_active",
            "is_admin",
            "created_at",
        ]
        # fields = '__all__'


class UserConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserConnection
        # fields = ["uid","sender", "reciever", "connection_status"]
        fields = ["uid", "connection_status"]

    # def update(self, instance, validated_data):
    #     print("serializer validated data->$$$$$$$$$$$->>>>>>",validated_data)
    #     # if instance.user.id == validated_data["user"].id:
    #     return super().update(instance, validated_data)
