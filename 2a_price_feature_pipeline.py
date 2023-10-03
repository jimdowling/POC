import hopsworks
from features.price import generate_today

# Generate price data form today
generated_data_today = generate_today()

# Connect to the Feature Store
project = hopsworks.login()
fs = project.get_feature_store() 

# Retrieve Prices Feature Group
prices_fg = fs.get_or_create_feature_group(
    name='prices',
    version=1,
)
# Insert generated data for today into Prices Feature Group
prices_fg.insert(generated_data_today)