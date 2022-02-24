##########
sphindexer
##########

.. contents::
   :local:

主に、ソースコードを読み解く上での要点.

パッケージは異なりますが、日本語で書く都合上こちらに書きます.

各クラスの役割
==============
Textクラス
 
- データの読み取り
- 各処理に応じた文字列の生成

IndexRackクラス

- 全体の処理を取りまとめるクラス

IndexEntryクラス

- indexドメインのentryのデータ構造に対応したクラス

IndexUnitクラス

- 索引ページに表示する一つ一つの用語に対応したクラス

ソースコードの読み方
====================

全体の流れを掴む
-----------------
IndexRack.__init__、create_indexがやっていることの全て

1. __init__ でbuilderオブジェクトのデータを受け取る
2. create_indexで処理を実行して、結果を返す

create_indexがやっていること
----------------------------
1. indexドメインからエントリーを受け取る.
2. エントリーにあるデータ一つ一つを確認しながら格納（extend, append）

   - self.entryclass内でKanaTextによって記法を含む文字列の解析が行われる.
   - 全てのデータを見て決定するような処理は、ここでxxx_catalogにデータを貯める.

3. データの調整作業（update_units）

   - xxx_catalogにデータを見て必要な更新を行う.

4. 並び替え（sort_units）

   - 並び順の細かい調整はassortで調整する.

5. データの作成（generate_genindex_data）

拡張性ためのコツ
----------------
他のクラスは直接使うのではなく、クラス変数（textclass, packclass, unitclass, entryclass）を介して使う.
こうすることで拡張クラスの差し替えが容易になる.

IndexRackクラス
===============

sort_unitsメソッド
------------------
このクラスの肝となるメソッド

.. code-block:: python

    def sort_units(self):
        """
        What is done in Text is done in Text,
        and what is done in IndexUnit is done in IndexUnit."""
        self._rack.sort(key=lambda unit: (
            unit[UNIT_CLSF].assort(),  # classifier
            unit[UNIT_TERM].assort(),  # primary term
            unit['link_type'],  # see Convert. 1:'see', 2:'seealso', 3:'uri'.
            unit[UNIT_SBTM].assort(),  # secondary term
            unit['main'],       # see Convert. 3:'main', 4:''.
            unit['file_name'],
            unit['target']), )
        # about x['file_name'], x['target'].
        # Reversing it will make it dependent on the presence of "make clean".:w

unit[UNIT_XXXX].assortの役目

- 文字列をそのままソートするだけでは達成出来ない並び順を実現するためにリストを返す.
- リストの最初の要素（数字）で独自の並び順を調整。次の要素は本来の文字列。

update_unitsメソッドの役目

- ここでいい感じに並び替えが行われるように文字列を更新しておく.

appendメソッド
--------------
ここも処理の肝.

- どんなデータがあるか全てチェックしてから登録する.
- 調べたデータを元にupdate_unitsメソッドが実行される.

generate_genindex_dataメソッド
------------------------------
プログラミングしていて楽しかった箇所.

- データを整形しやすいようにsort_unitsが並べ替えてくれている.
- 基本的にはデータの変わり目をチェックしてアレコレ.

IndexUnitクラス
===============
索引ページに表示する各用語に対応するクラス.

IndexEntryクラス
================
process_index_entry関数が作るデータに対応するクラス.
IndexUnitクラスへのデータ変換を請け負うメソッドも持つ.
