from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import joblib
import test_bangalore  # your existing prediction script

app = Flask(__name__)

def predict_from_input(inputs):
    """
    inputs: dict containing numeric features, area_type, month, possession, location
    returns: predicted price
    """
    model = test_bangalore.model
    model_columns = test_bangalore.model_columns

    input_dict = {col: 0 for col in model_columns}

    # Numeric
    for f in test_bangalore.numeric_features:
        input_dict[f] = float(inputs.get(f, 0))

    # Area type (mutually exclusive)
    input_dict[inputs['area_type']] = 1

    # Month (mutually exclusive)
    input_dict[inputs['month']] = 1

    # Possession
    if inputs['immediate']:
        input_dict['Immediate Possession'] = 1
        input_dict['Ready To Move'] = 0
    else:
        input_dict['Immediate Possession'] = 0
        input_dict['Ready To Move'] = 1

    # Location
    location = inputs.get('location', 'Others')
    if location in input_dict:
        input_dict[location] = 1
    else:
        input_dict['Others'] = 1

    df = pd.DataFrame([input_dict])
    price = model.predict(df)[0]
    return np.expm1(price)

@app.route('/')
def home():
    return render_template(
        "index.html",
        numeric_features=test_bangalore.numeric_features,
        area_features=test_bangalore.area_features,
        months=test_bangalore.months,
        location_features=test_bangalore.location_features
    )

@app.route('/predict', methods=['POST'])
def predict():
    data = request.form
    inputs = {f: data.get(f, 0) for f in test_bangalore.numeric_features}
    inputs['area_type'] = data.get('area_type')
    inputs['month'] = data.get('month')
    inputs['immediate'] = data.get('immediate') == 'y'
    inputs['location'] = data.get('location')

    price = predict_from_input(inputs)
    return jsonify({"predicted_price": f"₹{price:,.2f} Lakhs"})

if __name__ == "__main__":
    app.run(debug=True)
