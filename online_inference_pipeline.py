import streamlit as st
import hopsworks
st.header('📈 Online Inference Pipeline')

st.markdown('📡 Connecting to Hopsworks Feature Store...')

project = hopsworks.login()
fs = project.get_feature_store()

st.write("✅ Logged in successfully!")

@st.cache_resource()
def get_deployment():
    st.write("🚀 Retrieving and Starting Deployment...")
    ms = project.get_model_serving()

    # Get deployment
    deployment = ms.get_deployment("priceonlinemodeldeployment")

    # Start deployment
    deployment.start(await_running=180)
    
    st.write("✅ Success!")

    return deployment

deployment = get_deployment()

options = st.multiselect(
    'Select the identifier for which the price forecasting will be performed',
    (0, 1, 2, 3, 4, 5),
    (0))

st.write('You selected the next ID:', options)

preds = [deployment.predict({'instances': [option]}) for option in options]

for option, pred in zip(options, preds):
    st.write(f'🔮 Predicted Price for the {option} ID: {pred}💰')