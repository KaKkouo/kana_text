This is a sphinx extention. It extends the functionality of the Text class. Any person, who uses index/glossary directives with Japanse Kanji, is to be so happy.

.. image:: https://i.gyazo.com/4cbf3408c162fb2bfcc493661d35a42b.png

If word_list.txt is used by kana_text_word_file parameter, the genindex.html is created without editing rst files.

QUICK START
-----------

conf.py:

.. code-block:: python

   extensions = ['sphinxcontrib.kana_text']

.. code-block:: python

   #kana_text_word_file = '~/.config/sphinx/word_list.txt'
   #kana_text_word_list = ['ようご|用語^21', 'ぶんしょさくせい|文書作成^2222',]
   #kana_text_indexer_mode = 'small'
   #html_kana_text_on_genindex = False

.. warning::

   - 'word_list.txt' is required for kana_text_word_file
   - 'genindex.html' is required for html_kana_text_on_genindex = True.
   - both parameters are valid only against genindex.html.

rst file:

.. code-block:: rst

   .. index:: ようご|用語^21

.. code-block:: rst

   .. glossary::

      ようごいち|用語壱^212
        用語１の説明。

.. code-block:: rst

   夜空に浮かぶ\ :index:`あまた|数多^21`\ の星々が\ :kana:`きらめいて|煌めいて^2c`\ いる。

.. image:: https://i.gyazo.com/63fe4ccfaa8a57bb2d8db50c0a689cad.png

build:

.. code-block:: sh

   $ make kana

genindex.html
-------------

.. code-block:: sh

   $ sphinx-kana-genindex
   $ mv genindex.html.sample path_to_sphinx_project/_templates/genindex.html
