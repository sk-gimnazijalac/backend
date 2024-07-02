from django.utils import timezone
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Post
from .serializers import CreatePostSerializer, GetPostSerializer


class PostView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request, *args, **kwargs):
        result = Post.objects.all()
        serializers = GetPostSerializer(result, many=True)
        return Response({'status': 'success', "posts": serializers.data}, status=200)

    def post(self, request):
        data = {
            'description': request.data.get('description'),
            'shortDescription': request.data.get('shortDescription'),
            'title': request.data.get('title'),
            'src': request.data.get('src'),
            'author': request.user.id,
            'date': timezone.now().date()
        }
        serializer = CreatePostSerializer(data=data)
        if serializer.is_valid():
            instance = serializer.save()
            return Response({"status": "success", "id": instance.id}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        post_id = kwargs.get('id')
        try:
            post = Post.objects.get(id=post_id)
            post.delete()
            return Response({"status": "success", "data": "Post deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist:
            return Response({"status": "error", "data": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
