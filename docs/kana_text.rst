#######################
sphinxcontrib.kana_text
#######################

.. contents::
   :local:

参考情報
========
- https://www.sphinx-doc.org/ja/master/usage/restructuredtext/basics.html
- https://www.sphinx-doc.org/ja/master/development/tutorials/helloworld.html

機能
====
文字列を「かな|単語」という書式で記載することで、「かな」に応じた表示順となる。
「かな」は表示では非表示、もしくはルビ表示にする.

対象
----
- indexディレクティブ、glossaryディレクティブ
- indexロール（ルビと索引）、kanaロール（ルビのみ）.

「かな|単語^オプション」と書く以外は、これまでと同じ記法.

使い方
------
次のように「かな|」を記載文字の前方に付記する

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

   夜空に浮かぶ\ :index:`あまた|数多^21`\ の星々が\ :kana:`きらめいて|煌めいて^2c`\ いる。

読み仮名の表示の調整
--------------------
ルビの表示を細かく指定したい場合に使う

- 「かな|単語^オプション」とする
- 「^」以降はソート処理では無視される

指定方法

- 「かな|単語^」は読み仮名の表示。「^」がないと非表示

    - 記述が少ない時の振る舞いは「ルビ非表示」とした.
    - 索引ページでの並び順を優先した仕様にしている.

- 「かな|単語^2312」と数字が続く場合は、単語の各１文字に当てる読みの数
- 「かな|単語^2a1b」とアルファベットがある場合は、ルビ表示に使わない

    - 読み仮名の部分的非表示は「a-i」「q-y」の２種類で対応

- 「かな|単語^201」とゼロがある場合は、単語のその１文字の割当をスキップする

適切に設定していない場合

- 文字数以上の指定があった場合、在る文字を指定通りに表示する.
- 指定が不足している場合はルビは表示しない.

パラメータ
----------
kana_text_separator

- 「かな|単語」の区切りを指定する. 初期設定は「r'\|'」. 
- 現在は実装が不完全なため、初期設定以外は使えない.

kana_text_option_marker

- 「かな|単語^11」の「^」を指定する. 初期設定は「r'\^'」. 
- 現在は実装が不完全なため、初期設定以外は使えない.

kana_text_word_file

- 「かな|言葉^11」の書式で記載された設定ファイルの指定.
- 設定で指定したファイルがないとmakeがエラーで止まる.

kana_text_word_list

- 「かな|言葉^11」の書式で指定された文字列をリスト形式で設定する.

kana_text_indexer_mode

- 'small': ex.「モジュール」は「ま」の項目.
- 'large': ex.「モジュール」は「も」の項目.
- その他:  ex.「モジュール」は「モ」のまま.
- 省略時は`small`.

kana_text_on_genindex

- 索引ページでのかな表示を有効にする. 省略時は非表示. 推奨はTrue.

    - かな表示の指定は用語（主）のみ. 分類子、用語（副）は非表示.

- 対応した「genidex.html」が必要. コマンド「sphinx-kana-genindex」で作成される.

kana_text_change_triple

- tripleでの「3rd, 1st」の表示を「1st, 3rd」に変更する. 省略時はFalse.

kana_text_see_behavior（案）

- エントリータイプ「see」の振る舞いを、「keys」もしくは「pair」に変更する.

    - 実装は容易だけど、後々のrstのメンテが大変なので現状は保留.
    - indextypesの改変を模索するほうが素直な対応.

genindex.htmlの作り方
---------------------
コマンド「sphinx-kana-genindex」の実行で、
以下の内容のファイルがカレントディレクトリに作成される.

1. sphinx/themes/basic/genindex.html をプロジェクトの「_templates」にコピーする.
2. indexentriesマクロにある二つの「{{ firstname|e }}」から「|e」を取り除く。

    - 「|e」の代わりにメソッド側にて「nodes.unescape」で対処。

開発者向け
==========

データの優先順
-------------- 
早い者勝ちv.s.上書き許容（インデクシング）

- できる限り内部の処理順に依存しない実装を目指し、解消できない部分は「早い者勝ち」とする.

    - 「make clean」後の「make html」で安定する挙動として.

- 恐らくstd.pyでの登録データの方が、index.pyの登録データより処理が先.

設定中のかな情報v.s.ドキュメントファイル内のかな情報

- 現状は前者が優先される.
- 「絶対の設定を個別の記述で上書き」という考えなら、後者を優先すべき.

実装においての要点
------------------ 
KanaTextクラス

- かな表示を可能にする.
- 「.. index::」「..glossary::」「:index:」「:kana:」で使用.
- 「KanaWord」クラスに変更しようか悩み中.

KanaXxxクラス（案）

- HTML5Traslatorのvisit_Textで使おうと思っているクラス.
- Textクラスが持っている文字列を解析して、かな情報を持つ文字列を拾い上げる.

    - 処理前）Text('文字列１ かな|記載文字 文字列２')
    - 処理後）KanaText('文字列１'), KanaText('かな|記載文字'), KanaText('文字列２')

- 「Text('文字列１|漢字《よみ》文字列２')」案もあるけど、全体の整合性が取れないので不採用.

    - 希望する人は本パッケージを参考にして自作してもらう.

ExtSubtermクラス

- ExtIndexUnitクラス内のsubtermオブジェクトのクラス.
- KanaTextを最大で二つ持つ.

ExtIndexUnitクラス

- 索引ページで表示される各項目に対応したオブジェクトのクラス.

ExtIndexEntryクラス

- 「.. index::」でsingle/pair/tripleと一緒に書かれている用語に対応.
- ExIndexUnittクラスに乗る前のKanaTextオブジェクトを保持する.
- see: sphinx/util/nodes.py, process_index_entry.

ExtIndexRackクラス/create_geindex_entriesメソッド

- IndexEntriesクラス/create_indexメソッドを置き換える.
- 可能な限り、内部的な処理順に依存しないようにした.
- オリジナルは「func() (クラス名やモジュール名)」の集約処理が説明した通りではない.
- 「see/seealso」の表示順がオリジナルと異なる.

visit_kana/depart_kanaメソッド

- add_node()により、KanaTextクラスに紐付けてExHTMLBuilderクラスに登録される.
- glossaryで記載したテキストは、 **visit_term()** メソッドでKanaTextクラスにする.

    - 本来の調整場所はGlossaryクラスだが、コード量の少ないvisit_termメソッドを選択.

ExtHTML5Translatorクラス/visit_termメソッド

- 目的のTextノードをKanaTextノードに変更する.

    - visit_termメソッドはglossaryで定義された用語（termクラス）が通る.

- 本来であればGlossaryクラスで対応すべき内容.

    - ２～３行の変更のためにほぼ同じコードを丸々書くことになるので避けている.

ExtHTMLBuilderクラス/create_indexメソッド

- 索引ページの表示

備忘録
======
latexでの索引ページ
-------------------
実装の可能性

- 索引ページから対応するドキュメントへのジャンプする機能があれば、原理的には対応可能.

latexの関連情報

- `TeX Wiki 索引作成 <https://texwiki.texjp.org/?%E7%B4%A2%E5%BC%95%E4%BD%9C%E6%88%90>`_
- `TeX Wiki 相互参照 <https://texwiki.texjp.org/?LaTeX%E5%85%A5%E9%96%80%2F%E7%9B%B8%E4%BA%92%E5%8F%82%E7%85%A7%E3%81%A8%E3%83%AA%E3%83%B3%E3%82%AF>`_
