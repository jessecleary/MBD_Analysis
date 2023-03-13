
## Lenfest Biodiversity -IBA coverage
## coverage by Ecoregion
## coverage within MPAs by Ecoregion

import geopandas as gpd
import pandas as pd


## Ecoregion feature class
base_gdb =  r'V:\lenfest_nmsf_biodiversity\Data\lenfest_nmsf_base_prep.gdb'
ecoregion_base = gpd.read_file(f'{base_gdb}', layer='marine_ecoregions_final')
ecoregion_base["ER Area"] = (ecoregion_base["Shape_Area"] / (1000*1000))
ecoregion_base = ecoregion_base.drop(columns=["geometry","Shape_Length","Shape_Area"])


## CSVs to tables
all_output_csv = r'V:\lenfest_nmsf_biodiversity\Data\IBA\IBA_coverage_ecoregion.csv'
mpa_output_csv = r'V:\lenfest_nmsf_biodiversity\Data\IBA\IBA_coverage_MPA.csv'
fp_mpa_output_csv = r'V:\lenfest_nmsf_biodiversity\Data\IBA\IBA_coverage_FP_MPA.csv'

ecoregion_df = gpd.read_file(all_output_csv)
mpa_df = gpd.read_file(mpa_output_csv)
full_protect_mpa_df = gpd.read_file(fp_mpa_output_csv)


## rename area/percentage columns, drop columns
## drop columns and recalc below - checked that this matches the output from GPD intersect
ecoregion_df = ecoregion_df.apply(pd.to_numeric, errors='ignore')
ecoregion_df["IBA Area in ER"] = (ecoregion_df["iba_intersect_area"] / (1000*1000))
ecoregion_df = ecoregion_df.drop(columns=["field_1","geometry","NAME","Shape_Length_1","Shape_Area_1","Percent of Ecoregion Covered by IBA","iba_intersect_area"])

mpa_df = mpa_df.apply(pd.to_numeric, errors='ignore')
mpa_df["IBA Area in MPA"] = ( mpa_df["mpa_intersect_area"] / (1000*1000))
mpa_df = mpa_df.drop(columns=["field_1","geometry","NAME","Shape_Length_1","Shape_Area_1","mpa_intersect_area"])

full_protect_mpa_df = full_protect_mpa_df.apply(pd.to_numeric, errors='ignore')
full_protect_mpa_df["IBA Area in FP-MPA"] = (full_protect_mpa_df["fp_mpa_intersect_area"] / (1000*1000))
full_protect_mpa_df = full_protect_mpa_df.drop(columns=["field_1","geometry","NAME","Shape_Length_1","Shape_Area_1","fp_mpa_intersect_area"])


## join tables
summary_df = pd.merge(ecoregion_base, ecoregion_df, how="left", left_on="Ecoregion_ID", right_on="Ecoregion_ID")
summary_df = pd.merge(summary_df, mpa_df, how="left", left_on="Ecoregion_ID", right_on="Ecoregion_ID")
summary_df = pd.merge(summary_df, full_protect_mpa_df, how="left", left_on="Ecoregion_ID", right_on="Ecoregion_ID")


## calculate coverage of ecoregion feature in MPA networks
summary_df["PCT of ER Covered by IBA"] = (summary_df["IBA Area in ER"] / summary_df["ER Area"]) * 100
summary_df["PCT of ER IBA in MPA"] = (summary_df["IBA Area in MPA"] / summary_df["IBA Area in ER"]) * 100
summary_df["PCT of ER IBA in FP MPA"] = (summary_df["IBA Area in FP-MPA"] / summary_df["IBA Area in ER"]) * 100


## remove rows with no IBAs
summary_df = summary_df[summary_df['IBA Area in ER'].notna()]

## calculate summary row
summary_df = summary_df.append(
    {'NAME': 'All Ecoregions',
     'Ecoregion_ID': '0',
     'ER Area': summary_df["ER Area"].sum(),
     'IBA Area in ER': summary_df["IBA Area in ER"].sum(),
     'IBA Area in MPA': summary_df["IBA Area in MPA"].sum(),
     'IBA Area in FP-MPA': summary_df["IBA Area in FP-MPA"].sum(),
     'PCT of ER Covered by IBA': summary_df["IBA Area in ER"].sum() / summary_df["ER Area"].sum() * 100,
     'PCT of ER IBA in MPA': summary_df["IBA Area in MPA"].sum() / summary_df["IBA Area in ER"].sum() * 100,
     'PCT of ER IBA in FP MPA': summary_df["IBA Area in FP-MPA"].sum() / summary_df["IBA Area in ER"].sum() * 100
     }, 
    ignore_index = True)


## clean up table
summary_df.sort_values(by=['IBA Area in ER'], inplace=True, ascending=False)
summary_df.fillna("--", inplace=True)
summary_df.set_index('Ecoregion_ID', inplace=True)
pd.set_option('display.float_format', lambda x: '%.3f' % x)


## output to CSV
summary_df.to_csv(r'V:\lenfest_nmsf_biodiversity\Data\_Scripts\iba_coverage_ecoregion_MPA.csv')
