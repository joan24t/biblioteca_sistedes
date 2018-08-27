# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
# Create your views here.
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic import CreateView
from .models import Conference, Edition, Author
from .models import Track, Article, Sequence, Keyword, User, Bulletin
from .forms import ConferenceForm, EditionForm, AuthorForm
from .forms import TrackForm, ArticleForm, KeywordForm, UserForm, BulletinForm
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.conf import settings
import os
from django.http import HttpResponse
from django.http import Http404
from django.core.mail import send_mail


# PUBLIC PART

def index(request):
    # request.session['user'] = 'pepe'
    # request.session.set_expiry(30)
    key = request.GET.get('s') or False
    if key is not False:
        conference_list = search_article('b', key)
        context = {'conference_list': conference_list, 'key': key}
        context.update(global_context())
        return render(
            request,
            'biblioteca_sistedes/search_engine.html',
            context
            )
    else:
        return render(
            request,
            'biblioteca_sistedes/base.html',
            global_context()
            )


def Conferences(request):
    return render(
        request,
        'biblioteca_sistedes/conferences.html',
        global_context()
        )


def News(request):
    return render(
        request,
        'biblioteca_sistedes/news.html',
        global_context()
        )


def Aboutus(request):
    return render(
        request,
        'biblioteca_sistedes/about.html',
        global_context()
        )


def Contactus(request):
    return render(
        request,
        'biblioteca_sistedes/contactus.html',
        global_context()
        )


def download(request, pk=None):
    username = request.session.get('username')
    if username:
        type = request.GET.get('type')
        object = None
        file_path = ''
        if type == 'a':
            object = Article.objects.get(id=pk)
            file_path = os.path.join(settings.MEDIA_ROOT, object.url_file)
        elif type == 'b':
            object = Bulletin.objects.get(id=pk)
            file_path = os.path.join(settings.BULLETIN_ROOT, object.url_file)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/pdf")
                response['Content-Disposition'] = 'inline; filename=' + \
                    os.path.basename(file_path)
                return response
        raise Http404
    else:
        return HttpResponseRedirect('/')


def GetListObjects(username, rol, model):
    if username:
        if rol == 1:
            return model.objects.all()
        else:
            current_user = User.objects.filter(username=username)[0] or ''
            object_list = model.objects.filter(user_ids=current_user.id)
            return object_list
    else:
        return []


def GetLogin(request):
    return render(request, 'biblioteca_sistedes/login.html')


def CheckUser(username, password=False):
    users = User.objects.all()
    for user in users:
        if user.username == username and user.password == password:
            return True
            break
    else:
        return False


def check_rol(request):
    rol = request.session.get('rol')
    return JsonResponse({
        'rol': rol
        })


def check_data(request):
    object = request.GET.get('object', None)
    value = request.GET.get('value', None)
    taken = False
    if object == 'email':
        taken = User.objects.filter(email__iexact=value).exists()
    elif object == 'username':
        taken = User.objects.filter(username__iexact=value).exists()
    elif object == 'name-conference':
        taken = Conference.objects.filter(name__iexact=value).exists()
    elif object == 'domain-conference':
        taken = Conference.objects.filter(domain__iexact=value).exists()
    data = {
        'is_taken': taken
        }
    return JsonResponse(data)


def GetBulletin(request, year=False, pk=False):
    bulletin = Bulletin.objects.get(id=pk) or False
    context = {
        'bulletin': bulletin,
        'year': year,
        }
    context.update(global_context())
    return render(
        request,
        'biblioteca_sistedes/get_bulletin.html',
        context,
        )


def GetPressBulletins(request):
    return render(
        request,
        'biblioteca_sistedes/press_bulletins.html',
        global_context()
        )


def GetSistedesDocuments(request):
    return render(
        request,
        'biblioteca_sistedes/sistedes_documents.html',
        global_context()
        )


def GetSistedesDocumentation(request):
    return render(
        request,
        'biblioteca_sistedes/documentation.html',
        global_context()
        )


def GetSistedesInforms(request):
    return render(
        request,
        'biblioteca_sistedes/informs.html',
        global_context()
        )


def GetPressBulletinsByYear(request, year=False):
    bulletins_by_year = [
        b for b in Bulletin.objects.all() if b.date.year == year
        ]
    context = {
        'bulletins_by_year': bulletins_by_year,
        'year': year,
        }
    context.update(global_context())
    return render(
        request,
        'biblioteca_sistedes/press_bulletins_by_year.html',
        context,
        )


def GetConferences(request, name=None):
    conference = Conference.objects.filter(domain=name)[:1]
    editions = Edition.objects.filter(conference_id=conference)
    context = {'conference': conference, 'new_editions': editions}
    context.update(global_context())
    return render(request, 'biblioteca_sistedes/get_conference.html', context)


def GetArticle(request, pk=None):
    article = Article.objects.get(id=pk)
    context = {
        'article': article,
        }
    context.update(global_context())
    return render(request, 'biblioteca_sistedes/get_article.html', context)


def GetEditions(request, name=None, year=None, id=None):
    edition = Edition.objects.get(id=id)
    tracks = Track.objects.filter(edition_id=edition)
    context = {'edition': edition, 'new_tracks': tracks}
    context.update(global_context())
    if len(tracks) != 0:
        return render(request, 'biblioteca_sistedes/get_edition.html', context)
    else:
        articles = Article.objects.filter(edition_id=edition)
        context.update({'articles': articles})
        return render(
            request,
            'biblioteca_sistedes/get_article_from_edition.html',
            context
            )


def GetListOfTracks(request, name=None):
    tracks = Track.objects.all()
    track_name = name.split()
    final_list = []
    for tr in tracks:
        array_description = tr.description.split()
        array_title = tr.name.split()
        for tn in track_name:
            for ad in array_description:
                if tn == ad:
                    final_list.append(tr)
            for at in array_title:
                if tn == at:
                    final_list.append(tr)
    context = {
        'track_list': list(set(final_list)),
        }
    context.update(global_context())
    return render(request, 'biblioteca_sistedes/list_of_tracks.html', context)


def GetListOfArticles(request):
    txtAutor = request.GET.get('txtAutor') or False
    articles = Article.objects.all()
    final_list = []
    for ar in articles:
        for au in ar.author_ids.all():
            if txtAutor == au.name + ' ' + au.middle_name + ' ' + au.last_name:
                final_list.append(ar)
    context = {
        'article_list': list(set(final_list)),
        'author_name': txtAutor,
        }
    context.update(global_context())
    return render(
        request,
        'biblioteca_sistedes/list_of_articles.html',
        context
        )


def GetTracks(request, name=None, year=None, id=None, ided=None):
    conference = Conference.objects.filter(domain=name)[:1]
    edition = Edition.objects.filter(
            year=year,
            conference_id=conference
        )[:1]
    track = Track.objects.filter(edition_id=edition, id=id)[0]
    articles = Article.objects.filter(track_ids=track.id)
    context = {'track': track, 'articles': articles}
    context.update(global_context())
    return render(request, 'biblioteca_sistedes/get_track.html', context)


def Login(request):
    username = request.POST.get("username", "")
    password = request.POST.get("password", "")
    if CheckUser(username, password):
        user_loged = User.objects.get(username=username)
        request.session['username'] = username
        request.session['rol'] = user_loged.rol
        request.session['user'] = user_loged
        return HttpResponseRedirect('/')
    else:
        context = {'errorLogin': True, 'user_setted': username}
        return render(request, 'biblioteca_sistedes/login.html', context)


def Logout(request):
    if request.session.get('username'):
        del request.session['username']
    if request.session.get('rol'):
        del request.session['rol']
    if request.session.get('user'):
        del request.session['user']
    return HttpResponseRedirect('/')

# PRIVATE


def ConferenceView(request, pk=None):
    username = request.session.get('username')
    if username:
        conference = get_object_or_404(Conference, pk=pk)
        edition_list = Edition.objects.filter(conference_id=conference.id)
        context = {
            'conference': conference,
            'edition_list': edition_list,
            }
        return render(
            request,
            'biblioteca_sistedes/conference_detail.html',
            context
            )
    else:
        return HttpResponseRedirect('/')


def EditionView(request, pk=None):
    username = request.session.get('username')
    if username:
        edition = get_object_or_404(Edition, pk=pk)
        track_list = Track.objects.filter(edition_id=edition.id)
        logged_user = User.objects.get(username=username)
        context = {
            'edition': edition,
            'track_list': track_list,
            'logged_user': logged_user,
            }
        return render(
            request,
            'biblioteca_sistedes/edition_detail.html',
            context
            )
    else:
        return HttpResponseRedirect('/')


def TrackView(request, pk=None):
    username = request.session.get('username')
    if username:
        logged_user = User.objects.get(username=username)
        track = get_object_or_404(Track, pk=pk)
        article_list = Article.objects.filter(track_ids=track.id)
        context = {
            'track': track,
            'article_list': article_list,
            'logged_user': logged_user,
            }
        return render(
            request,
            'biblioteca_sistedes/track_detail.html',
            context
            )
    else:
        return HttpResponseRedirect('/')


def ArticleView(request, pk=None):
    username = request.session.get('username')
    if username:
        logged_user = User.objects.get(username=username)
        article = get_object_or_404(Article, pk=pk)
        article = get_object_or_404(Article, pk=pk)
        track_list = article.track_ids.all()
        keyword_list = article.keyword_ids.all()
        author_list = article.author_ids.all()
        logged_user = User.objects.get(username=username)
        context = {
            'article': article,
            'track_list': track_list,
            'keyword_list': keyword_list,
            'author_list': author_list,
            'logged_user': logged_user,
            }
        return render(
            request,
            'biblioteca_sistedes/article_detail.html',
            context
            )
    else:
        return HttpResponseRedirect('/')


def AuthorView(request, pk=None):
    username = request.session.get('username')
    if username:
        author = get_object_or_404(Author, pk=pk)
        article_list = Article.objects.filter(author_ids=author.id)
        context = {
            'author': author,
            'article_list': article_list,
            }
        return render(
            request,
            'biblioteca_sistedes/author_detail.html',
            context
            )
    else:
        return HttpResponseRedirect('/')


def BulletinView(request, pk=None):
    username = request.session.get('username')
    rol = request.session.get('rol')
    if username and rol == 1:
        bulletin = get_object_or_404(Bulletin, pk=pk)
        context = {
            'bulletin': bulletin,
            }
        return render(
            request,
            'biblioteca_sistedes/bulletin_detail.html',
            context
            )
    else:
        return HttpResponseRedirect('/')


def KeywordView(request, pk=None):
    username = request.session.get('username')
    if username:
        keyword = get_object_or_404(Keyword, pk=pk)
        article_list = Article.objects.filter(keyword_ids=keyword.id)
        context = {
            'keyword': keyword,
            'article_list': article_list,
            }
        return render(
            request,
            'biblioteca_sistedes/keyword_detail.html',
            context
            )
    else:
        return HttpResponseRedirect('/')


def UserView(request, pk=None):
    username = request.session.get('username')
    rol = request.session.get('rol')
    if username and rol == 1:
        user = get_object_or_404(User, pk=pk)
        article_list = Article.objects.filter(user_ids=user.id)
        track_list = Track.objects.filter(user_ids=user.id)
        edition_list = Edition.objects.filter(user_ids=user.id)
        context = {
            'user': user,
            'article_list': article_list,
            'track_list': track_list,
            'edition_list': edition_list,
            }
        return render(
            request,
            'biblioteca_sistedes/user_detail.html',
            context
            )
    else:
        return HttpResponseRedirect('/')


def global_context():
    years = [b.date.year for b in Bulletin.objects.all()]
    year_list = set(list(years))
    context = {
        "conferences": Conference.objects.all(),
        "editions": Edition.objects.all(),
        "tracks": Track.objects.all(),
        "bulletin_years": year_list,
        "bulletins": Bulletin.objects.all(),
        }
    return context


def search_article(
        stype,
        key=False,
        txtTitulo=False,
        selCondAutor=False,
        txtAutor=False,
        selCondAfiliacion=False,
        txtAfiliacion=False,
        selCondKeyword=False,
        txtKeyword=False
        ):
        articles = Article.objects.all()
        conference_list = []
        list_by_author = []
        list_by_keyword = []
        def_article_authors = []
        def_article_authors_mn = []
        def_article_authors_ln = []
        def_article_keywords = []
        if stype == 'b':
            for a in articles:
                article_name = a.name.split()
                article_description = a.description.split()
                article_authors = [
                    author.name for author in a.author_ids.all()
                    ]
                for defaut in article_authors:
                    def_article_authors = def_article_authors + defaut.split()

                article_authors_mn = [
                    author.middle_name for author in a.author_ids.all()
                    ]
                for defaut in article_authors_mn:
                    def_article_authors_mn = def_article_authors_mn + \
                        defaut.split()

                article_authors_ln = [
                    author.last_name for author in a.author_ids.all()
                    ]
                for defaut in article_authors_ln:
                    def_article_authors_ln = def_article_authors_ln + \
                        defaut.split()

                article_keywords = [
                    keyword.name for keyword in a.keyword_ids.all()
                    ]
                for defaut in article_keywords:
                    def_article_keywords = def_article_keywords + \
                        defaut.split()

                list_search = article_name + article_description + \
                    def_article_authors + \
                    def_article_authors_ln + \
                    def_article_authors_mn + \
                    def_article_keywords

                final_list = list(set(list_search))

                for n in final_list:
                    for k in key.split():
                        if k.lower() in n.lower():
                            conference_list.append(a)
                            break
                print(final_list)

        elif stype == 'a':
            conference_list = list([])
            for a in articles:
                article_name = a.name
                articles_autor = a.author_ids.all()
                article_keyword = a.keyword_ids.all()
                if txtTitulo:
                    for n in article_name.split():
                        for tt in txtTitulo.split():
                            if tt.lower() in n.lower():
                                conference_list = list(conference_list)
                                conference_list.append(a)
                                break
                if txtAutor:
                    for autor in articles_autor:
                        for n in autor.name.split():
                            if txtAutor.lower() in n.lower():
                                list_by_author.append(a)
                                break
                    if selCondAutor == 'o':
                        conference_list = list(conference_list) + \
                            list_by_author
                    else:
                        conference_list = set(conference_list).intersection(
                            list_by_author
                            )
                if txtKeyword:
                    for keyword in article_keyword:
                        for n in keyword.name.split():
                            if txtKeyword.lower() in n.lower():
                                list_by_keyword.append(a)
                                break
                    if selCondKeyword == 'o':
                        conference_list = list(conference_list) + \
                            list_by_keyword
                    else:
                        conference_list = set(conference_list).intersection(
                            list_by_keyword
                            )
        return list(set(conference_list))


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
        conference_list = search_article(
            'a',
            '',
            txtTitulo,
            selCondAutor,
            txtAutor,
            selCondAfiliacion,
            txtAfiliacion,
            selCondKeyword,
            txtKeyword
            )
        context.update({'conference_list': conference_list})
    context.update(global_context())
    return render(
        request,
        'biblioteca_sistedes/advanced_search_engine.html',
        context
        )


def ConferenceDelete(request, pk=None):
    username = request.session.get('username')
    rol = request.session.get('rol')
    if username and rol == 1:
        conference = get_object_or_404(Conference, pk=pk)
        if conference:
            conference.delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def BulletinDelete(request, pk=None):
    username = request.session.get('username')
    rol = request.session.get('rol')
    if username and rol == 1:
        bulletin = get_object_or_404(Bulletin, pk=pk)
        if bulletin:
            bulletin.delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def EditionDelete(request, pk=None):
    username = request.session.get('username')
    rol = request.session.get('rol')
    if username and rol == 1:
        edition = get_object_or_404(Edition, pk=pk)
        if edition:
            edition.delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect('/')


def TrackDelete(request, pk=None):
    username = request.session.get('username')
    rol = request.session.get('rol')
    track = get_object_or_404(Track, pk=pk)
    logged_user = User.objects.get(username=username)
    if username and (rol == 1 or (logged_user in track.user_ids.all())):
        if track:
            track.delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect('/')


def AuthorDelete(request, pk=None):
    username = request.session.get('username')
    if username:
        author = get_object_or_404(Author, pk=pk)
        if author:
            author.delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect('/')


def ArticleDelete(request, pk=None):
    username = request.session.get('username')
    rol = request.session.get('rol')
    article = get_object_or_404(Article, pk=pk)
    logged_user = User.objects.get(username=username)
    if username and (rol == 1 or (logged_user in article.user_ids.all())):
        if article:
            article.delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect('/')


class ConferenceList(ListView):

    def get(self, request, **kwargs):
        username = request.session.get('username')
        rol = request.session.get('rol')
        if username and rol == 1:
            context = {}
            context['object_list'] = Conference.objects.all()
            context.update(global_context())
            return render(
                request,
                'biblioteca_sistedes/conference_list.html',
                context
                )
        else:
            return HttpResponseRedirect('/')


class BulletinList(ListView):

    def get(self, request, **kwargs):
        username = request.session.get('username')
        rol = request.session.get('rol')
        if username and rol == 1:
            context = {}
            context['object_list'] = Bulletin.objects.all()
            context.update(global_context())
            return render(
                request,
                'biblioteca_sistedes/bulletin_list.html',
                context
                )
        else:
            return HttpResponseRedirect('/')


class EditionList(ListView):

    def get(self, request, **kwargs):
        username = request.session.get('username')
        rol = request.session.get('rol')
        if username and rol == 1:
            context = {}
            context['object_list'] = Edition.objects.all()
            context.update(global_context())
            return render(
                request,
                'biblioteca_sistedes/edition_list.html',
                context
                )
        else:
            return HttpResponseRedirect('/')


class AuthorList(ListView):

    def get(self, request, **kwargs):
        username = request.session.get('username')
        if username:
            context = {}
            context['object_list'] = Author.objects.all()
            context.update(global_context())
            return render(
                request,
                'biblioteca_sistedes/author_list.html',
                context
                )
        else:
            return HttpResponseRedirect('/')


class TrackList(ListView):

    def get(self, request, **kwargs):
        username = request.session.get('username')
        rol = request.session.get('rol')
        if username and (rol == 1 or rol == 2):
            logged_user = User.objects.get(username=username)
            context = {}
            context['logged_user'] = logged_user
            context['object_list'] = GetListObjects(username, rol, Track)
            context.update(global_context())
            return render(
                request,
                'biblioteca_sistedes/track_list.html',
                context
                )
        else:
            return HttpResponseRedirect('/')


class ArticleList(ListView):

    def get(self, request, **kwargs):
        username = request.session.get('username')
        rol = request.session.get('rol')
        if username:
            context = {}
            logged_user = User.objects.get(username=username)
            context['object_list'] = GetListObjects(username, rol, Article)
            context['logged_user'] = logged_user
            context.update(global_context())
            return render(
                request,
                'biblioteca_sistedes/article_list.html',
                context
                )
        else:
            return HttpResponseRedirect('/')


class KeywordList(ListView):

    def get(self, request, **kwargs):
        username = request.session.get('username')
        if username:
            context = {}
            context['object_list'] = Keyword.objects.all()
            context.update(global_context())
            return render(
                request,
                'biblioteca_sistedes/keyword_list.html',
                context
                )
        else:
            return HttpResponseRedirect('/')


class UserList(ListView):

    def get(self, request, **kwargs):
        username = request.session.get('username')
        rol = request.session.get('rol')
        if username and rol == 1:
            context = {}
            context['object_list'] = User.objects.all()
            context.update(global_context())
            return render(
                request,
                'biblioteca_sistedes/user_list.html',
                context
                )
        else:
            return HttpResponseRedirect('/')


class ConferenceCreate(CreateView):
    form_class = ConferenceForm

    def get(self, request, **kwargs):
        username = request.session.get('username')
        rol = request.session.get('rol')
        if username and rol == 1:
            context = {}
            pk = self.kwargs.get('pk', 0)
            conference = Conference.objects.get(id=pk) if pk != 0 else False
            if 'form_conference' not in context:
                if conference:
                    context['form_conference'] = self.form_class(
                        instance=conference
                        )
                    context['id'] = pk
                else:
                    context['form_conference'] = self.form_class(
                        self.request.GET
                        )
            context.update(global_context())
            return render(
                request,
                'biblioteca_sistedes/conference_create.html',
                context
                )
        else:
            return HttpResponseRedirect('/')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        pk = self.kwargs.get('pk', 0)
        conference = Conference.objects.get(id=pk) if pk != 0 else False
        if conference:
            form = self.form_class(request.POST, instance=conference)
        else:
            form = self.form_class(request.POST)
        if form.is_valid():
            conference = form.save()
            return HttpResponseRedirect('/conference_list/')
        else:
            return self.render_to_response(self.get_context_data(form=form))


class EditionCreate(CreateView):
    form_class = EditionForm

    def get(self, request, **kwargs):
        username = request.session.get('username')
        rol = request.session.get('rol')
        if username and rol == 1:
            context = {}
            pk = self.kwargs.get('pk', 0)
            edition = Edition.objects.get(id=pk) if pk != 0 else False
            if 'form_edition' not in context:
                if edition:
                    context['form_edition'] = self.form_class(instance=edition)
                    context['id'] = pk
                else:
                    context['form_edition'] = self.form_class(self.request.GET)
            context.update(global_context())
            return render(
                request,
                'biblioteca_sistedes/edition_create.html',
                context
                )
        else:
            return HttpResponseRedirect('/')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        pk = self.kwargs.get('pk', 0)
        edition = Edition.objects.get(id=pk) if pk != 0 else False
        if edition:
            form = self.form_class(request.POST, instance=edition)
        else:
            form = self.form_class(request.POST)
        if form.is_valid():
            edition = form.save()
            logged_user = request.session.get('user')
            edition.user_ids.add(logged_user)
            return HttpResponseRedirect('/edition_list/')
        else:
            return self.render_to_response(self.get_context_data(form=form))


class AuthorCreate(CreateView):
    form_class = AuthorForm

    def get(self, request, **kwargs):
        username = request.session.get('username')
        if username:
            context = {}
            pk = self.kwargs.get('pk', 0)
            author = Author.objects.get(id=pk) if pk != 0 else False
            if 'form_author' not in context:
                if author:
                    context['form_author'] = self.form_class(instance=author)
                    context['id'] = pk
                else:
                    context['form_author'] = self.form_class(self.request.GET)
            context.update(global_context())
            return render(
                request,
                'biblioteca_sistedes/author_create.html',
                context
                )
        else:
            return HttpResponseRedirect('/')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        pk = self.kwargs.get('pk', 0)
        author = Author.objects.get(id=pk) if pk != 0 else False
        if author:
            form = self.form_class(request.POST, instance=author)
        else:
            form = self.form_class(request.POST)
        if form.is_valid():
            author = form.save()
            return HttpResponseRedirect('/author_list/')
        else:
            return self.render_to_response(self.get_context_data(form=form))


class TrackCreate(CreateView):
    form_class = TrackForm

    def get(self, request, **kwargs):
        username = request.session.get('username')
        rol = request.session.get('rol')
        if username and (rol == 1 or rol == 2):
            logged_user = request.session.get('user')
            context = {}
            pk = self.kwargs.get('pk', 0)
            track = Track.objects.get(id=pk) if pk != 0 else False
            if 'form_track' not in context:
                if track:
                    if logged_user in track.user_ids.all() or rol == 1:
                        context['form_track'] = self.form_class(instance=track)
                        context['id'] = pk
                    else:
                        return HttpResponseRedirect('/')
                else:
                    context['form_track'] = self.form_class(self.request.GET)
            context.update(global_context())
            return render(
                request,
                'biblioteca_sistedes/track_create.html',
                context
                )
        else:
            return HttpResponseRedirect('/')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        pk = self.kwargs.get('pk', 0)
        track = Track.objects.get(id=pk) if pk != 0 else False
        if track:
            form = self.form_class(request.POST, instance=track)
        else:
            form = self.form_class(request.POST)
        if form.is_valid():
            track = form.save()
            logged_user = request.session.get('user')
            track.user_ids.add(logged_user)
            return HttpResponseRedirect('/track_list/')
        else:
            return self.render_to_response(self.get_context_data(form=form))


class ArticleCreate(CreateView):
    form_class = ArticleForm

    def get(self, request, **kwargs):
        username = request.session.get('username')
        if username:
            context = {}
            pk = self.kwargs.get('pk', 0)
            article = Article.objects.get(id=pk) if pk != 0 else False
            if 'form_article' not in context:
                if article:
                    logged_user = request.session.get('user')
                    if logged_user in article.user_ids.all() or \
                            logged_user.rol == 1:
                        context['form_article'] = self.form_class(
                            instance=article,
                            username=request.session.get('username'),
                            )
                        context['id'] = pk
                    else:
                        return HttpResponseRedirect('/')
                else:
                    context['form_article'] = self.form_class(
                        self.request.GET,
                        username=request.session.get('username'),
                        )
            context.update(global_context())
            return render(
                request,
                'biblioteca_sistedes/article_create.html',
                context
                )
        else:
            return HttpResponseRedirect('/')

    def post(self, request, *args, **kwargs):
        fs = FileSystemStorage()
        self.object = self.get_object
        pk = self.kwargs.get('pk', 0)
        article = Article.objects.get(id=pk) if pk != 0 else False
        if article:
            if article.url_file and article.url_file != '':
                fs.delete(article.url_file)
            form = self.form_class(
                request.POST or None,
                request.FILES or None,
                instance=article
                )

        else:
            form = self.form_class(request.POST or None, request.FILES or None)

        myfile = request.FILES.get('article_file')
        uploaded_file_url = ''
        if myfile:
            sufix_number = Sequence.get_last_number()
            next_number = int(sufix_number) + 1
            file_name = 'file_' + str(next_number)
            Sequence(number=next_number).save()
            filename = fs.save(file_name, myfile)
            uploaded_file_url = fs.url(filename)

        if form.is_valid():
            article = form.save()
            logged_user = request.session.get('user')
            article.user_ids.add(logged_user)
            article.url_file = uploaded_file_url
            article.save()
            return HttpResponseRedirect('/article_list/')
        else:
            return self.render_to_response(self.get_context_data(form=form))


class BulletinCreate(CreateView):
    form_class = BulletinForm

    def get(self, request, **kwargs):
        username = request.session.get('username')
        rol = request.session.get('rol')
        if username and rol == 1:
            context = {}
            pk = self.kwargs.get('pk', 0)
            bulletin = Bulletin.objects.get(id=pk) if pk != 0 else False
            if 'form_bulletin' not in context:
                if bulletin:
                    month = '0' + str(bulletin.date.month) \
                        if bulletin.date.month <= 9 \
                            else str(bulletin.date.month)
                    day = '0' + str(bulletin.date.day) \
                        if bulletin.date.day <= 9 else str(bulletin.date.day)
                    date = str(bulletin.date.year) + \
                        '-' + month + \
                        '-' + day
                    context['date'] = date
                    context['form_bulletin'] = self.form_class(
                        instance=bulletin,
                        )
                    context['id'] = pk
                else:
                    context['form_bulletin'] = self.form_class(
                        self.request.GET,
                        )
            context.update(global_context())
            return render(
                request,
                'biblioteca_sistedes/bulletin_create.html',
                context
                )
        else:
            return HttpResponseRedirect('/')

    def post(self, request, *args, **kwargs):
        fs = FileSystemStorage(location=settings.BULLETIN_ROOT)
        self.object = self.get_object
        pk = self.kwargs.get('pk', 0)
        bulletin = Bulletin.objects.get(id=pk) if pk != 0 else False
        if bulletin:
            if bulletin.url_file and bulletin.url_file != '':
                fs.delete(bulletin.url_file)
            form = self.form_class(
                request.POST or None,
                request.FILES or None,
                instance=bulletin
                )

        else:
            form = self.form_class(request.POST or None, request.FILES or None)

        myfile = request.FILES.get('bulletin_file')
        uploaded_file_url = ''
        if myfile:
            sufix_number = Sequence.get_last_number()
            next_number = int(sufix_number) + 1
            file_name = 'file_' + str(next_number)
            Sequence(number=next_number).save()
            filename = fs.save(file_name, myfile)
            uploaded_file_url = fs.url(filename)

        if form.is_valid():
            bulletin = form.save()
            bulletin.url_file = uploaded_file_url
            bulletin.name = bulletin.name + \
                self.get_name_month(bulletin.date)
            bulletin.save()
            return HttpResponseRedirect('/bulletin_list/')
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_name_month(self, date=False):
        month = ''
        if date.month == 1:
            month = 'Enero'
        elif date.month == 2:
            month = 'Febrero'
        elif date.month == 3:
            month = 'Marzo'
        elif date.month == 4:
            month = 'Abril'
        elif date.month == 5:
            month = 'Mayo'
        elif date.month == 6:
            month = 'Junio'
        elif date.month == 7:
            month = 'Julio'
        elif date.month == 8:
            month = 'Agosto'
        elif date.month == 9:
            month = 'Septiembre'
        elif date.month == 10:
            month = 'Octubre'
        elif date.month == 11:
            month = 'Noviembre'
        elif date.month == 12:
            month = 'Diciembre'
        return ' ' + month + ' de ' + str(date.year)


class KeywordCreate(CreateView):
    form_class = KeywordForm

    def get(self, request, **kwargs):
        username = request.session.get('username')
        if username:
            context = {}
            pk = self.kwargs.get('pk', 0)
            keyword = Keyword.objects.get(id=pk) if pk != 0 else False
            if 'form_keyword' not in context:
                if keyword:
                    context['form_keyword'] = self.form_class(instance=keyword)
                    context['id'] = pk
                else:
                    context['form_keyword'] = self.form_class(self.request.GET)
            context.update(global_context())
            return render(
                request,
                'biblioteca_sistedes/keyword_create.html',
                context
                )
        else:
            return HttpResponseRedirect('/')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        pk = self.kwargs.get('pk', 0)
        keyword = Keyword.objects.get(id=pk) if pk != 0 else False
        if keyword:
            form = self.form_class(request.POST, instance=keyword)
        else:
            form = self.form_class(request.POST)
        if form.is_valid():
            keyword = form.save()
            return HttpResponseRedirect('/keyword_list/')
        else:
            return self.render_to_response(self.get_context_data(form=form))


class UserCreate(CreateView):
    form_class = UserForm

    def get(self, request, **kwargs):
        username = request.session.get('username')
        rol = request.session.get('rol')
        if username and rol == 1:
            context = {}
            pk = self.kwargs.get('pk', 0)
            user = User.objects.get(id=pk) if pk != 0 else False
            if 'form_user' not in context:
                if user:
                    context['form_user'] = self.form_class(instance=user)
                    context['id'] = pk
                else:
                    context['form_user'] = self.form_class(self.request.GET)
            context.update(global_context())
            return render(
                request,
                'biblioteca_sistedes/user_registration.html',
                context
                )
        else:
            return HttpResponseRedirect('/')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        pk = self.kwargs.get('pk', 0)
        user = User.objects.get(id=pk) if pk != 0 else False
        form = self.form_class(request.POST, instance=user) if user else \
            self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            if user.email:
                texto = \
                    """
                    Se ha registrado en la Biblioteca Sistedes.

                    Nombre de usuario: {0}
                    Contraseña: {1}
                    """.format(user.username, user.password)
                send_mail(
                    'Nueva registro',
                    texto,
                    'pruebas.sistedes@gmail.com',
                    [user.email],
                    )
            return HttpResponseRedirect('/user_list/')
        else:
            return self.render_to_response(
                self.get_context_data(form=form)
                )


def change_password(request):
    username = request.session.get('username')
    rol = request.session.get('rol')
    if username and rol == 1:
        if request.method == 'POST':
            try:
                password = request.POST.get('pass1')
                userid = request.POST.get('userId')
                user = User.objects.get(id=userid)
                user.password = password
                user.save()
                if user.email:
                    texto = \
                        """
                        Se ha restablecido la contraseña.
                        Nueva contraseña: {0}
                        """.format(user.password)
                    send_mail(
                        'Nueva registro',
                        texto,
                        'pruebas.sistedes@gmail.com',
                        [user.email],
                        )
                return HttpResponse(
                    """
                    <script>
                        window.location.href = "/user_list/";
                        alert('Contraseña cambiada');
                    </script>
                    """
                    )
            except:
                return HttpResponse(
                    """
                    <script>
                        alert('Error inesperado');
                        window.location.href = "/user_list/";
                    </script>
                    """
                    )
                raise
    else:
        return HttpResponseRedirect('/')


def upload_file(request):
    username = request.session.get('username')
    if username:
        try:
            object_type = request.POST.get('objectType')
            articleid = request.POST.get('articleId')
            myfile = request.FILES.get('articleFile')
            uploaded_file_url = ''
            article = get_object_or_404(Article, pk=articleid) \
                if object_type == 'a' else get_object_or_404(
                    Bulletin, pk=articleid
                    )
            fs = FileSystemStorage() if object_type == 'a' else \
                FileSystemStorage(location=settings.BULLETIN_ROOT)
            if article.url_file and article.url_file != '':
                fs.delete(article.url_file)
            if myfile:
                sufix_number = Sequence.get_last_number()
                next_number = int(sufix_number) + 1
                file_name = 'file_' + str(next_number)
                Sequence(number=next_number).save()
                filename = fs.save(file_name, myfile)
                uploaded_file_url = fs.url(filename)
                article.url_file = uploaded_file_url
                article.save()
            if object_type == 'a':
                return HttpResponse(
                    """
                    <script>
                        window.location.href = "/article_list/";
                        alert('Archivo reemplazado');
                    </script>
                    """
                    )
            else:
                return HttpResponse(
                    """
                    <script>
                        window.location.href = "/bulletin_list/";
                        alert('Archivo reemplazado');
                    </script>
                    """
                    )
        except:
            return HttpResponse(
                """
                <script>
                    window.location.href = "/article_list/";
                    alert('Error inesperado');
                </script>
                """
                )
    else:
        return HttpResponseRedirect('/')


def UserDelete(request, pk=None):
    username = request.session.get('username')
    rol = request.session.get('rol')
    if username and rol == 1:
        user = get_object_or_404(User, pk=pk)
        if user:
            user.delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
