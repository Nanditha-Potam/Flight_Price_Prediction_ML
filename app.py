from flask import Flask, request, render_template
from flask_cors import cross_origin
import pickle
import pandas as pd

app = Flask(__name__)
model = pickle.load(open("flight_predict_model.pkl", "rb"))
print("Model loaded successfully.")

def convert_duration_to_minutes(duration):
    hours, minutes = 0, 0
    if 'h' in duration:
        hours = int(duration.split('h')[0].strip())
    if 'm' in duration:
        minutes = int(duration.split('h')[-1].split('m')[0].strip())
    return hours * 60 + minutes

@app.route("/")
@cross_origin()
def home():
    return render_template("index.html")

@app.route("/predict", methods=["GET", "POST"])
@cross_origin()
def predict():
    if request.method == "POST":
        # Date_of_Journey
        date_dep = request.form["date_of_journey"]
        journey_day = int(pd.to_datetime(date_dep).day)
        journey_month = int(pd.to_datetime(date_dep).month)

        # Departure time
        dep_time = request.form["Dep_Time"]
        dep_hour, dep_min = map(int, dep_time.split(':'))

        # Arrival time
        arr_time = request.form["Arr_Time"]
        arrival_hour, arrival_min = map(int, arr_time.split(':'))

        # Duration
        duration_input = request.form["Duration"]
        total_duration_minutes = convert_duration_to_minutes(duration_input)

        # Total Stops
        Total_Stops = int(request.form["stops"])

        # Airline
        airline = request.form['airline']
        Airline_AirIndia = 1 if airline == 'Air India' else 0
        Airline_GoAir = 1 if airline == 'GoAir' else 0
        Airline_IndiGo = 1 if airline == 'IndiGo' else 0
        Airline_JetAirways = 1 if airline == 'Jet Airways' else 0
        Airline_Jet_Airways_Business = 1 if airline == 'Jet Airways Business' else 0
        Airline_Multiple_Carriers = 1 if airline == 'Multiple carriers' else 0
        Airline_Multiple_Carriers_Premium_Economy = 1 if airline == 'Multiple carriers Premium economy' else 0
        Airline_SpiceJet = 1 if airline == 'SpiceJet' else 0
        Airline_Trujet = 1 if airline == 'Trujet' else 0
        Airline_Vistara = 1 if airline == 'Vistara' else 0
        Airline_Vistara_Premium_Economy = 1 if airline == 'Vistara Premium economy' else 0

        # Source
        Source = request.form["source"]
        Source_Chennai = 1 if Source == 'Chennai' else 0
        Source_Delhi = 1 if Source == 'Delhi' else 0
        Source_Kolkata = 1 if Source == 'Kolkata' else 0
        Source_Mumbai = 1 if Source == 'Mumbai' else 0

        # Destination
        Destination = request.form["destination"]
        Destination_Cochin = 1 if Destination == 'Cochin' else 0
        Destination_Delhi = 1 if Destination == 'Delhi' else 0
        Destination_Hyderabad = 1 if Destination == 'Hyderabad' else 0
        Destination_Kolkata = 1 if Destination == 'Kolkata' else 0

        # Create input DataFrame for prediction in correct order
        input_data = pd.DataFrame([[
            Total_Stops,
            journey_day,
            journey_month,
            arrival_hour,
            arrival_min,
            dep_hour,
            dep_min,
            total_duration_minutes,
            Airline_AirIndia,
            Airline_GoAir,
            Airline_IndiGo,
            Airline_JetAirways,
            Airline_Jet_Airways_Business,
            Airline_Multiple_Carriers,
            Airline_Multiple_Carriers_Premium_Economy,
            Airline_SpiceJet,
            Airline_Trujet,
            Airline_Vistara,
            Airline_Vistara_Premium_Economy,
            Source_Chennai,
            Source_Delhi,
            Source_Kolkata,
            Source_Mumbai,
            Destination_Cochin,
            Destination_Delhi,
            Destination_Hyderabad,
            Destination_Kolkata,
        ]], columns=[
            'Total_Stops',
            'Journey_date',
            'Journey_month',
            'Arrival_hour',
            'Arrival_min',
            'Dep_hour',
            'Dep_min',
            'Total_Duration_Minutes',
            'Airline_Air India',
            'Airline_GoAir',
            'Airline_IndiGo',
            'Airline_Jet Airways',
            'Airline_Jet Airways Business',
            'Airline_Multiple carriers',
            'Airline_Multiple carriers Premium economy',
            'Airline_SpiceJet',
            'Airline_Trujet',
            'Airline_Vistara',
            'Airline_Vistara Premium economy',
            'Source_Chennai',
            'Source_Delhi',
            'Source_Kolkata',
            'Source_Mumbai',
            'Destination_Cochin',
            'Destination_Delhi',
            'Destination_Hyderabad',
            'Destination_Kolkata',
        ])

        # Make prediction
        prediction = model.predict(input_data)
        
        output = round(prediction[0], 2)
        return render_template('index.html', prediction_text="Your Flight price is Rs. {}".format(output))

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
