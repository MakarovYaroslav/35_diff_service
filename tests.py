import unittest
from server import app, filetype_is_allowed
from diff import html_diff, create_replace_tag, create_delete_tag,\
    create_insert_tag, create_equal_tag


class TestHtmlDiff(unittest.TestCase):
    def setUp(self):
        self.basic_html = ['<li>Автор: Григорьев П.А.</li>',
                           '<li>Сумма: 126000 руб.</li>',
                           '<li>Дата: 26.12.14</li>']
        self.base_config = app.config['CONFIG']

    def test_replace(self):
        replacement_string = '<li>Replacement text</li>'
        changed_html = [replacement_string,
                        '<li>Сумма: 126000 руб.</li>',
                        '<li>Дата: 26.12.14</li>']
        expected_diff = '<{0} class="{1}"><li>Автор: Григорьев П.А.</li>' \
                        '</{0}><{2} class="{3}">{4}</{2}>' \
                        '<li>Сумма: 126000 руб.</li>' \
                        '<li>Дата: 26.12.14</li>'.format(
                            self.base_config['remove_element'],
                            self.base_config['remove_class'],
                            self.base_config['add_element'],
                            self.base_config['add_class'],
                            replacement_string)
        received_diff = html_diff(self.basic_html, changed_html,
                                  self.base_config)
        self.assertEqual(expected_diff, received_diff)

    def test_delete(self):
        changed_html = ['<li>Сумма: 126000 руб.</li>',
                        '<li>Дата: 26.12.14</li>']
        expected_diff = '<{0} class="{1}"><li>Автор: Григорьев П.А.</li>' \
                        '</{0}><{2} class="{3}"><li>Сумма: 126000 руб.</li>'\
                        '<li>Дата: 26.12.14</li></{2}>'.format(
                            self.base_config['remove_element'],
                            self.base_config['remove_class'],
                            self.base_config['moved_element'],
                            self.base_config['moved_class'])
        received_diff = html_diff(self.basic_html, changed_html,
                                  self.base_config)
        self.assertEqual(expected_diff, received_diff)

    def test_insert(self):
        new_string = '<li>New element</li>'
        changed_html = ['<li>Автор: Григорьев П.А.</li>',
                        '<li>Сумма: 126000 руб.</li>',
                        '<li>Дата: 26.12.14</li>',
                        new_string]
        expected_diff = '<li>Автор: Григорьев П.А.</li>' \
                        '<li>Сумма: 126000 руб.</li>' \
                        '<li>Дата: 26.12.14</li>' \
                        '<{0} class="{1}">{2}</{0}>'.format(
                            self.base_config['add_element'],
                            self.base_config['add_class'],
                            new_string)
        received_diff = html_diff(self.basic_html, changed_html,
                                  self.base_config)
        self.assertEqual(expected_diff, received_diff)

    def test_equal(self):
        changed_html = ['<li>Автор: Григорьев П.А.</li>',
                        '<li>Сумма: 126000 руб.</li>',
                        '<li>Дата: 26.12.14</li>']
        expected_diff = ''.join(changed_html)
        received_diff = html_diff(self.basic_html, changed_html,
                                  self.base_config)
        self.assertEqual(expected_diff, received_diff)


class TestTagCreation(unittest.TestCase):
    def setUp(self):
        self.basic_html = ['<li>Автор: Григорьев П.А.</li>',
                           '<li>Сумма: 126000 руб.</li>',
                           '<li>Дата: 26.12.14</li>']
        self.changed_html = ['<li>Сумма: 126000 руб.</li>',
                             '<li>Автор: Петров Г.Е.</li>',
                             '<li>Дата: 26.12.14</li>']
        self.base_config = app.config['CONFIG']
        self.base_positions = [0, 1, 2, 3]

    def test_replace_tag_creation(self):
        expected_tag = '<{0} class="{1}">{2}</{0}>' \
                       '<{3} class="{4}">{5}</{3}>'.format(
                           self.base_config['remove_element'],
                           self.base_config['remove_class'],
                           ''.join(self.basic_html[
                                   self.base_positions[0]:
                                   self.base_positions[1]]),
                           self.base_config['add_element'],
                           self.base_config['add_class'],
                           ''.join(self.changed_html[
                                   self.base_positions[2]:
                                   self.base_positions[3]]))
        received_tag = create_replace_tag(self.basic_html,
                                          self.changed_html,
                                          self.base_config,
                                          self.base_positions)
        self.assertEqual(expected_tag, received_tag)

    def test_delete_tag_creation(self):
        expected_tag = '<{0} class="{1}">{2}</{0}>'.format(
            self.base_config['remove_element'],
            self.base_config['remove_class'],
            ''.join(self.basic_html[self.base_positions[0]:
                                    self.base_positions[1]]))
        received_tag = create_delete_tag(self.basic_html, self.base_config,
                                         self.base_positions)
        self.assertEqual(expected_tag, received_tag)

    def test_insert_tag_creation(self):
        expected_tag = '<{0} class="{1}">{2}</{0}>'.format(
            self.base_config['add_element'],
            self.base_config['add_class'],
            ''.join(self.changed_html[self.base_positions[2]:
                                      self.base_positions[3]]))
        received_tag = create_insert_tag(self.changed_html, self.base_config,
                                         self.base_positions)
        self.assertEqual(expected_tag, received_tag)

    def test_moved_tag_creation(self):
        expected_tag = '<{0} class="{1}">{2}</{0}>'.format(
            self.base_config['moved_element'],
            self.base_config['moved_class'],
            ''.join(self.changed_html[self.base_positions[2]:
                                      self.base_positions[3]]))
        received_tag = create_equal_tag(self.changed_html, self.base_config,
                                        self.base_positions)
        self.assertEqual(expected_tag, received_tag)

    def test_equal_creation(self):
        self.base_positions = [0, 1, 0, 1]
        expected_tag = '{0}'.format(
            ''.join(self.changed_html[self.base_positions[2]:
                                      self.base_positions[3]]))
        received_tag = create_equal_tag(self.changed_html, self.base_config,
                                        self.base_positions)
        self.assertEqual(expected_tag, received_tag)


class TestFileTypeCheck(unittest.TestCase):
    def setUp(self):
        self.file_types = ['html', 'txt', 'json']
        self.allowed_types = app.config['ALLOWED_EXTENSIONS']

    def test_file_type_check(self):
        for file_type in self.file_types:
            if file_type in self.allowed_types:
                self.assertTrue(filetype_is_allowed("test.%s" % file_type))
            else:
                self.assertFalse(filetype_is_allowed("test.%s" % file_type))


if __name__ == '__main__':
    unittest.main()
