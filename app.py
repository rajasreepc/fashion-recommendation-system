from flask import Flask, request, render_template
import pandas as pd
import numpy as np
import pickle
import os
import requests
import time
import random


app = Flask(__name__,template_folder='templates')
@app.route('/', methods=['GET', 'POST'])
def main():
    
    # If a form is submitted
    if request.method == "POST":
        
        # Unpickle classifier
        model = pickle.load(open("model.pkl", "rb"))
        # le = pickle.load(open("le.pkl", "rb"))
        
        # Get values through input bars
        print("RFORM", request.form)
        Height = float(request.form.get("Height"))
        Bust = float(request.form.get("Bust"))
        Waist = float(request.form.get("Waist"))
        Hips = float(request.form.get("Hips"))

        X = pd.DataFrame([[Height, Bust, Waist, Hips]], columns = ["Height", "Bust", "Waist","Hips" ])
        print("final dataset",X)
        prediction = model.predict(X)[0]
        print("prediction",prediction)
        df_cloth = pd.read_csv('recommenderdata.csv')
        df_rec_winter = df_cloth[(df_cloth['BodyShape'] == prediction) & (df_cloth['Season'] == "Winter") ] 
        df_rec_summer = df_cloth[(df_cloth['BodyShape'] == prediction) & (df_cloth['Season'] == "Summer") ] 
        summer_clothes = df_rec_summer["URL"].tolist()
        winter_clothes = df_rec_winter["URL"].tolist()
        n = 4
        
        if len(summer_clothes) > 4:
            summer_clothes = random.sample(summer_clothes, n)
        
        if len(winter_clothes) > 4:
            winter_clothes = random.sample(winter_clothes, n)
        
        
        return render_template("website.html", prediction = prediction , summer_image = summer_clothes, winter_image = winter_clothes )


    elif request.method == "GET":
        return render_template("website.html")

if __name__ == '__main__':
    app.run(debug = True)