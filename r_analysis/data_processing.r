library(tidyverse)
library(dplyr)
library(readr)

#Import raw data
raw_data_sens <- read.csv2('r_analysis/raw_data/sensor_values_202410081428.csv')
raw_data_act <- read.csv2('r_analysis/raw_data/actuator_values_202410081742.csv')

#Delete not needed data
processed_data_sens <- raw_data_sens |>
  select(-c(id)) |>
  filter(sensor_id %in% c(105, 108))
  
processed_data_act <- raw_data_act |>
  select(-c(id)) 

#Convert to numeric values
processed_data_sens$timestamp <- as.numeric(processed_data_sens$timestamp)
processed_data_sens$value <- as.numeric(processed_data_sens$value)

processed_data_act$timestamp <- as.numeric(processed_data_act$timestamp)
processed_data_act$value <- as.numeric(processed_data_act$value)

#Normalize to starting time 
max_seconds <- max(processed_data_sens$timestamp)
min_seconds <- min(processed_data_sens$timestamp)

processed_data_sens$zero_time <- processed_data_sens$timestamp - min_seconds
processed_data_act$zero_time <- processed_data_act$timestamp - min_seconds

#Rearrange columns
processed_data_sens <- processed_data_sens |>
  relocate(zero_time)

processed_data_act <- processed_data_act |>
  relocate(zero_time)

#Correct for any offset
first_points <-  processed_data_sens |>
  filter(zero_time <1100)|>
  filter(sensor_id == 105)

prdt_offset <-  mean(first_points$value)

processed_data_sens <- processed_data_sens |>
  mutate(value = case_when(
    sensor_id == 105 ~ value - prdt_offset,
    TRUE ~ value
  ))



# #Create df for each sensor (if needed)
# processed_data_prdt_p <- processed_data_sens |>
#   filter(sensor_id == 105)
# 
# processed_data_ign_oss_p <- processed_data_sens |>
#   filter(sensor_id == 108)

#Save data as R df
#save(processed_data_sens, file = "r_analysis/processed_data/processed_data_sens.rds")
#save(processed_data_act, file = "r_analysis/processed_data/processed_data_act.rds")

#Save data as csv
write_csv(processed_data_sens, "r_analysis/processed_data/processed_data_sens.csv")
write_csv(processed_data_act, "r_analysis/processed_data/processed_data_act.csv")