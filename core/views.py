from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.contrib.auth import get_user_model
from django.db.models import Count

from core.models import (
    Follow, 
    Post, 
    Like, 
    Comment, 
    SavedPost,
    Category
    )
from core.forms import PostCreateForm

User = get_user_model()
# Create your views here.
class HomeView(View):
    template_name = 'core/feed.html'
    form_class = PostCreateForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        all_posts = Post.objects.all()
        categories = Category.objects.all()  # Retrieve all categories
        context = {'form': form, 'all_posts': all_posts, 'categories': categories}
        return render(request, self.template_name, context)


class PostDetailView(View):
    template_name = 'core/post_detail.html'

    def get(self, request, *args, **kwargs):
        post_id = kwargs.get('id')

        try:
            post_obj = Post.objects.get(pk=post_id)
        except Exception as e:
            return redirect(request.META.get('HTTP_REFERER'))

        try:
            Like.objects.get(user=request.user, post_id=post_id)
            liked_this_post = True
        except Exception as e:
            liked_this_post = False

        try:
            SavedPost.objects.get(user=request.user, post_id=post_id)
            post_saved = True
        except Exception as e:
            post_saved = False

        context = {
            'post': post_obj, 
            'liked_this_post': liked_this_post, 
            'post_saved': post_saved,
            }
            
        return render(request, self.template_name, context=context)



from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PostCreateForm
from .models import Category, Event, Carpooling, Absence , Stage , Logement

class PostCreatView(View):
    template_name = 'core/feed.html'
    form_class = PostCreateForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)

            # Associate the post with at least one category
            category_ids = request.POST.getlist('category')
            categories = Category.objects.filter(pk__in=category_ids)
            post.save()
            post.categories.add(*categories)
            
            # Process additional fields based on the selected category
            for category_id in category_ids:
                if category_id == '1'  :  # Event category
                    departure_time = request.POST.get('departure_time')
                    typestage = request.POST.get('typestage')
                    societe = request.POST.get('societe')
                    duree = request.POST.get('duree')
                    sujet = request.POST.get('sujet')
                    contactinfo = request.POST.get('contactinfo')
                    specialite = request.POST.get('specialite')

                    category = Category.objects.get(pk=category_id)
                    stage = Stage.objects.create(departure_time=departure_time, typestage=typestage, societe=societe, duree=duree, sujet=sujet, contactinfo=contactinfo, specialite=specialite, category=category)
                    post.stage = stage
                elif category_id == '2':  # Logement category
                    start_date = request.POST.get('start_date')
                    end_date = request.POST.get('end_date')
                    location = request.POST.get('location')
                    description = request.POST.get('description')
                    contactinfo = request.POST.get('contactinfo')
                    category = Category.objects.get(pk=category_id)
                    logement = Logement.objects.create(start_date=start_date, end_date=end_date, location=location, description=description, contactinfo=contactinfo, category=category)
                    post.logement = logement
                elif category_id == '3':  # Absence category
                   event_date = request.POST.get('event_date')
                   location = request.POST.get('location')
                   contactinfo = request.POST.get('contactinfo')
                   titre = request.POST.get('titre')
                   category = Category.objects.get(pk=category_id)
                   event = Event.objects.create(event_date=event_date, location=location, contactinfo=contactinfo, titre=titre, category=category)
                   post.event = event
                elif category_id == '4':  # Carpooling category
                   departure_time = request.POST.get('departure_time')
                   destination = request.POST.get('destination')
                   depart = request.POST.get('depart')
                   nbsiege = request.POST.get('nbsiege')
                   duree = request.POST.get('duree')
                   contactinfo = request.POST.get('contactinfo')
                   category = Category.objects.get(pk=category_id)
                   carpooling = Carpooling.objects.create(departure_time=departure_time, destination=destination, depart=depart, nbsiege=nbsiege, duree=duree, contactinfo=contactinfo, category=category)
                   post.carpooling = carpooling

            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('home_feed_view')
        else:
            context = {'form': form}
            return render(request, self.template_name, context=context)



class PostDeleteView(View):

    def post(self, request, *args, **kwargs):
        post_id = kwargs.get('id')
        try:
            post_obj = Post.objects.get(pk=post_id)
        except Exception as e:
            pass

        if request.user == post_obj.user:
            post_obj.delete()

        return redirect(request.META.get('HTTP_REFERER'))


class PostSaveView(View):
    def post(self, request, *args, **kwargs):
        post_id = kwargs.get('id')
        
        try:
            post_obj = Post.objects.get(pk=post_id)
        except Exception as e:
            pass

        try:
            SavedPost.objects.create(post_id=post_id)
        except Exception as e:
            pass        

        return redirect(request.META.get('HTTP_REFERER'))


class PostUnsaveView(View):
    def post(self, request, *args, **kwargs):
        post_id = kwargs.get('id')
        
        try:
            savedpost_obj = SavedPost.objects.get(post_id=post_id)
            savedpost_obj.delete()
        except Exception as e:
            pass       

        return redirect(request.META.get('HTTP_REFERER'))


class PostLikeView(View):
    def post(self, request, *args, **kwargs):
        post_id = kwargs.get('id')

        try:
            Like.objects.get(user=request.user, post_id=post_id)
        except Exception as e:
            Like.objects.create(post_id=post_id)

        return redirect(request.META.get('HTTP_REFERER'))


class PostUnlikeView(View):
    def post(self, request, *args, **kwargs):
        post_id = kwargs.get('id')

        try:
            like_obj = Like.objects.get(user=request.user, post_id=post_id)
            like_obj.delete()
        except Exception as e:
            pass

        return redirect(request.META.get('HTTP_REFERER'))


class PostCommentView(View):
    def post(self, request, *args, **kwargs):
        post_id = kwargs.get('id')
        comment_text = request.POST.get('comment_text')
        
        Comment.objects.create(post_id=post_id, text=comment_text)

        return redirect(request.META.get('HTTP_REFERER'))


class FollowDoneView(View):
    def post(self, request, *args, **kwargs):
        followed_user_id = request.POST.get('followed_user_id')
        followed_user_obj = User.objects.get(pk=followed_user_id)

        try:
            Follow.objects.get(user=request.user, followed=followed_user_obj)
        except Exception as e:
            follow_obj = Follow.objects.create(followed=followed_user_obj)

        return redirect(request.META.get('HTTP_REFERER'))


class UnfollowDoneView(View):
    def post(self, request, *args, **kwargs):
        unfollowed_user_id = request.POST.get('unfollowed_user_id')
        unfollowed_user_obj = User.objects.get(pk=unfollowed_user_id)

        try:
            follow_obj = Follow.objects.get(user=request.user, followed=unfollowed_user_obj)
            follow_obj.delete()
        except Exception as e:
            pass

        return redirect(request.META.get('HTTP_REFERER'))


class LikedPostsView(View):
    template_name = 'core/liked_posts.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class SavedPostsView(View):
    template_name = 'core/saved_posts.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class ExplorePostsView(View):
    template_name = 'core/posts_explore.html'
    def get(self, request, *args, **kwargs):

        all_posts = Post.objects.annotate(count=Count('like')).order_by('-count')
        context = {'all_posts': all_posts}
        return render(request, self.template_name, context=context)