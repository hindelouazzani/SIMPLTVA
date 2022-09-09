from django.urls import path

from . import views

urlpatterns = [
    #ex: /MyApp/
    path('', views.home, name='home'),
    path('ecart_dd_df/',views.ecart_dd_df,name='ecart_dd_df'),
    path('activite_contribuable',views.activite_contribuable, name='activite_contribuable'),
    path('comparaison_credit',views.comparaison_credit,name = 'comparaison_credit')

]