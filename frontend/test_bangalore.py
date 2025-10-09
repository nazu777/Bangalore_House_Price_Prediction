import pandas as pd
import numpy as np
import joblib

# Load model and columns
model = joblib.load("bangalore_price_model.pkl")
model_columns = joblib.load("model_columns.pkl")

# Numeric features
numeric_features = ['total_sqft', 'bath', 'Bedroom', 'balcony', 'Hall', 'Kitchen']

# Area types (mutually exclusive)
area_features = ['Built-up  Area', 'Carpet  Area', 'Plot  Area', 'Super built-up  Area']

# Months (mutually exclusive)
months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

# Possession
possession_features = ['Immediate Possession', 'Ready To Move']

# Locations
location_features = [
    'Bannerghatta Road / Arekere / Gottigere', 'Central Bangalore',
    'East Bangalore Corridors', 'Electronic City & Vicinity',
    'HSR Layout & Bommanahalli', 'Hebbal & Thanisandra Corridor',
    'Indiranagar & Domlur', 'JP Nagar & Surroundings',
    'Jayanagar & Basavangudi', 'KR Puram & East',
    'Kengeri & Rajarajeshwari Nagar', 'Koramangala & Surroundings',
    'Marathahalli - Brookefield - ORR', 'Northeast Cluster',
    'Other South Bangalore', 'Others', 'Outer and Peripheral Areas',
    'Rajajinagar & Malleshwaram', 'Sarjapur & Vicinity',
    'Sarjapur Extension & South-East', 'West & North-West Bangalore',
    'Whitefield Cluster', 'Yelahanka'
]

def predict_price():
    print("Enter Bengaluru House Details:\n")
    user_data = {}

    # Numeric features
    for feature in numeric_features:
        val = input(f"{feature} (0 if unknown): ").strip()
        user_data[feature] = float(val) if val else 0.0

    # Area type (mutually exclusive)
    print("\nSelect area type (only one):")
    for i, f in enumerate(area_features, 1):
        print(f"{i}. {f}")
    choice = int(input("Enter choice number: "))
    area_selected = area_features[choice-1]

    # Month (mutually exclusive)
    print("\nSelect month of possession (only one):")
    for i, m in enumerate(months, 1):
        print(f"{i}. {m}")
    month_choice = int(input("Enter choice number: "))
    month_selected = months[month_choice-1]

    # Possession
    poss = input("\nImmediate Possession? (y/n): ").strip().lower()
    if poss == 'y':
        immediate = 'Immediate Possession'
        ready = 'Ready To Move'
    else:
        immediate = 'Ready To Move'
        ready = 'Immediate Possession'

    # Location
    print("\nChoose location:")
    print(", ".join(location_features))
    location_name = input("Location: ").strip()
    if location_name not in location_features:
        print("Location not recognized. Defaulting to 'Others'.")
        location_name = 'Others'

    # Build input dictionary
    input_dict = {col:0 for col in model_columns}
    # Fill numeric
    for f in numeric_features:
        input_dict[f] = user_data[f]

    # Fill area type
    input_dict[area_selected] = 1

    # Fill month
    input_dict[month_selected] = 1

    # Fill possession
    input_dict[immediate] = 1
    input_dict[ready] = 0

    # Fill location
    input_dict[location_name] = 1

    # Convert to DataFrame
    input_df = pd.DataFrame([input_dict])

    # Predict
    price = model.predict(input_df)[0]
    print(f"\nPredicted Price: ₹{np.expm1(price):,.2f} Lakhs")

if __name__ == "__main__":
    predict_price()
