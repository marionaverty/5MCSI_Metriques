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
import matplotlib.pyplot as plt
from datetime import datetime

# Fonction pour extraire les minutes à partir d'une chaîne de date
def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return minutes

# API URL pour extraire les commits
api_url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"

# Effectuer la requête GET à l'API
response = requests.get(api_url)

# Vérifier si la requête a réussi
if response.status_code == 200:
    # Extraire les données JSON de la réponse
    commits_data = response.json()

    # Initialiser un dictionnaire pour stocker le nombre de commits par minute
    commits_per_minute = {}

    # Parcourir les données des commits
    for commit in commits_data:
        # Extraire la date du commit et les minutes correspondantes
        commit_date = commit['commit']['author']['date']
        minute = extract_minutes(commit_date)

        # Mettre à jour le dictionnaire avec le nombre de commits pour cette minute
        commits_per_minute[minute] = commits_per_minute.get(minute, 0) + 1

    # Convertir le dictionnaire en listes de minutes et de nombre de commits
    minutes = list(commits_per_minute.keys())
    commits_count = list(commits_per_minute.values())

    # Tracer le graphique
    plt.figure(figsize=(10, 6))
    plt.plot(minutes, commits_count, marker='o', linestyle='-')
    plt.title('Nombre de Commits par Minute')
    plt.xlabel('Minute')
    plt.ylabel('Nombre de Commits')
    plt.grid(True)
    plt.show()

else:
    print("La requête à l'API a échoué.")
  
if __name__ == "__main__":
  app.run(debug=True)
