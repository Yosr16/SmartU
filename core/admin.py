from django.contrib import admin
from .models import SmallBusiness,BusinessPost,Profile, Post, LikePost, FollowersCount,Stage, Evenement, EventSocial, EventClub, Logement, Transport
from .models import ContactMessage
# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(FollowersCount)
admin.site.register(Stage)
admin.site.register(Evenement)
admin.site.register(EventSocial)
admin.site.register(EventClub)
admin.site.register(Logement)
admin.site.register(Transport)
admin.site.register(SmallBusiness)
admin.site.register(BusinessPost)
admin.site.register(ContactMessage)