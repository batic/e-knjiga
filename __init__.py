# -*- coding: utf-8 -*-

from __future__ import (unicode_literals, division, absolute_import, print_function)

__license__ = 'GPL 3'
__copyright__ = '2012, Matej Batic, matej.batic@ijs.si'
__docformat__ = 'restructuredtext en'

from calibre.customize import StoreBase

class LibgenStore(StoreBase):
    name = 'e-knjiga library plugin'
    description = 'Plugin to download books in slovene from e-knjiga.si'
    author = 'Matej Batic'
    version = (1, 0, 0)
    drm_free_only = True
    formats = ['EPUB', 'PDF', 'MOBI']
    actual_plugin = 'calibre_plugins.store_eknjiga.eknjiga_plugin:EknjigaStore'
