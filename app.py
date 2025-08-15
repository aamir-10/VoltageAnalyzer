from flask import Flask, render_template
import plotly.io as pio
from charts import generate_charts  # import your function

app = Flask(__name__)

@app.route('/')
def index():
    charts_data = generate_charts()
    chart_html_list = [
        (pio.to_html(fig, full_html=False, include_plotlyjs='cdn'), title)
        for fig, title in charts_data
    ]
    return render_template('index.html', charts=chart_html_list)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
