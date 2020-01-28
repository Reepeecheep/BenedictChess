from django.db import models
from Apps.chessplayer.models import ChessPlayer

# Create your models here.

class Match(models.Model):
	white_id = models.ForeignKey(ChessPlayer, null=False, on_delete=models.CASCADE, related_name='%(class)s_white_id')	
	black_id = models.ForeignKey(ChessPlayer, null=False, on_delete=models.CASCADE, related_name='%(class)s_black_id')
	date_game = models.DateTimeField(null=False, auto_now_add=True)
	board_theme = models.TextField(null=False, default='default')
	piece_theme = models.TextField(null=False, default='wikipedia')
	active = models.PositiveSmallIntegerField(null=False, default=1)
	winner_id = models.ForeignKey(ChessPlayer, null=True, on_delete=models.CASCADE, related_name='%(class)s_winner_id')
	#def __str__(self):
	#	return ("{} {} {} {} {} {} {} {}".format(self.id, self.white_id, self.black_id, self.date_game, self.board_theme, self.piece_theme, self.active, self.winner_id))

class Match_Move(models.Model):
	TURN = (
		('white', 'WHITE'),
		('black', 'BLACK'),
	)
	match_id = models.ForeignKey(Match, null=False, on_delete=models.CASCADE, related_name='%(class)s_match_id')
	notation = models.TextField(null=False, default='')
	fen = models.TextField(null=False, default='')
	turn = models.TextField(null=False, choices=TURN, default='WHITE')
	castling = models.TextField(null=False, default='KQkq')

	def __str__(self):
		return ("Match:{} Notation:{} FEN:{} {} {}".format(self.match_id, self.notation, self.fen, self.turn, self.castling))
