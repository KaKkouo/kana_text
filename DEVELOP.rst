DEVELOPMENT
-----------
ex. KanaText('かな|言葉^11')

- object[0]: '言葉’
- object[1]: 'かな'
- object['separator']: '|'
- object['ruby']: 'specific'
- object['option']: '11'

ex. KanaUnit(ex. 'ああ|壱壱^11; いい|弐弐^11; うう|参参^11')

- object[0]: KanaText('ああ|壱壱^11')
- object[1]: KanaText('いい|弐弐^11')
- object[2]: KanaText('うう|参参^11')
- object['entry_type']: 'single'
- object['target']: ''
- object['main']: ''
- object['index_key']: None
- object.make_IndexUnit(): return [IndexUnit, IndexUnit, ...]

IndexUnit(T.B.D.)

- object[0][0]: sortkey
- object[1]: KanaText(classifier)
- object[2]: KanaText(main term)
- object[3]: [], [KanaText(2nd)], or [KanaText(2nd), KanaText(3rd)]
- object[4]: emphasis code ('main': 2, '': 5, 'see': 8, 'seealso': 9)
- object['file_name']: target file
- object['target']: target id
- object['main']: emphasis
- object['index_key']: index_key
- object.delimiter: ' ' or ', '

IndexRack(T.B.D.)

- object[n]: IndexUnit(...)

- object.append()
- object.extend()
- object.sort()
- object.create_genindex_entryies()
