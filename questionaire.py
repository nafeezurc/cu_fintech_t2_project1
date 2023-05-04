import fire
import questionary

def customer_data():
    name = questionary.text("What is your name?").ask()
    income = questionary.select(
        "What would you consider your income level to be?",
        choices=["Low","Medium","High"],
    ).ask()
    word = questionary.select(
        "Which of the following words do you most associate with risk in the financial context?",
        choices=["Loss","Uncertainty","Opportunity"],
    ).ask()
    expect = questionary.select(
        "Which statement describes your expected portfolio performance in the next 2 years?",
        choices=["I'm expecting a small return, I can't tolerate a loss", "I can tolerate a small loss", "I don't mind a loss"],
    ).ask()
    protect = questionary.select(
        "Do you agree with the following statement?: \"Protecting my portfolio is more important than my returns.\"",
        choices=["Agree","Neutral","Disagree"],
    ).ask()
    unexpected = questionary.select(
        "If you unexpectedly received $100,000 to invest today, which of the following best describes you?",
        choices=["Invest in quality bonds","Invest in a mix of bonds and stocks","Invest in Cryptocurrencies"],
    ).ask()
    
    answers = [name, income, word, expect, protect, unexpected]
    return answers

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

    q1 = income_val.get(customer_data[1])
    q2 = word_val.get(customer_data[2])
    q3 = expect_val.get(customer_data[3])
    q4 = protect_val.get(customer_data[4])
    q5 = unexpected_val.get(customer_data[5])
    total = q1 + q2 + q3 + q4 + q5
    if total in range(10,20):
        return "Low risk investment"
    elif total in range(20,30):
        return "Medium risk investment"
    elif total > 30:
        return "High risk investment"