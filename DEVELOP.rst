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

- unit(the other entry): [(classifier, term, subterm, emphasis, file_name, target, index_key)]

    - classifier: KanaText(index_key, word[:1] or a letter made by word[:1])
    - term: KanaText(word)
    - subterm: '', KanaText(word), KanaText(word1) and KanaText(word2)
    - emphasis
    - file_name
    - target
    - index_key

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
- ideo: the string '言葉' of 'かな|言葉^11', by object.ashier() which means hieroglyph.
- kana: the string 'かな' of 'かな|言葉^11'. by object.askana()
- ruby: ex. [(True, ('田', 'た')), (True, ('中', 'なか'))]
- html: ex. '<ruby><rb>言葉</by><rp></rp><rt>かな</rt><rp></rp></ruby>'
- latex: (T.B.D.)
- epub: (T.B.D.)
- separator: used by re.split()
- delimiter: used by object.astext(), etc.
- option_marker: the '^' of 'かな|言葉^11'

methods

- astext: return a string as ideogram
- assort: return a string like a eacy identifier
- askana: return a string which is reading
- aslist: return a list data for the display with ruby. for genindex.html.
- ashtml: return a string which is made with html tags. for genindex.html and glossary.
- __eq__: return self.astext() == other,  to be identified easily for unittest
- __str__: return a string by ashier/ashtml for jinja2

KanaText(ex. 'かな|言葉^11')

- object['ideo']: '言葉’
- object['kana']: 'かな'
- object['delimiter']: '|'
- object['ruby']: 'specific'
- object['option']: '11'
- object.whatiam: in('classifier', 'term':default, 'subterm')
- object.__eq__: used by unittest and IndexRack.generate_genindex_data
- object.__str__: used by jinja2. use object.whatiam

ExSubTerm

- object[0]: KanaText
- object[1]: KanaText
- object._delimiter

ExIndexUnit

- object[0]: KanaText(classifier)
- object[1]: KanaText(main term)
- object[2]: SubTerm([], [KanaText(2nd)], or [KanaText(2nd), KanaText(3rd)])
- object['link_type']: 1:'see', 2:'seealso', 3:'uri'
- object['file_name']: target file
- object['target']: target id
- object['main']: 3:'main', 4:''
- object['index_key']: None or classifier
- object.delimiter: ' ' or ', '
- object.get_terms: [object[1], object[2][0], object[2][1]]

ExIndexEntry(ex. 'ああ|壱壱^11; いい|弐弐^11; うう|参参^11')

- object[0]: KanaText('ああ|壱壱^11')
- object[1]: KanaText('いい|弐弐^11')
- object[2]: KanaText('うう|参参^11')
- object['entry_type']: 'single', 'pair', 'triple', 'see' or 'seealso'
- object['file_name']: file name
- object['target']: target id
- object['main']: 'main' or ''
- object['index_key']: None or classifier
- object.make_Index_units(): return [IndexUnit, IndexUnit, ...]

ExIndexRack

- object[n]: IndexUnit(...)
- object.append(): make/update classifier_catalog and kana_katalog
- object.extend(): call the object.append() by each IndexUnit object
- object.udpate_units(): update IndexUnit object with classifier_catalog and kana_catalog
- object.sort_units(): to be sorted
- object.generate_genindex_data()
