from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
from django.utils import timezone

from django.urls import reverse
User = get_user_model()


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    location = models.CharField(max_length=100, blank=True)
 
    def __str__(self):
        return self.user.username

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)
    CATEGORY_CHOICES = [
        ('transport', 'Transport'),
        ('logement', 'Logement'),
        ('stage', 'Stage'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='logement')

    def __str__(self):
        return self.user

    def delete_post(self):
        self.delete()

class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user

class Stage(models.Model):
    TYPE_CHOICES = [
        ('ouvrier', 'ouvrier'),
        ('technicien', 'technicien'),
        ('PFE', 'PFE'),
    ]
    
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='ouvrier')
    sujet = models.CharField(max_length=100)
    description = models.TextField()
    utilisateur = models.ForeignKey(Profile, on_delete=models.CASCADE)  # Updated to use UserProfile
    date_creation = models.DateTimeField(auto_now_add=True)
    nombre_interets = models.PositiveIntegerField(default=0)
    interesses = models.ManyToManyField(User, related_name='interets')

    def __str__(self):
        return self.sujet

class Evenement(models.Model):
    TYPE_CHOICES = [
        ('culturel', 'Culturel'),
        ('scientifique', 'Scientifique'),
    ]
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    titre = models.CharField(max_length=100)
    description = models.TextField()
    utilisateur = models.ForeignKey(Profile, on_delete=models.CASCADE)  # Updated to use UserProfile
    date_creation = models.DateTimeField(auto_now_add=True)
    nb_interessés = models.PositiveIntegerField(default=0) 
    interesses = models.ManyToManyField(User, related_name='stages_interesses', blank=True)

    def __str__(self):
        return self.titre
    

class EventSocial(Evenement):
    prix = models.FloatField()

    def __str__(self):
        return self.titre

class EventClub(Evenement):
    club = models.CharField(max_length=100)

    def __str__(self):
        return self.titre

class Logement(models.Model):
    adresse = models.CharField(max_length=200)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    utilisateur = models.ForeignKey(Profile, on_delete=models.CASCADE)  # Updated to use UserProfile
    date_creation = models.DateTimeField(auto_now_add=True)
    logement_reserve_par = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)  
    nbr_logements_reserves = models.IntegerField(default=0) 

    def __str__(self):
        return self.adresse

class Transport(models.Model):
    destination = models.CharField(max_length=200)
    moyen_transport = models.CharField(max_length=50, choices=[
        ('Avion', 'Avion'),
        ('Train', 'Train'),
        ('Voiture', 'Voiture'),
        ('Bus', 'Bus'),
    ])
    description = models.TextField()
    utilisateur = models.ForeignKey(Profile, on_delete=models.CASCADE)  # Assurez-vous que Profile est correctement défini
    date_creation = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='transport_images', null=True, blank=True)
    reserve_par = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    nbr_reservations = models.IntegerField(default=0)
    disponibilite = models.DateField(default=timezone.now)
    nbr_places_disponibles = models.IntegerField(default=0)

    def __str__(self):
        return self.destination




class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    post_type = models.CharField(max_length=20, default='stage')
    post_id = models.IntegerField(default=0)
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
class SmallBusiness(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='business_images')
    utilisateur = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)  # Modifiez pour autoriser les valeurs NULL

    def get_posts_url(self):
        return reverse('business_posts', args=[self.pk])

class BusinessPost(models.Model):
    business = models.ForeignKey(SmallBusiness, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='business_posts_images')
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)  # Champ pour enregistrer le nombre de "J'aime"
    
    def __str__(self):
        return self.title
    
class Comnt(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comnts')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comnt by {self.post.user} on {self.created_at}"


class Comment(models.Model):
    post = models.ForeignKey(BusinessPost, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.post.business.name} on {self.created_at}"
    
class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE)
    date_reservation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Reservation by {self.user.username} for {self.transport.destination}'
