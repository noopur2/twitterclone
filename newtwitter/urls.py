from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required as auth
from tweet.views import TweetsCreateView, TweetsDetailView ,TweetsUpdateView
from tweet.views import RetweetFormView#, FollowingListView

admin.autodiscover()

from tweet.views import TweetsListView, UserProfileDetailView, UserProfileEditView


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
                       #home page
    url(r'^$',TweetsListView.as_view(),name = 'home'),
                       #login page
    url(r"^login/$", "django.contrib.auth.views.login",
        {"template_name": "login.html"},name = "login"),
                       #dont need to define separate view 
    url(r"^logout/$","django.contrib.auth.views.logout_then_login",
        name = "logout"),
    
                       #urls provided by django registration
    url(r"^accounts/", include("registration.backends.simple.urls")),
                       #for profile view of user
    url(r'^users/(?P<slug>\w+)/$',UserProfileDetailView.as_view(),
        name="profile"),
                       #only authenticated user can edit profile
    url(r"^edit_profile/$",auth(UserProfileEditView.as_view()),
        name="edit_profile"),
    url(r'^tweets/create/$', auth(TweetsCreateView.as_view()),
        name='tweets_create'),
    url(r'^tweets/(?P<pk>\d+)/$', TweetsDetailView.as_view(),
        name='tweets_detail'),
    url(r'^tweets/update/(?P<pk>\d+)/$', auth(TweetsUpdateView.as_view()),
        name='tweets_update'),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^retweet/$', auth(RetweetFormView.as_view()), name="retweet"),
    #url(r'^following/$',FollowingListView.as_view(),name = 'following'),

)

