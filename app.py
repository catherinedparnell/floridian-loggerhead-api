from flask import Flask, request, jsonify
import constants
import calculations
import requests
import library

app = Flask(__name__)

@app.route('/')
def produce_info():
    days_second = request.args.get('days_second', type=int)

    hatch_time = calculations.produce_egg_time(days_second, constants.HATCH_DAYS)
    incubation_time = calculations.produce_egg_time(days_second, constants.INCUBATION_DAYS)
    season_time = calculations.produce_turtle_time(days_second, constants.SEASON_YEARS)
    maturity_time = calculations.produce_turtle_time(days_second, constants.MATURITY_YEARS)
    turtle_time = calculations.produce_turtle_time(days_second, constants.TURTLE_YEARS)
    decade_time = calculations.produce_turtle_time(days_second, constants.DECADE)

    res = dict({ 
        "seasonTime": season_time, 
        "maturityTime": maturity_time, 
        "maxAge": turtle_time, 
        "hatchTime": hatch_time, 
        "incubationTime": incubation_time,
        "decadeTime": decade_time
        })
    return jsonify(res)

@app.route('/geo')
def get_beach_data():
    density = request.args.get('density', type=str)

    geo_data = requests.get(constants.GEO_API)
    geo_json = geo_data.json()

    features = geo_json["features"]

    i = 0
    low = 0
    med = 0
    high = 0

    low_beaches = []
    med_beaches = []
    high_beaches = []

    for beach in features:
        if beach["attributes"]["ccDensClass"] != "not present":
            i += 1
            if beach["attributes"]["ccDensClass"] == "LOW":
                low += 1
                if beach["attributes"]["Beach"] not in low_beaches:
                    low_beaches.append(library.parseOutput(beach["attributes"]))
            elif beach["attributes"]["ccDensClass"] == "MED":
                med += 1
                if beach["attributes"]["Beach"] not in med_beaches:
                    med_beaches.append(library.parseOutput(beach["attributes"]))
            elif beach["attributes"]["ccDensClass"] == "HIGH":
                high += 1
                if beach["attributes"]["Beach"] not in high_beaches:
                    high_beaches.append(library.parseOutput(beach["attributes"]))

    print('There are', len(features), 'nesting beaches in florida')
    print('There are', i, 'nesting beaches for loggerheads in florida')
    print('There are', low, 'beaches with low loggerhead nesting patterns')
    print('There are', med, 'beaches with med loggerhead nesting patterns')
    print('There are', high, 'beaches with high loggerhead nesting patterns')

    if not density:
        response = dict({ "low_beaches": low_beaches, "med_beaches": med_beaches, "high_beaches": high_beaches})
    elif density == "high":
        response = dict({ 'high_beaches': high_beaches })
    elif density == "med":
        response = dict({ 'med_beaches': med_beaches })
    elif density == "low":
        response = dict({ 'low_beaches': low_beaches })

    return jsonify(response)