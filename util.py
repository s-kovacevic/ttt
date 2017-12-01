import logging
import configparser


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


def setup_logger():
    """
    Logger setup, call this at the beginning of the runtime
    """
    logging_config = get_config(section='LOGGING')
    # TODO make level configurable
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s | %(levelname)-8s %(name)-15s : %(message)s',
        filename=logging_config['file'] or 'mylog.log'
    )


def get_config(path='config.ini', section=None, force_reload=False):
    """
    Returns ConfigurationParsers instance for the given configuration path.
    Caches each file first time this method is called for that file in order
    to reduce IO calls unless force_reload is passed as True.
    :param path: file that should be read
    :param section: if provided, method will return this section of config file
    :param force_reload: if True, method will reload file from disk
    :return: ConfigurationParser instance for the given path
    """
    parsers = dict()
    if path not in parsers or force_reload:
        parser = configparser.ConfigParser()
        parser.read(path)
        parsers[path] = parser
    if section is not None:
        return parsers[path][section]
    return parsers[path]
