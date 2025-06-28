from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseForbidden

from django.http import JsonResponse
from django.views.decorators.http import require_POST

from django.shortcuts import render, redirect
from .forms import TrackForm
from .models import Track
from django.shortcuts import get_object_or_404


def home(request):
    if request.user.is_authenticated:
        return render(request, 'home2.html', {'user': request.user})
    else:
        return render(request, 'home.html')
    
def home2(request):
    user = request.user
    user_tracks = Track.objects.filter(uploaded_by=user)

    return render(request, 'home2.html', {
        'user': user,
        'tracks': user_tracks,
    })

@login_required(login_url='login')  
def upload_track(request):
	if request.method == "POST":
		form = TrackForm(request.POST, request.FILES)  
		if form.is_valid():
			track=form.save(commit=False)
			track.uploaded_by = request.user
			track.save()
			return render(request,'update.html',{'track':track})

  
	else:
		form = TrackForm()

	return render(request, 'upload.html', {'form': form})

def view_tracks(request):
    query=request.GET.get('q')
    if query:
        tracks=Track.objects.filter(Q(title__icontains=query) | Q(artist__icontains=query))
    else:
        tracks=Track.objects.all()
    return render(request,'view_tracks.html',{'tracks':tracks,'query':query})

def delete_track(request,pk):
    track=get_object_or_404(Track,pk=pk)
    if track.uploaded_by!=request.user:
        messages.error(request, "You are not allowed to delete this track.")
        return redirect('view_tracks')
    if request.method=="POST":
        track.delete()
        messages.success(request, "Track deleted successfully.")
        return redirect('view_tracks')
    return render(request,'delete.html',{'track':track})



def signup_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Account already exists with same username. Please choose a different one or login.")
            return redirect('signup')  # or render the form again with an error
        else:
            user = User.objects.create_user(username=username, password=password)
            messages.success(request, "Signup successful. Please log in.")
            return redirect('login')
    
    return render(request, 'signup.html')


# Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home2')  # change to your desired page
        else:
            messages.error(request, "Invalid credentials")
            return render(request, 'login.html')

    return render(request, 'login.html')

# Logout View
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def like_track(request, track_id):
    if request.method == 'POST':
        track = get_object_or_404(Track, id=track_id)
        user = request.user

        if user in track.likes.all():
            track.likes.remove(user)
            liked = False
        else:
            track.likes.add(user)
            liked = True

        return JsonResponse({
            'liked': liked,
            'like_count': track.likes.count()
        })