import difflib


def html_diff(html_text1, html_text2, config):
    out = []
    text1 = [line.strip() for line in html_text1]
    text2 = [line.strip() for line in html_text2]
    try:
        compare_data = difflib.SequenceMatcher(None, text1,
                                               text2, autojunk=False)
    except TypeError:
        compare_data = difflib.SequenceMatcher(None, text1, text2)
    for opcode, *positions in compare_data.get_opcodes():
        if opcode == "replace":
            out.append('<{0} class="{1}">{2}</{0}>'
                       '<{3} class="{4}">{5}</{3}>'.format(
                           config['remove_element'],
                           config['remove_class'],
                           ''.join(
                               text1[positions[0]:positions[1]]),
                           config['add_element'],
                           config['add_class'],
                           ''.join(
                               text2[positions[2]:positions[3]])))
        elif opcode == "delete":
            out.append('<{0} class="{1}">{2}</{0}>'.format(
                config['remove_element'],
                config['remove_class'],
                ''.join(text1[positions[0]:positions[1]])))
        elif opcode == "insert":
            out.append('<{0} class="{1}">{2}</{0}>'.format(
                config['add_element'],
                config['add_class'],
                ''.join(text2[positions[2]:positions[3]])))
        elif opcode == "equal":
            if positions[:2] == positions[2:4]:
                out.append('{0}'.format(''.join(
                    text2[positions[2]:positions[3]])))
            else:
                out.append('<{0} class="{1}">{2}</{0}>'.format(
                    config['moved_element'],
                    config['moved_class'],
                    ''.join(text2[positions[2]:positions[3]])))
    return ''.join(out)
