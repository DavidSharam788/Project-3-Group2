library(readr)
EXPORT_HourlyData_Feeders <- read_csv("C:/Users/daved/Downloads/PV Data/PV Data - csv files only/2014-11-28 Cleansed and Processed/EXPORT HourlyData/EXPORT HourlyData - Feeders.csv")
View(EXPORT_HourlyData_Feeders)
colMeans(EXPORT_HourlyData_Feeders)
