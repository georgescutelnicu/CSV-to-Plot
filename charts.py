import matplotlib.pyplot as plt
import matplotlib
import io
import base64

matplotlib.use('agg')


def generate_bar_chart(df, x_column, y_column):
    """
        Generate a bar chart from the given DataFrame.

        Parameters:
            df (pd.DataFrame): The DataFrame containing the data.
            x_column (str): The column to be used for the x-axis.
            y_column (str): The column to be used for the y-axis.

        Returns:
            str: Base64-encoded image URL of the generated bar chart.
    """
    plt.figure(figsize=(18, 10))
    df[x_column] = df[x_column].astype(str)

    plt.bar(df[x_column], df[y_column])
    plt.title('Bar Chart')
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.xticks(rotation=60, ha='right', fontsize=8)

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode()

    return plot_url


def generate_hist_plot(df, axis_column, bins):
    """
        Generate a histogram from the given DataFrame.

        Parameters:
            df (pd.DataFrame): The DataFrame containing the data.
            axis_column (str): The column to be used for the histogram.
            bins (int): The number of bins for the histogram.

        Returns:
            str: Base64-encoded image URL of the generated histogram.
    """
    plt.figure(figsize=(18, 8))

    plt.hist(df[axis_column], bins=bins, edgecolor='black')
    plt.title('Histogram')
    plt.xlabel(axis_column)
    plt.ylabel('Frequency')
    plt.xticks(rotation=60, ha='right', fontsize=8)

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode()

    return plot_url


def generate_pie_chart(df, column):
    """
        Generate a pie chart from the given DataFrame.

        Parameters:
            df (pd.DataFrame): The DataFrame containing the data.
            column (str): The column to be used for the pie chart.

        Returns:
            str: Base64-encoded image URL of the generated pie chart.
    """
    plt.figure(figsize=(10, 10))

    counts = df[column].value_counts()
    wedges, texts, autotexts = plt.pie(counts, labels=None, autopct='', textprops=dict(color="w"),  pctdistance=2)

    legend_labels = [f'{index}: {count} {autotext.get_text()}' for index, count, autotext in zip(counts.index, counts,
                                                                                                 autotexts)]
    plt.legend(legend_labels, title=column, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    plt.title(f'Pie Chart - {column}')

    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode()

    return plot_url


def generate_scatter_plot(df, x_column, y_column, color_column):
    """
        Generate a scatter plot from the given DataFrame.

        Parameters:
            df (pd.DataFrame): The DataFrame containing the data.
            x_column (str): The column to be used for the x-axis.
            y_column (str): The column to be used for the y-axis.
            color_column (str, optional): The column to be used for color-coding points (optional).

        Returns:
            str: Base64-encoded image URL of the generated scatter plot.
    """
    plt.figure(figsize=(10, 8))
    legend = None

    if color_column is not None:
        color_mapping = {value: code for code, value in enumerate(df[color_column].unique())}
        color_codes = df[color_column].map(color_mapping)

        scatter = plt.scatter(df[x_column], df[y_column], c=color_codes, alpha=0.7, cmap='tab10')

        handles, labels = scatter.legend_elements()
        legend_labels = list(map(str, df[color_column].unique()))
        legend = plt.legend(handles, legend_labels, title=color_column, loc='upper left', bbox_to_anchor=(1, 1))

    else:
        scatter = plt.scatter(df[x_column], df[y_column], alpha=0.7)

    plt.title('Scatter Plot')
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.xticks(rotation=60, ha='right', fontsize=8)

    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight', bbox_extra_artists=[legend] if color_column else None)
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode()

    return plot_url


def generate_line_chart(df, x_column, y_column):
    """
        Generate a line chart with rolling mean from the given DataFrame.

        Parameters:
            df (pd.DataFrame): The DataFrame containing the data.
            x_column (str): The column to be used for the x-axis.
            y_column (str): The column to be used for the y-axis.

        Returns:
            str: Base64-encoded image URL of the generated line chart.
    """
    plt.figure(figsize=(18, 10))

    df = df.sort_values(by=[x_column])

    # Calculate the rolling mean to smooth out the line
    df['rolling_mean'] = df[y_column].rolling(window=10).mean()

    plt.plot(df[x_column], df['rolling_mean'], linestyle='-', color='b')
    plt.title('Line Chart with Rolling Mean')
    plt.xlabel(x_column)
    plt.ylabel(f'{y_column} (with Rolling Mean)')
    plt.xticks(rotation=60, ha='right', fontsize=8)

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode()

    return plot_url


def generate_hexbin(df, x_column, y_column):
    """
       Generate a hexbin plot from the given DataFrame.

       Parameters:
           df (pd.DataFrame): The DataFrame containing the data.
           x_column (str): The column to be used for the x-axis.
           y_column (str): The column to be used for the y-axis.

       Returns:
           str: Base64-encoded image URL of the generated hexbin plot.
    """
    plt.figure(figsize=(12, 8))

    plt.hexbin(df[x_column], df[y_column], gridsize=20, cmap='Blues')
    plt.colorbar(label='Count')
    plt.title('Hexbin Plot')
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.xticks(rotation=60, ha='right', fontsize=8)

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode()

    return plot_url
