from rest_framework import viewsets, generics, status
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.views import APIView
from taggit.models import Tag
from .pagination import PageSetPagination
from .serializers import PostSerializer, TagSerializer, ContactSerializer, UserSerializer, RegisterSerializer, \
    CommentSerializer
from .models import Post, Comment
from rest_framework import permissions
from django.core.mail import send_mail


class PostViewSet(viewsets.ModelViewSet):
    search_fields = ['$content', '$h1']
    filter_backends = (filters.SearchFilter,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]
    pagination_class = PageSetPagination


class TagPostView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = PageSetPagination

    def get_queryset(self):
        tag_slug = self.kwargs['tag_slug'].capitalize()
        queryset = Post.objects.filter(tags__name__in=[tag_slug])
        return queryset


class TagsView(generics.ListAPIView):
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Tag.objects.all()


class LastPostsView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Post.objects.order_by('-id')[:3]


class FeedBackView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ContactSerializer

    def post(self, requests, *args, **kwargs):
        serializer = self.serializer_class(data=requests.data)
        if serializer.is_valid():
            subject = serializer.data['subject']
            message = serializer.data['message']
            email = serializer.data['email']
            name = serializer.data['name']
            name1 = requests.user.username
            send_mail(f'От {name} ({name1}) | {subject}', message, email, ['nikkres@mail.ru'])
            return Response({"success": "Sent"})
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "Пользователь успешно создан",
        })


class ProfileView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return Response({
            "user": UserSerializer(request.user, context=self.get_serializer_context()).data,
        })


class CommentView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        title_slug = self.kwargs['title_slug']
        post = Post.objects.get(slug=title_slug)
        return post.comment.all()

