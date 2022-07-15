from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

from applications.account.send_mail import send_confirmation_email

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(min_length=6, write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.pop('password2')

        if password != password2:
            raise serializers.ValidationError('password did not math')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        code = user.activation_code
        send_confirmation_email(code, user.email)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь не зарегестрирован!!!')
        return email

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError("Wrong email or password")
            attrs['user'] = user
            return attrs


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    password = serializers.CharField(required=True, min_length=6)
    password2 = serializers.CharField(required=True, min_length=6)

    def validate_old_password(self, p):
        user = self.context.get('request').user
        if not user.check_password(p):
            raise serializers.ValidationError('Wrong password')
        return p

    def validate(self, attrs):
        p1 = attrs.get('password')
        p2 = attrs.get('password2')
        if p1 != p2:
            raise serializers.ValidationError('passwords did not match')
        return attrs

    def set_new_password(self):
        user = self.context.get('request').user
        password = self.validated_data.get('password')
        user.set_password(password)
        user.save()