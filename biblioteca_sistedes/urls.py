from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('getlogin/', views.GetLogin, name='Get login'),
    path('login/', views.Login, name='Login'),
    path('logout/', views.Logout, name='Logout'),
    path('busqueda/', views.search, name='Busqueda avanzada'),
    path('download/<int:pk>/', views.download, name='Descargar fichero'),
    path(
        'conference_list/',
        views.ConferenceList.as_view(),
        name='Lista de conferencias'
        ),
    path(
        'conference_create/',
        views.ConferenceCreate.as_view(),
        name='Crear conferencia'
        ),
    path(
        'conference_update/<int:pk>/',
        views.ConferenceCreate.as_view(),
        name='Actualizar conferencia'
        ),
    path(
        'conference_delete/<int:pk>/',
        views.ConferenceDelete,
        name='Eliminar conferencia'
        ),
    path(
        'edition_list/',
        views.EditionList.as_view(),
        name='Lista de ediciones'
        ),
    path(
        'edition_create/',
        views.EditionCreate.as_view(),
        name='Crear edición'
        ),
    path(
        'edition_update/<int:pk>/',
        views.EditionCreate.as_view(),
        name='Actualizar edición'
        ),
    path(
        'edition_delete/<int:pk>/',
        views.EditionDelete,
        name='Eliminar edición'
        ),
    path('track_list/', views.TrackList.as_view(), name='Lista de tracks'),
    path('track_create/', views.TrackCreate.as_view(), name='Crear track'),
    path(
        'track_update/<int:pk>/',
        views.TrackCreate.as_view(),
        name='Actualizar track'
        ),
    path('track_delete/<int:pk>/', views.TrackDelete, name='Eliminar track'),
    path('author_list/', views.AuthorList.as_view(), name='Lista de autores'),
    path('author_create/', views.AuthorCreate.as_view(), name='Crear autor'),
    path(
        'author_update/<int:pk>/',
        views.AuthorCreate.as_view(),
        name='Actualizar autor'
        ),
    path('author_delete/<int:pk>/', views.AuthorDelete, name='Eliminar autor'),
    path(
        'article_list/',
        views.ArticleList.as_view(),
        name='Lista de articulos'
        ),
    path(
        'article_create/',
        views.ArticleCreate.as_view(),
        name='Crear articulo'
        ),
    path(
        'article_update/<int:pk>/',
        views.ArticleCreate.as_view(),
        name='Actualizar articulo'
        ),
    path(
        'article_delete/<int:pk>/',
        views.ArticleDelete,
        name='Eliminar articulo'
        ),
    path('conferencias/', views.Conferences, name='Conferencias'),
    path(
        'conferencias/<slug:name>/',
        views.GetConferences,
        name='Ver todas las conferencias'
        ),
    path(
        'conferencias/<slug:name>/<int:year>/',
        views.GetEditions,
        name='Ver todas las ediciones'
        ),
    path(
        'conferencias/<slug:name>/<int:year>/<int:id>',
        views.GetTracks,
        name='Ver todos los tracks'
        ),
    path(
        'keyword_list/',
        views.KeywordList.as_view(),
        name='Lista de palabras clave'
        ),
    path(
        'keyword_create/',
        views.KeywordCreate.as_view(),
        name='Crear palabra clave'
        ),
    path(
        'keyword_update/<int:pk>/',
        views.KeywordCreate.as_view(),
        name='Modificar palabra clave'
        ),
    path('user_list/', views.UserList.as_view(), name='Lista de usuarios'),
    path('user_create/', views.UserCreate.as_view(), name='Crear Usuario'),
    path(
        'user_update/<int:pk>/',
        views.UserCreate.as_view(),
        name='Actualizar usuario'
        ),
    path('noticias/', views.News, name='Noticias'),
    path('contacto/', views.Contactus, name='Contacto'),
    path('biblioteca/', views.Aboutus, name='Acerca de'),
    path(
        'conference_view/<int:pk>/',
        views.ConferenceView,
        name='Ver conferencia'
        ),
    path('edition_view/<int:pk>/', views.EditionView, name='Ver edicion'),
    path('track_view/<int:pk>/', views.TrackView, name='Ver track'),
    path('article_view/<int:pk>/', views.ArticleView, name='Ver articulo'),
    path('author_view/<int:pk>/', views.AuthorView, name='Ver autor'),
    path(
        'keyword_view/<int:pk>/',
        views.KeywordView,
        name='Ver palabra clave'
        ),
    path('user_view/<int:pk>/', views.UserView, name='Ver usuario'),
    path('check_user/', views.check_user, name='validate_username'),
    ]
