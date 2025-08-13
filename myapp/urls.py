from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

def maintenance_view(request):
    return HttpResponse(
        "<h1 style='text-align:center;margin-top:20%;'>Сайт временно недоступен<br>Ведутся технические работы</h1>",
        content_type="text/html",
        status=503
    )

urlpatterns = [
 #   path('', maintenance_view),
 #   path('<path:unused>', maintenance_view),
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('join_association/', views.join_association, name='join_association'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('course/<int:pk>/', views.course_detail, name='course_detail'),
    path('course/', views.course, name='course'),
    path('specialists/', views.specialist_list, name='specialist_list'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
