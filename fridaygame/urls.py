from django.urls import path, include
from rest_framework.routers import SimpleRouter

from fridaygame import views as fg_views

router = SimpleRouter()

router.register(r'users', fg_views.UserViewSet)
router.register(r'games', fg_views.GameViewSet)
router.register(r'teams', fg_views.TeamViewSet)
router.register(r'votes', fg_views.VoteViewSet)

urlpatterns = [
    path('', include(router.urls,))
]

