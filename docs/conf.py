# Configuration file for the Sphinx documentation builder.

import os
import sys
import django

sys.path.insert(0, os.path.abspath('..'))  # This adds the /app directory to Python path

os.environ['DJANGO_SETTINGS_MODULE'] = 'cms.settings'
django.setup()


from unittest.mock import Mock
sys.modules['django.views.decorators.http'] = Mock()


project = 'CMS'
copyright = '2023, Grupo6'
author = 'Grupo6'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon'
]
autodoc_default_options = {
    'members': True,
    'private-members': True,
    'show-inheritance': True,
    'exclude-members': 'DoesNotExist, MultipleObjectsReturned, _meta, get_next_by_fecha_cambio, get_previous_by_fecha_cambio, objects'
}

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'es'

html_theme = 'sphinx_rtd_theme'
#html_static_path = ['_static']

