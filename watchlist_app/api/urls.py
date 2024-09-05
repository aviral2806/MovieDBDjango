from django.urls import path
from .views import WatchListAll,WatchListDetails,StreamPlatformList,StreamPlatformDetail,ReviewList,ReviewDetail,ReviewCreate,UserList,WatchListAll2



urlpatterns = [
    path('list/',WatchListAll,name='movie-list'),
    path('list2/',WatchListAll2.as_view(),name='movie-list2'),
    path('<int:pk>/',WatchListDetails,name='movie-details'),
    path('stream/',StreamPlatformList.as_view(),name='stream-list'),
    path('stream/<int:pk>',StreamPlatformDetail.as_view(),name='stream-details'),
    path('stream/<int:pk>/review/',ReviewList.as_view(),name='review-list'),
    path('stream/<int:pk>/review-create/',ReviewCreate.as_view(),name='review-create'),
    path('stream/review/<int:pk>/',ReviewDetail.as_view(),name='review-details'),
    path('stream/review/user/',UserList.as_view(),name='review-user-details'),
]