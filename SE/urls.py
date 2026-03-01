from django.urls import path
from . import views
from django.views.generic.base import RedirectView
urlpatterns = [
    # DASHBOARD MANAGER (protégé)
    path('manager/', views.manager, name='dashboard_manager'),
    path('agent/', views.agent, name='agent'),
    path('dashboard_bailleur/', views.dashboard_bailleur, name='dashboard_bailleur'),
    path('client/', views.client, name='client'),
    path('accueil/', views.accueil, name='accueil'),
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('propierte/', views.propierte, name='propierte'),
    path('propos/', views.propos, name='propos'),
     # REDIRECTION - Ajoutez cette ligne
    path('login/', RedirectView.as_view(url='/connexion/', permanent=False), name='login_redirect'),
     

    
    
]
