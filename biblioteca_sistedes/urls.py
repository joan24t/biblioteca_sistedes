from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('busqueda/', views.search, name='Busqueda avanzada'),
    path('conference_list/', views.ConferenceList.as_view(), name='Lista de conferencias'),
    path('conference_create/', views.ConferenceCreate.as_view(), name='Crear conferencia'),
    path('conference_update/<int:pk>/', views.ConferenceUpdate.as_view(), name='Actualizar conferencia'),
    path('conference_delete/<int:pk>/', views.ConferenceDelete, name='Eliminar conferencia'),
    path('edition_list/', views.EditionList.as_view(), name='Lista de ediciones'),
    path('edition_create/', views.EditionCreate.as_view(), name='Crear edición'),
    path('edition_update/<int:pk>/', views.EditionUpdate.as_view(), name='Actualizar edición'),
    path('edition_delete/<int:pk>/', views.EditionDelete, name='Eliminar edición'),
    path('track_list/', views.TrackList.as_view(), name='Lista de tracks'),
    path('track_create/', views.TrackCreate.as_view(), name='Crear track'),
    path('track_update/<int:pk>/', views.TrackUpdate.as_view(), name='Actualizar track'),
    path('track_delete/<int:pk>/', views.TrackDelete, name='Eliminar track'),
    path('author_list/', views.AuthorList.as_view(), name='Lista de autores'),
    path('author_create/', views.AuthorCreate.as_view(), name='Crear autor'),
    path('author_update/<int:pk>/', views.AuthorUpdate.as_view(), name='Actualizar autor'),
    path('author_delete/<int:pk>/', views.AuthorDelete, name='Eliminar autor'),
    path('article_list/', views.ArticleList.as_view(), name='Lista de artçiculos'),
    path('article_create/', views.ArticleCreate.as_view(), name='Crear articulo'),
    path('article_update/<int:pk>/', views.ArticleUpdate.as_view(), name='Actualizar articulo'),
    path('article_delete/<int:pk>/', views.ArticleDelete, name='Eliminar articulo'),
    path('conferencias/', views.Conferences, name='Conferencias'),
    path('conferencias/<slug:name>/', views.GetConferences, name='Ver todas las conferencias'),
    path('conferencias/<slug:name>/<int:year>/', views.GetEditions, name='Ver todas las ediciones'),
    path('conferencias/<slug:name>/<int:year>/<int:id>', views.GetTracks, name='Ver todos los tracks')
]