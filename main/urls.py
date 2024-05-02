from django.urls import path
from .views import home, topic

urlpatterns = [
    path('', home, name='home'),
    path('<str:topic_id>/', topic, name='topic'),
]