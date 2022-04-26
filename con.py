from sys import maxsize
import akshare as ak
import h5py
from tqdm import tqdm

codes = [
    "000300",
    "000905",
    "000928",
    "000929",
    "000930",
    "000931",
    "000932",
    "000933",
    "000934",
    "000935",
    "000936",
    "000937",
    "000015",
    "000149",
    "000150",
    "000821",
    "000822",
    "000922"
]

def load():
    with h5py.File('csindex.h5', 'a') as f:
        for i in tqdm(range(len(codes))):
            code = codes[i]
            csindex_df = ak.index_stock_cons_weight_csindex(symbol=code)
            csindex_df["成分券代码"] = csindex_df["成分券代码"].map(lambda value: int(value))
            csindex_df = csindex_df.loc[:, ["成分券代码", "权重"]]
            dataset = csindex_df.to_numpy()
            if code not in f:
                ds = f.create_dataset(f"c{code}", data=dataset, compression="gzip")
            else:
                ds = f.create_dataset(f"c{code}", dataset.shape, compression="gzip", maxsize=(None, 2))
                ds[:dataset.shape[0]] = dataset


def load_history():
    for i in tqdm(range(len(codes))):
        code = codes[i]
        h_df = ak.index_stock_hist(symbol=f"sh{code}")
        h_df.to_csv(f"history/{code}.csv", index=False)

if __name__ == "__main__":
    # load()
    load_history()