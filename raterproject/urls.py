from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from raterapi.views import register_user, login_user, CategoryView, GameViewSet, ReviewViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'categories', CategoryView,'category')
router.register(r'games', GameViewSet,'game')
router.register(r'reviews', ReviewViewSet,'review')


urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
]

