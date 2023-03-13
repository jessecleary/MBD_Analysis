
## Read US OBIS shapefiles for each ecoregion and ecoregion MPAs, FP-MPAs
## Compare with RedList Species

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


## RedList Status CSVs from GBIF - https://www.gbif.org/dataset/19491596-35ae-4a91-9a98-85cf505f1bd3
taxon_df = pd.read_csv(r'V:\lenfest_nmsf_biodiversity\Data\OBIS\Occurrences\iucn-2020-3\taxon.txt', sep='\t')
taxon_df = taxon_df.astype({'taxonID': 'int64'})

status_df = pd.read_csv(r'V:\lenfest_nmsf_biodiversity\Data\OBIS\Occurrences\iucn-2020-3\distribution.txt', sep='\t')

redlist_df = taxon_df.merge(status_df, left_on="taxonID", right_on="taxonID", how="inner")
redlist_df = redlist_df[["taxonID", "scientificName", "threatStatus"]]

## clean up Scientific Names for OBIS matching
redlist_df['GenusSpecies'] = redlist_df.scientificName.apply(lambda x: pd.Series(' '.join(map(str, x.split(" ")[0:2]))))
redlist_df = redlist_df[redlist_df['threatStatus'].isin(["Vulnerable", "Endangered", "Critically Endangered"])]


## empty list for results
temp_list = []

## iterate over ecoregions and MPAs, FP MPAs in ecoregions
for ecoregion_id, row in ecoregion_df.iterrows():
    #if ecoregion_id != 1: continue

    #print(ecoregion_id)
    
    ## ER calcs    
    obis_er_temp = gpd.read_file(f'{shapefile_path}/OBIS_ER_{ecoregion_id}.shp')
    er_observations = obis_er_temp.shape[0]
    er_datasets = len(pd.unique(obis_er_temp['datasetID']))
            
    er_species = len(pd.unique(obis_er_temp['aphiaID']))

    ## join with ER obs  
    redlist_er_df = obis_er_temp.merge(redlist_df, left_on="scientific", right_on="GenusSpecies", how="inner")
    redlist_er = redlist_er_df.shape[0]
    redlist_er_species = len(pd.unique(redlist_er_df['aphiaID']))
    
    ## MPA calcs, test existence
    if path.exists(f'{shapefile_path}/OBIS_ER_MPA_{ecoregion_id}.shp'):

        obis_mpa_temp = gpd.read_file(f'{shapefile_path}/OBIS_ER_MPA_{ecoregion_id}.shp')
        er_mpa_observations = obis_mpa_temp.shape[0]  
        er_mpa_datasets = len(pd.unique(obis_mpa_temp['datasetID']))

        er_mpa_species = len(pd.unique(obis_mpa_temp['aphiaID']))
              
        redlist_mpa_df = obis_mpa_temp.merge(redlist_df, left_on="scientific", right_on="GenusSpecies", how="inner")
        redlist_mpa = redlist_mpa_df.shape[0]
        redlist_mpa_species = len(pd.unique(redlist_mpa_df['aphiaID']))
    else:
        redlist_mpa = np.NaN 
        redlist_mpa_species = np.NaN 
        

    ## FP MPA calcs, test existence
    if path.exists(f'{shapefile_path}/OBIS_ER_FP_MPA_{ecoregion_id}.shp'):

        obis_fp_mpa_temp = gpd.read_file(f'{shapefile_path}/OBIS_ER_FP_MPA_{ecoregion_id}.shp')
        er_fp_mpa_observations = obis_fp_mpa_temp.shape[0]  
        er_fp_mpa_datasets = len(pd.unique(obis_fp_mpa_temp['datasetID']))
        
        er_fp_mpa_species = len(pd.unique(obis_fp_mpa_temp['aphiaID']))

        redlist_fp_mpa_df = obis_fp_mpa_temp.merge(redlist_df, left_on="scientific", right_on="GenusSpecies", how="inner")
        redlist_fp_mpa = redlist_fp_mpa_df.shape[0]
        redlist_fp_mpa_species = len(pd.unique(redlist_fp_mpa_df['aphiaID']))
    else:
        redlist_fp_mpa = np.NaN
        redlist_fp_mpa_species = np.NaN
        
    ## add to temp list 
    temp_list.append(
            {
                "Ecoregion_ID": ecoregion_id,
                "NAME": row.NAME,
                "ER_Species": er_species,
                "ER_RedList_Obs": redlist_er,
                "ER_RedList_Species": redlist_er_species,
                "MPA_RedList_Obs": redlist_mpa,
                "MPA_RedList_Species": redlist_mpa_species,
                "FP_MPA_RedList_Obs": redlist_fp_mpa,
                "FP_MPA_RedList_Species": redlist_fp_mpa_species
            })
    
    
    

## US EEZ calcs 
## CSV is a subset of the fill OBIS CSV, select columsn and subset to our Ecoregions

obis_csv_file = r"V:\lenfest_nmsf_biodiversity\Data\OBIS\Occurrences\US_OBIS_CSV\us_obis_ecoregions.csv"

## look at organization - columns and data types
sample = pd.read_csv(obis_csv_file, nrows=100)
dtypes = sample.dtypes 
columns = sample.columns 

## read a subset by columns
cols=["scientificName","eventDate","date_year","decimalLongitude", "decimalLatitude", "datasetID", "aphiaID","node_id","taxonRank","kingdom","phylum","class","order","family", "genus", "species"]
obis_er_temp = pd.read_csv(obis_csv_file, usecols=cols)

## calcs
er_observations = obis_er_temp.shape[0]
er_datasets = len(pd.unique(obis_er_temp['datasetID']))
        
er_species = len(pd.unique(obis_er_temp['aphiaID']))

## join with ER obs  
redlist_er_df = obis_er_temp.merge(redlist_df, left_on="scientificName", right_on="GenusSpecies", how="inner")
redlist_er = redlist_er_df.shape[0]
redlist_er_species = len(pd.unique(redlist_er_df['aphiaID']))


## MPA calcs
obis_mpa_temp = gpd.read_file(f'{shapefile_path}/OBIS_All_MPA.shp')
er_mpa_observations = obis_mpa_temp.shape[0]  
er_mpa_datasets = len(pd.unique(obis_mpa_temp['datasetID']))
er_mpa_species = len(pd.unique(obis_mpa_temp['aphiaID']))
      
redlist_mpa_df = obis_mpa_temp.merge(redlist_df, left_on="scientific", right_on="GenusSpecies", how="inner")
redlist_mpa = redlist_mpa_df.shape[0]
redlist_mpa_species = len(pd.unique(redlist_mpa_df['aphiaID']))
    

## FP MPA calcs
obis_fp_mpa_temp = gpd.read_file(f'{shapefile_path}/OBIS_All_FP_MPA.shp')
er_fp_mpa_observations = obis_fp_mpa_temp.shape[0]  
er_fp_mpa_datasets = len(pd.unique(obis_fp_mpa_temp['datasetID']))
er_fp_mpa_species = len(pd.unique(obis_fp_mpa_temp['aphiaID']))

redlist_fp_mpa_df = obis_fp_mpa_temp.merge(redlist_df, left_on="scientific", right_on="GenusSpecies", how="inner")
redlist_fp_mpa = redlist_fp_mpa_df.shape[0]
redlist_fp_mpa_species = len(pd.unique(redlist_fp_mpa_df['aphiaID']))

    
## add to temp list 
temp_list.append(
        {
            "Ecoregion_ID": 0,
            "NAME": "All Ecoregions",
            "ER_Species": er_species,
            "ER_RedList_Obs": redlist_er,
            "ER_RedList_Species": redlist_er_species,
            "MPA_RedList_Obs": redlist_mpa,
            "MPA_RedList_Species": redlist_mpa_species,
            "FP_MPA_RedList_Obs": redlist_fp_mpa,
            "FP_MPA_RedList_Species": redlist_fp_mpa_species
        })


## create summary dataframe
summary_df = pd.DataFrame(temp_list)
summary_df.to_csv(r'V:/lenfest_nmsf_biodiversity/Data/_Scripts/OBIS_RedList_ecoregion.csv')

