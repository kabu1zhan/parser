from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('auth/<str:domain>', views.VkAuth.as_view()),
    path('auth/<str:domain>/analyze/posts', views.StartAnalyse.as_view()),
    path('auth/<str:domain>/analyze/detail/posts', views.GetIds.as_view()),
    path('auth/<str:domain>/analyze/comments', views.StartAnalyseComments.as_view()),
    path('auth/<str:domain>/analyze/detail/comments', views.DetailAnaliseComments.as_view()),
    path('auth/post/<int:post_id>', views.GetPost.as_view()),
    path('auth/comment/<int:post_id>', views.GetAllComment.as_view()),
    path('auth/comment/id/<int:comment_id>', views.GetComment.as_view()),
    path('auth/user/<int:user_id>', views.GetUser.as_view()),
    path('auth/bad_word/add', views.AddBadWord.as_view()),
    path('auth/bad_word/get', views.GetBadWord.as_view()),

    path('auth/<str:domain>/analyze/detail/ids', views.GetIds.as_view()),
    path('auth/<str:domain>/analyze/detail/commentsIds', views.GetCommentIds.as_view()),
    path('auth/<str:domain>/analyze/detail/bad', views.GetBadWords.as_view()),

    path('auth/bad_data/add', views.BadData.as_view()),
    path('auth/group/add', views.AddGroup.as_view()),
    path('auth/comment/add', views.AddComment.as_view()),

    path('user/add', views.AddUserApi.as_view()),
    path('group/add', views.GroupApi.as_view())
]
