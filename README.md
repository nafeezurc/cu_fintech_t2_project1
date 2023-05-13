### I-invest

I-invest is a python application that recommends to the user a portfolio based upon their risk tolerance.
Out of 11 ETF's stock & bonds sectors with 2 different cryptos I-invest will determine the best portfolio return based on the projected risk return methodology with the use of Monte Carlo simulation.

## Usage

An individual will answers a questioner a series of 8 questions to determine their risk tolerance.
Each question will have a certain weight that will be calculated at the end of the questioner.
The user will be asked for the username with expected time frame and the amount of investment.

The types are users risk tolerance and portfolio weights:
Aggressive: Aggressive risk investors are well versed with the market and take huge risks. 
Weights for aggressive investor would be 40% stocks and 20% bonds and 10% cryptos.
Moderate: Moderate risk investors are relatively less risk-tolerant when compared to aggressive risk investors. 40% Stocks and 60% bonds 
Conservative: Conservative investors take the least risk in the market
The portfolio that is generated will have different weights designed based upon our insight of their risk tolerance. 
Weights: 30% Stocks and 70% bonds

## Data collection & assets allocation

- Data Collection: importing a 5 years closing price for the top performed ETFs in the market.
- Stock & Bonds ETF Asset allocation: with the use of 5 years historical beta to determine the level of risk of each ETF 
- Crypto asset allocation : the optimal crypto in the market.


## Output

- The user will get after submitting the questioner a pie chart with exact weights for his portfolio.
- The final output would be the projected return based on the Monte Carlo simulation.


# Sources

Alpaca - https://github.com/alpacahq/alpaca-py 

# TODO

add the actual on what they want to invest, in the code and in the slides
code efficient frontier
make sure everything is included in the slides
image of answweing questionaries
change location of run function

Things to Add to the readme
- Questionnaire
- Weights for each questions
- Data Collection
- Asset allocation (historical Beta, optimum for the crypto)
- Visualizion charts
- How to use
- Pre-reqs

