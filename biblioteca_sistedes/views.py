# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from django.core.exceptions import ValidationError
from .models import Conference, Edition, Author, Track, Article, Sequence
from .forms import ConferenceForm, EditionForm, AuthorForm, TrackForm, ArticleForm
from django.core.files.storage import FileSystemStorage


def Conferences(request):
	return render(request, 'biblioteca_sistedes/conferences.html', global_context())

def GetConferences(request, name=None):
	conference = Conference.objects.filter(domain=name)[:1]
	editions = Edition.objects.filter(conference_id = conference)
	context = {'conference': conference, 'new_editions': editions}
	context.update(global_context())
	return render(request, 'biblioteca_sistedes/get_conference.html', context)

def GetEditions(request, name=None, year=None):
	conference = Conference.objects.filter(domain=name)[:1]
	edition = Edition.objects.filter(year = year, conference_id = conference)[:1]
	tracks = Track.objects.filter(edition_id = edition)
	context = {'edition': edition, 'new_tracks': tracks}
	context.update(global_context())
	return render(request, 'biblioteca_sistedes/get_edition.html', context)

def GetTracks(request, name=None, year=None, id=None):
	conference = Conference.objects.filter(domain=name)[:1]
	edition = Edition.objects.filter(year = year, conference_id = conference)[:1]
	track = Track.objects.filter(edition_id = edition, id = id)[0]
	articles = Article.objects.filter(track_ids = track.id)
	context = {'track': track, 'articles': articles}
	context.update(global_context())
	return render(request, 'biblioteca_sistedes/get_track.html', context)

def global_context():
	context = {
		"conferences": Conference.objects.all(),
		"editions": Edition.objects.all(),
		"tracks": Track.objects.all(),
	}
	return context

def search_article(stype, key= False,
				   txtTitulo = False,
				   selCondAutor = False,
				   txtAutor= False,
				   selCondAfiliacion= False,
				   txtAfiliacion= False,
				   selCondKeyword= False,
				   txtKeyword= False):
	articles = Article.objects.all()
	conference_list = []
	list_by_title= []
	list_by_author = []
	if stype == 'b':
		for a in articles:
			found = False
			article_name = a.name
			article_description = a.description
			for n in article_name.split():
				for k in key.split():
					if k.lower() in n.lower():
						conference_list.append(a)
						found = True
						break
			if not found:
				for d in article_description.split():
					for k in key.split():
						if k.lower() in d.lower():
							conference_list.append(a)
							break
	elif stype == 'a':
		for a in articles:
			article_name = a.name
			articles_autor = a.author_ids.all()
			article_keyword = a.keyword_ids.all()
			if txtTitulo:
				for n in article_name.split():
					if txtTitulo.lower() in n.lower():
						list_by_title.append(a)
			if txtAutor:
				for autor in articles_autor:
					for n in autor.name.split():
						if txtAutor.lower() in n.lower():
							list_by_author.append(a)
			if selCondAutor == 'o':
				conference_list = list_by_title + list_by_author
			else:
				conference_list = set(list_by_title).intersection(list_by_author) if txtAutor else list_by_title + list_by_author

	return list(set(conference_list))
			# if txtAutor:
			# 	if selCondAutor == 'o':
			# 		for autor in articles_autor:
			# 			for n in autor.name.split():
			# 				if txtAutor in n.lower():
			# 					conference_list.append(a)
			# if txtAutor:
			# 	if selCondAutor == 'o':
			# 		for autor in articles_autor:
			# 			for n in autor.name.split():
			# 				if txtAutor in n.lower():
			# 					conference_list.append(a)

def index(request):
	key = request.GET.get('s') or False
	if key is not False:
		conference_list = search_article('b', key)
		context = {'conference_list': conference_list, 'key': key}
		context.update(global_context())
		return render(request, 'biblioteca_sistedes/search_engine.html', context)

	else:
		return render(request, 'biblioteca_sistedes/base.html', global_context())

def search(request):
	params_exist = True if request.GET.get('selCondAutor') else False
	txtTitulo = request.GET.get('txtTitulo') or ''
	selCondAutor = request.GET.get('selCondAutor') or False
	txtAutor = request.GET.get('txtAutor') or ''
	selCondAfiliacion = request.GET.get('selCondAfiliacion') or False
	txtAfiliacion = request.GET.get('txtAfiliacion') or ''
	selCondKeyword = request.GET.get('selCondKeyword') or False
	txtKeyword = request.GET.get('txtKeyword') or ''
	context = {
		'txtTitulo': txtTitulo,
		'selCondAutor': selCondAutor,
		'txtAutor': txtAutor,
		'selCondAfiliacion': selCondAfiliacion,
		'txtAfiliacion': txtAfiliacion,
		'selCondKeyword': selCondKeyword,
		'txtKeyword': txtKeyword,
		'params_exist': params_exist
	}
	if params_exist:
		conference_list = search_article('a', '', txtTitulo, selCondAutor, txtAutor, selCondAfiliacion, txtAfiliacion, selCondKeyword, txtKeyword)
		context.update({'conference_list': conference_list})
	context.update(global_context())
	return render(request, 'biblioteca_sistedes/advanced_search_engine.html', context)

def ConferenceDelete(request, pk=None):
	conference = get_object_or_404(Conference, pk=pk)
	if conference:
		conference.delete()
		return HttpResponseRedirect('/biblioteca/conference_list/')

def EditionDelete(request, pk=None):
	edition = get_object_or_404(Edition, pk=pk)
	if edition:
		edition.delete()
		return HttpResponseRedirect('/biblioteca/edition_list/')

def TrackDelete(request, pk=None):
	track = get_object_or_404(Track, pk=pk)
	if track:
		track.delete()
		return HttpResponseRedirect('/biblioteca/track_list/')

def AuthorDelete(request, pk=None):
	author = get_object_or_404(Author, pk=pk)
	if author:
		author.delete()
		return HttpResponseRedirect('/biblioteca/author_list/')

def ArticleDelete(request, pk=None):
	article = get_object_or_404(Article, pk=pk)
	if article:
		article.delete()
		return HttpResponseRedirect('/biblioteca/article_list/')


class ConferenceList(ListView):
	model = Conference
	template_name = 'biblioteca_sistedes/conference_list.html'

	def get_context_data(self, **kwargs):
		context = super(ConferenceList, self).get_context_data(**kwargs)
		context.update(global_context())
		return context

class ConferenceCreate(CreateView):
	model = Conference
	template_name = 'biblioteca_sistedes/conference_create.html'
	form_class = ConferenceForm
	success_url = reverse_lazy('biblioteca_sistedes:conference_list')

	def get_context_data(self, **kwargs):
		context = super(ConferenceCreate, self).get_context_data(**kwargs)
		if 'form_conference' not in context:
			context['form_conference'] = self.form_class(self.request.GET)
		context.update(global_context())
		return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST)
		if form.is_valid():
			conference = form.save()
			return HttpResponseRedirect('/biblioteca/conference_list/')
		else:
			return self.render_to_response(self.get_context_data(form=form))


class ConferenceUpdate(UpdateView):
	model = Conference
	template_name = 'biblioteca_sistedes/conference_create.html'
	form_class = ConferenceForm
	success_url = reverse_lazy('biblioteca_sistedes:conference_list')

	def get_context_data(self, **kwargs):
		context = super(ConferenceUpdate, self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk', 0)
		conference = self.model.objects.get(id=pk)
		if 'form_conference' not in context:
			context['form_conference'] = self.form_class(instance=conference)
		context['id'] = pk
		context.update(global_context())
		return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		id_conference= kwargs['pk']
		conference = self.model.objects.get(id = id_conference)
		form = self.form_class(request.POST, instance=conference)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/biblioteca/conference_list/')
		else:
			return self.render_to_response(self.get_context_data(form=form))

class EditionList(ListView):
	model = Edition
	template_name = 'biblioteca_sistedes/edition_list.html'

	def get_context_data(self, **kwargs):
		context = super(EditionList, self).get_context_data(**kwargs)
		context.update(global_context())
		return context

class EditionCreate(CreateView):
	model = Edition
	template_name = 'biblioteca_sistedes/edition_create.html'
	form_class = EditionForm
	success_url = reverse_lazy('biblioteca_sistedes:edittion_list')

	def get_context_data(self, **kwargs):
		context = super(EditionCreate, self).get_context_data(**kwargs)
		if 'form_edition' not in context:
			context['form_edition'] = self.form_class(self.request.GET)
		context.update(global_context())
		return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST or None)
		if form.is_valid():
			edition = form.save()
			return HttpResponseRedirect('/biblioteca/edition_list/')
		else:
			return self.render_to_response(self.get_context_data(form=form))

class EditionUpdate(UpdateView):
	model = Edition
	template_name = 'biblioteca_sistedes/edition_create.html'
	form_class = EditionForm
	success_url = reverse_lazy('biblioteca_sistedes:edition_list')

	def get_context_data(self, **kwargs):
		context = super(EditionUpdate, self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk', 0)
		edition = self.model.objects.get(id=pk)
		if 'form_edition' not in context:
			context['form_edition'] = self.form_class(instance=edition)
		context['id'] = pk
		context.update(global_context())
		return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		id_edition= kwargs['pk']
		edition = self.model.objects.get(id = id_edition)
		form = self.form_class(request.POST, instance=edition)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/biblioteca/edition_list/')
		else:
			return self.render_to_response(self.get_context_data(form=form))

class AuthorList(ListView):
	model = Author
	template_name = 'biblioteca_sistedes/author_list.html'

	def get_context_data(self, **kwargs):
		context = super(AuthorList, self).get_context_data(**kwargs)
		context.update(global_context())
		return context

class AuthorCreate(CreateView):
	model = Author
	template_name = 'biblioteca_sistedes/author_create.html'
	form_class = AuthorForm
	success_url = reverse_lazy('biblioteca_sistedes:author_list')

	def get_context_data(self, **kwargs):
		context = super(AuthorCreate, self).get_context_data(**kwargs)
		if 'form_author' not in context:
			context['form_author'] = self.form_class(self.request.GET)
		context.update(global_context())
		return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST or None)
		if form.is_valid():
			author = form.save()
			return HttpResponseRedirect('/biblioteca/author_list/')
		else:
			return self.render_to_response(self.get_context_data(form=form))

class AuthorUpdate(UpdateView):
	model = Author
	template_name = 'biblioteca_sistedes/author_create.html'
	form_class = AuthorForm
	success_url = reverse_lazy('biblioteca_sistedes:author_list')

	def get_context_data(self, **kwargs):
		context = super(AuthorUpdate, self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk', 0)
		author = self.model.objects.get(id=pk)
		if 'form_author' not in context:
			context['form_author'] = self.form_class(instance=author)
		context['id'] = pk
		context.update(global_context())
		return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		id_author= kwargs['pk']
		author = self.model.objects.get(id = id_author)
		form = self.form_class(request.POST, instance=author)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/biblioteca/author_list/')
		else:
			return self.render_to_response(self.get_context_data(form=form))

class TrackList(ListView):
	model = Track
	template_name = 'biblioteca_sistedes/track_list.html'

	def get_context_data(self, **kwargs):
		context = super(TrackList, self).get_context_data(**kwargs)
		context.update(global_context())
		return context

class TrackCreate(CreateView):
	model = Track
	template_name = 'biblioteca_sistedes/track_create.html'
	form_class = TrackForm
	success_url = reverse_lazy('biblioteca_sistedes:track_list')

	def get_context_data(self, **kwargs):
		context = super(TrackCreate, self).get_context_data(**kwargs)
		if 'form_track' not in context:
			context['form_track'] = self.form_class(self.request.GET)
		context.update(global_context())
		return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST or None)
		if form.is_valid():
			track = form.save()
			return HttpResponseRedirect('/biblioteca/track_list/')
		else:
			return self.render_to_response(self.get_context_data(form=form))

class TrackUpdate(UpdateView):
	model = Track
	template_name = 'biblioteca_sistedes/track_create.html'
	form_class = TrackForm
	success_url = reverse_lazy('biblioteca_sistedes:track_list')

	def get_context_data(self, **kwargs):
		context = super(TrackUpdate, self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk', 0)
		track = self.model.objects.get(id=pk)
		if 'form_track' not in context:
			context['form_track'] = self.form_class(instance=track)
		context['id'] = pk
		context.update(global_context())
		return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		id_track= kwargs['pk']
		track = self.model.objects.get(id = id_track)
		form = self.form_class(request.POST, instance=track)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/biblioteca/track_list/')
		else:
			return self.render_to_response(self.get_context_data(form=form))

class ArticleList(ListView):
	model = Article
	template_name = 'biblioteca_sistedes/article_list.html'

	def get_context_data(self, **kwargs):
		context = super(ArticleList, self).get_context_data(**kwargs)
		context.update(global_context())
		return context

class ArticleCreate(CreateView):
	model = Article
	template_name = 'biblioteca_sistedes/article_create.html'
	form_class = ArticleForm
	success_url = reverse_lazy('biblioteca_sistedes:article_list')

	def get_context_data(self, **kwargs):
		context = super(ArticleCreate, self).get_context_data(**kwargs)
		if 'form_article' not in context:
			context['form_article'] = self.form_class(self.request.GET)
		context.update(global_context())
		return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST or None, request.FILES or None)
		myfile = request.FILES['article_file']
		fs = FileSystemStorage()
		sufix_number = Sequence.get_last_number()
		next_number = int(sufix_number) + 1
		file_name = 'file_' + str(next_number)
		Sequence(number = next_number).save()
		filename = fs.save(file_name, myfile)
		uploaded_file_url = fs.url(filename)
		if form.is_valid():
			article = form.save()
			article.url_file = uploaded_file_url
			article.save()
			return HttpResponseRedirect('/biblioteca/article_list/')
		else:
			return self.render_to_response(self.get_context_data(form=form))


class ArticleUpdate(UpdateView):
	model = Article
	template_name = 'biblioteca_sistedes/article_create.html'
	form_class = ArticleForm
	success_url = reverse_lazy('biblioteca_sistedes:article_list')

	def get_context_data(self, **kwargs):
		context = super(ArticleUpdate, self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk', 0)
		article = self.model.objects.get(id=pk)
		if 'form_article' not in context:
			context['form_article'] = self.form_class(instance=article)
		context['id'] = pk
		context.update(global_context())
		return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		id_article= kwargs['pk']
		article = self.model.objects.get(id = id_article)
		form = self.form_class(request.POST, instance=article)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/biblioteca/article_list/')
		else:
			return self.render_to_response(self.get_context_data(form=form))
