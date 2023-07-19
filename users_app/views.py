from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from authentication.renderer import UserRenderer
from authentication.models import User
from authentication.serializers import PublicUserRegistrationSerializer
from users_app.models import UserConnection
from users_app.serializers import (
    PrivateUserProfileDetailSerializer,
    UserConnectionSerializer,
)

import json


# Create your views here.
class PrivateUserProfileViewDetail(APIView):
    queryset = User.objects.all()
    serializer_class = PrivateUserProfileDetailSerializer
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None, pk=None):
        search_query = request.query_params.get("search", None)
        queryset = self.queryset

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | Q(email__icontains=search_query)
            )
        else:
            serializer = PrivateUserProfileDetailSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        serializer = PrivateUserProfileDetailSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        serializer = self.serializer_class(
            request.user, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            username = request.user
            message = f"{username} updated his profile successfully"
            return Response(
                {"success": True, "message": message},
                status=status.HTTP_202_ACCEPTED,
            )
        else:
            print(serializer.errors)
            return Response(
                {"success": False, "message": serializer.errors},
            )


class RetrieveUser(APIView):
    def get(self, request, uid, format=None):
        try:
            user = User.objects.get(uid=uid)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = PrivateUserProfileDetailSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DestroyUser(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, format=None):
        try:
            user = User.objects.get(id=pk)
            if pk == request.user.id:
                self.perform_destroy(request.user)
                return Response(
                    {"success": True, "message": "user deleted"},
                    status=status.HTTP_202_ACCEPTED,
                )
            else:
                return Response(
                    {"success": False, "message": "not enough permissions"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except User.DoesNotExist:
            return Response(
                {"success": False, "message": "user does not exist"},
                status=status.HTTP_200_OK,
            )


# managing friend request
class UserConnectionView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    # creating user_connection
    def post(self, request, uid, formate=None):
        user_reciever = User.objects.get(uid=uid)  # sahir

        is_prev_connection = UserConnection.objects.filter(
            sender=user_reciever, reciever=request.user
        )

        if is_prev_connection:
            return Response({"message": "User has already sent you a friend request"})
        elif request.user == user_reciever:
            return Response({"message": "You Cannot sent friend request to yourself"})
        else:
            user_connection = UserConnection.objects.filter(
                sender=request.user, reciever=user_reciever
            )
            if user_connection:
                user_connection.delete()
                return Response(
                    {"status": "Friend request cancelled"},
                    status=status.HTTP_201_CREATED,
                )
            else:
                user_connection = UserConnection.objects.create(
                    sender=request.user, reciever=user_reciever
                )
                message = f"Friend request sent to {user_connection.reciever.email}"
                return Response({"status": message}, status=status.HTTP_201_CREATED)

    # see all frnd request list
    def get(self, request):
        sender = UserConnection.objects.filter(sender=request.user)
        reciever = UserConnection.objects.filter(reciever=request.user)

        print(f"-------- {request.user}")
        print(f"-------- {reciever.__dict__}")

        sender_serializer = UserConnectionSerializer(sender, many=True)
        reciever_serializer = UserConnectionSerializer(reciever, many=True)
        return Response(
            {
                "following": sender_serializer.data,
                "followers": reciever_serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )

    # accept or decline request
    def put(self, request, uid, format=None):
        connection_obj = UserConnection.objects.get(uid=uid)
        serializer = UserConnectionSerializer(
            connection_obj, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            if connection_obj.connection_status == "ACCEPTED":
                return Response(
                    {"message": "Friend request Accepted"},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {"message": "Friend request Declined"},
                    status=status.HTTP_201_CREATED,
                )
        return Response(
            "User has not given you any request", status=status.HTTP_400_BAD_REQUEST
        )
