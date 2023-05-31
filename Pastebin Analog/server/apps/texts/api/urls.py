from django.urls import path
from .views import (
    TextBlockDetailsView,
    TextBlockListView,
)

app_name = 'texts'


urlpatterns = [
    path('', TextBlockListView.as_view(), name='text-block-list'),
    path('<str:hash>/', TextBlockDetailsView.as_view(), name='text-block-detail'),
]