

def pre_process_guitar_tabs(input_text, lines_per_tab=6):
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

    repeated_blocks = []
    # check if each row has a | at the end with only whitespace at the end
    # if thats not the case check if its a *[x|*]?\d? as we only allow this at the end of a row which means
    # its a repeated row -> remove it and copy the lines_per_tab which the row falls in and remember it
    for i in range(0, len(tab_lines), lines_per_tab):
        contains_repeating_indicator = [
          re.match(r'^.* +[x|*]+\d+[\t ]*$', line) for line in tab_lines[i:i + lines_per_tab]
        ]
        repeating_indicator_amount = len([x for x in contains_repeating_indicator if x])
        if repeating_indicator_amount > 1:
            raise ValueError("Invalid tab format. Only one repeating indicator per row is allowed")
        if repeating_indicator_amount == 1:

            line_with_a_match = [x for x in contains_repeating_indicator if x][0]
            repeat_amount = int(re.search(r'[x|*]+(\d+)', line_with_a_match.string).group(1))

            # remove the repeating indicator from the row
            repeated_block = tab_lines[i:i + lines_per_tab]
            repeated_block = [re.sub(r'[x|*]+\d+', '', line).strip() for line in repeated_block]

            # insert the repeated block at the position of the first row which has the repeating indicator
            tab_lines = tab_lines[:i] + repeated_block * repeat_amount + tab_lines[i + lines_per_tab:]
            repeated_blocks.append(i // lines_per_tab)


    # check if in each group of lines_per_tab all lines are equal length and return which lines are not equal
    for i in range(0, len(tab_lines), lines_per_tab):
        line_lengths = [len(line) for line in tab_lines[i:i + lines_per_tab]]
        if len(set(line_lengths)) != 1:
            raise ValueError("Invalid tab format. Number of columns must be equal")

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

    return rows