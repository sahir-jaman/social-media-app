from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter

from authentication.renderer import UserRenderer
from post_app.models import Post, PostLike, PostComment, User
from post_app.serializers import PostSerializer, PostLikeSerializer, CommentSerializer
from users_app.models import UserConnection
from users_app.serializers import UserConnectionSerializer


class CreatePost(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        context = {"request": request}
        serializer = PostSerializer(context=context, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        user_posts = Post.objects.filter(user=request.user.id)
        serializer = PostSerializer(user_posts, many=True)
        return Response({"posts": serializer.data}, status=status.HTTP_200_OK)


class PostDetail(APIView):
    def get(self, request, uid, format=None):
        try:
            post = Post.objects.get(uid=uid)
        except Post.DoesNotExist:
            return Response(
                {"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, uid, format=None):
        try:
            post = Post.objects.get(uid=uid)
        except Post.DoesNotExist:
            return Response(
                {"message": "Post not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                {"message": "The post updated successfully"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"message": "Error updating post", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, uid, format=None):
        try:
            post = Post.objects.get(uid=uid)
            if post.user.id == request.user.id:
                post.delete()
                return Response(
                    {"success": True, "message": "post deleted"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"success": False, "message": "not enough permissions"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Post.DoesNotExist:
            return Response(
                {"success": False, "message": "post does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class PrivateAllFriendsPosts(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    # serializer_class = PostSerializer
    def get(self, request, format=None):
        # connected_frnds = UserConnection.objects.filter(sender=request.user, connection_status="ACCEPTED").values_list('reciever', flat=True)
        connected_frnds = UserConnection.objects.filter(
            Q(sender=request.user) | Q(reciever=request.user),
            connection_status="ACCEPTED",
        )
        friends = []
        for frnd in connected_frnds:
            if frnd.sender != request.user:
                friends.append(frnd.sender)
            else:
                friends.append(frnd.reciever)

        user_posts = Post.objects.filter(user__in=friends)
        serializer = PostSerializer(user_posts, many=True)
        return Response({"Friends Posts": serializer.data}, status=status.HTTP_200_OK)


class LikePost(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get(self, request, uid):
        try:
            post = Post.objects.get(uid=uid)
            likes_list = PostLike.objects.filter(post=post)

            #  PostComment.objects.create(post=post, user=request.user, comment_text=request.data["comment_text"])
            serializer = PostLikeSerializer(likes_list, many=True)
            return Response({"likes_list": serializer.data}, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response(
                {"success": False, "message": "post does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def post(self, request, uid):
        try:
            post = Post.objects.get(uid=uid)
            new_post_like = PostLike.objects.get_or_create(user=request.user, post=post)
            if not new_post_like[1]:
                new_post_like[0].delete()
                return Response({"status": "post unliked"}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "post liked"}, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response(
                {"success": False, "message": "post does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class CommentPost(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, uid, format=None):
        try:
            post = Post.objects.get(uid=uid)
            comments = PostComment.objects.filter(post=post)
            serializer = CommentSerializer(comments, many=True)
            return Response(
                {"success": True, "comments": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        except Post.DoesNotExist:
            return Response(
                {"success": False, "message": "post does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def post(self, request, uid, format=None):
        try:
            context = {"request": request}
            post = Post.objects.get(uid=uid)
            serializer = CommentSerializer(context=context, data=request.data)
            if serializer.is_valid():
                serializer.save(
                    post=post, user=self.request.user
                )  # Access request object through self.request
                return Response(
                    {"status": "comment added successfully"},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {
                        "message": "error while adding a comment",
                        "errors": serializer.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Post.DoesNotExist:
            return Response(
                {"success": False, "message": "post does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )


# class SerachPost(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         try:
#             users = Post.objects.all()
#             search = request.GET.get("search")

#             if request.GET.get("search"):
#                 users = users.filter(Q(title__icontains=search))

#             serializer = PostSerializer(users, many=True)

#             return Response(
#                 {"Posts": serializer.data, "message": "users fetch successfully"},
#                 status=status.HTTP_200_OK,
#             )

#         except Exception as e:
#             print(e)

#             return Response(
#                 {"posts": [], "message": "Error occurred while fetching posts"},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )
