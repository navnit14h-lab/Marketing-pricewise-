import streamlit as st
import pandas as pd
from datetime import date
from vehicle_data import get_vehicle_dataframe

# -----------------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------------

st.set_page_config(
    page_title="Marketing PriceWise",
    page_icon="🏍️",
    layout="wide"
)

# -----------------------------------------
# 2. WEBSITE DESIGN
# -----------------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}
h1, h2, h3, h4, .stMetric label {
    font-family: 'Manrope', sans-serif;
    letter-spacing: -0.35px;
}
h1 { font-weight: 800; }
h2, h3 { font-weight: 700; }
.stApp {
    background: linear-gradient(
        135deg,
        #101820,
        #202a35,
        #111820
    );
    color: white;
}

h1, h2, h3 {
    color: #F4A261;
}

p, label {
    color: #EAEAEA;
}

div.stButton > button {
    background: linear-gradient(135deg, #E76F51, #F4A261);
    color: white;
    border-radius: 8px;
    border: none;
    height: 45px;
    font-weight: bold;
}

div.stButton > button:hover {
    background-color: #F4A261;
    color: black;
}

[data-testid="stSidebar"] {
    background-color: #151D27;
}
div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.14);
    padding: 14px;
    border-radius: 12px;
}
div[data-testid="stTabs"] button {
    font-weight: 700;
}
.stTextInput input, .stNumberInput input, .stSelectbox div,
.stDateInput input, .stTextArea textarea {
    border-radius: 8px;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------------------
# 3. COMPANY DATABASE
# -----------------------------------------

companies = [
    "Hero MotoCorp",
    "Honda",
    "TVS Motor",
    "Bajaj Auto",
    "Royal Enfield",
    "Suzuki",
    "Yamaha",
    "KTM",
    "Kawasaki",
    "BMW Motorrad",
    "Triumph",
    "Harley-Davidson",
    "Jawa",
    "Yezdi",
    "Aprilia",
    "Vespa",
    "Ather Energy",
    "Ola Electric",
    "Revolt Motors",
    "Ultraviolette",
    "Vida",
    "Bgauss",
    "Oben Electric",
    "Simple Energy",
    "Lectrix EV"
]

# Manufacturer domains used to retrieve brand marks in the report.
# The favicon service may return a compact brand icon rather than a full logo.
COMPANY_DOMAINS = {
    "Hero MotoCorp": "heromotocorp.com",
    "Honda": "honda2wheelersindia.com",
    "TVS Motor": "tvsmotor.com",
    "Bajaj Auto": "bajajauto.com",
    "Royal Enfield": "royalenfield.com",
    "Suzuki": "suzukimotorcycle.co.in",
    "Yamaha": " yamaha-motor-india.com".strip(),
    "KTM": "ktmindia.com",
    "Kawasaki": "kawasaki-india.com",
    "BMW Motorrad": "bmw-motorrad.in",
    "Triumph": "triumphmotorcycles.in",
    "Harley-Davidson": "harley-davidson.com",
    "Jawa": "jawamotorcycles.com",
    "Yezdi": "yezdi.com",
    "Aprilia": "aprilia.com",
    "Vespa": "vespa.com",
    "Ather Energy": "atherenergy.com",
    "Ola Electric": "olaelectric.com",
    "Revolt Motors": "revoltmotors.com",
    "Ultraviolette": "ultraviolette.com",
    "Vida": "vidaworld.com",
    "Bgauss": "bgauss.com",
    "Oben Electric": "obenelectric.com",
    "Simple Energy": "simpleenergy.in",
    "Lectrix EV": "lectrixev.com"
}

# -----------------------------------------
# 4. INDIAN STATES AND UNION TERRITORIES
# -----------------------------------------

states = [
    "Andhra Pradesh",
    "Arunachal Pradesh",
    "Assam",
    "Bihar",
    "Chhattisgarh",
    "Goa",
    "Gujarat",
    "Haryana",
    "Himachal Pradesh",
    "Jharkhand",
    "Karnataka",
    "Kerala",
    "Madhya Pradesh",
    "Maharashtra",
    "Manipur",
    "Meghalaya",
    "Mizoram",
    "Nagaland",
    "Odisha",
    "Punjab",
    "Rajasthan",
    "Sikkim",
    "Tamil Nadu",
    "Telangana",
    "Tripura",
    "Uttar Pradesh",
    "Uttarakhand",
    "West Bengal"
]

union_territories = [
    "Andaman and Nicobar Islands",
    "Chandigarh",
    "Dadra and Nagar Haveli and Daman and Diu",
    "Delhi",
    "Jammu and Kashmir",
    "Ladakh",
    "Lakshadweep",
    "Puducherry"
]

all_locations = sorted(states + union_territories)


# -----------------------------------------
# 5. ENGINE CAPACITY
# -----------------------------------------

engine_options = [
    f"{cc}cc" for cc in range(50, 601, 25)
]


# -----------------------------------------
# 6. VEHICLE CATEGORIES
# -----------------------------------------

vehicle_categories = [
    "Cruiser",
    "Sports Bike",
    "Street Naked",
    "Commuter",
    "Adventure Tourer",
    "Touring",
    "Cafe Racer",
    "Scrambler",
    "Dirt Bike",
    "Scooter",
    "Electric Motorcycle",
    "Electric Scooter"
]


# -----------------------------------------
# 7. COLOUR DATABASE
# -----------------------------------------

colour_names = [
    "Black", "White", "Red", "Blue",
    "Green", "Grey", "Silver", "Gold",
    "Orange", "Yellow", "Purple", "Brown",
    "Bronze", "Copper", "Maroon", "Cream",
    "Pink", "Teal", "Cyan", "Navy"
]

colour_prefixes = [
    "Lightning", "Heaven", "Hell Fire",
    "Midnight", "Royal", "Phantom",
    "Shadow", "Racing", "Electric",
    "Cosmic", "Mystic", "Thunder",
    "Storm", "Arctic", "Desert",
    "Sunset", "Ocean", "Galaxy",
    "Titanium", "Diamond",
    "Metallic", "Pearl", "Crystal",
    "Velvet", "Neon", "Imperial",
    "Stealth", "Inferno"
]

colour_finishes = [
    "", "Metallic", "Matte", "Gloss",
    "Pearl", "Satin", "Chrome",
    "Glossy", "Dual Tone"
]

generated_colours = []

for prefix in colour_prefixes:
    for colour in colour_names:
        for finish in colour_finishes:

            if finish:
                name = f"{prefix} {colour} {finish}"
            else:
                name = f"{prefix} {colour}"

            generated_colours.append(name)

generated_colours = sorted(set(generated_colours))


# -----------------------------------------
# 8. HEADER
# -----------------------------------------

st.title("🏍️ MARKETING PRICEWISE")

st.subheader(
    "Intelligent Pricing Decisions for Two-Wheeler Launches"
)

st.write(
    "A marketing decision-support platform "
    "for competitive vehicle pricing in India."
)

st.divider()


# -----------------------------------------
# 9. NAVIGATION
# -----------------------------------------

st.sidebar.title("MARKETING PRICEWISE")

page = st.sidebar.radio(
    "MAIN MENU",
    [
        "Dashboard",
        "New Vehicle Details",
        "Competitor Analysis",
        "Customer Insights",
        "Pricing Recommendation",
        "Scenario Simulator",
        "Reports"
    ]
)
# ==========================================
# DYNAMIC VEHICLE CATEGORY BACKGROUNDS
# ==========================================

def set_page_background(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image:
                linear-gradient(
                    rgba(10, 15, 22, 0.72),
                    rgba(10, 15, 22, 0.88)
                ),
                url("{image_url}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        h1, h2, h3 {{
            color: #F4A261 !important;
        }}

        p, label {{
            color: white !important;
        }}

        [data-testid="stSidebar"] {{
            background-color: #151D27;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Motorcycle image database
vehicle_backgrounds = {
    "Cruiser":
        "https://images.unsplash.com/photo-1481575184241-4754ea78a1bf?auto=format&fit=crop&w=2000&q=80",

    "Sports Bike":
        "https://images.unsplash.com/photo-1552642762-f55d06580015?auto=format&fit=crop&w=2000&q=80",

    "Street Naked":
        "https://images.unsplash.com/photo-1558981806-ec527fa84c39?auto=format&fit=crop&w=2000&q=80",

    "Commuter":
        "https://images.unsplash.com/photo-1558981806-ec527fa84c39?auto=format&fit=crop&w=2000&q=80",

    "Adventure Tourer":
        "https://images.unsplash.com/photo-1558981806-ec527fa84c39?auto=format&fit=crop&w=2000&q=80",

    "Touring":
        "https://images.unsplash.com/photo-1558981806-ec527fa84c39?auto=format&fit=crop&w=2000&q=80",

    "Cafe Racer":
        "https://images.unsplash.com/photo-1481575184241-4754ea78a1bf?auto=format&fit=crop&w=2000&q=80",

    "Scrambler":
        "https://images.unsplash.com/photo-1481575184241-4754ea78a1bf?auto=format&fit=crop&w=2000&q=80",

    "Dirt Bike":
        "https://images.unsplash.com/photo-1558981806-ec527fa84c39?auto=format&fit=crop&w=2000&q=80",

    "Scooter":
        "https://images.unsplash.com/photo-1558981806-ec527fa84c39?auto=format&fit=crop&w=2000&q=80",

    "Electric Motorcycle":
        "https://images.unsplash.com/photo-1558981806-ec527fa84c39?auto=format&fit=crop&w=2000&q=80",

    "Electric Scooter":
        "https://images.unsplash.com/photo-1558981806-ec527fa84c39?auto=format&fit=crop&w=2000&q=80"
}

# Get the manager's saved vehicle details and apply a relevant background
saved_vehicle = st.session_state.get("vehicle_data", {})
selected_category = saved_vehicle.get("Category", "Cruiser")
selected_image = vehicle_backgrounds.get(
    selected_category,
    vehicle_backgrounds["Cruiser"]
)
set_page_background(selected_image)

# -----------------------------------------
# 10. DASHBOARD
# -----------------------------------------

if page == "Dashboard":

    st.header("Marketing Overview")

    st.write(
        "Welcome to your two-wheeler pricing "
        "decision-support platform."
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Companies Listed", len(companies))
    col2.metric("Colour Options", len(generated_colours))
    col3.metric("Market Locations", len(all_locations))

    st.divider()

    st.subheader("Project Objectives")

    col1, col2 = st.columns(2)

    with col1:
        st.info("🏍️ Competitor Price Analysis")

        st.info("📊 Customer Preference Analysis")

    with col2:
        st.info("💰 Optimal Launch Pricing")

        st.info("📈 Pricing Scenario Simulation")

    st.success(
        "Select New Vehicle Details from the sidebar "
        "to begin."
    )


# -----------------------------------------
# 11. NEW VEHICLE DETAILS
# -----------------------------------------

elif page == "New Vehicle Details":

    st.header("New Vehicle Registration")

    st.write(
        "Enter the proposed vehicle specifications "
        "to begin market and pricing analysis."
    )

    st.subheader("Company Information")

    saved_vehicle = st.session_state.get("vehicle_data", {})
    company_default = saved_vehicle.get("Company", companies[0])
    company_index = companies.index(company_default) if company_default in companies else 0

    company = st.selectbox(
        "Select Company",
        companies,
        index=company_index,
        key="vehicle_company_input"
    )

    model = st.text_input(
        "Enter Model Name",
        value=saved_vehicle.get("Model", ""),
        placeholder="Example: Hunter 350",
        key="vehicle_model_input"
    )

    st.divider()

    st.subheader("Vehicle Specifications")

    col1, col2 = st.columns(2)

    with col1:

        saved_category = saved_vehicle.get("Category", vehicle_categories[0])
        category_index = vehicle_categories.index(saved_category) if saved_category in vehicle_categories else 0
        category = st.selectbox(
            "Vehicle Category",
            vehicle_categories,
            index=category_index,
            key="vehicle_category_input"
        )

        saved_engine = saved_vehicle.get("Engine Capacity", engine_options[0])
        engine_index = engine_options.index(saved_engine) if saved_engine in engine_options else 0
        engine = st.selectbox(
            "Engine Capacity",
            engine_options,
            index=engine_index,
            key="vehicle_engine_input"
        )

    with col2:

        state = st.selectbox(
            "Target State",
            all_locations
        )

        colour = st.selectbox(
            "Select Vehicle Colour",
            generated_colours,
            index=generated_colours.index(
                "Lightning Black Matte"
            )
        )

    st.divider()

    st.subheader("Financial Information")

    col1, col2 = st.columns(2)

    with col1:

        manufacturing_cost = st.number_input(
            "Estimated Manufacturing Cost (₹)",
            min_value=0,
            value=int(saved_vehicle.get("Manufacturing Cost", 65000)),
            step=1000,
            key="vehicle_manufacturing_cost_input"
        )

    with col2:

        target_age = st.selectbox(
            "Target Customer Age",
            ["18-20", "20-25", "25-30", "30-35", "35+"]
        )

    st.divider()

    if st.button("SAVE VEHICLE DETAILS"):

        if not model.strip():

            st.error("Please enter a vehicle model name.")

        else:

            vehicle_data = {
                "Company": company,
                "Model": model,
                "Category": category,
                "Engine Capacity": engine,
                "State": state,
                "Colour": colour,
                "Manufacturing Cost": manufacturing_cost,
                "Target Age": target_age
            }

            st.session_state["vehicle_data"] = vehicle_data

            st.success(
                "Vehicle details saved successfully!"
            )

            st.json(vehicle_data)


# -----------------------------------------
# 12. COMPETITOR ANALYSIS
# -----------------------------------------


elif page == "Competitor Analysis":

    st.header("Competitor Analysis")
    st.caption("Smart competitor benchmarking and launch price positioning")

    vehicle_data = st.session_state.get("vehicle_data", {})

    if not vehicle_data:
        st.warning("Please save your vehicle details first.")

    else:
        company = vehicle_data.get("Company", "Not selected")
        model = vehicle_data.get("Model", "Not entered")
        category = vehicle_data.get("Category", "Cruiser")
        engine = vehicle_data.get("Engine Capacity", "0cc")
        manufacturing_cost = vehicle_data.get("Manufacturing Cost", 0)

        try:
            selected_cc = int(
                ''.join(ch for ch in str(engine) if ch.isdigit())
            )
        except ValueError:
            selected_cc = 0

        st.subheader("Your Selected Vehicle")

        col1, col2, col3 = st.columns(3)
        col1.metric("Company", company)
        col2.metric("Category", category)
        col3.metric("Engine Capacity", f"{selected_cc}cc")

        st.write(f"**Model:** {model}")

        st.divider()

        # SIMULATED COMPETITOR DATA
        
        # CONSOLIDATED COMPETITOR DATABASE
        # Petrol models up to 600cc
        # All prices below are illustrative simulated values.

        competitor_data = [

            # COMMUTER - 90cc to 150cc
            ["Hero", "Splendor Plus", "Commuter", 97.2, 80000],
            ["Hero", "HF Deluxe", "Commuter", 97.2, 65000],
            ["Hero", "Glamour X", "Commuter", 124.7, 90000],
            ["Hero", "Super Splendor", "Commuter", 124.7, 88000],
            ["Hero", "Xtreme 125R", "Commuter", 124.7, 95000],
            ["Honda", "Shine 100", "Commuter", 98.98, 65000],
            ["Honda", "Shine 125", "Commuter", 123.94, 85000],
            ["Honda", "SP 125", "Commuter", 123.94, 92000],
            ["Honda", "CB125 Hornet", "Commuter", 123.94, 115000],
            ["TVS", "Radeon", "Commuter", 109.7, 75000],
            ["TVS", "Sport", "Commuter", 109.7, 65000],
            ["TVS", "Raider 125", "Commuter", 124.8, 90000],
            ["Bajaj", "Platina 110", "Commuter", 115.45, 75000],
            ["Bajaj", "CT 125X", "Commuter", 124.4, 75000],
            ["Bajaj", "Pulsar 125", "Commuter", 124.38, 92000],
            ["Bajaj", "Pulsar NS125", "Commuter", 124.45, 100000],
            ["Bajaj", "Freedom 125 CNG", "Commuter", 124.58, 95000],

            # STREET NAKED - 150cc to 400cc
            ["Yamaha", "FZ-S FI", "Street Naked", 149, 130000],
            ["Yamaha", "MT-15", "Street Naked", 155, 170000],
            ["TVS", "Apache RTR 160", "Street Naked", 159.7, 125000],
            ["TVS", "Apache RTR 180", "Street Naked", 177.4, 140000],
            ["TVS", "Apache RTR 200 4V", "Street Naked", 197.75, 155000],
            ["Bajaj", "Pulsar N150", "Street Naked", 149.68, 125000],
            ["Bajaj", "Pulsar NS160", "Street Naked", 160.3, 135000],
            ["Bajaj", "Pulsar NS200", "Street Naked", 199.5, 155000],
            ["Suzuki", "Gixxer", "Street Naked", 155, 140000],
            ["KTM", "Duke 200", "Street Naked", 199.5, 200000],
            ["KTM", "Duke 250", "Street Naked", 249.07, 220000],
            ["Triumph", "Speed 400", "Street Naked", 398, 240000],
            ["TVS", "Ronin", "Street Naked", 225.9, 150000],
            ["Bajaj", "Pulsar NS400Z", "Street Naked", 373.27, 190000],

            # SPORTS BIKE - 150cc to 500cc
            ["Yamaha", "R15 V4", "Sports Bike", 155, 185000],
            ["Yamaha", "R15M", "Sports Bike", 155, 200000],
            ["Suzuki", "Gixxer SF", "Sports Bike", 155, 145000],
            ["Suzuki", "Gixxer SF 250", "Sports Bike", 249, 195000],
            ["Bajaj", "Pulsar RS200", "Sports Bike", 199.5, 185000],
            ["Bajaj", "Pulsar F250", "Sports Bike", 249, 155000],
            ["KTM", "RC 200", "Sports Bike", 199.5, 220000],
            ["KTM", "RC 390", "Sports Bike", 373, 320000],
            ["TVS", "Apache RR 310", "Sports Bike", 312.12, 280000],
            ["TVS", "Apache RTR 310", "Sports Bike", 312.12, 250000],
            ["BMW", "G 310 RR", "Sports Bike", 312.12, 300000],
            ["Kawasaki", "Ninja 300", "Sports Bike", 296, 340000],
            ["Kawasaki", "Ninja 500", "Sports Bike", 451, 600000],

            # CRUISER - 150cc to 500cc
            ["Bajaj", "Avenger Street 160", "Cruiser", 160, 115000],
            ["Bajaj", "Avenger Cruise 220", "Cruiser", 220, 135000],
            ["Royal Enfield", "Meteor 350", "Cruiser", 349, 205000],
            ["Royal Enfield", "Classic 350", "Cruiser", 349, 193000],
            ["Royal Enfield", "Bullet 350", "Cruiser", 349, 175000],
            ["Jawa", "Jawa 350", "Cruiser", 334, 199000],
            ["Honda", "H'ness CB350", "Cruiser", 348.36, 210000],
            ["Honda", "CB350", "Cruiser", 348.36, 200000],
            ["Keeway", "K-Light 250V", "Cruiser", 249, 200000],
            ["Royal Enfield", "Goan Classic 350", "Cruiser", 349, 210000],

            # ADVENTURE TOURER - 200cc to 500cc
            ["Hero", "Xpulse 200 4V", "Adventure Tourer", 199.6, 150000],
            ["Hero", "Xpulse 210", "Adventure Tourer", 210, 165000],
            ["KTM", "Adventure 250", "Adventure Tourer", 248.76, 250000],
            ["KTM", "Adventure 390", "Adventure Tourer", 399, 350000],
            ["Suzuki", "V-Strom SX", "Adventure Tourer", 249, 215000],
            ["BMW", "G 310 GS", "Adventure Tourer", 313, 310000],
            ["Royal Enfield", "Himalayan 450", "Adventure Tourer", 452, 300000],
            ["Kawasaki", "Versys-X 300", "Adventure Tourer", 296, 340000],
            ["TVS", "Apache RTX", "Adventure Tourer", 299.1, 230000],

            # TOURING - 200cc to 600cc
            ["Bajaj", "Dominar 250", "Touring", 248.77, 185000],
            ["Bajaj", "Dominar 400", "Touring", 373.3, 230000],
            ["Royal Enfield", "Super Meteor 650", "Touring", 648, 370000],
            ["Kawasaki", "Ninja 500", "Touring", 451, 600000],
            ["Honda", "NX500", "Touring", 471, 600000],
            ["Royal Enfield", "Himalayan 450", "Touring", 452, 300000],

            # CAFE RACER - 250cc to 500cc
            ["Royal Enfield", "Continental GT 650", "Cafe Racer", 648, 350000],
            ["Triumph", "Speed 400", "Cafe Racer", 398, 240000],
            ["Jawa", "42", "Cafe Racer", 294.72, 180000],
            ["Jawa", "42 Bobber", "Cafe Racer", 334, 200000],
            ["Husqvarna", "Vitpilen 250", "Cafe Racer", 249.07, 220000],

            # SCRAMBLER - 250cc to 500cc
            ["Triumph", "Scrambler 400 X", "Scrambler", 398, 270000],
            ["Triumph", "Scrambler 400 XC", "Scrambler", 398, 290000],
            ["Ducati", "Scrambler Icon", "Scrambler", 803, 1000000],
            ["Royal Enfield", "Scram 440", "Scrambler", 443, 210000],
            ["Husqvarna", "Svartpilen 401", "Scrambler", 399, 300000],

            # DIRT BIKE - 100cc to 300cc
            ["Kawasaki", "KLX 230", "Dirt Bike", 233, 250000],
            ["Kawasaki", "KLX 230R", "Dirt Bike", 233, 300000],
            ["KTM", "250 SX-F", "Dirt Bike", 249.9, 950000],
            ["KTM", "300 EXC", "Dirt Bike", 293, 1100000],

            # SCOOTERS - 100cc to 160cc
            ["Honda", "Activa 6G", "Scooter", 109.51, 80000],
            ["Honda", "Dio", "Scooter", 109.51, 75000],
            ["TVS", "Jupiter 110", "Scooter", 113.3, 80000],
            ["TVS", "Jupiter 125", "Scooter", 124.8, 90000],
            ["TVS", "Ntorq 125", "Scooter", 124.8, 90000],
            ["Suzuki", "Access 125", "Scooter", 124, 85000],
            ["Suzuki", "Burgman Street", "Scooter", 124, 100000],
            ["Yamaha", "Fascino 125", "Scooter", 125, 85000],
            ["Yamaha", "Ray ZR 125", "Scooter", 125, 90000],
            ["Aprilia", "SR 160", "Scooter", 160, 135000],
            ["Vespa", "VXL 150", "Scooter", 149.5, 145000],

            # ELECTRIC MOTORCYCLES
            ["Revolt", "RV400", "Electric Motorcycle", 0, 140000],
            ["Ultraviolette", "F77", "Electric Motorcycle", 0, 300000],
            ["Oben Electric", "Rorr", "Electric Motorcycle", 0, 150000],

            # ELECTRIC SCOOTERS
            ["Ather", "450X", "Electric Scooter", 0, 150000],
            ["Ather", "Rizta", "Electric Scooter", 0, 120000],
            ["Ola Electric", "S1 Pro", "Electric Scooter", 0, 130000],
            ["TVS", "iQube", "Electric Scooter", 0, 110000],
            ["Bajaj", "Chetak", "Electric Scooter", 0, 120000],
            ["Vida", "V2", "Electric Scooter", 0, 110000]
        ]


        # Expanded catalogue coverage: additional Indian-market motorcycle models.
        # Prices are benchmark placeholders for the academic prototype, not live quotes.
        competitor_data.extend([['Hero', 'HF 100', 'Commuter', 97.2, 60000], ['Hero', 'Passion Plus', 'Commuter', 97.2, 82000], ['Hero', 'Splendor Plus XTEC', 'Commuter', 97.2, 85000], ['Hero', 'Splendor Plus XTEC 2.0', 'Commuter', 97.2, 87000], ['Hero', 'Super Splendor XTEC', 'Commuter', 124.7, 90000], ['Hero', 'Glamour X 125', 'Commuter', 124.7, 90000], ['Hero', 'Xtreme 125R', 'Commuter', 124.7, 100000], ['Honda', 'Shine 100 DX', 'Commuter', 98.98, 72000], ['Bajaj', 'Platina 100', 'Commuter', 102, 72000], ['Bajaj', 'Platina 110', 'Commuter', 115.45, 78000], ['Bajaj', 'CT 110X', 'Commuter', 115.45, 78000], ['Bajaj', 'Pulsar N125', 'Commuter', 124.58, 95000], ['TVS', 'Radeon', 'Commuter', 109.7, 78000], ['TVS', 'Star City Plus', 'Commuter', 109.7, 75000], ['TVS', 'XL100 Heavy Duty', 'Moped', 99.7, 60000], ['Yamaha', 'FZ Rave', 'Street Naked', 149, 125000], ['Yamaha', 'FZ-S FI V4', 'Street Naked', 149, 130000], ['Yamaha', 'XSR 155', 'Street Naked', 155, 155000], ['Yamaha', 'MT-03', 'Street Naked', 321, 330000], ['Honda', 'NX200', 'Street Naked', 184.4, 160000], ['Bajaj', 'Pulsar N160', 'Street Naked', 164.82, 125000], ['Bajaj', 'Pulsar N250', 'Street Naked', 249.07, 150000], ['Bajaj', 'Pulsar 180', 'Street Naked', 178.6, 125000], ['Bajaj', 'Pulsar 220F', 'Street Naked', 220, 140000], ['KTM', '160 Duke', 'Street Naked', 164.2, 185000], ['KTM', '200 Duke', 'Street Naked', 199.5, 200000], ['KTM', '250 Duke', 'Street Naked', 249.07, 220000], ['KTM', '390 Duke', 'Street Naked', 399, 285000], ['Triumph', 'Speed T4', 'Street Naked', 398, 210000], ['Triumph', 'Tracker 400', 'Street Naked', 398, 250000], ['Triumph', 'Thruxton 400', 'Cafe Racer', 398, 275000], ['TVS', 'Apache RTR 160 4V', 'Street Naked', 159.7, 135000], ['TVS', 'Apache RTR 200 4V', 'Street Naked', 197.75, 155000], ['TVS', 'Apache RTR 310', 'Street Naked', 312.12, 250000], ['TVS', 'Apache RTX 300', 'Adventure Tourer', 299, 220000], ['Bajaj', 'Pulsar NS400Z', 'Street Naked', 373.27, 190000], ['Bajaj', 'Dominar 400', 'Touring', 373.3, 230000], ['Suzuki', 'Gixxer 250', 'Street Naked', 249, 185000], ['Yamaha', 'R15S', 'Sports Bike', 155, 165000], ['Yamaha', 'R15 V4', 'Sports Bike', 155, 180000], ['Yamaha', 'R15M', 'Sports Bike', 155, 195000], ['Yamaha', 'R3', 'Sports Bike', 321, 340000], ['Suzuki', 'Gixxer SF 250', 'Sports Bike', 249, 195000], ['KTM', 'RC 160', 'Sports Bike', 164.2, 200000], ['KTM', 'RC 200', 'Sports Bike', 199.5, 230000], ['KTM', 'RC 390', 'Sports Bike', 399, 335000], ['TVS', 'Apache RR 310', 'Sports Bike', 312.12, 280000], ['BMW', 'G 310 RR', 'Sports Bike', 312.12, 300000], ['Aprilia', 'RS 457', 'Sports Bike', 457, 430000], ['Kawasaki', 'Ninja 300', 'Sports Bike', 296, 340000], ['Kawasaki', 'Ninja 500', 'Sports Bike', 451, 580000], ['Kawasaki', 'Versys-X 300', 'Adventure Tourer', 296, 350000], ['Royal Enfield', 'Hunter 350', 'Roadster', 349, 150000], ['Royal Enfield', 'Classic 350', 'Cruiser', 349, 200000], ['Royal Enfield', 'Bullet 350', 'Cruiser', 349, 180000], ['Royal Enfield', 'Meteor 350', 'Cruiser', 349, 210000], ['Royal Enfield', 'Goan Classic 350', 'Cruiser', 349, 220000], ['Royal Enfield', 'Guerrilla 450', 'Roadster', 452, 260000], ['Royal Enfield', 'Scram 440', 'Scrambler', 443, 230000], ['Royal Enfield', 'Himalayan 450', 'Adventure Tourer', 452, 320000], ['Honda', 'CB350', 'Cruiser', 348.36, 205000], ['Honda', "H'ness CB350", 'Cruiser', 348.36, 215000], ['Honda', 'CB350RS', 'Scrambler', 348.36, 220000], ['Honda', 'CB350C', 'Cruiser', 348.36, 210000], ['Jawa', '42', 'Roadster', 294.72, 190000], ['Jawa', '42 FJ', 'Roadster', 334, 210000], ['Jawa', '42 Bobber', 'Cruiser', 334, 215000], ['Jawa', 'Perak', 'Cruiser', 334, 225000], ['Jawa', '350', 'Cruiser', 334, 215000], ['Yezdi', 'Roadster', 'Roadster', 334, 205000], ['Yezdi', 'Scrambler', 'Scrambler', 334, 210000], ['Yezdi', 'Adventure', 'Adventure Tourer', 334, 225000], ['Harley-Davidson', 'X440', 'Roadster', 440, 250000], ['Harley-Davidson', 'X440 T', 'Roadster', 440, 290000], ['Hero', 'Mavrick 440', 'Roadster', 440, 220000], ['Triumph', 'Speed 400', 'Roadster', 398, 240000], ['Triumph', 'Scrambler 400 X', 'Scrambler', 398, 270000], ['Triumph', 'Scrambler 400 XC', 'Scrambler', 398, 290000], ['Husqvarna', 'Svartpilen 401', 'Street Naked', 399, 300000], ['QJ Motor', 'SRV 300', 'Cruiser', 296, 330000], ['QJ Motor', 'SRC 500', 'Cruiser', 480, 230000], ['QJ Motor', 'SRK 400', 'Street Naked', 400, 390000], ['Zontes', '350R', 'Street Naked', 348, 260000], ['Zontes', '350X', 'Adventure Tourer', 348, 235000], ['Zontes', '350T', 'Adventure Tourer', 348, 275000], ['Zontes', 'GK350', 'Street Naked', 348, 325000], ['Aprilia', 'Tuono 457', 'Street Naked', 457, 400000], ['BMW', 'F 450 GS', 'Adventure Tourer', 450, 500000], ['Brixton', 'Crossfire 500', 'Scrambler', 486, 500000], ['Benelli', 'TRK 502', 'Adventure Tourer', 500, 680000], ['Benelli', 'Leoncino 500', 'Scrambler', 500, 560000], ['Benelli', '502C', 'Cruiser', 500, 590000], ['Honda', 'NX500', 'Adventure Tourer', 471, 750000], ['Honda', 'Rebel 500', 'Cruiser', 471, 550000], ['Kawasaki', 'KLX 230', 'Dirt Bike', 233, 220000], ['Kawasaki', 'KLX 230R', 'Dirt Bike', 233, 300000], ['KTM', '390 Adventure', 'Adventure Tourer', 399, 300000], ['KTM', '390 Adventure R', 'Adventure Tourer', 399, 390000], ['KTM', '390 Enduro R', 'Dirt Bike', 399, 340000], ['Suzuki', 'V-Strom SX', 'Adventure Tourer', 249, 205000], ['BMW', 'G 310 GS', 'Adventure Tourer', 313, 320000], ['Hero', 'Xpulse 200 4V', 'Adventure Tourer', 199.6, 160000], ['Hero', 'Xpulse 210', 'Adventure Tourer', 210, 175000]])

        columns = [
            "Company", "Model", "Category", "Engine CC", "Price (₹)"
        ]

        competitor_df = pd.DataFrame(
            competitor_data,
            columns=columns
        )

        # Remove duplicate model rows and keep only combustion motorcycles
        # with a known engine capacity from 1cc through 600cc.
        competitor_df = competitor_df.drop_duplicates(
            subset=["Company", "Model"], keep="last"
        )

        excluded_types = {
            "Scooter", "Electric Scooter", "Electric Motorcycle", "Moped"
        }
        motorcycle_df = competitor_df[
            (competitor_df["Engine CC"] > 0) &
            (competitor_df["Engine CC"] <= 600) &
            (~competitor_df["Category"].isin(excluded_types))
        ].copy()

        motorcycle_df["Engine CC"] = pd.to_numeric(
            motorcycle_df["Engine CC"], errors="coerce"
        )
        motorcycle_df["Price (₹)"] = pd.to_numeric(
            motorcycle_df["Price (₹)"], errors="coerce"
        )
        motorcycle_df = motorcycle_df.dropna(
            subset=["Engine CC", "Price (₹)"]
        )

        st.subheader("1. Indian Motorcycle Market Database")

        db_col1, db_col2, db_col3 = st.columns(3)
        db_col1.metric("Motorcycle models listed", len(motorcycle_df))
        db_col2.metric("Brands covered", motorcycle_df["Company"].nunique())
        db_col3.metric("Engine-capacity ceiling", "600cc")

        with st.expander("Browse the full motorcycle database (up to 600cc)", expanded=False):
            st.caption(
                "This is a curated research catalogue of motorcycle model names and "
                "engine capacities. Model availability can change by city and date; "
                "check the linked manufacturer/dealer listing before making a purchase decision."
            )
            db_search = st.text_input(
                "Find a brand or model in the database",
                placeholder="Example: KTM, Himalayan, Ninja..."
            )
            db_view = motorcycle_df.copy()
            if db_search.strip():
                db_view = db_view[
                    db_view["Company"].str.contains(db_search, case=False, na=False) |
                    db_view["Model"].str.contains(db_search, case=False, na=False)
                ]
            db_view = db_view.sort_values(
                ["Engine CC", "Company", "Model"]
            ).reset_index(drop=True)
            st.dataframe(
                db_view,
                use_container_width=True,
                hide_index=True
            )
            st.caption(
                "Research references: "
                "[BikeCentral – 300–500cc catalogue](https://www.bikecentral.in/300-500cc-bikes) · "
                "[BikeDekho – under-500cc listings](https://www.bikedekho.com/find-250cc-500cc-bikes) · "
                "[SuperBikeWale – 350–500cc motorcycles](https://superbikewale.com/bikes/350-500cc) · "
                "[BikeCentral – latest bikes](https://www.bikecentral.in/latest-bikes)"
            )

        st.divider()
        st.subheader("2. Intelligent Competitor Matching")

        if selected_cc > 0:
            # Adaptive window: wider for larger engines, tighter for commuter bikes.
            tolerance = max(50, int(selected_cc * 0.25))
            lower_cc = max(1, selected_cc - tolerance)
            upper_cc = min(600, selected_cc + tolerance)

            st.write(
                f"Your bike: **{selected_cc}cc**. The system is checking "
                f"motorcycles from **{lower_cc}cc to {upper_cc}cc**, "
                "without restricting the search to one body-style category."
            )

            candidate_df = motorcycle_df[
                (motorcycle_df["Engine CC"] >= lower_cc) &
                (motorcycle_df["Engine CC"] <= upper_cc)
            ].copy()

            if candidate_df.empty:
                candidate_df = motorcycle_df.copy()
                st.warning(
                    "No models were found inside the preferred CC window. "
                    "Showing the closest available motorcycles below 600cc instead."
                )

            candidate_df["CC Difference"] = (
                candidate_df["Engine CC"] - selected_cc
            ).abs()

            # Category is a relevance signal, not a hard filter.
            category_aliases = {
                "Street": {"Street Naked", "Roadster"},
                "Street Naked": {"Street Naked", "Roadster"},
                "Sports": {"Sports Bike"},
                "Sport": {"Sports Bike"},
                "Cruiser": {"Cruiser"},
                "Commuter": {"Commuter"},
                "Adventure": {"Adventure Tourer"},
                "Adventure Tourer": {"Adventure Tourer"},
                "Touring": {"Touring", "Adventure Tourer"},
                "Cafe Racer": {"Cafe Racer", "Roadster"},
                "Scrambler": {"Scrambler"},
                "Dirt Bike": {"Dirt Bike"},
            }
            preferred_categories = category_aliases.get(
                str(category), {str(category)}
            )
            candidate_df["Segment Match"] = candidate_df["Category"].isin(
                preferred_categories
            ).map({True: "Same / similar segment", False: "Other segment"})
            candidate_df["Segment Priority"] = (
                candidate_df["Category"].isin(preferred_categories)
            ).astype(int)

            candidate_df = candidate_df.sort_values(
                ["Segment Priority", "CC Difference", "Price (₹)"],
                ascending=[False, True, True]
            )

            # Keep a useful shortlist for pricing calculations while the full
            # database remains available in the expander above.
            similar_df = candidate_df.head(20).copy()
            similar_df = similar_df.drop(
                columns=["Segment Priority"], errors="ignore"
            )

            st.success(
                f"Found **{len(candidate_df)}** motorcycles in the comparison pool. "
                f"Showing the {len(similar_df)} closest matches, prioritising "
                "similar riding segments and engine capacity."
            )

            st.dataframe(
                similar_df[
                    ["Company", "Model", "Category", "Engine CC",
                     "CC Difference", "Segment Match", "Price (₹)"]
                ],
                use_container_width=True,
                hide_index=True
            )

        else:
            st.warning(
                "The selected vehicle has no petrol engine capacity. "
                "Use the electric-vehicle comparison pathway for electric models."
            )
            similar_df = pd.DataFrame()

        if not similar_df.empty:

            st.subheader("3. Proposed Launch Price")

            average_price = similar_df["Price (₹)"].mean()
            # Share the benchmark with Pricing Recommendation so it is entered once.
            st.session_state["competitor_average_price"] = float(average_price)
            st.session_state["competitor_lowest_price"] = float(similar_df["Price (₹)"].min())
            st.session_state["competitor_highest_price"] = float(similar_df["Price (₹)"].max())
            st.session_state["competitor_match_count"] = int(len(similar_df))

            default_price = (
                int(manufacturing_cost * 1.25)
                if manufacturing_cost > 0
                else int(average_price)
            )

            default_price = max(10000, min(default_price, 5000000))

            proposed_price = st.number_input(
                "Enter your proposed vehicle launch price (₹)",
                min_value=10000,
                max_value=5000000,
                value=default_price,
                step=5000,
                key="competitor_proposed_price",
                help="Enter this once here. The same proposed price will be carried to Pricing Recommendation and Scenario Simulator."
            )
            st.session_state["manager_proposed_price"] = int(proposed_price)

            st.divider()

            st.subheader("4. Market Price Analysis")

            lowest_price = similar_df["Price (₹)"].min()
            highest_price = similar_df["Price (₹)"].max()

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Competitor Average",
                f"₹{average_price:,.0f}"
            )

            col2.metric(
                "Lowest Price",
                f"₹{lowest_price:,.0f}"
            )

            col3.metric(
                "Highest Price",
                f"₹{highest_price:,.0f}"
            )

            difference = proposed_price - average_price
            percentage = (difference / average_price) * 100

            st.write("### Your Price Position")

            if percentage < -10:
                position = "Budget"
                st.success(
                    f"Budget Position: Your proposed price is "
                    f"{abs(percentage):.1f}% below the competitor average."
                )

            elif percentage <= 10:
                position = "Competitive"
                st.success(
                    "Competitive Position: Your proposed price is "
                    "within 10% of the competitor average."
                )

            else:
                position = "Premium"
                st.warning(
                    f"Premium Position: Your proposed price is "
                    f"{percentage:.1f}% above the competitor average."
                )

            col1, col2 = st.columns(2)

            col1.metric(
                "Proposed Launch Price",
                f"₹{proposed_price:,.0f}"
            )

            col2.metric(
                "Difference from Market Average",
                f"₹{difference:,.0f}",
                f"{percentage:.1f}%"
            )

            st.divider()

            # PRICE COMPARISON CHART
            st.subheader("5. Price Positioning Chart")

            chart_df = similar_df.head(12)[
                ["Model", "Price (₹)"]
            ].copy()

            proposed_row = pd.DataFrame({
                "Model": ["Your Proposed Price"],
                "Price (₹)": [proposed_price]
            })

            chart_df = pd.concat(
                [chart_df, proposed_row],
                ignore_index=True
            )

            st.bar_chart(
                chart_df.set_index("Model")
            )

            st.divider()

            st.subheader("6. Competitor Comparison Table")

            st.dataframe(
                similar_df,
                use_container_width=True,
                hide_index=True
            )

            st.info(
                f"Market positioning result: {position}. "
                "Use customer preferences and manufacturing costs "
                "before finalising the launch price."
            )

        st.caption(
            "Academic prototype: model names and engine capacities are a curated "
            "research catalogue based on Indian two-wheeler listings. The price "
            "figures in this comparison are illustrative benchmark estimates, not "
            "live verified ex-showroom prices. Confirm current availability, exact "
            "variant specifications and prices with the manufacturer before use."
        )
# 13. CUSTOMER INSIGHTS
# -----------------------------------------

elif page == "Customer Insights":

    st.header("Customer Insights & Market Research")
    st.caption(
        "Explore the Indian two-wheeler market through vehicle "
        "categories, engine capacities and customer research."
    )

    st.info(
        "Research dashboard: Vehicle inventory is being organised. "
        "Customer ratings and review statistics will be added "
        "only after source verification."
    )

    # VEHICLE MASTER DATABASE
    vehicle_data = [
        ["Hero", "Splendor Plus", "Motorcycle", "Commuter", "Petrol", 97.2],
        ["Hero", "HF Deluxe", "Motorcycle", "Commuter", "Petrol", 97.2],
        ["Honda", "Shine 100", "Motorcycle", "Commuter", "Petrol", 98.98],
        ["Bajaj", "Platina 100", "Motorcycle", "Commuter", "Petrol", 102],
        ["TVS", "Sport", "Motorcycle", "Commuter", "Petrol", 109.7],
        ["TVS", "Radeon", "Motorcycle", "Commuter", "Petrol", 109.7],
        ["TVS", "Raider 125", "Motorcycle", "Street", "Petrol", 124.8],
        ["Honda", "SP 125", "Motorcycle", "Commuter", "Petrol", 123.94],
        ["Hero", "Xtreme 125R", "Motorcycle", "Street", "Petrol", 124.7],
        ["Bajaj", "Pulsar 125", "Motorcycle", "Street", "Petrol", 124.4],
        ["Bajaj", "Pulsar NS125", "Motorcycle", "Street", "Petrol", 124.45],
        ["Honda", "Shine 125", "Motorcycle", "Commuter", "Petrol", 123.94],
        ["Yamaha", "FZ-S", "Motorcycle", "Street Naked", "Petrol", 149],
        ["Bajaj", "Pulsar 150", "Motorcycle", "Street", "Petrol", 149.5],
        ["Yamaha", "MT-15", "Motorcycle", "Street Naked", "Petrol", 155],
        ["Yamaha", "R15 V4", "Motorcycle", "Sports", "Petrol", 155],
        ["TVS", "Apache RTR 160 4V", "Motorcycle", "Sports", "Petrol", 159.7],
        ["Honda", "Unicorn", "Motorcycle", "Commuter", "Petrol", 162.7],
        ["Bajaj", "Pulsar N160", "Motorcycle", "Street", "Petrol", 164.8],
        ["TVS", "Apache RTR 200 4V", "Motorcycle", "Sports", "Petrol", 197.75],
        ["Hero", "Xpulse 200 4V", "Motorcycle", "Adventure", "Petrol", 199.6],
        ["Bajaj", "Pulsar NS200", "Motorcycle", "Sports", "Petrol", 199.5],
        ["TVS", "Ronin", "Motorcycle", "Cruiser", "Petrol", 225.9],
        ["Bajaj", "Avenger 220", "Motorcycle", "Cruiser", "Petrol", 220],
        ["KTM", "Duke 250", "Motorcycle", "Street Naked", "Petrol", 249],
        ["Suzuki", "Gixxer 250", "Motorcycle", "Sports", "Petrol", 249],
        ["Bajaj", "Pulsar N250", "Motorcycle", "Street", "Petrol", 249],
        ["Hero", "Xpulse 210", "Motorcycle", "Adventure", "Petrol", 210],
        ["Royal Enfield", "Classic 350", "Motorcycle", "Cruiser", "Petrol", 349],
        ["Royal Enfield", "Hunter 350", "Motorcycle", "Roadster", "Petrol", 349],
        ["Royal Enfield", "Meteor 350", "Motorcycle", "Cruiser", "Petrol", 349],
        ["TVS", "Apache RTX", "Motorcycle", "Adventure", "Petrol", 299],
        ["Triumph", "Speed 400", "Motorcycle", "Roadster", "Petrol", 398],
        ["Hero", "Mavrick 440", "Motorcycle", "Roadster", "Petrol", 440],
        ["Harley-Davidson", "X440", "Motorcycle", "Roadster", "Petrol", 440],
        ["Royal Enfield", "Himalayan 450", "Motorcycle", "Adventure", "Petrol", 452],

        ["Honda", "Activa", "Scooter", "Commuter", "Petrol", 109.5],
        ["Honda", "Dio", "Scooter", "Sporty", "Petrol", 109.5],
        ["Suzuki", "Access 125", "Scooter", "Commuter", "Petrol", 124],
        ["TVS", "Jupiter 125", "Scooter", "Commuter", "Petrol", 124.8],
        ["TVS", "Ntorq 125", "Scooter", "Sporty", "Petrol", 124.8],
        ["Hero", "Xoom 125", "Scooter", "Sporty", "Petrol", 124.6],
        ["Hero", "Xoom 160", "Scooter", "Premium", "Petrol", 156],
        ["TVS", "XL100", "Moped", "Utility", "Petrol", 99.7],

        ["TVS", "iQube", "Scooter", "Electric", "Electric", None],
        ["TVS", "Orbiter", "Scooter", "Electric", "Electric", None],
        ["Bajaj", "Chetak", "Scooter", "Electric", "Electric", None],
        ["Ather", "Rizta", "Scooter", "Electric", "Electric", None],
        ["Ather", "450X", "Scooter", "Electric", "Electric", None],
        ["Hero VIDA", "V2", "Scooter", "Electric", "Electric", None],
        ["Honda", "Activa e:", "Scooter", "Electric", "Electric", None],
        ["Ola Electric", "S1 Pro", "Scooter", "Electric", "Electric", None],
    ]

    columns = [
        "Brand", "Model", "Vehicle Type", "Category",
        "Fuel Type", "Engine CC"
    ]

    df = pd.DataFrame(vehicle_data, columns=columns)

    # FILTERS
    st.subheader("Explore the Two-Wheeler Market")

    col1, col2, col3 = st.columns(3)

    with col1:
        selected_type = st.selectbox(
            "Vehicle Type",
            ["All"] + sorted(df["Vehicle Type"].unique().tolist())
        )

    with col2:
        selected_fuel = st.selectbox(
            "Fuel Type",
            ["All"] + sorted(df["Fuel Type"].unique().tolist())
        )

    with col3:
        selected_brand = st.selectbox(
            "Brand",
            ["All"] + sorted(df["Brand"].unique().tolist())
        )

    filtered_df = df.copy()

    if selected_type != "All":
        filtered_df = filtered_df[
            filtered_df["Vehicle Type"] == selected_type
        ]

    if selected_fuel != "All":
        filtered_df = filtered_df[
            filtered_df["Fuel Type"] == selected_fuel
        ]

    if selected_brand != "All":
        filtered_df = filtered_df[
            filtered_df["Brand"] == selected_brand
        ]

    # SEARCH
    search_model = st.text_input(
        "Search vehicle model",
        placeholder="Example: Raider, Activa, Hunter..."
    )

    if search_model:
        filtered_df = filtered_df[
            filtered_df["Model"].str.contains(
                search_model, case=False, na=False
            )
        ]

    # SUMMARY METRICS
    st.subheader("Market Overview")

    m1, m2, m3 = st.columns(3)

    m1.metric("Vehicles in database", len(filtered_df))

    m2.metric(
        "Brands represented",
        filtered_df["Brand"].nunique()
    )

    m3.metric(
        "Vehicle categories",
        filtered_df["Vehicle Type"].nunique()
    )

    # VEHICLE DATABASE
    st.subheader("Vehicle Research Database")

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )

    # CATEGORY ANALYSIS
    st.subheader("Vehicle Category Distribution")

    category_counts = (
        filtered_df["Vehicle Type"]
        .value_counts()
        .rename_axis("Vehicle Type")
        .reset_index(name="Number of Models")
    )

    st.bar_chart(
        category_counts,
        x="Vehicle Type",
        y="Number of Models"
    )

    # ENGINE CAPACITY ANALYSIS
    petrol_df = filtered_df[
        filtered_df["Engine CC"].notna()
    ]

    if not petrol_df.empty:
        st.subheader("Engine Capacity Comparison")

        engine_chart = petrol_df[
            ["Model", "Engine CC"]
        ].set_index("Model")

        st.bar_chart(engine_chart)

    # CUSTOMER RESEARCH SECTION
    st.subheader("Customer Review Research")

    st.warning(
        "Customer ratings, review counts and feature scores "
        "are not yet populated. They will be added from verified "
        "public review sources in the next development stage."
    )

    st.write(
        "Research factors planned for analysis:"
    )

    st.write(
        "- Design and appearance\n"
        "- Performance\n"
        "- Mileage or electric range\n"
        "- Comfort and handling\n"
        "- Features and technology\n"
        "- Value for money"
    )

    st.caption(
        "Note: This is an initial working vehicle inventory. "
        "Model availability and specifications must be verified "
        "against current manufacturer sources before final submission."
    )


# -----------------------------------------
# 14. PRICING RECOMMENDATION
# -----------------------------------------


elif page == "Pricing Recommendation":

        st.header("Pricing Recommendation")
        st.caption(
            "Marketing PriceWise | Data-driven launch pricing for two-wheelers"
        )

        st.markdown(
            "Enter the proposed vehicle's cost, competitor benchmark and "
            "customer willingness to pay to calculate a recommended launch price."
        )

        saved_vehicle = st.session_state.get("vehicle_data", {})
        if not saved_vehicle:
            st.warning("Please complete and save New Vehicle Details first.")

        vehicle_name = (
            f"{saved_vehicle.get('Company', '')} {saved_vehicle.get('Model', '')}".strip()
            or "Proposed Two-Wheeler"
        )
        manufacturing_cost = int(saved_vehicle.get("Manufacturing Cost", 50000))

        st.subheader("1. Vehicle and Cost Information")
        st.info(
            f"Vehicle: **{vehicle_name}**  |  "
            f"Manufacturing cost: **₹{manufacturing_cost:,.0f}** "
            f"(linked from New Vehicle Details)"
        )

        col1, col2 = st.columns(2)

        with col1:
            desired_margin = st.slider(
                "Desired Profit Margin (%)",
                min_value=5,
                max_value=50,
                value=20
            )

        competitor_price = float(st.session_state.get("competitor_average_price", 0))
        proposed_launch_price = int(st.session_state.get(
            "manager_proposed_price",
            st.session_state.get("competitor_proposed_price", 0)
        ))

        with col2:
            if competitor_price > 0:
                st.metric(
                    "Average Competitor Ex-showroom Price",
                    f"₹{competitor_price:,.0f}",
                    help="Automatically carried over from Competitor Analysis."
                )
            else:
                st.warning("Complete Competitor Analysis first. The competitor average will appear here automatically.")

            if proposed_launch_price > 0:
                st.metric(
                    "Your Proposed Launch Price",
                    f"₹{proposed_launch_price:,.0f}",
                    help="This is your input, not the model's recommendation. It will not be overwritten."
                )
            else:
                st.warning("Enter your proposed launch price once in Competitor Analysis.")

            willingness_to_pay = st.number_input(
                "Estimated Customer Willingness to Pay (₹)",
                min_value=10000,
                max_value=1000000,
                value=90000,
                step=1000
            )

            positioning = st.selectbox(
                "Brand Positioning",
                ["Budget", "Value for Money", "Premium"]
            )

        st.divider()

        st.subheader("2. Pricing Strategy")

        st.write(
            "Choose how the company wants to position its new vehicle "
            "against competitors."
        )

        strategy = st.selectbox(
            "Select Pricing Strategy",
            [
                "Balanced Market Pricing",
                "Penetration Pricing",
                "Premium Pricing"
            ]
        )

        if strategy == "Balanced Market Pricing":
            cost_weight = 0.25
            competitor_weight = 0.35
            customer_weight = 0.40
            adjustment = 1.00

        elif strategy == "Penetration Pricing":
            cost_weight = 0.25
            competitor_weight = 0.50
            customer_weight = 0.25
            adjustment = 0.95

        else:
            cost_weight = 0.25
            competitor_weight = 0.25
            customer_weight = 0.50
            adjustment = 1.05

        st.caption(
            f"Strategy weights — Cost: {cost_weight:.0%}, "
            f"Competitor: {competitor_weight:.0%}, "
            f"Customer: {customer_weight:.0%}"
        )

        if st.button("Calculate Pricing Recommendation", type="primary"):

            if competitor_price <= 0 or proposed_launch_price <= 0:
                st.error("Please complete Competitor Analysis and enter the proposed launch price before calculating the recommendation.")
            else:
                cost_based_price = manufacturing_cost / (
                    1 - desired_margin / 100
                )

                market_based_price = competitor_price
                customer_based_price = willingness_to_pay

                weighted_price = (
                    cost_based_price * cost_weight
                    + market_based_price * competitor_weight
                    + customer_based_price * customer_weight
                )

                adjusted_price = weighted_price * adjustment

                recommended_price = max(
                    cost_based_price,
                    adjusted_price
                )

                final_price = round(recommended_price / 500) * 500

                expected_profit = final_price - manufacturing_cost

                actual_margin = (
                    expected_profit / final_price
                ) * 100

                st.session_state["pricing_result"] = {
                    "vehicle": vehicle_name or "Proposed Two-Wheeler",
                    "cost": manufacturing_cost,
                    "cost_price": cost_based_price,
                    "competitor_price": competitor_price,
                    "customer_price": willingness_to_pay,
                    "proposed_price": proposed_launch_price,
                    "recommended_price": final_price,
                    "profit": expected_profit,
                    "margin": actual_margin,
                    "strategy": strategy
                }

        if "pricing_result" in st.session_state:

            result = st.session_state["pricing_result"]

            st.divider()
            st.subheader("3. Pricing Recommendation")

            st.success(
                f"Model-Suggested Launch Price for {result['vehicle']}: "
                f"₹{result['recommended_price']:,.0f}"
            )
            st.info(
                f"Your proposed launch price remains ₹{result['proposed_price']:,.0f}. "
                "The recommendation is a separate benchmark for comparison; your input has not been changed."
            )

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Cost-Based Price",
                f"₹{result['cost_price']:,.0f}"
            )

            col2.metric(
                "Expected Profit per Vehicle",
                f"₹{result['profit']:,.0f}"
            )

            col3.metric(
                "Estimated Profit Margin",
                f"{result['margin']:.1f}%"
            )

            st.subheader("4. Pricing Comparison")

            comparison_data = pd.DataFrame({
                "Pricing Method": [
                    "Cost-Based Price",
                    "Competitor-Based Price",
                    "Customer-Based Price",
                    "Manager's Proposed Launch Price",
                    "Model-Recommended Launch Price"
                ],
                "Price (₹)": [
                    result["cost_price"],
                    result["competitor_price"],
                    result["customer_price"],
                    result["proposed_price"],
                    result["recommended_price"]
                ]
            })

            st.dataframe(
                comparison_data,
                hide_index=True,
                width="stretch"
            )

            st.bar_chart(
                comparison_data.set_index("Pricing Method")
            )

            st.subheader("5. Managerial Interpretation")

            st.write(
                f"""
                - **Cost consideration:** The estimated cost-based price is
                  ₹{result['cost_price']:,.0f}.
                - **Competitive position:** The competitor benchmark is
                  ₹{result['competitor_price']:,.0f}.
                - **Customer affordability:** Estimated willingness to pay is
                  ₹{result['customer_price']:,.0f}.
                - **Recommended decision:** The suggested launch price is
                  ₹{result['recommended_price']:,.0f}.
                - **Strategy selected:** {result['strategy']}.
                """
            )

            if result["recommended_price"] > result["customer_price"]:
                st.warning(
                    "The recommended price exceeds estimated customer "
                    "willingness to pay. The manager should reconsider "
                    "costs, features or the target segment."
                )

            elif result["recommended_price"] > result["competitor_price"]:
                st.info(
                    "The recommended price is above the competitor benchmark. "
                    "The company should justify the premium through product "
                    "features, performance or brand positioning."
                )

            else:
                st.info(
                    "The recommended price is at or below the competitor "
                    "benchmark. This may support a competitive market entry."
                )

            st.subheader("6. Ten-Factor Pricing Benchmark")
            pricing_factors = [
                ("1. Manufacturing cost and minimum viable price", "Quantitative", f"The saved manufacturing cost is ₹{result['cost']:,.0f}. The cost-based price is used as a minimum price floor to protect the selected target margin."),
                ("2. Competitor average ex-showroom price", "Quantitative", f"The benchmark is ₹{result['competitor_price']:,.0f}, automatically calculated from the competitor set selected in Competitor Analysis."),
                ("3. Customer willingness to pay", "Quantitative input", f"The manager-entered estimate is ₹{result['customer_price']:,.0f}; it represents the upper customer affordability/value signal used in the weighted calculation."),
                ("4. Desired profit margin", "Quantitative input", f"The selected target margin is {desired_margin}%, which determines the cost-based price floor."),
                ("5. Pricing strategy", "Quantitative input", f"{result['strategy']} changes the relative weights assigned to cost, competitors and customer willingness to pay."),
                ("6. Competitive price position", "Managerial check", "Compare the proposed price with the competitor average and range to understand whether the launch is budget, competitive or premium."),
                ("7. Brand positioning", "Managerial check", f"The selected positioning is {positioning}. A premium position needs a credible reason for customers to accept a higher price."),
                ("8. Product features and perceived value", "Managerial check", "Performance, safety, design, technology, comfort, mileage/range and after-sales support should justify the price relative to alternatives."),
                ("9. Demand and price sensitivity", "Managerial check", "A lower price may improve purchase interest, while a higher price may reduce demand. Validate this with the customer questionnaire and scenario results."),
                ("10. Target segment and launch geography", "Managerial check", f"The saved target customer age and state should be considered because affordability, local competition, taxes and customer needs can vary by market."),
            ]
            for factor_title, factor_type, factor_detail in pricing_factors:
                with st.expander(f"{factor_title} — {factor_type}"):
                    st.write(factor_detail)

            st.caption(
                "Model transparency: factors 1–5 are directly represented in the current pricing calculation. "
                "Factors 6–10 are structured managerial validation checks; they are not yet separate numerical inputs in this prototype."
            )

            st.caption(
                "Note: This is an illustrative decision-support model. "
                "It uses user-entered estimates, not verified company costs "
                "or actual customer survey results. Taxes, dealer margins, "
                "distribution costs and demand forecasts are not yet included."
            )


# -----------------------------------------
# 15. SCENARIO SIMULATOR
# -----------------------------------------

elif page == "Scenario Simulator":

        st.header("Pricing Scenario Simulator")
        st.caption("Choose a pricing basis, set your own market benchmarks, and compare four adjustable price-change scenarios.")

        saved_vehicle = st.session_state.get("vehicle_data", {})
        saved_pricing = st.session_state.get("pricing_result", {})
        proposed_price = int(st.session_state.get("manager_proposed_price", st.session_state.get("competitor_proposed_price", 0)) or 0)
        recommended_price = int(saved_pricing.get("recommended_price", 0) or 0)
        unit_cost = int(saved_vehicle.get("Manufacturing Cost", 0) or 0)

        if proposed_price <= 0 and recommended_price <= 0:
            st.warning("Please enter a proposed launch price in Competitor Analysis or calculate a Pricing Recommendation first.")
        else:
            st.subheader("1. Select the price to simulate")
            available_price_options = []
            if recommended_price > 0:
                available_price_options.append("Use model-recommended price")
            if proposed_price > 0:
                available_price_options.append("Use manager-proposed price")

            default_choice = "Use manager-proposed price" if proposed_price > 0 else "Use model-recommended price"
            selected_basis = st.radio(
                "Choose your starting launch price",
                available_price_options,
                index=available_price_options.index(default_choice),
                horizontal=True,
                key="scenario_price_basis"
            )
            base_price = recommended_price if selected_basis == "Use model-recommended price" else proposed_price
            st.metric("Selected starting price", f"₹{base_price:,.0f}")
            if selected_basis == "Use model-recommended price":
                st.caption("Automatically carried from the latest Pricing Recommendation.")
            else:
                st.caption("Automatically carried from your proposed launch price. It remains unchanged in the saved vehicle details.")

            if unit_cost > 0:
                st.info(f"Manufacturing cost per vehicle: **₹{unit_cost:,.0f}** — automatically linked from New Vehicle Details. You do not need to enter it again.")
            else:
                st.warning("Manufacturing cost is not saved in New Vehicle Details. Profit calculations will be unavailable until it is entered there.")

            st.divider()
            st.subheader("2. Set expected monthly sales benchmarks")
            st.caption("Enter your own expected monthly unit sales for the selected state and for India as a whole.")
            state_name = str(saved_vehicle.get("State", "Selected State"))
            state_col, india_col = st.columns(2)
            with state_col:
                state_sales = st.number_input(
                    f"Expected monthly sales — {state_name}", min_value=1, max_value=1000000,
                    value=500, step=50, key="scenario_state_monthly_sales"
                )
            with india_col:
                india_sales = st.number_input(
                    "Expected monthly sales — All India", min_value=1, max_value=10000000,
                    value=10000, step=500, key="scenario_india_monthly_sales"
                )

            st.divider()
            st.subheader("3. Configure four price-change scenarios")
            st.caption("For each scenario, choose whether to raise or reduce the price. Set the price change and expected sales response from 1% to 100%.")
            scenario_specs = [
                ("Scenario 1 — Market penetration", "Decrease"),
                ("Scenario 2 — Small adjustment", "Decrease"),
                ("Scenario 3 — Premium positioning", "Increase"),
                ("Scenario 4 — Aggressive premium", "Increase"),
            ]
            scenario_configs = []
            for idx, (scenario_name, default_direction) in enumerate(scenario_specs, start=1):
                with st.expander(scenario_name, expanded=(idx == 1)):
                    direction = st.selectbox(
                        "Price direction", ["Decrease", "Increase"],
                        index=0 if default_direction == "Decrease" else 1,
                        key=f"scenario_{idx}_direction"
                    )
                    price_change_pct = st.slider(
                        "Price change (%)", min_value=1, max_value=100, value=[10, 5, 10, 20][idx-1],
                        step=1, key=f"scenario_{idx}_price_change"
                    )
                    demand_response_pct = st.slider(
                        "Expected monthly sales response (%)", min_value=1, max_value=100,
                        value=[15, 7, 10, 20][idx-1], step=1,
                        key=f"scenario_{idx}_demand_response",
                        help="Your assumption for how much monthly unit sales may change. This is a manager-set assumption, not a market forecast."
                    )
                    scenario_configs.append({
                        "Scenario": scenario_name.split("—", 1)[1].strip(),
                        "Direction": direction,
                        "Price Change (%)": price_change_pct,
                        "Sales Response (%)": demand_response_pct,
                    })

            rows = []
            for config in scenario_configs:
                sign = -1 if config["Direction"] == "Decrease" else 1
                scenario_price = base_price * (1 + sign * config["Price Change (%)"] / 100)
                demand_sign = 1 if config["Direction"] == "Decrease" else -1
                state_scenario_sales = max(0, round(state_sales * (1 + demand_sign * config["Sales Response (%)"] / 100)))
                india_scenario_sales = max(0, round(india_sales * (1 + demand_sign * config["Sales Response (%)"] / 100)))
                for market_name, sales in [(state_name, state_scenario_sales), ("All India", india_scenario_sales)]:
                    revenue = scenario_price * sales
                    total_cost = unit_cost * sales if unit_cost > 0 else None
                    profit = revenue - total_cost if total_cost is not None else None
                    rows.append({
                        "Scenario": config["Scenario"], "Market": market_name,
                        "Price Direction": config["Direction"],
                        "Price Change (%)": config["Price Change (%)"],
                        "Selling Price (₹)": round(scenario_price),
                        "Expected Monthly Sales": sales,
                        "Monthly Revenue (₹)": round(revenue),
                        "Estimated Monthly Profit (₹)": round(profit) if profit is not None else "Not available"
                    })

            results_df = pd.DataFrame(rows)
            st.session_state["scenario_results"] = results_df.copy()
            st.subheader("4. Side-by-side monthly outcome comparison")
            state_results = results_df[results_df["Market"] == state_name].drop(columns=["Market"]).reset_index(drop=True)
            india_results = results_df[results_df["Market"] == "All India"].drop(columns=["Market"]).reset_index(drop=True)
            left, right = st.columns(2)
            with left:
                st.markdown(f"**{state_name}**")
                st.dataframe(state_results, hide_index=True, use_container_width=True)
            with right:
                st.markdown("**All India**")
                st.dataframe(india_results, hide_index=True, use_container_width=True)

            st.subheader("5. Revenue comparison")
            chart_df = results_df.pivot(index="Scenario", columns="Market", values="Monthly Revenue (₹)")
            st.bar_chart(chart_df)
            st.warning("These results are scenario estimates based on the sales benchmarks and response percentages you set. State and India sales are independent inputs; the app does not extrapolate one into the other. Actual demand may differ.")


# -----------------------------------------
# 16. REPORTS
# -----------------------------------------

elif page == "Reports":

    st.header("Professional Pricing Analysis Report")
    st.caption("Marketing PriceWise | A4 Management Report Generator")

    if "pricing_result" not in st.session_state:
        st.warning(
            "Please calculate a Pricing Recommendation first."
        )

    else:

        report = st.session_state["pricing_result"]
        vehicle = st.session_state.get("vehicle_data", {})

        st.subheader("1. Company and Report Information")

        col1, col2 = st.columns(2)

        with col1:
            company_name = st.text_input(
                "Company Name",
                value=vehicle.get("Company", "Your Company")
            )

            prepared_by = st.text_input(
                "Prepared By",
                placeholder="Enter your name or department"
            )

            report_date = st.date_input(
                "Report Date",
                value=date.today()
            )

        with col2:
            reference_number = st.text_input(
                "Report Reference Number",
                value="MPW-" + date.today().strftime("%Y%m%d")
            )

            target_market = st.text_input(
                "Target Market",
                value="India"
            )

            st.info("Manufacturer logo is selected automatically from the saved vehicle brand.")

        st.divider()

        st.subheader("2. Vehicle Information")

        col1, col2 = st.columns(2)

        with col1:
            report_brand = st.text_input(
                "Vehicle Brand",
                value=vehicle.get("Company", ""),
                key="report_brand_input"
            )

            report_model = st.text_input(
                "Vehicle Model",
                value=vehicle.get(
                    "Model",
                    report.get("vehicle", "")
                ),
                key="report_model_input"
            )

        with col2:
            report_cc = st.text_input(
                "Engine Capacity (CC)",
                value=str(vehicle.get("Engine Capacity", "Not specified"))
            )

            report_category = st.text_input(
                "Vehicle Category",
                value=vehicle.get("Category", "Not specified")
            )

        st.divider()

        st.subheader("3. Report Generation")

        st.info(
            "Your report will contain the executive summary, "
            "pricing comparison, profitability and managerial recommendations."
        )

        if st.button("GENERATE FORMAL A4 REPORT", type="primary"):

            manufacturer_domain = COMPANY_DOMAINS.get(report_brand.strip())
            if manufacturer_domain:
                logo_url = (
                    "https://www.google.com/s2/favicons"
                    f"?domain={manufacturer_domain}&sz=256"
                )
                logo_html = (
                    f'<img src="{logo_url}" alt="{report_brand} logo" '
                    f'class="logo" onerror="this.style.display=\'none\'">'
                )
            else:
                logo_html = (
                    f'<div class="logo-fallback">{report_brand[:2].upper()}</div>'
                )

            report_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
            <meta charset="UTF-8">

            <style>

            @page {{
                size: A4 portrait;
                margin: 15mm;
            }}

            * {{
                box-sizing: border-box;
            }}

            html, body {{
                background: #ffffff !important;
                color: #172033 !important;
                font-family: Arial, sans-serif;
                font-size: 11px;
                line-height: 1.5;
                margin: 0;
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }}

            .page, section, article {{
                background: #ffffff !important;
                color: #172033 !important;
            }}

            p, li, td, .footer, .report-title p {{
                color: #263445 !important;
            }}

            td {{
                background: #ffffff !important;
            }}

            @media print {{
                html, body, .page {{
                    background: #ffffff !important;
                    color: #172033 !important;
                }}
                h2 {{ background: #e8eef5 !important; color: #17365D !important; }}
                th {{ background: #17365D !important; color: #ffffff !important; }}
                td {{ background: #ffffff !important; color: #263445 !important; }}
            }}

            .page {{
                width: 100%;
                max-width: 180mm;
                margin: auto;
            }}

            .header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 3px solid #17365D;
                padding-bottom: 15px;
            }}

            .logo {{
                width: 90px;
                height: 70px;
                object-fit: contain;
            }}

            .logo-fallback {{
                width: 64px;
                height: 64px;
                border-radius: 50%;
                background: #17365D;
                color: white;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 22px;
                font-weight: bold;
            }}

            .company {{
                font-size: 22px;
                font-weight: bold;
                color: #17365D;
                text-align: right;
            }}

            .report-title {{
                text-align: center;
                padding: 20px 0;
            }}

            .report-title h1 {{
                color: #17365D;
                font-size: 23px;
                margin: 0;
            }}

            .report-title p {{
                color: #64748b;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 10px 0 18px;
            }}

            td, th {{
                border: 1px solid #ccd5df;
                padding: 9px;
                text-align: left;
            }}

            th {{
                background: #17365D;
                color: white;
            }}

            h2 {{
                background: #eaf0f6;
                color: #17365D;
                padding: 8px;
                border-left: 4px solid #17365D;
                font-size: 14px;
                margin-top: 22px;
            }}

            .recommendation {{
                text-align: center;
                border: 2px solid #17365D;
                padding: 15px;
                margin: 18px 0;
                background: #f3f6fa;
            }}

            .price {{
                font-size: 27px;
                font-weight: bold;
                color: #17365D;
            }}

            .signatures {{
                display: flex;
                gap: 40px;
                margin-top: 55px;
            }}

            .signature {{
                width: 50%;
                border-top: 1px solid #444;
                padding-top: 8px;
            }}

            .footer {{
                border-top: 1px solid #aaa;
                text-align: center;
                margin-top: 30px;
                padding-top: 10px;
                font-size: 9px;
                color: #64748b;
            }}

            .no-print {{
                text-align: center;
                margin: 25px;
            }}

            button {{
                padding: 12px 25px;
                background: #17365D;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }}

            @media print {{
                .no-print {{
                    display: none;
                }}

                body {{
                    -webkit-print-color-adjust: exact;
                    print-color-adjust: exact;
                }}
            }}

            </style>
            </head>

            <body>

            <div class="page">

            <div class="header">

                <div>
                    {logo_html}
                </div>

                <div class="company">
                    {company_name}
                    <div style="font-size:10px;">
                        Marketing & Pricing Strategy Division
                    </div>
                </div>

            </div>

            <div class="report-title">

                <h1>PRICING ANALYSIS REPORT</h1>

                <p>New Two-Wheeler Launch Assessment</p>

            </div>

            <table>

                <tr>
                    <td><b>Report Date</b></td>
                    <td>{report_date.strftime("%d %B %Y")}</td>
                </tr>

                <tr>
                    <td><b>Reference Number</b></td>
                    <td>{reference_number}</td>
                </tr>

                <tr>
                    <td><b>Prepared By</b></td>
                    <td>{prepared_by or "Not specified"}</td>
                </tr>

                <tr>
                    <td><b>Target Market</b></td>
                    <td>{target_market}</td>
                </tr>

            </table>

            <h2>1. Executive Summary</h2>

            <p>
                This report evaluates the proposed launch pricing
                of {report_brand} {report_model} in {target_market}.
                The analysis considers manufacturing cost,
                competitor pricing and customer willingness to pay.
            </p>

            <div class="recommendation">

                RECOMMENDED LAUNCH PRICE

                <div class="price">
                    ₹{report['recommended_price']:,.0f}
                </div>

                <b>Strategy: {report['strategy']}</b>

            </div>

            <h2>2. Vehicle Specifications</h2>

            <table>

                <tr>
                    <th>Particulars</th>
                    <th>Details</th>
                </tr>

                <tr>
                    <td>Brand</td>
                    <td>{report_brand}</td>
                </tr>

                <tr>
                    <td>Model</td>
                    <td>{report_model}</td>
                </tr>

                <tr>
                    <td>Engine Capacity</td>
                    <td>{report_cc}</td>
                </tr>

                <tr>
                    <td>Vehicle Category</td>
                    <td>{report_category}</td>
                </tr>

            </table>

            <h2>3. Pricing Analysis</h2>

            <table>

                <tr>
                    <th>Pricing Method</th>
                    <th>Estimated Price</th>
                </tr>

                <tr>
                    <td>Cost-Based Pricing</td>
                    <td>₹{report['cost_price']:,.0f}</td>
                </tr>

                <tr>
                    <td>Competitor-Based Pricing</td>
                    <td>₹{report['competitor_price']:,.0f}</td>
                </tr>

                <tr>
                    <td>Customer-Based Pricing</td>
                    <td>₹{report['customer_price']:,.0f}</td>
                </tr>

                <tr>
                    <td><b>Recommended Price</b></td>
                    <td><b>₹{report['recommended_price']:,.0f}</b></td>
                </tr>

            </table>

            <h2>4. Profitability Analysis</h2>

            <table>

                <tr>
                    <th>Financial Indicator</th>
                    <th>Value</th>
                </tr>

                <tr>
                    <td>Manufacturing Cost</td>
                    <td>₹{report['cost']:,.0f}</td>
                </tr>

                <tr>
                    <td>Expected Profit per Vehicle</td>
                    <td>₹{report['profit']:,.0f}</td>
                </tr>

                <tr>
                    <td>Estimated Profit Margin</td>
                    <td>{report['margin']:.2f}%</td>
                </tr>

            </table>

            <h2>5. Managerial Recommendation</h2>

            <p>
                The selected pricing strategy is
                {report['strategy']}. Management should evaluate
                the recommended launch price against market demand,
                competitor positioning, customer research and
                the company's cost structure before final approval.
            </p>

            <h2>6. Assumptions and Limitations</h2>

            <p>
                This report uses user-entered estimates and
                illustrative assumptions. It does not guarantee
                actual sales or profitability. Taxes, dealer margins,
                distribution expenses and demand forecasts should
                be assessed separately.
            </p>

            <div class="signatures">

                <div class="signature">
                    Prepared By / Signature
                </div>

                <div class="signature">
                    Approved By / Signature
                </div>

            </div>

            <div class="footer">

                {company_name} | Marketing PriceWise

                <br>

                Confidential — For Management Use

            </div>

            </div>

            <div class="no-print">

                <button onclick="window.print()">
                    PRINT / SAVE AS PDF
                </button>

            </div>

            </body>
            </html>
            """

            st.session_state["formal_report_html"] = report_html

            st.success("Your formal report has been generated!")

        if "formal_report_html" in st.session_state:

            st.download_button(
                "DOWNLOAD FORMAL REPORT",
                data=st.session_state["formal_report_html"],
                file_name="Marketing_PriceWise_Formal_Report.html",
                mime="text/html",
                width="stretch"
            )

            st.components.v1.html(
                st.session_state["formal_report_html"],
                height=850,
                scrolling=True
            )

            st.info(
                "To save as PDF: open the downloaded HTML file in Chrome, "
                "click PRINT / SAVE AS PDF, and select A4 paper."
            )