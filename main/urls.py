# urls.py
from django.urls import path
from .views import home, topic, topic_detail, source_code

urlpatterns = [
    path('', home, name='home'),
    path('<str:topic_name>/', topic, name='topic'),  # Ajustar o nome do argumento para topic_name
    path('<str:topic_name>/<str:title_name>/', topic_detail, name='topic_detail'),
    path('<str:topic_name>/<str:title_name>/source-code/', source_code, name='source_code'),
]
