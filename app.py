from flask import Flask, request, render_template
from flask_cors import cross_origin
import sklearn
import pickle
import pandas as pd

app = Flask(__name__)
model = pickle.load(open("flight_rf.pkl", "rb"))

@app.route("/")
@cross_origin()
def home():
    return render_template("home.html")

   
@app.route("/predict", methods = ["GET", "POST"])
@cross_origin()
def predict():
    if request.method == "POST":
        date_dep = request.form["Dep_Time"]            #   2021-01-15T08:12
        date_arr = request.form["Arrival_Time"]        
        Total_stops = int(request.form["stops"])
        airline=request.form['airline']
        Source = request.form["Source"]
        Destination = request.form["Destination"]
        
        #Journey date and month by date departure
        Journey_date = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day)
        Journey_month = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").month)
        dep_hr = int(pd.to_datetime(date_dep,format= "%Y-%m-%dT%H:%M").hour)
        dep_min = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").minute)
        
        #Arrival hour and minute
        arrival_hr = int(pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").hour)
        arrival_min = int(pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").minute)
        
        #duration of flight
        duration_hr = abs(arrival_hr - dep_hr)
        duration_min = abs(arrival_min - dep_min)
        
        #stops 
        if Total_stops == "non-stop":
            stops = 0
        elif Total_stops == "1":
            stops = 1
        elif Total_stops == "2":
            stops = 2
        elif Total_stops == "3":
            stops = 3
        else:
            stops = 4
            
        # Airline
        airline_Jet_airways = 0
        airline_IndiGo = 0
        airline_Air_India = 0                                            
        airline_Multiple_carriers = 0  
        airline_SpiceJet =  0
        airline_Vistara =  0 
        airline_GoAir = 0   
        airline_Multiple_carriers_Premium_economy = 0 
        airline_Jet_Airways_Business = 0
        airline_Vistara_Premium_economy = 0
        airline_Trujet = 0
        if airline == "Jet Airways":
            airline_Jet_airways = 1
        elif airline == "Indigo":    
            airline_IndiGo = 1
        elif airline == "Air India":
            airline_Air_India = 1
        elif airline == "Multiple carriers":
            airline_Multiple_carriers = 0  
        elif airline =="SpiceJet":
            airline_SpiceJet =  0
        elif airline =="Vistara":    
            airline_Vistara =  0 
        elif airline == "GoAir":    
            airline_GoAir = 0   
        elif airline == "Multiple carriers Premium economy":    
            airline_Multiple_carriers_Premium_economy = 0 
        elif airline == "Jet Airways Business":    
            airline_Jet_Airways_Business = 0
        elif airline == "Vistara Premium economy":    
            airline_Vistara_Premium_economy = 0
        elif airline =="Trujet":    
            airline_Trujet = 0
            
        # Source of city
        Source_Delhi = 0
        Source_Kolkata = 0
        Source_Mumbai = 0
        Source_Chennai = 0
        if Source=="Delhi":
            Source_Delhi = 1
        elif Source == "Kolkata":
            Source_Kolkata = 1
        elif Source == "Mumbai":
            Source_Mumbai = 1
        elif Source == "Chennai":
            Source_Chennai = 1
            
        # Destination
        Destination_Cochin = 0
        Destination_Delhi = 0
        Destination_Hyderabad = 0
        Destination_Kolkata = 0
        Destination_New_Delhi = 0
        if Destination == "Cochin":
            Destination_Cochin = 1
        elif Destination == "Delhi":
            Destination_Delhi = 1
        elif Destination == "Hyderabad":
            Destination_Hyderabad= 1
        elif Destination == "Kolkata":
            Destination_Kolkata = 1
        elif Destination == "New Delhi":
            Destination_New_Delhi = 1
            
        list_of_values = [stops, Journey_date, Journey_month, dep_hr,dep_min, arrival_hr, arrival_min, duration_hr, duration_min,airline_Air_India, airline_GoAir, airline_IndiGo,airline_Jet_airways, airline_Jet_Airways_Business,airline_Multiple_carriers,airline_Multiple_carriers_Premium_economy, airline_SpiceJet,airline_Trujet, airline_Vistara, airline_Vistara_Premium_economy,Source_Chennai, Source_Delhi, Source_Kolkata, Source_Mumbai,Destination_Cochin, Destination_Delhi, Destination_Hyderabad, Destination_Kolkata, Destination_New_Delhi]
        
        model = open('flight_rf.pkl',"rb")
        forest = pickle.load(model)
        prediction = forest.predict([list_of_values])
        
        output=round(prediction[0],2)

        return render_template('home.html',prediction_text="Your previous Flight price prediction is Rs. {}".format(output))
        
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)    
