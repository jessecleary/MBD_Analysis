
## Summarize US OBIS shapefiles for each ecoregion and ecoregion MPAs
## Compare with NEMESIS Species lists

import geopandas as gpd
import pandas as pd
import numpy as np
from os import path

## paths
shapefile_path = r"V:\lenfest_nmsf_biodiversity\Data\OBIS\Occurrences\US_OBIS_Ecoregions"

## read in ecoregions and MPAs
project_gdb = r'V:\lenfest_nmsf_biodiversity\Data\lenfest_nmsf_base_prep.gdb'
ecoregion_df = gpd.read_file(f'{project_gdb}', layer='marine_ecoregions_final') 

## set index to be Ecoregion_ID
ecoregion_df.set_index('Ecoregion_ID', inplace=True)


## empty list for results
temp_list = []

## iterate over ecoregions and MPAs, FP MPAs in ecoregions
for ecoregion_id, row in ecoregion_df.iterrows():
    #if ecoregion_id != 1: continue

    print(ecoregion_id)
    
    ## ER calcs    
    obis_er_temp = gpd.read_file(f'{shapefile_path}/OBIS_ER_{ecoregion_id}.shp')
    er_observations = obis_er_temp.shape[0]
    er_datasets = len(pd.unique(obis_er_temp['datasetID']))
            
    er_species = len(pd.unique(obis_er_temp['aphiaID']))


    ## Read regional NEMESIS list
    if ecoregion_id in [1,9,12,18,23]:
        nemesis_df = pd.read_csv(r'V:/lenfest_nmsf_biodiversity/Data/OBIS/Occurrences/NEMESIS_Lists/East_Coast_Taxa.csv')
    
    elif ecoregion_id in [10,16,21,2,7,3]:
        nemesis_df = pd.read_csv(r'V:/lenfest_nmsf_biodiversity/Data/OBIS/Occurrences/NEMESIS_Lists/West_Coast_Taxa.csv')
    
    elif ecoregion_id in [17,22,20]:
        nemesis_df = pd.read_csv(r'V:/lenfest_nmsf_biodiversity/Data/OBIS/Occurrences/NEMESIS_Lists/Gulf_Coast_Taxa.csv')
    
    else:
        print(ecoregion_id,"No NEMESIS file for this ER")
        
        temp_list.append(
        {
            "Ecoregion_ID": ecoregion_id,
            "NAME": row.NAME,
            "ER_Species": er_species,
            "ER_NEMESIS_Obs": np.NaN,
            "ER_NEMESIS_Species": np.NaN,
            "MPA_NEMESIS_Obs": np.NaN,
            "MPA_NEMESIS_Species": np.NaN,            
            "FP_MPA_NEMESIS_Obs": np.NaN,
            "FP_MPA_NEMESIS_Species": np.NaN
        })
        
        continue
    
    ## join with ER obs    
    invasive_er_df = obis_er_temp.merge(nemesis_df, left_on="scientific", right_on="TXA_Binomial", how="inner")
    invasive_er = invasive_er_df.shape[0]
    invasive_species = len(pd.unique(invasive_er_df['aphiaID']))
    
    ## MPA calcs, test existence
    if path.exists(f'{shapefile_path}/OBIS_ER_MPA_{ecoregion_id}.shp'):

        obis_mpa_temp = gpd.read_file(f'{shapefile_path}/OBIS_ER_MPA_{ecoregion_id}.shp')
        er_mpa_observations = obis_mpa_temp.shape[0]  
        er_mpa_datasets = len(pd.unique(obis_mpa_temp['datasetID']))

        er_mpa_species = len(pd.unique(obis_mpa_temp['aphiaID']))
        
        ## join with ER MPA obs
        invasive_mpa_df = obis_mpa_temp.merge(nemesis_df, left_on="scientific", right_on="TXA_Binomial", how="inner")
        invasive_mpa = invasive_mpa_df.shape[0]
        invasive_mpa_species = len(pd.unique(invasive_mpa_df['aphiaID']))
    else:
        invasive_mpa = np.NaN
        invasive_mpa_species = np.NaN

    ## FP MPA calcs, test existence
    if path.exists(f'{shapefile_path}/OBIS_ER_FP_MPA_{ecoregion_id}.shp'):

        obis_fp_mpa_temp = gpd.read_file(f'{shapefile_path}/OBIS_ER_FP_MPA_{ecoregion_id}.shp')
        er_fp_mpa_observations = obis_fp_mpa_temp.shape[0]  
        er_fp_mpa_datasets = len(pd.unique(obis_fp_mpa_temp['datasetID']))
        
        er_fp_mpa_species = len(pd.unique(obis_fp_mpa_temp['aphiaID']))

        ## join with ER FP MPA obs
        invasive_fp_mpa_df = obis_fp_mpa_temp.merge(nemesis_df, left_on="scientific", right_on="TXA_Binomial", how="inner")
        invasive_fp_mpa = invasive_fp_mpa_df.shape[0]
        invasive_fp_mpa_species = len(pd.unique(invasive_fp_mpa_df['aphiaID']))
    else:
        invasive_fp_mpa = np.NaN
        invasive_fp_mpa_species = np.NaN
    
    ## add to temp list
    temp_list.append(
            {
                "Ecoregion_ID": ecoregion_id,
                "NAME": row.NAME,
                "ER_Species": er_species,
                "ER_NEMESIS_Obs": invasive_er,
                "ER_NEMESIS_Species": invasive_species,
                "MPA_NEMESIS_Obs": invasive_mpa,
                "MPA_NEMESIS_Species": invasive_mpa_species, 
                "FP_MPA_NEMESIS_Obs": invasive_fp_mpa,
                "FP_MPA_NEMESIS_Species": invasive_fp_mpa_species
            })

## create summary dataframe
summary_df = pd.DataFrame(temp_list)
summary_df.to_csv(r'V:/lenfest_nmsf_biodiversity/Data/_Scripts/OBIS_NEMESIS_ecoregion.csv')
