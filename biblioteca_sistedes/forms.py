# -*- encoding:utf-8 -*-
from django import forms
from .models import Conference, Edition, Track, Article
from .models import Author, Keyword, AccessRight, User, Bulletin
import datetime

ROL_CHOICE = (
    (1, 'Administrador'),
    (2, 'Presidente de comite de programa'),
    (3, 'Responsable de track'),
    )


class ConferenceForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ConferenceForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['domain'].required = True
        self.fields['description'].required = False

    class Meta:
        model = Conference
        fields = [
            'name',
            'domain',
            'description',
            ]
        labels = {
            'name': 'Nombre',
            'domain': 'Domain',
            'description': 'Descripción',
            }
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'id': 'name_con'
                        }),
            'domain': forms.TextInput(
                attrs={
                    'id': 'dom_con'
                    }),
            'description': forms.Textarea(
                attrs={
                    'id': 'desc_con'
                    }),
            }


class EditionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditionForm, self).__init__(*args, **kwargs)
        self.fields['conference_id'].queryset = Conference.objects.all()
        self.fields['conference_id'].label_from_instance = lambda obj: '%s' \
            % obj.name
        self.fields['preamble'].required = False
        self.fields['description'].required = False
        self.fields['conference_id'].required = True
        self.fields['place'].required = True
        self.fields['name'].required = True
        self.fields['year'].required = True

    class Meta:
        model = Edition
        choices = [(year, year) for year in range(
            2000,
            datetime.datetime.now().year + 1
            )]
        fields = [
            'name',
            'year',
            'place',
            'conference_id',
            'preamble',
            'description',
            ]
        labels = {
            'name': 'Nombre',
            'year': 'Year',
            'place': 'Place',
            'conference_id': 'Conference',
            'preamble': 'Preamble',
            'description': 'Description',
            }
        widgets = {
            'name': forms.TextInput(attrs={
                'id': 'name_ed',
                }),

            'year': forms.Select(
                choices=choices,
                attrs={
                    'id': 'year_ed',
                    }),

            'place': forms.TextInput(attrs={
                'id': 'place_ed'
                }),

            'conference_id': forms.Select(attrs={
                'id': 'con_ed',
                }),
            'preamble': forms.Textarea(attrs={
                'id': 'pre_ed',
                }),
            'description': forms.Textarea(attrs={
                'id': 'desc_ed',
                }),
            }


class AuthorForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AuthorForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['email'].required = True
        self.fields['middle_name'].required = False
        self.fields['last_name'].required = False
        self.fields['country'].required = False
        self.fields['department'].required = False
        self.fields['university'].required = False

    class Meta:
        model = Author
        fields = [
            'name',
            'middle_name',
            'last_name',
            'email',
            'country',
            'department',
            'university',
            ]
        labels = {
            'name': 'Nombre',
            'middle_name': 'Primer apellido',
            'last_name': 'Segundo apellido',
            'email': 'E-mail',
            'country': 'País',
            'department': 'Departamento',
            'university': 'Universidad',
            }
        widgets = {
            'name': forms.TextInput(attrs={
                'id': 'name_au',
                }),

            'middle_name': forms.TextInput(attrs={
                'id': 'middle_au',
                }),

            'last_name': forms.TextInput(attrs={
                'id': 'last_au'
                }),

            'email': forms.EmailInput(attrs={
                'id': 'em_au',
                }),
            'country': forms.TextInput(attrs={
                'id': 'co_au',
                }),
            'department': forms.TextInput(attrs={
                'id': 'de_au',
                }),
            'university': forms.TextInput(attrs={
                'id': 'uni_au',
                }),
                }


class TrackForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TrackForm, self).__init__(*args, **kwargs)
        self.fields['edition_id'].queryset = Edition.objects.all()
        self.fields['edition_id'].label_from_instance = lambda obj: '%s' % \
            obj.name
        self.fields['preamble'].required = False
        self.fields['description'].required = False
        self.fields['user_ids'].queryset = User.objects.all()
        self.fields['user_ids'].label_from_instance = lambda obj: '%s' % \
            obj.name
        self.fields['name'].required = True
        self.fields['user_ids'].required = True
        self.fields['edition_id'].required = True

    class Meta:
        model = Track
        fields = [
            'name',
            'preamble',
            'description',
            'edition_id',
            'user_ids',
            ]
        labels = {
            'name': 'Nombre',
            'preamble': 'Preambulo',
            'description': 'Descripcion',
            'edition_id': 'Edicion',
            'user_ids': 'Responsables del track',
            }
        widgets = {
            'name': forms.TextInput(attrs={
                'id': 'name_tr',
                }),

            'preamble': forms.Textarea(attrs={
                'id': 'pre_tr',
                }),

            'description': forms.Textarea(attrs={
                'id': 'desc_tr',
                }),

            'edition_id': forms.Select(attrs={
                'id': 'ed_tr',
                }),
            'user_ids': forms.SelectMultiple(attrs={
                'id': 'user_tr',
                'class': 'multiselect',
                }),
            }


class ArticleForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        users = []
        if kwargs.get('username'):
            username = kwargs.pop('username')
            user = User.objects.get(username=username)
            users.append(user)
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.fields['author_ids'].queryset = Author.objects.all()
        self.fields['author_ids'].label_from_instance = lambda obj: '%s' % \
            (obj.name + ' ' + obj.middle_name + ' ' + obj.last_name)

        self.fields['keyword_ids'].queryset = Keyword.objects.all()
        self.fields['keyword_ids'].label_from_instance = lambda obj: '%s' % \
            obj.name

        self.fields['access_right_ids'].queryset = AccessRight.objects.all()
        self.fields['access_right_ids'].label_from_instance = lambda obj: '%s'\
            % obj.name
        self.fields['access_right_ids'].required = False

        # self.fields['track_ids'].queryset = Track.objects.filter(
        #     user_ids__in=users,
        #     ) if kwargs.get('username') else Track.objects.all()
        self.fields['track_ids'].label_from_instance = lambda obj: '%s' % (
            obj.name + ' ' + '(' + str(obj.edition_id.name) + ' - ' +
            str(obj.edition_id.conference_id.domain.upper()) + ')'
            )
        self.fields['edition_id'].queryset = Edition.objects.all()
        self.fields['edition_id'].label_from_instance = lambda obj: '%s' % \
            obj.name
        self.fields['year'].required = False
        self.fields['description'].required = False
        self.fields['name'].required = True
        self.fields['handle'].required = False
        self.fields['edition_id'].required = False
    class Meta:
        model = Article
        fields = [
            'name',
            'description',
            'year',
            'edition_id',
            'author_ids',
            'keyword_ids',
            'access_right_ids',
            'track_ids',
            'handle',
            ]
        labels = {
            'name': 'Nombre',
            'year': 'Ano',
            'edition_id': 'Edicion',
            'description': 'Descripcion',
            'author_ids': 'Autores',
            'keyword_ids': 'Palabras clave',
            'access_right_ids': 'Derechos de acceso',
            'track_ids': 'Tracks',
            'handle': 'Handle',
            }
        widgets = {
            'name': forms.TextInput(attrs={
                'id': 'name_ar',
                }),
            'handle': forms.TextInput(attrs={
                'id': 'handle_ar',
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
                }),
            'edition_id': forms.Select(attrs={
                'id': 'ed_ar',
                }),
            }


class KeywordForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(KeywordForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = True

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
                'id': 'name_key'
                }),
            }


class UserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['surnames'].required = False
        self.fields['username'].required = True
        self.fields['email'].required = True
        self.fields['password'].required = True
        self.fields['rol'].required = True

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
            'rol': forms.Select(attrs={
                'id': 'rol_user', 'style': 'height: 40px; font-size: 20px;'},
                choices=ROL_CHOICE
                ),
            }


class BulletinForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BulletinForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['date'].required = True

    class Meta:
        model = Bulletin
        fields = [
            'name',
            'date',
            ]
        labels = {
            'name': 'Nombre',
            'date': 'Fecha',
            }
        widgets = {
            'name': forms.TextInput(attrs={'id': 'name_bul'}),
            'date': forms.DateInput(
                format='%d/%m/%Y',
                attrs={'id': 'date_bul'},
                ),
            }
