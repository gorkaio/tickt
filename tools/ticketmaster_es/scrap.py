import requests
import urllib.request
import time
import string
from bs4 import BeautifulSoup

def get_page_shows(soup, status, baseUrl):
  shows = []
  for show in soup.findAll('a', {'class': 'article-list-link'}):
    link = baseUrl + show['href']
    text = show.string.split(" - ")
    show = text[0]
    where = text[1]
    shows.append({'show': show, 'where': where, 'link': link, 'status': status})
  return shows

def to_html(data):
  html = '<table class="table is-striped is-hoverable is-fullwidth">\n'
  html += '<thead><tr><th>Show</th><th>Where</th><th>Status</th><th>Info</th></thead>\n'
  for row in data:
    html += f'\t<tr>\n\t\t<th>{row.get("show")}</th>\n'
    html += f'\t\t<td>{row.get("where")}, Spain</td>\n'
    if (row.get("status") == "Cancelled"):
      html += f'\t\t<td class="has-text-danger">Cancelled</td>\n'
    else:
      html += f'\t\t<td>Changed</td>\n'
    html += f'\t<td><a href="{row.get("link")}">More info</a></td></tr>\n'
  html += '</table>\n'
  return html

def get_shows(baseUrl, changeCategories):
  shows = []
  for root in changeCategories:
    response = requests.get(root.get("link"))
    soup = BeautifulSoup(response.text, "html.parser")
    shows += get_page_shows(soup, root.get("status"), baseUrl)
    next = soup.select('nav.pagination ul li.pagination-next a')

    while len(next) > 0:
      url = baseUrl + next[0]['href']
      response = requests.get(url)
      soup = BeautifulSoup(response.text, "html.parser")
      page_shows = get_page_shows(soup, root.get("status"), baseUrl)
      shows += page_shows
      next = soup.select('nav.pagination ul li.pagination-next a')
      time.sleep(1)
  return shows

baseUrl = 'https://help.ticketmaster.es'
changeCategories = [
  {'status': "Cancelled", 'link': baseUrl + '/hc/es/sections/360001508313-Cancelaciones'},
  {'status': "Changed", 'link': baseUrl + '/hc/es/sections/360001482214-Cambios'}
]

shows = sorted(get_shows(baseUrl, changeCategories), key= lambda i: i['show'])
print(to_html(shows))
