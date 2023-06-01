from django.urls import path
from .views import (
    TextBlockDetailsView,
    TextsForUser,
    TextBlockListView,
    CreateTextBlockView
)

app_name = 'texts'

urlpatterns = [
    path('', TextBlockListView.as_view(), name='text_block_list'),
    path('create/', CreateTextBlockView.as_view(), name='create_text_block'),
    path('user-<str:username>/', TextsForUser.as_view(), name='text_blocks_for_user'),
    path('<str:hash>/', TextBlockDetailsView.as_view(), name='text_block_detail'),
]
