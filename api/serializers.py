from rest_framework import serializers
from accounts.models import CustomUser
from blog.models import Post, Category
from django.conf import settings
from blog.storage import VercelBlobStorage

class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'full_name', 'profile_picture')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        if 'profile_picture' in validated_data and settings.VERCEL:
            old_picture = instance.profile_picture
            image = validated_data['profile_picture']
            storage = VercelBlobStorage()
            
            if old_picture:
                storage.delete(old_picture)
            
            path = f'profile_pics/{instance.username}/{image.name}'
            url = storage._save(path, image)
            validated_data['profile_picture'] = url

        return super().update(instance, validated_data)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    image = serializers.ImageField(required=False)

    class Meta:
        model = Post
        fields = '__all__'

    def update(self, instance, validated_data):
        if 'image' in validated_data and settings.VERCEL:
            old_image = instance.image
            image = validated_data['image']
            storage = VercelBlobStorage()
            
            if old_image:
                storage.delete(old_image)
            
            path = f'blog_images/{instance.slug}/{image.name}'
            url = storage._save(path, image)
            validated_data['image'] = url

        return super().update(instance, validated_data)

    def create(self, validated_data):
        if 'image' in validated_data and settings.VERCEL:
            image = validated_data['image']
            storage = VercelBlobStorage()
            path = f'blog_images/temp/{image.name}'  # Will be updated with slug
            url = storage._save(path, image)
            validated_data['image'] = url

        return super().create(validated_data)