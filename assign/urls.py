from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path("contact/", views.contact_view, name="contact"),
    path('website-designing/', views.website_designing, name='website_designing'),
    path('ecommerce-solutions/', views.ecommerce_solutions, name='ecommerce_solutions'),
    path('digital-marketing/', views.digital_marketing, name='digital_marketing'),
    path('ppc-campaigns/', views.ppc_campaigns, name='ppc_campaigns'),
    path('data-science/', views.data_science, name='data_science'),
    path('business-intelligence/', views.business_intelligence, name='business_intelligence'),

    path('training/subscription/application/', views.Application, name='application'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # assignment detail view
    path("assignments/", views.assignment_list, name="assignment_list"),
    path("assignments/day/<int:day>/", views.assignment_detail, name="assignment_detail"),

    path('Profile', views.PROFILE, name='profile'),
    path('Profile/update', views.PROFILE_UPDATE, name='profile_update'),
    
    path("check-username/", views.check_username, name="check_username"),
    path("check-email/", views.check_email, name="check_email"),

]

