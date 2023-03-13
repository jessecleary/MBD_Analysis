# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 12:36:22 2021

@author: sed45
"""

import geopandas as gpd
import pandas as pd


project_gdb = r'M:\lenfest_nmsf_biodiversity\Data\SD_Project\SD_Project.gdb'

ecoregion_df = gpd.read_file(f'{project_gdb}', layer='YessonConsensus_Ecoregion_Area') 
mpa_df = gpd.read_file(f'{project_gdb}', layer='YessonConsensus_MPA_area')
full_protect_mpa_df = gpd.read_file(f'{project_gdb}', layer='YessonConsensus_MPAfullprotect_area')

# reference layers
ref_gdb = r'M:\lenfest_nmsf_biodiversity\Data\lenfest_nmsf_base_prep.gdb'
ecoregions = gpd.read_file(f'{ref_gdb}', layer='marine_ecoregions_final')
mpas = gpd.read_file(f'{ref_gdb}', layer='noaa_mpai_ecoregion_final')
mpas_fullprotect = gpd.read_file(f'{ref_gdb}', layer='noaa_mpai_full_protect_ecoregion_final')

ecoreg_merge = pd.merge(ecoregion_df, ecoregions, how = 'left', left_on = 'ECOREGION_ID', right_on = 'Ecoregion_ID')
#mpa_merge = pd.merge(mpa_df, mpas, how = 'left', left_on = 'ECOREGION_ID', right_on = 'Ecoregion_ID')
#mpa_fp_merge = pd.merge(full_protect_mpa_df, mpas_fullprotect, how = 'left', left_on = 'ECOREGION_ID', right_on = 'Ecoregion_ID')

ecoreg_merge['Ecoregion_Area_Percent'] = (ecoreg_merge['VALUE_3']/ecoreg_merge['Shape_Area'])*100
#mpa_merge['MPA_Area_Percent'] = (mpa_merge['VALUE_3']/ecoreg_merge['Shape_Area'])*100
#mpa_fp_merge['FullProtect_MPA_Area_Percent'] = (mpa_fp_merge['VALUE_3']/ecoreg_merge['Shape_Area'])*100

ecoreg_df = ecoreg_merge.rename(index = str, columns = {'Shape_Area':'ER Area', 'VALUE_3':'CWC Habitat Area in ER', 'Ecoregion_Area_Percent':'PCT of ER Covered by CWC Habitat'})
ecoreg_df = ecoreg_df.drop(columns = ['VALUE_1', 'VALUE_2', 'geometry_x', 'Shape_Length', 'ECOREGION_ID', 'geometry_y'])
ecoreg_df['ER Area'] = ecoreg_df['ER Area']/1000000
ecoreg_df['CWC Habitat Area in ER'] = ecoreg_df['CWC Habitat Area in ER']/1000000

mpa_df = mpa_df.rename(index = str, columns = {'VALUE_3':'CWC Habitat Area in MPA'})
mpa_df = mpa_df.drop(columns = ['VALUE_1', 'VALUE_2', 'geometry'])
mpa_df['CWC Habitat Area in MPA'] = mpa_df['CWC Habitat Area in MPA']/1000000

mpafp_df = full_protect_mpa_df.rename(index = str, columns = {'VALUE_3':'CWC Habitat Area in FP-MPA'})
mpafp_df = mpafp_df.drop(columns = ['VALUE_1', 'VALUE_2', 'geometry'])
mpafp_df['CWC Habitat Area in FP-MPA'] = mpafp_df['CWC Habitat Area in FP-MPA']/1000000

summary_df = pd.merge(ecoreg_df, mpa_df, how="left", left_on="Ecoregion_ID", right_on="ECOREGION_ID")
summary_df = pd.merge(summary_df, mpafp_df, how="left", left_on="Ecoregion_ID", right_on="ECOREGION_ID")

summary_df["PCT of ER CWC Habitat in MPA"] = (summary_df["CWC Habitat Area in MPA"] / summary_df["CWC Habitat Area in ER"]) * 100
summary_df["PCT of ER CWC Habitat in FP-MPA"] = (summary_df["CWC Habitat Area in FP-MPA"] / summary_df["CWC Habitat Area in ER"]) * 100
summary_df = summary_df.drop(columns = ['ECOREGION_ID_x', 'ECOREGION_ID_y'])

## calculate summary row
summary_df = summary_df.append(
    {'NAME': 'All Ecoregions',
     'Ecoregion_ID': 0,
     'ER Area': summary_df["ER Area"].sum(),
     'CWC Habitat Area in ER': summary_df["CWC Habitat Area in ER"].sum(),
     'CWC Habitat Area in MPA': summary_df["CWC Habitat Area in MPA"].sum(),
     'CWC Habitat Area in FP-MPA': summary_df["CWC Habitat Area in FP-MPA"].sum(),
     'PCT of ER Covered by CWC Habitat': summary_df["CWC Habitat Area in ER"].sum() / summary_df["ER Area"].sum() * 100,
     'PCT of ER CWC Habitat in MPA': summary_df["CWC Habitat Area in MPA"].sum() / summary_df["CWC Habitat Area in ER"].sum() * 100,
     'PCT of ER CWC Habitat in FP-MPA': summary_df["CWC Habitat Area in FP-MPA"].sum() / summary_df["CWC Habitat Area in ER"].sum() * 100
     }, 
    ignore_index = True)

summary_df.fillna("--", inplace=True)
summary_df.set_index('Ecoregion_ID', inplace=True)
pd.set_option('display.float_format', lambda x: '%.3f' % x)
summary_df = summary_df.sort_values('Ecoregion_ID')

## remove rows with no Mangroves
summary_df = summary_df[summary_df['CWC Habitat Area in ER'].notna()]

summary_df = summary_df[['NAME',
  'PCT of ER Covered by CWC Habitat', 'PCT of ER CWC Habitat in MPA',
 'PCT of ER CWC Habitat in FP-MPA']]

summary_df.to_csv(r'M:\lenfest_nmsf_biodiversity\Data\SD_Project\Scripts\yesson_coverage_ecoregion_MPA_reducedcols.csv')
