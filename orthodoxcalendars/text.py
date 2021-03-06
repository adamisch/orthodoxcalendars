from .verses import get_verses, end_verse
import copy
import pandas as pd

def get_text(verses, key, bible):
    """Get text for verses from KJV bible"""
    if verses is not None:
        verses['b'] = verses['b'].map(dict(zip(key['n'], key['b'])))
        if verses['v'].str.contains('end').any():
            n_verses = pd.DataFrame(bible.groupby(['b', 'c']).apply(len)).reset_index()
            verses['v']
            verses['v'] = [verse.replace('end',  str(end_verse(book, chapter, n_verses)))
                           if verse.endswith('-end') else verse 
                           for book, chapter, verse in zip(verses['b'], verses['c'], verses['v'])]
        if verses['v'].str.contains('-').any():
            verses['v'] = [x.split('-') for x in verses['v']]
            verses['v'] = [list(range(y[0], y[1]+1)) if len(y)==2 else y 
                           for y in [list(map(int, x)) for x in verses['v']]]
            verses = verses.explode('v').reset_index(drop=True)
        verses = verses.astype(str)
        verses['b'] = verses['b'].str.zfill(2)
        verses['c'] = verses['c'].str.zfill(3)
        verses['v'] = verses['v'].str.zfill(3)
        verses['id'] = verses['b']+verses['c']+verses['v']
        verses['text'] = [bible[bible['id']==int(x)]['t'].item() for x in verses['id']]
        return verses
    else:
        return pd.DataFrame({'text': [" "]})

def text_columns(df, key, bible):
    """Create new columns with text of each verse in each column"""
    static_colnames = copy.deepcopy(df.columns.tolist())
    for col in static_colnames:
        if col.startswith("Reading"):
            text_number = col[len("Reading"):]
            reading_name = "Text" + text_number
            df[reading_name] = [" ".join(get_text(get_verses(x), key, bible)['text'])
                                for x in df[col]]
    return df
