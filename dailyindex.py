import akshare as ak
import pandas as pd
import h5py
import datetime
from tqdm import tqdm

symbols = [
'sh000300',
'sh000905',
'sh000928',
'sh000929',
'sh000930',
'sh000931',
'sh000932',
'sh000933',
'sh000934',
'sh000935',
'sh000936',
'sh000937',
'sh000015',
'sh000149',
'sh000150',
'sh000821',
'sh000822',
'sh000922',
'sz399324'
]

def update():
  with h5py.File('daily_index.h5', 'a') as f:
    for i in tqdm(range(len(symbols))):
      sym = symbols[i]
      df = ak.stock_zh_index_daily(symbol=sym)
      df["date"] = pd.DatetimeIndex(df["date"])
      df["idate"] = df["date"].map(lambda d: d.toordinal())
      df.index = df["date"]
      df = df.loc[:, ["idate", "close"]]

      if sym not in f:
        dset = f.create_dataset(sym, data=df.to_numpy(), compression="gzip", maxshape=(None, 2))
      else:
        dset = f[sym]
        last_day = datetime.date.fromordinal(int(dset[-1, 0]))
        last_day = last_day + datetime.timedelta(days=1)
        df_append = df.loc[last_day:]
        data_append = df_append.to_numpy()

        size = dset.len()
        dset.resize(size + data_append.shape[0], axis=0)
        dset[size:] = data_append


if __name__ == "__main__":
  update()