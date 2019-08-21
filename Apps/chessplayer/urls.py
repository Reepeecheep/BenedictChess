from django.urls import path
from Apps.chessplayer.views import ChessPlayerList, ChessPlayerCreate, ChessPlayerUpdate, ChessPlayerDelete

urlpatterns = [
    path('', ChessPlayerList.as_view(), name='index'),
    path('add/', ChessPlayerCreate.as_view(), name='add'),
    path('edit/<int:pk>/', ChessPlayerUpdate.as_view(), name='edit'),
    path('delete/<int:pk>/', ChessPlayerDelete.as_view(), name='delete'),
    #path('edit/<int:id>', edit, name='edit'),
    #path('delete/<int:id>', delete, name='delete'),
]