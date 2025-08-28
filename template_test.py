# Simple test file to check if templates are working
from flask import Flask, render_template
from jinja2 import TemplateNotFound

app = Flask(__name__)

@app.route('/test')
def test():
    try:
        return render_template('browse.html', models={'items': [], 'pages': 0}, search='')
    except TemplateNotFound as e:
        return f"Template not found: {e}"
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)
