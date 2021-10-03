DEVELOPMENT
-----------
ex. KanaText('かな|言葉^11')

- object[0]: '言葉’
- object[1]: 'かな'
- object['ruby']: 'specific'
- object['option']: '11'

KanaValue(ex. 'ああ|壱壱^11; いい|弐弐^11; うう|参参^11')

- object[0]: KanaText('ああ|壱壱^11')
- object[1]: KanaText('いい|弐弐^11')
- object[2]: KanaText('うう|参参^11')
- object['entry_type']: 'single'
- object['target']: ''
- object['main']: ''
- object['index_key']: None

- object.create_IndexEntry(): return [IndexEntry(..), IndexEntry(..), ]

IndexEntry(T.B.D.)

- object[0]: sortkey
- object[1]: KanaText(classifier)
- object[2]: KanaText(main term)
- ojbect[3]: '', KanaText(only 2nd term), or KanaValue(2nd term, 3rd term)
- object['index_key']: index_key
- object['main']: emphasis
- object['target']: target id

IndexEntries(T.B.D.)

- object[n]: IndexEntry(...)

- object.append()
- object.extend()
- object.sort()
- object.create_genindex_entryies()
