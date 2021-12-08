"""
sphinxcontrib.kana_text
=======================

Class, Function
===============
"""

import re, pathlib
from typing import TYPE_CHECKING, Any, Dict, List, Tuple, Pattern, Type, cast

from docutils import nodes

from sphinx.domains.index import IndexRole
from sphinx.errors import NoUri
from sphinx.locale import _, __
from sphinx.util import logging, split_into, docutils
from sphinx.writers import html5

import sphindexer as idxr
from sphindexer.rack import UNIT_CLSF, UNIT_TERM, UNIT_SBTM
from sphindexer.glossary import BaseGlossary


__copyright__ = 'Copyright (C) 2021 @koKkekoh'
__license__ = 'BSD 2-Clause License'
__author__  = '@koKekkoh'
__version__ = '0.31.0' # 2021-12-07
__url__     = 'https://qiita.com/tags/sphinxcotrib.kana_text'


logger = logging.getLogger(__name__)


# ------------------------------------------------------------


_chop = re.compile(r'^\\')

_dflt_separator = r'\|'
_dflt_option_marker = r'\^'

def parser_for_kana_text(separator, option_marker):
    """かな|単語^オプション」を取り出す正規表現を作る.

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

#オプションに英字があるか
_a2z = re.compile(r'[a-zA-Z]')

#「かな|単語^オプション」の「オプション」の変換用
class _s2i:
    each_together = {
        'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5,
        'f': 6, 'g': 7, 'h': 8, 'i': 9
    }

    step_by_step = {
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
        elif o in _s2i.each_together: #ルビとしては使用しない
            t_end = t_s + _s2i.each_together[o]
            r_end = r_s + _s2i.each_together[o]
            rtn.append((False,word[t_s:t_end]))
        elif o in _s2i.step_by_step: #ルビとしては使用しない
            t_end = t_s + 1
            r_end = r_s + _s2i.step_by_step[o]
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

    - 内部表現としては「よみ|記載文字」をIDとして、他の情報は属性値として扱う.
    - 表示に於いては「記載文字」が同じであれば、同じ「読み」として処理する.
    - self.astext()を「表示すべき標準的な記載文字」を返すメソッドとする.
    """

    children = () #これでTextクラスと同じ扱いになる.
    config = None

    def __init__(self, rawword, rawsource=''):
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
        self._separator = separator
        self._option_marker = option_marker
        self.whatiam = 'term' #in('classifier', 'term')

        if not rawsource:
            rawsource = rawword

        delimiter = _chop.sub('', separator)

        parser = parser_for_kana_text(separator, option_marker)
        ideo, kana, ruby, option = self._parse_text(rawword.strip(), parser)

        super().__init__(rawsource, ideo=ideo, kana=kana, ruby=ruby, option=option,
                          null=not ideo, delimiter=delimiter)

    def __len__(self):
        if not self['kana'] is None: return 2
        if not self['ideo'] is None: return 1 #0.22.0: 'is None'を削除しても動作するように調整.
        raise ValueError(repr(self))

    def __eq__(self, other):
        """unittest用"""
        try:
            return self.as_identifier() == other.as_identifier()
        except AttributeError:
            return self.as_identifier() == other

    def __str__(self):
        """jinja2用"""
        try:
            # IndexRackで初めて設定されるので、タイミングによっては存在しない.
            parameter = self.kana_text_on_genindex
        except AttributeError:
            return self.astext()

        if self.whatiam == 'term' and parameter:
            return self.ashtml()
        else:
            return self.astext()

    def __repr__(self):
        """
        doctest:
            >>> kana = KanaText('はなこ|はな子^b1')
            >>> kana
            <KanaText: len=2 ruby='specific' option='b1' <#text: 'はなこ|はな子'>>
        """
        return self.asrepr()

    def asrepr(self):
        name = self.__class__.__name__
        if self['ideo']:
            prop = f"<{name}: len={len(self)} "
            if self['kana']:
                if len(self['ruby']) > 0:
                    prop += f"ruby='{self['ruby']}' "
                if len(self['option']) > 0:
                    prop += f"option='{self['option']}' "
                prop += f"<#text: '{self['kana']}|{self['ideo']}'>>"
            else:
                prop += f"<#text: '{self['ideo']}'>>"
            return prop
        elif self.rawsource:
            return f"<#rawsource: '{self.rawsource}'>"
        else:
            return "<#text: ''>"

    def _parse_text(self, text, parser):
        """
        doctest:

            >>> kana = KanaText('たなかはなこ|田中はな子^12b1')
            >>> kana
            <KanaText: len=2 ruby='specific' option='12b1' <#text: 'たなかはなこ|田中はな子'>>
        """
        match = parser.match(text)

        if not match:
            raise ValueError(self._rawword)

        _, _, kana, ideo, _, marker, opt = match.groups()

        # display mode of ruby
        if not kana  : ruby = ''  # off
        elif   opt   : ruby = 'specific'
        elif   marker: ruby = 'on'
        else         : ruby = ''  # off

        if not opt: opt = ''

        return ideo, kana, ruby, opt

    def astext(self):
        if self['ideo']: return self['ideo']
        return ''

    def assort(self):
        """表示順の調整

        classifierの場合
        1. 記号
        2. ２文字以上、英数字始まり
        3. １文字、日本語（英数字と記号以外）
        4. ２文字以上、かな文字
        5. １文字、英数字
        6. ２文字以上、英数字・かな文字以外（ほぼ漢字）
        """
        if self.whatiam != 'classifier':
            return self.as_identifier()

        key = self.as_identifier()
        if not key[0].isnumeric() and not key[0].upper().isalpha() and not key.startswith('_'):
            return (1, key)

        if len(key) > 1:
            if _a2z.match(key[0]) or key[0].isnumeric():
                return (2, key)
            if key[0] in _first_char.small:
                return (4, key)
            return (6, key)
        elif len(key) == 1:
            if _a2z.match(key) or key.isnumeric():
                return (5, key)
            return (3, key)

        raise ValueError(key)

    def as_identifier(self):
        if self['kana']: return self['kana'] + self['delimiter'] + self['ideo']
        if self['ideo']: return self['ideo']
        return ''

    def askana(self):
        """
        doctest:
            >>> kana = KanaText('たなかはなこ|田中はな子^12b1')
            >>> kana.askana()
            'たなかはなこ'
        """
        if len(self) == 2:
            return self['kana']
        if len(self) == 1:
            return ''
        # len(self) < 1の時は、__len__内でValueErrorが発生する

    def aslist(self):
        """
        doctest:
            >>> kana = KanaText('たなかはなこ|田中はな子^12b1')
            >>> kana.aslist()
            [(True, ('田', 'た')), (True, ('中', 'なか')), (False, 'はな'), (True, ('子', 'こ'))]
            >>> kana = KanaText('たなかはなこ|田中はな子^')
            >>> kana.aslist()
            [(True, ('田中はな子', 'たなかはなこ'))]
            >>> kana = KanaText('たなかはなこ|田中はな子')
            >>> kana.aslist()
            [(False, '田中はな子')]
        """

        if self['null']: return None

        ruby, option = self['ruby'], self['option']

        if len(self) == 1:
            ideo = self['ideo']
            if ideo:
                data = [(False, ideo)]
            else:
                raise ValueError(self._rawword, repr(self))
        elif not ruby:
            ideo = self['ideo']
            data = [(False, ideo), ]
        elif ruby == 'specific':  # 細かくルビの表示/非表示を指定する
            # アレコレがんばる
            ideo, kana = self['ideo'], self['kana']
            data = make_specific_by_parsing_option(ideo, kana, option)
        elif ruby == 'on':  # ルビを付ける。文字の割当位置は気にしない。
            ideo, kana = self['ideo'], self['kana']
            data = [(True, (ideo, kana))]
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
        for isruby, value in self.aslist():
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
        return nodes.unescape(self.astext())

    def astext(self):
        if self['template'] and len(self) == 1:
            return self['template'] % self[0].astext()

        if self.change_triple and len(self) == 2 and self['delimiter'] == ', ':
            return self[1].astext() + self['delimiter'] + self[0].astext()

        text = ""
        for subterm in self:
            text += subterm.astext() + self['delimiter']
        return text[:-len(self['delimiter'])]

    def assort(self):
        if self['template'] and len(self) == 1:
            return self['template'] % self[0].assort()

        if self.change_triple and len(self) == 2 and self['delimiter'] == ', ':
            return self[1].assort() + self['delimiter'] + self[0].assort()

        text = ""
        for subterm in self:
            text += subterm.assort() + self['delimiter']
        return text[:-len(self['delimiter'])]


class ExtIndexUnit(idxr.IndexUnit):
    def get_terms(self):
        terms = [self[1]]
        for s in self[2]:
            terms.append(s)
        return terms


class ExtIndexEntry(idxr.IndexEntry):

    textclass = KanaText
    packclass = ExtSubterm
    unitclass = ExtIndexUnit

    testmode = False

    def make_index_units(self):
        """
        sphinx/util/nodes.py
        
        - process_index_entryが参照するindextypesをしないと機能しないメソッド.
        - いずれどうにかしたいので、コードは残しておく.
        """

        if self['entry_type'] not in ('keys', 'pairs'):
            return super().make_index_units()

        if not self.testmode:
            message = 'see: process_index_entry and indextypes in sphinx/util/nodes.py'
            raise NotImplementedError(message)

        fn = self['file_name']
        tid = self['target']
        main = self['main']
        index_key = self['index_key']

        def _index_unit(term, sub1, sub2):
            link = self.type2link('uri')
            emphasis = self.main2code(main)

            if not sub1:
                sub1 = self.textclass('')
            if not sub2:
                sub2 = self.textclass('')
            subterm = self.packclass(link, sub1, sub2)

            index_unit = self.unitclass(term, subterm, link, emphasis, fn, tid, index_key)
            return index_unit

        index_units = []
        try:
            last = len(self) - 1
            for i in range(last):
                if self['entry_type'] == 'pairs':
                    index_units.append(_index_unit(self[last], self[i], ''))
                index_units.append(_index_unit(self[i], self[last], ''))
        except IndexError as err:
            raise IndexError(str(err), repr(self))
        except ValueError as err:
            logger.warning(str(err), location=fn)

        print(index_units)
        return index_units


# ------------------------------------------------------------


class _first_char(object):
    small = {
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
        'わ': 'わ', 'を': 'わ', 'ワ': 'わ', 'ヲ': 'わ', 'ん': 'わ', 'ン': 'わ'
        }

    large = {
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
        'わ': 'わ', 'を': 'を', 'ん': 'ん', 'ワ': 'わ', 'ヲ': 'を', 'ン': 'ん'
        }


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
    2. self.append() ExtIndexUnitの取り込み. self.update_units()の準備.
    3. self.update_units() 各unitの更新、並び替えの準備.
    4. self.sort_units() 並び替え.
    5. self.generate_genindex_data() genindex用データの生成.
    """

    textclass = KanaText
    packclass = ExtSubterm
    unitclass = ExtIndexUnit
    entryclass = ExtIndexEntry

    def __init__(self, builder, testmode=False):
        """rstファイル外にある読み仮名情報の取り込み."""

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
        - 更新処理のための全てのunitから情報を収集する.
        """
        # かな情報の収集
        self.put_in_kana_catalog(unit['main'], unit.get_terms())
        unit[UNIT_TERM].kana_text_on_genindex = self.config.kana_text_on_genindex

        # 残りの情報収集とrackへの格納.
        super().append(unit)

    def put_in_kana_catalog(self, emphasis, terms):
        """KanaText用の処理"""
        for term in terms:
            kana, ideo, ruby, spec = term.askana(), term.astext(), term['ruby'], term['option']
            if kana and ideo in self._kana_catalog:
                item = self._kana_catalog[ideo]
                if emphasis < item[0]:
                    # emphasisコードが異なる場合は、数字の小さい方が優先.
                    self._kana_catalog[ideo] = (emphasis, kana, ruby, spec)
                elif emphasis == item[0]:
                    # emphasisコードが同じなら、かな文字の長いほうが優先.
                    if len(kana) > len(item[1]):
                        self._kana_catalog[ideo] = (emphasis, kana, ruby, spec)
                    # かな文字の長さも同じなら、、
                    elif len(kana) == len(item[1]):
                        # 'specific'に限りオプションコードが多い方を採用する.
                        if ruby == 'specific' and ruby == item[2] and len(spec) > len(item[3]):
                            self._kana_catalog[ideo] = (emphasis, kana, ruby, spec)
                    else:
                        pass
                else:
                    # その他は、先に登録された方が優先. （∵「make clean」の有無に依存しない）
                    pass  # 明示しておく.
            elif kana:
                self._kana_catalog[ideo] = (emphasis, kana, ruby, spec)

    def make_classifier_from_first_letter(self, term):
        """
        先頭の一文字を必要な加工をして分類子に使う.
        """
        text = term.assort()
        try:
            # パラメータに応じて変換テーブルを使い分ける.
            if 'small' == self.config.kana_text_indexer_mode:
                return _first_char.small[text[:1]]
            elif 'large' == self.config.kana_text_indexer_mode:
                return _first_char.large[text[:1]]
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
            assert [unit[UNIT_TERM]]

            # 各termの読みの設定（「同じ単語は同じ読み」とする）

            self.update_term_with_kana_catalog(unit[UNIT_TERM])

            for subterm in unit[UNIT_SBTM]:
                self.update_term_with_kana_catalog(subterm)

            # kana_text_change_tripleの設定値を反映
            unit[UNIT_SBTM].change_triple = self.config.kana_text_change_triple

        # 残りの更新処理
        super().update_units()

    def update_term_with_kana_catalog(self, term):
        if term.astext() in self._kana_catalog:
            term['kana'] = self._kana_catalog[term.astext()][1]
            term['ruby'] = self._kana_catalog[term.astext()][2]
            term['option'] = self._kana_catalog[term.astext()][3]
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

    def visit_term(self, node: nodes.Element) -> None:
        """
        目的の文字列をKanaTextクラスにするための対応.
        後は、add_nodeで割り当てたメソッドが行う.
        """

        try:
            term = KanaText(node[0].rawsource)
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

    name = 'html'

    #def build(self, docnames, summary = None, method = 'update'):
    #    super().build(docnames, summary, method)
    #    nodes.Text = KanaText
    #エラーにならないだけで、HTMLTranslatorの代わりにはならない.

    def index_adapter(self) -> None:
        """索引の作成"""
        # 自前のIndexerを使う
        return ExtIndexRack(self).create_index()


class NormalHTMLBuilder(idxr.HTMLBuilder):
    """日本語対応なし版"""

    name = 'nokana'


# ------------------------------------------------------------


class ExtXRefIndex(idxr.XRefIndex):
    textclass = KanaText


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

    # glossaryディレクティブ
    app.add_directive("glossary", BaseGlossary)

    # HTML出力
    app.add_builder(ExtHTMLBuilder, True)
    app.set_translator('html', ExtHTML5Translator)

    # HTML出力/sphindexer/"make idxr"
    app.add_builder(NormalHTMLBuilder)

    # 設定の登録
    app.add_config_value('kana_text_separator', _dflt_separator, 'env')
    app.add_config_value('kana_text_option_marker', _dflt_option_marker, 'env')
    app.add_config_value('kana_text_word_file', '', 'env')
    app.add_config_value('kana_text_word_list', (), 'env')
    app.add_config_value('kana_text_indexer_mode', 'small', 'env')
    app.add_config_value('kana_text_on_genindex', False, 'html')
    app.add_config_value('kana_text_change_triple', False, 'html')

    # バージョン情報（x.y.z.[.n[.YYYYMMDD]]）
    return {'version': __version__,
            'parallel_read_safe': True,
            'parallel_write_safe': True,
            }


# ------------------------------------------------------------


if __name__ in ('__main__', 'src'):
    import doctest
    doctest.testmod()
