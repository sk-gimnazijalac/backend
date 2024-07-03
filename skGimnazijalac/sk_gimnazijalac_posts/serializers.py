import base64

from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Post, Image


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
    image = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_image(self, obj):
        if obj.image:
            return '/post/image/' + str(obj.image.id)
        return None


class CreatePostSerializer(serializers.ModelSerializer):
    description = serializers.CharField(max_length=2000, required=True)
    shortDescription = serializers.CharField(max_length=400)
    title = serializers.CharField(max_length=100, required=True)
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    date = serializers.DateField(required=True)
    image = serializers.ImageField(required=True)

    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data):
        image = validated_data.pop('image')
        image_bytes = image.read()
        image_instance = Image.objects.create(content=image_bytes)
        validated_data['image'] = image_instance
        return Post.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.description = validated_data.get('description', instance.description)
        instance.shortDescription = validated_data.get('shortDescription', instance.shortDescription)
        instance.title = validated_data.get('title', instance.title)
        if 'image' in validated_data:
            image = validated_data.pop('image')
            image_bytes = image.read()
            image_instance = Image.objects.create(content=image_bytes)
            instance.image = image_instance.id
        instance.save()
        return instance


class Base64ImageField(serializers.Field):
    def to_representation(self, obj):
        return base64.b64encode(obj).decode('utf-8')

    def to_internal_value(self, data):
        pass


class ImageSerializer(serializers.ModelSerializer):
    content = Base64ImageField()

    class Meta:
        model = Image
        fields = ('content',)
