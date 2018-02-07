from flask import Flask, render_template, request
from diff import html_diff

app = Flask(__name__)


app.config['DEBUG'] = False
app.config['CONFIG'] = {
    "add_class": "green",
    "add_element": "span",
    "remove_class": "red",
    "remove_element": "span",
    "moved_class": "yellow",
    "moved_element": "span",
}
app.config['ALLOWED_EXTENSIONS'] = {'html'}


def filetype_is_allowed(filename):
    maxsplit = 1
    return '.' in filename and \
           filename.rsplit('.', maxsplit)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def main():
    return render_template('index.html',
                           diffresult="Select files and click START button")


@app.route('/diff', methods=['POST'])
def api():
    if 'file1' not in request.files:
        return render_template('index.html', diffresult="Select source file!")
    else:
        file1 = request.files['file1']
    if filetype_is_allowed(file1.filename):
        file1_lines = [str(line, encoding='utf-8')
                       for line in file1.readlines()]
    else:
        return render_template('index.html',
                               diffresult="Source file should be HTML!")
    if 'file2' not in request.files:
        return render_template('index.html', diffresult="Select modified file!")
    else:
        file2 = request.files['file2']
    if filetype_is_allowed(file2.filename):
        file2_lines = [str(line, encoding='utf-8')
                       for line in file2.readlines()]
    else:
        return render_template('index.html',
                               diffresult="Modified file should be HTML!")
    diffresult = html_diff(file1_lines, file2_lines, app.config['CONFIG'])
    return render_template('index.html', diffresult=diffresult)


if __name__ == "__main__":
    app.run()
