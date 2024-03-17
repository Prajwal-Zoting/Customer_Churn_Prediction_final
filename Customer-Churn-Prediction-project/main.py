import base64
import streamlit as st
import pickle
import pandas as pd
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def load_model(model_path):
    with open(model_path, 'rb') as model_file:
        model = pickle.load(model_file)
    return model
model = load_model('CustomerChurn.pkl')

img = get_img_as_base64("background.png")
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("data:image/png;base64,{img}");
width: 100%;
height:100%
background-repeat: no-repeat;
background-attachment: fixed;
background-size: cover;
}}

[data-testid="stSidebar"] > div:first-child {{
background-image: url("data:image/png;base64,{img}");
background-position: center; 
background-repeat: no-repeat;
background-attachment: fixed;
}}

[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}

[data-testid="stToolbar"] {{
right: 2rem;
}}
</style>
"""

# PreferredPaymentMode = ['--- select ---','Debit Card','UPI','Cash on Delivery','Credit Card','E wallet']
# Gender = ['--- select ---','Male','Female']
# PreferedOrderCat = ['--- select ---','Laptop & Accessory','Mobile Phone','Fashion','Mobile']
# MaritalStatus = ['--- select ---', 'Single', 'Married','Divorced']
# Mapping for string to numerical conversion
# Corrected mapping for PreferredLoginDevice

CityTier = ['--- select ---',1,2,3]
SatisfactionScore = ['--- select ---',1,2,3,4,5]
Complain = ['--- select ---',0,1]
preferred_login_device_mapping = {'--- select ---': None, 'Mobile Phone': 1, 'Computer': 2}
preferred_payment_mode_mapping = {'--- select ---': None, 'Credit Card': 1, 'Debit Card': 2, 'Cash on Delivery': 3, 'UPI': 4, 'E wallet': 5}
gender_mapping = {'--- select ---': None, 'Male': 1, 'Female': 0}
preferred_order_cat_mapping = {'--- select ---': None, 'Fashion': 1, 'Laptop & Accessory': 2, 'Mobile Phone': 3}
marital_status_mapping = {'--- select ---': None, 'Married': 1, 'Single': 2, 'Divorced': 3}

st.markdown(page_bg_img, unsafe_allow_html=True)
st.markdown("""
    # **Customer Churn Prediction**            
""")
col1, col2, col3 = st.columns(3)
with col1:
   tenure = st.number_input('Tenure')
with col2:
    PreferredLoginDevice = st.selectbox('PreferredLoginDevice', ['--- select ---', 'Mobile Phone', 'Computer'])
    PreferredLoginDevice = preferred_login_device_mapping.get(PreferredLoginDevice)
with col3:
   CityTier =  st.selectbox('CityTier', ['--- select ---', 1, 2, 3])

col4, col5, col6 = st.columns(3)
with col4:
    WarehouseToHome = st.number_input('WarehouseToHome')
with col5:
   PreferredPaymentMode =  st.selectbox('PreferredPaymentMode', ['--- select ---', 'Credit Card', 'Debit Card', 'Cash on Delivery', 'UPI', 'E wallet'])
   PreferredPaymentMode = preferred_payment_mode_mapping.get(PreferredPaymentMode)
with col6:
    Gender = st.selectbox('Gender', ['--- select ---', 'Male', 'Female'])
    Gender = gender_mapping.get(Gender)

col7, col8, col9 = st.columns(3)
with col7:
    HourSpendOnApp = st.number_input('HourSpendOnApp')
with col8:
    NumberOfDeviceRegistered = st.number_input('NumberOfDeviceRegistered')
with col9:
   PreferedOrderCat =  st.selectbox('PreferedOrderCat', ['--- select ---', 'Fashion', 'Laptop & Accessory', 'Mobile Phone'])
   PreferedOrderCat = preferred_order_cat_mapping.get(PreferedOrderCat)

col10, col11, col12 = st.columns(3)
with col10:
    SatisfactionScore = st.selectbox('SatisfactionScore', ['--- select ---', 1, 2, 3, 4, 5])
with col11:
   MaritalStatus =  st.selectbox('MaritalStatus', ['--- select ---', 'Married', 'Single', 'Divorced'])
   MaritalStatus = marital_status_mapping.get(MaritalStatus)
with col12:
    NumberOfAddress = st.number_input('NumberOfAddress')

col13, col14, col15 = st.columns(3)
with col13:
   Complain =  st.selectbox('Complain', ['--- select ---', 0, 1])
with col14:
    OrderAmountHikeFromlastYear = st.number_input('OrderAmountHikeFromlastYear')
with col15:
   CouponUsed = st.number_input('CouponUsed')

col16, col17, col18 = st.columns(3)
with col16:
    OrderCount = st.number_input('OrderCount')
with col17:
   DaySinceLastOrder = st.number_input('DaySinceLastOrder')
with col18:
    CashbackAmount = st.number_input('CashbackAmount')

if st.button('Predict Customer Churn'):
    
    # Prepare input data based on user inputs
    input_data = {
        'Tenure': tenure,
        'PreferredLoginDevice': preferred_login_device_mapping.get(PreferredLoginDevice),  # Returns None if '--- select ---' is selected
        'CityTier': CityTier,
        'WarehouseToHome': WarehouseToHome,
        'PreferredPaymentMode': preferred_payment_mode_mapping.get(PreferredPaymentMode),  # Returns None if '--- select ---' is selected
        'Gender': gender_mapping.get(Gender),  # Returns None if '--- select ---' is selected
        'HourSpendOnApp': HourSpendOnApp,
        'NumberOfDeviceRegistered': NumberOfDeviceRegistered,
        'PreferedOrderCat': preferred_order_cat_mapping.get(PreferedOrderCat),  # Returns None if '--- select ---' is selected
        'SatisfactionScore': SatisfactionScore,
        'MaritalStatus': marital_status_mapping.get(MaritalStatus),  # Returns None if '--- select ---' is selected
        'NumberOfAddress': NumberOfAddress,
        'Complain': Complain,
        'OrderAmountHikeFromlastYear': OrderAmountHikeFromlastYear,
        'CouponUsed': CouponUsed,
        'OrderCount': OrderCount,
        'DaySinceLastOrder': DaySinceLastOrder,
        'CashbackAmount': CashbackAmount
    }

    # Convert input data to DataFrame
    input_df = pd.DataFrame(input_data, index=[0])

    # Make prediction
    churn_prediction = model.predict(input_df)

    # Display result
    if churn_prediction[0] == 1:
        st.write("Yes")
    else:
        st.write("No")
