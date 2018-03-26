#!/usr/bin/env python3
from urllib import request, error
from bs4 import BeautifulSoup
import csv

popular_plugins = 'https://wordpress.org/plugins/browse/popular/page/{}'
pages = 1000
plugins_file = 'popular-plugins-list.csv'
plugins_dict = {}

def request_html(url):
    req = None
    try:
        req = request.urlopen(url)
    except error.HTTPError as e:
        print('{} - {}'.format(e, url))
    return req

for pageId in range(1, pages):
    url = popular_plugins.format(pageId)
    response = request_html(url)
    if not response:
        break

    parser = BeautifulSoup(response.read(), 'html.parser')
    plugins_list = parser.findAll('h2', {'class': 'entry-title'})

    for element in plugins_list:
        # get plugin name
        plugin_url = element.find('a')['href']
        plugin_name = plugin_url.split('/')[-2]

        # get plugin version
        response = request_html(plugin_url)
        parser = BeautifulSoup(response.read(), 'html.parser')
        version = parser.find('div', {'class': 'widget plugin-meta'}).find('li').find('strong').text
        plugins_dict[plugin_name] = version

# save plugin list on csv file
with open(plugins_file, 'w') as f:
    fields_name = ['name', 'version']
    writer = csv.DictWriter(f, fieldnames=fields_name)
    for name, version in plugins_dict.items():
        writer.writerow({'name': name, 'version': version})