from bs4 import BeautifulSoup


def bs_html_parser(http_response):
    return BeautifulSoup(http_response, 'html.parser')


def exract_comittees_name_and_id(html):
    parser = bs_html_parser(html)
    select = parser.find('select', {'name': 'code_pratiquer'})
    return [(opt.get('value'), opt.text) for opt in select.find_all(
        'option') if opt.get('value') != '']
