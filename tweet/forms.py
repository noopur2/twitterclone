from django import forms
from .models import UserProfile
from .models import Tweets
from .models import Retweet


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ("user","followes","following")
        
class TweetsForm(forms.ModelForm):
    class Meta:
        model = Tweets
        exclude = ("submitter", "rank_score")

class RetweetForm(forms.ModelForm):
    class Meta:
        model = Retweet
        exclude = ("time")
'''
class FollowingForm(forms.ModelForm):
    class Meta:
        model = UserProfile
   '''     
