from django import forms
from Apps.match.models import Match

class MatchForm(forms.ModelForm):

	class Meta:
		model = Match

		boards = (
			('default_board_theme', 'default'),
			('wood_board_theme', 'wood'),
			('dark_wood_board_theme', 'dark wood'),
			('wikipedia_board_theme', 'wikipedia'),
			('classic_board_theme', 'classic'),
			('cristal_board_theme', 'cristal'),
			('white_board_theme', 'white'),
			('blue_board_theme', 'blue'),
			('royal_blue_board_theme', 'royal blue'),
			('green_board_theme', 'green'),
			('light_green_board_theme', 'light green'),
			('marble_board_theme', 'marble'),
			('red_board_theme', 'red'),
			('pink_board_theme', 'pink'),
		)

		pieces = (
			('alpha', 'alpha'),
			('california', 'california'),
			('cardinal','cardinal'),
			('chess7','chess7'),
			('chess24', 'chess24'),
			('chess.com', 'chess.com'),

			('dilena', 'dilena'),
			('leipzig', 'leipzig'),
			('letter','letter'),

			('metro', 'metro'),
			('merida','merida'),
			('symbol', 'symbol'),
			('uscf', 'uscf'),
			('wikipedia', 'wikipedia'),

			('shapes','shapes'),
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

