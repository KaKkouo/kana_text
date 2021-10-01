extends the functionality of the Text class. any person, who use index/glossary directives with Japanse Kanji, is to be so happy.

.. image:: https://i.gyazo.com/4cbf3408c162fb2bfcc493661d35a42b.png

conf.py
-------

First of all, add **sphinxcontrib-kana_text** to sphinx extension list in conf.py

.. code-block:: python

   extensions = ['sphinxcontrib.kana_text']

.. code-block:: python

   #html_kana_text_on_genindex = False
   #html_kana_text_use_own_indexer = 'large'

.. warning::

   You need 'genindex.html' for taking True on html_kana_text_on_genindex.

rst file
--------

then use **index** directive, **glossary** directive, **index** role and **kana** role.

You can specify the follwings:

.. code-block:: rst

   .. index:: ようご|用語^21

.. code-block:: rst

   .. glossary::

      ようごいち|用語壱^212
        用語１の説明。

And you can also use index/kana role. 

.. code-block:: rst

   夜空に浮かぶ\ :index:`あまた|数多^21`\ の星々が\ :kana:`きらめいて|煌めいて^2c`\ いる。

build
-----

finally, build your sphinx project:

.. code-block:: sh

   $ make kana

take a look at genindex.html.

genindex.html
-------------

.. code-block:: sh

   $ sphinx-kana-genindex
   $ mv genindex.html.sample path_to_sphinx_project/_templates/genindex.html

