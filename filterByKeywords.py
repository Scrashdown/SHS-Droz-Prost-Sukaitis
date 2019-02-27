import bz2, json, os

RAW_DATA_DIR = 'raw-data'
FILTERED_DATA_DIR = 'filtered-data'
KEYWORDS = ['vietnam', 'viet nam', 'saigon', 'sai gon', 'hanoi', 'hanoï', 'ha noi', 'ho chi minh', 'ho chi-minh', 'ngo dinh diem']

def error(errorMsg):
    print()
    print(f'ERROR: {errorMsg}')
    exit()

def getBZ2FileNames(dir):
    '''Return filenames with the .bz2.jsonl file extension in given directory dir.
    
    Assumes dir exists.'''
    return list(filter(lambda fln: fln.endswith('.jsonl.bz2'), os.listdir(dir)))

def preprocess(txt):
    '''Preprocess txt to make searching word easier.
    
    Reduces all words to lower-case.'''
    if txt is None:
        return None
    result = txt.lower()
    return result

def filterJSON(jsonArticle):
    '''Return true if the article contains some of the keywords,
    either in its title, or in the full text.'''
    decodedDict = json.loads(jsonArticle)
    for kw in KEYWORDS:
        title, fulltext = preprocess(decodedDict['title']), preprocess(decodedDict['fulltext'])
        if title is not None and kw in title:
            return True
        if fulltext is not None and kw in fulltext:
            return True
    return False

def filterBZ2File(fileName):
    inpath = os.path.join(RAW_DATA_DIR, fileName)
    outpath = os.path.join(FILTERED_DATA_DIR, fileName)
    print(f'Decompressing file {inpath}... ', end = '')
    with bz2.BZ2File(inpath) as inputBZ2File:
        rawText = inputBZ2File.read().decode('utf-8')
        print('done.')

        print(f'Filtering articles... ', end = '')
        articles = filter(lambda line: line != '', rawText.split('\n'))
        filtered = filter(filterJSON, articles)
        print(f'done.')

        print(f'Writing results to {outpath}... ', end = '')
        with bz2.BZ2File(os.path.join(FILTERED_DATA_DIR, fileName), mode = 'w') as outputBZ2File:
            encoded = '\n'.join(filtered).encode('utf-8')
            outputBZ2File.write(encoded)
            print('done.\n')

# Verify directories exist
thisDir = os.listdir('.')
if RAW_DATA_DIR not in thisDir:
    error(f'Directory {RAW_DATA_DIR} not found.')
if FILTERED_DATA_DIR not in thisDir:
    error(f'Directory {FILTERED_DATA_DIR} not found.')

# Get filenames
BZ2FileNames = getBZ2FileNames(RAW_DATA_DIR)
if BZ2FileNames == []:
    print(f'No .jsonl files found in directory {RAW_DATA_DIR}')

# Filter files
for fileName in BZ2FileNames:
    filterBZ2File(fileName)