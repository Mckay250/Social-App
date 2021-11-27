from rest_framework import serializers
from .models import Like, User, UserPost

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'ip_address', 'password']
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'ip_address': {
                'write_only': True
            }
        }


    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPost
        fields = ['id', 'text']
        

class LikePostSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Like
        fileds = ['id', 'user', 'post']


class UserPostDetailedSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    likes_count = serializers.SerializerMethodField(read_only=True)

    def get_likes_count(self, post):
        return len([1 for like in post.likes.all() if not like.deleted])


    class Meta:
        model = UserPost
        fields = ['id', 'text', 'user', 'likes_count']

