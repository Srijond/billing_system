from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import SubscriptionPackageViewSet

router = DefaultRouter()
router.register(r'packages', SubscriptionPackageViewSet, basename='package')

urlpatterns = [
    path('', include(router.urls)),
]