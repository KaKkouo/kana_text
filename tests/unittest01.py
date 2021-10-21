#!/usr/bin/python
import sys
import unittest
sys.path.append('sphinxcontrib')
from src import KanaText

#正規表現による字句解析
testcase1i = [
    #テストパターン
    "よみ１|用語１",
    "よみ２|用語２^120a3",
    "よみ３|用語３^",
    "よみ４|用語４^10a3あいうえお",
    "よみ５|用語５^あいうえお",
    "用語６",
    "用語７^120a3",
    "用語８^",
    "用語９^120a3あいうえお",
    "用語Ａ^あいうえお",
    "  よみ１|用語１",
    "  よみ２|用語２^120a3",
    "  よみ３|用語３^",
    "  よみ４|用語４^10a3あいうえお",
    "  よみ５|用語５^あいうえお",
    "  用語６",
    "  用語７^120a3",
    "  用語８^",
    "  用語９^10a3あいうえお",
    "  用語Ａ^あいうえお",
    " 　よみ１|用語１",
    " 　よみ２|用語２^120a3",
    " 　よみ３|用語３^",
    " 　よみ４|用語４^10a3あいうえお",
    " 　よみ５|用語５^あいうえお",
    " 　用語６",
    " 　用語７^120a3",
    " 　用語８^",
    " 　用語９^10a3あいうえお",
    " 　用語Ａ^あいうえお",
    "", "  ", " 　", ]

testcase1o = [   #想定する結果
    "よみ１|用語１",
    "よみ２|用語２",
    "よみ３|用語３",
    "よみ４|用語４",
    "よみ５|用語５",
    "用語６",
    "用語７",
    "用語８",
    "用語９",
    "用語Ａ",
    "よみ１|用語１",
    "よみ２|用語２",
    "よみ３|用語３",
    "よみ４|用語４",
    "よみ５|用語５",
    "用語６",
    "用語７",
    "用語８",
    "用語９",
    "用語Ａ",
    "よみ１|用語１",
    "よみ２|用語２",
    "よみ３|用語３",
    "よみ４|用語４",
    "よみ５|用語５",
    "用語６",
    "用語７",
    "用語８",
    "用語９",
    "用語Ａ",
    "", "", ""]

#オプションの処理
testcase2i = [
    #テストパターン
    "よみ１|用語１",
    "よみ２|用語２^120a3",
    "よみ３|用語３^",
    "よみ４|用語４^10a3あいうえお",
    "よみ５|用語５^あいうえお",
    "用語６",
    "用語７^120a3",
    "用語８^",
    "用語９^120a3あいうえお",
    "用語Ａ^あいうえお", ]

testcase2o = [   #想定する結果
    [(False, '用語１')],
    [(True, ('用', 'よ')), (True, ('語', 'み２')), (False, '２')],
    [(True, ('用語３', 'よみ３'))],
    [(True, ('用', 'よ')), (False, '語'), (False, '４')],
    [(True, ('用語５', 'よみ５'))],
    [(False, '用語６')],
    [(False, '用語７')],
    [(False, '用語８')],
    [(False, '用語９')],
    [(False, '用語Ａ')], ]

#オプションと文字データの文字数の多少
testcase3i = [ #テストケース
    'いろはにほへと|壱弐参四五六七八九',
    'いろはにほへと|壱弐参四五六七八九^',
    'いろはにほへと|壱弐参四五六七八九^111010111',
    'いろはにほへと|壱弐参四五六七八九^1201012',
    'いろはにほへと|壱弐参四五六七八九^33',
    'いろはにほへと|壱弐参四五六七八九^45',
    'いろはにほへと|壱弐参四五六七八九^55',
    'いろはにほへと|壱弐参四五六七八九^0000000000',
    'いろはにほへと|壱弐参四五六七八九^i9',
    'いろはにほへと|壱弐参四五六七八九^jkl7',
    'いろはにほへと|壱弐参四五六七八九^jkl9',
    'いろはにほへと|壱弐参四五六七八九^jkl55',
        ]

testcase3o = [   #期待する結果
    [(False, '壱弐参四五六七八九')],
    [(True, ('壱弐参四五六七八九', 'いろはにほへと'))],
    [  (True, ('壱', 'い')),
        (True, ('弐', 'ろ')),
        (True, ('参', 'は')),
        (False, '四'),
        (True, ('五', 'に')),
        (False, '六'),
        (True, ('七', 'ほ')),
        (True, ('八', 'へ')),
        (True, ('九', 'と'))],
    [  (True, ('壱', 'い')),
        (True, ('弐', 'ろは')),
        (False, '参'),
        (True, ('四', 'に')),
        (False, '五'),
        (True, ('六', 'ほ')),
        (True, ('七', 'へと')),
        (False, '八九')],
    [(True, ('壱', 'いろは')), (True, ('弐', 'にほへ')), (False, '参四五六七八九')],
    [(True, ('壱', 'いろはに')), (True, ('弐', 'ほへと')), (False, '参四五六七八九')],
    [(True, ('壱', 'いろはにほ')), (True, ('弐', 'へと')), (False, '参四五六七八九')],
    [  (False, '壱'), (False, '弐'), (False, '参'), (False, '四'), (False, '五'),
        (False, '六'), (False, '七'), (False, '八'), (False, '九')],
    [(False, '壱弐参四五六七八九')],
    [(True, ('壱', 'いろはにほへと')), (False, '弐参四五六七八九')],
    [(True, ('壱', 'いろはにほへと')), (False, '弐参四五六七八九')],
    [(True, ('壱', 'いろはにほ')), (True, ('弐', 'へと')), (False, '参四五六七八九')],
]

#非表示指定の「a-i」「q-y」の動作
testcase4i = [
    #テストケース
    # 1 2 3 4 5 6 7 8 9101112131415
    'いろはにほへとちりぬるをわかよ|壱弐参四五六七八九拾壱弐参四五',
    'いろはにほへとちりぬるをわかよ|壱弐参四五六七八九拾壱弐参四五^',
    'いろはにほへとちりぬるをわかよ|壱弐参四五六七八九拾壱弐参四五^1a1', #1
    'いろはにほへとちりぬるをわかよ|壱弐参四五六七八九拾壱弐参四五^1b1', #2
    'いろはにほへとちりぬるをわかよ|壱弐参四五六七八九拾壱弐参四五^1c1', #3
    'いろはにほへとちりぬるをわかよ|壱弐参四五六七八九拾壱弐参四五^1d1', #4
    'いろはにほへとちりぬるをわかよ|壱弐参四五六七八九拾壱弐参四五^1e1', #5
    'いろはにほへとちりぬるをわかよ|壱弐参四五六七八九拾壱弐参四五^1f1', #6
    'いろはにほへとちりぬるをわかよ|壱弐参四五六七八九拾壱弐参四五^1g1', #7
    'いろはにほへとちりぬるをわかよ|壱弐参四五六七八九拾壱弐参四五^1h1', #8
    'いろはにほへとちりぬるをわかよ|壱弐参四五六七八九拾壱弐参四五^1i1', #9
    'いろはにほへとちりぬるをわかよ|壱弐参四五六七八九拾壱弐参四五^1j1',
    'いろはにほへとちりぬるをわかよ|壱弐参四五六七八九拾壱弐参四五^1q1', #1
    'いろはにほへとちりぬるをわかよ|壱弐参四五六七八九拾壱弐参四五^1r1', #2
    'いろはにほへとちりぬるをわかよ|壱弐参四五六七八九拾壱弐参四五^1s1', #3
    'いろはにほへとちりぬるをわかよ|壱弐参四五六七八九拾壱弐参四五^1t1', #4
    'いろはにほへとちりぬるをわかよ|壱弐参四五六七八九拾壱弐参四五^1u1', #5
    'いろはにほへとちりぬるをわかよ|壱弐参四五六七八九拾壱弐参四五^1v1', #6
    'いろはにほへとちりぬるをわかよ|壱弐参四五六七八九拾壱弐参四五^1w1', #7
    'いろはにほへとちりぬるをわかよ|壱弐参四五六七八九拾壱弐参四五^1x1', #8
    'いろはにほへとちりぬるをわかよ|壱弐参四五六七八九拾壱弐参四五^1y1', #9
    'いろはにほへとちりぬるをわかよ|壱弐参四五六七八九拾壱弐参四五^1z1',
    'いろはにほへとちりぬるをわかよ|壱弐参四五六七八九拾壱弐参四五^ii', #99
    'いろはにほへとちりぬるをわかよ|壱弐参四五六七八九拾壱弐参四五^yy', #99
    'いろはにほへとちりぬるをわかよ|壱弐参四五六七八九拾壱弐参四五^1ii1', #99
    'いろはにほへとちりぬるをわかよ|壱弐参四五六七八九拾壱弐参四五^1yy1', #99
    'いろはにほへとちりぬるをわかよ|壱弐参四五六七八九拾壱弐参四五^1ff1', 
    'いろはにほへとちりぬるをわかよ|壱弐参四五六七八九拾壱弐参四五^1uu1', 
] 

testcase4o = [
    #期待する結果
    [(False, '壱弐参四五六七八九拾壱弐参四五')],
    [(True, ('壱弐参四五六七八九拾壱弐参四五', 'いろはにほへとちりぬるをわかよ'))],
    [(True, ('壱', 'い')),(False, '弐'),(True, ('参', 'は')),
        (False, '四五六七八九拾壱弐参四五')],
    [(True, ('壱', 'い')),(False, '弐参'),(True, ('四', 'に')),
        (False, '五六七八九拾壱弐参四五')],
    [(True, ('壱', 'い')),(False, '弐参四'),(True, ('五', 'ほ')),
        (False, '六七八九拾壱弐参四五')],
    [(True, ('壱', 'い')),(False, '弐参四五'),(True, ('六', 'へ')),
        (False, '七八九拾壱弐参四五')],
    [(True, ('壱', 'い')),(False, '弐参四五六'),(True, ('七', 'と')),
        (False, '八九拾壱弐参四五')],
    [(True, ('壱', 'い')),(False, '弐参四五六七'),(True, ('八', 'ち')),
        (False, '九拾壱弐参四五')],
    [(True, ('壱', 'い')),(False, '弐参四五六七八'),(True, ('九', 'り')),
        (False, '拾壱弐参四五')],
    [(True, ('壱', 'い')),(False, '弐参四五六七八九'),(True, ('拾', 'ぬ')),
        (False, '壱弐参四五')],
    [(True, ('壱', 'い')),(False, '弐参四五六七八九拾'),(True, ('壱', 'る')),
        (False, '弐参四五')],
    [(True, ('壱', 'い')), (True, ('弐', 'ろ')), (False, '参四五六七八九拾壱弐参四五')],
    [(True, ('壱', 'い')), (False, '弐'),
        (True, ('参', 'は')), (False, '四五六七八九拾壱弐参四五')],
    [(True, ('壱', 'い')), (False, '弐'),
        (True, ('参', 'に')), (False, '四五六七八九拾壱弐参四五')],
    [(True, ('壱', 'い')), (False, '弐'),
        (True, ('参', 'ほ')), (False, '四五六七八九拾壱弐参四五')],
    [(True, ('壱', 'い')), (False, '弐'),
        (True, ('参', 'へ')), (False, '四五六七八九拾壱弐参四五')],
    [(True, ('壱', 'い')), (False, '弐'),
        (True, ('参', 'と')), (False, '四五六七八九拾壱弐参四五')],
    [(True, ('壱', 'い')), (False, '弐'),
        (True, ('参', 'ち')), (False, '四五六七八九拾壱弐参四五')],
    [(True, ('壱', 'い')), (False, '弐'),
        (True, ('参', 'り')), (False, '四五六七八九拾壱弐参四五')],
    [(True, ('壱', 'い')), (False, '弐'),
        (True, ('参', 'ぬ')), (False, '四五六七八九拾壱弐参四五')],
    [(True, ('壱', 'い')), (False, '弐'),
        (True, ('参', 'る')), (False, '四五六七八九拾壱弐参四五')],
    [(True, ('壱', 'い')), (True, ('弐', 'ろ')), (False, '参四五六七八九拾壱弐参四五')],
    [(False, '壱弐参四五六七八九'), (False, '拾壱弐参四五')],
    [(False, '壱'), (False, '弐'), (False, '参四五六七八九拾壱弐参四五')],
    [(True, ('壱', 'い')), (False, '弐参四五六七八九拾'), (False, '壱弐参四五')],
    [(True, ('壱', 'い')), (False, '弐'), (False, '参'), (False, '四五六七八九拾壱弐参四五')],
    [(True, ('壱', 'い')), (False, '弐参四五六七'),
        (False, '八九拾壱弐参'), (True, ('四', 'か')), (False, '五')],
    [(True, ('壱', 'い')), (False, '弐'), (False, '参'), (True, ('四', 'を')),
        (False, '五六七八九拾壱弐参四五')],
]

#未入力/扱えない文字列
testcase5i = [
    '', '  ', '　　',
    'かな|^',
    ]

testcase5o = [None, None, None, None]

#self.ashier()の基本チェック
testcase6i = testcase1i

testcase6o = [   #想定する結果
    "用語１", "用語２", "用語３", "用語４", "用語５",
    "用語６", "用語７", "用語８", "用語９", "用語Ａ",
    "用語１", "用語２", "用語３", "用語４", "用語５",
    "用語６", "用語７", "用語８", "用語９", "用語Ａ",
    "用語１", "用語２", "用語３", "用語４", "用語５",
    "用語６", "用語７", "用語８", "用語９", "用語Ａ",
    "", "", ""]

#askana()の基本チェック
testcase7i = testcase1i

testcase7o = [   #想定する結果
    "よみ１", "よみ２", "よみ３", "よみ４", "よみ５", "", "", "", "", "",
    "よみ１", "よみ２", "よみ３", "よみ４", "よみ５", "", "", "", "", "",
    "よみ１", "よみ２", "よみ３", "よみ４", "よみ５", "", "", "", "", "",
    "", "", ""
    ]

#len()の基本チェック
testcase8i = testcase1i

testcase8o = [   #想定する結果
    2, 2, 2, 2, 2, 1, 1, 1, 1, 1,
    2, 2, 2, 2, 2, 1, 1, 1, 1, 1,
    2, 2, 2, 2, 2, 1, 1, 1, 1, 1,
    #0, 0, 0, #0.22.0/対応保留
    ]

class testKanaText(unittest.TestCase):
    #正規表現による字句解析
    def test01_astext(self):
        for t, e in zip(testcase1i, testcase1o):
            term = KanaText(t)
            rslt = term.astext()
            self.assertEqual(e, rslt)

    #オプションの処理
    def test02_asruby(self):
        for t, e in zip(testcase2i, testcase2o):
            term = KanaText(t)
            rslt = term.asruby()
            self.assertEqual(e, rslt)

    #オプションと文字データの文字数の多少
    def test03_asruby(self):
        for t, e in zip(testcase3i, testcase3o):
            term = KanaText(t)
            rslt = term.asruby()
            self.assertEqual(e, rslt)

    #非表示指定の「a-i」「q-y」の動作
    def test04_asruby(self):
        for t, e in zip(testcase4i, testcase4o):
            term = KanaText(t)
            rslt = term.asruby()
            self.assertEqual(e, rslt)

    #非表示指定の「a-i」「q-y」の動作
    def test05_asruby(self):
        for t, e in zip(testcase5i, testcase5o):
            term = KanaText(t)
            rslt = term.asruby()
            self.assertEqual(e, rslt)

    #ashierの基本チェック
    def test06_ashier(self):
        for t, e in zip(testcase6i, testcase6o):
            term = KanaText(t)
            rslt = term.ashier()
            self.assertEqual(e, rslt)

    #askanaの基本チェック
    def test07_askana(self):
        for t, e in zip(testcase7i, testcase7o):
            term = KanaText(t)
            rslt = term.askana()
            self.assertEqual(e, rslt)

    #lenで基本チェック
    def test08_len(self):
        for t, e in zip(testcase8i, testcase8o):
            term = KanaText(t)
            rslt = len(term)
            self.assertEqual(e, rslt)

def main():
    unittest.main()

if __name__ == '__main__':
    unittest.main()