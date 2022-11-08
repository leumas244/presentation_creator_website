import datetime
from bs4 import BeautifulSoup
import requests
import re

from django.core.management.base import BaseCommand
from home.models import WeekMotto


class Command(BaseCommand):
    help = 'Create automatically calender entries with bible passages'

    def handle(self, *args, **options):
        self.books = {'Genesis': 'ge',
                '1. Mose': 'ge',
                'Exodus': 'exo',
                '2. Mose': 'exo',
                'Levitikus': 'lev',
                '3.Mose': 'lev',
                'Numeri': 'num',
                '4. Mose': 'num',
                'Deuteronomium': 'deu',
                '5. Mose': 'deu',
                'Josua': 'josh',
                'Richter': 'jdgs',
                'Ruth': 'ruth',
                '1. Samuel': '1sm',
                '2. Samuel': '2sm',
                '1. Könige': '1ki',
                '2. Könige': '2ki',
                '1. Chronik': '1chr',
                '2. Chronik': '2chr',
                'Esra': 'ezra',
                'Nehemia': 'neh',
                'Ester': 'est',
                'Hiob': 'job',
                'Psalm': 'psa',
                'Sprüche': 'prv',
                'Prediger': 'eccl',
                'Hohelied': 'ssol',
                'Jesaja': 'isa',
                'Jeremia': 'jer',
                'Klagelieder': 'lam',
                'Hesekiel': 'eze',
                'Daniel': 'dan',
                'Hosea': 'hos',
                'Joel': 'joel',
                'Amos': 'amos',
                'Obadja': 'obad',
                'Jona': 'jonah',
                'Micha': 'mic',
                'Nahum': 'nahum',
                'Habakuk': 'hab',
                'Zefanja': 'zep',
                'Haggai': 'hag',
                'Sacharja': 'zec',
                'Maleachi': 'mal',
                'Matthäus': 'mat',
                'Mt': 'mat',
                'Markus': 'mark',
                'Mk': 'mark',
                'Lukas': 'luke',
                'Lk': 'luke',
                'Johannes': 'john',
                'Apostelgeschichte': 'acts',
                'Apg': 'acts',
                'Römer': 'rom',
                '1. Korinther': '1cor',
                '2. Korinther': '2cor',
                'Galater': 'gal',
                'Epheser': 'eph',
                'Philipper': 'phi',
                'Kolosser': 'col',
                '1. Thessalonicher': '1th',
                '2. Thessalonicher': '2th',
                '1. Timotheus': '1tim',
                '2. Timotheus': '2tim',
                'Titus': 'titus',
                'Philemon': 'phmn',
                'Hebräer': 'heb',
                'Jakobus': 'jas',
                '1. Petrus': '1pet',
                '2. Petrus': '2pet',
                '1. Johannes': '1jn',
                '2. Johannes': '2jn',
                '3. Johannes': '3jn',
                'Judas': 'jude',
                'Offenbarung': 'rev',
                'Offb': 'rev',
                }
        
        self.basic_url = 'http://ibibles.net/quote.php?'
        mottos = WeekMotto.objects.filter(motto_api='')

        self.write_api_term_in_db(mottos)

        mottos = WeekMotto.objects.filter(motto_luther_modern='')
        self.write_full_motto_in_db(mottos)

        
    def write_full_motto_in_db(self, mottos):
        counter = 0
        motto_count = len(mottos)

        for motto in mottos:
            counter += 1
            percent = round((counter/motto_count)*100, 1)
            try:
                verses = self.get_verses_from_sreach_term(motto.motto_api)
                my_motto_luther_modern = ''
                for vers in verses:
                    my_motto_luther_modern = verses[vers] + ' '
                motto.motto_luther_modern = my_motto_luther_modern + '\n' + motto.motto_short
                motto.save()
                print('[' + str(percent) + '%]' + str(motto.id) + '  Good')
            except:
                print('[' + str(percent) + '%]' + str(motto.id) + '  PROBLEM BY FULL-MOTTO!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')


    def write_api_term_in_db(self, mottos):
        counter = 0
        motto_count = len(mottos)

        for motto in mottos:
            counter += 1
            percent = round((counter/motto_count)*100, 1)
            print('[' + str(percent) + '%]  ')
            try:
                weekmotto_short = motto.motto_short
                
                #weekmotto_short = re.sub(r'\(?\)', '', weekmotto_short)
                weekmotto_short_split = weekmotto_short.split(' ')
                if re.search(r'^[0-999].', weekmotto_short):
                    book = weekmotto_short_split[0] + ' ' + weekmotto_short_split[1]
                    chapter = weekmotto_short_split[2].replace(',', '')
                    vers = weekmotto_short_split[3]
                else:
                    book = weekmotto_short_split[0]
                    chapter = weekmotto_short_split[1].replace(',', '')
                    vers = weekmotto_short_split[2]
                
                search_term = self.get_search_term(book, chapter, vers)

                motto.motto_api = search_term
                motto.save()
                print('[' + str(percent) + '%]' + str(motto.id) + '  Good')
            except:
                print('[' + str(percent) + '%]' + str(motto.id) + '  PROBLEM BY API-TERM!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                continue
    

    def get_search_term(self, book, chapter, vers_begin, vers_end=0, uebersetzung='glm'):
        book_api = 'No Book set'
        for bookname in self.books:
            if book in bookname:
                book_api = self.books[bookname]
                break

        if book_api == 'No Book set':
            return 'No Book found'

        if vers_end == 0:
            search_term = uebersetzung + '-' + book_api + '/' + str(chapter) + ':' + str(vers_begin)
        else:
            search_term = uebersetzung + '-' + book_api + '/' + str(chapter) + ':' + str(vers_begin) + '-' + str(vers_end)

        return search_term
    

    def get_verses_from_response(self, response):
        text_without_header = str(response.text).replace(
            '<!doctype html>\n<html>\n<head>\n<meta http-equiv="content-type" content="text/html;charset=utf-8"/>\n<title>Bible Quote</title>\n</head>\n<body bgcolor="#e0e0e0">',
            "")
        text_without_header_and_footer = text_without_header.replace('</body>\n</html>', "")
        if text_without_header_and_footer != '\nBible book not found.<br>\n\n' or text_without_header_and_footer != '\nBible verse not found.<br>\n\n':
            text_without_header_and_footer = text_without_header_and_footer.replace('<br>\r\n', '')
            text_without_header_and_footer = text_without_header_and_footer.replace('\n', '')
            list = text_without_header_and_footer.split('</small> ')
            new_list = []
            verses = {}
            for entry in list:
                if '<small>' in entry:
                    my_split = entry.split('<small>')
                    for s in my_split:
                        if s != '':
                            new_list.append(s)
                else:
                    new_list.append(entry)

            if len(new_list) != 1:
                index = 0
                while (index + 1) < len(new_list):
                    vers = new_list[index].replace('<small>', '')
                    content = new_list[index + 1].replace('<br>\r\n\n', '')
                    verses[vers] = content

                    index = index + 2
                return verses
            else:
                return "Book not found from ibibles"
        else:
            return "Book not found from ibibles"


    def get_verses_from_sreach_term(self, search_term):
        response = requests.get(self.basic_url + search_term)

        verses = self.get_verses_from_response(response)

        return verses