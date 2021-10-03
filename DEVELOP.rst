DEVELOPMENT
-----------
KanaOne(ex. 'かな|言葉^11')

- obj[obj.i_1st]: 'かな'
- obj[obj.t_2nd]: '言葉’
- obj['ruby']: 'specific'
- obj['option']: '11'

KanaText(ex. 'ああ|壱壱^11; いい|弐弐^11; うう|参参^11')

- obj[0]: KanaOne('ああ|壱壱^11')
- obj[1]: KanaOne('いい|弐弐^11')
- obj[2]: KanaOne('うう|参参^11')
- obj['index_key']: None
- obj['index_type']: ''
- obj['main']: ''
- obj['target']: ''

KanaEntry(T.B.D.)

- obj[0]: sortkey
- obj[1]: KanaOne(classifier)
- obj[2]: KanaOne(main term)
- ojb[3]: '', KanaOne(sub term), or KanaText(2nd term, 3rd term)
- obj['index_key']: index_key
- obj['main']: emphasis
- obj['target']: target id
