from django.urls import path
from . import views
from django.views.generic.base import RedirectView
urlpatterns = [
    # DASHBOARD MANAGER (protégé)
    path('manager/', views.manager, name='dashboard_manager'),
    path('agent/', views.agent, name='agent'),
    path('bailleur/', views.bailleur, name='bailleur'),
    path('client/', views.client, name='dashboard_client'),
    path('accueil/', views.accueil, name='accueil'),
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('propierte/', views.propierte, name='propierte'),
    path('propos/', views.propos, name='propos'),
     # REDIRECTION - Ajoutez cette ligne
    path('login/', RedirectView.as_view(url='/connexion/', permanent=False), name='login_redirect'),
     

    
    
]
