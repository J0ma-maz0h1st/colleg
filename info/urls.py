from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NewsViewSet, FAQViewSet, AboutSectionViewSet, StatisticsViewSet

router = DefaultRouter()
router.register(r'news', NewsViewSet, basename='news')
router.register(r'faq', FAQViewSet, basename='faq')
router.register(r'about', AboutSectionViewSet, basename='about')
router.register(r'statistics', StatisticsViewSet, basename='statistics')

urlpatterns = [
    path('', include(router.urls)),
]