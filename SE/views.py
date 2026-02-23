from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.test import Client
from .models import Profil, Propriete, RendezVous, Categorie,Favori
from datetime import date
import os
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import InscriptionForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ConnexionForm
from .forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Count, Q, Sum, Avg
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Profil, Propriete, Favori, RendezVous, Categorie
import json

def accueil(request):
    # Récupérer toutes les propriétés
    proprietes = Propriete.objects.all().order_by('-id')
    
    # Récupérer les catégories pour un filtre éventuel
    categories = Categorie.objects.all()
    
    # Récupérer les dernières propriétés (optionnel)
    dernieres_proprietes = Propriete.objects.all().order_by('-id')[:6]
                                                                             
    context = {
        'proprietes': proprietes,
        'categories': categories,
        'dernieres_proprietes': dernieres_proprietes,
        }

    return render(request, 'SE/accueil.html', context)


# views.py - AJOUTEZ CETTE FONCTION


# views.py - VERSION CORRIGÉE

def connexion(request):
    """
    Vue de connexion
    """
    if request.user.is_authenticated:
        # Rediriger vers le dashboard selon le rôle
        try:
            role = request.user.profil.role
            if role == 'bailleur':
                return redirect('SE:bailleur')  # ← SANS 'SE/'
            elif role == 'agent':
                return redirect('SE:agent')     # ← SANS 'SE/'
            elif role == 'manager':
                return redirect('SE:manager')   # ← SANS 'SE/'
            else:
                return redirect('SE:client')    # ← SANS 'SE/'
        except Profil.DoesNotExist:  # ← Attrape SEULEMENT l'absence de profil
            return redirect('SE:client')
        except Exception as e:       # ← Attrape les autres erreurs mais les LOGUE
            print(f"⚠️ Erreur de redirection: {e}")
            return redirect('SE:client')
    
    if request.method == 'POST':
        form = ConnexionForm(request, data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me', False)
            
            # Authentifier l'utilisateur
            user = authenticate(username=username, password=password)
            
            if user is not None:
                # Connecter l'utilisateur
                login(request, user)
                
                # Gérer "Se souvenir de moi"
                if not remember_me:
                    request.session.set_expiry(0)
                
                messages.success(request, f"✅ Content de vous revoir {user.first_name} !")
                
                # Rediriger selon le rôle
                try:
                    role = user.profil.role
                    if role == 'bailleur':
                        return redirect('dashboard_bailleur')  # ← CORRIGÉ
                    elif role == 'agent':
                        return redirect('dashboard_agent')     # ← CORRIGÉ
                    elif role == 'manager':
                        return redirect('dashboard_manager')   # ← CORRIGÉ
                    else:
                        return redirect('dashboard_client')    # ← CORRIGÉ
                except Profil.DoesNotExist:  # ← Spécifique
                    return redirect('dashboard_client')
                except Exception as e:       # ← Avec log
                    print(f"⚠️ Erreur de redirection: {e}")
                    return redirect('dashboard_client')
        else:
            messages.error(request, "❌ Nom d'utilisateur ou mot de passe incorrect.")
    else:
        form = ConnexionForm()
    
    context = {
        'form': form,
        'page_title': 'Connexion'
    }
    
    return render(request, 'SE/connexion.html', context)




def deconnexion_view(request):
    """
    Vue de déconnexion
    """
    logout(request)
    messages.success(request, "👋 Vous avez été déconnecté avec succès.")
    return redirect('accueil')


def deconnexion_view(request):
    """
    Vue de déconnexion
    """
    logout(request)
    messages.success(request, "👋 Vous avez été déconnecté avec succès.")
    return redirect('accueil')
    
    return render(request, 'SE/connection.html')




def inscription(request):
    """
    Vue unique pour l'inscription avec création de profil
    Redirection automatique vers le dashboard
    """
    # Si l'utilisateur est déjà connecté, rediriger vers le dashboard
    if request.user.is_authenticated:
        # Déterminer le dashboard selon le rôle
        try:
            profil = request.user.profil
            if profil.role == 'bailleur':
                return redirect('/SE/dashboard_bailleur/')
            elif profil.role == 'agent':
                return redirect('/SE/dashboard_agent/')
            elif profil.role == 'manager':
                return redirect('/SE/dashboard_manager/')
            else:
                return redirect('/SE/dashboard_client/')
        except:
            return redirect('/SE/accueil/')
    
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        
        if form.is_valid():
            try:
                # Sauvegarder l'utilisateur et créer le profil
                user = form.save()
                
                # Connecter automatiquement l'utilisateur
                login(request, user)
                
                # Message de succès
                role_display = dict(form.fields['role'].choices)[form.cleaned_data['role']]
                messages.success(
                    request,
                    f"✅ Inscription réussie ! Bienvenue {user.first_name} en tant que {role_display}."
                )
                
                # Rediriger vers le dashboard selon le rôle
                role = form.cleaned_data['role']
                if role == 'bailleur':
                    return redirect('/SE/dashboard_bailleur/')
                elif role == 'agent':
                    return redirect('/SE/dashboard_agent/')
                elif role == 'manager':
                    return redirect('/SE/dashboard_manager/')
                else:  # client
                    return redirect('/SE/client/')
                    
            except Exception as e:
                messages.error(request, f"❌ Une erreur est survenue : {str(e)}")
        else:
            # Afficher les erreurs de validation
            for field, errors in form.errors.items():
                for error in errors:
                    if field == '__all__':
                        messages.error(request, error)
                    else:
                        field_name = form.fields[field].label if field in form.fields else field
                        messages.error(request, f"{field_name}: {error}")
    else:
        form = InscriptionForm()
    
    context = {
        'form': form,
        'page_title': 'Inscription'
    }
    
    
    return render(request, 'SE/inscription.html')



def agent(request):
    
    
    return render(request, 'SE/dashboard_agent.html')

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Propriete, Favori, Profil

@login_required
def client(request):
    """
    Dashboard client - Gestion complète des favoris
    """
    # VÉRIFICATION DU RÔLE CLIENT
    try:
        profil = request.user.profil
        if profil.role != 'client':
            messages.error(request, "⛔ Accès non autorisé - Espace réservé aux clients")
            return redirect('SE:connexion')
    except Profil.DoesNotExist:
        messages.error(request, "❌ Profil utilisateur introuvable")
        return redirect('SE:connexion')
    
    # TRAITEMENT DES ACTIONS POST (Ajout/Suppression)
    if request.method == 'POST':
        action = request.POST.get('action')
        
        # AJOUTER AUX FAVORIS
        if action == 'ajouter':
            propriete_id = request.POST.get('propriete_id')
            propriete = get_object_or_404(Propriete, id=propriete_id)
            
            favori_existant = Favori.objects.filter(
                client=request.user,
                propriete=propriete
            ).first()
            
            if favori_existant:
                messages.info(request, f"ℹ️ {propriete} est déjà dans vos favoris")
            else:
                Favori.objects.create(
                    client=request.user,
                    propriete=propriete
                )
                messages.success(request, f"✅ {propriete} ajouté à vos favoris")
        
        # SUPPRIMER DES FAVORIS
        elif action == 'supprimer':
            favori_id = request.POST.get('favori_id')
            favori = get_object_or_404(
                Favori, 
                id=favori_id, 
                client=request.user
            )
            propriete = favori.propriete
            favori.delete()
            messages.success(request, f"🗑️ {propriete} retiré de vos favoris")
        
        return redirect('SE:client')
    
    # AFFICHAGE DES FAVORIS (GET)
    # ✅ 'date_ajout' EXISTE dans Favori !
    favoris_list = Favori.objects.filter(
        client=request.user
    ).select_related('propriete').order_by('-date_ajout')
    
    # Pagination
    paginator = Paginator(favoris_list, 12)
    page = request.GET.get('page')
    favoris = paginator.get_page(page)
    
    # Propriétés disponibles pour ajout (hors déjà favoris)
    favoris_ids = favoris_list.values_list('propriete_id', flat=True)
    
    # ✅ Pas de 'disponible' donc on prend toutes les propriétés
    # ✅ Pas de 'date_creation' donc on trie par 'id' ou 'prix'
    proprietes_disponibles = Propriete.objects.exclude(
        id__in=favoris_ids
    ).order_by('-id')[:20]  # Trie par id (plus récent d'abord)
    
    # Statistiques
    total_favoris = favoris_list.count()
    total_proprietes = Propriete.objects.all().count()  # ✅ Toutes les propriétés
    
    context = {
        'favoris': favoris,
        'total_favoris': total_favoris,
        'total_proprietes': total_proprietes,
        'client_nom': request.user.get_full_name() or request.user.username,
        'proprietes_disponibles': proprietes_disponibles,
        'favoris_ids': list(favoris_ids),
        'page_title': 'Mes propriétés favorites',
    }
    
    return render(request, 'SE/dashboard_client.html', context)
def bailleur(request):
    
    
    return render(request, 'SE/dashboard_bailleur.html')



def propierte(request):
    
    
    return render(request, 'SE/propierte.html')



def propos(request):
    
    
    return render(request, 'SE/propos.html')





def manager(request):
    
    
    return render(request, 'SE/dashboard_manager.html')


# partie du formulaire d'inscription


# views.py


# views.py

@login_required(login_url='connexion')
def manager(request):
    """
    Tableau de bord du manager - UNE SEULE FONCTION UNIQUE
    C'est votre fonction manager(request) intégrée avec toutes les fonctionnalités
    """
    # VÉRIFICATION DU RÔLE - Accès réservé aux managers
    if not hasattr(request.user, 'profil') or request.user.profil.role != 'manager':
        messages.error(request, "❌ Accès non autorisé. Vous n'êtes pas manager.")
        return redirect('accueil')
    
    # ============================================
    # 1. STATISTIQUES GÉNÉRALES
    # ============================================
    
    # Comptes utilisateurs
    total_clients = User.objects.filter(profil__role='client').count()
    total_agents = User.objects.filter(profil__role='agent').count()
    total_bailleurs = User.objects.filter(profil__role='bailleur').count()
    total_managers = User.objects.filter(profil__role='manager').count()
    total_utilisateurs = User.objects.count()
    
    # Propriétés et transactions
    total_proprietes = Propriete.objects.count()
    proprietes_vente = Propriete.objects.filter(option='vente').count()
    proprietes_location = Propriete.objects.filter(option='location').count()
    valeur_totale = Propriete.objects.aggregate(total=Sum('prix'))['total'] or 0
    prix_moyen = Propriete.objects.aggregate(moyen=Avg('prix'))['moyen'] or 0
    
    # Rendez-vous
    total_rdv = RendezVous.objects.count()
    rdv_en_attente = RendezVous.objects.filter(statut='en_attente').count()
    rdv_confirme = RendezVous.objects.filter(statut='confirme').count()
    rdv_annule = RendezVous.objects.filter(statut='annule').count()
    
    # Favoris
    total_favoris = Favori.objects.count()
    
    # ============================================
    # 2. STATISTIQUES TEMPORELLES
    # ============================================
    
    aujourd_hui = timezone.now()
    debut_mois = aujourd_hui.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    debut_semaine = aujourd_hui - timedelta(days=aujourd_hui.weekday())
    debut_annee = aujourd_hui.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # Inscriptions
    inscriptions_aujourdhui = User.objects.filter(date_joined__date=aujourd_hui.date()).count()
    inscriptions_cette_semaine = User.objects.filter(date_joined__gte=debut_semaine).count()
    inscriptions_ce_mois = User.objects.filter(date_joined__gte=debut_mois).count()
    inscriptions_cette_annee = User.objects.filter(date_joined__gte=debut_annee).count()
    
    # Propriétés ajoutées
    proprietes_aujourdhui = Propriete.objects.filter(id__gte=aujourd_hui).count()
    proprietes_ce_mois = Propriete.objects.filter(id__gte=debut_mois).count()
    
    # Rendez-vous
    rdv_aujourdhui = RendezVous.objects.filter(date=aujourd_hui.date()).count()
    rdv_cette_semaine = RendezVous.objects.filter(date__gte=debut_semaine.date()).count()
    rdv_ce_mois = RendezVous.objects.filter(date__gte=debut_mois.date()).count()
    
    # ============================================
    # 3. PERFORMANCE DES AGENTS
    # ============================================
    
    agents = User.objects.filter(profil__role='agent').prefetch_related('profil')
    agents_performance = []
    
    for agent in agents:
        # Clients suivis par cet agent
        clients_agent = User.objects.filter(
            profil__role='client',
            proprietes_agent__agent=agent
        ).distinct().count()
        
        # Propriétés gérées par cet agent
        proprietes_agent = Propriete.objects.filter(agent=agent).count()
        
        # Rendez-vous gérés par cet agent
        rdv_agent = RendezVous.objects.filter(propriete__agent=agent).count()
        
        # Valeur des transactions
        valeur_agent = Propriete.objects.filter(agent=agent).aggregate(total=Sum('prix'))['total'] or 0
        
        # Taux de conversion (RDV confirmés)
        rdv_total = RendezVous.objects.filter(propriete__agent=agent).count()
        rdv_reussis = RendezVous.objects.filter(propriete__agent=agent, statut='confirme').count()
        taux_conversion = (rdv_reussis / rdv_total * 100) if rdv_total > 0 else 0
        
        agents_performance.append({
            'id': agent.id,
            'nom': f"{agent.first_name} {agent.last_name}",
            'username': agent.username,
            'email': agent.email,
            'telephone': agent.profil.telephone if hasattr(agent, 'profil') else '',
            'date_embauche': agent.date_joined,
            'clients': clients_agent,
            'proprietes': proprietes_agent,
            'rdv': rdv_agent,
            'valeur': valeur_agent,
            'taux_conversion': round(taux_conversion, 1),
            'performance': 'Élevée' if taux_conversion > 70 else 'Moyenne' if taux_conversion > 40 else 'Faible'
        })
    
    # Trier les agents par performance
    agents_performance = sorted(agents_performance, key=lambda x: x['taux_conversion'], reverse=True)
    
    # ============================================
    # 4. CLIENTS SANS AGENT
    # ============================================
    
    clients_sans_agent = User.objects.filter(
        profil__role='client'
    ).exclude(
        id__in=User.objects.filter(
            profil__role='client', 
            proprietes_agent__isnull=False
        ).distinct()
    ).order_by('-date_joined')
    
    total_clients_sans_agent = clients_sans_agent.count()
    clients_sans_agent = clients_sans_agent[:20]  # Limiter à 20
    
    # ============================================
    # 5. ACTIVITÉS RÉCENTES
    # ============================================
    
    # Dernières inscriptions
    dernieres_inscriptions = User.objects.order_by('-date_joined')[:15]
    
    # Derniers rendez-vous
    derniers_rdv = RendezVous.objects.select_related(
        'client', 'propriete'
    ).order_by('-date', '-heure')[:15]
    
    # Dernières propriétés
    dernieres_proprietes = Propriete.objects.select_related(
        'bailleur', 'agent', 'categorie'
    ).order_by('-id')[:15]
    
    # Derniers favoris
    derniers_favoris = Favori.objects.select_related(
        'client', 'propriete'
    ).order_by('-id')[:10]
    
    # ============================================
    # 6. STATISTIQUES PAR CATÉGORIE
    # ============================================
    
    categories = Categorie.objects.all()
    stats_categories = []
    for cat in categories:
        nb_proprietes = Propriete.objects.filter(categorie=cat).count()
        if nb_proprietes > 0:
            stats_categories.append({
                'nom': cat.type_categorie,
                'nb_proprietes': nb_proprietes,
                'prix_moyen': Propriete.objects.filter(categorie=cat).aggregate(Avg('prix'))['prix__avg'] or 0
            })
    
    # ============================================
    # 7. STATISTIQUES PAR VILLE (à partir des adresses)
    # ============================================
    
    # Extraction simple des villes (à adapter selon votre format d'adresse)
    villes = {}
    for prop in Propriete.objects.all()[:100]:  # Limiter pour performance
        adresse = prop.adresse
        # Tentative d'extraire la ville (simplifié)
        parties = adresse.split(',')
        if len(parties) > 1:
            ville = parties[-1].strip()
        else:
            ville = 'Non spécifiée'
        
        if ville not in villes:
            villes[ville] = 0
        villes[ville] += 1
    
    top_villes = sorted(villes.items(), key=lambda x: x[1], reverse=True)[:10]
    
    # ============================================
    # 8. GESTION DES ACTIONS POST
    # ============================================
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        # --- AJOUTER UN UTILISATEUR ---
        if action == 'ajouter_utilisateur':
            try:
                role = request.POST.get('role')
                nom = request.POST.get('nom')
                prenom = request.POST.get('prenom')
                email = request.POST.get('email')
                username = request.POST.get('username')
                telephone = request.POST.get('telephone')
                password = request.POST.get('password', 'Passer@123')
                
                # Vérifier si l'email existe déjà
                if User.objects.filter(email=email).exists():
                    messages.error(request, "❌ Cet email est déjà utilisé.")
                else:
                    # Créer l'utilisateur
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password,
                        first_name=prenom,
                        last_name=nom
                    )
                    
                    # Créer le profil
                    Profil.objects.create(
                        user=user,
                        role=role,
                        telephone=telephone
                    )
                    
                    messages.success(request, f"✅ {role} ajouté avec succès : {prenom} {nom}")
                    
            except Exception as e:
                messages.error(request, f"❌ Erreur : {str(e)}")
            
            return redirect('manager')
        
        # --- SUPPRIMER UN UTILISATEUR ---
        elif action == 'supprimer_utilisateur':
            user_id = request.POST.get('user_id')
            try:
                user = User.objects.get(id=user_id)
                
                # Empêcher la suppression de soi-même
                if user.id == request.user.id:
                    messages.error(request, "❌ Vous ne pouvez pas supprimer votre propre compte.")
                else:
                    nom_complet = f"{user.first_name} {user.last_name}"
                    role = user.profil.role if hasattr(user, 'profil') else 'utilisateur'
                    user.delete()
                    messages.success(request, f"✅ {role} supprimé : {nom_complet}")
                    
            except User.DoesNotExist:
                messages.error(request, "❌ Utilisateur introuvable.")
            
            return redirect('manager')
        
        # --- AFFECTER UN CLIENT À UN AGENT ---
        elif action == 'affecter_client':
            client_id = request.POST.get('client_id')
            agent_id = request.POST.get('agent_id')
            
            try:
                client = User.objects.get(id=client_id, profil__role='client')
                agent = User.objects.get(id=agent_id, profil__role='agent')
                
                # Affecter toutes les propriétés du client à l'agent
                nb_proprietes = Propriete.objects.filter(bailleur=client).update(agent=agent)
                
                messages.success(
                    request, 
                    f"✅ Client {client.first_name} {client.last_name} affecté à {agent.first_name}. "
                    f"{nb_proprietes} propriété(s) transférée(s)."
                )
                
            except User.DoesNotExist:
                messages.error(request, "❌ Client ou agent introuvable.")
            except Exception as e:
                messages.error(request, f"❌ Erreur d'affectation : {str(e)}")
            
            return redirect('manager')
        
        # --- RÉAFFECTER UN CLIENT ---
        elif action == 'reaffecter_client':
            client_id = request.POST.get('client_id')
            nouvel_agent_id = request.POST.get('nouvel_agent_id')
            
            try:
                client = User.objects.get(id=client_id, profil__role='client')
                nouvel_agent = User.objects.get(id=nouvel_agent_id, profil__role='agent')
                
                # Ancien agent (pour le message)
                ancien_agent = Propriete.objects.filter(bailleur=client).exclude(agent__isnull=True).first()
                nom_ancien = f"{ancien_agent.agent.first_name}" if ancien_agent and ancien_agent.agent else "non assigné"
                
                # Réaffecter toutes les propriétés
                nb_proprietes = Propriete.objects.filter(bailleur=client).update(agent=nouvel_agent)
                
                messages.success(
                    request,
                    f"✅ Client {client.first_name} réaffecté de {nom_ancien} vers {nouvel_agent.first_name}. "
                    f"{nb_proprietes} propriété(s) transférée(s)."
                )
                
            except Exception as e:
                messages.error(request, f"❌ Erreur de réaffectation : {str(e)}")
            
            return redirect('manager')
        
        # --- MODIFIER UN UTILISATEUR ---
        elif action == 'modifier_utilisateur':
            user_id = request.POST.get('user_id')
            try:
                user = User.objects.get(id=user_id)
                
                # Modifier les informations
                user.first_name = request.POST.get('prenom', user.first_name)
                user.last_name = request.POST.get('nom', user.last_name)
                user.email = request.POST.get('email', user.email)
                user.save()
                
                # Modifier le profil
                if hasattr(user, 'profil'):
                    user.profil.telephone = request.POST.get('telephone', user.profil.telephone)
                    user.profil.save()
                
                messages.success(request, f"✅ Utilisateur {user.first_name} {user.last_name} modifié avec succès.")
                
            except User.DoesNotExist:
                messages.error(request, "❌ Utilisateur introuvable.")
            except Exception as e:
                messages.error(request, f"❌ Erreur : {str(e)}")
            
            return redirect('manager')
        
        # --- CHANGER LE MOT DE PASSE ---
        elif action == 'changer_mot_de_passe':
            user_id = request.POST.get('user_id')
            nouveau_password = request.POST.get('nouveau_password')
            
            try:
                user = User.objects.get(id=user_id)
                user.set_password(nouveau_password)
                user.save()
                
                messages.success(request, f"✅ Mot de passe changé pour {user.first_name} {user.last_name}.")
                
            except Exception as e:
                messages.error(request, f"❌ Erreur : {str(e)}")
            
            return redirect('manager')
    
    # ============================================
    # 9. GESTION DES FILTRES GET
    # ============================================
    
    # Filtre par type d'utilisateur
    filtre_type = request.GET.get('type', 'tous')
    if filtre_type == 'clients':
        utilisateurs_liste = User.objects.filter(profil__role='client').order_by('-date_joined')
    elif filtre_type == 'agents':
        utilisateurs_liste = User.objects.filter(profil__role='agent').order_by('-date_joined')
    elif filtre_type == 'bailleurs':
        utilisateurs_liste = User.objects.filter(profil__role='bailleur').order_by('-date_joined')
    elif filtre_type == 'managers':
        utilisateurs_liste = User.objects.filter(profil__role='manager').order_by('-date_joined')
    else:
        utilisateurs_liste = User.objects.all().order_by('-date_joined')
    
    # Recherche
    recherche = request.GET.get('recherche', '')
    if recherche:
        utilisateurs_liste = utilisateurs_liste.filter(
            Q(username__icontains=recherche) |
            Q(first_name__icontains=recherche) |
            Q(last_name__icontains=recherche) |
            Q(email__icontains=recherche)
        )
    
    # Pagination
    page = int(request.GET.get('page', 1))
    elements_par_page = 20
    debut = (page - 1) * elements_par_page
    fin = debut + elements_par_page
    utilisateurs_pagines = utilisateurs_liste[debut:fin]
    
    # ============================================
    # 10. PRÉPARATION DU CONTEXTE
    # ============================================
    
    context = {
        # === STATISTIQUES GÉNÉRALES ===
        'total_clients': total_clients,
        'total_agents': total_agents,
        'total_bailleurs': total_bailleurs,
        'total_managers': total_managers,
        'total_utilisateurs': total_utilisateurs,
        'total_proprietes': total_proprietes,
        'total_rdv': total_rdv,
        'total_favoris': total_favoris,
        
        # === STATISTIQUES FINANCIÈRES ===
        'valeur_totale': valeur_totale,
        'prix_moyen': round(prix_moyen, 0),
        'proprietes_vente': proprietes_vente,
        'proprietes_location': proprietes_location,
        
        # === STATISTIQUES RENDEZ-VOUS ===
        'rdv_en_attente': rdv_en_attente,
        'rdv_confirme': rdv_confirme,
        'rdv_annule': rdv_annule,
        'rdv_aujourdhui': rdv_aujourdhui,
        'rdv_cette_semaine': rdv_cette_semaine,
        'rdv_ce_mois': rdv_ce_mois,
        
        # === STATISTIQUES D'INSCRIPTION ===
        'inscriptions_aujourdhui': inscriptions_aujourdhui,
        'inscriptions_cette_semaine': inscriptions_cette_semaine,
        'inscriptions_ce_mois': inscriptions_ce_mois,
        'inscriptions_cette_annee': inscriptions_cette_annee,
        
        # === PERFORMANCES ===
        'agents_performance': agents_performance,
        'top_agent': agents_performance[0] if agents_performance else None,
        
        # === CLIENTS SANS AGENT ===
        'clients_sans_agent': clients_sans_agent,
        'total_clients_sans_agent': total_clients_sans_agent,
        
        # === ACTIVITÉS RÉCENTES ===
        'dernieres_inscriptions': dernieres_inscriptions,
        'derniers_rdv': derniers_rdv,
        'dernieres_proprietes': dernieres_proprietes,
        'derniers_favoris': derniers_favoris,
        
        # === STATISTIQUES PAR CATÉGORIE ===
        'stats_categories': stats_categories,
        'top_villes': top_villes,
        
        # === LISTES POUR FORMULAIRES ===
        'liste_agents': User.objects.filter(profil__role='agent').order_by('first_name'),
        'liste_clients': User.objects.filter(profil__role='client').order_by('first_name')[:50],
        'liste_bailleurs': User.objects.filter(profil__role='bailleur').order_by('first_name')[:50],
        'liste_managers': User.objects.filter(profil__role='manager').order_by('first_name'),
        
        # === RÉSULTATS DE RECHERCHE ===
        'utilisateurs': utilisateurs_pagines,
        'total_utilisateurs_filtres': utilisateurs_liste.count(),
        'filtre_type': filtre_type,
        'recherche': recherche,
        'page_actuelle': page,
        'pages_total': (utilisateurs_liste.count() + elements_par_page - 1) // elements_par_page,
        
        # === INFORMATIONS TEMPORELLES ===
        'date_aujourd_hui': aujourd_hui,
        'mois_courant': aujourd_hui.strftime('%B %Y'),
        'annee_courante': aujourd_hui.year,
        
        # === TITRE DE LA PAGE ===
        'page_title': 'Tableau de bord Manager',
    }
    
    return render(request, 'SE/dashboard_manager.html', context)