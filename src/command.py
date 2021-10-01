"""
genindex.html.sample
"""

from os.path import dirname

def genindex():
    file_name = 'genindex.html.sample'
    read_file = dirname(__file__) + '/templates/'+file_name

    fd = open(read_file, 'r')
    jinja = fd.read()
    fd.close()

    print('creating:', file_name, end=' . . . ')
    fd = open(file_name, 'w')
    fd.write(jinja)
    fd.close()
    print('done.')
