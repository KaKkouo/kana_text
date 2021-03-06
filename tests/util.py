from src import ExtIndexRack as IndexRack

class Domain(object):
    def __init__(self, entries):
        self.entries = entries

class Env(object):
    def __init__(self, entries):
        self.domain = {}
        self.domain['index'] = Domain(entries)
    def get_domain(self, domain_type):
        return self.domain[domain_type]

class Config(object):
    def __init__(self):
        self.kana_text_separator = r'\|'
        self.kana_text_option_marker = r'\^'
        self.kana_text_indexer_mode = 'normal'
        self.kana_text_word_file = ''
        self.kana_text_word_list = ()
        self.kana_text_on_genindex = False
        self.kana_text_change_triple = False

class builder(object):
    def __init__(self, entries):
        self.env = Env(entries)
        self.get_domain = self.env.get_domain
        self.config = Config()
    def get_relative_uri(self, uri_type, file_name):
        return f'{file_name}.html'

class IndexEntries(IndexRack):
    def __init__(self, env):
        self.env = env
        self._kana_catalog = {}
    def create_index(self, builder):
        self.__init__(builder)
        self.builder = builder
        self.config = builder.config
        self.get_relative_uri = builder.get_relative_uri
        return super().create_index()
