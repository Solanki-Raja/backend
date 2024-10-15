from django.contrib import admin
from django.urls import path, include
from api.views import HomeView , ImagePredictor
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  #  app-level URLs must be included to catch app urls
    path('api/home/', HomeView.as_view(), name='home'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('predict/', ImagePredictor.as_view(), name='image-predictor'),
]

