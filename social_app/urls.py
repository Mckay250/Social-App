
from django.urls import path

from .views import (CreatePostView, DeletePostView, LikePostView, GetPostView,
    ListPostView, SignUpView, UnlikePostView, UpdatePostView, UserView)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



urlpatterns = [
    path('sign-up', SignUpView.as_view(), name='sign_up'),
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),\
    path('user', UserView.as_view(), name='user_details'),
    path('posts', ListPostView.as_view(), name='list_posts'),
    path('post/create', CreatePostView.as_view(), name='create_post'),
    path('post/update', UpdatePostView.as_view(), name='update_post'),
    path('post/delete', DeletePostView.as_view(), name='delete_post'),
    path('post/like', LikePostView.as_view(), name='like_post'),
    path('post/unlike', UnlikePostView.as_view(), name='unlike_post'),
    path('post/<str:id>', GetPostView.as_view(), name='get_post')
]


