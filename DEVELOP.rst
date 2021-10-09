DEVELOPMENT
-----------
structure of the data for genindex.html

- genidex: [(classifier, terms)]

    - classifier: KanaText
    - terms: [(term, list)]

        - term: KanaText
        - list: [links, subterms, index_key]

            - links: [(main, uri)]
            - subterms: [(subterm, links)]

                - subterm: SubTerm[KanaText]
                - links: [(main, uri)]

            - index_key: str

variable name

- term: KanaText OBJect. it might be ktobj.
- rawtext: ex. 'かな|言葉^11', 'かな|言葉^11; い|壱^1' or 'かな|言葉^11; い|壱^1; ろ|弐^1`
- rawsouce: means Elemnt.rawsource.
- text: the string 'かな|言葉' of 'かな|言葉^11', by object.asword() of KanaText.
- hier: the string '言葉' of 'かな|言葉^11', by object.ashier() which means hieroglyph.
- kana: the string 'かな' of 'かな|言葉^11'. by object.askana()
- html: ex. '<ruby><rb>言葉</by><rp></rp><rt>かな</rt><rp></rp></ruby>'
- latex: (T.B.D.)
- epub: (T.B.D.)
- separator: used by re.split()
- delimiter: used by object.astext(), etc.
- option_marker: the '^' of 'かな|言葉^11'

KanaText(ex. 'かな|言葉^11')

- object[0]: '言葉’
- object[1]: 'かな'
- object['delimiter']: '|'
- object['ruby']: 'specific'
- object['option']: '11'
- object.whatiam: in('classifier', 'term':default, 'subterm')
- object.__eq__: used for unittest, and IndexRack.generate_genindex_data
- object.__str__: used for jinja2. use object.whatiam

KanaTextUnit(ex. 'ああ|壱壱^11; いい|弐弐^11; うう|参参^11')

- object[0]: KanaText('ああ|壱壱^11')
- object[1]: KanaText('いい|弐弐^11')
- object[2]: KanaText('うう|参参^11')
- object['entry_type']: 'single', 'pair', 'triple', 'see' or 'seealso'
- object['file_name']: file name
- object['target']: target id
- object['main']: 'main' or ''
- object['index_key']: None or classifier
- object.make_IndexUnit(): return [IndexUnit, IndexUnit, ...]

TextUnit(T.B.D.)

- object[0]: Text(rawtext)
- object[1]: Text(rawtext)
- object[2]: Text(rawtext)
- object['entry_type']: 'single', 'pair', 'triple', 'see' or 'seealso'
- object['file_name']: a file name
- object['target']: a target id
- object['main']: 'main' or ''
- object['index_key']: None or classifier
- object.make_index_unit(): return [IndexUnit, IndexUnit, ...]

IndexRack

- object[n]: IndexUnit(...)
- object.append(): make/update classifier_catalog and kana_katalog
- object.extend(): call the object.append() by each IndexUnit object
- object.udpate(): update IndexUnit object with classifier_catalog and kana_catalog
- object.sort(): to be sorted
- object.generate_genindex_data()

IndexUnit

- object._sortkey: for emphasis which means 'main'.
- object[0]: KanaText(classifier)
- object[1]: KanaText(main term)
- object[2]: SubTerm([], [KanaText(2nd)], or [KanaText(2nd), KanaText(3rd)])
- object[3]: emphasis code ('main': 1, '': 5, 'see': 8, 'seealso': 9)
- object['file_name']: target file
- object['target']: target id
- object['main']: emphasis
- object['index_key']: None or classifier
- object.delimiter: ' ' or ', '
