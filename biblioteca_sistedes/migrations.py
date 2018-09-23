from .models import Conference, Edition, Track, Article
from .models import Author, Keyword
import xml.etree.ElementTree as ET
from unidecode import unidecode


def migrate(request):
    tree = ET.parse('biblioteca_sistedes/migrations_library/datos_sistedes.xml')
    root = tree.getroot()
    user = create_user('Administrador', 'admin', 'admin@admin.es', 'admin', 1)
    for item in root.findall('item'):
        title = unidecode(item.find('title').text)
        content = unidecode(item.find('content').text) if item.find('content').text else ''
        article = create_article(title, content)
        print(article.name)
        # for pm in item.findall('postmeta'):
        #     for key in pm.findall('meta_key'):
        #         if 'author_name' in key.text:
        #             for mv in pm.findall('meta_value'):
        #                 if mv.text:
        #                     print(unidecode('     Author ' + mv.text))
        #                 else:
        #                     print(unidecode('     Author ' + 'Unknown'))
        #         if 'author_email' in key.text:
        #             for mv in pm.findall('meta_value'):
        #                 if mv.text:
        #                     print(unidecode('     Email ' + mv.text))
        #                 else:
        #                     print(unidecode('     Email ' + 'Unknown'))
        #         if 'author_univ' in key.text:
        #             for mv in pm.findall('meta_value'):
        #                 if mv.text:
        #                     print(unidecode('     Universidad: ' + mv.text))
        #                 else:
        #                     print(unidecode('     Universidad: ' + 'Unknown'))
        #         if 'track' in key.text:
        #             for mv in pm.findall('meta_value'):
        #                 if mv.text:
        #                     print(unidecode('     Track: ' + mv.text))
        #                 else:
        #                     print(unidecode('     Track: ' + 'Unknown'))
        #         if 'handle' in key.text:
        #             for mv in pm.findall('meta_value'):
        #                 if mv.text:
        #                     if 'JCIS' in mv.text:
        #                         conference = mv.text.split('/')[1]
        #                         edition = mv.text.split('/')[2]
        #                         print(unidecode('      conferencia: ' + conference))
        #                         print(unidecode('      edicion: ' + edition))
        #                         print(unidecode('      handle: ' + mv.text))
        #                     elif 'JISBD' in mv.text:
        #                         conference = mv.text.split('/')[1]
        #                         edition = mv.text.split('/')[2]
        #                         print(unidecode('      conferencia: ' + conference))
        #                         print(unidecode('      edicion: ' + edition))
        #                         print(unidecode('      handle: ' + mv.text))
        #                     elif 'PROLE' in mv.text:
        #                         conference = mv.text.split('/')[1]
        #                         edition = mv.text.split('/')[2]
        #                         print(unidecode('      conferencia: ' + conference))
        #                         print(unidecode('      edicion: ' + edition))
        #                         print(unidecode('      handle: ' + mv.text))
        #                     else:
        #                         print(unidecode('      conferencia: ' + 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'))
        #                 else:
        #                     print(unidecode('     conferencia: ' + 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'))

def create_author(name, email, university, article):
    author = Author.objects.get(email=email) or False
    if author is False:
        author = Author.objects.create(name=name, email=email, university=university)
    author.article_ids.add(article)
    return author

def create_keyword(name, article):
    keyword = Keyword.objects.get(name=name) or False
    if keyword is False:
        keyword = Keyword.objects.create(name=name)
    keyword.article_ids.add(article)
    return keyword

def create_conference(name, domain, description):
    conference = Conference.objects.get(domain=domain) or False
    if conference is False:
        Conference.objects.create(name=name, domain=domain, description=description)
    return conference

def create_edition(name, preamble, description, year, conference, user):
    edition = Edition.objects.get(year=year, conference_id=conference) or False
    if edition is False:
        edition = Edition.objects.create(name=name, year=year, conference_id=conference)
        edition.user_ids.add(user)
    return edition

def create_track(name, edition, user, article):
    track = Track.objects.get(name=name) or False
    if track is False:
        track = Track.objects.create(name=name, edition_id=edition)
        if user not in track.user_ids.all():
            track.user_ids.add(user)
        track.article_ids.add(article)
    return track


def create_article(name, description, user):
    article = Article.objects.create(name=name, description=description)
    if user not in article.user_ids.all():
        article.user_ids.add(user)
    return article

def create_user(name, username, email, password, rol):
    user = User.objects.get(username=username) or False
    if user is False
        user = User.objects.create(name=name, username=username, email=email, password=password, rol=rol)
    return user
