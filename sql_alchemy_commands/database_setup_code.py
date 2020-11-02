import pandas as pd
"""
post_data = pd.DataFrame(columns=["user_handle", "description", "price"])
post_data.to_csv("data/product_data.csv", index=False)
"""
user_data = pd.DataFrame(columns=["first_name", "last_name", "user_handle", "email", "password"])
user_data.to_csv("data/user_data.csv", index=False)
