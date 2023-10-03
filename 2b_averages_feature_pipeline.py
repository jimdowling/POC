from datetime import datetime, timedelta
from features.averages import calculate_second_order_features
import hopsworks

# Connect to the Feature Store
project = hopsworks.login()
fs = project.get_feature_store() 

# Retrieve Averages Feature Group
averages_fg = fs.get_or_create_feature_group(
    name='averages',
    version=1,
)
# Retrieve Prices Feature Group
prices_fg = fs.get_or_create_feature_group(
    name='prices',
    version=1,
)
# Get today's date
today = datetime.today()

# Calculate the date 30 days ago
thirty_days_ago = (today - timedelta(days=31)).strftime("%Y-%m-%d")

# Read price data for 30 days ago
month_price_data = prices_fg.filter(prices_fg.date >= thirty_days_ago).read()

# Calculate second order features
averages_df = calculate_second_order_features(month_price_data)

# Get calculated second order features only for today
averages_today = averages_df[averages_df.date == today.strftime("%Y-%m-%d")]

# Insert second order features for today into Averages Feature Group
averages_fg.insert(averages_today)