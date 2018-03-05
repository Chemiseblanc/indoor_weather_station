# Read data from csv into R
Data <- read.csv(file="temp_history.csv", header=TRUE, sep=",")
# Write plot to file
png("temperature.png")
# Plot Data
plot(strptime(Data$timestamp, format="%c"), Data$temperature, xlab="Time", ylab="Temperature (C)", main="How hot is it? (as a function of time)")
# Interpolate splines between points
lines(strptime(Data$timestamp, format="%c"), Data$temperature, type="c")
# Close the device
dev.off()