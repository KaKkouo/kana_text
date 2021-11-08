"""
sphinxcontrib.kana_text
=======================

Class, Function
===============
"""

__copyright__ = 'Copyright (C) 2021 @koKkekoh'
__license__ = 'BSD 2-Clause License'
__author__  = '@koKekkoh'
__version__ = '0.28.1' # 2021-11-04
__url__     = 'https://qiita.com/tags/sphinxcotrib.kana_text'

import re, pathlib
from typing import TYPE_CHECKING, Any, Dict, List, Tuple, Pattern, Type, cast

from docutils import nodes
from docutils.nodes import Node, Text, Element, system_message

from sphinx import addnodes
import sphinx.builders.html as builders
from sphinx.config import Config
from sphinx.domains.index import IndexDomain, IndexRole
from sphinx.errors import NoUri
from sphinx.environment.adapters.indexentries import IndexEntries
from sphinx.locale import _, __
from sphinx.util import logging, split_into, docutils
from sphinx.util.nodes import process_index_entry
from sphinx.writers import html5

import sphindexer as idxr

logger = logging.getLogger(__name__)


# ------------------------------------------------------------


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
    _word = nodes.unescape(word)
    _kana = nodes.unescape(kana)

    rb = f'<rb>{_word}</rb>' #単語
    rt = f'<rt>{_kana}</rt>' #かな
    rp = ('<rp>（</rp>', '<rp>）</rp>')

    return f'<ruby>{rb}{rp[0]}{rt}{rp[1]}</ruby>'

def make_specific_by_parsing_option(word, kana, option):
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


class KanaText(nodes.Element):
    """かな文字を扱うTextクラス

    - Jinja2のstring判定ではFalseとなるように、reprunicode(str)は継承しない.
    - __str__はText.astext()と同じ挙動としてashier()を使う.
    - KanaText.astext()は簡易IDとして扱う.
    """

    children = () #これでTextクラスと同じ扱いになる.
    config = None

    def __init__(self, rawword, rawtext=''):
        """
        doctest:

            >>> kana = KanaText('はなこ|はな子^b1')
            >>> kana
            <KanaText: len=2 ruby='specific' option='b1' <#text: 'はなこ|はな子'>>
        """

        if self.config and _dflt_separator != self.config.kana_text_separator:
            separator = self.config.kana_text_separator
        else:
            separator = _dflt_separator

        if self.config and _dflt_option_marker != self.config.kana_text_option_marker:
            option_marker = self.config.kana_text_option_marker
        else:
            option_marker = _dflt_option_marker

        self._rawword = rawword
        self._rawtext = rawtext
        self._separator = separator
        self._option_marker = option_marker
        self.whatiam = 'term' #in('classifier', 'term')

        if rawtext:
            rawsource = rawtext
        else:
            rawsource = rawword

        delimiter = _chop.sub('', separator)

        parser = parser_for_kana_text(separator, option_marker)
        hier, kana, ruby, option = self._parse_text(rawword.strip(), parser)

        super().__init__(rawsource, hier=hier, kana=kana, ruby=ruby, option=option,
                          null=not hier, delimiter=delimiter)

    def __len__(self):
        if not self['kana'] is None: return 2
        if not self['hier'] is None: return 1 #0.22.0: 'is None'を削除しても動作するように調整.
        raise ValueError(repr(self))

    def __eq__(self, other):
        """unittest用"""
        return self.astext() == other

    def __str__(self):
        """jinja2用"""
        if self.whatiam == 'term' and self.kana_text_on_genindex:
            return self.ashtml()
        else:
            return self.ashier()

    def __repr__(self):
        return self.entity_of_repr()

    def entity_of_repr(self):
        """
        doctest:
            >>> kana = KanaText('はなこ|はな子^b1')
            >>> kana
            <KanaText: len=2 ruby='specific' option='b1' <#text: 'はなこ|はな子'>>
        """
        name = self.__class__.__name__
        rb, op = self['ruby'], self['option']
        hier, kana = self['hier'], self['kana']
        if kana:
            prop = f"<{name}: len={len(self)} "
            if len(rb) > 0: prop += f"ruby='{rb}' "
            if len(op) > 0: prop += f"option='{op}' "
            prop += f"<#text: '{kana}|{hier}'>>"

            return prop
        elif hier:
            return f"<{name}: len={len(self)} <#text: '{hier}'>>"
        elif self._rawword:
            return f"<{name}: <#rawword: '{self._rawword}'>>"
        elif self._rawtext:
            return f"<#rawtext: '{self._rawtext}'>"
        else:
            return "<#text: ''>"

    def _parse_text(self, text, parser):
        """
        doctest:

            >>> kana = KanaText('たなかひさみつ|田中ひさみつ^12d')
            >>> kana
            <KanaText: len=2 ruby='specific' option='12d' <#text: 'たなかひさみつ|田中ひさみつ'>>
        """
        match = parser.match(text)

        if not match:
            raise ValueError(self._rawword)

        _, _, kana, hier, _, marker, opt = match.groups()

        # display mode of ruby
        if not kana  : ruby = ''  # off
        elif   opt   : ruby = 'specific'
        elif   marker: ruby = 'on'
        else         : ruby = ''  # off

        if not opt: opt = ''

        return hier, kana, ruby, opt

    def astext(self):
        if self['kana']: return self['kana'] + self['delimiter'] + self['hier']
        if self['hier']: return self['hier']
        return ''

    def askana(self):
        """
        doctest:
            >>> kana = KanaText('たなかはなこ|田中はな子^12b1')
            >>> kana.askana()
            'たなかはなこ'
        """
        if len(self) < 1:
            raise ValueError(repr(self))

        if len(self) < 2:
            return ''
        else:
            return self['kana']

    def ashier(self):
        """
        doctest:
            >>> kana = KanaText('たなかはなこ|田中はな子^12b1')
            >>> kana.ashier()
            '田中はな子'
        """
        if len(self) < 1:
            raise ValueError(self._rawword, repr(self))

        return self['hier']

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
        """

        if self['null']: return None

        ruby, option = self['ruby'], self['option']

        if len(self) < 1:
            raise ValueError(self._rawword, repr(self))
        elif len(self) == 1:
            hier = self['hier']
            if hier: data = [(False, hier)]
            else   : raise ValueError(self._rawword, repr(self))
        elif not ruby:
            hier = self['hier']
            data = [(False, hier), ]
        elif ruby == 'specific':  # 細かくルビの表示/非表示を指定する
            # アレコレがんばる
            hier, kana = self['hier'], self['kana']
            data = make_specific_by_parsing_option(hier, kana, option)
        elif ruby == 'on':  # ルビを付ける。文字の割当位置は気にしない。
            hier, kana = self['hier'], self['kana']
            data = [(True, (hier, kana))]
        else:
            # ここは通らないはずだけど、念の為
            raise ValueError(repr(self))

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


# ------------------------------------------------------------


class ExtSubterm(idxr.Subterm):
    """subterm in IndexUnit"""

    def __init__(self, emphasis, *terms):
        self.change_triple = False
        super().__init__(emphasis, *terms)

    def __str__(self):
        """Jinja2用"""
        return nodes.unescape(self.ashier())

    def astext(self):
        if self['template'] and len(self) == 1:
            return self['template'] % self[0].ashier()

        text = ""
        for subterm in self:
            text += subterm.astext() + self['delimiter']
        return text[:-len(self['delimiter'])]

    def ashier(self):
        if self['template'] and len(self) == 1:
            return self['template'] % self[0].ashier()

        if self.change_triple and len(self) == 2 and self['delimiter'] == ', ':
            return self[1].ashier() + self['delimiter'] + self[0].ashier()

        hier = ""
        for subterm in self:
            hier += subterm.ashier() + self['delimiter']
        return hier[:-len(self['delimiter'])]


class ExtIndexUnit(idxr.IndexUnit):
    def get_terms(self):
        terms = [self[1]]
        for s in self[2]:
            terms.append(s)
        return terms


# ------------------------------------------------------------


_each_words = re.compile(r' *; +')


class ExtIndexEntry(idxr.IndexEntry):

    textclass = KanaText
    packclass = ExtSubterm
    unitclass = ExtIndexUnit

    def __init__(self, rawtext, entry_type='single', file_name=None, target=None, main='',
                 index_key=''):

        super().__init__(rawtext, entry_type, file_name, target, main, index_key)

    def __repr__(self):
        """
        doctest:

            >>> ktext = Ext[:wIndexEntry('壱壱; 弐弐')
            >>> ktext
            <Ext[:wIndexEntry: entry_type='single' <KanaText: len=1 <#text: '壱壱'>><KanaText: len=1 <#text: '弐弐'>>>
            >>> ktext = Ext[:wIndexEntry('ああ|壱壱^')
            >>> ktext
            <Ext[:wIndexEntry: entry_type='single' <KanaText: len=2 ruby='on' <#text: 'ああ|壱壱'>>>
            >>> ktext = Ext[:wIndexEntry('あ|壱^1')
            >>> ktext
            <ExtIndexEntry: entry_type='single' <KanaText: len=2 ruby='specific' option='1' <#text: 'あ|壱'>>>
        """

        name = self.__class__.__name__
        prop = f"<{name}: "

        etype, ikey = self['entry_type'], self['index_key']
        main, fn, tid = self['main'], self['file_name'], self['target']
        if etype: prop += f"entry_type='{etype}' "
        if main : prop += f"main='{main}' "
        if fn   : prop += f"file_name='{fn}' "
        if tid  : prop += f"target='{tid}' "
        if ikey : prop += f"index_key='{ikey}' "

        children = ''.join([c.entity_of_repr() for c in self])
        prop += children + ">"

        return prop

    def asruby(self):
        """
        doctest:
            >>> kanatext = ExtIndexEntry('ああ|壱壱; いい|弐弐^; うう|参参')
            >>> kanatext.asruby()
            [[(False, '壱壱')], [(True, ('弐弐', 'いい'))], [(False, '参参')]]
        """
        rubys = []
        for child in self:
            rubys.append(child.asruby())
        return rubys

    def ashtml(self, concat=(', ', 3)):
        html = concat[0].join(h.ashtml() for h in self)
        return html


# ------------------------------------------------------------


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
    'わ': 'わ', 'を': 'わ', 'ワ': 'わ', 'ヲ': 'わ', 'ん': 'わ', 'ン': 'わ'}

_first_char_large = {
    'あ': 'あ', 'い': 'い', 'う': 'う', 'え': 'え', 'お': 'お',
    'ア': 'あ', 'イ': 'い', 'ウ': 'う', 'エ': 'え', 'オ': 'お',
    'か': 'か', 'き': 'き', 'く': 'く', 'け': 'け', 'こ': 'こ',
    'カ': 'か', 'キ': 'き', 'ク': 'く', 'ケ': 'け', 'コ': 'こ',
    'が': 'か', 'ぎ': 'き', 'ぐ': 'く', 'げ': 'け', 'ご': 'こ',
    'さ': 'さ', 'し': 'し', 'す': 'す', 'せ': 'せ', 'そ': 'そ',
    'ガ': 'か', 'ギ': 'き', 'グ': 'く', 'ゲ': 'け', 'ゴ': 'こ',
    'サ': 'さ', 'シ': 'し', 'ス': 'す', 'セ': 'せ', 'ソ': 'そ',
    'ざ': 'さ', 'じ': 'し', 'ず': 'す', 'ぜ': 'せ', 'ぞ': 'そ',
    'ザ': 'さ', 'ジ': 'し', 'ズ': 'す', 'ゼ': 'せ', 'ゾ': 'そ',
    'た': 'た', 'ち': 'ち', 'つ': 'つ', 'て': 'て', 'と': 'と',
    'タ': 'た', 'チ': 'ち', 'ツ': 'つ', 'テ': 'て', 'ト': 'と',
    'だ': 'た', 'ぢ': 'ち', 'づ': 'つ', 'で': 'て', 'ど': 'と',
    'ダ': 'た', 'ヂ': 'ち', 'ヅ': 'つ', 'デ': 'て', 'ド': 'と',
    'な': 'な', 'に': 'に', 'ぬ': 'ぬ', 'ね': 'ね', 'の': 'の',
    'ナ': 'な', 'ニ': 'に', 'ヌ': 'ぬ', 'ネ': 'ね', 'ノ': 'の',
    'は': 'は', 'ひ': 'ひ', 'ふ': 'ふ', 'へ': 'へ', 'ほ': 'ほ',
    'ハ': 'は', 'ヒ': 'ひ', 'フ': 'ふ', 'ヘ': 'へ', 'ホ': 'ほ',
    'ば': 'は', 'び': 'ひ', 'ぶ': 'ふ', 'べ': 'へ', 'ぼ': 'ほ',
    'バ': 'は', 'ビ': 'ひ', 'ブ': 'ふ', 'ベ': 'へ', 'ボ': 'ほ',
    'ま': 'ま', 'み': 'み', 'む': 'む', 'め': 'め', 'も': 'も',
    'ぱ': 'は', 'ぴ': 'ひ', 'ぷ': 'ふ', 'ぺ': 'へ', 'ぽ': 'ほ',
    'パ': 'は', 'ピ': 'ひ', 'プ': 'ふ', 'ペ': 'へ', 'ポ': 'ほ',
    'マ': 'ま', 'ミ': 'み', 'ム': 'む', 'メ': 'め', 'モ': 'も',
    'や': 'や', 'ゆ': 'ゆ', 'よ': 'よ', 'ヤ': 'や', 'ユ': 'ゆ', 'ヨ': 'よ',
    'ゃ': 'や', 'ゅ': 'ゆ', 'ょ': 'よ', 'ャ': 'や', 'ュ': 'ゆ', 'ョ': 'よ',
    'ら': 'ら', 'り': 'り', 'る': 'る', 'れ': 'れ', 'ろ': 'ろ',
    'ラ': 'ら', 'リ': 'り', 'ル': 'る', 'レ': 'れ', 'ロ': 'ろ',
    'わ': 'わ', 'を': 'を', 'ん': 'ん', 'ワ': 'わ', 'ヲ': 'を', 'ン': 'ん'}


def get_word_list_from_file(config):
    if not config.kana_text_word_file: return []

    file_name = config.kana_text_word_file
    file_name = pathlib.Path(file_name).expanduser()

    with open(file_name, 'r') as fd:
        lines = fd.readlines()

    return lines


class ExtIndexRack(idxr.IndexRack):
    """
    処理概要

    1. self.__init__() 初期化. 設定からの読み込み.
    2. self.append() ExtIndexUnitの取り込み. self.update()の準備.
    3. self.update_units() 各unitの更新、並び替えの準備.
    4. self.sort_units() 並び替え.
    5. self.generate_genindex_data() genindex用データの生成.
    """

    UNIT_CLSF, UNIT_TERM, UNIT_SBTM = 0, 1, 2

    textclass = KanaText
    packclass = ExtSubterm
    unitclass = ExtIndexUnit
    entryclass = ExtIndexEntry

    def __init__(self, builder, testmode=False):
        """ExtIndexUnitの取り込み、整理、並べ替え. データの生成."""

        # 制御情報の保存
        self.testmode = testmode  # 0.24 未使用になった.
        self._kana_catalog = {}   # {term: (emphasis, kana)} #KanaText

        # 設定で用意されたかな文字情報の登録
        for rawword in builder.config.kana_text_word_list:
            entry = ExtIndexEntry(rawword, 'list', 'WORD_LIST', '', 'conf.py', None)  # _cnfpy_
            index_units = entry.make_index_units()
            for iu in index_units:
                self.put_in_kana_catalog(iu['main'], iu.get_terms())

        # 設定ファイルで用意されたかな文字情報の登録
        for rawword in get_word_list_from_file(builder.config):
            entry = ExtIndexEntry(rawword, 'list', 'WORD_FILE', '', 'rcfile', None)  # _rncmd_
            index_units = entry.make_index_units()
            for iu in index_units:
                self.put_in_kana_catalog(iu['main'], iu.get_terms())

        super().__init__(builder)

    def create_index(self, entries=None, group_entries: bool = True,
                     _fixre: Pattern = re.compile(r'(.*) ([(][^()]*[)])')
                     ) -> List[Tuple[str, List[Tuple[str, Any]]]]:
        """IndexEntriesクラス/create_indexメソッドを置き換える."""

        # 入れ物の用意とリセット
        self._kana_catalog_pre = self._kana_catalog  # (注)__init__がないと前回分が残る.
        self._kana_catalog = {}  # {term: (emphasis, kana, ruby, option)}

        return super().create_index(group_entries, _fixre)

    def append(self, unit):
        """
        - 全unitを見て決める更新処理のための情報収集
        """
        # 情報収集
        self.put_in_kana_catalog(unit['main'], unit.get_terms())
        unit[self.UNIT_TERM].kana_text_on_genindex = self.config.kana_text_on_genindex

        # 残りの処理
        super().append(unit)

    def put_in_kana_catalog(self, emphasis, terms):
        """KanaText用の処理"""
        for term in terms:
            kana, hier, ruby, spec = term.askana(), term.ashier(), term['ruby'], term['option']
            if kana and hier in self._kana_catalog:
                item = self._kana_catalog[hier]
                if emphasis < item[0]:
                    # emphasisコードが異なる場合は、数字の小さい方が優先.
                    self._kana_catalog[hier] = (emphasis, kana, ruby, spec)
                elif emphasis == item[0]:
                    # emphasisコードが同じなら、かな文字の長いほうが優先.
                    if len(kana) > len(item[1]):
                        self._kana_catalog[hier] = (emphasis, kana, ruby, spec)
                    # 検討）かな文字の長さも同じなら、、
                    elif len(kana) == len(item[1]):
                        # 'specific'に限りオプションコードが多い方を採用する.
                        if ruby == 'specific' and ruby == item[2] and len(spec) > len(item[3]):
                            self._kana_catalog[hier] = (emphasis, kana, ruby, spec)
                    else:
                        pass
                else:
                    # その他は、先に登録された方が優先. （∵「make clean」の有無に依存しない）
                    pass  # 明示しておく.
            elif kana:
                self._kana_catalog[hier] = (emphasis, kana, ruby, spec)

    def make_classifier_from_first_letter(self, text):
        """
        先頭の一文字を必要な加工をして分類子に使う.
        """
        try:
            # パラメータに応じて変換テーブルを使い分ける.
            if 'small' == self.config.kana_text_indexer_mode:
                return _first_char_small[text[:1]]
            elif 'large' == self.config.kana_text_indexer_mode:
                return _first_char_large[text[:1]]
            else:
                # 想定パラメータ以外なら基本的な処理
                return text[:1].upper()
        except KeyError:
            # 変換表になければ基本的な処理
            return text[:1].upper()

    def update_units(self):
        """rackに格納されている全てのunitの更新を行う."""

        # __init__で貯めた情報を追加する.
        self._kana_catalog.update(self._kana_catalog_pre)

        # カタログ情報を使った更新/kana_text_change_tripleの反映
        for unit in self._rack:
            assert [unit[self.UNIT_TERM]]

            # 各termの読みの設定（「同じ単語は同じ読み」とする）

            self.update_term_with_kana_catalog(unit[self.UNIT_TERM])

            for subterm in unit[self.UNIT_SBTM]:
                self.update_term_with_kana_catalog(subterm)

            # kana_text_change_tripleの設定値を反映
            unit[self.UNIT_SBTM].change_triple = self.config.kana_text_change_triple

        super().update_units()

    def get_word(self, term):
        return term.ashier()

    def update_term_with_kana_catalog(self, term):
        if term.ashier() in self._kana_catalog:
            term['kana'] = self._kana_catalog[term.ashier()][1]
            term['ruby'] = self._kana_catalog[term.ashier()][2]
            term['option'] = self._kana_catalog[term.ashier()][3]
        else:
            pass


# ------------------------------------------------------------


class ExtRole(docutils.SphinxRole):
    """「:kana:`かな|単語`」によるルビ表示"""

    def run(self):
        node = KanaText(self.text)
        return [node], []


def visit_kana(self, node):
    """KanaTextクラスで作成されたオブジェクトの表示処理"""
    self.body.append(node.ashtml())


def depart_kana(self, node):
    """KanaTextクラスで作成されたオブジェクトの表示処理"""
    pass


# ------------------------------------------------------------


class ExtHTML5Translator(html5.HTML5Translator):

    def visit_term(self, node: Element) -> None:
        """
        目的の文字列をKanaTextクラスにするための対応.
        後は、add_nodeで割り当てたメソッドが行う.
        """

        try:
            term = KanaText(node[0].astext())
        except TypeError as e:
            pass
        else:
            # なくても動作しているのだけど、念の為
            term.parent = node[0].parent
            term.document = node[0].document
            term.source = node[0].source
            term.line = node[0].line
            term.children = node[0].children
            # ここまでが念の為

            node[0] = term

        self.body.append(self.starttag(node, 'dt', ''))


# ------------------------------------------------------------


class ExtHTMLBuilder(idxr.HTMLBuilder):
    """索引ページの日本語対応"""

    name = 'kana'

    def index_adapter(self) -> None:
        """索引の作成"""
        # 自前のIndexerを使う
        return ExtIndexRack(self).create_index()


# ------------------------------------------------------------


class ExtXRefIndex(idxr.XRefIndex):
    def textclass(self, text, rawtext):
        return KanaText(text)


# ------------------------------------------------------------


def setup(app) -> Dict[str, Any]:
    """各クラスや設定の登録

    :param app: add_buidder, add_config_valueの実行に必要
    :type app: Sphinx
    :return: 本Sphinx拡張の基本情報など
    :rtype: Dict[name: value]
    """
    # 「:index:`かな|単語<かな|単語>`」が使用可能になる
    app.add_role('index', ExtXRefIndex(), True)

    # 「:kana:`かな|単語^11`」が使用可能になる
    app.add_role('kana', ExtRole())

    # glossaryディレクティブ、kanaロールの表示用
    app.add_node(KanaText, html=(visit_kana, depart_kana))
    app.add_node(ExtIndexEntry, html=(visit_kana, depart_kana))
    # 索引の表示はExtHTMLBuilderで行う

    # HTML出力
    app.add_builder(ExtHTMLBuilder)
    app.set_translator('kana', ExtHTML5Translator)

    # 設定の登録
    app.add_config_value('kana_text_separator', _dflt_separator, 'env')
    app.add_config_value('kana_text_option_marker', _dflt_option_marker, 'env')
    app.add_config_value('kana_text_word_file', '', 'env')
    app.add_config_value('kana_text_word_list', (), 'env')
    app.add_config_value('kana_text_indexer_mode', 'small', 'env')
    app.add_config_value('kana_text_on_genindex', False, 'html')
    app.add_config_value('kana_text_change_triple', False, 'html')

    # バージョンの最後は作成日（MMDDYY）
    return {'version': __version__,
            'parallel_read_safe': True,
            'parallel_write_safe': True,
            }


# ------------------------------------------------------------


if __name__ in ('__main__', 'src'):
    import doctest
    doctest.testmod()
