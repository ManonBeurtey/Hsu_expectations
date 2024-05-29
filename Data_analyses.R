#### #### #### #### ##### #### #### #### ##### #### #### #### # 
# Pilot - CEA - Neurospin Unicog, CBD Team
# 
# Interaction effect in the spectral  
# and temporal expectations in auditory system
#
# May 2024 - Cogmaster (M1)
#### #### #### #### ##### #### #### #### ##### #### #### #### # 

# Packages
install.packages("dplyr")
install.packages("ggplot2")
install.packages("car")

library(dplyr)
library(ggplot2)
library(car)

# Loading the CSV and cleaning the data
raw_data1 = read.csv("participant1.xpd", sep = ",", comment.char = "#")
raw_data2 = read.csv("participant2.xpd", sep = ",", comment.char = "#")
raw_data3 = read.csv("participant3.xpd", sep = ",", comment.char = "#")
raw_data4 = read.csv("participant4.xpd", sep = ",", comment.char = "#")
raw_data5 = read.csv("participant5.xpd", sep = ",", comment.char = "#")
raw_data6 = read.csv("participant6.xpd", sep = ",", comment.char = "#")
raw_data7 = read.csv("participant7.xpd", sep = ",", comment.char = "#")

raw_data = rbind(raw_data1, raw_data2, raw_data3, raw_data4, raw_data5, raw_data6, raw_data7)

raw_data <- raw_data %>% 
  mutate(RT = replace(RT, RT == "None", NA))

big_data = na.omit(raw_data)

big_data = big_data %>% 
  mutate(RT = as.numeric(RT),
         SOA = as.numeric(SOA),
         ITI = as.numeric(ITI),
         Cue = as.numeric(Cue),
         Target = as.numeric(Target))

# Removing outliers 
SD = sd(big_data$RT)
µ = mean(big_data$RT)
#borne_inf = µ-3*SD
borne_sup = µ+3*SD

data <- big_data %>%
  filter(RT <= borne_sup)

outliers <- big_data %>%
  filter(RT >= borne_sup)

boxplot(big_data$RT)
boxplot(data$RT)

summary(big_data$RT)
summary(data$RT)
sd(big_data$RT)
sd(data$RT)

# Shaping the dataframe

  # Two new columns conditions
data <- data %>%
  mutate(
    Temporal_condition = if_else(Cue == 1318, "Fixed", "Variable"),
    Spectral_condition = if_else(Target == 1975, "Fixed", "Variable")
  )

data <- data %>%
  mutate(
    Temporal_condition = if_else(Cue == 1318, "Fixed", "Variable"),
    Spectral_condition = if_else(Target == 1975, "Fixed", "Variable")
  )


mean_values <- data %>% 
  group_by(Temporal_condition, Spectral_condition) %>% 
  summarize(RT = mean(RT))

meanRTs <- mean(data$RT)
meanRTs

# GGplots
ggplot(data, aes(x=RT)) + 
  geom_histogram() + 
  geom_vline(aes(xintercept = meanRTs), color = "red") +
  annotate("text", x = 410, y = 150, label = sprintf("Mean: %.2f", meanRTs),
           color = "red") +
  theme_bw() +
  labs(title = "Responses time distribution",
       x = "Response time", 
       y="Frequency",
       caption = "...")

# ITI distribution
ggplot(data, aes(x=ITI)) + 
  geom_histogram(bins = 50) + 
  theme_bw() +
  labs(title = "Intertrial interval distribution",
       x = "Intertrial duration", 
       y="Frequency",
       caption = "...")

# Boxplot RTs function of Temporal condition
ggplot(data, aes(x = Temporal_condition, y = RT)) +
  geom_boxplot(alpha = 0.1) +
  geom_violin(aes(color = Temporal_condition, fill = Temporal_condition), alpha = 0.4) +
  scale_color_manual(values = c("Fixed" = "#0737fc", "Variable" = "#66c7ff")) +
  scale_fill_manual(values = c("Fixed" = "#0737fc", "Variable" = "#66c7ff")) +
  theme_bw() +
  labs(title = "RTs function of temporal expectations",
       x = "Temporal condition",
       y = "Response time",
       caption = "...")

# Boxplot RTs function of Spectral condition
ggplot(data, aes(x = Spectral_condition, y = RT)) +
  geom_boxplot(alpha = 0.1) +
  geom_violin(aes(color = Spectral_condition, fill = Spectral_condition), alpha = 0.4) +
  scale_color_manual(values = c("Fixed" = "#FF0000", "Variable" = "#fab6e9")) +
  scale_fill_manual(values = c("Fixed" = "#FF0000", "Variable" = "#fab6e9")) +
  theme_bw() +
  labs(title = "RTs function of spectral expectations",
       x = "Spectral condition",
       y = "Response time",
       caption = "...")

## Interaction
ggplot(mean_values, aes(x = Spectral_condition, y = RT, color = Temporal_condition, group = Temporal_condition)) +
  geom_point(size=2) +
  geom_line(lty=2, lwd=1) +
  scale_y_continuous(limits = c(200, 600)) +
  theme_bw() +
  labs(title = "Interaction Effect of Spectral and Temporal Conditions",
       x = "Levels of Spectral Condition",
       y = "Mean Response Time")

# Statistical analyses wih t.test
t.test(data$RT[data$Temporal_condition == "Fixed"], data$RT[data$Temporal_condition == "Variable"])
t.test(data$RT[data$Spectral_condition == "Fixed"], data$RT[data$Spectral_condition == "Variable"])

# Statistical analyses with ANOVA
model <- aov(RT ~ Temporal_condition * Spectral_condition, data = data)
summary(model)

model2 <- lm(RT ~ ITI, data = data)
summary(model2)

ggplot(data, aes(x = RT, y = ITI)) + 
  geom_point() +  # Ajouter un nuage de points
  geom_smooth(method = "lm", se = TRUE, color = "blue") +  # Ajouter la ligne de régression linéaire
  labs(title = "Linear regression between RT and intertrial duration",
       x = "response time",
       y = "intertrial duration")

