# urls.py
from django.urls import path
from django.views.generic import RedirectView
from .views import home, topic, topic_detail, source_code

urlpatterns = [
    path('favicon.ico/', RedirectView.as_view(url='/static/favicon.ico', permanent=True)),
    path('', home, name='home'),
    path('<str:topic>/', topic, name='topic'),  # Ajustar o nome do argumento para topic_name
    path('<str:topic>/<str:topic_name>/', topic_detail, name='topic_detail'),
    path('<str:topic>/<str:topic_name>/<str:problem_id>/source-code/', source_code, name='source_code'),
]
