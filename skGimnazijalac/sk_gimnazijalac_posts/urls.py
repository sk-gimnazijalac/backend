from .views import PostView, ImageView
from django.urls import path


urlpatterns = [
    path('post', PostView.as_view()),
    path('post/<int:id>', PostView.as_view()),
    path('post/image/<int:id>', ImageView.as_view()),
]
