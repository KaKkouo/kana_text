##########
sphindexer
##########

.. contents::
   :local:

主に、ソースコードを読み解く上での説明.

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

update_unitsメソッドの役目

- ここでいい感じに並び替えが行われるように文字列を更新しておく.

assortの役目

- 文字列をそのままソートするだけでは達成出来ない並び順を実現するためにリストを返す.
- リストの第一データで独自の並び順を調整。第二データは文字列。

appendメソッド
--------------
ここも処理の肝.

- どんなデータがあるか全てチェックしてから登録する.
- 調べたデータを元にupdate_unitsメソッドが実行される.

generate_genindex_dataメソッド
------------------------------
プログラミングしていて楽しかった箇所.

- データを整形しやすいようにsort_unitsが並べ替えてくれている.
