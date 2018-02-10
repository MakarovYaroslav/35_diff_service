from flask import Flask, render_template, request
from diff import html_diff, filetype_is_allowed
from config import DevelopmentConfig

app = Flask(__name__)

app.config.from_object(DevelopmentConfig)


@app.route('/')
def main():
    return render_template('index.html',
                           diffresult="Select files and click START button")


@app.route('/difffile', methods=['POST'])
def diff_file():
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
        return render_template('index.html',
                               diffresult="Select modified file!")
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


@app.route('/difftext', methods=['POST'])
def diff_text():
    source_html = request.form['sourcehtml']
    modified_html = request.form['modifiedhtml']
    if not source_html:
        return render_template('index.html', diffresult="Source HTML is empty")
    if not modified_html:
        return render_template('index.html', diffresult="Modified HTML is empty")
    source_lines = source_html.split('\n')
    modified_lines = modified_html.split('\n')
    diffresult = html_diff(source_lines, modified_lines, app.config['CONFIG'])
    return render_template('index.html', diffresult=diffresult)


if __name__ == "__main__":
    app.run()
