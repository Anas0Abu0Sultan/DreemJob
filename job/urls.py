from django.urls import path
from job import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy


urlpatterns = [
    path('', views.index, name='index'),
    path('job/<int:job_id>/', views.job_details, name="job_details"),
    path("browse_more_job/",views.all_jobs,name="all_jobs"),
    path('home/category/<int:category_id>', views.all_jobs_category, name="all_jobs_category"),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('index')), name='logout'),
    path('offers/<int:job_id>', views.offers, name="offers"),
    path("signup/", views.signup, name="signup"),

    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("stttings/change_password/", auth_views.PasswordChangeView.as_view(template_name="registration/change_password.html"), name="change_password"),
    path("stttings/change_password/done/", auth_views.PasswordChangeDoneView.as_view(template_name="registration/password_change_done.html"), name="password_change_done"),
    path("profile/<str:name>", views.profile, name="profile"),


]
