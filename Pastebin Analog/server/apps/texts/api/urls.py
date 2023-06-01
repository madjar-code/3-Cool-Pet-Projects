from django.urls import path
from .views import (
    TextBlockDetailsView,
    TextsForUser,
    TextBlockListView,
    UpdateTextBlockView,
    CreateTextBlockView
)

app_name = 'texts'

urlpatterns = [
    path('', TextBlockListView.as_view(), name='text_block_list'),
    path('create/', CreateTextBlockView.as_view(), name='create_text_block'),
    path('user-<str:username>/', TextsForUser.as_view(), name='text_blocks_for_user'),
    path('update/<str:hash>/', UpdateTextBlockView.as_view(), name='update_text_block'),
    path('<str:hash>/', TextBlockDetailsView.as_view(), name='text_block_detail'),
]
