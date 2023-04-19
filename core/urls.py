from django.urls import path, include
from rest_framework.routers import SimpleRouter

from core import views


user_router = SimpleRouter()
user_router.register(r'users', views.UserViewSet, basename="users")

post_router = SimpleRouter()
post_router.register(r'posts', views.PostViewSet, basename="posts")

comment_router = SimpleRouter()
comment_router.register(r'comments', views.CommentViewSet, basename="comments")


urlpatterns = [
    path('auth/', views.AuthView.as_view()),
    path('', include(user_router.urls)),
    path('', include(post_router.urls)),
    path('', include(comment_router.urls)),
]


