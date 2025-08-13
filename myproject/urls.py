from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.i18n import set_language
from django.conf.urls.i18n import i18n_patterns
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

# Не оборачивается в i18n
urlpatterns = [
    path('set_language/', set_language, name='set_language'),  # переключение языка без /ru/
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Всё остальное — с языковым префиксом
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),

    # Основные страницы
    path('', views.index, name='index'),
    path('join_association/', views.join_association, name='join_association'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('success/', views.success, name='success'),
    path('members/', views.members_list, name='members_list'),

    # Подключаемые приложения
    path('news/', include('news.urls')),
    path('users/', include('users.urls')),
    path('', include('myapp.urls')),
)
