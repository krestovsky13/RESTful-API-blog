from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, TagPostView, TagsView, LastPostsView, FeedBackView, RegisterView, ProfileView, \
    CommentView

router = DefaultRouter()
router.register('posts', PostViewSet, basename='posts')

urlpatterns = [
    path("", include(router.urls)),
    path('tags/', TagsView.as_view()),
    path('tags/<slug:tag_slug>/', TagPostView.as_view()),
    path('aside/', LastPostsView.as_view()),
    path('contact/', FeedBackView.as_view()),
    path('register/', RegisterView.as_view()),
    path('profile/', ProfileView.as_view()),
    path("comments/", CommentView.as_view()),
    path("comments/<slug:title_slug>/", CommentView.as_view())
]
