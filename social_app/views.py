from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from social_app.exceptions import APIKeyNotFound
from .serializers import UserPostDetailedSerializer, UserPostSerializer, UserSerializer, GeoLocationSerializer, UserHolidayDataSerializer
from .models import UserPost, Like
from . import utils 
from ipware import get_client_ip
from datetime import date


class SignUpView(APIView):

    def post(self, request):
        client_ip, _ = get_client_ip(request)
        if client_ip is not None:
            request.data['ip_address'] = client_ip
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            if not utils.is_email_valid_format(request.data['email']):
                return get_response(message='Invalid email format', status=status.HTTP_400_BAD_REQUEST)
        except APIKeyNotFound:
            # alert team of this error
            return get_response(message="An error occured from our end, we will fix this as soon as possible", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer.save()
        user = serializer.validated_data
        print('saved user is ', user)
        populate_user_geo_location_data(user)
        return get_response(message='successful', status=status.HTTP_201_CREATED)


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)    
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreatePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = UserPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return get_response('Success', status=status.HTTP_201_CREATED)


class GetPostView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        post = UserPost.objects.filter(id=id, deleted=False).first()
        if post is None:
            return get_response('Post not found', status=status.HTTP_404_NOT_FOUND)
        serializer = UserPostDetailedSerializer(post)
        return Response(serializer.data)
    

class ListPostView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = UserPost.objects.filter(deleted=False)
        data = UserPostDetailedSerializer(queryset, many=True)
        return Response(data.data, status=status.HTTP_200_OK)


class UpdatePostView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        post_id = get_value_from_key_in_request(request, 'postId')
        if post_id is None:
            return get_response('postId is required', status=status.HTTP_400_BAD_REQUEST)
        post = UserPost.objects.filter(id=post_id, deleted=False).first()
        if post is None:
            return get_response('Post not found', status=status.HTTP_404_NOT_FOUND)
        if post.user != user:
            return get_response("Cannot update another user's post", status=status.HTTP_403_FORBIDDEN)
        serializer = UserPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post.text = serializer.data['text']
        post.save(update_fields=['text'])
        return get_response('Success', status=status.HTTP_200_OK)


class DeletePostView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        post_id = get_value_from_key_in_request(request, 'postId')
        if post_id is None:
            return get_response('postId is required', status=status.HTTP_400_BAD_REQUEST)
        post = UserPost.objects.filter(id=post_id, deleted=False).first()
        if post is None:
            return get_response('Post not found', status=status.HTTP_404_NOT_FOUND)
        if post.user != user:
            return get_response("Cannot update another user's post", status=status.HTTP_403_FORBIDDEN)
        post.deleted = True
        post.save(update_fields=['deleted'])
        return get_response('Success', status=status.HTTP_200_OK)


class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        post_id = get_value_from_key_in_request(request, 'postId')
        if post_id is None:
            return get_response('postId is required', status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        post = UserPost.objects.filter(id=post_id, deleted=False).first()
        if post is None:
            return get_response('Post not found', status=status.HTTP_404_NOT_FOUND)
        like = Like.objects.filter(user=user, post=post_id).first()
        if like is None:
            like = Like()
            like.post = post
            like.user = user
        like.deleted = False
        like.save()
        return get_response('Success', status=status.HTTP_201_CREATED)


class UnlikePostView(APIView):
    permission_class = [IsAuthenticated]

    def post(self, request):
        post_id = get_value_from_key_in_request(request, 'postId')
        if post_id is None:
            return get_response('postId is required', status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        like = Like.objects.filter(user=user, post=post_id, deleted=False).first()
        if like is not None:
            like.deleted = True
            like.save()
        return Response('Success', status=status.HTTP_200_OK)


def get_value_from_key_in_request(request, key : str):
        try:
            value = request.data[key]
        except KeyError:
            return None
        return value

def get_response(message: str, status=status.HTTP_200_OK):
    return Response({'message': f'{message}'}, status=status)


def populate_user_geo_location_data(user):
    geolocation_data = utils.get_geolocation_data_from_ip_address(user['ip_address'])
    print('geolocation data here >>>>>> ', geolocation_data)
    serializer = GeoLocationSerializer(data=geolocation_data)
    serializer.is_valid(raise_exception=True)
    serializer.save(user=user)
    user_geolocation = serializer.validated_data
    populate_user_Holiday_data(user_geolocation, user)


def populate_user_Holiday_data(geolocation_data, user):
    todays_date = date.today()
    holiday_data = utils.get_holiday_data_from_geolocation(geolocation_data['country_code'], todays_date.year, todays_date.month, todays_date.day)
    if holiday_data is None:
        return
    serializer = UserHolidayDataSerializer(data=holiday_data)
    serializer.is_valid(raise_exception=True)
    serializer.save(user)
    return
