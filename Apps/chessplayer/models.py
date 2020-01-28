from django.db import models

# Create your models here.

class ChessPlayer(models.Model):
	username = models.CharField(max_length=25,unique=True)
	email = models.EmailField(default='',unique=True)
	#email = models.EmailField(default='guess@chess.play.com')

	def __str__(self):
		return self.username