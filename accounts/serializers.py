from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from rest_framework import serializers
from .models import User
from .models import EmployerProfile, ConsultancyProfile, CandidateProfile



class UserCreateSerializer(BaseUserCreateSerializer):
    re_password = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=True)
    name = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    user_type = serializers.ChoiceField(choices=User.USER_TYPES, required=True)

    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'name', 'phone', 'password', 're_password', 'user_type')

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_phone(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Phone number should contain only digits.")
        if len(value) < 10:
            raise serializers.ValidationError("Phone number should be at least 10 digits.")
        return value

    def validate_user_type(self, value):
        if value not in dict(User.USER_TYPES).keys():
            raise serializers.ValidationError("Invalid user type. Must be one of: employer, consultancy, candidate")
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['re_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('re_password', None)
        return super().create(validated_data)


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ('id', 'email', 'name', 'phone', 'user_type')


# Employer Profile Serializer
class EmployerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployerProfile
        fields = '__all__' 
        read_only_fields = ['user']


# Consultancy Profile Serializer
class ConsultancyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultancyProfile
        fields = '__all__'
        read_only_fields = ['user']


# Candidate Profile Serializer
class CandidateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateProfile
        fields = '__all__'
        read_only_fields = ['user']

