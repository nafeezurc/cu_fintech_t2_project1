# importing modules required for customer inputs
import fire
import questionary
from questionary import Validator, ValidationError, prompt
from questionary import Style
import stocks
import crypto_alpaca
import pandas as pd


# Applying style to the input questions
custom_style_fancy = Style([
    ('qmark', 'fg:#00CC99 bold'),       # token in front of the question
    ('question', 'fg:#66CC66 bold'),    # question text
    ('answer', 'fg:#FF9933 bold'),      # submitted answer text behind the question
    ('pointer', 'fg:#673ab7 bold'),     # pointer used in select and checkbox prompts
    ('highlighted', 'fg:#673ab7 bold'), # pointed-at choice in select and checkbox prompts
    ('selected', 'fg:#cc5454'),         # style for a selected item of a checkbox
    ('separator', 'fg:#cc5454'),        # separator in lists
    ('instruction', ''),                # user instructions for select, rawselect, checkbox
    ('text', ''),                       # plain text
    ('disabled', 'fg:#858585 italic')   # disabled choices for select and checkbox prompts
])

# validating the input for investment value
class value_validator(Validator):
    def validate(self, document):
        if len(document.text) == 0:
            raise ValidationError(
                message="Please enter a value",
                cursor_position=len(document.text),
            )
        if document.text.isdecimal() == False:
            raise ValidationError(
                message="Please enter a dollar value value without string characters or decimal points",
                cursor_position=len(document.text),
            )
        if int(document.text) < 5000:
            raise ValidationError(
                message="Please enter a value greater than $5000",
                cursor_position=len(document.text),
            )

# validating the input for investor name
class name_validator(Validator):
    def validate(self, document):
        if len(document.text) == 0:
            raise ValidationError(
                message="Please enter a value",
                cursor_position=len(document.text),
            )
        if document.text.isdigit() == True:
            raise ValidationError(
                message="Please enter a non-numeric value for name",
                cursor_position=len(document.text),
            )
# Function to capture customer inputs
def customer_data():
    
    instruction_to_user ="Use up/down arrow keys to select, and hit enter"

    #Asking customer name with input validation
    name = questionary.text("What is your name?",
        qmark="1.",
        validate=name_validator,
        style=custom_style_fancy
    ).ask()
    
    #Asking customer about the income
    income = questionary.select(
        "What would you consider your income level to be?",
        qmark="2.",
        instruction=instruction_to_user,
        choices=["Low","Medium","High"],
        style=custom_style_fancy
    ).ask()
    
    #Asking customer about the perspective about financial risks
    word = questionary.select(
        "Which of the following words do you most associate with risk in the financial context?",
        qmark="3.",
        instruction=instruction_to_user,
        choices=["Loss","Uncertainty","Opportunity"],
        style=custom_style_fancy
    ).ask()
    
    #Asking customer about financial performance
    expect = questionary.select(
        "Which statement describes your expected portfolio performance in the next 2 years?",
        qmark="4.",
        instruction=instruction_to_user,
        choices=["I'm expecting a small return, I can't tolerate a loss", "I can tolerate a small loss", "I don't mind a loss"],
        style=custom_style_fancy
    ).ask()
    
    #Asking customer about the perspective on losses
    protect = questionary.select(
        "Do you agree with the following statement?: \"Protecting my portfolio is more important than my returns.\"",
        qmark="5.",
        instruction=instruction_to_user,
        choices=["Agree","Neutral","Disagree"],
        style=custom_style_fancy
    ).ask()
    
    #Asking customer about investment choices
    unexpected = questionary.select(
        "If you unexpectedly received $100,000 to invest today, which of the following best describes you?",
        qmark="6.",
        instruction=instruction_to_user,
        choices=["Invest in quality bonds","Invest in a mix of bonds and stocks","Invest in Cryptocurrencies"],
        style=custom_style_fancy
    ).ask()
    
    #Asking customer about investment timeframe
    investment_timeframe = questionary.select(
        "How long do you want to invest?",
        qmark="7.",
        instruction=instruction_to_user,
        choices=["5-Years","6-Years","7-Years","8-Years","9-Years","10-Years"],
        style=custom_style_fancy
    ).ask()
    
    #Asking customer about investment amount
    investment_amount = questionary.text("How much do you want to invest? (min $5000)",
        qmark="8.",
        validate=value_validator,
        style=custom_style_fancy
    ).ask()

    # Taking the inputs from customer and creating a list
    answers = [name, income, word, expect, protect, unexpected,investment_timeframe, investment_amount]
    return answers

# Function to interprit the customer inputs and assigming values to calcuate risk levels
def interpret(customer_data):
    income_val = {
        "Low": 2,
        "Medium": 4,
        "High": 8
    }
    word_val = {
        "Loss": 2,
        "Uncertainty": 4,
        "Opportunity": 8
    }
    expect_val = {
        "I'm expecting a small return, I can't tolerate a loss": 2,
        "I can tolerate a small loss": 4,
        "I don't mind a loss": 8
    }
    protect_val = {
        "Agree": 2,
        "Neutral": 4,
        "Disagree": 8
    }
    unexpected_val = {
        "Invest in quality bonds": 2,
        "Invest in a mix of bonds and stocks": 4,
        "Invest in Cryptocurrencies": 8
    }

    # collecting the scores and aggregating them to derive the customer risk level
    q1 = income_val.get(customer_data[1])
    q2 = word_val.get(customer_data[2])
    q3 = expect_val.get(customer_data[3])
    q4 = protect_val.get(customer_data[4])
    q5 = unexpected_val.get(customer_data[5])
    
    # Adding up the scores for customers
    total = q1 + q2 + q3 + q4 + q5

    #Evaluating the score and assigning risk level
    if total in range(10,20):
        print("Low risk investment")
        return ("Low risk investment","low")
    elif total in range(20,30):
        print("Medium risk investment")
        return ("Medium risk investment","mid")
    elif total > 30:
        print("High risk investment")
        return ("High risk investment","high")
    

def run():
    #starts questionary and stores the data in a list
    customer_responses = customer_data()
    
    #deconstructs name an income for later use from customer_responses list
    name,*_,investment_amount = customer_responses

    #gets risk level from response interpretation
    _, risk = interpret(customer_responses)

    #retrieves crypto data and stock data, organizes it into a DataFrame with close dates
    crypto_df = crypto_alpaca.get_crypto_df()
    stocks_df = stocks.get_stocks_df(risk)

    #normalizing date values to have the same day in each index
    crypto_df.index = crypto_df.index.normalize()
    stocks_df.index = stocks_df.index.normalize()
    
    portfolio = pd.concat([stocks_df,crypto_df],axis=1).dropna()

    print(stocks.simulate(portfolio,risk,300,10))

if __name__ == "__main__":
    fire.Fire(run)
