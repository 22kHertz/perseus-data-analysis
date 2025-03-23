library(tidyverse)
library(dplyr)
library(readr)

raw_data_sens <- read.csv('r_analysis/raw_data/Medusa_01_0_002.csv')

processed_data_sens <-  raw_data_sens 

min_value <- min(processed_data_sens$s)
#max_value <- max(processed_data_sens$pC)

processed_data_sens$s <- processed_data_sens$s - min_value

# # Find the row with the maximum pC value
# max_row <- processed_data_sens[which.max(processed_data_sens$pC), ]
# 
# # Extract the time (s) corresponding to the maximum pC
# time_at_max_pC <- max_row$s
# 
# max_t <- time_at_max_pC + 5
# min_t <- time_at_max_pC - 0

processed_data_sens <- processed_data_sens |>
  filter(s <=  5)|>
  filter(s >= 3.2)

min_value <- min(processed_data_sens$s)
#max_value <- max(processed_data_sens$pC)

processed_data_sens$s <- processed_data_sens$s - min_value

write_csv(processed_data_sens, "r_analysis/processed_data/Medusa_01_02_complete.csv")
