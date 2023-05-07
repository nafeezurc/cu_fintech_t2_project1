import stocks
import sys
import crypto_alpaca
import os
#from dotenv import load_dotenv


# Load the environment variables from the .env file
#by calling the load_dotenv function
#load_dotenv('api.env')
    
# Set the variables for the Alpaca API and secret keys
#alpaca_api_key = os.getenv("ALPACA_API_KEY")
#alpaca_secret_key = os.getenv("ALPACA_SECRET_KEY")

#print(alpaca_api_key,alpaca_secret_key)
risk = "high"
#crypto_df = crypto_alpaca.get_crypto_df()
stocks_df = stocks.get_stocks_df(risk)