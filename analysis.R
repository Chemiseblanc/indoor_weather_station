DataFull <- read.csv(file="temperature_data.csv", header=TRUE, sep=",")

png("apartment_temperature.png")
sampling_freq = 2 # In measurements/hour
sampling_range = 7 # In days
recent = sampling_freq * 24 * sampling_range

# timespan = strptime(tail(DataFull$timestamp, recent), format="%c")
# temp = tail(DataFull$temperature, recent)
# ext_temp = tail(DataFull$external_temperature, recent)

# Data = data.frame(timespan,temp,ext_temp)
Data = data.frame(timespan = strptime(tail(DataFull$timestamp, recent), format="%c"),
temp = tail(DataFull$temperature, recent),
ext_temp = tail(DataFull$external_temperature, recent))

temp_range = get_ranges(Data$temp,Data$ext_temp)
ideal_range = c(21,23)

Data$col = "green"
Data$col[Data$temp > ideal_range[2]] = "red"
Data$col[Data$temp < ideal_range[1]] = "blue"

Data$ext_col = "black"
Data$ext_col[Data$ext_temp > 0] = "red"
Data$ext_col[Data$ext_temp < 0] = "blue"

plot(Data$timespan, Data$temp, ylim=temp_range, xlab="Time", ylab="Temperature (C)", main="Temperature Inside My Apartment", col=Data$col)
lines(Data$timespan, Data$temp, type="c")

par(new=TRUE)
plot(Data$timespan, Data$ext_temp, ylim=temp_range, xlab="", ylab="", pch=20, col=Data$ext_col)
lines(Data$timespan, Data$ext_temp, type="c")
abline(h=0, lty="solid")

thermostat = 19
abline(h=thermostat, lty="dotted")
text(Data$timespan[length(Data$timespan)],thermostat,adj=c(1,1.5),labels="Thermostat Setting", cex=0.6)

abline(h=ideal_range[1], lty="dashed")
abline(h=ideal_range[2], lty="dashed")
rect(0,ideal_range[1],Data$timespan[length(Data$timespan)]+ 1000000,ideal_range[2], col="palegreen", border=NA)
text(Data$timespan[length(Data$timespan)/2], 22, labels="Ideal Temperature Zone", cex=0.8)
dev.off()