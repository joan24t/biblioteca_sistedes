# -*- encoding:utf-8 -*-
from django import forms
from .models import Conference, Edition, Track, Article, Author, Keyword, AccessRight, User
from django.contrib import admin

ROL_CHOICE = (
    (1, 'Administrador'),
    (2, 'Presidente de comite de programa'),
    (3, 'Responsable de track'),
)

class ConferenceForm(forms.ModelForm):

	class Meta:
		model = Conference
		fields = [
			'name', 
			'domain',
		]
		labels = {
			'name': 'Nombre', 
			'domain': 'Domain',
		}
		widgets = {
			'name': forms.TextInput(attrs={
            'id': 'name_con'}),

			'domain': forms.TextInput(attrs={
            'id': 'dom_con'}),
		}

class EditionForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(EditionForm, self).__init__(*args, **kwargs)
		self.fields['conference_id'].queryset = Conference.objects.all()
		self.fields['conference_id'].label_from_instance = lambda obj: '%s' % obj.name

	class Meta:
		model = Edition
		fields = [
			'name',
			'year',
			'place',
			'topic',
			'conference_id',
		]
		labels = {
			'name': 'Nombre',
			'year': 'Year',
			'place': 'Place',
			'topic': 'Topic',
			'conference_id': 'Conference',
		}
		widgets = {
			'name': forms.TextInput(attrs={
            'id': 'name_ed',
			}),

			'year': forms.NumberInput(attrs={
            'id': 'year_ed',
			}),

			'place': forms.TextInput(attrs={
			'id': 'place_ed'}),

			'topic': forms.TextInput(attrs={
			'id': 'top_ed',
			}),

			'conference_id': forms.Select(attrs={
			'id': 'con_ed',
			}),
		}

class AuthorForm(forms.ModelForm):

	class Meta:
		model = Author
		fields = [
			'name',
			'middle_name',
			'last_name',
			'email',
		]
		labels = {
			'name': 'Nombre',
			'middle_name': 'Primer apellido',
			'last_name': 'Segundo apellido',
			'email': 'E-mail',
		}
		widgets = {
			'name': forms.TextInput(attrs={
            'id': 'name_au',
			}),

			'middle_name': forms.TextInput(attrs={
            'id': 'middle_au',
			}),

			'last_name': forms.TextInput(attrs={
			'id': 'last_au'}),

			'email': forms.EmailInput(attrs={
			'id': 'em_au',
			}),
		}

class TrackForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(TrackForm, self).__init__(*args, **kwargs)
		self.fields['edition_id'].queryset = Edition.objects.all()
		self.fields['edition_id'].label_from_instance = lambda obj: '%s' % obj.name

	class Meta:
		model = Track
		fields = [
			'name',
			'edition_id',
		]
		labels = {
			'name': 'Nombre',
			'edition_id': 'Edicion',
		}
		widgets = {
			'name': forms.TextInput(attrs={
            'id': 'name_tr',
			}),

			'edition_id': forms.Select(attrs={
            'id': 'ed_tr',
			}),
		}

class ArticleForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(ArticleForm, self).__init__(*args, **kwargs)

		self.fields['author_ids'].queryset = Author.objects.all()
		self.fields['author_ids'].label_from_instance = lambda obj: '%s' % obj.name
		self.fields['author_ids'].required = False

		self.fields['keyword_ids'].queryset = Keyword.objects.all()
		self.fields['keyword_ids'].label_from_instance = lambda obj: '%s' % obj.name
		self.fields['keyword_ids'].required = False

		self.fields['access_right_ids'].queryset = AccessRight.objects.all()
		self.fields['access_right_ids'].label_from_instance = lambda obj: '%s' % obj.name
		self.fields['access_right_ids'].required = False

		self.fields['track_ids'].queryset = Track.objects.all()
		self.fields['track_ids'].label_from_instance = lambda obj: obj.name + ' ' + '(' + str(obj.edition_id.conference_id.domain) + ')'
		self.fields['track_ids'].required = False

		self.fields['file'].required = False

	class Meta:
		model = Article
		fields = [
			'name',
			'description',
			'year',
			'author_ids',
			'keyword_ids',
			'access_right_ids',
			'track_ids',
			'file',
		]
		labels = {
			'name': 'Nombre',
			'year': 'Edicion',
			'description': 'Descripcion',
			'author_ids': 'Autores',
			'keyword_ids': 'Palabras clave',
			'access_right_ids': 'Derechos de acceso',
			'track_ids': 'Tracks',
			'file': 'Fichero',
		}
		widgets = {
			'name': forms.TextInput(attrs={
            'id': 'name_ar',
			}),
			'description': forms.Textarea(attrs={
				'id': 'desc_ar',
			}),
			'year': forms.NumberInput(attrs={
            'id': 'year_ar',
			}),
			'author_ids': forms.SelectMultiple(attrs={
            'id': 'author_ar',
			'class': 'multiselect',
			}),
			'keyword_ids': forms.SelectMultiple(attrs={
            'id': 'keyword_ar',
			'class': 'multiselect',
			}),
			'access_right_ids': forms.SelectMultiple(attrs={
            'id': 'access_right_ar',
			'class': 'multiselect',
			}),
			'track_ids': forms.SelectMultiple(attrs={
            'id': 'track_ar',
			'class': 'multiselect',
			})
		}

class KeywordForm(forms.ModelForm):

	class Meta:
		model = Keyword
		fields = [
			'name',
		]
		labels = {
			'name': 'Nombre',
		}
		widgets = {
			'name': forms.TextInput(attrs={
            'id': 'name_key'}),
		}

class UserForm(forms.ModelForm):

	class Meta:
		model = User
		fields = [
			'name',
			'surnames',
			'username',
			'email',
			'password',
			'rol',
		]
		labels = {
			'name': 'Nombre',
			'surnames': 'Apellidos',
			'username': 'Nombre de usuario',
			'email': 'Email',
			'password': 'Contraseña',
			'rol': 'Rol',
		}
		widgets = {
			'name': forms.TextInput(attrs={'id': 'name_user'}),
			'surnames': forms.TextInput(attrs={'id': 'surname_user'}),
			'username': forms.TextInput(attrs={'id': 'username_user'}),
			'email': forms.EmailInput(attrs={'id': 'email_user'}),
			'password': forms.PasswordInput(attrs={'id': 'pass_user'}),
			'rol': forms.Select(attrs={'id': 'rol_user', 'style': 'height: 40px; font-size: 20px;'}, choices=ROL_CHOICE),
		}

# class FormLogin(forms.Form):
# 	username = forms.CharField(
# 		label=("Username"),
# 		required=True,
# 		name=('username'),
# 		# id=('id_username'),
# 	)
# 	password = forms.CharField(
# 		label=("Password"),
# 		widget=forms.PasswordInput,
# 		required=True,
# 		name=('password'),
# 		# id=('id_password'),
# 	)