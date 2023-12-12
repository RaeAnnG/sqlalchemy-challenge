# Import the dependencies.
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Station = Base.classes.station
measurement = Base.classes.measurement

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
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start<br/>"
        f"/api/v1.0/temp/start/end"
    )


# Query results from precipitation analysis - last 12 months
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query list of date and prcp
    presults = session.query(measurement.date, measurement.prcp).all()
    
    session.close()

    # Convert list of tuples into dictionary
    all_prcp = []
    for date,prcp in presults:
        prcp_dict = {}
        prcp_dict[date] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

# Query List of Stations
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query list of date and prcp
    sresults = session.query(Station.station).all()
    
    session.close()
    print (sresults)
    # Convert list into dictionary
    all_stations = list(np.ravel(sresults))

    return jsonify(all_stations)

# Query the date and temp observations of the most active stations 
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query the most active station
    tresults = session.query(measurement.tobs).\
        filter(measurement.date>='2016-08-23').filter(measurement.station == 'USC00519281').all()
    
    session.close()

    # Convert list into dictionary
    tobs_list = list(np.ravel(tresults)) 

    return jsonify(tobs_list)

# Return the min, avg, and max temps for a specified start or start-end range.
@app.route("/api/v1.0/temp/<start>")
def stats(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query list
    rresults = session.query(func.min(measurement.tobs),
                             func.avg(measurement.tobs),
                             func.max(measurement.tobs)).\
                            filter(measurement.date >= start).all()
    
    session.close()

    # Convert list into dictionary
    temp_list = list(np.ravel(rresults)) 

    return jsonify(temp_list)

# Return the min, avg, and max temps for a specified start or start-end range.
@app.route("/api/v1.0/temp/<start>/<end>")
def stats2(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query list
    rresults = session.query(func.min(measurement.tobs),
                             func.avg(measurement.tobs),
                             func.max(measurement.tobs)).\
                            filter(measurement.date >= start).\
                            filter(measurement.date <= end).\
                            all()

    
    session.close()

    temp_list = list(np.ravel(rresults)) 

    return jsonify(temp_list)


if __name__ == '__main__':
    app.run(debug=True)

    