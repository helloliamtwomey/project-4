from nltk.stem import WordNetLemmatizer
from flask import Flask, request, render_template
from flask_wtf.csrf import CSRFProtect
from flask_caching import Cache
import contractions
import joblib
import string
import os
import re

app = Flask(__name__, static_url_path='/Users/liamtwomey/Desktop/my_project/static')

# Load the pre-trained machine learning model
model_path = os.path.join('models', 'pre-trained-model.pkl')
model = joblib.load(model_path)

# Initialize Flask-Caching
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# Preprocess the data here
def preprocess_data(text):
    # lowercasing
    text = text.lower()
    
    # expand contractions
    text = contractions.fix(text)
    
    # remove punctuations
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    
    # remove double spaces
    text = re.sub(' +', ' ', text)
    
    # lemmatize text
    lemmatizer = WordNetLemmatizer()
    text = ' '.join([lemmatizer.lemmatize(word) for word in text.split()])
    
    return text

# Use the model to make predictions
@cache.memoize(timeout=60)
def get_prediction(data):
    # Preprocess the data
    preprocessed_data = preprocess_data(data)
    
    # Use the model to make predictions
    prediction = model.predict(preprocessed_data)
    
    # Determine the health issue based on the prediction
    if prediction == 'respiratory':
        issue = 'Respiratory Issue'
    elif prediction == 'digestive':
        issue = 'Digestive Issue'
    elif prediction == 'mental':
        issue = 'Mental Health Issue'
    else:
        issue = 'Unknown Issue'
    
    return issue

# Render the index page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Retrieve the data submitted in the form
        data = request.form['data']
        
        # Retrieve the response data from the cache if it exists
        response = cache.get(data)
        
        if not response:
            # Call the get_prediction function if the response data is not in the cache
            response = get_prediction(data)
            
            # Store the response data in the cache
            cache.set(data, response)
        
        return render_template('index.html', response=response)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)