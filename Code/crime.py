from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn import metrics
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import ComplementNB
from sklearn.feature_selection import chi2
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = [15, 5]
crime_data = pd.read_csv('C:/Users/Sandi/Downloads/Crime1.csv',
                           sep= ',', header= 0)
columnsTitles=['Category', 'Dates', 'Descript', 'DayOfWeek', 'PdDistrict', 'Resolution', 'Address', 'X', 'Y']
crime_data=crime_data.reindex(columns=columnsTitles)
crime_data= crime_data[:3000]

crime_data['category_id'] = crime_data['Category'].factorize()[0]
crime_data['Date_id'] = crime_data['Dates'].factorize()[0]
#crime_data['Time_id'] = crime_data['Time'].factorize()[0]
crime_data['DayOfWeek_id'] = crime_data['DayOfWeek'].factorize()[0]
crime_data['PdDistrict_id'] = crime_data['PdDistrict'].factorize()[0]
crime_data['Resolution_id'] = crime_data['Resolution'].factorize()[0]
crime_data['Address_id'] = crime_data['Address'].factorize()[0]
columnsTitles=['Category', 'category_id', 'Date_id','Descript', 'DayOfWeek', 'DayOfWeek_id','PdDistrict','PdDistrict_id', 'Resolution', 'Resolution_id','Address','Address_id', 'X', 'Y']
crime_data=crime_data.reindex(columns=columnsTitles)

'''
category_id_df = crime_data[['Category', 'category_id']].drop_duplicates().sort_values('category_id')
category_to_id = dict(category_id_df.values)
id_to_category = dict(category_id_df[['category_id', 'Category']].values)
'''

tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2', encoding='latin-1', ngram_range=(1, 2), stop_words='english')

features = tfidf.fit_transform(crime_data['Descript']).toarray()
features2 = tfidf.fit_transform(crime_data['DayOfWeek']).toarray()
print(features2)
labels = crime_data['category_id']
features.shape
'''
N = 2
for Category, category_id in sorted(category_to_id.items()):
    features_chi2 = chi2(features, labels == category_id)
    indices = np.argsort(features_chi2[0])
    feature_names = np.array(tfidf.get_feature_names())[indices]
    unigrams = [v for v in feature_names if len(v.split(' ')) == 1]
    bigrams = [v for v in feature_names if len(v.split(' ')) == 2]
    print("# '{}':".format(Category))
    print("  . Most correlated unigrams:\n       . {}".format('\n       . '.join(unigrams[-N:])))
    print("  . Most correlated bigrams:\n       . {}".format('\n       . '.join(bigrams[-N:])))
'''