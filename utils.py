from tqdm import tqdm
import codecs
import glob

def load_files(dir='data/', file_type='.txt'):
    file_names = sorted(glob.glob('{}*{}'.format(dir, file_type)))
    print('Total files : {}'.format(len(file_names)))
    return_text = ''
    pbar = tqdm(file_names)
    for name in pbar:
        pbar.set_description('Reading : {}'.format(name))
        with codecs.open(name, 'r', 'utf-8') as f:
            return_text += f.read()
    print('Reading completed, {} chars in total'.format(len(return_text)))
    return return_text
