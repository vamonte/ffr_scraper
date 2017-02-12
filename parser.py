import re
from bs4 import BeautifulSoup


def bs_html_parser(http_response):
    return BeautifulSoup(http_response, 'html.parser')


def extract_comittees_name_and_id(html):
    parser = bs_html_parser(html)
    select = parser.find('select', {'name': 'code_pratiquer'})
    return [(opt.get('value'), opt.text) for opt in select.find_all(
        'option') if opt.get('value') != '']


def clean_string(value):
    return value.replace(u'\xa0', ' ').replace('\u00a0', ' ').strip().lower()


def get_row_data(row):
    try:
        key_td, value_td = row.find_all('td', {'valign': 'top'})
    except ValueError:
        pass
    else:
        key, value = None, None
        try:
            key = key_td.get_text().split(':')[0]
        except IndexError:
            key = key_td.get_text()
        finally:
            if key:
                try:
                    link = value_td.find_all('a')[0]
                except (IndexError, TypeError):
                    value = value_td.get_text()
                else:
                    value = link.get('href').replace('mailto:', '')
                finally:
                    return key, value


def extract_generic_detail(html, get_rows, end_condition=None, parser=None):
    parser = parser or bs_html_parser(html)
    rows = get_rows(parser)
    data = {}
    for row in rows:
        if end_condition and end_condition(row):
            break
        try:
            key, value = get_row_data(row)
        except TypeError:
            pass
        else:
            data[clean_string(key)] = clean_string(value)
    return data


def get_committee_rows(parser):
    try:
        table = parser.find_all('table', {'class': 'text_ffr_gris'})[1]
    except IndexError:
        raise Exception('The committee details display has changed.')
    else:
        return table.find_all('tr')


def extract_committee_detail(html, committee_id, cookie):
    parser = bs_html_parser(html)
    committee_detail = extract_generic_detail(html, get_committee_rows,
                                              parser=parser)

    clubs_select = parser.find('select', {'name': 'ID_CLUB'})
    clubs = [(committee_id, club.text, club.get('value'), cookie) for club
             in clubs_select.find_all('option') if club.get('value') != 'vide']

    return committee_detail, clubs


def get_club_rows(parser):
    club_menu = parser.find('ul', id='menu')
    return club_menu.find_all('tr')[1:]


def club_details_end_condition(row):
    return row.get('style') == 'font-weight:bold;'


def extract_club_city_name_and_ffr_id(title):
    ffr_id = ''
    title_splited = re.split('\(\w{5}\)', title)
    city, name = title_splited[0].split(' - ', 1)
    try:
        ffr_id = re.search('\((.*?)\)', title).groups()[0]
    except (IndexError, AttributeError):
        ffr_id = ''
    finally:
        return city.strip(), name.strip(), ffr_id


def extract_club_detail(html, title):
    club_detail = extract_generic_detail(html, get_club_rows,
                                         club_details_end_condition)
    city, name, ffr_id = extract_club_city_name_and_ffr_id(title)
    club_detail['nom'] = name
    club_detail['ville'] = city
    return {ffr_id: club_detail}
