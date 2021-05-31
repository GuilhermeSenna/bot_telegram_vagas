import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', }

URL = 'https://github.com/frontendbr/vagas/issues'

page = requests.get(URL, headers=headers)

soup = BeautifulSoup(page.text, 'html.parser')

# for vaga in soup.findAll('div', attrs={'class', 'js-navigation-container js-active-navigation-container'}):
#     for titulo in vaga.findAll('a', attrs={'class': 'Link--primary v-align-middle no-underline h4 js-navigation-open markdown-title'}):
#         print(titulo.string)
#
#     for tags

tags = []
tags_texto = ''
for vaga in soup.findAll('div', attrs={'class': 'd-flex Box-row--drag-hide position-relative'}):
    tags.clear()
    tags_texto = ''
    link = ''
    tags_texto
    print("-="*20)
    print(f"Título: {vaga.find('a', attrs={'class', 'Link--primary v-align-middle no-underline h4 js-navigation-open markdown-title'}).string}")
    link = vaga.find('a', attrs={'class', 'Link--primary v-align-middle no-underline h4 js-navigation-open markdown-title'})['href']
    tags = vaga.findAll('span', attrs={'class', 'labels lh-default d-block d-md-inline'})
    for tag in tags:
        for text_tag in tag.strings:
            tags_texto += f'{text_tag.strip()} '
        # tags_texto += f'{tag.text} - '
    print(f'Tags: {tags_texto}')
    # print(f'https://www.github.com{link}')

    page = requests.get(f'https://www.github.com{link}', headers=headers)

    soup = BeautifulSoup(page.text, 'html.parser')

    print(soup.find('td', attrs={'class', 'd-block'}).text)





# js-navigation-container js-active-navigation-container

# print(soup.prettify())
