
import pandas as pd

# Marketing PriceWise - Master Vehicle Database

VEHICLES = [
    {
        "Brand": "Hero",
        "Model": "Splendor Plus",
        "Vehicle Type": "Motorcycle",
        "Category": "Commuter",
        "Fuel Type": "Petrol",
        "Engine CC": 97.2,
        "Market Status": "Verify",
        "Source": "Hero official website"
    },
    {
        "Brand": "Honda",
        "Model": "Shine 100",
        "Vehicle Type": "Motorcycle",
        "Category": "Commuter",
        "Fuel Type": "Petrol",
        "Engine CC": 98.98,
        "Market Status": "Verify",
        "Source": "Honda official website"
    },
    {
        "Brand": "TVS",
        "Model": "Raider 125",
        "Vehicle Type": "Motorcycle",
        "Category": "Street",
        "Fuel Type": "Petrol",
        "Engine CC": 124.8,
        "Market Status": "Verify",
        "Source": "TVS official website"
    },
    {
        "Brand": "Bajaj",
        "Model": "Pulsar N160",
        "Vehicle Type": "Motorcycle",
        "Category": "Street",
        "Fuel Type": "Petrol",
        "Engine CC": 164.8,
        "Market Status": "Verify",
        "Source": "Bajaj official website"
    },
    {
        "Brand": "Yamaha",
        "Model": "MT-15",
        "Vehicle Type": "Motorcycle",
        "Category": "Street Naked",
        "Fuel Type": "Petrol",
        "Engine CC": 155,
        "Market Status": "Verify",
        "Source": "Yamaha official website"
    },
    {
        "Brand": "Royal Enfield",
        "Model": "Classic 350",
        "Vehicle Type": "Motorcycle",
        "Category": "Cruiser",
        "Fuel Type": "Petrol",
        "Engine CC": 349,
        "Market Status": "Verify",
        "Source": "Royal Enfield official website"
    },
    {
        "Brand": "Honda",
        "Model": "Activa",
        "Vehicle Type": "Scooter",
        "Category": "Commuter",
        "Fuel Type": "Petrol",
        "Engine CC": 109.5,
        "Market Status": "Verify",
        "Source": "Honda official website"
    },
    {
        "Brand": "TVS",
        "Model": "XL100",
        "Vehicle Type": "Moped",
        "Category": "Utility",
        "Fuel Type": "Petrol",
        "Engine CC": 99.7,
        "Market Status": "Verify",
        "Source": "TVS official website"
    },
    {
        "Brand": "TVS",
        "Model": "iQube",
        "Vehicle Type": "Scooter",
        "Category": "Electric",
        "Fuel Type": "Electric",
        "Engine CC": None,
        "Market Status": "Verify",
        "Source": "TVS official website"
    },
    {
        "Brand": "Bajaj",
        "Model": "Chetak",
        "Vehicle Type": "Scooter",
        "Category": "Electric",
        "Fuel Type": "Electric",
        "Engine CC": None,
        "Market Status": "Verify",
        "Source": "Bajaj official website"
    }
]

def get_vehicle_dataframe():
    """Return the master vehicle database as a Pandas DataFrame."""
    return pd.DataFrame(VEHICLES)

def get_vehicle_summary():
    """Return basic database statistics."""
    df = get_vehicle_dataframe()

    return {
        "total_models": len(df),
        "total_brands": df["Brand"].nunique(),
        "vehicle_types": df["Vehicle Type"].nunique(),
        "fuel_types": df["Fuel Type"].nunique()
    }