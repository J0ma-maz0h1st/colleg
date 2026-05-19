from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NewsViewSet, FAQViewSet, AboutSectionViewSet

router = DefaultRouter()
router.register(r'news', NewsViewSet, basename='news')
router.register(r'faq', FAQViewSet, basename='faq')
router.register(r'about', AboutSectionViewSet, basename='about')

urlpatterns = [
    path('', include(router.urls)),
]