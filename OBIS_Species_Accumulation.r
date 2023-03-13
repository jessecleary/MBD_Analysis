
## species accumulation curves
## example from https://obis.org/manual/processing_old/


require(dplyr)
require(ggplot2)
require(readr)
require(vegan)
library(sf)


## full dataset

data_start <- read_csv("V:/lenfest_nmsf_biodiversity/Data/OBIS/Occurrences/US_OBIS_CSV/us_obis.csv", 
                 #n_max=100000, 
                 progress = show_progress(),
                 col_types=cols_only(date_year=col_integer(), taxonRank=col_character(), aphiaID=col_integer(), species=col_character())
                 )            

#data_all <- data_start %>% filter(!is.na(species) & !is.na(date_year) & (taxonRank=="Species" | taxonRank=="species" | taxonRank=="SPECIES"))

data_all <- data_start %>% filter(!is.na(species) & !is.na(date_year))

currentyear <- as.numeric(format(Sys.Date(), "%Y"))
data_all$year2 <- factor(data_all$date_year, levels=seq(1900, currentyear))

t_all <- xtabs(~ year2 + species, data=data_all)
acc_all <- specaccum(t_all)
specpool(t_all)

accdf_all <- data.frame(richness=acc_all$richness, sd=acc_all$sd, years=acc_all$sites)




## All US MPAs

mpa_shapefile_path = "V:/lenfest_nmsf_biodiversity/Data/OBIS/Occurrences/US_OBIS_Ecoregions/OBIS_All_MPA.shp"
mpa_obs <- st_read(mpa_shapefile_path)


#data_mpa <- mpa_obs %>% filter(!is.na(species) & !is.na(date_year) & (taxonRank=="Species" | taxonRank=="species" | taxonRank=="SPECIES"))
data_mpa <- mpa_obs %>% filter(!is.na(species) & !is.na(date_year))

currentyear <- as.numeric(format(Sys.Date(), "%Y"))
data_mpa$year2 <- factor(data_mpa$date_year, levels=seq(1900, currentyear))

t_mpa <- xtabs(~ year2 + species, data=data_mpa)
acc_mpa <- specaccum(t_mpa)
specpool(t_mpa)

accdf_mpa <- data.frame(richness=acc_mpa$richness, sd=acc_mpa$sd, years=acc_mpa$sites)



## All US FP MPAs
fp_mpa_shapefile_path = "V:/lenfest_nmsf_biodiversity/Data/OBIS/Occurrences/US_OBIS_Ecoregions/OBIS_All_FP_MPA.shp"
fp_mpa_obs <- st_read(fp_mpa_shapefile_path)

#data_fp_mpa <- fp_mpa_obs %>% filter(!is.na(species) & !is.na(date_year) & (taxonRank=="Species" | taxonRank=="species" | taxonRank=="SPECIES"))
data_fp_mpa <- fp_mpa_obs %>% filter(!is.na(species) & !is.na(date_year))

currentyear <- as.numeric(format(Sys.Date(), "%Y"))
data_fp_mpa$year2 <- factor(data_fp_mpa$date_year, levels=seq(1900, currentyear))

t_fp_mpa <- xtabs(~ year2 + species, data=data_fp_mpa)
acc_fp_mpa <- specaccum(t_fp_mpa)
specpool(t_fp_mpa)

accdf_fp_mpa <- data.frame(richness=acc_fp_mpa$richness, sd=acc_fp_mpa$sd, years=acc_fp_mpa$sites)

# 
# ggplot() + 
#   geom_ribbon(data=accdf_all, aes(x=years, ymin=richness-sd, ymax=richness+sd, fill="All"), alpha=0.7) +
#   geom_line(data=accdf_all, aes(x=years, y=richness)) +
#   geom_ribbon(data=accdf_mpa, aes(x=years, ymin=richness-sd, ymax=richness+sd, fill="MPA"), alpha=0.7) +
#   geom_line(data=accdf_mpa, aes(x=years, y=richness)) +
#   geom_ribbon(data=accdf_fp_mpa, aes(x=years, ymin=richness-sd, ymax=richness+sd, fill="FP MPA"), alpha=0.7) +
#   geom_line(data=accdf_fp_mpa, aes(x=years, y=richness)) +
#   xlab("Samples") +
#   ylab("Species Richness") +
#   labs(title = "Species Accumulation Curves: OBIS Observations in US EEZ, MPAs, and FP MPAs") +
#   scale_fill_manual(name="OBIS Observations", values=c("All"="steelblue","MPA"="aquamarine4","FP MPA"="darkorange"), 
#                     labels=c("All"="All Observations","MPA"="MPA Observations","FP MPA"="Fully Protected MPA Observations"))


## export acc dfs to CSVs

write.csv(accdf_all, file='V:/lenfest_nmsf_biodiversity/Graphics_Manuscript/Plot_CSV_v2/Fig_Data_OBIS_acc_all.csv')
write.csv(accdf_mpa, file='V:/lenfest_nmsf_biodiversity/Graphics_Manuscript/Plot_CSV_v2/Fig_Data_OBIS_acc_mpa.csv')
write.csv(accdf_fp_mpa, file='V:/lenfest_nmsf_biodiversity/Graphics_Manuscript/Plot_CSV_v2/Fig_Data_OBIS_acc_fp_mpa.csv')
