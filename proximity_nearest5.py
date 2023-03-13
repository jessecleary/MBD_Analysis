
## Proximity for nearest 5 MPAs from Near Table analysis in AGP

import pandas as pd
import geopandas as gpd

project_gdb = r'V:/lenfest_nmsf_biodiversity/Data/lenfest_nmsf_results.gdb'
base_gdb = r'V:/lenfest_nmsf_biodiversity/Data/lenfest_nmsf_base_prep.gdb'


## MPA results 
near_table_df = gpd.read_file(f'{project_gdb}', layer='MPAI2020_NearTable')
near_table_df = near_table_df[near_table_df['NEAR_DIST'] > 0]

five_near_df = near_table_df.sort_values('NEAR_DIST').groupby('IN_FID', as_index=False).head(5)
five_near_df_fid_mean = five_near_df.groupby('IN_FID')['NEAR_DIST'].agg(['mean', 'count'])
five_near_df_fid_mean = five_near_df_fid_mean[five_near_df_fid_mean['count'] > 1]
us_mean_five_near_distance = five_near_df_fid_mean['mean'].mean() / 1000
us_std_five_near_distance = five_near_df_fid_mean['mean'].std() / 1000
us_med_five_near_distance = five_near_df_fid_mean['mean'].median() / 1000

## FP MPA results 
fp_near_table_df = gpd.read_file(f'{project_gdb}', layer='MPAI2020_Full_Protect_NearTable')
fp_near_table_df = fp_near_table_df[fp_near_table_df['NEAR_DIST'] > 0]

fp_five_near_df = fp_near_table_df.sort_values('NEAR_DIST').groupby('IN_FID', as_index=False).head(5)
fp_five_near_df_fid_mean = fp_five_near_df.groupby('IN_FID')['NEAR_DIST'].agg(['mean', 'count'])
fp_five_near_df_fid_mean = fp_five_near_df_fid_mean[fp_five_near_df_fid_mean['count'] > 1]
us_mean_fp_five_near_distance = fp_five_near_df_fid_mean['mean'].mean() / 1000
us_std_fp_five_near_distance = fp_five_near_df_fid_mean['mean'].std() / 1000
us_med_fp_five_near_distance = fp_five_near_df_fid_mean['mean'].median() / 1000

## store results
temp_list = [] 
temp_list.append(
    {
        "Ecoregion_ID": 0,
        "MPA_Near5_Mean": us_mean_five_near_distance,
        "FP_MPA_Near5_Mean": us_mean_fp_five_near_distance
    })


## Calc for Ecoregions
for ecoregion_id in range(1,25):

    ## MPA results 
    er_near_table_df = gpd.read_file(f'{project_gdb}', layer=f'ER_{ecoregion_id}_MPAI2020_Proj_NearTable')
    if er_near_table_df.shape[0] == 0:
        er_mean_five_near_distance = "--"
    else:
        er_near_table_df = er_near_table_df[er_near_table_df['NEAR_DIST'] > 0]
    
        er_five_near_df = er_near_table_df.sort_values('NEAR_DIST').groupby('IN_FID', as_index=False).head(5)
        er_five_near_df_fid_mean = er_five_near_df.groupby('IN_FID')['NEAR_DIST'].agg(['mean', 'count'])
        er_five_near_df_fid_mean = er_five_near_df_fid_mean[er_five_near_df_fid_mean['count'] > 1]
        er_mean_five_near_distance = er_five_near_df_fid_mean['mean'].mean() / 1000

    ## FP MPA results 
    er_fp_near_table_df = gpd.read_file(f'{project_gdb}', layer=f'ER_{ecoregion_id}_MPAI2020_Proj_Full_Protect_NearTable')
    if er_fp_near_table_df.shape[0] == 0:
        er_mean_fp_five_near_distance = "--"
    else:
        er_fp_near_table_df = er_fp_near_table_df[er_fp_near_table_df['NEAR_DIST'] > 0]
    
        er_fp_five_near_df = er_fp_near_table_df.sort_values('NEAR_DIST').groupby('IN_FID', as_index=False).head(5)
        er_fp_five_near_df_fid_mean = er_fp_five_near_df.groupby('IN_FID')['NEAR_DIST'].agg(['mean', 'count'])
        er_fp_five_near_df_fid_mean = er_fp_five_near_df_fid_mean[er_fp_five_near_df_fid_mean['count'] > 1]
        er_mean_fp_five_near_distance = er_fp_five_near_df_fid_mean['mean'].mean() / 1000
    
    temp_list.append(
    {
        "Ecoregion_ID": ecoregion_id,
        "MPA_Near5_Mean": er_mean_five_near_distance,
        "FP_MPA_Near5_Mean": er_mean_fp_five_near_distance
    })
    
## create summary dataframe
proximity_df = pd.DataFrame(temp_list)


## Ecoregion file to get names, add "All Ecoregions" name
ecoregion_df = gpd.read_file(f'{base_gdb}', layer='marine_ecoregions_final') 
ecoregion_df.drop(['geometry','Shape_Length','Shape_Area'], axis=1, inplace=True)
summary_df = proximity_df.merge(ecoregion_df, left_on="Ecoregion_ID", right_on="Ecoregion_ID", how="left")
summary_df.at[0,'NAME'] = "All Ecoregions"

summary_df.fillna("--", inplace=True)
summary_df.set_index('Ecoregion_ID', inplace=True)


## output to CSV
summary_df.to_csv(r'V:\lenfest_nmsf_biodiversity\Data\_Scripts\proximity_nearest5.csv')
