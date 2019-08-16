#

# from excel to json file

import pandas as pd
import sys
import json

DEALING_FS = {
    "": str,
    "group": str, "proc": str, "title": str, "link": str, "description": str,
    "year": int,
    "task": lambda x: x.split("|"),
    "tag": lambda x: x.split("|"),
}

def main(fin: str, fout: str):
    df = pd.read_excel(fin, sheet_name='Sheet1')
    # read input
    fields = list(df.columns)
    assert len(set(fields)) == len(fields)  # no repeat names
    num_field = len(fields)
    fs = [DEALING_FS[k] for k in fields]
    # rs = []
    with open(fout, 'w', encoding='utf-8') as fd:
        for idx in range(df.shape[0]):
            cur_fields = df.iloc[idx].values
            assert len(cur_fields) == num_field
            r = {k:f(v) for k, v, f in zip(fields, cur_fields, fs)}
            # rs.append(r)
            fd.write(json.dumps(r)+"\n")

if __name__ == '__main__':
    main(*sys.argv[1:])
