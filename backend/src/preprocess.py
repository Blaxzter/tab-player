import re
from typing import List


def pre_process_guitar_tabs(input_text, lines_per_tab = 6) -> (List[str], List[int]):
    """
    Preprocesses the input text and returns a list of rows
    :param input_text: the copied text from ultimate guitar
    :param lines_per_tab: the number of strings of the tab/instrument
    :return: a list of rows with len lines_per_tab where each row is a string
    """
    # Split the input into lines
    lines = input_text.split('\n')
    
    filter_regex = r'^[\t ]*[a-zA-Z]?\s*\|[-0-9h/p\\*^|]+\| *[x|*]?\d?$'
    
    # Filter out empty lines and lines that don't contain tab notation
    tab_lines = [
        line.strip() for line in lines if line.strip() and re.match(filter_regex, line)
    ]
    
    # check if tab is multiple of lines_per_tab
    if len(tab_lines) % lines_per_tab != 0:
        raise ValueError(
            f"Invalid tab format. Number of lines must be a multiple of {lines_per_tab}"
        )
    
    repeated_blocks, tab_lines = check_for_repeat_indicators(tab_lines, lines_per_tab)
    
    tab_lines = equalize_lines(tab_lines, lines_per_tab)
    
    rows = []
    # Split the tab lines into groups of lines_per_tab
    for i in range(0, lines_per_tab):
        row_list = tab_lines[i::lines_per_tab]
        # join rows and strip \s*[a-zA-Z]\s*\| from the beginning of each row
        cleand_row = [row_list[0]] + [re.sub(r'^\s*[a-zA-Z]\s*\|', '', line) for line in row_list[1:]]
        rows.append("".join(cleand_row))
    
    # check if len of each row is equal
    if len(set([len(_row) for _row in rows])) != 1:
        raise ValueError("Invalid tab format. Number of columns must be equal")
    
    return rows, repeated_blocks


def equalize_lines(tab_lines, lines_per_tab):
    # check if in each group of lines_per_tab all lines are equal length and return which lines are not equal
    for i in range(0, len(tab_lines), lines_per_tab):
        line_lengths = [len(line) for line in tab_lines[i:i + lines_per_tab]]
        max_line_length = max(line_lengths)
        # fill the lines that are shorter with - at the second last position until they are equal
        for j in range(len(line_lengths)):
            if line_lengths[j] < max_line_length:
                current_line = tab_lines[i + j]
                required_length = max_line_length - line_lengths[j]
                tab_lines[i + j] = current_line[:-1] + '-' * required_length + current_line[-1:]
                
    return tab_lines


def check_for_repeat_indicators(tab_lines: List[str], lines_per_tab: int = 6) -> (List[int], List[str]):
    """
    Search for x2 or *2 indicators at the end of a tab row and repeat the block of lines
    also remove the indicator from the row
    :param tab_lines: the list of tab lines found in the input text
    :param lines_per_tab: the number of strings of the tab/instrument
    :return: 1. A list of integers indicating the block with a repeating indicator
             2. The tab lines with repeated tab rows and removed indicators
    """
    repeated_blocks = []
    for i in range(0, len(tab_lines), lines_per_tab):
        contains_repeating_indicator = [
            re.match(r'^.* +[x|*]+\d+[\t ]*$', line) for line in tab_lines[i:i + lines_per_tab]
        ]
        repeating_indicator_amount = len([x for x in contains_repeating_indicator if x])
        if repeating_indicator_amount > 1:
            raise ValueError("Invalid tab format. Only one repeating indicator per row is allowed")
        elif repeating_indicator_amount == 1:
            line_with_a_match = [x for x in contains_repeating_indicator if x][0]
            repeat_amount = int(re.search(r'[x|*]+(\d+)', line_with_a_match.string).group(1))
            
            # remove the repeating indicator from the row
            repeated_block = tab_lines[i:i + lines_per_tab]
            repeated_block = [re.sub(r'[x|*]+\d+', '', line).strip() for line in repeated_block]
            
            # insert the repeated block at the position of the first row which has the repeating indicator
            tab_lines = tab_lines[:i] + repeated_block * repeat_amount + tab_lines[i + lines_per_tab:]
            repeated_blocks.append(i // lines_per_tab)
    return repeated_blocks, tab_lines
