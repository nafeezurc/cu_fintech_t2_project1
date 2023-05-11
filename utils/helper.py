def get_years_from_answer(answer):
    if answer is None:
        return None
    return answer.split('-')[0]

def interpret_results(table,initial_investment,name,investment_timeframe):
    mean = table[1]
    lower_95 = float(table[8])
    upper_95 = float(table[9])

    #print(type(lower_95),type(upper_95),type(initial_investment))

    return f"""
          {name}, with your current investment of ${initial_investment}. You will get an  estimated return of {round(mean*100,2)}% 
           with a total between ${round(lower_95*initial_investment,2)} in {investment_timeframe} years and 
          ${round(upper_95*initial_investment,2)}
          """
    