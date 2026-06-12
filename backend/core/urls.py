from django.contrib import admin
from django.urls import path
from movies.views import register_user
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from movies.views import register_user, get_movies, log_click, recommend_movies 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/register/', register_user, name='register'),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # مسیرهای فیلم و رفتارهای کاربر
    path('api/movies/', get_movies, name='get_movies'),
    path('api/movies/<int:movie_id>/click/', log_click, name='log_click'),
    path('api/movies/recommendations/', recommend_movies, name='recommendations'),
]