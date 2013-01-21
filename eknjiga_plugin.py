# -*- coding: utf-8 -*-

from __future__ import (unicode_literals, division, absolute_import, print_function)

__license__ = 'GPL 3'
__copyright__ = '2012, Matej Batic, matej.batic@ijs.si'
__docformat__ = 'restructuredtext en'

from contextlib import closing

#from bs4 import BeautifulSoup

import re
import urllib2
from PyQt4.Qt import QUrl

from lxml import html, etree

from calibre import browser, url_slash_cleaner
from calibre.gui2 import open_url
from calibre.gui2.store import StorePlugin
from calibre.gui2.store.basic_config import BasicStoreConfig
from calibre.gui2.store.search_result import SearchResult
from calibre.gui2.store.web_store_dialog import WebStoreDialog

class EknjigaStore(BasicStoreConfig, StorePlugin):

    def open(self, parent=None, detail_item=None, external=False):
        url = 'http://www.e-knjiga.si'

        if external or self.config.get('open_external', False):
            open_url(QUrl(url_slash_cleaner(detail_item if detail_item else url)))
        else:
            d = WebStoreDialog(self.gui, url, parent, detail_item)
            d.setWindowTitle(self.name)
            d.set_tags(self.config.get('tags', ''))
            d.exec_()
            
    def search(self, query, max_results=100, timeout=180):
        url = 'http://www.e-knjiga.si/rezultati_cover.php?query=' + urllib2.quote(query)

        print("will search for: " + urllib2.quote(query) + ":\n  " + url)

        br = browser()

        # counter = max_results
        with closing(br.open(url, timeout=timeout)) as f:

            html=etree.HTML(f.read())
            
            #get list of books
            for book in html.xpath("//table[@class='zebra']"):
                print(etree.tostring(book, pretty_print=True, method="html"))
        
                author = book.find('.//tr/[0]/td/[1]').text
                title = book.find('.//tr/[0]/td/[2]/a').text
                details = 'http://www.e-knjiga.si/' + book.find('.//tr/[0]/td/[2]/a').get("href")

                ## get details
                fo =  urllib2.urlopen(details)
                det=etree.HTML(fo.read())
                fo.close()
                
                table=det.find(".//div[@id='center_container']").find('./table')
                cover='http://www.e-knjiga.si/' + table.find('.//tr/[1]/td/[1]/div/img').get("src")
                description=table.find(".//tr/[6]/td[@class='knjige_spremna']").text
                
                links=[]
                files=table.find('.//tr/[7]/td/[1]')
                for file in files.iter('a'):
                    links.append("http://www.e-knjiga.si/"+file.get("href"))

                
                #print("Author:    " + author)
                #print("Title:     " + title)
                #print("Details:   " + details)
                #print("Description:  " + description)
                #print("Cover:        " + cover)
                #print("Files:       ")
                #print('\n              '.join(links))
                
                s = SearchResult()
                s.title = title
                s.author = author
                s.price = "0.00eur"
                s.drm = SearchResult.DRM_UNLOCKED
                s.detail_item = description
                
                for f in links:
                    ftype = f.split(".")[-1]
                    s.downloads[ftype] = f
                    s.formats += ftype
                    
                s.cover_url = cover

                yield s

            
            

                        
