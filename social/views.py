from django.shortcuts import render, redirect
from django.db.models import Q
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone

from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views import View
from .models import Meeting, Request,Tag ,Post, Comment, UserProfile, Notification, ThreadModel, MessageModel, FriendRequest, Story, HelpPost
from .forms import CreateRdvForm ,ExploreForm, ShareForm,PostForm, CommentForm, ThreadForm, MessageForm, StoryForm, HelpPostForm
from django.views.generic.edit import UpdateView, DeleteView
from django.utils.html import linebreaks
import datetime
import pytz

class CreatePostView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = PostForm()
        context = {
            'form': form,
        }

        return render(request, 'social/post.html', context)
    
    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            
            new_post.create_tags()
        return redirect('post-list')

class HelpPostView(View):
    def get(self, request, *arg, **kwargs):
        posts = HelpPost.objects.all().order_by('-created_on')
        
        meeting = []
        for meet in Meeting.objects.filter(teacher=request.user):
            meeting.append(meet)
        for meet in Meeting.objects.filter(student=request.user):
            meeting.append(meet)
        
        for meet in meeting:
            if meet.date.astimezone(pytz.timezone('Europe/Paris')) < datetime.datetime.now().astimezone(pytz.timezone('Europe/Paris')):
                meeting.remove(meet)

        rdvrequest_infos = Request.objects.filter(to_user=request.user, is_read=False)
        requests_infos = []
        
        for rdvrequest in rdvrequest_infos:
            requests_infos.append([rdvrequest, 0])
        for meet in meeting:
            requests_infos.append([meet, 1])

    
        context = {
            'posts': posts,
            'rdvrequest_infos': requests_infos,
        }
        
        return render(request, 'social/study_help.html', context)

class CreateHelpPost(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        form = HelpPostForm()
        context = {
            'form': form,
        }
        return render(request,'social/create_posthelp.html', context)
    
    def post(self, request, *args, **kwargs):
        form = HelpPostForm(request.POST)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            
            new_post.create_tags()
        return redirect('study-posts')

class CreateRdv(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = CreateRdvForm()
        context = {
            'form': form,
        }
        return render(request,'social/create_rdv.html', context)
    def post(self, request, post_pk,*args, **kwargs):
        form = CreateRdvForm(request.POST)
        post = HelpPost.objects.get(pk=post_pk)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.teacher = post.author
            new_post.student = request.user
            
            # Récupération de la date et de l'heure depuis les données du formulaire
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']
            
            # Combiner date et heure pour créer un objet datetime
            datetime_combined = datetime.datetime.combine(date, time)
            
            time = datetime_combined
            
            new_post.save()
        
            to_user = User.objects.get(pk=post.author.pk)
            if Request.objects.filter(from_user=request.user, to_user=to_user).exists():
                pass
            else:
                Request.objects.create(from_user=request.user, to_user=to_user, topic=post.title, date=time)
        
        return redirect('study-posts')

class AcceptRequest(View):
    def post(self, request, request_pk, *args, **kwargs):
        friend_request = Request.objects.get(pk=request_pk)
        friend_request.is_accepted = True
        friend_request.is_read = True
        
        Meeting.objects.create(teacher=friend_request.to_user, student=friend_request.from_user, topic=friend_request.topic, date=friend_request.date)
        
        friend_request.save()

        return redirect('study-posts')
    
class RejectRequest(View):
    def post(self, request, request_pk, *args, **kwargs):
        friend_request = Request.objects.get(pk=request_pk)
        friend_request.delete()

        return redirect('study-posts')
   
class DeleteHelpPost(View):
    def get(self, request, post_pk, *args, **kwargs):
        post = HelpPost.objects.get(pk=post_pk)
        post.delete()
        
        return redirect('study-posts')

class PostListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-created_on')
        friendrequests = FriendRequest.objects.filter(to_user=request.user, is_accepted=False)
        friendrequest_infos = []
        nb_mutual_friend = 0
        for friendrequest in friendrequests:
            for follower in request.user.profile.followers.all():
                if follower in friendrequest.from_user.profile.followers.all():
                    nb_mutual_friend += 1
            friendrequest_infos.append([friendrequest, nb_mutual_friend])
            nb_mutual_friend = 0
        
        notifications = Notification.objects.filter(to_user=request.user).exclude(user_has_seen=True).order_by('-date')
        
        storys = Story.objects.all().order_by('-created_on')
        for story in storys:
            
            date_actuelle = timezone.now()
            difference = date_actuelle - story.created_on
            if difference.total_seconds() >= 24 * 3600:
                story.delete()
            else:
                if story.author == request.user:
                    story.is_follow = True
                else:
                    story.is_follow = story.is_followed_by(request.user)
                story.save()
            
        form = PostForm()
        story_form = StoryForm()
        thread_form = ThreadForm()
        
        followers = request.user.followers.all()
        
        is_liked = False
        
        post_data = []
        for post in posts:
            post.created_on = post.created_on.strftime("%d/%m/%Y")
            
            post.body = linebreaks(post.body)
            if post.image:
                if request.user in post.likes.all():
                    is_liked = True
                post_data.append([post.is_followed_by(request.user), post, post.image.url, is_liked])
            else:
                if request.user in post.likes.all():
                    is_liked = True
                post_data.append([post.is_followed_by(request.user), post, False, is_liked])

        threads = ThreadModel.objects.filter(Q(user=request.user) | Q(receiver=request.user) )
        threads_infos = []
        if len(threads) != 0:
            for thread in threads:
                threads_infos.append([thread, MessageModel.objects.filter(thread__pk__contains=thread.pk, is_deleted=False).last()])
        else:
            threads_infos = []
    
    
        context = {
            'post_list': posts,
            'threads_infos': threads_infos,
            'form': form,
            'thread_form': thread_form,
            'post_data': post_data,
            'friendrequest_infos': friendrequest_infos,
            'storys': storys,
            'notifications': notifications,
            'followers': followers,
            'story_form': story_form,
        }

        return render(request, 'social/post_list.html', context)

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            
            new_post.create_tags()

        story_form = StoryForm(request.POST, request.FILES)
        if story_form.is_valid():
            new_story = story_form.save(commit=False)
            new_story.author = request.user
            new_story.save()
        
        thread_form = ThreadForm(request.POST)
        
        username = request.POST.get('username')
        
        try:
            receiver = User.objects.get(username=username)
            if ThreadModel.objects.filter(user=request.user, receiver=receiver).exists():
                if request.user in receiver.profile.followers.all():
                    thread = ThreadModel.objects.filter(user=request.user, receiver=receiver)
                else:
                    return redirect('post-list')
                
                return redirect('thread', pk=thread.pk)
                
            elif ThreadModel.objects.filter(user=receiver, receiver=request.user).exists():
                if request.user in receiver.profile.followers.all():
                    thread = ThreadModel.objects.filter(user=receiver, receiver=request.user)
                else:
                    return redirect('post-list')
                
                
                return redirect('thread', pk=thread.pk)
            
            if thread_form.is_valid():
                if request.user in receiver.profile.followers.all():
                    thread = ThreadModel(
                        user=request.user,
                        receiver=receiver
                    )
                    thread.save()
                    return redirect('thread', pk=thread.pk)
                else:
                    return redirect('post-list')
        except:
            return redirect('post-list')
        return redirect('post-list')

class PostDetailView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        post.created_on = post.created_on.strftime("%d/%m/%Y")
        
        form = CommentForm()
        comments = Comment.objects.filter(post=post).order_by('-created_on')
        post.body = linebreaks(post.body)
        
        
        
        is_liked = False
        if request.user in post.likes.all():
            is_liked = True
        
        comment_infos = []
        
        for comment in Comment.objects.filter(post=post).all():
            comment.created_on = comment.created_on.strftime("%d/%m/%Y")
            
            comment.comment = linebreaks(comment.comment)
            if request.user in comment.likes.all():
                comment_infos.append([True, comment])
            else:
                comment_infos.append([False, comment])
        
        context = {
            'post': post,
            'form': form,
            'comments': comments,
            'comment_infos': comment_infos,
            'liked': is_liked,
        }

        return render(request, 'social/post_detail.html', context)

    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()
            new_comment.create_tags()
        
        notification = Notification.objects.create(notification_type=2, from_user=request.user, to_user=post.author, comment=new_comment)
        
        return redirect('post-detail', pk=pk)

class CommentReplyView(LoginRequiredMixin, View):
    def post(self, request, post_pk, pk, *args, **kwargs):
        post = Post.objects.get(pk=post_pk)
        parent_comment = Comment.objects.get(pk=pk)
        form = CommentForm(request.POST)
        
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.parent = parent_comment
            new_comment.save()
        
        notification = Notification.objects.create(notification_type=2, from_user=request.user, to_user=parent_comment.author, comment=new_comment)
            
        return redirect('post-detail', pk=post_pk)
        
class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['body', 'image']
    template_name = 'social/post_edit.html'
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('post-detail', kwargs={'pk': pk})
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'social/post_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'social/comment_delete.html'

    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('post-detail', kwargs={'pk': pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

class ProfileView(View):
    
    def get(self, request, pk,*args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        user = profile.user
        posts = Post.objects.filter(author=user).order_by('-created_on')
        followers = profile.followers.all()
        
        profile.bio = linebreaks(profile.bio)
        
        number_of_followers = len(followers)
        
        if number_of_followers == 0:
            is_following = False
            
        for follower in followers:
            if follower == request.user:
                is_following = True
                break
            else:
                is_following = False
        
        cofollowers = []
        for follower in followers:
            if follower in request.user.profile.followers.all():
                if len(cofollowers) <= 3:
                    cofollowers.append(follower)
        
        
        number_of_posts = len(posts)
            
        context = {
            'user': user,
            'profile': profile,
            'number_of_posts': number_of_posts,
            'posts': posts,
            'number_of_followers': number_of_followers,
            'is_following': is_following,
            'cofollowers': cofollowers,
        }
        
        return render(request, 'social/profile.html', context)
    
class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserProfile
    fields = ['name', 'bio', 'birth_date', 'location', 'picture']
    template_name = 'social/profile_edit.html'
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('profile', kwargs={'pk': pk})
    
    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user

class AddFollower(LoginRequiredMixin, View):
    def post(self, request, pk,*args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.followers.add(request.user)

        notification = Notification.objects.create(notification_type=3, from_user=request.user, to_user=profile.user)
        
        return redirect('profile', pk=profile.pk)
    
class RemoveFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.followers.remove(request.user)
        
        request.user.profile.followers.remove(profile.user)
        
        if FriendRequest.objects.filter(from_user=request.user, to_user=profile.user).exists():
            friend_requests = FriendRequest.objects.filter(from_user=request.user, to_user=profile.user).all()
            for friend_request in friend_requests:
                friend_request.delete()
        
        return redirect('profile', pk=profile.pk)
    
class AddFollowerPost(LoginRequiredMixin, View):
    def post(self, request, pk,*args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.followers.add(request.user)
    
        return redirect('post-list')
    
class RemoveFollowerPost(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.followers.remove(request.user)
        
        request.user.profile.followers.remove(profile.user)
        
        if FriendRequest.objects.filter(from_user=request.user, to_user=profile.user).exists():
            friend_requests = FriendRequest.objects.filter(from_user=request.user, to_user=profile.user).all()
            for friend_request in friend_requests:
                friend_request.delete()
        
        return redirect('post-list')

class AddFollowerList(LoginRequiredMixin, View):
    def post(self, request, pk, pk_page,*args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.followers.add(request.user)
    
        return redirect('list-followers', pk=pk_page)
    
class RemoveFollowerList(LoginRequiredMixin, View):
    def post(self, request, pk, pk_page,*args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.followers.remove(request.user)
        
        request.user.profile.followers.remove(profile.user)
        
        if FriendRequest.objects.filter(from_user=request.user, to_user=profile.user).exists():
            friend_requests = FriendRequest.objects.filter(from_user=request.user, to_user=profile.user).all()
            for friend_request in friend_requests:
                friend_request.delete()
        
        return redirect('list-followers', pk=pk_page)

class AddLike(LoginRequiredMixin, View):
    def post(self, request, pk,*args, **kwargs):
        
        post = Post.objects.get(pk=pk)
        
        is_dislike = False
        
        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break
        
        if is_dislike:
            post.dislikes.remove(request.user)
        
        is_likes = False
        
        for like in post.likes.all():
            if like == request.user:
                is_likes = True
                break
            
        if not is_likes:
            post.likes.add(request.user)
            notification = Notification.objects.create(notification_type=1, from_user=request.user, to_user=post.author, post=post)
        if is_likes:
            post.likes.remove(request.user)    
        
        next = request.POST.get('next', '/')
        
        return HttpResponseRedirect(next)

class StoryAddLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Story.objects.get(pk=pk)
        
        is_dislike = False
        
        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break
        
        if is_dislike:
            post.dislikes.remove(request.user)
        
        is_likes = False
        
        for like in post.likes.all():
            if like == request.user:
                is_likes = True
                break
            
        if not is_likes:
            post.likes.add(request.user)
            notification = Notification.objects.create(notification_type=1, from_user=request.user, to_user=post.author, story=post)
        if is_likes:
            post.likes.remove(request.user)    
        
        next = request.POST.get('next', '/')
        
        return HttpResponseRedirect(next)

class AddDisLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        
        is_likes = False
        
        for like in post.likes.all():
            if like == request.user:
                is_likes = True
                break
        
        if is_likes:
            post.likes.remove(request.user)
        
        is_dislike = False
        
        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break
        
        if not is_dislike:
            post.dislikes.add(request.user)
        if is_dislike:
            post.dislikes.remove(request.user)
        
        next = request.POST.get('next', '/')
        
        return HttpResponseRedirect(next)
        
class UserSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('query')
        profile_list = UserProfile.objects.filter(
            Q(user__username__icontains=query)
        ).order_by('user')
        
        context = {
            'profile_list': profile_list,
        }
        
        return render(request, 'social/search.html', context)
    
class ListFollowers(View):
    def get(self, request, pk, *args, **kwargs):
        profile  = UserProfile.objects.get(pk=pk)
        followers = profile.followers.all().order_by('username')
        
        followers_info = []
        
        for follower in followers:
            if request.user in follower.profile.followers.all():
                followers_info.append([True, follower])
            else:
                followers_info.append([False, follower])
                
        context = {
            'profile': profile,
            'followers': followers,
            'followers_info': followers_info,
        }
        
        return render(request, 'social/followers_list.html/', context)

class AddCommentLike(LoginRequiredMixin, View):
    def post(self, request, pk,*args, **kwargs):
        comment = Comment.objects.get(pk=pk)
        
        is_dislike = False
        
        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break
        
        if is_dislike:
            comment.dislikes.remove(request.user)
        
        is_likes = False
        
        for like in comment.likes.all():
            if like == request.user:
                is_likes = True
                break
            
        if not is_likes:
            comment.likes.add(request.user)
            notification = Notification.objects.create(notification_type=1, from_user=request.user, to_user=comment.author, comment=comment)
        if is_likes:
            comment.likes.remove(request.user)    
        
        next = request.POST.get('next', '/')
        
        return HttpResponseRedirect(next)

class AddCommentDisLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)
        
        is_likes = False
        
        for like in comment.likes.all():
            if like == request.user:
                is_likes = True
                break
        
        if is_likes:
            comment.likes.remove(request.user)
        
        is_dislike = False
        
        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break
        
        if not is_dislike:
            comment.dislikes.add(request.user)
        if is_dislike:
            comment.dislikes.remove(request.user)
        
        next = request.POST.get('next', '/')
        
        return HttpResponseRedirect(next)
 
class PostNotification(View):
    def get(self, request, notification_pk, post_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        post = Post.objects.get(pk=post_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('post-detail', pk=post_pk)

class FollowNotification(View):
    def get(self, request, notification_pk, profile_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        profile = UserProfile.objects.get(pk=profile_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('profile', pk=profile_pk)

class ThreadNotification(View):
    def get(self, request, notification_pk, object_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        thread = ThreadModel.objects.get(pk=object_pk)

        notification.user_has_seen = True
        notification.save()
        
        return redirect('thread', pk=object_pk)

class RemoveNotification(View):
    def delete(self, request, notification_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)

        notification.user_has_seen = True
        notification.save()

        return HttpResponse('Success', content_type='text/plain')

class ListThreads(View):
    def get(self, request, *args, **kwargs):
        threads = ThreadModel.objects.filter(Q(user=request.user) | Q(receiver=request.user) )
        
        
        context = {
            'threads': threads,
        }
        
        return render(request, 'social/inbox.html', context)

class CreateThread(View):
    def get(self, request, *args, **kwargs):
        form = ThreadForm()
        
        context = {
            'form': form,
        }
        
        return render(request, 'social/create_thread.html', context)
        
    def post(self, request, *args, **kwargs):
        form = ThreadForm(request.POST)
        
        username = request.POST.get('username')
        
        try:
            receiver = User.objects.get(username=username)
            if ThreadModel.objects.filter(user=request.user, receiver=receiver).exists():
                thread = ThreadModel.objects.filter(user=request.user, receiver=receiver)
                
                return redirect('thread', pk=thread.pk)
                
            elif ThreadModel.objects.filter(user=receiver, receiver=request.user).exists():
                thread = ThreadModel.objects.filter(user=receiver, receiver=request.user)
                
                return redirect('thread', pk=thread.pk)
            
            if form.is_valid():
                thread = ThreadModel(
                    user=request.user,
                    receiver=receiver
                )
                thread.save()
                return redirect('thread', pk=thread.pk) 
        except:
            
            messages.error(request, "Nom d'utilisateur incorrect")
            return redirect('post-list')
        
class ThreadView(View):
    def get(self, request, pk, *args, **kwargs):
        form = MessageForm()
        thread = ThreadModel.objects.get(pk=pk)
        message_list = MessageModel.objects.filter(thread__pk__contains=pk, is_deleted=False)
        
        context = {
            'thread': thread,
            'form': form,
            'message_list': message_list
        }

        return render(request, 'social/thread.html', context)

class CreateMessage(View):
    def post(self, request, pk, *args, **kwargs):
        form = MessageForm(request.POST, request.FILES)
        thread = ThreadModel.objects.get(pk=pk)
        if thread.receiver == request.user:
            receiver = thread.user
        else:
            receiver = thread.receiver
            
        notification = Notification.objects.create(
            notification_type=4,
            from_user=request.user,
            to_user=receiver,
            thread=thread, 
        )

        if form.is_valid():
            message = form.save(commit=False)
            message.thread = thread
            message.sender_user = request.user
            message.receiver_user = receiver
            message.save()
            
        return redirect('thread', pk=pk)

class DeleteMessage(View):
    def get(self, request, pk, message_pk, *args, **kwargs):
        message_list = MessageModel.objects.filter(thread__pk__contains=pk)
        for message in message_list:
            if message.pk == message_pk:
                message.is_deleted = True
                message.save()
        return redirect('thread', pk=pk)
        
class CreateFriendRequest(View):
    def post(self, request, to_user_pk, *args, **kwargs):
        to_user = User.objects.get(pk=to_user_pk)
        if FriendRequest.objects.filter(from_user=request.user, to_user=to_user).exists():
            pass
        else:
            FriendRequest.objects.create(from_user=request.user, to_user=to_user)
        
        return redirect('profile', pk=to_user_pk)

class AcceptFriendRequest(View):
    def post(self, request, request_pk, *args, **kwargs):
        friend_request = FriendRequest.objects.get(pk=request_pk)
        friend_request.is_accepted = True
        friend_request.save()
        
        profile = UserProfile.objects.get(pk=friend_request.from_user.pk)
        profile.followers.add(request.user)

        request.user.profile.followers.add(friend_request.from_user)

        notification = Notification.objects.create(notification_type=5, from_user=request.user, to_user=friend_request.from_user)
        return redirect('post-list')
    
class RejectFriendRequest(View):
    def post(self, request, request_pk, *args, **kwargs):
        friend_request = FriendRequest.objects.get(pk=request_pk)
        friend_request.delete()


        return redirect('post-list')
    
class SharedPostView(View):
    def post(self, request, pk, *args, **kwargs):
        original_post = Post.objects.get(pk=pk)
        form = ShareForm(request.POST)
        
        if form.is_valid():
            new_post = Post(
                shared_body = self.request.POST.get('body'),
                body = original_post.body,
                author = original_post.author,
                created_on = original_post.created_on,
                shared_user = request.user,
                shared_on = timezone.now(),
            )
            new_post.save()
            
            for img in original_post.image.all():
                new_post.image.add(img)
            
            new_post.save()
        return redirect('post-list')

class Explore(View):
    def get(self, request, *args, **kwargs):
        explore_form = ExploreForm()
        query = self.request.GET.get('query')
        tag = Tag.objects.filter(name=query).first()
        if tag:
            posts = Post.objects.filter(tags__in=[tag])
        else:
            posts = Post.objects.all()
            
        
        post_data = []
        for post in posts:
            is_liked = False
            post.created_on = post.created_on.strftime("%d/%m/%Y")
            post.body = linebreaks(post.body)
            if post.image:
                if request.user in post.likes.all():
                    is_liked = True
                post_data.append([post.is_followed_by(request.user), post, post.image.url, is_liked])
            else:
                if request.user in post.likes.all():
                    is_liked = True
                post_data.append([post.is_followed_by(request.user), post, False, is_liked])

        context = {
            'tag': tag,
            'posts': post_data,
            'explore_form': explore_form,
        }
        
        return render(request, 'social/explore.html', context)
    
    def post(self, request, *args, **kwargs):
        explore_form = ExploreForm(request.POST)
        
        if explore_form.is_valid():
            query = explore_form.cleaned_data['query']
            tag = Tag.objects.filter(name=query).first()
            
            posts = None
            if tag:
                posts = Post.objects.filter(tags__in=[tag])
                
                post_data = []
                for post in posts:
                    post.created_on = post.created_on.strftime("%d/%m/%Y")
                    
                    post.body = linebreaks(post.body)
                    if post.image:
                        if request.user in post.likes.all():
                            is_liked = True
                            post_data.append([post.is_followed_by(request.user), post, post.image.url, is_liked])
                    else:
                        if request.user in post.likes.all():
                            is_liked = True
                            post_data.append([post.is_followed_by(request.user), post, False, is_liked])

            return HttpResponseRedirect(f'explore?query={query}')
        
        return HttpResponseRedirect('explore/')