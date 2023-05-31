from os.path import exists
import pandas as pd


def create_empty_cars_df():
    # TODO: add more features to columns
    return pd.DataFrame(columns=["brand"])


def create_car_df_from_features(brand):
    # TODO: add more features to args
    car = {"brand": brand}
    return pd.DataFrame(car)
