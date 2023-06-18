from django.urls import path
from blogs.views import (
    AddBlogsListView,
    SignupCreateView,
    CreateBlogsCreateView,
    CommentCreateView,
    BlogsListView,
    BlogDetailsListView,
    BloggerDetailsListView,
    BloggersListView,
    BlogUpdateView,
    BlogDeleteView,
    CommentUpdateView,
    CommentDeleteView,
    UserUpdateView,
    UserDeleteView,
    ProfileUpdateForm
)

urlpatterns = [
    path("", AddBlogsListView.as_view(), name="home"),
    path("signup/", SignupCreateView.as_view(), name="signup"),
    path("Create_blogs/", CreateBlogsCreateView.as_view(), name="create_blogs"),
    path("<int:id>/create/", CommentCreateView.as_view(), name="create"),
    path("blogs/", BlogsListView.as_view(), name="blogs"),
    path("<int:id>", BlogDetailsListView.as_view(), name="bloginfo"),
    path("blogger/<int:id>/", BloggerDetailsListView.as_view(), name="blogger"),
    path("bloggers/", BloggersListView.as_view(), name="bloggers"),
    path("update/blog/<int:pk>/", BlogUpdateView.as_view(), name="update_blog"),
    path("delete/blog/<int:pk>/", BlogDeleteView.as_view(), name="delete_blog"),
    path("update/comment/<int:pk>/", CommentUpdateView.as_view(), name="update_comment"),
    path("delete/comment/<int:pk>/", CommentDeleteView.as_view(), name="delete_comment"),
    path("update/blogger/<int:pk>/", UserUpdateView.as_view(), name="update_blogger"),
    path("delete/blogger/<int:pk>/", UserDeleteView.as_view(), name="delete_blogger"),
    path("profile/<int:pk>/", ProfileUpdateForm.as_view(), name="profile"),
]
