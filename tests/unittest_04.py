#!/usr/bin/python3.8
import sys
import unittest
from pprint import pprint
sys.path.append('sphinxcontrib')
from src import IndexRack

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


#同じ単語なら同じ読み（細かく検証）
testcase07in = {
'doc01b': [('single','むむ|検証０１','id-01b','',None)],
'doc01a': [('single','ああ|検証０１','id-01a','',None)],
'doc01c': [('single','をを|検証０１','id-01c','',None)], #KaKkou
'doc02a': [('single','ああ|検証０２','id-02a','',None)],
'doc02b': [('single','むむ|検証０２','id-02b','main',None)], #KaKkou
'doc02c': [('single','をを|検証０２','id-02c','',None)],
'doc03a': [('single','ああ|検証０３','id-03a','',None)],
'doc03b': [('single',  'む|検証０３','id-03b','main',None)], #KaKkou
'doc03c': [('single','をを|検証０３','id-03c','',None)],
'doc04a': [('single',  'あ|検証０４','id-04a','',None)],
'doc04b': [('single','むむ|検証０４','id-04b','',None)], #KaKkou
'doc04c': [('single',  'を|検証０４','id-04c','',None)],
'doc05a': [('single','ああ|検証０５; いい|検証０５','id-05a','',None)],
'doc05b': [('single','むむ|検証０５; めめ|検証０５','id-05b','main',None)], #KaKkou
'doc05c': [('single','をを|検証０５; んん|検証０５','id-05c','',None)],
'doc06a': [('single','ああ|検証０６; いい|検証０６','id-06a','',None)],
'doc06b': [('single',  'む|検証０６; めめ|検証０６','id-06b','main',None)], #KaKkou
'doc06c': [('single','をを|検証０６; んん|検証０６','id-06c','',None)],
'doc07a': [('pair','ああ|検証０７; いい|検証０７','id-07a','',None)],
'doc07b': [('pair','むむ|検証０７; めめ|検証０７','id-07b','main',None)],
'doc07c': [('pair','をを|検証０７; んん|検証０７','id-07c','',None)],
'doc08a': [('pair','ああ|検証０８; いい|検証０８','id-08a','',None)],
'doc08b': [('pair',  'む|検証０８; めめ|検証０８','id-08b','main',None)],
'doc08c': [('pair','をを|検証０８; んん|検証０８','id-08c','',None),],
}

testcase07out = [
('ま',
  [('む|検証０３',
    [[('main', 'doc03b.html#id-03b'),
      ('', 'doc03a.html#id-03a'),
      ('', 'doc03c.html#id-03c')],
     [],
     None]),
   ('むむ|検証０１',
    [[('', 'doc01a.html#id-01a'),
      ('', 'doc01b.html#id-01b'),
      ('', 'doc01c.html#id-01c')],
     [],
     None]),
   ('むむ|検証０２',
    [[('main', 'doc02b.html#id-02b'),
      ('', 'doc02a.html#id-02a'),
      ('', 'doc02c.html#id-02c')],
     [],
     None]),
   ('むむ|検証０４',
    [[('', 'doc04a.html#id-04a'),
      ('', 'doc04b.html#id-04b'),
      ('', 'doc04c.html#id-04c')],
     [],
     None]),
   ('むむ|検証０５',
    [[],
     [('むむ|検証０５',
       [('main', 'doc05b.html#id-05b'),
        ('', 'doc05a.html#id-05a'),
        ('', 'doc05c.html#id-05c')])],
     None]),
   ('むむ|検証０７',
    [[],
     [('むむ|検証０７',
       [('main', 'doc07b.html#id-07b'),
        ('main', 'doc07b.html#id-07b'),
        ('', 'doc07a.html#id-07a'),
        ('', 'doc07a.html#id-07a'),
        ('', 'doc07c.html#id-07c'),
        ('', 'doc07c.html#id-07c')])],
     None]),
   ('めめ|検証０６',
    [[],
     [('めめ|検証０６',
       [('main', 'doc06b.html#id-06b'),
        ('', 'doc06a.html#id-06a'),
        ('', 'doc06c.html#id-06c')])],
     None]),
   ('めめ|検証０８',
    [[],
     [('めめ|検証０８',
       [('main', 'doc08b.html#id-08b'),
        ('main', 'doc08b.html#id-08b'),
        ('', 'doc08a.html#id-08a'),
        ('', 'doc08a.html#id-08a'),
        ('', 'doc08c.html#id-08c'),
        ('', 'doc08c.html#id-08c')])],
     None])])
]

testcase07out_ = [ #0.21までの実装での挙動
('ま',
 [('む|検証０３',
   [[('main', 'doc03b.html#id-03b'),
     ('', 'doc03a.html#id-03a'),
     ('', 'doc03c.html#id-03c')],
    [],
    None]),
  ('む|検証０６',
   [[],
    [('いい|検証０６', [('', 'doc06a.html#id-06a')]),
     ('めめ|検証０６', [('main', 'doc06b.html#id-06b')]),
     ('んん|検証０６', [('', 'doc06c.html#id-06c')])],
    None]),
  ('むむ|検証０１',
   [[('', 'doc01a.html#id-01a'),
     ('', 'doc01b.html#id-01b'),
     ('', 'doc01c.html#id-01c')],
    [],
    None]),
  ('むむ|検証０２',
   [[('main', 'doc02b.html#id-02b'),
     ('', 'doc02a.html#id-02a'),
     ('', 'doc02c.html#id-02c')],
    [],
    None]),
  ('むむ|検証０４',
   [[('', 'doc04a.html#id-04a'),
     ('', 'doc04b.html#id-04b'),
     ('', 'doc04c.html#id-04c')],
    [],
    None]),
  ('むむ|検証０５',
   [[],
    [('いい|検証０５', [('', 'doc05a.html#id-05a')]),
     ('めめ|検証０５', [('main', 'doc05b.html#id-05b')]),
     ('んん|検証０５', [('', 'doc05c.html#id-05c')])],
    None]),
  ('むむ|検証０７',
   [[],
    [('ああ|検証０７', [('', 'doc07a.html#id-07a')]),
     ('いい|検証０７', [('', 'doc07a.html#id-07a')]),
     ('むむ|検証０７', [('main', 'doc07b.html#id-07b')]),
     ('めめ|検証０７', [('main', 'doc07b.html#id-07b')]),
     ('をを|検証０７', [('', 'doc07c.html#id-07c')]),
     ('んん|検証０７', [('', 'doc07c.html#id-07c')])],
    None]),
  ('めめ|検証０８',
   [[],
    [('ああ|検証０８', [('', 'doc08a.html#id-08a')]),
     ('いい|検証０８', [('', 'doc08a.html#id-08a')]),
     ('む|検証０８', [('main', 'doc08b.html#id-08b')]),
     ('めめ|検証０８', [('main', 'doc08b.html#id-08b')]),
     ('をを|検証０８', [('', 'doc08c.html#id-08c')]),
     ('んん|検証０８', [('', 'doc08c.html#id-08c')])],
    None])])
]

#同じ単語なら同じ読み（triple）
testcase08in = {
'doc09a': [('triple','ああ|球球球; いい|球球球; そそ|球球球','id-09a','',None)],
'doc09b': [('triple','むむ|球球球; めめ|球球球; もも|球球球','id-09b','main',None)],
'doc09c': [('triple','をを|球球球; んん|球球球; ろろ|球球球','id-09c','',None)],
'doc10a': [('triple','ああ|拾拾拾; いい|拾拾拾; そそ|拾拾拾','id-10a','',None)],
'doc10b': [('triple',  'む|拾拾拾; めめ|拾拾拾; もも|拾拾拾','id-10b','main',None)],
'doc10c': [('triple','をを|拾拾拾; んん|拾拾拾; ろろ|拾拾拾','id-10c','',None)],
}

testcase08out = [
('ま',
  [('むむ|球球球',
    [[],
     [('むむ|球球球 むむ|球球球', #seeのデリミタ仕様
       [('main', 'doc09b.html#id-09b'),
        ('main', 'doc09b.html#id-09b'),
        ('', 'doc09a.html#id-09a'),
        ('', 'doc09a.html#id-09a'),
        ('', 'doc09c.html#id-09c'),
        ('', 'doc09c.html#id-09c')]),
      ('むむ|球球球, むむ|球球球', #seealsoのデリミタ仕様
       [('main', 'doc09b.html#id-09b'),
        ('', 'doc09a.html#id-09a'),
        ('', 'doc09c.html#id-09c')])],
     None]),
   ('めめ|拾拾拾',
    [[],
     [('めめ|拾拾拾 めめ|拾拾拾', #seeのデリミタ仕様
       [('main', 'doc10b.html#id-10b'),
        ('main', 'doc10b.html#id-10b'),
        ('', 'doc10a.html#id-10a'),
        ('', 'doc10a.html#id-10a'),
        ('', 'doc10c.html#id-10c'),
        ('', 'doc10c.html#id-10c')]),
      ('めめ|拾拾拾, めめ|拾拾拾', #seealsoのデリミタ仕様
       [('main', 'doc10b.html#id-10b'),
        ('', 'doc10a.html#id-10a'),
        ('', 'doc10c.html#id-10c')])],
     None])])
]

#同名の関数が複数のモジュールにある
testcase09in = {
'doc01a': [('single','function1() (aaa モジュール)','id-01a','',None)],
'doc01b': [('single','function1() (bbb モジュール)','id-01b','',None)],
'doc01c': [('single','function1() (ccc モジュール)','id-01c','',None)],
'doc01d': [('single','function1() (ddd モジュール)','id-01d','',None)],
'doc01e1': [('single','function1() (eee モジュール)','id-01e1','',None)],
'doc01e2': [('single','function1() (eee モジュール)','id-01e2','main',None)],
'doc01e3': [('single','function1() (eee モジュール)','id-01e3','',None)],
'doc01e4': [('single','function1() (eee モジュール)','id-01e4','main',None)],
'doc01f1': [('single','function1() (fff モジュール)','id-01f1','main',None)],
'doc01f2': [('single','function1() (fff モジュール)','id-01f2','main',None)],
}

testcase09out = [
  ('F',
   [('function1()',
     [[],
      [('(aaa モジュール)', [('', 'doc01a.html#id-01a')]),
       ('(bbb モジュール)', [('', 'doc01b.html#id-01b')]),
       ('(ccc モジュール)', [('', 'doc01c.html#id-01c')]),
       ('(ddd モジュール)', [('', 'doc01d.html#id-01d')]),
       ('(eee モジュール)',
        [('main', 'doc01e2.html#id-01e2'),
         ('main', 'doc01e4.html#id-01e4'),
         ('', 'doc01e1.html#id-01e1'),
         ('', 'doc01e3.html#id-01e3')]),
       ('(fff モジュール)',
        [('main', 'doc01f1.html#id-01f1'), ('main', 'doc01f2.html#id-01f2')])],
      None])])
]

#同じ単語なら読みを揃える

testcase10in = {
'doc01': [('single','ああ|球球球; いい|球球球','id-01','',None)],
'doc02': [('see','かか|球球球; めめ|球球球','id-02','',None)],
'doc03': [('single','ささ|球球球; んん|球球球','id-03','',None)],
'doc04': [('seealso','たた|拾拾拾; いい|拾拾拾','id-04','',None)],
'doc05': [('single','なな|拾拾拾; めめ|拾拾拾','id-05','',None)],
'doc06': [('single','おお|拾拾拾; んん|拾拾拾','id-06','',None)],
}

testcase10out = [
('あ',
  [('ああ|球球球',
    [[],
     [('ああ|球球球', [('', 'doc01.html#id-01'), ('', 'doc03.html#id-03')]),
      ('see 球球球', [])],
     None])]),
 ('な',
  [('なな|拾拾拾',
    [[],
     [('なな|拾拾拾', [('', 'doc05.html#id-05'), ('', 'doc06.html#id-06')]),
      ('see also 拾拾拾', [])],
     None])])
]

#同名の関数がある場合とない場合
testcase11in = {
'doc01a': [('single','function1() (aaa モジュール)','id-01a','',None)],
'doc01b': [('single','function1() (bbb モジュール)','id-01b','',None)],
'doc01c': [('single','function3() (ccc モジュール)','id-01c','',None)],
'doc01d': [('single','function4() (ddd モジュール)','id-01d','',None)],
'doc01e1': [('single','function2() (eee モジュール)','id-01e1','',None)],
'doc01e2': [('single','function1() (eee モジュール)','id-01e2','main',None)],
'doc01e3': [('single','function1() (eee モジュール)','id-01e3','',None)],
'doc01e4': [('single','function1() (eee モジュール)','id-01e4','main',None)],
'doc01f1': [('single','function1() (fff モジュール)','id-01f1','main',None)],
'doc01f2': [('single','function1() (fff モジュール)','id-01f2','main',None)],
}

testcase11out = [
  ('F',
    [('function1()',
      [[],
       [('(aaa モジュール)', [('', 'doc01a.html#id-01a')]),
        ('(bbb モジュール)', [('', 'doc01b.html#id-01b')]),
        ('(eee モジュール)',
         [('main', 'doc01e2.html#id-01e2'),
          ('main', 'doc01e4.html#id-01e4'),
          ('', 'doc01e3.html#id-01e3')]),
        ('(fff モジュール)',
         [('main', 'doc01f1.html#id-01f1'), ('main', 'doc01f2.html#id-01f2')])],
       None]),
     ('function2() (eee モジュール)', [[('', 'doc01e1.html#id-01e1')], [], None]),
     ('function3() (ccc モジュール)', [[('', 'doc01c.html#id-01c')], [], None]),
     ('function4() (ddd モジュール)', [[('', 'doc01d.html#id-01d')], [], None])])
]


#html_kana_text_on_genindex = True
testcase12in = {
'doc04': [('single','にに|四四^11; へへ|六六^11','id-04','',None)],
'doc03': [('single','にに|四四^11; ほほ|五五^11','id-03','', '分類子')],
'doc02': [('single','いい|壱壱^11; はは|参参^11','id-02','',None)],
'doc01': [('single','いい|壱壱^11; ろろ|弐弐^11','id-01','',None)],
}

testcase12out = [
('あ',
  [([(True, ('壱', 'い')), (True, ('壱', 'い'))],
    [[],
     [('参参', [('', 'doc02.html#id-02')]),
      ('弐弐', [('', 'doc01.html#id-01')])],
     None])]),
 ('分類子',
  [([(True, ('四', 'に')), (True, ('四', 'に'))],
    [[],
     [('六六', [('', 'doc04.html#id-04')]),
      ('五五', [('', 'doc03.html#id-03')])],
     None])])
]

#同名の関数がある場合とない場合
testcase13in = {
'doc01a': [('single','function1() (aaa モジュール)','id-01a','',None)],
}

testcase13out = [
('F',
  [('function1() (aaa モジュール)',
    [[('', 'doc01a.html#id-01a')], [], None])])]

#同名の関数がある場合とない場合
testcase14in = {
'doc01a': [('single','function1() (aaa モジュール)','id-01a','',None)],
'doc01b': [('single','function1() (bbb モジュール)','id-01b','',None)],
}

testcase14out = [
('F',
  [('function1()',
    [[],
     [('(aaa モジュール)', [('', 'doc01a.html#id-01a')]),
      ('(bbb モジュール)', [('', 'doc01b.html#id-01b')])],
     None])])]

#同名の関数がある場合とない場合
testcase15in = {
'doc01a': [('single','function1() (aaa モジュール)','id-01a','',None)],
'doc01b': [('single','function1() (bbb モジュール)','id-01b','',None)],
'doc01c': [('single','function3() (ccc モジュール)','id-01c','',None)],
}

testcase15out = [
('F',
  [('function1()',
    [[],
     [('(aaa モジュール)', [('', 'doc01a.html#id-01a')]),
      ('(bbb モジュール)', [('', 'doc01b.html#id-01b')])],
     None]),
   ('function3() (ccc モジュール)',
    [[('', 'doc01c.html#id-01c')], [], None])
  ])
]

#同名の関数がある場合とない場合
testcase16in = {
'doc01a': [('single','function1() (aaa モジュール)','id-01a','',None)],
'doc01b': [('single','function1() (bbb モジュール)','id-01b','',None)],
'doc01c': [('single','function3() (ccc モジュール)','id-01c','',None)],
'doc01d': [('single','function4() (ddd モジュール)','id-01d','',None)],
}

testcase16out = [
('F',
  [('function1()',
    [[],
     [('(aaa モジュール)', [('', 'doc01a.html#id-01a')]),
      ('(bbb モジュール)', [('', 'doc01b.html#id-01b')])],
     None]),
   ('function3() (ccc モジュール)', [[('', 'doc01c.html#id-01c')], [], None]),
   ('function4() (ddd モジュール)', [[('', 'doc01d.html#id-01d')], [], None])
  ])
]

#html_kana_text_on_genindex = True
testcase17in = {
'doc04': [('single','にに|四四^11; へへ|六六^11','id-04','',None)],
}

testcase17out = [
('な',
  [([(True, ('四', 'に')), (True, ('四', 'に'))],
    [[], [('六六', [('', 'doc04.html#id-04')])], None])])]

#html_kana_text_on_genindex = True
testcase18in = {
'doc04': [('single','にに|四四^11; へへ|六六^11','id-04','',None)],
'doc03': [('single','にに|四四^11; ほほ|五五^11','id-03','', '分類子')],
}

testcase18out = [
('分類子',
  [([(True, ('四', 'に')), (True, ('四', 'に'))],
    [[],
     [('六六', [('', 'doc04.html#id-04')]),
      ('五五', [('', 'doc03.html#id-03')])],
     None])])]

#html_kana_text_on_genindex = True
testcase19in = {
'doc04': [('single','にに|四四^11; へへ|六六^11','id-04','',None)],
'doc03': [('single','にに|四四^11; ほほ|五五^11','id-03','', '分類子')],
'doc02': [('single','いい|壱壱^11; はは|参参^11','id-02','',None)],
}

testcase19out = [
('あ',
  [([(True, ('壱', 'い')), (True, ('壱', 'い'))],
    [[], [('参参', [('', 'doc02.html#id-02')])], None])]),
 ('分類子',
  [([(True, ('四', 'に')), (True, ('四', 'に'))],
    [[],
     [('六六', [('', 'doc04.html#id-04')]),
      ('五五', [('', 'doc03.html#id-03')])],
     None])])]

#html_kana_text_on_genindex = True
testcase20in = {
'doc04': [('single','にに|四四^11; へへ|六六^11','id-04','',None)],
'doc03': [('single','にに|四四^11; ほほ|五五^11','id-03','', '分類子')],
'doc02': [('single','いい|壱壱^11; はは|参参^11','id-02','',None)],
'doc01': [('single','いい|壱壱^11; ろろ|弐弐^11','id-01','',None)],
}

testcase20out = [
('あ',
  [([(True, ('壱', 'い')), (True, ('壱', 'い'))],
    [[],
     [('参参', [('', 'doc02.html#id-02')]),
      ('弐弐', [('', 'doc01.html#id-01')])],
     None])]),
 ('分類子',
  [([(True, ('四', 'に')), (True, ('四', 'に'))],
    [[],
     [('六六', [('', 'doc04.html#id-04')]),
      ('五五', [('', 'doc03.html#id-03')])],
     None])])]

#kana_text_word_listの上書き
testcase21in = {
'doc01': [('single','ああ|球球球; いい|球球球','id-01','',None)],
'doc02': [('see','かか|球球球; めめ|球球球','id-02','',None)],
'doc03': [('single','ささ|球球球; んん|球球球','id-03','',None)],
'doc04': [('seealso','たた|拾拾拾; いい|拾拾拾','id-04','',None)],
'doc05': [('single','なな|拾拾拾; めめ|拾拾拾','id-05','',None)],
'doc06': [('single','おお|拾拾拾; んん|拾拾拾','id-06','',None)],
}

testcase21out = [
('な',
  [([(True, ('球球球', 'ののの'))],
    [[],
     [('球球球', [('', 'doc01.html#id-01'), ('', 'doc03.html#id-03')]),
      ('see 球球球', [])],
     None])]),
 ('ら',
  [([(True, ('拾拾拾', 'れれれ'))],
    [[],
     [('拾拾拾', [('', 'doc05.html#id-05'), ('', 'doc06.html#id-06')]),
      ('see also 拾拾拾', [])],
     None])])]

#kana_text_word_listの上書き
testcase22in = {
'doc01': [('single','ああ|球球球; いい|球球球','id-01','',None)],
'doc02': [('see','かか|球球球; めめ|球球球','id-02','',None)],
'doc03': [('single','ささ|球球球; んん|球球球','id-03','',None)],
'doc04': [('seealso','たた|拾拾拾; いい|拾拾拾','id-04','',None)],
'doc05': [('single','なな|拾拾拾; めめ|拾拾拾','id-05','',None)],
'doc06': [('single','おお|拾拾拾; んん|拾拾拾','id-06','',None)],
}

testcase22out = [
('な',
  [([(True, ('拾拾拾', 'ねねね'))],
    [[],
     [('拾拾拾', [('', 'doc05.html#id-05'), ('', 'doc06.html#id-06')]),
      ('see also 拾拾拾', [])],
     None])]),
 ('ら',
  [([(True, ('球球球', 'るるる'))],
    [[],
     [('球球球', [('', 'doc01.html#id-01'), ('', 'doc03.html#id-03')]),
      ('see 球球球', [])],
     None])])
 ]

#-------------------------------------------------------------------

class _env(object): pass

class _config(object):
    def __init__(self):
        self.kana_text_separator = r'\|'
        self.kana_text_indexer_mode = 'normal'
        self.kana_text_word_file = '~/.config/sphinx/kana_word_list.txt'
        self.kana_text_word_list = ()
        self.html_kana_text_on_genindex = False
        self.html_change_triple = False

class _builder(object):
    def __init__(self, env, cfg):
        self.env = env
        self.config = cfg

    def get_relative_uri(self, _, fn):
        return fn+'.html'

env = _env()
cfg = _config()
bld = _builder(env, cfg)
idx = IndexRack(bld, True)
idx0 = IndexRack(bld)

class testIndexRack(unittest.TestCase):
    def test01_create_genindex(self):
        self.maxDiff = None
        gidx = idx.create_genindex(testcase01in)
        self.assertEqual(gidx, testcase01out)

    def test02_create_genindex(self):
        self.maxDiff = None
        gidx = idx.create_genindex(testcase02in)
        self.assertEqual(gidx, testcase02out)

    def test03_create_genindex(self):
        self.maxDiff = None
        gidx = idx.create_genindex(testcase03in)
        self.assertEqual(gidx, testcase03out)

    def test04_first_letter_of_term(self):
        self.maxDiff = None
        idx04 = IndexRack(bld, True)
        idx04.config.kana_text_indexer_mode = 'large'
        gidx = idx04.create_genindex(testcase04in)
        self.assertEqual(gidx, testcase04out)

    def test05_first_letter_of_term(self):
        self.maxDiff = None
        idx05 = IndexRack(bld, True)
        idx05.config.kana_text_indexer_mode = 'small'
        gidx = idx05.create_genindex(testcase05in)
        self.assertEqual(gidx, testcase05out)

    def test06_first_letter_of_term(self):
        self.maxDiff = None
        idx06 = IndexRack(bld, True)
        idx06.config.kana_text_indexer_mode = 'small'
        gidx = idx06.create_genindex(testcase06in)
        self.assertEqual(gidx, testcase06out)

    def test07_kana_catalog(self):
        self.maxDiff = None
        idx.config.kana_text_indexer_mode = 'small'
        gidx = idx.create_genindex(testcase07in)
        self.assertEqual(gidx, testcase07out)

    def test08_kana_catalog(self):
        self.maxDiff = None
        cfg = _config()
        cfg.kana_text_word_file = False
        cfg.kana_text_indexer_mode = 'small'
        bld = _builder(env, cfg)
        gidx = idx.create_genindex(testcase08in)
        self.assertEqual(gidx, testcase08out)

    def test09_homonymous_function(self):
        self.maxDiff = None
        idx.config.kana_text_indexer_mode = 'small'
        gidx = idx.create_genindex(testcase09in)
        self.assertEqual(gidx, testcase09out)

    def test10_kana_catalog(self):
        self.maxDiff = None
        cfg = _config()
        cfg.kana_text_word_file = False
        bld = _builder(env, cfg)
        idx = IndexRack(bld, True)
        idx.config.kana_text_indexer_mode = 'small'
        gidx = idx.create_genindex(testcase10in)
        self.assertEqual(gidx, testcase10out)

    def test11_homonymous_function(self):
        self.maxDiff = None
        idx.config.kana_text_indexer_mode = 'small'
        gidx = idx.create_genindex(testcase11in)
        self.assertEqual(gidx, testcase11out)

    def test12_kana_text_on_genindex(self):
        self.maxDiff = None
        idx0.config.kana_text_indexer_mode = 'small'
        idx0.config.html_kana_text_on_genindex = True
        gidx = idx0.create_genindex(testcase12in)
        self.assertEqual(gidx, testcase12out)

    def test13_homonymous_function(self):
        self.maxDiff = None
        idx.config.kana_text_indexer_mode = 'small'
        gidx = idx.create_genindex(testcase13in)
        self.assertEqual(gidx, testcase13out)

    def test14_homonymous_function(self):
        self.maxDiff = None
        idx.config.kana_text_indexer_mode = 'small'
        gidx = idx.create_genindex(testcase14in)
        self.assertEqual(gidx, testcase14out)

    def test15_homonymous_function(self):
        self.maxDiff = None
        idx.config.kana_text_indexer_mode = 'small'
        gidx = idx.create_genindex(testcase15in)
        self.assertEqual(gidx, testcase15out)

    def test16_homonymous_function(self):
        self.maxDiff = None
        idx.config.kana_text_indexer_mode = 'small'
        gidx = idx.create_genindex(testcase16in)
        self.assertEqual(gidx, testcase16out)

    def test17_kana_text_on_genindex(self):
        self.maxDiff = None
        idx0.config.kana_text_indexer_mode = 'small'
        idx0.config.html_kana_text_on_genindex = True
        gidx = idx0.create_genindex(testcase17in)
        self.assertEqual(gidx, testcase17out)

    def test18_kana_text_on_genindex(self):
        self.maxDiff = None
        idx0.config.kana_text_indexer_mode = 'small'
        idx0.config.html_kana_text_on_genindex = True
        gidx = idx0.create_genindex(testcase18in)
        self.assertEqual(gidx, testcase18out)

    def test19_kana_text_on_genindex(self):
        self.maxDiff = None
        idx0.config.kana_text_indexer_mode = 'small'
        idx0.config.html_kana_text_on_genindex = True
        gidx = idx0.create_genindex(testcase19in)
        self.assertEqual(gidx, testcase19out)

    #def test20_kana_text_on_genindex(self):
    #   self.maxDiff = None
    #   idx0.config.kana_text_indexer_mode = 'small'
    #   idx0.config.html_kana_text_on_genindex = True
    #   gidx = idx0.create_genindex(testcase20in)
    #   self.assertEqual(gidx, testcase20out)

    def test21_kana_catalog(self):
        self.maxDiff = None
        cfg21 = _config()
        bld21 = _builder(env, cfg21)
        bld21.config.kana_text_word_list = ['ののの|球球球^', 'れれれ|拾拾拾^']
        bld21.config.html_kana_text_on_genindex = True
        bld21.config.kana_text_indexer_mode = 'small'
        idx21 = IndexRack(bld21)
        gidx = idx21.create_genindex(testcase21in)
        self.assertEqual(gidx, testcase21out)

    def test22_kana_catalog(self):
        self.maxDiff = None
        cfg = _config()
        cfg.kana_text_word_list = []
        cfg.kana_text_word_file = 'tests/word_list.txt'
        cfg.html_kana_text_on_genindex = True
        cfg.kana_text_indexer_mode = 'small'
        bld = _builder(env, cfg)
        idx = IndexRack(bld)
        gidx = idx.create_genindex(testcase22in)
        self.assertEqual(gidx, testcase22out)

#-------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()

    #bld.config.kana_text_indexer_mode = 'small'
    #gidx = bld.create_genindex(testcase08in)
    #pprint(gidx)
