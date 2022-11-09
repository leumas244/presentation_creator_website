import datetime
from bs4 import BeautifulSoup
import requests
import re
import progressbar

from django.core.management.base import BaseCommand
from home.models import WeekMotto
from home.churchtools_connection_package.settings import books, booknames, html_tables_with_weekmottos, ibibles_basic_url


class Command(BaseCommand):
    help = 'Create automatically weekmotto entries with bible passages from html table from https://www.daskirchenjahr.de/tag.php?name=kalender&zeit=&typ=kalender \nand with http://ibibles.net/ for the bible passage'

    def handle(self, *args, **options):
        print('######## START CREATE_WEEKMOTTOS ########')

        # write weekmottos in database
        print('### Getting weekmottos from html_tables')
        amount_of_html_files = len(html_tables_with_weekmottos)
        for html_file in html_tables_with_weekmottos:
            print(f'    html_table {html_tables_with_weekmottos.index(html_file)+1}/{amount_of_html_files}')
            self.create_weekmotto_from_html_table(html_file)
        print('### Finishing weekmottos from html_tables\n')

        print('### Writing API term in weekmotto entries')
        mottos = WeekMotto.objects.filter(motto_api='')
        self.write_api_term_in_db(mottos)
        print('### Finishing API term in weekmotto entries\n')

        print('### Writing long term in weekmotto entries')
        mottos = WeekMotto.objects.filter(motto_long='')
        self.write_motto_long_in_db(mottos)
        print('### Finishing long term in weekmotto entries\n')

        print('### Writing full motto in weekmotto entries')
        mottos = WeekMotto.objects.filter(motto_luther_modern='')
        self.write_full_motto_in_db(mottos)
        print('### Finishing full motto in weekmotto entries')

        print('######## ENDING CREATE_WEEKMOTTOS ########')
    
    def create_weekmotto_from_html_table(self, path_to_html_file):
        source_file = open(path_to_html_file)
        soup = BeautifulSoup(source_file, features="html.parser")
        source_file.close()

        existing_weekmottos = WeekMotto.objects.all()
        created_weekmoot_counter = 0

        rows = soup.findAll('tr')
        row_count = len(rows[1:])

        bar = progressbar.ProgressBar(maxval=row_count, widgets=[progressbar.Bar('=', '        [', ']'), ' ', progressbar.Percentage()])
        bar.start()
        for row in rows[1:]:
            fields = row('td')

            title = fields[0].contents[0]
            year, month, day = self.get_date(fields[1].contents[0])
            date = datetime.date(year, month, day)
            gospels = fields[2].contents[0]
            epistle = fields[3].contents[0]
            old_testament = fields[4].contents[0]
            lecture = fields[5].contents[0]
            motto_short = fields[6].contents[0]
            motto_long = ''
            motto_api = ''

            if title == '2. Sonntag nach Trinitatis' or title == '2. Sonntag nach trinitatis':
                motto_short = 'Mt 11, 28'
            if title == '4. Sonntag nach Trinitatis' or title == '4. Sonntag nach trinitatis':
                motto_short = 'Gal 6, 2'
            if 'Gedenktag der Enthauptung' in title:
                motto_short = 'Ps 116, 15'
            if 'Tag der unschuldigen Kinder' in title:
                motto_short = 'Ps 116, 15'
            if '3. Sonntag im Advent (Gaudete)' in title:
                motto_short = 'Jes 40, 3'

            is_existing = False
            for existing_weekmotto in existing_weekmottos:
                if existing_weekmotto.title == title and existing_weekmotto.date == date:
                    is_existing = True
                    break

            if not is_existing:
                try:
                    week_motto = WeekMotto(title=title, date=date, gospels=gospels, epistle=epistle,
                                        old_testament=old_testament, lecture=lecture, motto_short=motto_short,
                                        motto_long=motto_long, motto_api=motto_api)
                    week_motto.save()
                    created_weekmoot_counter += 1
                except Exception as e:
                    print(f'        Error by create_weekmotto_from_html_table with error: "{str(e)}"')
            
            counter = rows.index(row)
            bar.update(counter)
        bar.finish()
        print(f'        Created {created_weekmoot_counter} WeekMottos')

    def get_date(self, date_field):
        date_helper_list = date_field.split('(')
        date_helper = date_helper_list[0].replace(' ', '')
        date_list = date_helper.split('.')
        year = int(date_list[2])
        month = int(date_list[1])
        day = int(date_list[0])
        return year, month, day


    def write_full_motto_in_db(self, mottos):
        counter = 0
        motto_count = len(mottos)
        print(f'    WeekMottos to edit: {motto_count}')

        bar = progressbar.ProgressBar(maxval=motto_count, widgets=[progressbar.Bar('=', '    [', ']'), ' ', progressbar.Percentage()])
        bar.start()

        for motto in mottos:
            counter += 1
            try:
                verses = self.get_verses_from_sreach_term(motto.motto_api)
                my_motto_luther_modern = ''
                for vers in verses:
                    my_motto_luther_modern = verses[vers] + ' '
                motto.motto_luther_modern = my_motto_luther_modern + '\n' + motto.motto_long
                motto.save()
                bar.update(counter)
            except Exception as e:
                print(f'    Error by write_full_motto_in_db by ID:{motto.id} with error: "{str(e)}"')
                bar.update(counter)
                continue
            
        bar.finish()


    def write_api_term_in_db(self, mottos):
        counter = 0
        motto_count = len(mottos)
        print(f'    WeekMottos to edit: {motto_count}')

        bar = progressbar.ProgressBar(maxval=motto_count, widgets=[progressbar.Bar('=', '    [', ']'), ' ', progressbar.Percentage()])
        bar.start()

        for motto in mottos:
            counter += 1
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
                bar.update(counter)
            except Exception as e:
                print(f'    Error by write_api_term_in_db by ID:{motto.id} with error: "{str(e)}"')
                bar.update(counter)
                continue
        bar.finish()


    def write_motto_long_in_db(self, mottos):
        counter = 0
        motto_count = len(mottos)
        print(f'    WeekMottos to edit: {motto_count}')

        bar = progressbar.ProgressBar(maxval=motto_count, widgets=[progressbar.Bar('=', '    [', ']'), ' ', progressbar.Percentage()])
        bar.start()

        for motto in mottos:
            counter += 1
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
                
                long_term = self.get_long_term(book, chapter, vers)

                motto.motto_long = long_term
                motto.save()
                bar.update(counter)
            except Exception as e:
                print(f'    Error by write_api_term_in_db by ID:{motto.id} with error: "{str(e)}"')
                bar.update(counter)
                continue
        bar.finish()
    

    def get_search_term(self, book, chapter, vers_begin, vers_end=0, uebersetzung='glm'):
        book_api = 'No Book set'
        for bookname in books:
            if book in bookname:
                book_api = books[bookname]
                break

        if book_api == 'No Book set':
            return 'No Book found'

        if vers_end == 0:
            search_term = uebersetzung + '-' + book_api + '/' + str(chapter) + ':' + str(vers_begin)
        else:
            search_term = uebersetzung + '-' + book_api + '/' + str(chapter) + ':' + str(vers_begin) + '-' + str(vers_end)

        return search_term

    
    def get_long_term(self, book, chapter, vers):
        long_bookname = 'No Book set'
        for bookname in booknames:
            if book in bookname:
                long_bookname = booknames[bookname]
                break

        if long_bookname == 'No Book set':
            return 'No Book found'

        long_term = f'{long_bookname} {chapter}, {vers}'

        return long_term
    
    

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
        response = requests.get(ibibles_basic_url + search_term)

        verses = self.get_verses_from_response(response)

        return verses
