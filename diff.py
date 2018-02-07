import difflib


def get_compare_data(text1, text2):
    try:
        compare_data = difflib.SequenceMatcher(None, text1,
                                               text2, autojunk=False)
    except TypeError:
        compare_data = difflib.SequenceMatcher(None, text1, text2)
    return compare_data


def create_replace_tag(text1, text2, config, positions):
    replace_tag = '<{0} class="{1}">{2}</{0}>' \
                  '<{3} class="{4}">{5}</{3}>'.format(
                      config['remove_element'], config['remove_class'],
                      ''.join(text1[positions[0]:positions[1]]),
                      config['add_element'], config['add_class'],
                      ''.join(text2[positions[2]:positions[3]]))
    return replace_tag


def create_delete_tag(text1, config, positions):
    delete_tag = '<{0} class="{1}">{2}</{0}>'.format(
                 config['remove_element'], config['remove_class'],
                 ''.join(text1[positions[0]:positions[1]]))
    return delete_tag


def create_insert_tag(text2, config, positions):
    insert_tag = '<{0} class="{1}">{2}</{0}>'.format(
                 config['add_element'], config['add_class'],
                 ''.join(text2[positions[2]:positions[3]]))
    return insert_tag


def create_equal_tag(text2, config, positions):
    if positions[:2] == positions[2:4]:
        equal_tag = '{0}'.format(''.join(text2[positions[2]:positions[3]]))
    else:
        equal_tag = '<{0} class="{1}">{2}</{0}>'.format(
                    config['moved_element'], config['moved_class'],
                    ''.join(text2[positions[2]:positions[3]]))
    return equal_tag


def html_diff(html_text1, html_text2, config):
    out = []
    text1 = [line.strip() for line in html_text1]
    text2 = [line.strip() for line in html_text2]
    compare_data = get_compare_data(text1, text2)
    for opcode, *positions in compare_data.get_opcodes():
        if opcode == "replace":
            replace_tag = create_replace_tag(text1, text2, config, positions)
            out.append(replace_tag)
        elif opcode == "delete":
            delete_tag = create_delete_tag(text1, config, positions)
            out.append(delete_tag)
        elif opcode == "insert":
            insert_tag = create_insert_tag(text2, config, positions)
            out.append(insert_tag)
        elif opcode == "equal":
            equal_tag = create_equal_tag(text2, config, positions)
            out.append(equal_tag)
    return ''.join(out)
