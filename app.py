from flask import Flask, request, render_template
import pickle
import numpy as np

app = Flask(__name__)

model = pickle.load(open('model.pkl', 'rb'))

@app.route("/")
def hello_world():
    return render_template('index.html', result='🤔')

@app.route("/result/", methods=['POST', 'GET'])
def predict_value():
    try:
        longitude = float(request.form['longitude'])
        latitude = float(request.form['latitude'])
        med_age = float(request.form['med_age'])
        total_rooms = float(request.form['total_rooms'])
        total_bedrooms = float(request.form['total_bedrooms'])
        population = float(request.form['population'])
        households = float(request.form['households'])
        med_income = float(request.form['med_income'])
        ocean_prox = request.form['ocean_proximity']
    
    except:
        return render_template('index.html', 
                               result='Incomplete or invalid input...',
                               state='failure')

    try:
        bedroom_ratio = total_bedrooms / total_rooms
        household_ratio = households / population
        room_ratio = total_rooms / households
    
    except:
        return render_template('index.html', 
                               result='Total rooms, population, or households cannot be 0...',
                               state='failure')

    one_hr = ocean_prox == '<1H OCEAN'
    inland = ocean_prox == 'INLAND'
    island = ocean_prox == 'ISLAND'
    near_bay = ocean_prox == 'NEAR BAY'
    near_ocean = ocean_prox == 'NEAR OCEAN'

    input = [np.array([longitude, latitude, med_age, total_rooms,
                     total_bedrooms, population, households,
                     med_income, bedroom_ratio, household_ratio,
                     room_ratio, one_hr, inland,
                     island, near_bay, near_ocean])]

    prediction = model.predict(input)
    output = '${pred:.2f}'.format(pred=round(prediction[0], -2))

    return render_template('index.html', result=output, state='success')

if __name__ == '__main__':
    app.run()