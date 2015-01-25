from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count
from django.core.urlresolvers import reverse

class TweetsRetweetCountManager(models.Manager):
    def get_query_set(self):
        return super(TweetsRetweetCountManager,self).get_query_set().annotate(
            retweets= Count('retweet')).order_by("submitted_on")


# tweets model.
class Tweets(models.Model):
    tweet = models.TextField(blank =True,max_length=140)
    submitter = models.ForeignKey(User)
    submitted_on = models.DateTimeField(auto_now_add=True)
    retweet_status = models.BooleanField(default = False)
    with_retweets = TweetsRetweetCountManager()
    objects = models.Manager() #default manager
  
    def __unicode__(self):              # __unicode__ on Python 2
        return self.tweet

    def get_absolute_url(self):
        return reverse("tweets_detail", kwargs={"pk": str(self.id)})

#reply table    
class Reply(models.Model):
    tweet = models.ForeignKey(Tweets)
    user = models.ForeignKey(User)
    content = models.TextField(blank= True,max_length = 250)
    time = models.DateTimeField(auto_now_add = True)
    def __unicode__(self):              # __unicode__ on Python 2
        return self.content

#hashtag        
class Hashtag(models.Model):
    tweet = models.ForeignKey(Tweets)
    hashtag = models.CharField(max_length=100)
    reply = models.ForeignKey(Reply)
    def __unicode__(self):              # __unicode__ on Python 2
        return self.hashtag
    
#retweets
class Retweet(models.Model):
    tweetId = models.ForeignKey(Tweets)
    userId = models.ForeignKey(User)
    time = models.DateTimeField(auto_now_add = True)
    def __unicode__(self):              # __unicode__ on Python 2
        return "retweet"

#user's profile
class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    bio = models.TextField(null=True)
    #profile_image = models.ImageField(upload_to='user-images/', null=True, blank=True)

    def __unicode__(self):
        return "%s's profile" % self.user
    
    
'''
class FollowingCountManager(models.Manager):
    def get_query_set(self):
        return super(FollowingCountManager,self).get_query_set().annotate(
            followings= Count('following'))

class FollowerCountManager(models.Manager):
    def get_query_set(self):
        return super(FollowerCountManager,self).get_query_set().annotate(
            follow= Count('userId')).group_by("self.user")
'''
class Following(models.Model):
    follower = models.ForeignKey(UserProfile)
    follow = models.ForeignKey(User)
   # with_following = FollowingCountManager()
   # objects = models.Manager() #default manager

    def __unicode__(self):
        return "following"
   # def get_absolute_url(self):
    #    return reverse("following_detail", kwargs={"pk": str(self.id)})

#to ensure user profile is created-- signal handler
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)

#catching signals from signal handler
from django.db.models.signals import post_save
post_save.connect(create_profile,sender =User)
