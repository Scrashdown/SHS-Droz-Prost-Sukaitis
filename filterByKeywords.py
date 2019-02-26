import json, os

RAW_DATA_DIR = 'raw-data'
FILTERED_DATA_DIR = 'filtered-data'
KEYWORDS = ['viet', 'saigon', 'sai gon', 'hanoi', 'hanoï', 'ha noi', 'ho chi minh', 'ngo dinh diem']

def error(errorMsg):
    print()
    print(f'ERROR: {errorMsg}')
    exit()

def getJSONFileNames(dir):
    return list(filter(lambda fln: fln.endswith('.jsonl'), os.listdir(dir)))

def filterJSON(jsonArticle):
    '''Return true if the article contains some of the keywords,
    either in its title, or in the full text.'''
    decodedDict = json.loads(jsonArticle)
    for kw in KEYWORDS:
        title, fulltext = decodedDict['title'], decodedDict['fulltext']
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

JSONFileNames = getJSONFileNames(RAW_DATA_DIR)
if JSONFileNames == []:
    print(f'No .jsonl files found in directory {RAW_DATA_DIR}')

for fileName in JSONFileNames:
    with open(RAW_DATA_DIR + '/' + fileName, 'r') as inputFile:
        print(f'Filtering file {fileName}... ', end = '')
        with open(FILTERED_DATA_DIR + '/' + fileName, 'w') as outputFile:
            filterFile(inputFile, outputFile)
        print('done.')