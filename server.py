from flask import Flask, render_template, request
from config import DiffConfig
from diff import html_diff

app = Flask(__name__)

app.config.from_object(DiffConfig)


def filetype_is_allowed(filename):
    maxsplit = 1
    return '.' in filename and \
           filename.rsplit('.', maxsplit)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def main():
        return render_template('index.html',
                               result="Select files and click START button")


@app.route('/diff', methods=['POST'])
def api():
    if 'file1' not in request.files:
        return render_template('index.html', result="Select source file!")
    else:
        file1 = request.files['file1']
    if filetype_is_allowed(file1.filename):
        file1_lines = [str(line, encoding='utf-8')
                       for line in file1.readlines()]
    else:
        return render_template('index.html',
                               result="Source file should be HTML!")
    if 'file2' not in request.files:
        return render_template('index.html', result="Select modified file!")
    else:
        file2 = request.files['file2']
    if filetype_is_allowed(file2.filename):
        file2_lines = [str(line, encoding='utf-8')
                       for line in file2.readlines()]
    else:
        return render_template('index.html',
                               result="Modified file should be HTML!")
    result = html_diff(file1_lines, file2_lines, app.config['CONFIG'])
    return render_template('index.html', result=result)


if __name__ == "__main__":
    app.run()
