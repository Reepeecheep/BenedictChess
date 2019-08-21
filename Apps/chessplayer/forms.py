from django import forms
from Apps.chessplayer.models import ChessPlayer

class ChessPlayerForm(forms.ModelForm):

	class Meta:
		model = ChessPlayer

		fields = [
			'username',
			'email'
		]

		labels = {
			'username': 'Username',
			'email': 'Email'
		}

		widgets = {
			'username': forms.TextInput(attrs={'class': 'input-field'}),
			'email': forms.TextInput(attrs={'class': 'input-field', 'type':'email'})
		}
	'''
	def clean_email(self, *args, **kwargs):
		email = self.cleaned_data.get("email")
		if ("@lichess.com" in email):
			print ("YEAH\n"*10)
			return email
		else:
			raise forms.ValidationError("Hola")
	'''


