import json, os

RAW_DATA_DIR = 'raw-data'
FILTERED_DATA_DIR = 'filtered-data'
KEYWORDS = ['vietnam', 'viet nam', 'saigon', 'sai gon', 'hanoi', 'hanoï', 'ha noi', 'ho chi minh', 'ho chi-minh', 'ngo dinh diem']

def error(errorMsg):
    print()
    print(f'ERROR: {errorMsg}')
    exit()

def getJSONFileNames(dir):
    '''Return filenames with the .jsonl file extension in given directory dir.
    
    Assumes dir exists.'''
    return list(filter(lambda fln: fln.endswith('.jsonl'), os.listdir(dir)))

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

def filterFile(inputFile, outputFile):
    '''Reads data from inputFile, filters it and writes to outputFile.
    
    Each line of the file must be a properly formed JSON Object, representing an article.'''
    for line in inputFile:
        if filterJSON(line):
            outputFile.write(line + '\n')

# Verify directories exist
thisDir = os.listdir('.')
if RAW_DATA_DIR not in thisDir:
    error(f'Directory {RAW_DATA_DIR} not found.')
if FILTERED_DATA_DIR not in thisDir:
    error(f'Directory {FILTERED_DATA_DIR} not found.')

# Get filenames
JSONFileNames = getJSONFileNames(RAW_DATA_DIR)
if JSONFileNames == []:
    print(f'No .jsonl files found in directory {RAW_DATA_DIR}')

# Filter files
for fileName in JSONFileNames:
    with open(RAW_DATA_DIR + '/' + fileName, 'r') as inputFile:
        print(f'Filtering file {fileName}... ', end = '')
        with open(FILTERED_DATA_DIR + '/' + fileName, 'w') as outputFile:
            filterFile(inputFile, outputFile)
        print('done.')