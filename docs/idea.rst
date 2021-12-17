実装アイデア
############
思いついた機能を書き出しておく.

索引タイプ
==========
attribute
---------
記載例

.. code-block:: rst

   .. index::
      attribute: main; attr1; attr2; attr3; ...; attrN

以下の記述と同値

.. code-block:: rst

   .. index::
      single: main
      single: attr1; main
      single: attr2; main
      single: attr3; main
      …
      single: attrN; main

keys
----
記載例

.. code-block:: rst

   .. index::
      keys: main; key1; key2; key3; ...; keyN

以下の記述と同値

.. code-block:: rst

   .. index::
      pair: main; key1
      pair: main; key2
      pair: main; key3
      …
      pair: main; keyN

下拵え
------
process_index_entryに拡張性を持たせて、indextypesのカスタムができるようにする.
