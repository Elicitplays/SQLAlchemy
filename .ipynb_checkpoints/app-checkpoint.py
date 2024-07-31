# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify, render_template



#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
measurement = Base.classes.measurement
station = Base.classes.station

# Create a session
session = Session(bind=engine)

recent = session.query(measurement.date).order_by(measurement.date.desc()).first().date
year=dt.datetime.strptime(recent,'%Y-%m-%d') - dt.timedelta(days=365)



#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def opening():
        return render_template ("page.html")

@app.route("/api/precipitation")
def precip():

    #perform query
    precip = session.query(measurement.date, measurement.prcp).\
                        filter(measurement.date >= year).\
                        order_by(measurement.date).all()
    session.close()

    #Store as dict

    precip_dic = dict(precip)

    print(precip_dic)

    return jsonify(precip_dic)

@app.route("/api/stations")
def stations():
    
    #perform query
    stations = session.query(station.station).all()

    session.close()

    #list stations
    station_dic = list(np.ravel(stations))

    print(station_dic)

    return jsonify(station_dic)

@app.route("/api/tobs")
def tobs():

    #perform query
    year_results = session.query(measurement.tobs).\
                            filter(measurement.station =='USC00519281').\
                            filter(measurement.date > year).all()
    session.close()
    #store as dict
    tobs_dic = dict(tobs_dic)

    print(tobs_dic)
    return jsonify(tobs_dic)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
    
    
    



