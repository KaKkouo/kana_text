import sys
from setuptools import setup

import src as kt
sys.path.append('tests')

setup(
    version = kt.__version__,
    license = kt.__license__,
    author = kt.__author__,
    url = kt.__url__,
    download_url = 'https://pypi.org/project/sphinxcontrib.kana-text/',
    project_urls = {
        'Knowledge': 'https://qiita.com/tags/sphinxcotrib.kana_text',
        'Code': 'https://github.com/KaKkouo/kana_text',
        'Issue tracker': 'https://github.com/KaKkouo/kana_text/issues',
    }
)
