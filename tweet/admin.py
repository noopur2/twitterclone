from django.contrib import admin

# Register your models here.
from .models import Tweets,Retweet,Hashtag,UserProfile,Following
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

class TweetsAdmin(admin.ModelAdmin):
    pass
admin.site.register(Tweets,TweetsAdmin)


class RetweetAdmin(admin.ModelAdmin):
    pass
admin.site.register(Retweet,RetweetAdmin)

class HashtagAdmin(admin.ModelAdmin):
    pass
admin.site.register(Hashtag,HashtagAdmin)

class FollowingAdmin(admin.ModelAdmin):
    pass
admin.site.register(Following,FollowingAdmin)
#extend user admin which is existing

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

#create extended usermodel
class UserProfileAdmin(UserAdmin):
    inlines = (UserProfileInline, )

#unregister existing user admin
admin.site.unregister(get_user_model())

#register new user admin
admin.site.register(get_user_model(), UserProfileAdmin)
