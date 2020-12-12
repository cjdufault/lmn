from django.urls import path
from django.contrib.auth import views as auth_views
from . import api_views
from . import views
from .views import views_main, views_artists, views_venues, views_notes, views_users


# app_name = 'lmn'

urlpatterns = [

    path('', views_main.homepage, name='homepage'),

    # Venue-related
    path('venues/list/', views_venues.venue_list, name='venue_list'),
    path('venues/detail/<int:venue_pk>/', views_venues.venue_detail, name='venue_detail'),
    path('venues/artists_at/<int:venue_pk>/', views_venues.artists_at_venue, name='artists_at_venue'),

    # Note related
    path('notes/latest/', views_notes.latest_notes, name='latest_notes'),
    path('notes/my_notes/', views_notes.user_notes, name='user_notes'),
    path('notes/detail/<int:note_pk>/', views_notes.note_detail, name='note_detail'),
    path('notes/for_show/<int:show_pk>/', views_notes.notes_for_show, name='notes_for_show'),
    path('notes/add/<int:show_pk>/', views_notes.new_note, name='new_note'),
    path('notes/<int:note_pk>/delete', views_notes.delete_note, name='delete_note'), #delete note feature
    path('notes/<int:note_pk>/modify', views_notes.modify_note, name='modify_note'),
    path('notes/best_shows/', views_notes.best_shows, name='best_shows'),

    # Artist related
    path('artists/list/', views_artists.artist_list, name='artist_list'),
    path('artists/detail/<int:artist_pk>/', views_artists.artist_detail, name='artist_detail'),
    path('artists/venues_played/<int:artist_pk>/', views_artists.venues_for_artist, name='venues_for_artist'),

    # User related
    path('user/profile/<int:user_pk>/', views_users.user_profile, name='user_profile'),
    path('user/profile/', views_users.my_user_profile, name='my_user_profile'),

    # Account related
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', views_users.logout_user, name='logout'),
    path('register/', views_users.register, name='register'),

    # Api related
    path('artist', api_views.get_artist, name='admin_get_artist'),
    path('venue', api_views.get_venue, name='admin_get_venue'),
    path('show', api_views.get_show, name='admin_get_show'),

]
