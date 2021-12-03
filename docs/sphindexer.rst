##########
sphindexer
##########

.. contents::
   :local:

主に、ソースコードを読み解く上での要点.

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
