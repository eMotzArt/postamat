from datetime import date

from django.contrib.auth.password_validation import validate_password, MinimumLengthValidator
from django.core.validators import validate_email
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.models import User, Post, Comment
from core.validators import IsNumbersIncluded, DomainValidator


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['login', 'password']

class UserCreateUpdateDestroySerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

    def validate_password(self, password):
        validate_password(password, password_validators=[MinimumLengthValidator(8), IsNumbersIncluded()])
        return password

    def validate_email(self, email):
        validate_email(email)
        DomainValidator().validate(email)
        return email

    class Meta:
        model = User
        fields = ('login', 'password', 'phone', 'birthday', 'email')

        read_only_fields = [
            'id',
            'last_login',
            'created_at',
            'edited_at',
            'is_superuser',
            'is_staff',
            'is_active',
            'date_joined',
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

class UserListRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('login', 'phone', 'birthday', 'email')


class PostListRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'text', 'author', 'image')

class PostCreateUpdateDestroySerializer(serializers.ModelSerializer):
    def validate_author(self, author):
        today = date.today()
        age = today.year - author.birthday.year - ((today.month, today.day) < (author.birthday.month, author.birthday.day))
        if age < 18:
            raise ValidationError('For posting author age must be more or equals than 18 years')
        return author

    def validate_text(self, text):
        restricted_words = [
            "ерунда",
            "глупость",
            "чепуха",
        ]

        check_result = [word in text.lower() for word in restricted_words]
        if True in check_result:
            raise ValidationError("Text contains abandoned word inside")

        return text


    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'edited_at']

class CommentListRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'post')

class CommentCreateUpdateDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'edited_at']