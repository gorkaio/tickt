import requests
import urllib.request
import time
import string
from bs4 import BeautifulSoup

baseUrl = 'https://help.ticketmaster.es'

def get_page_shows(soup):
  shows = []
  for show in soup.findAll('a', {'class': 'article-list-link'}):
    link = baseUrl + show['href']
    text = show.string.split(" - ")
    show = text[0]
    where = text[1]
    shows.append({'show': show, 'where': where, 'link': link})
  return shows

def toHtml(data):
  html = '<table class="table is-striped is-hoverable">\n'
  for row in data:
    html += f'\t<tr>\n\t\t<th>{row.get("show")}</th>\n\t\t<td><a href="{row.get("link")}">{row.get("where")}, Spain</a></td>\n\t</tr>\n'
  html += '</table>\n'
  return html

url = baseUrl + '/hc/es/sections/360001508313-Cancelaciones'
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

shows = get_page_shows(soup)
next = soup.select('nav.pagination ul li.pagination-next a')
while len(next) > 0:
  url = baseUrl + next[0]['href']
  response = requests.get(url)
  soup = BeautifulSoup(response.text, "html.parser")
  page_shows = get_page_shows(soup)
  shows += page_shows
  next = soup.select('nav.pagination ul li.pagination-next a')
  time.sleep(1)

print(toHtml(shows))
