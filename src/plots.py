import matplotlib
import matplotlib.pyplot as plt

import plotly.express as px
import seaborn as sns

from pandas import DataFrame
import pandas as pd


def plot_revenue_by_month_year(df: DataFrame, year: int):
    """Plot revenue by month in a given year

    Args:
        df (DataFrame): Dataframe with revenue by month and year query result
        year (int): It could be 2016, 2017 or 2018
    """
    matplotlib.rc_file_defaults()
    sns.set_style(style=None, rc=None)

    _, ax1 = plt.subplots(figsize=(12, 6))

    sns.lineplot(data=df[f"Year{year}"], marker="o", sort=False, ax=ax1)
    ax2 = ax1.twinx()

    sns.barplot(data=df, x="month", y=f"Year{year}", alpha=0.5, ax=ax2)
    ax1.set_title(f"Revenue by month in {year}")

    plt.show()


def plot_real_vs_predicted_delivered_time(df: DataFrame, year: int):
    """Plot real vs predicted delivered time by month in a given year

    Args:
        df (DataFrame): Dataframe with real vs predicted delivered time by month and
                        year query result
        year (int): It could be 2016, 2017 or 2018
    """
    matplotlib.rc_file_defaults()
    sns.set_style(style=None, rc=None)

    _, ax1 = plt.subplots(figsize=(12, 6))

    sns.lineplot(data=df[f"Year{year}_real_time"], marker="o", sort=False, ax=ax1)
    ax1.twinx()
    g = sns.lineplot(
        data=df[f"Year{year}_estimated_time"], marker="o", sort=False, ax=ax1
    )
    g.set_xticks(range(len(df)))
    g.set_xticklabels(df.month.values)
    g.set(xlabel="month", ylabel="Average days delivery time", title="some title")
    ax1.set_title(f"Average days delivery time by month in {year}")
    ax1.legend(["Real time", "Estimated time"])

    plt.show()


def plot_global_amount_order_status(df: DataFrame):
    """Plot global amount of order status

    Args:
        df (DataFrame): Dataframe with global amount of order status query result
    """
    _, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

    elements = [x.split()[-1] for x in df["order_status"]]

    wedges, autotexts = ax.pie(df["Ammount"], textprops=dict(color="w"))

    ax.legend(
        wedges,
        elements,
        title="Order Status",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1),
    )

    plt.setp(autotexts, size=8, weight="bold")

    ax.set_title("Order Status Total")

    my_circle = plt.Circle((0, 0), 0.7, color="white")
    p = plt.gcf()
    p.gca().add_artist(my_circle)

    plt.show()


def plot_revenue_per_state(df: DataFrame):
    """Plot revenue per state

    Args:
        df (DataFrame): Dataframe with revenue per state query result
    """
    fig = px.treemap(
        df, path=["customer_state"], values="Revenue", width=800, height=400
    )
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    fig.show()


def plot_top_10_least_revenue_categories(df: DataFrame):
    """Plot top 10 least revenue categories

    Args:
        df (DataFrame): Dataframe with top 10 least revenue categories query result
    """
    _, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

    elements = [x.split()[-1] for x in df["Category"]]

    revenue = df["Revenue"]
    wedges, autotexts = ax.pie(revenue, textprops=dict(color="w"))

    ax.legend(
        wedges,
        elements,
        title="Top 10 Revenue Categories",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1),
    )

    plt.setp(autotexts, size=8, weight="bold")
    my_circle = plt.Circle((0, 0), 0.7, color="white")
    p = plt.gcf()
    p.gca().add_artist(my_circle)

    ax.set_title("Top 10 Least Revenue Categories ammount")

    plt.show()


def plot_top_10_revenue_categories_ammount(df: DataFrame):
    """Plot top 10 revenue categories

    Args:
        df (DataFrame): Dataframe with top 10 revenue categories query result
    """
    # Plotting the top 10 revenue categories ammount
    _, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

    elements = [x.split()[-1] for x in df["Category"]]

    revenue = df["Revenue"]
    wedges, autotexts = ax.pie(revenue, textprops=dict(color="w"))

    ax.legend(
        wedges,
        elements,
        title="Top 10 Revenue Categories",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1),
    )

    plt.setp(autotexts, size=8, weight="bold")
    my_circle = plt.Circle((0, 0), 0.7, color="white")
    p = plt.gcf()
    p.gca().add_artist(my_circle)

    ax.set_title("Top 10 Revenue Categories ammount")

    plt.show()


def plot_top_10_revenue_categories(df: DataFrame):
    """Plot top 10 revenue categories

    Args:
        df (DataFrame): Dataframe with top 10 revenue categories query result
    """
    fig = px.treemap(df, path=["Category"], values="Num_order", width=800, height=400)
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    fig.show()


def plot_freight_value_weight_relationship(df: DataFrame):
    """Plot freight value vs product weight relationship.

    Args:
        df (DataFrame): DataFrame con las columnas 'product_weight_g' y 'freight_value'
                        que describen el peso y el valor del flete, respectivamente.
    """
    
    # TODO: Representar gráficamente la relación entre el valor del flete y el peso usando un scatterplot de seaborn.
    # El eje x debe ser el peso (weight) y el eje y debe ser el valor del flete (freight value).

    # Ajustamos el estilo y el tamaño de la figura
    plt.figure(figsize=(8, 6))

    # Creamos el scatterplot con seaborn
    sns.scatterplot(
        data=df,
        x='product_weight_g',     
        y='freight_value',        
        alpha=0.7                
    )

    plt.xlabel('Product Weight (g)')
    plt.ylabel('Freight Value')
    plt.title('Freight Value vs Product Weight')

    # Mostramos el gráfico
    plt.show()


def plot_delivery_date_difference(df: DataFrame):
    """Plot delivery date difference

    Args:
        df (DataFrame): Dataframe with delivery date difference query result
    """
    sns.barplot(data=df, x="Delivery_Difference", y="State").set(
        title="Difference Between Delivery Estimate Date and Delivery Date"
    )


def plot_order_amount_per_day_with_holidays(df: DataFrame):
    """Grafica la cantidad de pedidos por día, marcando los días festivos.

    Args:
        df (DataFrame): DataFrame con los resultados de cantidad de pedidos por día y días festivos.
                       Se espera que tenga las columnas 'order_count', 'date' y 'holiday'.
    """
    
    # TODO: Graficar el monto de pedidos por día con los días festivos usando matplotlib.
    # Marcar los días festivos con líneas verticales.
    # Sugerencia: usar plt.axvline.

    # Convertimos la columna 'date' a formato datetime
    df['date'] = pd.to_datetime(df['date'])

    # Creamos la figura y el eje
    fig, ax = plt.subplots(figsize=(12, 6))

    # Graficamos la cantidad de pedidos por día (línea verde)
    ax.plot(df['date'], df['order_count'], label='Order Count', color='green')

    # Verificamos si existe la columna 'holiday' que indique los días festivos
    if 'holiday' in df.columns:
        # 'holiday' es booleana: True indica un día festivo
        holiday_dates = df.loc[df['holiday'] == True, 'date']
    else:
        holiday_dates = []

    # Dibujamos líneas verticales para cada día festivo (línea punteada azul)
    for i, holiday in enumerate(holiday_dates):
        label = 'Holiday' if i == 0 else None
        ax.axvline(
            holiday,
            color='blue',
            linestyle=':',
            alpha=0.7,
            label=label
        )

    ax.set_title('Order Count per Day with Holidays')
    ax.set_xlabel('Date')
    ax.set_ylabel('Order Count')
    ax.legend()

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    #raise NotImplementedError