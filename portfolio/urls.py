from django.urls import path
from . import views  # Ensure all views are imported
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # ✅ User Authentication & Dashboard
    path('', views.user_login, name='login'),  
    path("home/", views.home, name="home"),  
    path('register/', views.register, name='register'),  
    path('dashboard/', views.dashboard, name='dashboard'),  
    path('view-portfolio/', views.view_portfolio, name='view_portfolio'),
    path('logout/', views.user_logout, name='logout'),

    # ✅ Company & Feedback URLs
    path("companies/", views.company_list, name="company_list"),  
    path("company-form/", views.company_form, name="company_form"),  
    path("feedback/", views.feedback_view, name="feedback"),

    # ✅ Admin Dashboard URLs
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/user/<int:user_id>/', views.admin_view_user, name='admin_view_user'),

    # ✅ About Us Page
    path("about-us/", views.about_us, name="about_us"),
]

# ✅ Serve Media Files in Development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
