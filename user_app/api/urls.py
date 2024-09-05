from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from user_app.api.views import RegisterUser,LogoutView,LoginUser
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns = [
    path('login/',LoginUser,name='login-user'),
    path('register/',RegisterUser,name='register-user'),
    path('logout/',LogoutView,name='logout-user'),
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]