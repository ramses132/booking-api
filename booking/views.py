from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_json_api import views
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
import requests
from django.db.models import Count, F
from booking import models, serializers, permissions
from drf_yasg import openapi


class UserViewSet(views.ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        return queryset.filter(id=user.id)


class RoomViewSet(views.ModelViewSet):
    permission_classes = (permissions.IsBusiness, )
    serializer_class = serializers.RoomSerializer
    queryset = models.Room.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.events.exists():
            return Response(data="Error: room has at least one event", status=status.HTTP_400_BAD_REQUEST)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class EventListCreateApiView(permissions.PermissionMixin, views.generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    permission_classes_per_method = {
        'create': [permissions.IsBusiness, ]
    }
    serializer_class = serializers.EventSerializer
    queryset = models.Event.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user and self.request.user.role == self.request.user.CUSTOMER:
            return queryset.annotate(
                places_booked=Count("books")
            ).filter(
                places_booked__lt=F("room__capacity"),
                event_type=models.Event.PUBLIC
            )
        return queryset

    def create(self, request, *args, **kwargs):
        # data = request.data
        # room_pk = data["room"]
        # room = models.Room.objects.get(pk=room_pk)
        # data.update({
        #     "room": room
        # })
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        date = serializer.validated_data["date"]
        room = serializer.validated_data["room"]
        if models.Event.objects.filter(date=date, room=room).exists():
            
            return Response(data=f"Error: room {room} already has an event on {date} ", status=status.HTTP_400_BAD_REQUEST)
    
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class BookCreateApiView(views.generics.CreateAPIView):
    permission_classes = (permissions.IsCustomer, )
    serializer_class = serializers.BookSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        event = serializer.validated_data['event']
        if event.event_type != models.Event.PUBLIC:
            return Response(data="event must be public", status=status.HTTP_400_BAD_REQUEST)

        if event.room.capacity - event.books.count() <= 0:
            return Response(data="event room capacity is allocated", status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class BookCancelApiView(views.generics.DestroyAPIView):
    permission_classes = (permissions.IsCustomer, )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.customer:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(request_body=serializers.LogoutSerializer)
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as err:
            print(err)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):
    permission_classes = ()

    @swagger_auto_schema(request_body=serializers.RegisterSerializer)
    def post(self, request):
        # Validating our serializer from the UserRegistrationSerializer
        serializer = serializers.RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Everything's valid, so send it to the UserSerializer
        model_serializer = serializers.UserSerializer(data=serializer.data)
        model_serializer.is_valid(raise_exception=True)
        user = model_serializer.save()
        refresh = RefreshToken.for_user(user)
        response = {
            "user": model_serializer.data,
            "auth": {"refresh": str(refresh), "access": str(refresh.access_token)},
        }

        return Response(response)
