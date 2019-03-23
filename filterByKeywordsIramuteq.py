import bz2, json, os, sys
from datetime import datetime as dt

RAW_DATA_DIR = 'raw-data'
FILTERED_DATA_DIR = 'filtered-data'
IRAMUTEQ_FILENAME = 'iramuteq.txt'

MAIN_KEYWORDS = ['vietnam'] # AND

OPTIONAL_KEYWORDS = \
    ['accords de genève', 'ho chi minh', 'kennedy', 'eisenhower', 'johnson', \
    'guérilla', 'guerilla', ' tet ', ' tet.', ' tet,', ' têt ', 'têt.', ' têt,', 'communisme', 'communiste']

#OPTIONAL_KEYWORDS = \
#    ['accords de geneve', 'pentagon papers', 'tet', 'paris', 'guerilla', 'guérilla', 'mobe', 'communisme', 'kennedy',\
#    'johnson', 'eisenhower', 'nixon', 'ford', 'front national de libération', 'napalm', 'communiste', 'université de kent', 'freedom deal', 'offensive de pâques',\
#    'offensive de pâcques', 'pourparlers'] # OR

YEAR_RANGE = range(1955, 1975 + 1)

# problèmes : hue qui désigne la ville vietnamienne de Huế
# se retrouve souvent dans des noms allemands
# solution => utiliser ' hue.' et ' hue '

# problème : tết est souvent ortographié tet ou têt
# se retrouve souvent parmi d'autres mots français (tête, Pittet, etc.)
# solution => utiliser ' tet ', ' tet.', ' têt ', ' têt.'

articleTemplate = \
    "**** *date_{date} *an_{year} *mois_{month}" + \
    " *jour_{day} *j_{journal} *lenMots_{words} *lenChar_{chars}"

def error(errorMsg):
    print()
    print(f'ERROR: {errorMsg}')
    exit()

def getBZ2filenames(dir):
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

def filterKeywords(article):
    '''Return true if the article contains some of the keywords,
    either in its title, or in the full text.'''
    for kw in MAIN_KEYWORDS:
        if kw not in article:
            return False
    for kw in OPTIONAL_KEYWORDS:
        if kw in article:
            return True
    return OPTIONAL_KEYWORDS == []

def filterBZ2File(filename):
    inpath = os.path.join(RAW_DATA_DIR, filename)
    outpath = os.path.join(FILTERED_DATA_DIR, filename)
    print(f'Decompressing file {inpath}... ', end = '')
    sys.stdout.flush()
    with bz2.BZ2File(inpath, mode = 'rb') as inputBZ2File,\
        open(os.path.join(FILTERED_DATA_DIR, IRAMUTEQ_FILENAME), mode = 'a') as outputJSONFile:

        rawText = inputBZ2File.read().decode('utf-8')
        print('done.')

        print(f'Filtering articles... ', end = '')
        sys.stdout.flush()

        preprocessed = preprocess(rawText)
        filtered = filter(filterKeywords, filter(lambda line: line != '', preprocessed.split('\n')))
        jsonArticles = map(json.loads, filtered)
        print(f'done.')

        for jsonArticle in jsonArticles:
            dateString = jsonArticle['date']
            date = dt.strptime(dateString, "%Y-%m-%d")
            texts = jsonArticle['fulltext']

            if 'GDL' in jsonArticle['id']:
                journal = 'Gazette_de_Lausanne'
            else:
                journal = 'Journal_de_Geneve'
                
            numWords = len(texts.split())
            numChars = len(texts)
            header = articleTemplate.format(date = dateString, year = date.year, month = date.month, day = date.day, journal = journal, words = numWords, chars = numChars)

            outputJSONFile.write('\n' + header + '\n' + ''.join(texts).replace('*', ' '))

# Verify directories exist
thisDir = os.listdir('.')
if RAW_DATA_DIR not in thisDir:
    error(f'Directory {RAW_DATA_DIR} not found.')
if FILTERED_DATA_DIR not in thisDir:
    error(f'Directory {FILTERED_DATA_DIR} not found.')

# Remove old iramuteq file if it exists
if IRAMUTEQ_FILENAME in os.listdir(FILTERED_DATA_DIR):
    print(f"Found old file, removing '{IRAMUTEQ_FILENAME}'...")
    os.remove(os.path.join(FILTERED_DATA_DIR, IRAMUTEQ_FILENAME))

# Get filenames
BZ2filenames = getBZ2filenames(RAW_DATA_DIR)
if BZ2filenames == []:
    print(f'No .jsonl files found in directory {RAW_DATA_DIR}')

# Filter files
for filename in BZ2filenames:
    if int(filename.split('-')[1]) in YEAR_RANGE:
        filterBZ2File(filename)