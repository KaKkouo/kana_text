"""
sphinxcontrib.kana_text
=======================
参考情報
--------
- https://www.sphinx-doc.org/ja/master/usage/restructuredtext/basics.html
- https://www.sphinx-doc.org/ja/master/development/tutorials/helloworld.html

機能
====
文字列を「かな|単語」という書式で記載することで、「かな」に応じた表示順となる。
表示の時は「かな」を非表示、もしくはルビ表示にする.

対象
----
- indexディレクティブ、glossaryディレクティブ
- indexロール（索引での表示）、kanaロール（読み仮名のみ）.

「かな|単語^オプション」と書く以外の使い方はこれまでと同じ.

使い方
------
次のように「かな|」を文字列の前方に付記する

.. code-block:: rst

   .. glossary::

      ひ|微分
        距離の関数から速度の関数、速度の関数から加速度の関数を導く

      せ|積分
        加速度の関数から速度の関数、速度の関数から距離の関数を導く

      たなかはなこ|田中はな子^12aa1
        読み仮名の表示の確認のサンプル

   .. index::
      pair: かなの表示; き|記載方法

   例えば、 「たなかはなこ:田中はな子^12b1」 と書くと、索引に記載される。

   例えば、 :index:`たなかはなこ|田中はな子^12b1` と書くと、索引に記載される。

   ロールでは、 :index:`!たなかはなこ|田中はな子^12b1` と書くと、項目の上位に表示される。

   更に、 :index:`たなかはなこ|田中はな子^12qq1<pair: し|架空の小説; て|お試し>` と書くこともできる。

   索引に表示しないのなら、 :kana:`たなかはなこ|田中はな子^12aa1` と書く。

読み仮名の表示の調整
--------------------
ルビの表示を細かく指定したい場合に使う

- 「かな|単語^オプション」とする
- 「^」以降はソート処理では無視される

指定方法

- 「かな|単語^」は読み仮名の表示。「^」がないと非表示
- 「かな|単語^2312」と数字が続く場合は、単語の各１文字に当てる読みの数
- 「かな|単語^2a1b」とアルファベットがある場合は、ルビ表示に使わない
- 「かな|単語^201」とゼロがある場合は、単語のその１文字の割当をスキップする
- 読み仮名の部分的非表示は「a-i」「q-y」の２種類で対応

適切に設定していない場合

- 文字数以上の指定があった場合は可能な範囲で処理される
- 指定が不足している場合はルビは表示しない

パラメータ
----------
kana_text_separator

- 「かな|単語」の区切りを指定する.
- 省略時は「r'\|'」. 

kana_text_option_marker

- 「かな|単語^22」の「^」を指定する。
- 省略時は「r'\^'」. 

html_kana_text_on_genindex

- 索引ページでのかな表示を有効にする.
- 省略時は非表示. 推奨はTrue.
- これに対応した「genidex.html」が必要.

html_change_triple

- tripleでの「3rd, 1st」の表示を「1st, 3rd」に変更する.
- 省略時はFalse.

html_kana_text_use_own_indexer

- Sphinxのインデクサーでなく、Sphinx拡張が提供するインデクサーを行う.
- パラーメターの値と挙動

    - False:  IndexEntriesクラスを使用.
    - 'small': KanaIndexerクラスを使用. ex.「モジュール」は「ま」の項目.
    - 'large': KanaIndexerクラスを使用. ex.「モジュール」は「も」の項目.
    - その他:  KanaIndexerクラスを使用. ex.「モジュール」は「モ」のまま.

- 省略時は`small`. 索引に載る言葉が少ないうちは'small'を推奨.

debug_kana_text_genindex_entries

- デバッグ用.

genindex.htmlの作り方
---------------------

1. sphinx/themes/basic/genindex.html をプロジェクトの「_templates」にコピーする.
2. 「{{ firstname|e }}」を次のように変更し、続けて同ファイルに「macro」を記述する.

.. code-block:: jinja

    {{ kana_entry(firstname) }}

.. code-block:: jinja

    {% macro kana_entry(kname) %}
    {%- if kname is string -%}
      {{ kname|e }}
    {%- else %}
      {%- for isruby, val in kname -%}
      {%- if isruby -%}
        <ruby><rb>{{ val[0]|e }}</rb><rp>（</rp>
        <rt>{{ val[1]|e }}</rt><rp>）<rp>
        </ruby>
      {%- else %}
        {{ val|e }}
      {%- endif %}
      {%- endfor %}
    {%- endif %}
    {% endmacro %}

開発者向け
==========
変数名
------
- KanaText内. 未処理は「text」で解析済みは「kana/word」.
- index/glossaryとしては「kana/term」.
- 文言もこれに合わせる.

データの優先順
-------------- 
早い者勝ちv.s.上書き許容（インデクシング）

- できる限り「entriesへの登録順に依存しない」を目指し、解消できない部分は「早い者勝ち」とする.
- 「make clean」後の「make kana」で安定する挙動として.
- 恐らくstd.pyでの登録データの方が、index.pyの登録データより処理が先.

実装においての要点
------------------ 
KanaTextクラス

- かな表示を可能にする.
- 「.. index::」「..glossary::」「:index:」「:kana:」で使用.

visit_kana/depart_kanaメソッド

- add_node()により、KanaTextクラスに紐付けてKanaHTMLBuilderクラスに登録される.
- glossaryで記載したテキストは、 **visit_term()** メソッドでKanaTextクラスにする.

    - 本来の調整場所はGlossaryクラスだが、コード量の少ないvisit_termメソッドを選択.

KanaHTML5Translatorクラス/visit_termメソッド

- 目的のTextノードをKanaTextノードに変更する.

    - visit_termメソッドはglossaryで定義された単語（termクラス）が通る.

KanaIndexerクラス/create_geindex_entriesメソッド

- IndexEntriesクラス/create_indexメソッドを置き換える.
- sortkeyを作って「[sortkey, databody]」のリストを作るところが肝.
- 「早い者勝ちv.s.上書き許容」の件.
- オリジナルは「func() (クラス名やモジュール名)」の集約処理が説明した通りではない.
- 「see/seealso」の表示順がオリジナルと異なる.

KanaHTMLBuilderクラス/create_genindexメソッド

- 索引ページの表示、ソート処理前の「^オプション」の削除を行う.

備忘録
======
Glossaryの検討
--------------
Glossary側でKanaTextノード作る場合、termクラス→TextElementクラスまで遡って手を入れる必要がある.

- TextElementクラス内でTextクラスでのオブジェクト化があるため、他の場所でKanaTextクラスにしても上書きされる.

Glossary内でtermノードを作った後に置き換える方法

- 現状のvisit_termメソッドで置き換える方法とは、入れ替えるタイミングの違いのみ.
- Glossaryでの改良は変更するコード量に対して影響範囲が大きい.
- KanaHTMLTranslatorなら設定で挙動を制御できる.

latexやerubへの対応
-------------------
KanaTextクラス/astextメソッド

- 現在はソート処理に使う文字列と、html表示用の文字列が用意されている.
- これに対して、latex/erub用の文字列を作るように実装.

visit_xxx/depart_xxxメソッド

- latex/erub用のメソッドをそれぞれ用意する.

latexでの索引ページ
-------------------
実装の可能性

- 索引ページから対応するドキュメントへのジャンプする機能があれば、原理的には対応可能.

latexの関連情報

- `TeX Wiki 索引作成 <https://texwiki.texjp.org/?%E7%B4%A2%E5%BC%95%E4%BD%9C%E6%88%90>`_
- `TeX Wiki 相互参照 <https://texwiki.texjp.org/?LaTeX%E5%85%A5%E9%96%80%2F%E7%9B%B8%E4%BA%92%E5%8F%82%E7%85%A7%E3%81%A8%E3%83%AA%E3%83%B3%E3%82%AF>`_

各クラス、メソッド
==================
"""

__copyright__ = 'Copyright (C) 2021 @koKkekoh'
__license__ = 'BSD 2-Clause License'
__author__  = '@koKekkoh'
__version__ = '0.22.0.dev20'
__url__     = 'https://qiita.com/tags/sphinxcotrib.kana_text'

import re, pprint
from typing import TYPE_CHECKING, Any, Dict, List, Tuple, Pattern, Type, cast

from docutils import nodes
from docutils.nodes import Node, Text, Element, system_message

from sphinx import addnodes
import sphinx.builders.html as builders
from sphinx.config import Config
from sphinx.domains.index import IndexDomain, IndexRole
from sphinx.domains.std import Glossary
from sphinx.errors import NoUri
from sphinx.environment.adapters.indexentries import IndexEntries
from sphinx.locale import _, __
from sphinx.util import logging, split_into
from sphinx.util.nodes import process_index_entry
from sphinx.writers import html5

pretty = pprint.pprint

logger = logging.getLogger(__name__)

#------------------------------------------------------------

_chop = re.compile(r'^\\')

_dflt_separator = r'\|'
_dflt_option_marker = r'\^'

def parser_for_kana_text(separator, option_marker):
    """「かな|単語^オプション」を取り出す正規表現を作る.

    :param separator: 「かな」と「単語」を分ける文字の指定.
    :type separator: str
    :param option_marker: 「^オプション」の開始文字の指定.
    :type option_marker: str
    :return: 「かな|単語^オプション」を取り出す正規表現.
    :rtype: 正規表現.

    doctest::

       >>> parser_for_kana_text(r'\|', r'\^')
       re.compile('([ \\u3000]*)((.*?)\\\\|)*([^\\\\^]*)((\\\\^)([0-9a-z]*)?)?')
    """

    ahead = r'([ 　]*)'
    kana_parts = (r'((.*?)', r')*')
    word_parts = (r'([^', r']*)')
    mark_parts = (r'((', r')([0-9a-z]*)?)?')

    re_kana = kana_parts[0] + separator + kana_parts[1]
    re_word = word_parts[0] + option_marker + word_parts[1]
    re_mark = mark_parts[0] + option_marker + mark_parts[1]

    return re.compile(ahead + re_kana + re_word + re_mark)

#オプションに「a-z」があるか
_a2z = re.compile(r'[a-z]')

#「かな|単語^オプション」のオプションの変換用
_s2i_each_together = {
    'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5,
    'f': 6, 'g': 7, 'h': 8, 'i': 9
    }

_s2i_step_by_step = {
    'q': 1, 'r': 2, 's': 3, 't': 4, 'u': 5,
    'v': 6, 'w': 7, 'x': 8, 'y': 9
    }

def make_html_with_ruby(word: str, kana: str) -> str:
    """ルビ表示用の文字列を作成

    :param word: 単語
    :type word: str
    :param kana: かな
    :type kana: str
    :param purpose: 表示目的. 現状は 'html' のみ.
    :type purpose: str
    :return: 表示用の文字列
    :rtype: str

    doctest::

        >>> make_html_with_ruby("単語","たんご")
        '<ruby><rb>単語</rb><rp>（</rp><rt>たんご</rt><rp>）</rp></ruby>'
    """

    rb = f'<rb>{word}</rb>' #単語
    rt = f'<rt>{kana}</rt>' #かな
    rp = ('<rp>（</rp>', '<rp>）</rp>')

    return f'<ruby>{rb}{rp[0]}{rt}{rp[1]}</ruby>'

def get_specific_by_parsing_option(word, kana, option):
    rtn, opt, t_s, t_end, r_s, r_end = [], list(option), 0, 0, 0, 0
    for o in opt:
        if not word[t_s:] or not kana[r_s:]: #文字がない
            break
        elif o in _s2i_each_together: #ルビとしては使用しない
            t_end = t_s + _s2i_each_together[o]
            r_end = r_s + _s2i_each_together[o]
            rtn.append((False,word[t_s:t_end]))
        elif o in _s2i_step_by_step: #ルビとしては使用しない
            t_end = t_s + 1
            r_end = r_s + _s2i_step_by_step[o]
            rtn.append((False,word[t_s:t_end]))
        elif _a2z.match(o): #上記以外の文字は無視する
            continue
        elif o == '0': #'0'の時はかなを消費せずに、１文字処理する
            t_end = t_s + 1
            rtn.append((False,word[t_s:t_end]))
        else: #ルビとして表示する
            t_end = t_s + 1
            r_end = r_s + int(o)
            rtn.append((True, (word[t_s:t_end], kana[r_s:r_end])))

        #次のループに入る前に位置情報を更新
        t_s, r_s = t_end, r_end

    if word[t_end:]: #オプションが尽きた
            rtn.append((False,word[t_end:]))

    return rtn

class KanaText(nodes.Text):

    def __init__(self, rawtext, separator=_dflt_separator, option_marker=_dflt_option_marker):
        """
        doctest:

            >>> kana = KanaText('はなこ|はな子^b1')
            >>> kana
            <KanaText: ruby='specific' option='b1' <#text: 'はなこ|はな子'>>
        """

        self._rawtext = rawtext
        self._delimiter = _chop.sub('', separator)
        self._separator = separator
        self._option_marker = option_marker

        parser = parser_for_kana_text(separator, option_marker)
        word, kana, ruby, option = self._parse_text(rawtext.strip(), parser)

        self._properties = {'word': word, 'kana': kana, 'ruby': ruby, 'option': option,
                            'null': not word, 'separator':  self._delimiter, }

        if kana:
            d = self._delimiter
            super().__init__(kana+d+word, kana+d+word)
        else:
            super().__init__(word, word)

    def __len__(self):
        if self['kana']: return 2
        if self['word']: return 1
        return 0

    def length(self):
        #return len(self['kana']) + len(self['separator'] + len(self['word'])
        pass

    def __getitem__(self, key):
        if isinstance(key, str):
            return self._properties[key]
        elif isinstance(key, int):
            if key == 0: return self._properties['word']
            if key == 1: return self._properties['kana']
            raise KeyError(key)
        else:
            raise TypeError(key)

    def __setitem__(self, key, value):
        if isinstance(key, int):
            if key == 1:
                self._properties['kana'] = value
            else:
                raise KeyError(key)
        else:
            raise TypeError(key)

    def __repr__(self):
        return self.entity_of_repr()

    def entity_of_repr(self):
        """
        doctest:
            >>> kana = KanaText('はなこ|はな子^b1')
            >>> kana
            <KanaText: ruby='specific' option='b1' <#text: 'はなこ|はな子'>>
        """
        name = self.__class__.__name__
        rb, op = self['ruby'], self['option']
        word, kana = self[0], self[1]
        if kana:
            prop = f"<{name}: "
            if len(rb) > 0: prop += f"ruby='{rb}' "
            if len(op) > 0: prop += f"option='{op}' "
            prop += f"<#text: '{kana}|{word}'>>"

            return prop
        elif word:
            return f"<{name}: <#text: '{word}'>>"
        elif self.rawsource:
            return f"<{name}: <#rawsource: '{self.rawsource}'>>"
        elif self._rawtext:
            return f"<{name}: <#rawtext: '{self._rawtext}'>>"
        else:
            return f"<{name}: <#empty>>"

    def __eq__(self, other):
        return self.astext() == other.astext()

    def __ne__(self, other):
        return self.astext() != other.astext()

    def __str__(self):
        """フォーマットが増えたら、パラメーターを見て使い分けるロジックを組む."""
        return self.ashtml()

    def _parse_text(self, text, parser):
        """
        doctest:

            >>> kana = KanaText('たなかひさみつ|田中ひさみつ^12d')
            >>> kana
            <KanaText: ruby='specific' option='12d' <#text: 'たなかひさみつ|田中ひさみつ'>>
        """
        match = parser.match(text)

        if not match:
            raise ValueError(rawtext)

        _, _, kana, word, _, marker, opt = match.groups()

        # display mode of ruby
        if not kana:   ruby = '' #off
        elif   opt:    ruby = 'specific'
        elif   marker: ruby = 'on'
        else:          ruby = '' #off

        if not opt: opt = ''

        return word, kana, ruby, opt

    def length(self):
        """
        doctest:
            >>> kana = KanaText('たなかはなこ|田中はな子^12b1')
            >>> kana.length()
            12
        """
        return len(self.astext())

    def astext(self):
        if len(self) == 2: return self[1] + self._delimiter + self[0]
        if len(self) == 1: return self[0]
        return ''

    def askana(self):
        """
        doctest:
            >>> kana = KanaText('たなかはなこ|田中はな子^12b1')
            >>> kana.askana()
            'たなかはなこ'
        """
        if len(self) < 1:
            raise ValueError(self, self.rawsource)

        if len(self) < 2:
            return ''
        else:
            return self[1]

    def asword(self):
        """
        doctest:
            >>> kana = KanaText('たなかはなこ|田中はな子^12b1')
            >>> kana.asword()
            '田中はな子'
        """
        if len(self) < 1:
            raise ValueError(self, self.rawsource)

        return self[0]

    def asterm(self): #alias name
        """
        doctest:

            >>> kana = KanaText('たなかはなこ|田中はな子^12b1')
            >>> kana.asterm()
            '田中はな子'
        """
        if len(self) < 1:
            raise ValueError(self, self.rawsource)

        return self.asword()

    def asruby(self):
        """
        doctest:
            >>> kana = KanaText('たなかはなこ|田中はな子^12b1')
            >>> kana.asruby()
            [(True, ('田', 'た')), (True, ('中', 'なか')), (False, 'はな'), (True, ('子', 'こ'))]
            >>> kana = KanaText('たなかはなこ|田中はな子^')
            >>> kana.asruby()
            [(True, ('田中はな子', 'たなかはなこ'))]
            >>> kana = KanaText('たなかはなこ|田中はな子')
            >>> kana.asruby()
            [(False, '田中はな子')]
            >>> kana = KanaText('田中はな子')
            >>> kana.asruby()
            [(False, '田中はな子')]
            >>> kana = KanaText('田中はな子')
        """

        if self['null']: return None

        ruby, option = self['ruby'], self['option']

        if len(self) < 1:
            raw = self.rawsource
            name = self.__class__.__name__
            raise ValueError(f"{name}('{raw}')", self.children)
        elif len(self) == 1:
            word = self[0]
            if word: data = [(False, word)]
            else:    data = None
        elif not ruby:
            word = self[0]
            data = [(False, word),]
        elif ruby == 'specific': #細かくルビの表示/非表示を指定する
            #アレコレがんばる
            word, kana = self[0], self[1]
            data = get_specific_by_parsing_option(word, kana, option)
        elif ruby == 'on': #ルビを付ける。文字の割当位置は気にしない。
            word, kana = self[0], self[1]
            data = [(True, (word, kana))]
        else:
            #ここは通らないはずだけど、念の為
            raise ValueError(self)

        return data

    def ashtml(self):
        """
        doctest:
            >>> kana = KanaText('はなこ|はな子^b1')
            >>> kana.ashtml()
            'はな<ruby><rb>子</rb><rp>（</rp><rt>こ</rt><rp>）</rp></ruby>'
        """

        html = ""
        for isruby, value in self.asruby():
            if isruby:
                html += make_html_with_ruby(value[0], value[1])
            else:
                html += value
        return html

#------------------------------------------------------------

_each_words = re.compile(r' *; +')

class KanaUnit(nodes.Element):

    _number_of_terms = { 'single': 2, 'pair': 2, 'triple': 3, 'see': 2, 'seealso': 2, }

    child_text_delimiter = '; '

    def __init__(self, value, entry_type='single', file_name=None, target=None, main='', index_key=''):
        """
        doctest:

            >>> ktext = KanaUnit('壱壱; 弐弐')
            >>> ktext
            <KanaUnit: entry_type='single' <KanaText: <#text: '壱壱'>><KanaText: <#text: '弐弐'>>>
            >>> ktext = KanaUnit('ああ|壱壱^')
            >>> ktext
            <KanaUnit: entry_type='single' <KanaText: ruby='on' <#text: 'ああ|壱壱'>>>
            >>> ktext = KanaUnit('あ|壱^1')
            >>> ktext
            <KanaUnit: entry_type='single' <KanaText: ruby='specific' option='1' <#text: 'あ|壱'>>>
        """


        kanatexts = []
        words = _each_words.split(value)

        for word in words:
            kanatexts.append(KanaText(word))

        super().__init__(value, *kanatexts, entry_type=entry_type, 
                         file_name=file_name, target=target, main=main, index_key=index_key)

    def __repr__(self):
        name = self.__class__.__name__
        prop = f"<{name}: "

        etype, ikey = self['entry_type'], self['index_key']
        main, fn, tid = self['main'], self['file_name'], self['target']
        if etype: prop += f"entry_type='{etype}' "
        if main:  prop += f"main='{main}' "
        if fn:    prop += f"file_name='{fn}' "
        if tid:   prop += f"target='{tid}' "
        if ikey:  prop += f"index_key='{ikey}' "

        children = ''.join([c.entity_of_repr() for c in self])
        prop += children + ">"

        return prop

    def make_index_unit(self):
        index_units = []

        entry_type = self['entry_type']
        fn = self['file_name']
        tid = self['target']
        main = self['main']
        index_key = self['index_key']

        def add_entry(ent, sub1, sub2):
            if entry_type in ('see', 'seealso'):
                #この二つentry_typeについては「かな表示」を一端諦める.
                emphasis = _emphasis2char['see']
                if entry_type == 'see':
                    sub = _('see %s') % sub1.asterm()
                if entry_type == 'seealso':
                    sub = _('see also %s') % sub1.asterm()
                index_unit = IndexUnit(ent._rawtext, sub, '', emphasis, '', '', index_key, KanaText)
            else:
                emphasis = _emphasis2char[main]
                try:
                    text1 = sub1._rawtext
                except AttributeError as err:
                    text1 = ''
                try:
                    text2 = sub2._rawtext
                except AttributeError as err:
                    text2 = ''
                index_unit = IndexUnit(ent._rawtext, text1, text2, emphasis, fn, tid, index_key, KanaText)

            return index_unit

        try:
            #add_entry(term, subterm1, subterm2)
            if entry_type == 'single':
                try:
                    index_units.append(add_entry(self[0], self[1], ''))
                except IndexError as err:
                    index_units.append(add_entry(self[0], '', ''))
            elif entry_type == 'pair':
                index_units.append(add_entry(self[0], self[1], ''))
                index_units.append(add_entry(self[1], self[0], ''))
            elif entry_type == 'triple':
                index_units.append(add_entry(self[2], self[0], self[1]))
                index_units.append(add_entry(self[0], self[1], self[2]))
                u = add_entry(self[1], self[2], self[0])
                u.set_subterm_delimiter(', ')
                index_units.append(u)
            elif entry_type == 'see':
                index_units.append(add_entry(self[0], self[1], ''))
            elif entry_type == 'seealso':
                index_units.append(add_entry(self[0], self[1], ''))
            else:
                logger.warning(__('unknown index entry type %r'), entry_type,
                                  location=fn)
        except ValueError as err:
            logger.warning(str(err), location=fn)

        return index_units

    def askana(self, concat=(', ', 3)):
        """
        doctest:
            >>> ktext = KanaUnit('壱壱')
            >>> ktext.askana()
            ''
            >>> ktext = KanaUnit('ああ|壱壱^11')
            >>> ktext.askana()
            'ああ'
            >>> ktext = KanaUnit('ああ|壱壱^11; いい|弐弐; うう|参参^11')
            >>> ktext.askana()
            'ああ, いい, うう'
        """
        kana = concat[0].join(k.askana() for k in self)
        return kana

    def asword(self, concat=(', ', 3)):
        """
        doctest:
            >>> ktext = KanaUnit('壱壱')
            >>> ktext.asword()
            '壱壱'
            >>> ktext = KanaUnit('ああ|壱壱^11')
            >>> ktext.asword()
            '壱壱'
            >>> ktext = KanaUnit('ああ|壱壱^11; いい|弐弐; うう|参参^11')
            >>> ktext.asword()
            '壱壱, 弐弐, 参参'
        """
        word = concat[0].join(k.asword() for k in self)
        return word

    def asterm(self, concat=(', ', 3)):
        """
        doctest:
            >>> ktext = KanaUnit('壱壱')
            >>> ktext.asterm()
            '壱壱'
            >>> ktext = KanaUnit('ああ|壱壱^11')
            >>> ktext.asterm()
            '壱壱'
            >>> ktext = KanaUnit('ああ|壱壱^11; いい|弐弐; うう|参参^11')
            >>> ktext.asterm()
            '壱壱, 弐弐, 参参'
        """
        term = concat[0].join(k.asterm() for k in self)
        return term

    def astext(self, concat=('; ', 3)):
        """
        doctest:
            >>> ktext = KanaUnit('壱壱')
            >>> ktext.astext()
            '壱壱'
            >>> ktext = KanaUnit('ああ|壱壱^11')
            >>> ktext.astext()
            'ああ|壱壱'
            >>> ktext = KanaUnit('ああ|壱壱^11; いい|弐弐; うう|参参^11')
            >>> ktext.astext()
            'ああ|壱壱; いい|弐弐; うう|参参'
        """
        text = concat[0].join(k.astext() for k in self)
        return text

    def asruby(self):
        """
        doctest:
            >>> kanatext = KanaUnit('ああ|壱壱; いい|弐弐^; うう|参参')
            >>> kanatext.asruby()
            [[(False, '壱壱')], [(True, ('弐弐', 'いい'))], [(False, '参参')]]
        """
        rubys = []
        for child in self:
            rubys.append(child.asruby())
        return rubys

    def ashtml(self, concat=('; ', 3)):
        html = concat[0].join(h.ashtml() for h in self)
        return html

#------------------------------------------------------------

def KanaRole(name, rawtext, text, lineno, inliner, options={}, content=[]):
    """「:kana:`かな|単語`」によるルビ表示

    :param name: ロール名. kana
    :type name: str
    :param rawtext: ロール名を含む全体. ex. \:kana\:\`たなかはなこ|田中はな子^\`
    :type rawtext: str
    :param text: ロール内データ. ex たなかはなこ|田中はな子^
    :type text: str
    :param inliner: Inliner object
    :type inliner: docutils.parsers.rst.states.Inliner
    :return: 作成したノード
    :rtype: [node], [システムメッセージ]
    """
    node = KanaText(text)
    return [node], []

def visit_kana(self, node):
    """KanaTexttクラスで作成されたオブジェクトの表示処理"""
    self.body.append(node.ashtml())

def depart_kana(self, node):
    """KanaTextクラスで作成されたオブジェクトの表示処理"""
    pass

#------------------------------------------------------------

class KanaHTML5Translator(html5.HTML5Translator):

    def visit_term(self, node: Element) -> None:
        """
        目的の文字列をKanaTextクラスにするための対応.
        後は、add_nodeで割り当てたメソッドが行う.
        """

        try:
            textnode = KanaText(node[0])
        except TypeError as e:
            pass
        else:
            #なくても動作しているのだけど、念の為
            textnode.parent = node[0].parent
            textnode.document = node[0].document
            textnode.source = node[0].source
            textnode.line = node[0].line
            textnode.children = node[0].children
            #ここまでが念の為

            node[0] = textnode

        self.body.append(self.starttag(node,'dt',''))

#------------------------------------------------------------

_first_char_small = {
    'あ': 'あ', 'い': 'あ', 'う': 'あ', 'え': 'あ', 'お': 'あ',
    'ア': 'あ', 'イ': 'あ', 'ウ': 'あ', 'エ': 'あ', 'オ': 'あ', 
    'か': 'か', 'き': 'か', 'く': 'か', 'け': 'か', 'こ': 'か',
    'カ': 'か', 'キ': 'か', 'ク': 'か', 'ケ': 'か', 'コ': 'か',
    'が': 'か', 'ぎ': 'か', 'ぐ': 'か', 'げ': 'か', 'ご': 'か',
    'ガ': 'か', 'ギ': 'か', 'グ': 'か', 'ゲ': 'か', 'ゴ': 'か', 
    'さ': 'さ', 'し': 'さ', 'す': 'さ', 'せ': 'さ', 'そ': 'さ',
    'サ': 'さ', 'シ': 'さ', 'ス': 'さ', 'セ': 'さ', 'ソ': 'さ',
    'ざ': 'さ', 'じ': 'さ', 'ず': 'さ', 'ぜ': 'さ', 'ぞ': 'さ',
    'ザ': 'さ', 'ジ': 'さ', 'ズ': 'さ', 'ゼ': 'さ', 'ゾ': 'さ', 
    'た': 'た', 'ち': 'た', 'つ': 'た', 'て': 'た', 'と': 'た',
    'タ': 'た', 'チ': 'た', 'ツ': 'た', 'テ': 'た', 'ト': 'た',
    'だ': 'た', 'ぢ': 'た', 'づ': 'た', 'で': 'た', 'ど': 'た',
    'ダ': 'た', 'ヂ': 'た', 'ヅ': 'た', 'デ': 'た', 'ド': 'た', 
    'な': 'な', 'に': 'な', 'ぬ': 'な', 'ね': 'な', 'の': 'な',
    'ナ': 'な', 'ニ': 'な', 'ヌ': 'な', 'ネ': 'な', 'ノ': 'な', 
    'は': 'は', 'ひ': 'は', 'ふ': 'は', 'へ': 'は', 'ほ': 'は',
    'ハ': 'は', 'ヒ': 'は', 'フ': 'は', 'ヘ': 'は', 'ホ': 'は',
    'ば': 'は', 'び': 'は', 'ぶ': 'は', 'べ': 'は', 'ぼ': 'は',
    'バ': 'は', 'ビ': 'は', 'ブ': 'は', 'ベ': 'は', 'ボ': 'は',
    'ぱ': 'は', 'ぴ': 'は', 'ぷ': 'は', 'ぺ': 'は', 'ぽ': 'は',
    'パ': 'は', 'ピ': 'は', 'プ': 'は', 'ペ': 'は', 'ポ': 'は', 
    'ま': 'ま', 'み': 'ま', 'む': 'ま', 'め': 'ま', 'も': 'ま',
    'マ': 'ま', 'ミ': 'ま', 'ム': 'ま', 'メ': 'ま', 'モ': 'ま', 
    'や': 'や', 'ゆ': 'や', 'よ': 'や', 'ヤ': 'や', 'ユ': 'や', 'ヨ': 'や',
    'ゃ': 'や', 'ゅ': 'や', 'ょ': 'や', 'ャ': 'や', 'ュ': 'や', 'ョ': 'や', 
    'ら': 'ら', 'り': 'ら', 'る': 'ら', 'れ': 'ら', 'ろ': 'ら',
    'ラ': 'ら', 'リ': 'ら', 'ル': 'ら', 'レ': 'ら', 'ロ': 'ら', 
    'わ': 'わ', 'を': 'わ', 'ワ': 'わ', 'ヲ': 'わ', 'ん': 'わ', 'ン': 'わ' }

_first_char_large = {
    'ア': 'あ', 'イ': 'い', 'ウ': 'う', 'エ': 'え', 'オ': 'お', 
    'カ': 'か', 'キ': 'き', 'ク': 'く', 'ケ': 'け', 'コ': 'こ',
    'が': 'か', 'ぎ': 'き', 'ぐ': 'く', 'げ': 'け', 'ご': 'こ',
    'ガ': 'か', 'ギ': 'き', 'グ': 'く', 'ゲ': 'け', 'ゴ': 'こ', 
    'サ': 'さ', 'シ': 'し', 'ス': 'す', 'セ': 'せ', 'ソ': 'そ',
    'ざ': 'さ', 'じ': 'し', 'ず': 'す', 'ぜ': 'せ', 'ぞ': 'そ',
    'ザ': 'さ', 'ジ': 'し', 'ズ': 'す', 'ゼ': 'せ', 'ゾ': 'そ', 
    'タ': 'た', 'チ': 'ち', 'ツ': 'つ', 'テ': 'て', 'ト': 'と',
    'だ': 'た', 'ぢ': 'ち', 'づ': 'つ', 'で': 'て', 'ど': 'と',
    'ダ': 'た', 'ヂ': 'ち', 'ヅ': 'つ', 'デ': 'て', 'ド': 'と', 
    'ナ': 'な', 'ニ': 'に', 'ヌ': 'ぬ', 'ネ': 'ね', 'ノ': 'の', 
    'ハ': 'は', 'ヒ': 'ひ', 'フ': 'ふ', 'ヘ': 'へ', 'ホ': 'ほ',
    'ば': 'は', 'び': 'ひ', 'ぶ': 'ふ', 'べ': 'へ', 'ぼ': 'ほ',
    'バ': 'は', 'ビ': 'ひ', 'ブ': 'ふ', 'ベ': 'へ', 'ボ': 'ほ',
    'ぱ': 'は', 'ぴ': 'ひ', 'ぷ': 'ふ', 'ぺ': 'へ', 'ぽ': 'ほ',
    'パ': 'は', 'ピ': 'ひ', 'プ': 'ふ', 'ペ': 'へ', 'ポ': 'ほ', 
    'マ': 'ま', 'ミ': 'み', 'ム': 'む', 'メ': 'め', 'モ': 'も', 
    'ヤ': 'や', 'ユ': 'ゆ', 'ヨ': 'よ',
    'ゃ': 'や', 'ゅ': 'ゆ', 'ょ': 'よ', 'ャ': 'や', 'ュ': 'ゆ', 'ョ': 'よ', 
    'ラ': 'ら', 'リ': 'り', 'ル': 'る', 'レ': 'れ', 'ロ': 'ろ', 
    'ワ': 'わ', 'ヲ': 'を', 'ン': 'ん' }

_emphasis2char = {
    'main': '1', #glossaryで定義した用語. indexでは「!」が先頭にあるもの.
    '':     '5', #上記以外
    'see':  '9', #see
}

_char2emphasis = {
    '0': '', '1': 'main', '2': '', '3': '', '4': '',
    '5': '', '6': '', '7': '', '8': '', '9': 'see',
}

def _get_classifier_by_first_char(term, config):
    """
    先頭の一文字を必要な加工をして分類子に使う.
    """
    try:
        #パラメータに応じて変換テーブルを使い分ける.
        if 'small' == config.html_kana_text_use_own_indexer:
            return _first_char_small[term[:1]]
        elif 'large' == config.html_kana_text_use_own_indexer:
            return _first_char_large[term[:1]]
        else:
            #想定パラメータ以外なら基本的な処理
            return term[:1].upper()
    except KeyError as err:
        #変換表になければ基本的な処理
        try:
            return term[:1].upper()
        except AttributeError as err:
            raise AttributeError(term)

class IndexRack(object):
    """
    処理概要

    1. self.__init__() 初期化.
    2. self.append() IndexUnitの取り込み. self.update()の準備.
    3. self.update() 各unitの更新、並び替えの準備.
    4. self.sort() 並び替え. ※3,4は分ける必要はないけど、見通しが良くなる気がするので. 
    5. self.generate_genindex_data() genindex用データの生成.

    .. note::

        - Textクラスの場合はastext()一種類で済むが、KanaTextクラスはastext()/ashtml()を使い分ける.
        - KanaTexttで以下の点を押さえれば、IndexRack/IndexUnitのロジックはTextと共有できると考えられる.

            - Textでの文字列の比較. KanaTextで__eq__()/__ne__()を定義する.
            - __str__()の実体としてashtml()を使う.

        - その他、KanaText固有と思われる箇所に「#KanaText」を挿入しておく.
    """
    
    UNIT_CLSF, UNIT_TERM, UNIT_SBTM, UNIT_EMPH = 0, 1, 2, 3

    def __init__(self, builder, group_entries=True, _fixre=re.compile(r'(.*) ([(][^()]*[)])') ):
        """IndexUnitの取り込み、整理、並べ替え. データの生成."""

        #制御情報の保存
        self._config = builder.config
        self.get_relative_uri = builder.get_relative_uri
        self._group_entries = group_entries
        self._fixre = _fixre

        #入れ物の用意
        self._rack = [] # [IndexUnit, IndexUnit, ...]
        self._max_length = [0, 0, 0, 0] #classifier, term, subterm, emphasis
        self._classifier_catalog = {} # {term: classifier} 
        self._kana_catalog = {} # {term: (emphasis, kana)} #KanaText
        self._function_catalog = {} #{function name: number of homonymous funcion}

    def append(self, unit):
        """
        - 全unitを見て決まる処理のための情報収集
        """
        #情報収集
        self.update_max_length(unit.length()) #各データの最大長の更新
        self.update_classifier_catalog(unit['index_key'], unit.asterms())
        self.update_kana_catalog(unit.askanas(), unit[self.UNIT_EMPH], unit.asterms()) #KanaText

        if self._group_entries:
            self.update_function_catalog(unit.asterms(), self._fixre)

        #unitをrackに乗せる
        self._rack.append(unit)

    def extend(self, units):
        for unit in units:
            self.append(unit)

    def update_max_length(self, length):
        for i in (0, 1, 2, 3):
            if length[i] > self._max_length[i]:
                self._max_length[i] = length[i]

    def update_classifier_catalog(self, index_key, terms):
        """Text/KanaText共通の処理"""
        if not index_key: return

        for term in terms:
            if not term in self._classifier_catalog:
                #上書きはしない.（∵「make clean」での状況を真とするため）
                self._classifier_catalog[term] = index_key

    def update_kana_catalog(self, kanas, emphasis, terms): #KanaText
        """KanaText用の処理"""
        for kana, term in zip(kanas, terms):
            if term in self._kana_catalog:
                if emphasis < self._kana_catalog[term][0]:
                    #emphasisコードが異なる場合は、数字の小さい方が優先.
                    self._kana_catalog[term] = (emphasis, kana)
                elif emphasis == self._kana_catalog[term][0] and len(kana) > len(self._kana_catalog[term][1]):
                    #emphasisコードが同じなら、かな文字の長いほうが優先.
                    self._kana_catalog[term] = (emphasis, kana)
                else:
                    #その他は、先に登録された方が優先. （∵「make clean」の状態で挙動が一定になるように）
                    pass #明示しておく.
            else:
                self._kana_catalog[term] = (emphasis, kana)

    def update_function_catalog(self, terms, _fixre):
        for term in terms:
            m = _fixre.match(term)
            if m:
                try:
                    self._function_catalog[m.group(1)] += 1
                except KeyError as err:
                    self._function_catalog[m.group(1)] = 1
            else:
                pass

    def update(self):
        """rack格納されている全てのunitの更新を行う."""
        for unit in self._rack:
            term = unit[self.UNIT_TERM].asterm() #KanaText. Textならastext().
            subterms = unit[self.UNIT_SBTM]
            ikey = unit['index_key']

            #各termの読みの設定
            #- 「同じ単語は同じ読み」を前提とした実装.
            #- 設定で挙動を選べるようにすべきかもしれない.

            kanatexts = [unit[self.UNIT_TERM]] #KanaText
            for subterm in subterms: #KanaText
                kanatexts.append(subterm)

            for kanatext in kanatexts: #KanaText
                if kanatext.asterm() in self._kana_catalog:
                    kanatext[1] = self._kana_catalog[kanatext.asterm()][1]
                else:
                    pass

            #classifierの設定（［重要］if/elifの判定順）
            #- 同じ用語が複数glossaryである場合、分類子は一箇所で設定すべき
            #- 複数の同じ用語が別々の分類子を設定していた場合、集約されるのは一つのみ.
            #- 複数箇所で設定していた場合は、修正すべき用語が特定できるようにする.

            if ikey:
                unit[self.UNIT_CLSF] = unit.textclass(ikey)
            elif term in self._classifier_catalog:
                unit[self.UNIT_CLSF] = unit.textclass(self._classifier_catalog[term])
            else:
                kana = unit[self.UNIT_TERM].askana()
                if kana:
                    unit[self.UNIT_CLSF] = unit.textclass(_get_classifier_by_first_char(kana, self._config))
                else:
                    unit[self.UNIT_CLSF] = unit.textclass(term[:1])

            #sortkeyの作成
            #- 各データの最大長に足りない文を半角スペースで埋める.
            #- 半角スペースで埋めて固定長にした文字列を連結してsortkeyとする.
            #- subtermは最大二つのKanaTextがある
            #  - それぞれ別々に読みが補完された場合は最大長をはみ出す.
            #  - とは言え、はみ出していない分の文字列のソートで実害はない（はず）.

            if unit[self.UNIT_EMPH] in ('7', '8', '9'):
                code = '2'
            else:
                code = '1'

            clsf = unit[self.UNIT_CLSF].astext() + ' '*self._max_length[self.UNIT_CLSF] #classifier
            term = unit[self.UNIT_TERM].astext() + ' '*self._max_length[self.UNIT_TERM] #term
            code = code + ' '*self._max_length[self.UNIT_EMPH] #emphasis. 長さは1で固定だけど..
            sbtm = unit[self.UNIT_SBTM].astext() + ' '*self._max_length[self.UNIT_SBTM] #subterm
            emph = unit[self.UNIT_EMPH] + ' '*self._max_length[self.UNIT_EMPH] #emphasis. 長さは1で固定だけど..

            sortkey  = clsf[:self._max_length[self.UNIT_CLSF]] + '|' #classifier
            sortkey += term[:self._max_length[self.UNIT_TERM]] + '|' #term
            sortkey += code[:self._max_length[self.UNIT_EMPH]] + '|' #position 'see' and 'seealso'
            sortkey += sbtm[:self._max_length[self.UNIT_SBTM]] + '|' #subterm
            sortkey += emph[:self._max_length[self.UNIT_EMPH]] + '|' #emphasis

            #sortkeyの設定
            unit._sortkey = sortkey

    def sort(self):
        #self._rack[x]._sortkeyがsortkeyなので、これで並び替える.
        self._rack.sort(key=lambda x: x._sortkey)

    def generate_genindex_data(self):
        """
        Text/KanaTextの選択を意識して書く.
        """
        rtnlist = [] #判定用

        _clf, _tm, _sub = -1, -1, -1
        for unit in self._rack: #rackからunitを取り出す
            i_clf = unit[self.UNIT_CLSF]
            i_tm  = unit[self.UNIT_TERM]
            i_sub = unit[self.UNIT_SBTM] #see: SubTerm
            i_em  = unit[self.UNIT_EMPH]
            i_fn  = unit['file_name']
            i_tid = unit['target']
            i_iky = unit['index_key']

            # fixup entries: transform
            #   func() (in module foo)
            #   func() (in module bar)
            # into
            #   func()
            #     (in module foo)
            #     (in module bar) 
            if self._group_entries:
                sub = ''
                m = self._fixre.match(i_tm.astext()) #関数を想定しているので、astext()とasterm()に差異はない.
                if m and self._function_catalog[m.group(1)] > 1:
                    #状況的にsubtermは空のはず.
                    assert not unit[self.UNIT_SBTM], f'{self.__class__.__name__}: subterm is not null'
                    tm = unit.textclass(m.group(1))
                    sub = unit.textclass(m.group(2))
                else:
                    tm, sub = i_tm, i_sub
            else:
                tm, sub = i_tm, i_sub
            #subの情報が消えるが、このケースに該当する場合はsubにはデータがないはず.

            #make a uri
            if i_fn:
                try:
                    r_uri = self.get_relative_uri('genindex', i_fn) + '#' + i_tid
                except NoUri:
                    continue

            #see: KanaText.__ne__
            if len(rtnlist) == 0 or rtnlist[_clf][0] != i_clf:
                rtnlist.append((i_clf, []))

                #追加された「(clf, [])」を見るように_clfを更新する. 他はリセット.
                _clf, _tm, _sub = _clf+1, -1, -1

            r_clsfr = rtnlist[_clf] #[classifier, [term, term, ..]]
            r_clfnm = r_clsfr[0] #classifier is KanaText object.
            r_terms = r_clsfr[1] #[term, term, ..]

            #see: KanaText.__ne__
            if len(r_terms) == 0 or r_terms[_tm][0] != tm:
                r_terms.append((tm, [[], [], i_iky]))
                _tm, _sub = _tm+1, -1

            r_term = r_terms[_tm]       #[term, [links, [subterm, subterm, ..], index_key]
            r_term_value = r_term[0]    #term_value is KanaText object.
            r_term_links = r_term[1][0] #[(main, uri), (main, uri), ..]
            r_subterms = r_term[1][1]   #[subterm, subterm, ..]

            #一文字から元の文字列に戻す
            r_main = _char2emphasis[i_em]

            #sub(class SubTerm): [], [KanaText], [KanaText, KanaText].
            if len(sub) == 0:
                if i_fn: r_term_links.append((r_main, r_uri))
            elif len(r_subterms) == 0 or r_subterms[_sub][0] != sub: #SubTerm.__ne__
                r_subterms.append((sub, []))

                _sub = _sub+1
                r_subterm = r_subterms[_sub]
                r_subterm_value = r_subterm[0]
                r_subterm_links = r_subterm[1]
                if i_fn: r_subterm_links.append((r_main, r_uri))
            else:
                if i_fn: r_subterm_links.append((r_main, r_uri))

        return rtnlist

class SubTerm(object):
    _delimiter = ' '
    def __init__(self):
        self._subterms = []
    def set_delimiter(self, delimiter=', '):
        #デフォルトから変更する場合は「', '」のパターンしかない.
        self._delimiter = delimiter
    def __len__(self):
        return len(self._subterms)
    def __eq__(self, otehr):
        return self.astext() == other.astext()
    def __ne__(self, other):
        return self.astext() != other.astext()
    def __iter__(self):
        self._counter = -1
        return self
    def __next__(self):
        self._counter += 1
        try:
            return self._subterms[self._counter]
        except IndexError as err:
            raise StopIteration
    def append(self, subterm):
        self._subterms.append(subterm)
    def length(self):
        leng, slen = 0, len(self._delimiter)
        for subterm in self._subterms:
            leng += subterm.length() + slen
        if leng > 0: leng -= slen
        return leng
    def astext(self):
        text = ""
        for subterm in self._subterms:
            text += subterm.astext() + self._delimiter
        return text[:-len(self._delimiter)]
    def asterm(self, delimiter):
        term = ""
        for subterm in self._subterms:
            term += subterm.asterm() + delimiter
        return term[:-len(delimiter)]

class IndexUnit(object):

    CLSF, TERM, SBTM, EMPH = 0, 1, 2, 3

    def __init__(self, term, subterm1, subterm2, emphasis, file_name, target, index_key, textclass=nodes.Text):
        """
        - リンクを作成しない場合は、file_name, targetは空文字かNoneにする.
        - Text/KanaTextを選択できる口だけ用意しているけど、実装はKanaText用でやっている.
        - IndexUnitを継承してKanaIndexUnitを定義するようなIndexUnitにすればイケる.
        """

        subterm = SubTerm()
        if subterm1: subterm.append(textclass(subterm1))
        if subterm2: subterm.append(textclass(subterm2))

        self._sortkey = None
        self._display_data = [textclass(''), textclass(term), subterm] #classifierを更新するのでタプルにはできない.
        self._link_data = (emphasis, file_name, target)
        self._index_key = index_key

        self.textclass = textclass

    def __repr__(self):
        name = self.__class__.__name__
        main = self['main']
        rpr  = f"'<{name}: "
        rpr += repr(self[0]) + repr(self[1])
        rpr += ">"
        return rpr

    def __getitem__(self, key):
        if isinstance(key, str):
            if key == 'main':      return self._link_data[0]
            if key == 'file_name': return self._link_data[1]
            if key == 'target':    return self._link_data[2]
            if key == 'index_key': return self._index_key
            raise KeyError(key)
        elif isinstance(key, int):
            if key == self.CLSF: return self._display_data[self.CLSF] #classifier
            if key == self.TERM: return self._display_data[self.TERM] #term
            if key == self.SBTM: return self._display_data[self.SBTM] #subterm
            if key == self.EMPH: return self._link_data[0]    #emphasis(main)
            raise KeyError(key)
        else:
            raise TypeError(key)

    def __setitem__(self, key, value): #更新するデータだけ対応する.
        if isinstance(key, int):
            if key == 0: self._display_data[key] = value
        else:
            raise KeyError(key)

    def set_subterm_delimiter(self, delimiter=', '):
        self[self.SBTM].set_delimiter(delimiter)

    def length(self):
        classifier = self._index_key
        term      = self[self.TERM]
        subterms  = self[self.SBTM]
        emphasis  = self[self.EMPH]
        if not classifier: classifier = ''

        if subterms:
            length = subterms.length()
        else:
            length = 0

        return (len(classifier), term.length(), length, len(emphasis))

    def askanas(self):
        kanas = [self[self.TERM].askana()]

        for subterm in self[self.SBTM]:
            kanas.append(subterm.askana())

        return kanas

    def asterms(self):
        """Textなら、astexts()になっている."""
        terms = [self[self.TERM].asterm()]

        for subterm in self[self.SBTM]:
            terms.append(subterm.asterm())

        return terms

#--------------------

class KanaIndexer(object):
    """Indexing用のメソッド群"""

    def __init__(self, builder):
        self.env = builder.env
        self.config = builder.config
        self.get_relative_uri = builder.get_relative_uri

    def create_genindex_entries(self, entries=None, group_entries: bool = True,
                     _fixre: Pattern = re.compile(r'(.*) ([(][^()]*[)])')
                     ) -> List[Tuple[str, List[Tuple[str, Any]]]]:
        """IndexEntriesクラス/create_indexメソッドを置き換える.

        group_entries, _fixreはオリジナルにあるので残しておく.
        （このオプションを使っている場所は見当たらない.）
        """

        #get entries（引数にあるentriesは単体テストからの受け取り場所）
        if not entries:
            domain = cast(IndexDomain, self.env.get_domain('index'))
            entries = domain.entries
        #entries: Dict{ファイル名: List[Tuple(type, value, tid, main, index_key)]}

        #インデクシングで共有されるデータ
        self._now_entries: List[str, Tuple] = []

        #インデクシングでgroup by的なことをやるための変数
        self._max_len_clf  = 0 #max length of classifier  
        self._max_len_term = 0 #max length of term
        self._max_len_sub  = 0 #max length of subterm
        self._term_to_classifier = {}
        self._term_to_kana = {} #Dict{term: List[emphasis, kana]}
        self._homonymous_functions = {} #Dict{func name: number of func}


        self._index_rack = IndexRack(self, group_entries, _fixre)
        #インデクシング（概要）
        #1. self._prepare_sortkey_and_make_entries()
        #   - ソート用文字列の下拵え（group by含む）
        #   - 2で作るsortkeyを収める場所を確保.
        #   - 3で必要な要素をタプルで用意する.
        #   - 2,3で必要な、全データを確認して分かることを調べておく.
        self._prepare_sortkey_and_make_entries(entries.items(), group_entries, _fixre)
        #2. self._make_sortkey_and_sort()
        #   - ソート用文字列の作成とソート.
        #   1. ソート用の各データは最大長に合わせて半角空白で埋めて固定長にする.
        #   2. 固定長になった各データを結合して一つの固定長文字列を作る.
        #   3. この固定長でソートする.
        self._make_sortkey_and_sort()
        self._index_rack.update()
        self._index_rack.sort()
        #3. self._create_genindex_entries()
        #   - ソート済みを前提にデータの作成
        #   - データ構造が複雑なので、混乱しないように意図の分かる変数名を逐一当てる.
        genidx = self._index_rack.generate_genindex_data()
        return self._create_genindex_entries(group_entries, _fixre)

    def _prepare_sortkey_and_make_entries(self, entries_on_each_file, group_entries, _fixre):
        def add_entry(term, subterm, emphasis, link=True):
            if index_key:
                _clf = index_key

                if not term in self._term_to_classifier:
                    self._term_to_classifier[term] = index_key
                #indexでclassifierの指定はできないが、念の為"早い者勝ち"にしておく.
            else:
                _clf = _get_classifier_by_first_char(term, self.config)

            #homonymous functions
            if group_entries:
                m = _fixre.match(term)
                if m:
                    try:
                        self._homonymous_functions[m.group(1)] += 1
                    except KeyError as err:
                        self._homonymous_functions[m.group(1)] = 1

            #ソート処理のために文字幅が揃う一文字に変換
            _em = _emphasis2char[emphasis] 

            #tripleのsubtermは扱えないので、termのみとする.
            node = KanaText(term)
            t, k = node.asterm(), node.askana()

            if not t in self._term_to_kana:
                #データが登録されていない
                self._term_to_kana[t] = (_em, k)
            elif _em < self._term_to_kana[t][0]:
                #emphasisが強いなら上書き
                self._term_to_kana[t] = (_em, k)
            elif _em == self._term_to_kana[t][0] and len(k) > len(self._term_to_kana[t][1]):
                #長さが同じ場合は上書きしない（∵make cleanでのデータ順を”正”とするため）
                self._term_to_kana[t] = (_em, k)

            #max of length
            if len(_clf) > self._max_len_clf: self._max_len_clf = len(_clf)
            if len(term) > self._max_len_term: self._max_len_term = len(term)
            if len(subterm) > self._max_len_sub: self._max_len_sub = len(subterm)

            #dataset
            dataset = (_clf, term, subterm, _em, link, fn, tid, index_key)

            #insert
            entry = [None, dataset]
            self._now_entries.append(entry)

        for fn, entries in entries_on_each_file:
            for entry_type, value, tid, main, index_key in entries:
                unit = KanaUnit(value, entry_type, fn, tid, main, index_key)
                index_units = unit.make_index_unit()
                self._index_rack.extend(index_units) #KaKkouoDebug
                try:
                    if entry_type == 'single':
                        try:
                            entry, subentry = split_into(2, 'single', value)
                        except ValueError:
                            entry, = split_into(1, 'single', value)
                            subentry = ''
                        add_entry(entry, subentry, main)
                    elif entry_type == 'pair':
                        first, second = split_into(2, 'pair', value)
                        add_entry(first, second, main)
                        add_entry(second, first, main)
                    elif entry_type == 'triple':
                        first, second, third = split_into(3, 'triple', value)
                        add_entry(first, second + ' ' + third, main)
                        add_entry(second, third + ', ' + first, main)
                        add_entry(third, first + ' ' + second, main)
                    elif entry_type == 'see':
                        first, second = split_into(2, 'see', value)
                        add_entry(first, _('see %s') % second, 'see', link=False)
                    elif entry_type == 'seealso':
                        first, second = split_into(2, 'see', value)
                        add_entry(first, _('see also %s') % second, 'see', link=False)
                    else:
                        logger.warning(__('unknown index entry type %r'), entry_type,
                                          location=fn)
                except ValueError as err:
                    logger.warning(str(err), location=fn)

    def _make_sortkey_and_sort(self):
        for entry in self._now_entries:
            clf, tm, sub, em, link, fn, tid, ikey = entry[1]

            #subはtripleで複数の単語を持つので処理できない.
            node = KanaText(tm)

            t, k = node.asterm(), node.askana()
            delimiter = re.sub(r'^\\', '', self.config.kana_text_separator)
            try:
                if self._term_to_kana[t][1]:
                    tm = self._term_to_kana[t][1]+delimiter+t
            except KeyError as err:
                pass

            if tm in self._term_to_classifier:
                _clf = self._term_to_classifier[tm]
            else:
                _clf = _get_classifier_by_first_char(tm, self.config)

            entry[1] = (_clf, tm, sub, em, link, fn, tid, ikey)

            classifier = _clf + ' '*self._max_len_clf
            term       = tm   + ' '*self._max_len_term
            subterm    = sub  + ' '*self._max_len_sub

            if em == '9': #see: _emphasis2char
                _sub_order = '9'
            else:
                _sub_order = '5'

            sortkey  = classifier[:self._max_len_clf]+'|'
            sortkey += term[:self._max_len_term]+'|'
            sortkey += _sub_order+'|' #see/seealsoの表示順をここで調整.
            sortkey += subterm[:self._max_len_sub]+'|'
            sortkey += em+'|'

            entry[0] = sortkey

        self._now_entries.sort()

    def _create_genindex_entries(self, group_entries, _fixre):
        newlist = []

        _clf, _tm, _sub = -1, -1, -1
        for _, (clf, tm, sub, em, link, fn, tid, ikey) in self._now_entries:
            # fixup entries: transform
            #   func() (in module foo)
            #   func() (in module bar)
            # into
            #   func()
            #     (in module foo)
            #     (in module bar) 
            if group_entries:
                m = _fixre.match(tm)
                if m and self._homonymous_functions[m.group(1)] > 1:
                    #状況的にsubtermは空のはず.
                    assert not sub, f'{self.__class__.__name__}: subterm is not null: {sub}'
                    tm = m.group(1)
                    sub = m.group(2)
            #subの情報が消えるが、このケースに該当する場合はsubにはデータがないはず.

            #make a uri
            if link:
                try:
                    uri = self.get_relative_uri('genindex', fn) + '#' + tid
                except NoUri:
                    continue

            if len(newlist) == 0 or newlist[_clf][0] != clf:
                newlist.append((clf, []))
                _clf, _tm, _sub = _clf+1, -1, -1

            classifier = newlist[_clf]
            cname = classifier[0]
            terms = classifier[1]

            if len(terms) == 0 or terms[_tm][0] != tm:
                terms.append((tm, [[], [], ikey]))
                _tm, _sub = _tm+1, -1

            term = terms[_tm]
            term_value = term[0]
            term_links = term[1][0]
            subterms = term[1][1]

            #一文字から元の文字列に戻す
            main = _char2emphasis[em]

            if not sub:
                if link: term_links.append((main, uri))
            elif len(subterms) == 0 or subterms[_sub][0] != sub:
                subterms.append((sub, []))

                _sub = _sub+1
                subterm = subterms[_sub]
                subterm_value = subterm[0]
                subterm_links = subterm[1]
                if link: subterm_links.append((main, uri))
            else:
                if link: subterm_links.append((main, uri))

        return newlist

#------------------------------------------------------------

class _StandaloneHTMLBuilder(builders.StandaloneHTMLBuilder):
    """
    オリジナルに依存する部分と拡張部分を区別するために用意したクラス.
    """

    def create_genindex(self) -> None: #KaKkou
        """
        このように分けてくれると、self.create_index()を書き換えるだけで済む.
        """

        return IndexEntries(self.env).create_index(self)

    def write_genindex(self) -> None:
        genindex = self.create_genindex() #KaKkou. データのソートが終わった直後

        #以降の処理はSphinx4.1.2オリジナルと同じ
        indexcounts = []
        for _k, entries in genindex:
            indexcounts.append(sum(1 + len(subitems)
                                   for _, (_, subitems, _) in entries))

        genindexcontext = {
            'genindexentries': genindex,
            'genindexcounts': indexcounts,
            'split_index': self.config.html_split_index,
        }
        logger.info('genindex ', nonl=True)

        if self.config.html_split_index:
            self.handle_page('genindex', genindexcontext,
                             'genindex-split.html')
            self.handle_page('genindex-all', genindexcontext,
                             'genindex.html')
            for (key, entries), count in zip(genindex, indexcounts):
                ctx = {'key': key, 'entries': entries, 'count': count,
                       'genindexentries': genindex}
                self.handle_page('genindex-' + key, ctx,
                                 'genindex-single.html')
        else:
            self.handle_page('genindex', genindexcontext, 'genindex.html')

class KanaHTMLBuilder(_StandaloneHTMLBuilder):
    """索引ページの日本語対応"""

    name = 'kana'

    def _prepare_for_creating_genindex(self) -> None:
        """索引作成前の準備"""

        domain = cast(IndexDomain, self.env.get_domain('index'))
        #see: sphinx/domains/index.py

        self._kanatext_nodes = {}
        for fn, entries in domain.entries.items():
            new_entries = []
            for entry_type, value, tid, main, index_key in entries:

                textnode = KanaUnit(value, entry_type, fn, tid, main, index_key)
                if self.config.html_kana_text_on_genindex:
                    key = textnode.astext(concat=("",1))
                    if key in self._kanatext_nodes:
                        pass
                    else:
                        self._kanatext_nodes[key] = textnode 
                value = textnode.astext()
                new = (entry_type, value, tid, main, index_key)
                new_entries.append(new)
            domain.entries[fn] = new_entries

    def create_genindex(self) -> None: #KaKkou
        """索引の作成"""

        self._prepare_for_creating_genindex()
        #次のコードがアクセスしているデータを手直しする
        #Glossaryから登録されたTermについて、末尾の「^xxx」を削除する

        #インデクサーの選択
        if self.config.html_kana_text_use_own_indexer:
            #自前のIndexerを使う
            entries = KanaIndexer(self).create_genindex_entries()
        else:
            #self.write_index()にあったソート処理
            entries = IndexEntries(self.env).create_index(self)

        #結果の確認
        if self.config.debug_kana_text_genindex_entries:
            pretty(entries) #KaKkou

        #ソートの後処理。表示文字を加工して出力処理に渡す
        genindex = []
        for classifier, terms in entries:
            #index_keyの処理
            classifier = self._manage_kana_of_term(classifier)

            new_terms = []
            for term, term_info in terms:
                #用語（主）の処理
                term = self._manage_kana_of_term(term)

                term_links = term_info[0]
                subterms = term_info[1]
                index_key = term_info[2]

                #用語（副）の処理
                if subterms:
                    new_subterms = []
                    for subterm, subterm_links in subterms:
                        #用語（副）は次の３パターンがある。
                        #- １文字（用語）
                        #- ２文字（用語1 用語2） カンマなし
                        #- ２文字（用語1, 用語2） カンマあり
                        cfg_sep = self.config.kana_text_separator
                        regex = r'(^.*?'+cfg_sep+r'|[^ ]+?\|)'
                        subterm = re.sub(regex,'',subterm)
                        #詳細はindexentries.pyのadd_entryの実行箇所を参照

                        #tripleの表示仕様を変更
                        #see: indexentries.py, IndexEntries.create_index
                        if self.config.html_change_triple:
                            #（f'{3rd}, {1st}' to f'{1st}, {3rd}'）
                            parts = re.split(', ',subterm)+[None]
                            if parts[1]:
                                subterm = parts[1]+', '+parts[0]
                        new_subterms.append((subterm,subterm_links))
                    term_info[1] = new_subterms
                new_terms.append((term,term_info))
            genindex.append([classifier,new_terms])
        return genindex

    def _manage_kana_of_term(self, term: str) -> str:
        """索引ページ用に、かなを削除して表示に使う文字のみにする"""

        #読み仮名の対応
        if self.config.html_kana_text_on_genindex:
            if term in self._kanatext_nodes:
                terms = self._kanatext_nodes[term].asruby()
                return terms[0]

        #かなと分割する
        cfg_sep = self.config.kana_text_separator
        parts = re.split(cfg_sep, term) + [None]

        #読み仮名がないなら文字列をそのまま帰す
        if parts[1] is None:
            return term

        #読み仮名を除いた文字を返す
        return parts[1]

#------------------------------------------------------------

class _IndexRole(IndexRole):
    """
    変更点は次の通り
    - 変更前）text = nodes.Text(title, title)
    - 変更後）text = self.create_textnode(title, title)
    """
    def create_textnode(sefl, text, rawtext):
        return Text(text, rawtext)

    def run(self) -> Tuple[List[Node], List[system_message]]:
        target_id = 'index-%s' % self.env.new_serialno('index')
        if self.has_explicit_title:
            # if an explicit target is given, process it as a full entry
            title = self.title
            entries = process_index_entry(self.target, target_id)
        else:
            # otherwise we just create a single entry
            if self.target.startswith('!'):
                title = self.title[1:]
                entries = [('single', self.target[1:], target_id, 'main', None)]
            else:
                title = self.title
                entries = [('single', self.target, target_id, '', None)]

        index = addnodes.index(entries=entries)
        target = nodes.target('', '', ids=[target_id])
        text = self.create_textnode(title, title) #KaKkou
        self.set_source_info(index)
        return [index, target, text], []

class KanaIndexRole(_IndexRole):
    def create_textnode(self, text, rawtext):
        return KanaText(text)

#------------------------------------------------------------

def setup(app) -> Dict[str, Any]:
    """各クラスや設定の登録

    :param app: add_buidder, add_config_valueの実行に必要
    :type app: Sphinx
    :return: 本Sphinx拡張の基本情報など
    :rtype: Dict[name: value]
    """
    #「:index:`かな|単語<かな|単語>`」が使用可能になる
    app.add_role('index', KanaIndexRole(), True)

    #「:kana:`かな|単語^11`」が使用可能になる
    app.add_role('kana', KanaRole)

    #glossaryディレクティブ、kanaロールの表示用
    app.add_node(KanaText, html=(visit_kana, depart_kana))
    app.add_node(KanaUnit, html=(visit_kana, depart_kana))
    #索引の表示はKanaHTMLBuilderで行う

    #HTML出力
    app.add_builder(KanaHTMLBuilder)
    app.set_translator('kana', KanaHTML5Translator)

    #設定の登録
    app.add_config_value('kana_text_separator', r'\|', 'env') 
    app.add_config_value('kana_text_option_marker', r'\^', 'env') 
    app.add_config_value('html_change_triple', False, 'html') 
    app.add_config_value('html_kana_text_on_genindex', False, 'html') 
    app.add_config_value('html_kana_text_use_own_indexer', 'small', 'html') 
    app.add_config_value('debug_kana_text_genindex_entries', False, 'html') 

    #バージョンの最後は作成日（MMDDYY）
    return {
            'version': __version__,
            'parallel_read_safe': True,
            'parallel_write_safe': True,
        }

#------------------------------------------------------------

if __name__ == '__main__':
    import doctest
    doctest.testmod()
