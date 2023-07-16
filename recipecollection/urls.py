
from django.contrib import admin
from django.urls import path
from mainApp import views
from django.conf.urls.static import static 
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),


    path('',views.homepage),
    path('add/',views.addPage),
    path('view/',views.viewPage),
    path('register/',views.registerPage),
    path('delete/<id>/', views.delete_recipe),
    path('update/<id>/', views.update_recipe),
    path('login/',views.loginPage),
    path('logout/',views.logoutPage),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


