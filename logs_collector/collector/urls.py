from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index',),
    path('test/<str:path>/', views.test_page, name='test_page'),
    path('archives/<ticket>/<archive>', views.download, name="download")
]
