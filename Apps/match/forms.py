from django import forms
from Apps.match.models import Match

class MatchForm(forms.ModelForm):

	class Meta:
		model = Match

		boards = (
			('default', 'default'),
			('chess24_board_theme', 'chess24_board_theme'),
			('metro_board_theme', 'metro_board_theme'),
			('leipzig_board_theme', 'leipzig_board_theme'),
			('wikipedia_board_theme', 'wikipedia_board_theme'),
			('dilena_board_theme', 'dilena_board_theme'),
			('uscf_board_theme', 'uscf_board_theme'),
			('symbol_board_theme', 'symbol_board_theme'),
			('lichess_board_theme', 'lichess_board_theme'),
			('tournament_board_theme', 'tournament_board_theme'),
		)

		pieces = (
			('alpha', 'alpha'),
			('chess24', 'chess24'),
			('dilena', 'dilena'),
			('gothic', 'gothic'),
			('leipzig', 'leipzig'),
			('lichess', 'lichess'),
			('medieval', 'medieval'),
			('metro', 'metro'),
			('symbol', 'symbol'),
			('uscf', 'uscf'),
			('wikipedia', 'wikipedia'),
		)

		fields = [
			'white_id',
			'black_id',
			'board_theme',
			'piece_theme'
		]

		labels = {
			'white_id': 'White',
			'black_id': 'Black',
			'board_theme': 'Board Theme',
			'piece_theme': 'Piece Theme' 
		}

		widgets = {
			'white_id': forms.Select(attrs={'class': 'input-field player_select'}),
			'black_id': forms.Select(attrs={'class': 'input-field player_select'}),
			'board_theme': forms.Select(attrs={'class': 'input-field board_draw'}, choices=boards),
			'piece_theme': forms.Select(attrs={'class': 'input-field board_draw'}, choices=pieces)
		}

