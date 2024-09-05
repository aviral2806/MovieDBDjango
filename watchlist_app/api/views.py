from django.shortcuts import render,get_object_or_404
from ..models import WatchList,StreamPlatform,Review
from .serializers import watchListSerializer,streamPlatformSerializer,ReviewSerializer
from watchlist_app.api.permissions import ReviewUserOrReadOnly,AdminOrReadOnly
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle,ScopedRateThrottle
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status,permissions
from rest_framework import generics
from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import WatchListPagination
# Create your views here.

class ReviewCreate(generics.CreateAPIView):
    serializer_class=ReviewSerializer
    permission_classes=[permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self,serializer):
        pk=self.kwargs['pk']
        movie=WatchList.objects.get(pk=pk)
        user=self.request.user
        rev_query=Review.objects.filter(watchlist=movie,review_user=user)
        if rev_query.exists():
            raise ValidationError("Cannot make more than one reviews for a movie")
        if movie.number_rating==0:
            movie.avg_rating=serializer.validated_data['rating']
        else:
            movie.avg_rating=((movie.avg_rating*movie.number_rating)+serializer.validated_data['rating'])/(movie.number_rating+1)
        movie.number_rating+=1
        movie.save()
        serializer.save(watchlist=movie,review_user=user)

class ReviewList(generics.ListAPIView):
    queryset=Review.objects.all()
    serializer_class=ReviewSerializer
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-list'
    def get_queryset(self):
        pk=self.kwargs['pk']
        q = Review.objects.filter(watchlist=pk)
        return q
  
class UserList(generics.ListAPIView):
    queryset=Review.objects.all()
    serializer_class=ReviewSerializer
    def get_queryset(self):
        username = self.request.query_params.get('username',None)
        queryset=Review.objects.all()
        if username is not None:
            queryset=queryset.filter(review_user__username=username)
        return queryset
    
# class UserList(generics.ListAPIView):
#     queryset=Review.objects.all()
#     serializer_class=ReviewSerializer
#     def get_queryset(self):
#         username=self.kwargs['username']
#         userReviews=Review.objects.filter(review_user__username=username)
#         return userReviews
   
class WatchListAll2(generics.ListAPIView):
    queryset=WatchList.objects.all()
    pagination_class = WatchListPagination
    serializer_class=watchListSerializer
    filter_backends=[filters.OrderingFilter]
    # search_fields=['title']
    ordering_fields=['title']
    
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Review.objects.all()
    serializer_class=ReviewSerializer
    permission_classes=[ReviewUserOrReadOnly]



# class ReviewDetail(generics.GenericAPIView,mixins.RetrieveModelMixin):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#     def get(self,request,*args,**kwargs):
#         return self.retrieve(request,*args,**kwargs)

# class ReviewList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#     def get(self,request,*args,**kwargs):
#         return self.list(request,*args,**kwargs)
#     def post(self,request,*args,**kwargs):
#         return self.create(request,*args,**kwargs)

# class StreamPlatform(viewsets.ViewSet):
    
#     def list(self,request):
#         queryset=StreamPlatform.objects.all()
#         serializer = streamPlatformSerializer(queryset,many=True)
#         return Response(serializer.data)
    
#     def retrieve(self,request,pk=None):
#         queryset=StreamPlatform.objects.all()
#         stream= get_object_or_404(queryset,pk=pk)
#         return Response(streamPlatformSerializer(stream).data)
          
        

class StreamPlatformList(APIView):
    permission_classes=[AdminOrReadOnly]
    def get(self,request):
        streamplats = StreamPlatform.objects.all()
        streamplatforms = streamPlatformSerializer(streamplats,many=True)
        return Response(streamplatforms.data)
    
    def post(self,request):
        streamplatform = streamPlatformSerializer(data=request.data)
        if streamplatform.is_valid():
            streamplatform.save()
            return Response(streamplatform.data)
        else:
            return Response(streamplatform.errors)
        
class StreamPlatformDetail(APIView):
    permission_classes=[AdminOrReadOnly]
    def get(self,request,pk):
        try:
            stream = StreamPlatform.objects.get(pk=pk)
        except:
            return Response({'error':'Stream Platform does not exist'},status=status.HTTP_404_NOT_FOUND)
        st = streamPlatformSerializer(stream)
        return Response(st.data)
    
    def put(self,request,pk):
        stream = StreamPlatform.objects.get(pk=pk)
        st = streamPlatformSerializer(stream,data=request.data)
        if st.is_valid():
            st.save()
            return Response(st.data)
        else:
            return Response(st.errors)
    def delete(self,request,pk):
        stream = StreamPlatform.objects.get(pk=pk)
        stream.delete()
        return Response(status=status.HTTP_200_OK)

@api_view(['GET','POST'])
# @permission_classes([AdminOrReadOnly])
def WatchListAll(request):
    if request.method == 'GET':
        watchlist=WatchList.objects.all()
        moviesSerialized = watchListSerializer(watchlist,many=True)
        return Response(moviesSerialized.data,status=status.HTTP_200_OK)
    if request.method == 'POST':
        movieSerialized = watchListSerializer(data=request.data)
        if movieSerialized.is_valid():
            movieSerialized.save()
            return Response(movieSerialized.data,status=status.HTTP_201_CREATED)
        else:
            return Response(movieSerialized.errors)

@api_view(['GET','PUT','DELETE'])
@permission_classes([AdminOrReadOnly])
def WatchListDetails(request,pk):
    if request.method=='GET':
        try:
            movie=WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'error':'Watchlist does not exist'},status=status.HTTP_404_NOT_FOUND)
        movieSerialized = watchListSerializer(movie)
        return Response(movieSerialized.data,status=status.HTTP_200_OK)
    if request.method=='PUT':
        movie=WatchList.objects.get(pk=pk)
        movieSerialized=watchListSerializer(movie,data=request.data)
        if movieSerialized.is_valid():
            movieSerialized.save()
            return Response(movieSerialized.data)
        else:
            return Response(movieSerialized.errors)
    if request.method=='DELETE':
        movie=WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_200_OK)    
    