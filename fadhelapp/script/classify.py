import sys, os
sys.path.insert(0, os.path.abspath('..'))
from preprocess import prep
import joblib
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import datetime
import pandas as pd
stemmer = StemmerFactory().create_stemmer()
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
stopword = StopWordRemoverFactory().create_stop_word_remover()
loaded_model = joblib.load('../modelNB.sav')
vectorizer = joblib.load('../vectorizer.sav')

def massive(df):
    df['stemmed'] = df['tweet'].apply(lambda x: stemmer.stem(stopword.remove(prep(x)))) # Stem every word.
    df['waktu'] = pd.to_datetime(df['date']).dt.date
    df = df.sample(frac=1).reset_index(drop=True)
    df = df.drop_duplicates(subset=['stemmed'], keep='first')
    df = df.drop_duplicates(subset=['tweet'], keep='first')
    result = vectorizer.transform(df['stemmed'])
    result = loaded_model.predict(result)
    df['tweet'] = df['tweet'].apply(lambda x: prep(x)) # Stem every word.
    df['tweet'] = df.apply(lambda row: "<a href='{}'>{}</a>".format(row['link'],row['tweet']),axis=1)
    df = df.drop(columns=['stemmed','date','link']) 
    df['label'] = result
    return df
def predicts(req):
    cleantext = stemmer.stem(stopword.remove(prep(req)))
    listz = [cleantext]
    listz = vectorizer.transform(listz)
    result = loaded_model.predict(listz)[0]
    return result