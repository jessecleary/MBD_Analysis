# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 03:31:48 2021

@author: sed45
"""
# joining habitat tables into one csv file

import geopandas as gpd
import pandas as pd


project_gdb = r'M:\lenfest_nmsf_biodiversity\Data\SD_Project\tables'

# define habitat dataframes
seagrass_df = gpd.read_file(f'{project_gdb}\seagrass_coverage_ecoregion_MPA.csv')
mangrove_df = gpd.read_file(f'{project_gdb}\mangrove_coverage_ecoregion_MPA.csv')

coral_df = gpd.read_file(f'{project_gdb}\coral_reef_coverage_ecoregion_MPA.csv')

cwc_df = gpd.read_file(f'{project_gdb}\yesson_coverage_ecoregion_MPA_reducedcols.csv')

ec_mammal = gpd.read_file(f'{project_gdb}\mammal_coverage_ecoregion_MPA_reducedcols.csv')

ec_avian = gpd.read_file(f'{project_gdb}\\avian_coverage_ecoregion_MPA_reducedcols.csv')


# merge into habitat dataframe
hab_df = pd.merge(cwc_df, seagrass_df, how = 'left', on = ['Ecoregion_ID','NAME'])
hab_df = pd.merge(hab_df, mangrove_df, how = 'left', on = ['Ecoregion_ID','NAME'])
hab_df = pd.merge(hab_df, coral_df, how = 'left', on = ['Ecoregion_ID','NAME'])
hab_df = pd.merge(hab_df, ec_mammal, how = 'left', on = ['Ecoregion_ID','NAME'])
hab_df = pd.merge(hab_df, ec_avian, how = 'left', on = ['Ecoregion_ID','NAME'])

hab_df.to_csv(r'M:\lenfest_nmsf_biodiversity\Data\SD_Project\tables\habitat_coverage.csv')

cols = list(hab_df.columns.values)
hab_df = hab_df[['Ecoregion_ID','NAME','PCT of ER Covered by CWC Habitat','PCT of ER CWC Habitat in MPA','PCT of ER CWC Habitat in FP-MPA','PCT of ER Covered by Seagrass','PCT of ER Seagrass in MPA','PCT of ER Seagrass in FP MPA','PCT of ER Covered by Mangrove','PCT of ER Mangrove in MPA','PCT of ER Mangrove in FP MPA','PCT of ER Covered by CR','PCT of ER CR in MPA','PCT of ER CR in FP MPA','PCT of ER Covered by Cetacean Presence','PCT of ER Cetacean Presence in MPA','PCT of ER Cetacean Presence in FP-MPA','ER Area','PCT of ER Covered by Avian Presence','PCT of ER Avian Presence in MPA','PCT of ER Avian Presence in FP-MPA']]

hab_df.to_csv(r'M:\lenfest_nmsf_biodiversity\Data\SD_Project\tables\habitat_coverage_percents.csv')

