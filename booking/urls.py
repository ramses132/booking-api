from rest_framework.routers import SimpleRouter

from django.urls import path, re_path
from booking import views

r = SimpleRouter(trailing_slash=False)

r.register(r"users", views.UserViewSet)
r.register(r"rooms", views.RoomViewSet)

urlpatterns = [
    path("events", views.EventListCreateApiView.as_view()),
    path("book", views.BookCreateApiView.as_view()),
    path("book/<int:id>", views.BookCancelApiView.as_view())
]


urlpatterns += r.urls
