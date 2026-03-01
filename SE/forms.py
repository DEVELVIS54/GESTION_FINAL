# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profil
from django.contrib.auth import authenticate  # ← AJOUTE CETTE LIGNE !
import re
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
class InscriptionForm(UserCreationForm):
    
    """
    Formulaire d'inscription personnalisé avec choix de profil
    """
    
    # Champs supplémentaires pour l'inscription
    ROLE_CHOICES = [
        ('', '--- Choisir votre profil ---'),
        ('client', '👤 Client'),
        ('bailleur', '👑 Bailleur'),
        ('agent', '🤝 Agent'),
        ('manager', '👨‍💼 Manager'),
    ]
    
    # Champ pour le rôle
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_role_field'
        })
    )
    
    # Champ téléphone
    telephone = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: 01 23 45 67 89',
            'id': 'id_telephone'
        }),
        help_text="Format: 10 chiffres minimum"
    )
    
    # Champ email
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'votre@email.com',
            'id': 'id_email'
        })
    )
    
    # Champ nom
    nom = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre nom',
            'id': 'id_nom'
        })
    )
    
    # Champ prénom
    prenom = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre prénom',
            'id': 'id_prenom'
        })
    )
    
    class Meta:
        model = User
        fields = ['role', 'nom', 'prenom', 'email', 'username', 'telephone', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Personnaliser les champs existants de UserCreationForm
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Choisissez un nom d\'utilisateur',
            'id': 'id_username'
        })
        
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Mot de passe (min 8 caractères)',
            'id': 'id_password1'
        })
        
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirmer le mot de passe',
            'id': 'id_password2'
        })
        
        # Personnaliser les labels
        self.fields['password1'].label = "Mot de passe"
        self.fields['password2'].label = "Confirmation du mot de passe"
    
    def clean_email(self):
        """
        Vérifier que l'email n'existe pas déjà
        """
        email = self.cleaned_data.get('email')
        
        if User.objects.filter(email=email).exists():
            raise ValidationError("Cette adresse email est déjà utilisée.")
        
        return email
    
    def clean_telephone(self):
        """
        Valider le numéro de téléphone
        """
        telephone = self.cleaned_data.get('telephone')
        
        # Nettoyer le numéro (enlever les espaces, tirets, etc.)
        telephone_nettoye = re.sub(r'[^\d+]', '', telephone)
        
        # Vérifier la longueur minimale
        if len(telephone_nettoye) < 8:
            raise ValidationError("Le numéro de téléphone doit contenir au moins 8 chiffres.")
        
        return telephone_nettoye
    
    def clean_password2(self):
        """
        Validation supplémentaire pour les mots de passe
        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        
        if password1 and password2 and password1 != password2:
            raise ValidationError("Les mots de passe ne correspondent pas.")
        
        # Vérifier la force du mot de passe
        if len(password1) < 8:
            raise ValidationError("Le mot de passe doit contenir au moins 8 caractères.")
        
        if not any(char.isdigit() for char in password1):
            raise ValidationError("Le mot de passe doit contenir au moins un chiffre.")
        
        if not any(char.isalpha() for char in password1):
            raise ValidationError("Le mot de passe doit contenir au moins une lettre.")
        
        return password2
    
    def save(self, commit=True):
        """
        Surcharge de la méthode save pour créer l'utilisateur ET le profil
        """
        # Créer l'utilisateur User standard
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['prenom']
        user.last_name = self.cleaned_data['nom']
        
        if commit:
            # Sauvegarder l'utilisateur
            user.save()
            
            # Créer le profil avec le rôle et le téléphone
            try:
                profil = Profil.objects.create(
                    user=user,
                    role=self.cleaned_data['role'],
                    telephone=self.cleaned_data['telephone']
                )
                profil.save()
                print(f"✅ Profil créé pour {user.username} - Rôle: {profil.role}")
            except Exception as e:
                print(f"❌ Erreur création profil: {e}")
                # Si échec création profil, supprimer l'utilisateur
                user.delete()
                raise
        
        return user


class ConnexionForm(forms.Form):
    """
    Formulaire de connexion (optionnel - pour compléter)
    """
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nom d\'utilisateur ou email'
        })
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mot de passe'
        })
    )
    
    remember_me = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )


class ProfilForm(forms.ModelForm):
    """
    Formulaire pour mettre à jour le profil (optionnel)
    """
    class Meta:
        model = Profil
        fields = ['role', 'telephone']
        widgets = {
            'role': forms.Select(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
        
        
        # ============================================
# FORMULAIRE DE CONNEXION
# ============================================

class ConnexionForm(AuthenticationForm):
    """
    Formulaire de connexion personnalisé
    """
    username = forms.CharField(
        label="Nom d'utilisateur ou Email",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Entrez votre nom d\'utilisateur',
            'autofocus': True
        })
    )
    
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Entrez votre mot de passe'
        })
    )
    
    remember_me = forms.BooleanField(
        label="Se souvenir de moi",
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    
    def clean(self):
        """
        Validation personnalisée - Permet la connexion avec email OU username
        """
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username and password:
            # Essayer d'abord avec username
            self.user_cache = authenticate(username=username, password=password)
            
            # Si ça échoue, essayer avec email
            if self.user_cache is None:
                try:
                    user = User.objects.get(email=username)
                    self.user_cache = authenticate(username=user.username, password=password)
                except User.DoesNotExist:
                    self.user_cache = None
            
            if self.user_cache is None:
                raise forms.ValidationError(
                    "Nom d'utilisateur/email ou mot de passe incorrect.",
                    code='invalid_login'
                )
            else:
                self.confirm_login_allowed(self.user_cache)
        
        return self.cleaned_data


# ============================================
# FORMULAIRE DE MISE À JOUR DU PROFIL
# ============================================

class ProfilUpdateForm(forms.ModelForm):
    """
    Formulaire pour mettre à jour le profil utilisateur
    """
    class Meta:
        model = Profil
        fields = ['telephone']
        widgets = {
            'telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre numéro de téléphone'
            })
        }


class UserUpdateForm(forms.ModelForm):
    """
    Formulaire pour mettre à jour les informations utilisateur
    """
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control'
        })
    )
    
    first_name = forms.CharField(
        label="Prénom",
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    
    last_name = forms.CharField(
        label="Nom",
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']