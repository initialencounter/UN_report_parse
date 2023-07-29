from flask import Flask, request, render_template, jsonify

from io import BytesIO

from main import pdf_parser
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    """
        This is a function that returns an HTML string.

        :return: The HTML string.
        :rtype: str
    """
    if request.method == 'POST':
        file = request.files['file']
        if file:
            # file.save(file.filename)
            file_bytes = BytesIO(file.read())
            data = pdf_parser(file_bytes)
            return jsonify(data)
    return render_template('index.html', name="from")


if __name__ == '__main__':
    app.run()
