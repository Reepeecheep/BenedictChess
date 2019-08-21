from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from Apps.match.ChessValidator import Move_Validator
from django.views.generic import ListView, CreateView
from Apps.match.models import Match, Match_Move, Match_Castling_Options
from django.urls import reverse_lazy
from Apps.match.forms import MatchForm
'''
from django.core import serializers
import json
'''

# Create your views here.
'''
def index(request):
    #return HttpResponse("Hello, world. You're at the match index.")
    return render(request, 'match/index.html')
'''

class MatchList(ListView):
	model = Match
	template_name = 'match/index.html'

class MatchCreate(CreateView):
	model = Match
	form_class = MatchForm
	template_name = 'match/form.html'
	success_url = reverse_lazy('match:index')

def view(request, id):
    #return HttpResponse("Hello, world. You're at the match index.")
    match = Match.objects.get(id = id)
    moves = Match_Move.objects.filter(match_id = id).order_by('-id')
    turn = 'white' if len(moves)%2 == 0 else 'black'
    context = {'match': match, 'moves':moves, 'turn':turn}
    return render(request, 'match/view.html', context)

@csrf_exempt
def calculate_attack(request):
	data = {}
	if request.method == 'POST':
		source = request.POST.get('source')
		target = request.POST.get('target')
		piece = request.POST.get('piece')
		board_fen = request.POST.get('board_fen')
		board_pos = request.POST.get('board_pos')
		promote = request.POST.get('promote')
		match_id = request.POST.get('match_id')
		
		if (int(promote) == 0):
			promote = False
		else:
			promote = True
		
		move = Move_Validator(source, target, piece, board_fen)

		data = {
			'valid': move.validate(promote, match_id), 'move': repr(move), 'piece': piece, 'source': source, 'target': target, 'match': match_id
			#'board': move.board, 'board_fen':move.board_fen
		}
	return JsonResponse(data)

@csrf_exempt
def insert_move(request):
	data = {}
	if request.method == 'POST':
		move = Match_Move()
		move.match_id = Match.objects.get(id = request.POST.get('match_id'))
		move.notation = request.POST.get('notation')
		move.fen = request.POST.get('fen')
		move.save()

		piece = request.POST.get('piece')
		source = request.POST.get('source')

		if (piece[1] in ['K', 'R']):
			insert_castling_option(move.match_id, piece, source)

		data['id'] = move.id
		data['notation'] = move.notation
		data['fen'] = move.fen
	return JsonResponse(data)

def insert_castling_option(match_id, piece, source):
	if (piece == 'wK'):
		castling = Match_Castling_Options.objects.update_or_create(
			match_id = match_id,
			defaults = {'white_sort':False, 'white_large':False}
		)
	elif (piece == 'bK'):
		castling = Match_Castling_Options.objects.update_or_create(
			match_id = match_id,
			defaults = {'black_sort':False, 'black_large':False}
		)
	elif (source == 'a1'):
		castling = Match_Castling_Options.objects.update_or_create(
			match_id = match_id,
			defaults = {'white_large':False}
		)
	elif (source == 'h1'):
		castling = Match_Castling_Options.objects.update_or_create(
			match_id = match_id,
			defaults = {'white_sort':False}
		)
	elif (source == 'a8'):
		castling = Match_Castling_Options.objects.update_or_create(
			match_id = match_id,
			defaults = {'black_large':False}
		)
	elif (source == 'h8'):
		castling = Match_Castling_Options.objects.update_or_create(
			match_id = match_id,
			defaults = {'black_sort':False}
		)