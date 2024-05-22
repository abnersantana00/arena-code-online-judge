from django.urls import path
from .views import home, topic, topic_detail

urlpatterns = [
    path('', home, name='home'),
    path('<str:topic_id>/', topic, name='topic'),
    path('<str:topic_name>/<str:title_name>/', topic_detail, name='topic_detail'),
]
