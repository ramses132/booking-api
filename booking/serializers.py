from django.contrib.auth import get_user_model
from rest_framework_json_api import serializers
from .models import Room, Event, Book

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    name = serializers.CharField(source="first_name")

    class Meta:
        model = get_user_model()
        fields = get_user_model().REQUIRED_FIELDS + [get_user_model().USERNAME_FIELD, "name"]


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    name = serializers.CharField()
    password = serializers.CharField()
    confirm = serializers.CharField()

    def validate_email(self, email):
        existing = User.objects.filter(email=email).first()
        if existing:
            raise serializers.ValidationError(
                "Someone with that email "
                "address has already registered. Was it you?"
            )
        return email

    def validate(self, data):
        if not data.get("password") or not data.get("confirm"):
            raise serializers.ValidationError(
                "Please enter a password and "
                "confirm it."
            )
        if data.get("password") != data.get("confirm"):
            raise serializers.ValidationError("Those passwords don't match.")
        return data


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ["id", "name", "date", "room", "event_type"]


class RoomSerializer(serializers.ModelSerializer):
    events = EventSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ["id", "name", "capacity", "events"]


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "event", "customer"]
