from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from Apps.chessplayer.models import ChessPlayer
from django.urls import reverse_lazy
from Apps.chessplayer.forms import ChessPlayerForm

# Create your views here.
'''
def index(request):
    #return HttpResponse("<h2>Perfiles</h2>")
    chessplayers = ChessPlayer.objects.all()
    context = {'chessplayers': chessplayers}
    return render(request, 'chessplayer/index.html', context)

def add(request):
	if (request.method == 'POST'):
		form = ChessPlayerForm(request.POST)
		if (form.is_valid()):
			form.save()
			return redirect('index')
	else:
		form = ChessPlayerForm()
	context = {'form': form, 'title': 'Add'}
	return render(request, 'chessplayer/form.html', context)

def edit(request, id):
	chessplayer = ChessPlayer.objects.get(id=id)
	if (request.method == 'GET'):
		form = ChessPlayerForm(instance=chessplayer)
	else:
		form = ChessPlayerForm(request.POST, instance=chessplayer)
		if (form.is_valid()):
			form.save()
			return redirect('index')
	context = {'form': form, 'title': 'Edit'}
	return render(request, 'chessplayer/form.html', context)

def delete(request, id):
	chessplayer = ChessPlayer.objects.get(id=id)
	if (request.method == 'POST'):
		chessplayer.delete()
		return redirect('index')
	context = {'chessplayer': chessplayer}
	return render(request, 'chessplayer/delete.html', context)
'''

class ChessPlayerList(ListView):
	model = ChessPlayer
	template_name = 'chessplayer/index.html'

class ChessPlayerCreate(CreateView):
	model = ChessPlayer
	form_class = ChessPlayerForm
	template_name = 'chessplayer/form.html'
	success_url = reverse_lazy('chessplayer:index')

	def get_context_data(self, *args, **kwargs):
		context = super(ChessPlayerCreate, self).get_context_data()
		context['title'] = 'New'
		return context

class ChessPlayerUpdate(UpdateView):
	model = ChessPlayer
	form_class = ChessPlayerForm
	template_name = 'chessplayer/form.html'
	success_url = reverse_lazy('chessplayer:index')

	def get_context_data(self, *args, **kwargs):
		context = super(ChessPlayerUpdate, self).get_context_data()
		context['title'] = 'Edit'
		return context

class ChessPlayerDelete(DeleteView):
	model = ChessPlayer
	template_name = 'chessplayer/delete.html'
	success_url = reverse_lazy('chessplayer:index')