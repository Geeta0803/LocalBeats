from django.urls import path
from .views import upload_track
from .views import upload_track, view_tracks,delete_track,login_view,signup_view,logout_view,home,home2,like_track

urlpatterns = [
    path('upload/', upload_track, name='upload'),
    path('tracks/',view_tracks,name='view_tracks'),
    path('delete/<int:pk>/', delete_track, name='delete_track'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('', home, name='home'),
    path('home2/', home2, name='home2'),
    path('like/<int:track_id>/',like_track, name='like_track'),

]
