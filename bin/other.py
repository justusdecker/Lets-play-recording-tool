from bin.welcome_popup import WELCOME
WELCOME.update_message(f'Load: {__name__}')

GERMAN_CHAR_TO_ENTITY = {
    'Ä': '&Auml;', 'ä': '&auml;',
    'Ö': '&Ouml;', 'ö': '&ouml;',
    'Ü': '&Uuml;', 'ü': '&uuml;',
    'ß': '&szlig;',
    # Add more if needed, e.g., Euro sign if it's relevant for your German text
    # '€': '&euro;'
}
ENTITY_TO_GERMAN_CHAR = {v: k for k, v in GERMAN_CHAR_TO_ENTITY.items()}

def convert_to_entities(text: str) -> str:
    """
    Converts German umlauts (Ä, Ö, Ü) and 'ß' in a string to their
    corresponding HTML entities (e.g., 'ä' becomes '&auml;').

    Args:
        text (str): The input string.

    Returns:
        str: The string with German characters replaced by HTML entities.
    """
    if text is None: return ''
    converted_text = text
    for char, entity in GERMAN_CHAR_TO_ENTITY.items():
        converted_text = converted_text.replace(char, entity)
    return converted_text

def convert_from_entities(text: str) -> str:
    """
    Converts HTML entities for German umlauts (e.g., '&auml;') and 'ß'
    back to their corresponding German characters (e.g., 'ä').

    Args:
        text (str): The input string, potentially containing HTML entities.

    Returns:
        str: The string with HTML entities replaced by German characters.
    """
    if text is None: return ''
    for phrase in ENTITY_TO_GERMAN_CHAR:
        text = text.replace(phrase, ENTITY_TO_GERMAN_CHAR[phrase])
    return text