from django.contrib import admin
from .models import Meeting,Request,Post, UserProfile, Comment, Notification, ThreadModel, Story, FriendRequest

admin.site.register(Post)
admin.site.register(UserProfile)
admin.site.register(Comment)
admin.site.register(Notification)
admin.site.register(ThreadModel)
admin.site.register(Story)
admin.site.register(FriendRequest)
admin.site.register(Request)
admin.site.register(Meeting)
