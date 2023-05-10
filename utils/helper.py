def get_years_from_answer(answer):
    if answer is None:
        return None
    return answer.split('-')[0]