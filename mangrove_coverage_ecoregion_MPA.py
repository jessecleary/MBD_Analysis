
## Lenfest Biodiversity - Mangroves
## coverage by Ecoregion
## coverage within MPAs by Ecoregion


import geopandas as gpd
import pandas as pd


## Ecoregion feature class
base_gdb =  r'V:\lenfest_nmsf_biodiversity\Data\lenfest_nmsf_base_prep.gdb'
ecoregion_base = gpd.read_file(f'{base_gdb}', layer='marine_ecoregions_final')
ecoregion_base["ER Area"] = (ecoregion_base["Shape_Area"] / (1000*1000))
ecoregion_base = ecoregion_base.drop(columns=["geometry","Shape_Length","Shape_Area"])


## Coverage tables
project_gdb = r'V:\lenfest_nmsf_biodiversity\Data\lenfest_nmsf_results.gdb'
ecoregion_df = gpd.read_file(f'{project_gdb}', layer='mangrove_coverage_ecoregion') 
mpa_df = gpd.read_file(f'{project_gdb}', layer='mangrove_coverage_ecoregion_mpa')
full_protect_mpa_df = gpd.read_file(f'{project_gdb}', layer='mangrove_coverage_ecoregion_full_protect_mpa')


## rename area/percentage columns, drop columns
## drop percentage column and recalc below - checked that this matches the output from ArcPro
ecoregion_df = ecoregion_df.rename(index=str, columns={"AREA":"Mangrove Area in ER"})
ecoregion_df = ecoregion_df.drop(columns=["geometry","PERCENTAGE"])

mpa_df = mpa_df.rename(index=str, columns={"AREA":"Mangrove Area in MPA"})
mpa_df = mpa_df.drop(columns=["geometry","PERCENTAGE"])

full_protect_mpa_df = full_protect_mpa_df.rename(index=str, columns={"AREA":"Mangrove Area in FP-MPA"})
full_protect_mpa_df = full_protect_mpa_df.drop(columns=["geometry","PERCENTAGE"])


## join tables
summary_df = pd.merge(ecoregion_base, ecoregion_df, how="left", left_on="Ecoregion_ID", right_on="Ecoregion_ID")
summary_df = pd.merge(summary_df, mpa_df, how="left", left_on="Ecoregion_ID", right_on="Ecoregion_ID")
summary_df = pd.merge(summary_df, full_protect_mpa_df, how="left", left_on="Ecoregion_ID", right_on="Ecoregion_ID")


## calculate coverage of ecoregion feature in MPA networks
summary_df["PCT of ER Covered by Mangrove"] = (summary_df["Mangrove Area in ER"] / summary_df["ER Area"]) * 100
summary_df["PCT of ER Mangrove in MPA"] = (summary_df["Mangrove Area in MPA"] / summary_df["Mangrove Area in ER"]) * 100
summary_df["PCT of ER Mangrove in FP MPA"] = (summary_df["Mangrove Area in FP-MPA"] / summary_df["Mangrove Area in ER"]) * 100


## remove rows with no Mangroves
summary_df = summary_df[summary_df['Mangrove Area in ER'].notna()]

## calculate summary row
summary_df = summary_df.append(
    {'NAME': 'All Ecoregions',
     'Ecoregion_ID': '0',
     'ER Area': summary_df["ER Area"].sum(),
     'Mangrove Area in ER': summary_df["Mangrove Area in ER"].sum(),
     'Mangrove Area in MPA': summary_df["Mangrove Area in MPA"].sum(),
     'Mangrove Area in FP-MPA': summary_df["Mangrove Area in FP-MPA"].sum(),
     'PCT of ER Covered by Mangrove': summary_df["Mangrove Area in ER"].sum() / summary_df["ER Area"].sum() * 100,
     'PCT of ER Mangrove in MPA': summary_df["Mangrove Area in MPA"].sum() / summary_df["Mangrove Area in ER"].sum() * 100,
     'PCT of ER Mangrove in FP MPA': summary_df["Mangrove Area in FP-MPA"].sum() / summary_df["Mangrove Area in ER"].sum() * 100
     }, 
    ignore_index = True)
    

## clean up table
summary_df.sort_values(by=['Mangrove Area in ER'], inplace=True, ascending=False)
summary_df.fillna("--", inplace=True)
summary_df.set_index('Ecoregion_ID', inplace=True)
pd.set_option('display.float_format', lambda x: '%.4f' % x)

## output to CSV
summary_df.to_csv(r'V:\lenfest_nmsf_biodiversity\Data\_Scripts\mangrove_coverage_ecoregion_MPA.csv')
