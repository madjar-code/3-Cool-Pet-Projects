from django.urls import path
from .views import (
    TextBlockDetailsView
)

app_name = 'texts'


urlpatterns = [
    path('<str:hash>/', TextBlockDetailsView.as_view()),
]