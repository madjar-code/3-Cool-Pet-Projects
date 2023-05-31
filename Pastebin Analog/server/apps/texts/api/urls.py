from django.urls import path
from .views import (
    TextBlockDetailsView,
    TextsForUser,
    TextBlockListView,
)

app_name = 'texts'

urlpatterns = [
    path('', TextBlockListView.as_view(), name='text_block_list'),
    path('user-<str:username>/', TextsForUser.as_view(), name='text_blocks_for_user'),
    path('<str:hash>/', TextBlockDetailsView.as_view(), name='text_block_detail'),
]