from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Post


class AuthorSerializer(serializers.ModelSerializer):
    firstName = serializers.CharField(source='first_name')
    lastName = serializers.CharField(source='last_name')

    class Meta:
        model = User
        fields = ['firstName', 'lastName']


class GetPostSerializer(serializers.ModelSerializer):
    description = serializers.CharField(max_length=2000, required=True)
    shortDescription = serializers.CharField(max_length=400)
    title = serializers.CharField(max_length=100, required=True)
    author = AuthorSerializer()
    date = serializers.DateField(required=True)
    src = serializers.CharField(max_length=100)

    class Meta:
        model = Post
        fields = '__all__'


class CreatePostSerializer(serializers.ModelSerializer):
    description = serializers.CharField(max_length=2000, required=True)
    shortDescription = serializers.CharField(max_length=400)
    title = serializers.CharField(max_length=100, required=True)
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    date = serializers.DateField(required=True)
    src = serializers.CharField(max_length=100)

    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data):
        return Post.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.description = validated_data.get('description', instance.description)
        instance.shortDescription = validated_data.get('shortDescription', instance.shortDescription)
        instance.title = validated_data.get('title', instance.title)
        instance.src = validated_data.get('src', instance.src)

        instance.save()
        return instance
