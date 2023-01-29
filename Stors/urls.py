from django.urls import path
from Stors.views import Administrations, Product_detail, ProductCreate, ProductDeleteView, ProductUpdateView, about, add_to_cart, category_product, commande_cart, contact, delete_cart, panier_info, panier_vide, recus_pdf, view_cart, index, getdata


urlpatterns = [
    path('', index, name='home'),
    #path('genericviews/', indexhome.as_view(), name='homev'),
    path('product/<int:pk>/', Product_detail, name='detail'),
    path('product/<int:pk>/add-to-cart/', add_to_cart, name='AjoutPanier'),
    # path('product/add-to-cart/<int:pk>/', add_to_cart2, name='AjoutPanier2'),
    path('cart/', view_cart, name='VoirePanier'),
    path('category/<int:pk>', category_product, name='category'),
    path('cart/delete/', delete_cart, name='delete'),
    path('panier/info/', panier_info, name='panierinfo'),
    path('panier/vide/', panier_vide, name='paniervide'),
    path('commande/', commande_cart, name='commande'),
    path('recus/', recus_pdf, name='recus'),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
    path('getdata/', getdata, name='getdata'),
    
    ##-----------Creations des liens Administrateur----------------##
    path('administrateur/', Administrations, name='administrateur'),
    path('administrateur/product/<int:pk>/', Product_detail, name='Adetail'),
    #path('administrateur/creer/', ProductCreateView.as_view(), name='creer'),
    path('administrateur/creer/', ProductCreate, name='creer'),
    path('administrateur/edit/<int:pk>/', ProductUpdateView.as_view(), name='editer'),
    path('administrateur/delete/<int:pk>/', ProductDeleteView.as_view(), name='supprimer'),
]