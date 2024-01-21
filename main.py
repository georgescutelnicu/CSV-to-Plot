from flask import Flask, render_template, redirect, url_for, request
import pandas as pd
import os
from charts import (generate_bar_chart, generate_hist_plot, generate_pie_chart, generate_scatter_plot,
                    generate_line_chart)
from helper_functions import preprocess_data


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

df = pd.DataFrame()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/dataframe', methods=['POST'])
def upload():
    file = request.files['file']

    if file and file.filename.endswith('.csv'):
        global df
        df = pd.read_csv(file).dropna()
        df = preprocess_data(df)
        unique_elements = {col: f'{col_data.nunique()} unique elements' for col, col_data in df.items()}
        df_modified = df.copy(deep=True)
        df_modified.loc[-1] = unique_elements
        df_modified = df_modified.dropna().sort_index()

        columns = list(df.columns)

        if len(df_modified) > 50:
            df_modified = df_modified.head(50)

        return render_template('dataframe.html', df_html=df_modified.to_html(index=False), columns=columns, df=df,
                               name=file.filename)

    return redirect(url_for("home"))


@app.route('/demo')
def demo():
    file = 'movies.csv'
    global df

    df = pd.read_csv(file).dropna()
    df = preprocess_data(df)
    unique_elements = {col: f'{col_data.nunique()} unique elements' for col, col_data in df.items()}
    df_modified = df.copy(deep=True)
    df_modified.loc[-1] = unique_elements
    df_modified = df_modified.dropna().sort_index()

    columns = list(df.columns)

    if len(df_modified) > 50:
        df_modified = df_modified.head(50)

    return render_template('dataframe.html', df_html=df_modified.to_html(index=False), columns=columns, df=df,
                           name=file)


@app.route('/generate_chart', methods=['POST'])
def generate_chart():
    try:
        chart_type = request.form['chartType']

        if chart_type == 'bar':
            x_axis = request.form['xAxis']
            y_axis = request.form['yAxis']
            plot_url = generate_bar_chart(df, x_axis, y_axis)
        elif chart_type == 'hist':
            axis_column = request.form['axis']
            bins = int(request.form['bins'])
            plot_url = generate_hist_plot(df, axis_column, bins)
        elif chart_type == 'line':
            x_axis = request.form['xAxis']
            y_axis = request.form['yAxis']
            plot_url = generate_line_chart(df, x_axis, y_axis)
        elif chart_type == 'pie':
            pie_column = request.form['pieColumn']
            plot_url = generate_pie_chart(df, pie_column)
        elif chart_type == 'scatter':
            x_axis = request.form['xAxis']
            y_axis = request.form['yAxis']
            c = request.form['scatterColor']
            if c == "None":
                c = None
            plot_url = generate_scatter_plot(df, x_axis, y_axis, c)
        else:
            return redirect(url_for("home"))

        return render_template('chart.html', plot_url=plot_url)

    except NameError:
        return redirect(url_for("home"))


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
