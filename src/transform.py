from collections import namedtuple
from enum import Enum
from typing import Callable, Dict, List

import pandas as pd
from pandas import DataFrame, read_sql
from sqlalchemy.engine.base import Engine

from src.config import QUERIES_ROOT_PATH

QueryResult = namedtuple("QueryResult", ["query", "result"])


class QueryEnum(Enum):
    """This class enumerates all the queries that are available"""

    DELIVERY_DATE_DIFFERECE = "delivery_date_difference"
    GLOBAL_AMMOUNT_ORDER_STATUS = "global_ammount_order_status"
    REVENUE_BY_MONTH_YEAR = "revenue_by_month_year"
    REVENUE_PER_STATE = "revenue_per_state"
    TOP_10_LEAST_REVENUE_CATEGORIES = "top_10_least_revenue_categories"
    TOP_10_REVENUE_CATEGORIES = "top_10_revenue_categories"
    REAL_VS_ESTIMATED_DELIVERED_TIME = "real_vs_estimated_delivered_time"
    ORDERS_PER_DAY_AND_HOLIDAYS_2017 = "orders_per_day_and_holidays_2017"
    GET_FREIGHT_VALUE_WEIGHT_RELATIONSHIP = "get_freight_value_weight_relationship"


def read_query(query_name: str) -> str:
    """Read the query from the file.

    Args:
        query_name (str): The name of the file.

    Returns:
        str: The query as a string.
    """
    with open(f"{QUERIES_ROOT_PATH}/{query_name}.sql", "r") as f:
        sql = f.read()
    return sql


def query_delivery_date_difference(database: Engine) -> QueryResult:
    """Get the query for delivery date difference."""
    query_name = QueryEnum.DELIVERY_DATE_DIFFERECE.value
    query = read_query(query_name)
    with database.connect() as connection:
        result = read_sql(query, connection.connection)
    return QueryResult(query=query_name, result=result)


def query_global_ammount_order_status(database: Engine) -> QueryResult:
    """Get the query for global amount of order status."""
    query_name = QueryEnum.GLOBAL_AMMOUNT_ORDER_STATUS.value
    query = read_query(query_name)
    with database.connect() as connection:
        result = read_sql(query, connection.connection)
    return QueryResult(query=query_name, result=result)


def query_revenue_by_month_year(database: Engine) -> QueryResult:
    """Get the query for revenue by month year."""
    query_name = QueryEnum.REVENUE_BY_MONTH_YEAR.value
    query = read_query(query_name)
    with database.connect() as connection:
        result = read_sql(query, connection.connection)
    return QueryResult(query=query_name, result=result)


def query_revenue_per_state(database: Engine) -> QueryResult:
    """Get the query for revenue per state."""
    query_name = QueryEnum.REVENUE_PER_STATE.value
    query = read_query(query_name)
    with database.connect() as connection:
        result = read_sql(query, connection.connection)
    return QueryResult(query=query_name, result=result)


def query_top_10_least_revenue_categories(database: Engine) -> QueryResult:
    """Get the query for top 10 least revenue categories."""
    query_name = QueryEnum.TOP_10_LEAST_REVENUE_CATEGORIES.value
    query = read_query(query_name)
    with database.connect() as connection:
        result = read_sql(query, connection.connection)
    return QueryResult(query=query_name, result=result)


def query_top_10_revenue_categories(database: Engine) -> QueryResult:
    """Get the query for top 10 revenue categories."""
    query_name = QueryEnum.TOP_10_REVENUE_CATEGORIES.value
    query = read_query(query_name)
    with database.connect() as connection:
        result = read_sql(query, connection.connection)
    return QueryResult(query=query_name, result=result)


def query_real_vs_estimated_delivered_time(database: Engine) -> QueryResult:
    """Get the query for real vs estimated delivered time."""
    query_name = QueryEnum.REAL_VS_ESTIMATED_DELIVERED_TIME.value
    query = read_query(query_name)
    with database.connect() as connection:
        result = read_sql(query, connection.connection)
    return QueryResult(query=query_name, result=result)


def query_freight_value_weight_relationship(database: Engine) -> QueryResult:
    """Get the freight_value vs weight relationship for delivered orders.

    This query merges the orders, items, and products tables, filtering only
    'delivered' orders and aggregating freight_value and product_weight_g by order.
    """
    query_name = QueryEnum.GET_FREIGHT_VALUE_WEIGHT_RELATIONSHIP.value

    with database.connect() as connection:
        # Leemos las tablas
        orders = read_sql("SELECT * FROM olist_orders", connection.connection)
        items = read_sql("SELECT * FROM olist_order_items", connection.connection)
        products = read_sql("SELECT * FROM olist_products", connection.connection)

    # Fusionamos las tablas
    data = pd.merge(items, orders, on="order_id", how="inner")
    data = pd.merge(data, products, on="product_id", how="inner")

    # Filtramos pedidos con estado 'delivered'
    delivered = data[data["order_status"] == "delivered"]

    # Sumamos freight_value y product_weight_g por order_id
    aggregations = delivered.groupby("order_id", as_index=False).agg(
        {"freight_value": "sum", "product_weight_g": "sum"}
    )

    return QueryResult(query=query_name, result=aggregations)


def query_orders_per_day_and_holidays_2017(database: Engine) -> QueryResult:
    """Get the query for orders per day and holidays in 2017."""
    query_name = QueryEnum.ORDERS_PER_DAY_AND_HOLIDAYS_2017.value
    with database.connect() as connection:
        # Leemos los días festivos
        holidays = read_sql("SELECT * FROM public_holidays", connection.connection)
        holidays["date"] = pd.to_datetime(holidays["date"]).dt.date

        # Leemos las órdenes
        orders = read_sql("SELECT * FROM olist_orders", connection.connection)
        orders["order_purchase_timestamp"] = pd.to_datetime(orders["order_purchase_timestamp"])
        filtered_dates = orders[orders["order_purchase_timestamp"].dt.year == 2017]

        order_purchase_ammount_per_date = (
            filtered_dates.groupby(filtered_dates["order_purchase_timestamp"].dt.date)
            .size()
            .reset_index(name="order_count")
        )

        order_purchase_ammount_per_date.rename(
            columns={order_purchase_ammount_per_date.columns[0]: "date"}, inplace=True
        )
        order_purchase_ammount_per_date["holiday"] = order_purchase_ammount_per_date["date"].apply(
            lambda x: x in set(holidays["date"])
        )
        result_df = order_purchase_ammount_per_date[["order_count", "date", "holiday"]]

    return QueryResult(query=query_name, result=result_df)


def get_all_queries() -> List[Callable[[Engine], QueryResult]]:
    """Get all queries.

    Returns:
        List[Callable[[Engine], QueryResult]]: A list of all queries.
    """
    return [
        query_delivery_date_difference,
        query_global_ammount_order_status,
        query_revenue_by_month_year,
        query_revenue_per_state,
        query_top_10_least_revenue_categories,
        query_top_10_revenue_categories,
        query_real_vs_estimated_delivered_time,
        query_orders_per_day_and_holidays_2017,
        query_freight_value_weight_relationship,
    ]


def run_queries(database: Engine) -> Dict[str, DataFrame]:
    """Run all queries and store results in a dictionary.

    Args:
        database (Engine): Database connection.

    Returns:
        Dict[str, DataFrame]: A dictionary with keys as query names and values as dataframes.
    """
    query_results = {}
    for query in get_all_queries():
        query_result = query(database)
        query_results[query_result.query] = query_result.result
    return query_results
