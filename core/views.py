from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, LikePost, FollowersCount
from itertools import chain
import random

from .models import SmallBusiness, BusinessPost
from django.http import JsonResponse, HttpResponseNotAllowed

from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .forms import SmallBusinessForm

from django.shortcuts import render, redirect,get_object_or_404
from .models import SmallBusiness
from .models import ContactMessage

from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.http import HttpResponseNotFound

from django.contrib.auth.decorators import login_required
from .models import Notification
from .models import Profile
from .models import Logement
import logging
from .forms import SmallBusinessForm, BusinessPostForm
from .models import Comment

from .models import Transport  
from .models import Stage # Assurez-vous d'importer votre modèle de transport
from .models import Post
from .models import Evenement
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Logement

from datetime import datetime
from django import forms

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .forms import CommentForm
from .forms import CommentForm

def business_posts(request, business_id):
    business = get_object_or_404(SmallBusiness, pk=business_id)
    posts = BusinessPost.objects.filter(business=business)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            post_id = request.POST.get('post_id')
            post = get_object_or_404(BusinessPost, pk=post_id)
            comment = Comment(post=post, content=content)
            comment.save()
            return redirect('business_posts', business_id=business_id)
    else:
        form = CommentForm()

    return render(request, 'business_posts.html', {'business': business, 'posts': posts, 'form': form})

# Create your views here.
@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    user_following_list = []
    feed = []
    
    user_following = FollowersCount.objects.filter(follower=request.user.username)
    logement_posts = Logement.objects.all()

    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        feed.append(feed_lists)

    feed_list = list(chain(*feed))

    # user suggestion starts
    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)
    
    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(new_suggestions_list) if ( x not in list(current_user))]
    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))

    # Retrieve notifications for the current user
    notifications = Notification.objects.filter(user=request.user)
    unread_notifications_count = Notification.objects.filter(user=request.user, is_read=False).count()


    return render(request, 'index.html', {'user_profile': user_profile, 'posts':feed_list, 'logement_posts': logement_posts,'suggestions_username_profile_list': suggestions_username_profile_list[:4], 'notifications': notifications, 'unread_notifications_count': unread_notifications_count})
@login_required(login_url='signin')
def upload(request):

    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']
        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect('/')
    else:
        return redirect('/')

@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)
        
        username_profile_list = list(chain(*username_profile_list))
    return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})

@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes + 1
        post.save()
        return JsonResponse({'likes': post.no_of_likes})  # Retourne le nombre de likes sous forme de réponse JSON
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes - 1
        post.save()
        return JsonResponse({'likes': post.no_of_likes})  # Retourne le nombre de likes sous forme de réponse JSON

@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)

    follower = request.user.username
    user = pk

    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,
    }
    return render(request, 'profile.html', context)
User = get_user_model()

@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')

@login_required(login_url='signin')


def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        # Récupérer les données du formulaire
        bio = request.POST.get('bio', '')
        location = request.POST.get('location', '')
        # Enregistrer les informations dans le champ intro
        user_profile.intro = f"Bio: {bio}, Location: {location}"
        user_profile.save()

        # Rediriger l'utilisateur vers la page des paramètres
        return redirect('settings')

    return render(request, 'setting.html', {'user_profile': user_profile})

def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                #create a Profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
        
    else:
        return render(request, 'signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            # Rediriger vers la page de profil
            return redirect('profile', pk=username)  # Assurez-vous que le nom de l'URL pour la page de profil est correct
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('signin')  # Rediriger vers la page de connexion en cas d'échec de connexion

    return render(request, 'signin.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')
@login_required
def acceuil(request):
    return render(request, 'acceuil.html')
def home(request):
    return render(request, 'home.html')
def delete_post(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(pk=post_id)
        post.delete()
    return redirect('index')
@login_required(login_url='signin')
def edit_post(request, post_id):
    # Récupérer la publication à modifier
    post = Post.objects.get(pk=post_id)
    
    if request.method == 'POST':
        # Traiter les données du formulaire de modification de la publication
        if 'image' in request.FILES:
            # Si un nouveau fichier a été téléchargé, mettez à jour l'image de la publication
            post.image = request.FILES['image']
            post.save()
            return JsonResponse({'imageUrl': post.image.url})  # Retourner l'URL de l'image mise à jour sous forme de réponse JSON
     
    return HttpResponse(status=400)
def hom(request):
    return render(request, 'hom.html')





from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from .models import Stage

@login_required(login_url='signin')
def upload_stage_post(request):
    if request.method == 'POST':
        # Traiter la logique de votre formulaire POST ici
        pass  # Remplacez cette instruction par votre logique
        
    # Récupérer tous les stages depuis la base de données
    stages = Stage.objects.all()
    
    # Passer les stages au template
    return render(request, 'upload_stage_post.html', {'stages': stages})

@login_required(login_url='signin')
def upload_transport_post(request):
    # Récupérer tous les transports existants depuis la base de données
    transports = Transport.objects.all()
    # Passer les transports au template
    return render(request, 'upload_transport_post.html', {'transports': transports})
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Transport, Reservation

@login_required(login_url='signin')
def reserve_transport(request, transport_id):
    transport = get_object_or_404(Transport, pk=transport_id)

    # Vérifier si l'utilisateur a déjà réservé ce transport
    if transport.reserve_par == request.user:
        return JsonResponse({'error': 'Vous avez déjà réservé ce transport.'}, status=400)

    # Vérifier si des places sont disponibles
    if transport.nbr_places_disponibles > 0 and not transport.est_reserve:
        # Mettre à jour les informations sur la réservation
        transport.est_reserve = True
        transport.nbr_reservations += 1
        transport.nbr_places_disponibles -= 1  # Diminuer le nombre de places disponibles
        transport.reserve_par = request.user  # Marquer l'utilisateur comme réservant ce transport
        transport.save()
        # Renvoyer une réponse JSON indiquant que la réservation a été effectuée avec succès
        return JsonResponse({'message': 'Réservation effectuée avec succès.', 'nbr_places_disponibles': transport.nbr_places_disponibles})
    else:
        # Renvoyer une réponse JSON indiquant que la réservation n'a pas pu être effectuée
        return JsonResponse({'error': 'Impossible de réserver ce transport.'}, status=400)



@login_required(login_url='signin')
def upload_logement_post(request):
    # Récupérer tous les logements existants depuis la base de données
    logements = Logement.objects.all()
    # Passer les logements au template
    return render(request, 'upload_logement_post.html', {'logements': logements})
@login_required(login_url='signin')
def upload_stag_post(request):
    # Récupérer tous les stages existants depuis la base de données
    stags = Evenement.objects.all()
    # Passer les stages au template
    return render(request, 'upload_stag_post.html', {'stags': stags})
@login_required  # Décorateur pour s'assurer que l'utilisateur est connecté
def toggle_interest(request, evenement_id):
    evenement = Evenement.objects.get(pk=evenement_id)
    if request.user.is_authenticated:
        if request.user in evenement.interesses.all():
            evenement.interesses.remove(request.user)
            evenement.nb_interessés -= 1
        else:
            evenement.interesses.add(request.user)
            evenement.nb_interessés += 1
        evenement.save()
    
    # Renvoyer les données mises à jour sous forme de JSON
    return JsonResponse({'nb_interesses': evenement.nb_interessés})
logger = logging.getLogger(__name__)

@login_required(login_url='signin')
def create_post_view(request):
    logger.info("start creating post view")
    if request.method == 'POST':
        logger.info("starting post")
        post_type = request.POST.get('post_type')

        if post_type == 'Stage':
            logger.info("start creating stage")
            sujet = request.POST.get('sujet')
            type = request.POST.get('type')
            description = request.POST.get('description')
            utilisateur = Profile.objects.get(user=request.user) 
            stage = Stage.objects.create(sujet=sujet,type=type, description=description, utilisateur=utilisateur)
            stage.save()
            messages.success(request, 'Le post de stage a été ajouté avec succès!')
            logger.info("finish creating stage")
        elif post_type == 'Transport':
            destination = request.POST.get('destination')
            moyen_transport = request.POST.get('moyen_transport')
            description = request.POST.get('description')
            utilisateur = Profile.objects.get(user=request.user) 
            transport = Transport.objects.create(destination=destination, moyen_transport=moyen_transport, description=description, utilisateur=utilisateur)
            transport.save()
            messages.success(request, 'Le post de transport a été ajouté avec succès!')
        elif post_type == 'Logement':
            adresse = request.POST.get('adresse')
            prix = request.POST.get('prix')
            description = request.POST.get('description')
            utilisateur = Profile.objects.get(user=request.user) 
            logement = Logement.objects.create(adresse=adresse, prix=prix, description=description, utilisateur=utilisateur)
            logement.save()
            messages.success(request, 'Le post de logement a été ajouté avec succès!')
        elif post_type == 'Evenement':
            # Traitement pour la création d'un événement
            type_evenement = request.POST.get('type')
            titre = request.POST.get('titre')
            description = request.POST.get('description')
            utilisateur = Profile.objects.get(user=request.user)
            evenement = Evenement.objects.create(type=type_evenement, titre=titre, description=description, utilisateur=utilisateur)
            evenement.save()
            messages.success(request, 'Lévénement a été ajouté avec succès!')



        return redirect('create-post')  # Rediriger vers la même page après avoir ajouté le post

    else:
        # Si la méthode n'est pas POST, affichez simplement le formulaire
        post_type = request.GET.get('post_type')
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

    return render(request, 'create_post.html', {'post_type': post_type, 'user_profile': user_profile})

def reserve_logement(request, logement_id):
    logement = get_object_or_404(Logement, pk=logement_id)
    if request.user.is_authenticated:
        # Vérifier si l'utilisateur a déjà réservé ce logement
        if request.user == logement.logement_reserve_par:
            return JsonResponse({'error': 'Vous avez déjà réservé ce logement.'}, status=400)

        # Mettre à jour le nombre de réservations du logement
        logement.nbr_logements_reserves += 1
        
        # Enregistrer l'utilisateur qui a réservé
        logement.logement_reserve_par = request.user
        
        # Enregistrer les modifications dans la base de données
        logement.save()

        data = {
            'message': 'Réservé avec succès!',
            'nb_logements_reserves': logement.nbr_logements_reserves
        }
        Notification.objects.create(
            user=logement.utilisateur.user,  # Propriétaire du transport
            message=f"{request.user.username} a réservé votre transport '{logement.destination}'.",
            post_type='transport',
            post_id=logement.id
        )
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Vous devez être connecté pour réserver un logement.'}, status=401)
@login_required(login_url='signin')
def toggle_interest_stage(request, stage_id):
    stage = get_object_or_404(Stage, pk=stage_id)
    if request.user.is_authenticated:
        if request.user in stage.interesses.all():
            stage.interesses.remove(request.user)
            stage.nombre_interets -= 1
        else:
            stage.interesses.add(request.user)
            stage.nombre_interets += 1
        # Sauvegardez les modifications apportées au stage
        stage.save()
        
        # Créer une notification lorsque l'utilisateur s'intéresse à un stage
        Notification.objects.create(
            user=stage.utilisateur.user,  # Propriétaire du stage
            message=f"{request.user.username} s'intéresse à votre stage '{stage.sujet}'.",
            post_type='stage',
            post_id=stage.id
        )
        
    # Renvoyez les données mises à jour sous forme de JSON
    return JsonResponse({'nb_interesses': stage.interesses.count()})
def random_post(request):
    # Récupérer tous les objets de chaque modèle
    stages = Stage.objects.all()
    transports = Transport.objects.all()
    logements = Logement.objects.all()

    # Concaténer les listes d'objets
    all_posts = list(stages) + list(transports) + list(logements)

    # Sélectionner un post aléatoire
    random_post = random.choice(all_posts)

    # Passer le post aléatoire au template pour l'affichage
    return render(request, 'random_post.html', {'random_post': random_post})
def notifications(request):
    user_notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'notifications.html', {'notifications': user_notifications})
@csrf_exempt
def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        try:
            # Envoi de l'e-mail
            send_mail(
                'Nouveau message de contact',
                f'Nom: {name}\nEmail: {email}\nMessage: {message}',
                'yosrabdeladhime16*.com',  # Remplacez par votre adresse e-mail
                ['yosrabdeladhime16*.com'],  # Remplacez par l'adresse e-mail de destination
                fail_silently=False,
            )

            # Enregistrement du message dans la base de données
            ContactMessage.objects.create(name=name, email=email, message=message)

            return JsonResponse({'success': True})
        except Exception as e:
            # En cas d'erreur lors de l'envoi de l'e-mail
            print(e)  # Afficher l'erreur dans la console
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'})
@login_required
def update_profile(request):
    if request.method == 'POST':
        # Récupérez les données du formulaire
        image = request.FILES.get('profilePhoto')
        bio = request.POST.get('bio')

        # Mettez à jour le modèle de profil de l'utilisateur
        profile = Profile.objects.get(user=request.user)
        profile.bio = bio
        if image:
            profile.profileimg = image
        profile.save()

        # Retournez une réponse JSON indiquant que la page doit être rechargée
        return JsonResponse({'message': 'reload'})

    else:
        # Retournez une réponse HTTP 405 (Method Not Allowed)
        return HttpResponseNotAllowed(['POST'])

def business_list(request):
    businesses = SmallBusiness.objects.all()
    return render(request, 'business_list.html', {'businesses': businesses})

from django.shortcuts import render, get_object_or_404
from .models import SmallBusiness, Post

def like_postss(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = get_object_or_404(BusinessPost, pk=post_id)
        post.likes += 1
        post.save()
        return JsonResponse({'likes': post.likes})
    else:
        return JsonResponse({'error': 'Invalid request'})


def business_posts(request, business_id):
    # Récupérer le small business spécifique à partir de son ID
    business = get_object_or_404(SmallBusiness, pk=business_id)
    # Récupérer tous les posts associés à ce small business
    posts = Post.objects.filter(business=business)
    return render(request, 'business_detail.html', {'business': business, 'posts': posts})

def business_detail(request, business_id):
    business = get_object_or_404(SmallBusiness, pk=business_id)
    posts = business.posts.all()  # Récupérer toutes les publications associées à cette entreprise
    return render(request, 'business_detail.html', {'business': business, 'posts': posts})
from django.shortcuts import render, redirect
from .forms import SmallBusinessForm

def create_small_business(request):
    if request.method == 'POST':
        form = SmallBusinessForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('business_list')  # Rediriger vers la page Business List après la création du Small Business
    else:
        form = SmallBusinessForm()
    return render(request, 'create_small_business.html', {'form': form})
def add_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            post_id = request.POST.get('post_id')
            content = form.cleaned_data['content']
            post = get_object_or_404(BusinessPost, pk=post_id)
            comment = Comment(post=post, content=content)
            comment.save()
            return redirect('business_posts', business_id=post.business.id)
    return redirect('business_list')  # Redirection vers une page appropriée en cas d'erreur ou de requête invalide
from django.shortcuts import get_object_or_404, redirect
from .models import Post, Comnt
from .forms import ComntForm

from django.http import JsonResponse

def add_comnt(request):
    if request.method == 'POST':
        form = ComntForm(request.POST)
        if form.is_valid():
            post_id = request.POST.get('post_id')
            content = form.cleaned_data['content']
            post = get_object_or_404(Post, pk=post_id)
            comnt = Comnt(post=post, content=content)
            comnt.save()
            return JsonResponse({
                'success': True,
                'user': comnt.post.user.username,
                'content': comnt.content
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'Invalid form data'
            })
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Transport, Reservation

@csrf_exempt
def reserve_transport(request, transport_id):
    if request.method == 'POST':
        transport = get_object_or_404(Transport, id=transport_id)
        user = request.user

        # Vérifiez si l'utilisateur a déjà réservé ce transport
        if Reservation.objects.filter(user=user, transport=transport).exists():
            return JsonResponse({'error': 'Vous avez déjà réservé ce transport.'}, status=400)

        # Vérifiez si des places sont disponibles
        if transport.nbr_places_disponibles <= 0:
            return JsonResponse({'error': 'Aucune place disponible.'}, status=400)

        # Créez la réservation
        reservation = Reservation.objects.create(user=user, transport=transport)
        transport.nbr_places_disponibles -= 1
        transport.save()

        return JsonResponse({'nbr_places_disponibles': transport.nbr_places_disponibles})
    
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
