
def limited_input(prompt='', limit_to=(), help_=''):
    """
    Utility function that reduces boilerplate code when user input is limited
    to several choices
    :param limit_to: list of things that user can input
    :param prompt: will be printed when user input is required
    :param help_: what to print in case user provides invalid value
    :return: user input that passed the check
    """
    user_input = input(prompt)
    while user_input not in limit_to:
        print(help_)
        user_input = input()
    return user_input
