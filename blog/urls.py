from django.urls import path
from .import views
from .views import CustomLogoutView
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView


urlpatterns = [
    path('blog/', views.index, name='blog-index'),
    path('post_detail/<int:pk>/', views.post_detail, name='blog-post-detail'),
    path('post_edit/<int:pk>/', views.post_edit, name='blog-post-edit'),
    path('post_delete/<int:pk>/', views.post_delete, name='blog-post-delete'),
    
    path('logout/success/', TemplateView.as_view(template_name="logout.html"), name='users-logout-success'),
]
