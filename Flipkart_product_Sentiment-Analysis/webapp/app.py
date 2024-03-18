from flask import Flask, render_template, request

import sklearn
import joblib 


app = Flask(__name__)

# Load the model
with open('models/logistic_regression.pkl', 'rb') as file:
    loaded_model = joblib.load(file)



# Define a function to predict the sentiment
def predict(text):
    
    
    sentiment_prediction = loaded_model.predict([text]) 
    if sentiment_prediction==1:
        prediction="Positive Review"
    else:
        prediction="Negative Review"
    
    return prediction

# Define routes and render HTML templates
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict_sentiment():
    if request.method == "POST":
        user_input = request.form["user_input"]
        if user_input.strip() != '':
            sentiment = predict(user_input)
            return render_template("results.html", sentiment=sentiment)
        else:
            return render_template("results.html", error="Please enter some text.")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0',port=5000)