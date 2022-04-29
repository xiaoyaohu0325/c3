import pandas as pd
import h5py
import os

def compare_date(item):
    return (item[0], item[1])

def order_list(df):
    unique_in_dates = set(df["in_date"].to_list())
    unique_in_dates = list(unique_in_dates)
    unique_in_dates.sort()
    unique_out_dates = set(df["out_date"].to_list())
    unique_out_dates= list(unique_out_dates)
    unique_out_dates.sort()

    unique_in_dates = [(item, 'in') for item in unique_in_dates]
    unique_out_dates = [(item, 'out') for item in unique_out_dates]
    unique_dates = unique_in_dates + unique_out_dates

    unique_dates.sort(key=compare_date, reverse=True)
    return unique_dates


def add(stock_set, df, outdate):
    out_df = df[df["out_date"] == outdate]
    stocks = out_df["stock_code"].to_list()
    stock_set.update(stocks)
    return stock_set


def remove(stock_set, df, indate):
    in_df = df[df["in_date"] == indate]
    stocks = in_df["stock_code"].to_list()
    for item in stocks:
        if item in stock_set:
            stock_set.remove(item)
    return stock_set


def save(stock_set, code, date):
    out_df = pd.DataFrame(list(stock_set), columns=["code"])
    out_df["code"] = out_df["code"].map(lambda value: str(value).zfill(6))

    if not os.path.exists(f"index_history/{code}"):
        os.makedirs(f"index_history/{code}")

    out_df.to_csv(f"index_history/{code}/{date}.csv", index=False)


def generate_history(code):
    with h5py.File("csindex.h5", "r") as f:
        dset = f["c000300"][:, 0]

    dset = [int(item) for item in dset]
    df = pd.read_csv(f"history/{code}.csv")
    orders = order_list(df)
    current_stocks = set(dset)

    for order in orders:
        # 倒序方式处理历史数据，把out的加回到列表，把in的移除出列表
        if order[1] == 'out':
            current_stocks = add(current_stocks, df, order[0])
            save(current_stocks, code, order[0])
        elif order[1] == 'in':
            current_stocks = remove(current_stocks, df, order[0])
            save(current_stocks, code, order[0])

if __name__ == "__main__":
    generate_history("000905")