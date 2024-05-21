from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import SmallBusiness,Profile
from .models import BusinessPost


class EditProfileForm(forms.ModelForm):
    image = forms.ImageField(required=True)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'First Name'}), required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Last Name'}), required=True)
    bio = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Bio'}), required=True)
    url = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'URL'}), required=True)
    location = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Address'}), required=True)

    class Meta:
        model = Profile
        fields = ['image', 'first_name', 'last_name', 'bio', 'url', 'location']



class SmallBusinessForm(forms.ModelForm):
    class Meta:
        model = SmallBusiness
        fields = ['name', 'description', 'image']
class BusinessPostForm(forms.ModelForm):
    class Meta:
        model = BusinessPost
        fields = ['title', 'content', 'image']
class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Écrire un commentaire'}))
from django import forms
from .models import Comnt

class ComntForm(forms.Form):
        content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Écrire un commentaire'}))


