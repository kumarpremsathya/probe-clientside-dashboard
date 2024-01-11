from django.urls import path
# from .views import show
from probe_agile_data import views

urlpatterns = [
    
    # path('get_data_for_popup1/<str:table_name>/', views.get_data_for_popup1, name='get_data_for_popup1'),
    # path('newhome/', views.newhome, name='newhome')
    # path('todaynewfema_datefilter/', views.todaynewfema_datefilter, name='todaynewfema_datefilter'),
    path('rbinewhome/', views.rbinewhome, name='rbinewhome'),
    path('rbi_tab/', views.rbi_tab, name='rbi_tab'),
    path('rbinewhome123/', views.rbinewhome123, name='rbinewhome123'),
    path('rbiget_data_for_popup1/<str:source_name>/', views.rbiget_data_for_popup1, name='rbiget_data_for_popup1'),
    path('rbinewfema_datefilter/', views.rbinewfema_datefilter, name='rbinewfema_datefilter'),
    path('rbinewecb_datefilter/', views.rbinewecb_datefilter, name='rbinewecb_datefilter'),
    path('rbinewodi_datefilter/', views.rbinewodi_datefilter, name='rbinewodi_datefilter'),

]
