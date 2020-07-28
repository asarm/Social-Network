from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.urls import reverse
from django import forms
from .models import *
from django.core.paginator import Paginator

class PostForm(forms.Form):
    content = forms.CharField(label='Content',widget=forms.Textarea(attrs={'class' :'form-control col-md-8 col-lg-8','rows':8,'name':'content','id':'content'}))

class EditForm(forms.Form):
    content = forms.CharField(label='Content',widget=forms.Textarea(attrs={'class' :'form-control col-md-8 col-lg-8','rows':8,'name':'content','id':'content'}))


def index(request):
    if request.user.is_authenticated:
        posts = Post.objects.all().order_by('-date')
        current_user = request.user
        paginator = Paginator(posts,10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        if request.method == 'POST':
            post_id = request.POST['post_id']
            likedpost = Post.objects.get(pk=post_id)
            if current_user in likedpost.liked.all():
                likedpost.liked.remove(current_user)
            else:
                likedpost.liked.add(current_user)
                likedpost.save()
        return render(request,"network/index.html",{'page_obj':page_obj,'posts':posts,'current_user':current_user})
    else:
        return HttpResponseRedirect("login")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def profile(request,username):
    if request.user.is_authenticated:
        check_following = Profile.objects.filter(target_user=get_object_or_404(User, username=username),follower=request.user)
        #Following any user from profile page
        if request.method == 'POST':
            if 'post_id' in request.POST:
                current_user = request.user
                post_id = request.POST['post_id']
                likedpost = Post.objects.get(pk=post_id)
                if current_user in likedpost.liked.all():
                    likedpost.liked.remove(current_user)
                else:
                    likedpost.liked.add(current_user)
                    likedpost.save()
            else:
                current_user = request.user
                target_user = get_object_or_404(User, username=username)
                if not check_following:
                   follow = Profile.objects.create(target_user=target_user,follower=current_user)
                   follow.save()
                   check_following = Profile.objects.filter(target_user=get_object_or_404(User, username=username),
                                                            follower=request.user)

                elif check_following:
                    check_following.delete()
                    check_following = Profile.objects.filter(target_user=get_object_or_404(User, username=username),follower=request.user)

        current_user = request.user
        userpage = get_object_or_404(User, username=username)
        follower = Profile.objects.filter(follower=userpage)
        follows = Profile.objects.filter(target_user=userpage)
        follows_count = len(follows)
        follower_count = len(follower)
        posts = Post.objects.filter(user=userpage)
        return render(request,"network/profile.html",{'check_following':check_following,'current_user':current_user,'userpage':userpage,'posts':posts,'follower':follower,'follows':follows,'follows_count':follows_count,'follower_count':follower_count})
    else:
        return HttpResponseRedirect(reverse("login"))


def newPost(request):
    form = PostForm()
    username = request.user.username
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        form = PostForm(request.POST)
        content = request.POST['content']
        post = Post.objects.create(user=user,content=content)
        post.save()
        return HttpResponseRedirect(reverse("index"))
    return render(request,'network/new_post.html',{'form':form})


def error(request):
    return render(request,'network/error.html')


def editPost(request,pk):
    form = EditForm()
    post = Post.objects.get(pk=pk)

    if post.user.username != request.user.username:
        return HttpResponseRedirect(reverse("error"))

    form.fields['content'].initial = post.content
    if request.method == 'POST':
        form = EditForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            post.content = content
            post.save()
            return HttpResponseRedirect(reverse('index'))
    return render(request,'network/edit_post.html',{'form':form,'post':post})


def following_view(request):
    username = request.user.username
    current_user = get_object_or_404(User, username=username)
    try:
        following_list= Profile.objects.filter(follower=current_user)
    except:
        return render(request,'network/empty_follow_list.html')
    else:
        posts = Post.objects.all().order_by('-date')
        listed_posts = []
        for post in posts:
            for follower in following_list:
                if post.user.username in follower.target_user.username:
                    listed_posts.append(post)
    if request.method == 'POST':
        post_id = request.POST['post_id']
        likedpost = Post.objects.get(pk=post_id)
        if current_user in likedpost.liked.all():
            likedpost.liked.remove(current_user)
        else:
            likedpost.liked.add(current_user)
            likedpost.save()

    return render(request,'network/following.html',{'posts':listed_posts})


def like_post(request):
    user = request.user
    if request.method == 'GET':
        post_id = request.GET['post_id']
        likedpost = Post.objects.get(pk=post_id)
        if user in likedpost.liked.all():
            likedpost.liked.remove(user)
            like = Like.objects.get(post=likedpost, user=user)
            like.delete()
        else:
            like = Like.objects.get_or_create(post=likedpost, user=user)
            likedpost.liked.add(user)
            likedpost.save()

        return HttpResponse('Success')
