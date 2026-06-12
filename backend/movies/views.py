from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

# ۱. API ثبت‌نام کاربر جدید
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
    user = User.objects.create_user(username=username, password=password)
    
    # تولید توکن برای کاربر ثبت‌نام شده تا بلافاصله لاگین شود
    refresh = RefreshToken.for_user(user)
    return Response({
        'message': 'User registered successfully!',
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }, status=status.HTTP_201_CREATED)


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Movie, UserAction
from .serializers import MovieSerializer

# ۱. دریافت لیست همه فیلم‌ها + قابلیت سرچ و فیلتر ژانر
@api_view(['GET'])
@permission_classes([AllowAny]) # همه می‌تونن فیلم‌ها رو ببینن
def get_movies(request):
    movies = Movie.objects.all()
    
    # قابلیت سرچ بر اساس نام فیلم
    search_query = request.query_params.get('search', None)
    if search_query:
        movies = movies.filter(title__icontains=search_query)
        
        # اگر کاربر لاگین بود، این سرچ رو توی تاریخچه‌اش ذخیره کن
        if request.user.is_authenticated:
            UserAction.objects.create(user=request.user, search_query=search_query, action_type='search')

    # قابلیت فیلتر بر اساس ژانر
    genre_filter = request.query_params.get('genre', None)
    if genre_filter:
        movies = movies.filter(genre__icontains=genre_filter)
        
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


# ۲. ثبت کلیک روی یک فیلم خاص
@api_view(['POST'])
@permission_classes([IsAuthenticated]) # فقط کاربران لاگین شده
def log_click(request, movie_id):
    try:
        movie = Movie.objects.get(id=movie_id)
        UserAction.objects.create(user=request.user, movie=movie, action_type='click')
        return Response({'message': f'Click logged for movie: {movie.title}'}, status=status.HTTP_201_CREATED)
    except Movie.DoesNotExist:
        return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
    


from .ai_service import get_ai_recommendations

@api_view(['GET'])
@permission_classes([IsAuthenticated]) # فقط کاربرانی که لاگین کردند سابقه دارند
def recommend_movies(request):
    recommendations = get_ai_recommendations(request.user)
    
    if recommendations is None:
        return Response({'error': 'Failed to fetch recommendations from AI'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    # برگرداندن پاسخ نهایی هوش مصنوعی به فرانت‌اَند
    return Response(recommendations)