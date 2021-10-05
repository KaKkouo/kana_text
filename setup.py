import sys
from setuptools import setup

sys.path.append('src')
sys.path.append('tests')
import src as kt

setup(
    version = kt.__version__,
    license = kt.__license__,
    author = kt.__author__,
    url = kt.__url__,
    download_url = 'https://pypi.org/project/sphinxcontrib.kana-text/',
    project_urls = {
        'Knowledge': 'https://qiita.com/tags/sphinxcotrib.kana_text',
        'Code': 'https://github.com/KaKkouo/sphinxcontrib.kana_text',
        'Issue tracker': 'https://github.com/KaKkouo/sphinxcontrib.kana_text/issues',
    }
)
