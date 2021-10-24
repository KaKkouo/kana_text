DEVELOPMENT
-----------
structure of the data for genindex.html

- entry: {file_name: [(entry_type, value, target, main, index_key)]}

    - file_name: the name without suffix
    - entries: [entry]

        - entry: (entry_type, value, target, main, index_key)

            - entry_type: in('single', 'pair', 'triple', 'see', 'seealso')
            - value: 'word', 'word; word' or 'word; word; word'
            - target: the target id
            - main: 'main' or ''
            - index_key: classifier or None

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

variables

- term: KanaText OBJect. it had better to be 'ktobj' vaiable name.
- rawword: ex. 'かな|言葉^11'
- rawtext: ex. 'かな|言葉^11', 'かな|言葉^11; いい|壱壱^11' or 'かな|言葉^11; ...; ...'
- rawsouce: means Element.rawsource.
- text: the string 'かな|言葉' of 'かな|言葉^11', by object.astext() of KanaText.
- word: use as hier.
- hier: the string '言葉' of 'かな|言葉^11', by object.ashier() which means hieroglyph.
- kana: the string 'かな' of 'かな|言葉^11'. by object.askana()
- ruby: ex. [(True, ('田', 'た')), (True, ('中', 'なか'))]
- html: ex. '<ruby><rb>言葉</by><rp></rp><rt>かな</rt><rp></rp></ruby>'
- latex: (T.B.D.)
- epub: (T.B.D.)
- separator: used by re.split()
- delimiter: used by object.astext(), etc.
- option_marker: the '^' of 'かな|言葉^11'

methods

- ashier: return a string like hieroglyph
- astext: return a string like a eacy identifier
- askana: return a string which is reading
- asruby: return a list data for the display with ruby. for genindex.html.
- ashtml: return a string which is made with html tags. for genindex.html and glossary.
- __eq__: return self.astext() == other,  to be identified easily for unittest
- __str__: return a string by ashier/ashtml for jinja2

KanaText(ex. 'かな|言葉^11')

- object[0]: '言葉’
- object[1]: 'かな'
- object['delimiter']: '|'
- object['ruby']: 'specific'
- object['option']: '11'
- object.whatiam: in('classifier', 'term':default, 'subterm')
- object.__eq__: used by unittest and IndexRack.generate_genindex_data
- object.__str__: used by jinja2. use object.whatiam

ExIndexEntry(ex. 'ああ|壱壱^11; いい|弐弐^11; うう|参参^11')

- object[0]: KanaText('ああ|壱壱^11')
- object[1]: KanaText('いい|弐弐^11')
- object[2]: KanaText('うう|参参^11')
- object['entry_type']: 'single', 'pair', 'triple', 'see' or 'seealso'
- object['file_name']: file name
- object['target']: target id
- object['main']: 'main' or ''
- object['index_key']: None or classifier
- object.make_IndexUnit(): return [IndexUnit, IndexUnit, ...]

ExIndexRack

- object[n]: IndexUnit(...)
- object.append(): make/update classifier_catalog and kana_katalog
- object.extend(): call the object.append() by each IndexUnit object
- object.udpate(): update IndexUnit object with classifier_catalog and kana_catalog
- object.sort(): to be sorted
- object.generate_genindex_data()

ExIndexUnit

- object._sortkey: for emphasis which means 'main'.
- object[0]: KanaText(classifier)
- object[1]: KanaText(main term)
- object[2]: SubTerm([], [KanaText(2nd)], or [KanaText(2nd), KanaText(3rd)])
- object[3]: emphasis code ('main': 3, '': 5, 'see': 8, 'seealso': 9)
- object['file_name']: target file
- object['target']: target id
- object['main']: emphasis
- object['index_key']: None or classifier
- object.delimiter: ' ' or ', '
- object.get_children: [object[1], object[2][0], object[2][1]]

ExSubTerm

- object[0]: KanaText
- object[1]: KanaText
- object._delimiter
