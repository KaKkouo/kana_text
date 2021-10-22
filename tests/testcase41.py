#!/usr/bin/python3.8
import sys
import unittest
from pprint import pprint
sys.path.append('sphinxcontrib')
from src import IndexRack
from . import util

#-------------------------------------------------------------------

testcase01in = { #テストパターン
    'doc3': [
        ('single','あああ','id-311','',None),
        ('single','ううう','id-313','main',None),
        ('single','おおお','id-315','',None),
        ('single','あああ','id-316','main',None),
        ('single','ううう','id-318','',None),
        ('single','おおお','id-310','main',None),
        ('pair','あああ; かかか','id-321','',None),
        ('pair','ううう; くくく','id-323','main',None),
        ('pair','おおお; こここ','id-325','',None),
        ('pair','あああ; かかか','id-326','main',None),
        ('pair','ううう; くくく','id-328','',None),
        ('pair','おおお; こここ','id-320','main',None),
        ('triple','あああ; かかか; さささ','id-331','',None),
        ('triple','ううう; くくく; すすす','id-333','main',None),
        ('triple','おおお; こここ; そそそ','id-335','','分類'),
        ('triple','あああ; かかか; さささ','id-336','main',None),
        ('triple','ううう; くくく; すすす','id-338','',None),
        ('triple','おおお; こここ; そそそ','id-330','main',None),
        ('single','あああ; かかか','id-341','',None),
        ('single','ううう; くくく','id-343','main',None),
        ('single','おおお; こここ','id-345','',None),
        ('single','あああ; かかか','id-346','main',None),
        ('single','ううう; くくく','id-348','',None),
        ('single','おおお; こここ','id-340','main',None),
    ],
    'doc1': [
        ('single','おおお; こここ','id-140','main',None),
        ('single','ううう; くくく','id-148','main',None),
        ('single','あああ; かかか','id-146','main',None),
        ('single','あああ; かかか','id-141','',None),
        ('triple','おおお; こここ; そそそ','id-130','main',None),
        ('triple','ううう; くくく; すすす','id-138','main','分類'),
        ('triple','あああ; かかか; さささ','id-136','main',None),
        ('triple','おおお; こここ; そそそ','id-135','',None),
        ('triple','ううう; くくく; すすす','id-133','',None),
        ('triple','あああ; かかか; さささ','id-131','','分類'),
        ('pair','おおお; こここ','id-120','main',None),
        ('pair','ううう; くくく','id-128','main',None),
        ('pair','あああ; かかか','id-126','main',None),
        ('pair','おおお; こここ','id-125','','分類'),
        ('pair','ううう; くくく','id-123','',None),
        ('pair','あああ; かかか','id-121','',None),
        ('single','おおお','id-110','main',None),
        ('single','ううう','id-118','main','分類'),
        ('single','あああ','id-116','main',None),
        ('single','おおお','id-115','',None),
        ('single','ううう','id-113','',None),
        ('single','あああ','id-111','','分類'),
        ('single','ううう; くくく','id-143','',None),
        ('single','おおお; こここ','id-145','','分類'),
    ],
    'doc2': [
        ('single','おおお','id-215','',None),
        ('single','ううう','id-213','',None),
        ('single','あああ','id-211','','分類'),
        ('single','あああ','id-216','main',None),
        ('single','ううう','id-218','main','分類'),
        ('single','おおお','id-210','main',None),
        ('pair','おおお; こここ','id-225','','分類'),
        ('pair','ううう; くくく','id-223','',None),
        ('pair','あああ; かかか','id-221','',None),
        ('pair','おおお; こここ','id-220','main',None),
        ('pair','ううう; くくく','id-228','main',None),
        ('pair','あああ; かかか','id-226','main',None),
        ('triple','おおお; こここ; そそそ','id-235','',None),
        ('triple','ううう; くくく; すすす','id-233','',None),
        ('triple','あああ; かかか; さささ','id-231','','分類'),
        ('triple','あああ; かかか; さささ','id-236','main',None),
        ('triple','ううう; くくく; すすす','id-238','main','分類'),
        ('triple','おおお; こここ; そそそ','id-230','main',None),
        ('single','おおお; こここ','id-245','','分類'),
        ('single','ううう; くくく','id-243','',None),
        ('single','あああ; かかか','id-241','',None),
        ('single','あああ; かかか','id-246','main',None),
        ('single','ううう; くくく','id-248','main',None),
        ('single','おおお; こここ','id-240','main',None),
    ],
}

testcase01out = [ #想定する結果
('分類',
    [('あああ',
      [[('main', 'doc1.html#id-116'),
        ('main', 'doc2.html#id-216'),
        ('main', 'doc3.html#id-316'),
        ('', 'doc1.html#id-111'),
        ('', 'doc2.html#id-211'),
        ('', 'doc3.html#id-311')],
       [('かかか',
         [('main', 'doc1.html#id-126'),
          ('main', 'doc1.html#id-146'),
          ('main', 'doc2.html#id-226'),
          ('main', 'doc2.html#id-246'),
          ('main', 'doc3.html#id-326'),
          ('main', 'doc3.html#id-346'),
          ('', 'doc1.html#id-121'),
          ('', 'doc1.html#id-141'),
          ('', 'doc2.html#id-221'),
          ('', 'doc2.html#id-241'),
          ('', 'doc3.html#id-321'),
          ('', 'doc3.html#id-341')]),
        ('かかか さささ',
         [('main', 'doc1.html#id-136'),
          ('main', 'doc2.html#id-236'),
          ('main', 'doc3.html#id-336'),
          ('', 'doc1.html#id-131'),
          ('', 'doc2.html#id-231'),
          ('', 'doc3.html#id-331')])],
       None]),
     ('ううう',
      [[('main', 'doc1.html#id-118'),
        ('main', 'doc2.html#id-218'),
        ('main', 'doc3.html#id-313'),
        ('', 'doc1.html#id-113'),
        ('', 'doc2.html#id-213'),
        ('', 'doc3.html#id-318')],
       [('くくく',
         [('main', 'doc1.html#id-128'),
          ('main', 'doc1.html#id-148'),
          ('main', 'doc2.html#id-228'),
          ('main', 'doc2.html#id-248'),
          ('main', 'doc3.html#id-323'),
          ('main', 'doc3.html#id-343'),
          ('', 'doc1.html#id-123'),
          ('', 'doc1.html#id-143'),
          ('', 'doc2.html#id-223'),
          ('', 'doc2.html#id-243'),
          ('', 'doc3.html#id-328'),
          ('', 'doc3.html#id-348')]),
        ('くくく すすす',
         [('main', 'doc1.html#id-138'),
          ('main', 'doc2.html#id-238'),
          ('main', 'doc3.html#id-333'),
          ('', 'doc1.html#id-133'),
          ('', 'doc2.html#id-233'),
          ('', 'doc3.html#id-338')])],
       '分類']),
     ('おおお',
      [[('main', 'doc1.html#id-110'),
        ('main', 'doc2.html#id-210'),
        ('main', 'doc3.html#id-310'),
        ('', 'doc1.html#id-115'),
        ('', 'doc2.html#id-215'),
        ('', 'doc3.html#id-315')],
       [('こここ',
         [('main', 'doc1.html#id-120'),
          ('main', 'doc1.html#id-140'),
          ('main', 'doc2.html#id-220'),
          ('main', 'doc2.html#id-240'),
          ('main', 'doc3.html#id-320'),
          ('main', 'doc3.html#id-340'),
          ('', 'doc1.html#id-125'),
          ('', 'doc1.html#id-145'),
          ('', 'doc2.html#id-225'),
          ('', 'doc2.html#id-245'),
          ('', 'doc3.html#id-325'),
          ('', 'doc3.html#id-345')]),
        ('こここ そそそ',
         [('main', 'doc1.html#id-130'),
          ('main', 'doc2.html#id-230'),
          ('main', 'doc3.html#id-330'),
          ('', 'doc1.html#id-135'),
          ('', 'doc2.html#id-235'),
          ('', 'doc3.html#id-335')])],
       None]),
     ('かかか',
      [[],
       [('あああ',
         [('main', 'doc1.html#id-126'),
          ('main', 'doc2.html#id-226'),
          ('main', 'doc3.html#id-326'),
          ('', 'doc1.html#id-121'),
          ('', 'doc2.html#id-221'),
          ('', 'doc3.html#id-321')]),
        ('さささ, あああ',
         [('main', 'doc1.html#id-136'),
          ('main', 'doc2.html#id-236'),
          ('main', 'doc3.html#id-336'),
          ('', 'doc1.html#id-131'),
          ('', 'doc2.html#id-231'),
          ('', 'doc3.html#id-331')])],
       None]),
     ('くくく',
      [[],
       [('ううう',
         [('main', 'doc1.html#id-128'),
          ('main', 'doc2.html#id-228'),
          ('main', 'doc3.html#id-323'),
          ('', 'doc1.html#id-123'),
          ('', 'doc2.html#id-223'),
          ('', 'doc3.html#id-328')]),
        ('すすす, ううう',
         [('main', 'doc1.html#id-138'),
          ('main', 'doc2.html#id-238'),
          ('main', 'doc3.html#id-333'),
          ('', 'doc1.html#id-133'),
          ('', 'doc2.html#id-233'),
          ('', 'doc3.html#id-338')])],
       None]),
     ('こここ',
      [[],
       [('おおお',
         [('main', 'doc1.html#id-120'),
          ('main', 'doc2.html#id-220'),
          ('main', 'doc3.html#id-320'),
          ('', 'doc1.html#id-125'),
          ('', 'doc2.html#id-225'),
          ('', 'doc3.html#id-325')]),
        ('そそそ, おおお',
         [('main', 'doc1.html#id-130'),
          ('main', 'doc2.html#id-230'),
          ('main', 'doc3.html#id-330'),
          ('', 'doc1.html#id-135'),
          ('', 'doc2.html#id-235'),
          ('', 'doc3.html#id-335')])],
       None]),
     ('さささ',
      [[],
       [('あああ かかか',
         [('main', 'doc1.html#id-136'),
          ('main', 'doc2.html#id-236'),
          ('main', 'doc3.html#id-336'),
          ('', 'doc1.html#id-131'),
          ('', 'doc2.html#id-231'),
          ('', 'doc3.html#id-331')])],
       None]),
     ('すすす',
      [[],
       [('ううう くくく',
         [('main', 'doc1.html#id-138'),
          ('main', 'doc2.html#id-238'),
          ('main', 'doc3.html#id-333'),
          ('', 'doc1.html#id-133'),
          ('', 'doc2.html#id-233'),
          ('', 'doc3.html#id-338')])],
       '分類']),
     ('そそそ',
      [[],
       [('おおお こここ',
         [('main', 'doc1.html#id-130'),
          ('main', 'doc2.html#id-230'),
          ('main', 'doc3.html#id-330'),
          ('', 'doc1.html#id-135'),
          ('', 'doc2.html#id-235'),
          ('', 'doc3.html#id-335')])],
       None])])
]

testcase02in = { #テストパターン
    'doc1': [
        ('single','あああ','id-311','',None),
        ('single','あああ','id-313','main',None),
        ('pair','あああ; かかか','id-321','',None),
        ('pair','あああ; くくく','id-323','main',None),
        ('triple','あああ; かかか; さささ','id-331','',None),
        ('triple','あああ; くくく; すすす','id-333','main',None),
        ('single','あああ; かかか','id-341','',None),
        ('single','あああ; くくく','id-343','main',None),
    ],
    'doc3': [
        ('single','あああ; こここ','id-140','main',None),
        ('single','あああ; くくく','id-148','main',None),
        ('triple','あああ; くくく; すすす','id-133','',None),
        ('triple','あああ; かかか; さささ','id-131','','分類'),
        ('pair','あああ; くくく','id-123','',None),
        ('pair','あああ; かかか','id-121','',None),
        ('single','あああ; くくく','id-143','',None),
        ('single','あああ; こここ','id-145','','分類'),
    ],
}

testcase02out = [
('く', [
  ('くくく', [
    [],
    [('あああ', [('main', 'doc1.html#id-323'), ('', 'doc3.html#id-123')]),
     ('すすす, あああ', [('main', 'doc1.html#id-333'), ('', 'doc3.html#id-133')])],
    None])]),
('す', [
  ('すすす', [
    [],
    [('あああ くくく', [('main', 'doc1.html#id-333'), ('', 'doc3.html#id-133')])],
    None])]),
('分類', [
  ('あああ', [
    [('main', 'doc1.html#id-313'), ('', 'doc1.html#id-311')],
    [('かかか', [
      ('', 'doc1.html#id-321'),
      ('', 'doc1.html#id-341'),
      ('', 'doc3.html#id-121')]),
     ('かかか さささ', [('', 'doc1.html#id-331'), ('', 'doc3.html#id-131')]),
     ('くくく', [
       ('main', 'doc1.html#id-323'),
       ('main', 'doc1.html#id-343'),
       ('main', 'doc3.html#id-148'),
       ('', 'doc3.html#id-123'),
       ('', 'doc3.html#id-143')]),
     ('くくく すすす', [('main', 'doc1.html#id-333'), ('', 'doc3.html#id-133')]),
     ('こここ', [('main', 'doc3.html#id-140'), ('', 'doc3.html#id-145')])],
    None]),
  ('かかか', [
    [],
    [('あああ', [('', 'doc1.html#id-321'), ('', 'doc3.html#id-121')]),
     ('さささ, あああ', [('', 'doc1.html#id-331'), ('', 'doc3.html#id-131')])],
    None]),
  ('さささ', [
    [],
    [('あああ かかか', [('', 'doc1.html#id-331'), ('', 'doc3.html#id-131')])],
    None])])
]

#同じ副用語は一つ
testcase03in = { #テストパターン
    'doc1': [
        ('single','あああ|太郎','id-311','',None),
        ('single','いいい|はな子; くくく|森の熊','id-343','main',None),
        ('pair','ううう|手紙; かかか|狸と狐','id-321','',None),
        ('triple','えええ|犬猫; かかか|子鹿; さささ|急須','id-331','',None),
    ],
    'doc3': [
        ('single','かかか|東京; くくく|戦斧','id-148','main',None),
        ('single','ききき|満月; くくく|騎士','id-143','',None),
        ('pair','くくく|月光; くくく|伯爵','id-123','',None),
        ('triple','けけけ|花見; かかか|男爵; さささ|機関室','id-131','',None),
    ],
}

testcase03out = [
 ('あ', [('あああ|太郎', [[('', 'doc1.html#id-311')], [], None])]),
 ('い',
  [('いいい|はな子', [[], [('くくく|森の熊', [('main', 'doc1.html#id-343')])], None])]),
 ('う', [('ううう|手紙', [[], [('かかか|狸と狐', [('', 'doc1.html#id-321')])], None])]),
 ('え',
  [('えええ|犬猫', [[], [('かかか|子鹿 さささ|急須', [('', 'doc1.html#id-331')])], None])]),
 ('か',
  [('かかか|子鹿', [[], [('さささ|急須, えええ|犬猫', [('', 'doc1.html#id-331')])], None]),
   ('かかか|東京', [[], [('くくく|戦斧', [('main', 'doc3.html#id-148')])], None]),
   ('かかか|狸と狐', [[], [('ううう|手紙', [('', 'doc1.html#id-321')])], None]),
   ('かかか|男爵', [[], [('さささ|機関室, けけけ|花見', [('', 'doc3.html#id-131')])], None])]),
 ('き', [('ききき|満月', [[], [('くくく|騎士', [('', 'doc3.html#id-143')])], None])]),
 ('く',
  [('くくく|伯爵', [[], [('くくく|月光', [('', 'doc3.html#id-123')])], None]),
   ('くくく|月光', [[], [('くくく|伯爵', [('', 'doc3.html#id-123')])], None])]),
 ('け',
  [('けけけ|花見', [[], [('かかか|男爵 さささ|機関室', [('', 'doc3.html#id-131')])], None])]),
 ('さ',
  [('さささ|急須', [[], [('えええ|犬猫 かかか|子鹿', [('', 'doc1.html#id-331')])], None]),
   ('さささ|機関室', [[], [('けけけ|花見 かかか|男爵', [('', 'doc3.html#id-131')])], None])])]

#ひらがなにまとめる
testcase04in = { #テストパターン
    'doc1': [
        ('single','ナナナ|太郎','id-311','',None),
        ('single','ニニニ|はな子; フフフ|森の熊','id-343','main',None),
        ('pair','ヌヌヌ|手紙; ハハハ|狸と狐','id-321','',None),
        ('triple','ネネネ|犬猫; ハハハ|子鹿; さささ|急須','id-331','',None),
    ],
    'doc3': [
        ('single','かかか|東京; くくく|戦斧','id-148','main',None),
        ('single','ききき|満月; くくく|騎士','id-143','',None),
        ('pair','くくく|月光; くくく|伯爵','id-123','',None),
        ('triple','けけけ|花見; かかか|男爵; さささ|機関室','id-131','',None),
    ],
}

testcase04out = [
  ('か',
   [('かかか|東京', [[], [('くくく|戦斧', [('main', 'doc3.html#id-148')])], None]),
    ('かかか|男爵', [[], [('さささ|機関室, けけけ|花見', [('', 'doc3.html#id-131')])], None])]),
  ('き', [('ききき|満月', [[], [('くくく|騎士', [('', 'doc3.html#id-143')])], None])]),
  ('く',
   [('くくく|伯爵', [[], [('くくく|月光', [('', 'doc3.html#id-123')])], None]),
    ('くくく|月光', [[], [('くくく|伯爵', [('', 'doc3.html#id-123')])], None])]),
  ('け',
   [('けけけ|花見', [[], [('かかか|男爵 さささ|機関室', [('', 'doc3.html#id-131')])], None])]),
  ('さ',
   [('さささ|急須', [[], [('ネネネ|犬猫 ハハハ|子鹿', [('', 'doc1.html#id-331')])], None]),
    ('さささ|機関室', [[], [('けけけ|花見 かかか|男爵', [('', 'doc3.html#id-131')])], None])]),
  ('な', [('ナナナ|太郎', [[('', 'doc1.html#id-311')], [], None])]),
  ('に',
   [('ニニニ|はな子', [[], [('フフフ|森の熊', [('main', 'doc1.html#id-343')])], None])]),
  ('ぬ', [('ヌヌヌ|手紙', [[], [('ハハハ|狸と狐', [('', 'doc1.html#id-321')])], None])]),
  ('ね',
   [('ネネネ|犬猫', [[], [('ハハハ|子鹿 さささ|急須', [('', 'doc1.html#id-331')])], None])]),
  ('は',
   [('ハハハ|子鹿', [[], [('さささ|急須, ネネネ|犬猫', [('', 'doc1.html#id-331')])], None]),
    ('ハハハ|狸と狐', [[], [('ヌヌヌ|手紙', [('', 'doc1.html#id-321')])], None])])
]

#あかさたな…にまとめる
testcase05in = { #テストパターン
    'doc1': [
        ('single','ナナナ|太郎','id-311','',None),
        ('single','ニニニ|はな子; フフフ|森の熊','id-343','main',None),
        ('pair','ヌヌヌ|手紙; ハハハ|狸と狐','id-321','',None),
        ('triple','ネネネ|犬猫; ハハハ|子鹿; さささ|急須','id-331','',None),
    ],
    'doc3': [
        ('single','かかか|東京; くくく|戦斧','id-148','main',None),
        ('single','ききき|満月; くくく|騎士','id-143','',None),
        ('pair','くくく|月光; くくく|伯爵','id-123','',None),
        ('triple','けけけ|花見; かかか|男爵; さささ|機関室','id-131','',None),
    ],
}

testcase05out = [
  ('か',
   [('かかか|東京', [[], [('くくく|戦斧', [('main', 'doc3.html#id-148')])], None]),
    ('かかか|男爵', [[], [('さささ|機関室, けけけ|花見', [('', 'doc3.html#id-131')])], None]),
    ('ききき|満月', [[], [('くくく|騎士', [('', 'doc3.html#id-143')])], None]),
    ('くくく|伯爵', [[], [('くくく|月光', [('', 'doc3.html#id-123')])], None]),
    ('くくく|月光', [[], [('くくく|伯爵', [('', 'doc3.html#id-123')])], None]),
    ('けけけ|花見', [[], [('かかか|男爵 さささ|機関室', [('', 'doc3.html#id-131')])], None])]),
  ('さ',
   [('さささ|急須', [[], [('ネネネ|犬猫 ハハハ|子鹿', [('', 'doc1.html#id-331')])], None]),
    ('さささ|機関室', [[], [('けけけ|花見 かかか|男爵', [('', 'doc3.html#id-131')])], None])]),
  ('な',
   [('ナナナ|太郎', [[('', 'doc1.html#id-311')], [], None]),
    ('ニニニ|はな子', [[], [('フフフ|森の熊', [('main', 'doc1.html#id-343')])], None]),
    ('ヌヌヌ|手紙', [[], [('ハハハ|狸と狐', [('', 'doc1.html#id-321')])], None]),
    ('ネネネ|犬猫', [[], [('ハハハ|子鹿 さささ|急須', [('', 'doc1.html#id-331')])], None])]),
  ('は',
   [('ハハハ|子鹿', [[], [('さささ|急須, ネネネ|犬猫', [('', 'doc1.html#id-331')])], None]),
    ('ハハハ|狸と狐', [[], [('ヌヌヌ|手紙', [('', 'doc1.html#id-321')])], None])])
]

#「ぱ」が「は」の項目に表示される.
testcase06in = { #テストパターン
'doc1': [ ('single','ナナナ|太郎','id-311','',None), ],
'doc2': [ ('single','ニニニ|はな子; フフフ|森の熊','id-343','main',None), ], #KaKkou
'doc3': [ ('pair','ヌヌヌ|手紙; ハハハ|狸と狐','id-321','',None), ],
'doc4': [ ('triple','ネネネ|犬猫; ハハハ|子鹿; さささ|急須','id-331','',None), ], #KaKkou
'doc5': [ ('single','かかか|東京; くくく|戦斧','id-148','main',None), ],
'doc6': [ ('single','ききき|満月; くくく|騎士','id-143','',None), ],
'doc7': [ ('single','ぱなぱな|はな子; ほほ|野良熊','id-343','main',None), ], #KaKkou
'doc8': [ ('pair','くくく|月光; くくく|伯爵','id-123','',None), ],
'doc9': [ ('triple','けけけ|花見; かかか|男爵; さささ|機関室','id-131','',None), ], #KaKkou
}

#「はなこ」だけ確認できればOK
testcase06out = [
('か',
 [('かかか|東京', [[], [('くくく|戦斧', [('main', 'doc5.html#id-148')])], None]),
  ('かかか|男爵', [[], [('さささ|機関室, けけけ|花見', [('', 'doc9.html#id-131')])], None]),
  ('ききき|満月', [[], [('くくく|騎士', [('', 'doc6.html#id-143')])], None]),
  ('くくく|伯爵', [[], [('くくく|月光', [('', 'doc8.html#id-123')])], None]),
  ('くくく|月光', [[], [('くくく|伯爵', [('', 'doc8.html#id-123')])], None]),
  ('けけけ|花見', [[], [('かかか|男爵 さささ|機関室', [('', 'doc9.html#id-131')])], None])]),
('さ',
 [('さささ|急須', [[], [('ネネネ|犬猫 ハハハ|子鹿', [('', 'doc4.html#id-331')])], None]),
  ('さささ|機関室', [[], [('けけけ|花見 かかか|男爵', [('', 'doc9.html#id-131')])], None])]),
('な',
 [('ナナナ|太郎', [[('', 'doc1.html#id-311')], [], None]),
  ('ヌヌヌ|手紙', [[], [('ハハハ|狸と狐', [('', 'doc3.html#id-321')])], None]),
  ('ネネネ|犬猫', [[], [('ハハハ|子鹿 さささ|急須', [('', 'doc4.html#id-331')])], None])]),
('は',
 [('ぱなぱな|はな子',
   [[],
    [('ほほ|野良熊', [('main', 'doc7.html#id-343')]),
     ('フフフ|森の熊', [('main', 'doc2.html#id-343')])],
    None]),
  ('ハハハ|子鹿', [[], [('さささ|急須, ネネネ|犬猫', [('', 'doc4.html#id-331')])], None]),
  ('ハハハ|狸と狐', [[], [('ヌヌヌ|手紙', [('', 'doc3.html#id-321')])], None])])
]

#-------------------------------------------------------------------

class testIndexRack(unittest.TestCase):
    def test01_create_genindex(self):
        self.maxDiff = None
        env = util.env(testcase01in)
        bld = util.builder(env)
        idx = IndexRack(bld)
        gidx = idx.create_genindex()
        self.assertEqual(gidx, testcase01out)

    def test02_create_genindex(self):
        self.maxDiff = None
        env = util.env(testcase02in)
        bld = util.builder(env)
        idx = IndexRack(bld)
        gidx = idx.create_genindex()
        self.assertEqual(gidx, testcase02out)

    def test03_create_genindex(self):
        self.maxDiff = None
        env = util.env(testcase03in)
        bld = util.builder(env)
        idx = IndexRack(bld)
        gidx = idx.create_genindex()
        self.assertEqual(gidx, testcase03out)

    def test04_first_letter_of_term(self):
        self.maxDiff = None
        env = util.env(testcase04in)
        bld = util.builder(env)
        bld.config.kana_text_indexer_mode = 'large'
        idx = IndexRack(bld)
        gidx = idx.create_genindex()
        self.assertEqual(gidx, testcase04out)

    def test05_first_letter_of_term(self):
        self.maxDiff = None
        env = util.env(testcase05in)
        bld = util.builder(env)
        bld.config.kana_text_indexer_mode = 'small'
        idx = IndexRack(bld)
        gidx = idx.create_genindex()
        self.assertEqual(gidx, testcase05out)

    def test06_first_letter_of_term(self):
        self.maxDiff = None
        env = util.env(testcase06in)
        bld = util.builder(env)
        bld.config.kana_text_indexer_mode = 'small'
        idx = IndexRack(bld)
        gidx = idx.create_genindex()
        self.assertEqual(gidx, testcase06out)

#-------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()

    #bld.config.kana_text_indexer_mode = 'small'
    #gidx = bld.create_genindex(testcase08in)
    #pprint(gidx)
