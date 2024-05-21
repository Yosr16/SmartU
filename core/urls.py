from django.urls import path, re_path
from .views import upload_stag_post, toggle_interest
from .views import  reserve_transport
from .views import  reserve_logement
from .views import random_post
from .views import  toggle_interest_stage
from .views import notifications
from .views import contact_view 
from . import views
from .views import acceuil
from .views import business_posts
from .views import business_list, business_detail
from .views import create_small_business
from .views import     update_profile

urlpatterns = [
    path('add_comment/', views.add_comment, name='add_comment'),
    path('add_comnt/', views.add_comnt, name='add_comnt'),

    path('', views.home, name='home'),
    path('like-post/', views.like_postss, name='like_postss'),
    path('create-small-business/', create_small_business, name='create_small_business'),
    path('notifications/', notifications, name='notifications'),  # Move this line to the top
    path('index', views.index, name='index'),
    path('settings', views.settings, name='settings'),
    path('upload', views.upload, name='upload'),
    path('follow', views.follow, name='follow'),
    path('search', views.search, name='search'),
    path('acceuil/', acceuil, name='acceuil'),
    path('business/', business_list, name='business_list'),  # Changer le chemin pour éviter la duplication
    path('business/<int:business_id>/', business_detail, name='business_detail'),
    path('business/<int:business_id>/posts/', business_posts, name='business_posts'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('like-post', views.like_post, name='like-post'),
    path('signup', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout', views.logout, name='logout'),
    path('create-post/', views.create_post_view, name='create-post'),
    path('delete-post/<str:post_id>/', views.delete_post, name='delete-post'),
    path('edit-post/<str:post_id>/', views.edit_post, name='edit-post'),
    path('home/', views.hom, name='hom'),
    path('update_profile/', update_profile, name='update_profile'),

    path('upload/stage/', views.upload_stage_post, name='upload_stage_post'),
    path('upload/transport/', views.upload_transport_post, name='upload_transport_post'),
    path('upload/logement/', views.upload_logement_post, name='upload_logement_post'),
    path('upload/stag/', views.upload_stag_post, name='upload_stag_post'),
    path('toggle_interest/<int:evenement_id>/', toggle_interest, name='toggle_interest'),
    path('toggl_interest/<int:stage_id>/', toggle_interest, name='toggl_interest'),
    path('toggle_interest_stage/<int:stage_id>/', toggle_interest_stage, name='toggle_interest_stage'),
    path('reserve_transport/<int:transport_id>/', reserve_transport, name='reserve_transport'),
    path('random/post/', random_post, name='random_post'),
    path('contact/', contact_view, name='contact'),
    path('reserve_logement/<int:logement_id>/', reserve_logement, name='reserve_logement'),

    # Autres chemins d'URL pour d'autres vues...
    
]
