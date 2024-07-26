from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'bookings', BookingViewSet)
router.register(r'menus', MenuViewSet)

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('viewsets', include(router.urls)),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]