code_keypad = [49, 50, 51, 52, 53, 54, 55, 56, 57]  # 1 - 9 respectively
# code_mouse = [1, 2, 3]  # Left click, middle click, right click respectively


def translate_pygame_keypadcode(user_input):

    """
    :param user_input: a keyboard press
    :return: the raw representation of the keyboard input
    :type: int

    This module is separate for scalability purposes.
    """

    if user_input in code_keypad:
        return code_keypad.index(user_input) + 1
    return None
