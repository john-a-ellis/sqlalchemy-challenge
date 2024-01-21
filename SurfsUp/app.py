# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (  
        f"<h1 style='color:blue; font-family:verdana'>Welcome to the Hawaii Weather Tracker</h1>"
        f"Available Routes:<br/>"
        f"<a href='http:/api/v1.0/precipitation'>/api/v1.0/precipitation</a><br/>"
        f"<a href='http:/api/v1.0/stations'>/api/v1.0/stations</a></br>"
        f"<a href='http:/api/v1.0/tobs'>/api/v1.0/tobs</a></br>"
        f"/api/v1.0/<start></br>"
        f"/api/v1.0/<start>/<end></br>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():


    """Returns json with the date as the key and the value as the precipitation
    Only returns the jsonified precipitation data for the last year in the database """
    # Query precipitation measurments for the most recent year
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').all()

    session.close()

    # Convert list of tuples into normal list
    # mylist = list(np.ravel(results))
    
    mylist = []
    for date, prcp in results:
        mylist_dict = {}
        mylist_dict[date] = prcp
        mylist.append(mylist_dict)


    return jsonify(mylist)

@app.route("/api/v1.0/stations")
def stations():


    """Return a JSON list of stations from the dataset."""
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    mylist = list(np.ravel(results))
    # return(results)
    return jsonify(mylist)

@app.route("/api/v1.0/tobs")
def tobs():
    
    """Returns jsonified data for the most active station (USC00519281)
Only returns the jsonified data for the last year of data """
    # Query precipitation measurments for the most recent year
    results = session.query(Measurement.date, Measurement.tobs)\
                       .filter(Measurement.date >= '2016-08-23')\
                       .filter(Measurement.station =='USC00519281')\
                       .order_by(Measurement.date).all()

    session.close()

    # Convert list of tuples into normal list
    mylist = list(np.ravel(results))
    return jsonify(mylist)


@app.route("/api/v1.0/<start>")
def start(start):

    """Accepts the start date as a parameter from the URL. Returns the min, max, and average temperatures 
        calculated from the given start date to the end of the dataset"""

    results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs), func.max(Measurement.tobs))\
                       .filter(Measurement.date >= start).all()

    session.close()

    # Convert list of tuples into normal list
    mylist = list(np.ravel(results))
    return jsonify(mylist)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):


    """Accepts the start and end dates as parameters from the URL. Returns the min, max, and average 
        temperatures calculated from the given start date to the given end date"""
    
    print(f"looking for {start} to {end}")
    results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs), func.max(Measurement.tobs))\
                       .filter(Measurement.date >= start)\
                       .filter(Measurement.date <= end).all()

    session.close()

    # Convert list of tuples into normal list
    mylist = list(np.ravel(results))
    return jsonify(mylist)

if __name__ == '__main__':
    app.run(debug=True)


