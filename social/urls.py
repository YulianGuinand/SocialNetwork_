from django.urls import path
from .views import PostListView, PostDetailView, PostEditView, PostDeleteView, CommentDeleteView, ProfileView, ProfileEditView, AddFollower, RemoveFollower
from .views import AddLike, AddDisLike, UserSearch, AddFollowerPost, RemoveFollowerPost, ListFollowers, AddFollowerList, RemoveFollowerList
from .views import AddCommentLike, AddCommentDisLike, CommentReplyView, PostNotification, FollowNotification, RemoveNotification
from .views import DeleteHelpPost, RejectRequest, AcceptRequest, CreateRdv,CreateHelpPost, HelpPostView, CreatePostView, Explore,CreateThread, ListThreads, ThreadView, CreateMessage, ThreadNotification, DeleteMessage, AcceptFriendRequest, RejectFriendRequest, CreateFriendRequest, StoryAddLike
urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/edit/<int:pk>/', PostEditView.as_view(), name='post-edit'),
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:post_pk>/comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment-delete'),
    path('post/<int:post_pk>/comment/<int:pk>/like/', AddCommentLike.as_view(), name='comment-like'),
    path('post/<int:post_pk>/comment/<int:pk>/dislike/', AddCommentDisLike.as_view(), name='comment-dislike'),
    path('post/<int:post_pk>/comment/<int:pk>/reply/', CommentReplyView.as_view(), name="comment-reply"),
    path('explore', Explore.as_view(), name='explore'),
    path('post/<int:pk>/like/', AddLike.as_view(), name="like"),
    path('post/<int:pk>/dislike/', AddDisLike.as_view(), name="dislike"),
    
    path('post/create/', CreatePostView.as_view(), name='create-post'),
    
    path('story/<int:pk>/like/', StoryAddLike.as_view(), name="story-like"),
    
    path('post/accept_friend_request/<int:request_pk>/', AcceptFriendRequest.as_view(), name='accept-friend-request'),
    path('post/reject_friend_request/<int:request_pk>/', RejectFriendRequest.as_view(), name='reject-friend-request'),
    
    path('studypost/accept_request/<int:request_pk>/', AcceptRequest.as_view(), name="accept-request"),
    path('studypost/reject_request/<int:request_pk>/', RejectRequest.as_view(), name="reject-request"),
    
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('profile/edit/<int:pk>/', ProfileEditView.as_view(), name='profile-edit'),
    
    path('profile/send_friend_request/<int:to_user_pk>/', CreateFriendRequest.as_view(), name='send-friend-request'),
    
    path('profile/<int:pk>/followers/', ListFollowers.as_view(), name='list-followers'),
    path('profile/<int:pk>/followers/add/', AddFollower.as_view(), name='add-follower'),
    path('profile/<int:pk>/followers/remove/', RemoveFollower.as_view(), name='remove-follower'),
    path('profile/<int:pk>/followers/add-post/', AddFollowerPost.as_view(), name='add-follower-post'),
    path('profile/<int:pk>/followers/remove-post/', RemoveFollowerPost.as_view(), name='remove-follower-post'),
    path('profile/<int:pk>/followers/add-list/<int:pk_page>/', AddFollowerList.as_view(), name='add-follower-list'),
    path('profile/<int:pk>/followers/remove-list/<int:pk_page>/', RemoveFollowerList.as_view(), name='remove-follower-list'),
    path('search/', UserSearch.as_view(), name='profile-search'),

    path('notification/<int:notification_pk>/post/<int:post_pk>', PostNotification.as_view(), name='post-notification'),
    path('notification/<int:notification_pk>/profile/<int:profile_pk>', FollowNotification.as_view(), name='follow-notification'),
    path('notification/delete/<int:notification_pk>', RemoveNotification.as_view(), name='notification-delete'),
    path('notification/<int:notification_pk>/thread/<int:object_pk>', ThreadNotification.as_view(), name='thread-notification'),


    path('inbox/', ListThreads.as_view(), name='inbox'),
    path('inbox/create-thread/', CreateThread.as_view(), name='create-thread'),
    path('inbox/<int:pk>/', ThreadView.as_view(), name='thread'),
    path('inbox/<int:pk>/create-message/', CreateMessage.as_view(), name='create-message'),
    path('inbox/<int:pk>/delete-message/<int:message_pk>', DeleteMessage.as_view(), name='delete-message'),

    path('studypost', HelpPostView.as_view(), name="study-posts"),
    path('stdypost/post/<int:post_pk>/delete/', DeleteHelpPost.as_view(), name="post-help-delete"),
    path('studypost/createpost/', CreateHelpPost.as_view(), name="create-post-help"),
    path('studypost/post/<int:post_pk>/', CreateRdv.as_view(), name="posthelp-rdv"),
    
]
