# Create your views here.
#for rendering a tempate back to browser
from django.shortcuts import render_to_response

#for list view of tweets and detail view of user
from django.views.generic import ListView, DetailView

from .forms import UserProfileForm
from django.views.generic.edit import UpdateView
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

#models which will be used in view
from .models import Tweets,Retweet,UserProfile#, Following

from django.views.generic.edit import CreateView
from .forms import TweetsForm
from django.views.generic import DetailView
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import UpdateView

from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.views.generic.edit import FormView
from .forms import RetweetForm

#from .forms import FollowingForm


# Create your views here.

class TweetsListView(ListView):
    model = Tweets
    #stores all the tweets
    queryset = Tweets.with_retweets.all()

class UserProfileDetailView(DetailView):
    model = get_user_model()
    #key to lookup model. Slug field is primary key.
    slug_field = "username"
    template_name = "user_detail.html"
    #queryset = Tweets.with_retweets.all()

    #override
    #ensure userprofile is always created even we dont have signals for it.
    def get_object(self, queryset=None):
        user = super(UserProfileDetailView, self).get_object(queryset)
        UserProfile.objects.get_or_create(user=user)
        return user
    

#crud interface-- update view to edit userprofile 
class UserProfileEditView(UpdateView):
    model = UserProfile
    #will show fieldsdefined by custom form
    form_class = UserProfileForm
    template_name ="edit_profile.html"
    
    def get_object(self, queryset=None):
        return UserProfile.objects.get_or_create(user=self.request.user)[0]

    def get_success_url(self):
        return reverse("profile", kwargs={"slug":self.request.user})

class TweetsCreateView(CreateView):
    model = Tweets
    form_class = TweetsForm

    def form_valid(self, form):
        f = form.save(commit=False)
        f.rank_score = 0.0
        f.submitter = self.request.user
        f.save()

        return super(CreateView, self).form_valid(form)   
    
class TweetsDetailView(DetailView):
    model = Tweets

class TweetsUpdateView(UpdateView):
    model = Tweets
    form_class = TweetsForm


class RetweetFormView(FormView):
    form_class = RetweetForm

    def form_valid(self, form):
        tweets = get_object_or_404(Tweets, pk=form.data["tweetId"])
        user = self.request.user
        prev_retweets = Retweet.objects.filter(userId=user, tweetId=tweets)
        has_retweeted = (prev_retweets.count() > 0)

        if not has_retweeted:
            # add retweet
            Retweet.objects.create(userId=user, tweetId=tweets)
            print("retweeted")
        else:
            # delete vote
            prev_retweets[0].delete()
            print("deleted retweet")


        return redirect("home")

    def form_invalid(self, form):
        print("invalid")
        return redirect("home")
'''
class FollowingListView(ListView):
    model= Following
    queryset = Following.with_following.all()


class FollowingFormView(FormView):
    form_class = FollowingForm

    def form_valid(self,form):
        users = get_object_or_404(UserProfile, pk=form.data[""])
        
    '''
