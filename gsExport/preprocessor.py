from nbconvert.preprocessors import *
import hashlib
import nbformat as nbf

class gsExportPreprocessor(Preprocessor):
    def preprocess(self, nb, resources):
        for cell in nb['cells']:
            cell['metadata']['#student'] = '#student' in cell['source']
            cell['source'] = '\n'.join([line for line in cell['source'].split('\n') if '#student' not in line])
            
        number_of_newpages = len([cell for cell in nb['cells'] if '#newpage' in cell['source']])
        nb['metadata']['number_of_pagebreaks'] = number_of_newpages
        
        # Checksum material
        remove_all_whitespace = lambda string: "".join(string.split())
        nb['metadata']['checksums'] = [hashlib.md5(remove_all_whitespace(cell['source']).encode('utf8')).hexdigest() for cell in nb['cells']] 
        
        return nb,resources