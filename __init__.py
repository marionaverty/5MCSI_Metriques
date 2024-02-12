from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__) 

                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #Comm2

@app.route("/contact/")
def MaPremiereAPI():
    return  render_template("contact.html")

@app.route('/paris/')
def meteo():
    response = urlopen('https://api.openweathermap.org/data/2.5/forecast/daily?q=Paris,fr&cnt=16&appid=bd5e378503939ddaee76f12ad7a97608')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('temp', {}).get('day') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def mongraphiqueG():
    return render_template("histogramme.html")

@app.route("/commits/")
def commits():
  import requests
from datetime import datetime

# Fonction pour extraire les minutes d'une chaîne de date
def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return minutes

# URL de l'API GitHub pour les commits
github_api_url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"

# Effectuer une requête GET à l'API GitHub
response = requests.get(github_api_url)

# Vérifier si la requête a réussi
if response.status_code == 200:
    commits_data = response.json()  # Convertir la réponse en JSON
    commits_per_minute = {}  # Dictionnaire pour stocker le nombre de commits par minute

    # Parcourir les données des commits
    for commit in commits_data:
        commit_date = commit['commit']['author']['date']
        commit_minute = extract_minutes(commit_date)
        
        # Ajouter ou incrémenter le nombre de commits pour cette minute
        commits_per_minute[commit_minute] = commits_per_minute.get(commit_minute, 0) + 1

    # Afficher le nombre de commits par minute
    for minute, count in commits_per_minute.items():
        print(f"{minute} : {count}")

    # Maintenant, vous pouvez utiliser ces données pour créer votre graphique
else:
    print("Échec de la requête à l'API GitHub")

  
if __name__ == "__main__":
  app.run(debug=True)
