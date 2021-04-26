import argparse
import pandas as pd
from pubchempy import get_compounds, Compound


# imports canonical smiles from PubChem by cid
def canonical_extractor(data):
    comp_canonical = Compound.from_cid(data)
    return comp_canonical.canonical_smiles


# imports tpsa descriptor from PubChem by cid
def tpsa_extractor(data):
    comp_tpsa = get_compounds(data)
    return comp_tpsa[0].tpsa


# parses csv file, makes list of 'cid' and appends imported descriptors in columns
def create_new_features_csv(csv_src, csv_dest):
    dataframe = pd.read_csv(csv_src)
    canonical_list = []
    tpsa_list = []
    data_list = dataframe['cid'].to_list()

    for item in data_list:
        canonical_list.append(canonical_extractor(item))
        tpsa_list.append(tpsa_extractor(item))

    dataframe['Canonical_Smiles'] = canonical_list
    dataframe['tpsa'] = tpsa_list
    dataframe.to_csv(csv_dest, index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--src', help='Source of CSV file', required=True)
    parser.add_argument('--dest', help='Destination of CSV file', required=True)

    args = parser.parse_args()

    create_new_features_csv(args.src, args.dest)
