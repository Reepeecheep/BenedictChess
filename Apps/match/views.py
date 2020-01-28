from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from Apps.match.ChessValidator import Move_Validator
from django.views.generic import ListView, CreateView
from Apps.match.models import Match, Match_Move#, Match_Castling_Options
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
    turn =  ('white' if moves[0].turn == 'black' else 'black') if len(moves) > 0 else 'white'
    context = {'match': match, 'moves':moves, 'turn':turn, 'winner_id':match.winner_id}
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
		my_move = move.validate(promote, match_id)
		notation = repr(move)

		if my_move[3] != False:
			notation += '#'
			match = Match.objects.get(id = request.POST.get('match_id'))
			players = {'w':match.white_id, 'b':match.black_id}
			match.winner_id = players[my_move[3]]
			match.active = 0

			match.save()

		data = {
			'valid': my_move,
			'move': notation,
			'piece': piece,
			'source': source,
			'target': target,
			'match': match_id,
			'winner': my_move[3]
			#'board': move.board, 'board_fen':move.board_fen
		}
	return JsonResponse(data)

@csrf_exempt
def insert_move(request):
	data = {}
	if request.method == 'POST':

		piece = request.POST.get('piece')
		source = request.POST.get('source')
		castling = request.POST.get('castling')

		move = Match_Move()
		move.match_id = Match.objects.get(id = request.POST.get('match_id'))
		move.notation = request.POST.get('notation')
		move.fen = request.POST.get('fen')
		move.turn = request.POST.get('turn')

		if (piece[1] in ['K', 'R'] and castling != '-'):
			if (piece == 'wK' and ('K' in castling or 'Q' in castling)):
				castling = castling.replace('K', '')
				castling = castling.replace('Q', '')

			elif (piece == 'bK' and ('k' in castling or 'q' in castling)):
				castling = castling.replace('k', '')
				castling = castling.replace('q', '')

			elif (source == 'a1'):
				castling = castling.replace('Q', '')

			elif (source == 'h1'):
				castling = castling.replace('K', '')

			elif (source == 'a8'):
				castling = castling.replace('q', '')
			elif (source == 'h8'):
				castling = castling.replace('k', '')

			if castling == '':
				castling = '-'

		move.castling = castling

		move.save()

		data['id'] = move.id
		data['notation'] = move.notation
		data['fen'] = move.fen
		data['castling'] = move.castling
	return JsonResponse(data)