import os
import json
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
import string

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')


def preprocess(x):
    parent_directory = os.path.abspath('..')
    data_file_path = os.path.join(parent_directory, x)

    # Load the JSON
    with open(data_file_path, 'r') as e:
        data = e.read()

    df = pd.DataFrame(json.loads(data))

    # Drop instances where the date is not found
    df.drop(df.loc[df['date'] == "Date not found"].index, inplace=True)

    # Convert the 'content' column to lowercase
    df['content'] = df['content'].str.lower()

    # Remove punctuation, numbers, and specific characters
    punctuation_to_remove = string.punctuation.replace("'", "") + "–"
    df['content'] = df['content'].apply(lambda text: text.translate(str.maketrans('', '', punctuation_to_remove)))
    df['content'] = df['content'].apply(lambda text: ''.join([i for i in text if not i.isdigit()]))

    # Tokenization
    df['content'] = df['content'].apply(nltk.word_tokenize)

    # Stopword Removal
    stop_words = set(stopwords.words('english'))
    df['content'] = df['content'].apply(lambda tokens: [token for token in tokens if token not in stop_words])

    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    df['content'] = df['content'].apply(lambda tokens: [lemmatizer.lemmatize(token) for token in tokens])

    # Stemming
    stemmer = PorterStemmer()
    df['content'] = df['content'].apply(lambda tokens: [stemmer.stem(token) for token in tokens])

    # Remove specific words
    df['content'] = df['content'].apply(lambda tokens: [token for token in tokens if token not in ['cooki', 'gov.uk','govuk','’','search', 'page','u','help','menu','chang','set','new','tab','addit', 'insur','carebusi','lawdis','selfemployedchildcar','parentingcitizenship','transporteduc',"'", ',',]])

    # Convert the index of df to a DatetimeIndex
    df.index = pd.to_datetime(df['date'])

    # Filter dates after 2012
    df = df[df.index >= '2012-01-01']

    # Convert the 'date' column to year-month periods
    df['year-month'] = df.index.to_period('M')

    # Convert each year-month period to a timestamp and assign it to the 'Date (by month)' column
    df['Date (by month)'] = df['year-month'].dt.to_timestamp()

    # Set the 'Date (by month)' column as the index of the DataFrame df
    df = df.set_index('Date (by month)')

    return df
