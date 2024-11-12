library(tidyverse)
library(dplyr)
library(readr)

#sens:  mnl_oss_p, rnl_oss_p, oss_pln_p, fss_mnl_p, fss_rnl_p, fss_pln_p, fss_mf

# act:  at_oss_pur, at_fss_pur, at_oss_mnv, at_fss_mnv, at_oss_emgu, at_oss_emgd, at_fss_emg, at_oss_war

sensor_ids <- c(227:246)

#Import raw data
raw_data_sens <- read.csv('r_analysis/raw_data/sensor_15_10-25-2024.csv')
raw_data_act <- read.csv('r_analysis/raw_data/actuator_15_10-25-2024.csv')


#Delete not needed data
processed_data_sens <- raw_data_sens |>
  select(-c(index))
  
processed_data_act <- raw_data_act |>
  select(-c(index)) 


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


#Correct for any offset (taking mean over first values until first actuation)
first_act <- min(processed_data_act$zero_time) -100

# for (id in sensor_ids) {
#   first_points <- processed_data_sens |>
#     filter(zero_time < first_act) |>
#     filter(sensor_id == id)
#   
#   offset <- mean(first_points$value)
#   
#   processed_data_sens <- processed_data_sens |>
#     mutate(value = case_when(
#       sensor_id == id ~ value - offset,
#       TRUE ~ value
#     ))
# }


#Save data as csv
write_csv(processed_data_sens, "r_analysis/processed_data/processed_data_sens.csv")
write_csv(processed_data_act, "r_analysis/processed_data/processed_data_act.csv")


###Additional functions###

##Convert to numeric values (if needed)
#processed_data_sens$timestamp <- as.numeric(processed_data_sens$timestamp)
#processed_data_sens$value <- as.numeric(processed_data_sens$value)

#processed_data_act$timestamp <- as.numeric(processed_data_act$timestamp)
#processed_data_act$value <- as.numeric(processed_data_act$value)

##Plotting function
# first_points <- processed_data_sens |>
#   filter(zero_time < first_act) |>
#   filter(sensor_id == 169)
# 
# ggplot(first_points, aes(x = zero_time, 
#                          y = value))+
#   geom_path()+
#   theme_minimal()


##Create df for each sensor (if needed)
# processed_data_prdt_p <- processed_data_sens |>
#   filter(sensor_id == 105)
# 
# processed_data_ign_oss_p <- processed_data_sens |>
#   filter(sensor_id == 108)

#Save data as R df
#save(processed_data_sens, file = "r_analysis/processed_data/processed_data_sens.rds")
#save(processed_data_act, file = "r_analysis/processed_data/processed_data_act.rds")

