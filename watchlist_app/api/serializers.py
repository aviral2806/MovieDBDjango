from rest_framework import serializers
from ..models import WatchList,StreamPlatform,Review

# def title_len_check(value):
#     if len(value)<3:
#         raise serializers.ValidationError("Name short")

class ReviewSerializer(serializers.ModelSerializer):
    watchlist_title = serializers.CharField(source='watchlist.title',read_only=True)
    review_user = serializers.CharField(read_only=True)
    class Meta:
        model=Review
        # fields='__all__'
        exclude=('watchlist',)
class watchListSerializer(serializers.ModelSerializer):
    
    reviews = ReviewSerializer(many=True,read_only=True)
    
    class Meta:
        model=WatchList
        fields='__all__'
    # id = serializers.IntegerField(read_only=True)
    # title = serializers.CharField(validators=[title_len_check])
    # genre = serializers.CharField()
    # active = serializers.BooleanField()
    
    # def create(self,validated_data):
    #     movie=Movie.objects.create(**validated_data)
    #     return movie
     
    def update(self,instance,validated_data):
        instance.title=validated_data.get('title',instance.title)
        instance.storyline=validated_data.get('storyline',instance.storyline)
        # instance.genre=validated_data.get('genre',instance.genre)
        instance.active=validated_data.get('active',instance.active)
        instance.save()
        return instance
    
   

class streamPlatformSerializer(serializers.ModelSerializer):
    
    watchlist = watchListSerializer(many=True,read_only=True)
    
    class Meta:
        model = StreamPlatform
        fields = '__all__'
        
    