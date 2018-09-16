from .models import Conference, Edition, Track, Article
from .models import Author, Keyword
import xml.etree.ElementTree as ET
from unidecode import unidecode


def migrate(request):
    tree = ET.parse('biblioteca_sistedes/migrations_library/datos_sistedes.xml')
    root = tree.getroot()
    for item in root.findall('item'):
        title = unidecode(item.find('title').text)
        content = unidecode(item.find('content').text) if item.find('content').text else ''
        print(title)
        print(content)
        for pm in item.findall('postmeta'):
            for key in pm.findall('meta_key'):
                if 'author_name' in key.text:
                    for mv in pm.findall('meta_value'):
                        if mv.text:
                            print(unidecode('     Author ' + mv.text))
                        else:
                            print(unidecode('     Author ' + 'Unknown'))
                if 'author_email' in key.text:
                    for mv in pm.findall('meta_value'):
                        if mv.text:
                            print(unidecode('     Email ' + mv.text))
                        else:
                            print(unidecode('     Email ' + 'Unknown'))
                if 'author_univ' in key.text:
                    for mv in pm.findall('meta_value'):
                        if mv.text:
                            print(unidecode('     Universidad: ' + mv.text))
                        else:
                            print(unidecode('     Universidad: ' + 'Unknown'))
                if 'track' in key.text:
                    for mv in pm.findall('meta_value'):
                        if mv.text:
                            print(unidecode('     Track: ' + mv.text))
                        else:
                            print(unidecode('     Track: ' + 'Unknown'))
                if 'handle' in key.text:
                    for mv in pm.findall('meta_value'):
                        if mv.text:
                            if 'JCIS' in mv.text:
                                conference = mv.text.split('/')[1]
                                edition = mv.text.split('/')[2]
                                print(unidecode('      conferencia: ' + conference))
                                print(unidecode('      edicion: ' + edition))
                                print(unidecode('      handle: ' + mv.text))
                            elif 'JISBD' in mv.text:
                                conference = mv.text.split('/')[1]
                                edition = mv.text.split('/')[2]
                                print(unidecode('      conferencia: ' + conference))
                                print(unidecode('      edicion: ' + edition))
                                print(unidecode('      handle: ' + mv.text))
                            elif 'PROLE' in mv.text:
                                conference = mv.text.split('/')[1]
                                edition = mv.text.split('/')[2]
                                print(unidecode('      conferencia: ' + conference))
                                print(unidecode('      edicion: ' + edition))
                                print(unidecode('      handle: ' + mv.text))
                            else:
                                print(unidecode('      conferencia: ' + 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'))
                        else:
                            print(unidecode('     conferencia: ' + 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'))
        # title = unidecode(item.find('title').text)
        # title = unidecode(item.find('title').text)
        # title = unidecode(item.find('title').text)
        # title = unidecode(item.find('title').text)
