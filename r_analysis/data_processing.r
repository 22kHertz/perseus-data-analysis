library(tidyverse)
library(dplyr)
library(readr)

#sens:  prdt_p      159
#       ign_fue_p   166
#       ign_oxd_p   169

# act:  fue   216
#       ox    217 
#       spk   218

sensor_ids <- c(159, 166, 169)

#Import raw data
raw_data_sens <- read.csv('r_analysis/raw_data/sensor_11_10-18-2024.csv')
raw_data_act <- read.csv('r_analysis/raw_data/actuator_11_10-18-2024.csv')


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

for (id in sensor_ids) {
  first_points <- processed_data_sens |>
    filter(zero_time < first_act) |>
    filter(sensor_id == id)
  
  offset <- mean(first_points$value)
  
  processed_data_sens <- processed_data_sens |>
    mutate(value = case_when(
      sensor_id == id ~ value - offset,
      TRUE ~ value
    ))
}


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

