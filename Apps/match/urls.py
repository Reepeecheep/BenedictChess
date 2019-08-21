from django.urls import path
from Apps.match.views import MatchList, MatchCreate, view, calculate_attack, insert_move

urlpatterns = [
	path('', MatchList.as_view(), name='index'),
	path('add/', MatchCreate.as_view(), name='add'),
    path('view/<int:id>/', view, name='view'),
    path('calculate_attack/', calculate_attack, name='calculate_attack'),
    path('insert_move/', insert_move, name='insert_move'),
]