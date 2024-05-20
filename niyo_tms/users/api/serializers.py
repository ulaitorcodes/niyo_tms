from rest_framework import serializers

from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'first_name', 'last_name', 'email', 'photo', 'created_at']
        read_only_fields = ['created_at']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255, write_only=True)
    password_confirmation = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'password_confirmation')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
            'password': {'required': True},
            'password_confirmation': {'required': True},
        }

    def validate(self, data):
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError({'password_confirmation': 'Passwords don\'t match'})
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirmation')
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user