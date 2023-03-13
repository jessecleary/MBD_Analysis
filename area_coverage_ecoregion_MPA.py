
## Lenfest Biodiversity - Area Coverage by Ecoregion and MPA
## Run for all MPAs

import geopandas as gpd
import pandas as pd
import numpy as np


## Ecoregion feature class
base_gdb =  r'V:\lenfest_nmsf_biodiversity\Data\lenfest_nmsf_base_prep.gdb'
ecoregion_base = gpd.read_file(f'{base_gdb}', layer='marine_ecoregions_final')
ecoregion_base["ER Area"] = (ecoregion_base["Shape_Area"] / (1000*1000))
ecoregion_base = ecoregion_base.drop(columns=["geometry","Shape_Length","Shape_Area"])


## Coverage tables
project_gdb = r'V:\lenfest_nmsf_biodiversity\Data\lenfest_nmsf_results.gdb'
mpa_df = gpd.read_file(f'{project_gdb}', layer='ecoregion_coverage_MPA')
full_protect_mpa_df = gpd.read_file(f'{project_gdb}', layer='ecoregion_coverage_full_protect_MPA')


## rename area/percentage columns, drop columns
## drop percentage column and recalc below - checked that this matches the output from ArcPro

mpa_df = mpa_df.rename(index=str, columns={"AREA":"MPA Coverage Area"})
mpa_df = mpa_df.drop(columns=["geometry","PERCENTAGE"])

full_protect_mpa_df = full_protect_mpa_df.rename(index=str, columns={"AREA":"FP-MPA Coverage Area"})
full_protect_mpa_df = full_protect_mpa_df.drop(columns=["geometry","PERCENTAGE"])


## join tables
summary_df = pd.merge(ecoregion_base, mpa_df, how="left", left_on="Ecoregion_ID", right_on="Ecoregion_ID")
summary_df = pd.merge(summary_df, full_protect_mpa_df, how="left", left_on="Ecoregion_ID", right_on="Ecoregion_ID")


## calculate coverage of ecoregion feature in MPA networks
summary_df["PCT Covered by MPA"] = (summary_df["MPA Coverage Area"] / summary_df["ER Area"]) * 100
summary_df["PCT Covered by FP MPA"] = (summary_df["FP-MPA Coverage Area"] / summary_df["ER Area"]) * 100


## calculate summary row
summary_df = summary_df.append(
    {'NAME': 'All Ecoregions',
     'Ecoregion_ID': '0',
     'ER Area': summary_df["ER Area"].sum(),
     'MPA Coverage Area': summary_df["MPA Coverage Area"].sum(),
     'FP-MPA Coverage Area': summary_df["FP-MPA Coverage Area"].sum(),
     'PCT Covered by MPA': summary_df["MPA Coverage Area"].sum() / summary_df["ER Area"].sum() * 100,
     'PCT Covered by FP MPA': summary_df["FP-MPA Coverage Area"].sum() / summary_df["ER Area"].sum() * 100,
     }, 
    ignore_index = True)


## clean up table
summary_df.fillna(0, inplace=True)
summary_df.set_index('Ecoregion_ID', inplace=True)
pd.set_option('display.float_format', lambda x: '%.3f' % x)
summary_df.sort_values(by=['ER Area'], inplace=True, ascending=False)

## output to CSV
summary_df.to_csv(r'V:\lenfest_nmsf_biodiversity\Data\_Scripts\coverage_ecoregion_MPA.csv')
