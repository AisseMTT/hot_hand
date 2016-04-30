library(dplyr)
library(tidyr)
library(ggplot2)

setwd('/Users/benpeloquin/Desktop/Spring2016/Stats267/hot_hand')

d <- read.csv('player_data/203500.csv', stringsAsFactors = FALSE)

## Some initial data processing
d$PERIOD <- as.factor(d$PERIOD)

## Add more features here?
d <- d %>%
  mutate(total_sec_remaining = MINUTES_REMAINING * 60 + SECONDS_REMAINING,
         shot_zone_type_concat = as.factor(paste0(SHOT_ZONE_RANGE, '-', SHOT_TYPE)),
         action_type_shot_type = as.factor(paste0(ACTION_TYPE, '-', SHOT_TYPE)))

d2 <- d %>%
  mutate(prev_shot1 = NA)
for (row in seq(1, nrow(d))) {
  if (row != 1) {
    d2[row, "prev_shot1"] <- d2[row - 1, "SHOT_MADE_FLAG"]
  } 
}
d2
sum(d2$prev_shot1[2:length(d2$prev_shot1)]) / nrow(d2)
sum(d2$SHOT_MADE_FLAG) / nrow(d2)
names(d2)
summary(glm(SHOT_MADE_FLAG ~
              SHOT_DISTANCE +
              PERIOD +
              SHOT_TYPE +
              LOC_X +
              LOC_Y +
              prev_shot1 +
              total_sec_remaining,
            family = "binomial", data = d2))

player_shot_summary <- function(d) {
  player_name <- unique(d$PLAYER_NAME)
  cat(paste0("Player name: ", player_name), "\n")  
  
  team_name <- unique(d$TEAM_NAME)
  cat(paste0("Team name: ", team_name), "\n")  
  
  shots_attempted <- sum(d$SHOT_ATTEMPTED_FLAG)
  cat(paste0("Shots attempted: ", shots_attempted), "\n")
  
  shots_made <- sum(d$SHOT_MADE_FLAG)
  cat(paste0("Shots made: ", shots_made), "\n")
  
  shooting_percentage <- shots_made / shots_attempted
  cat(paste0("Shot percentage: ", shooting_percentage), "\n")
}
player_shot_summary(d)

## Plot shots made / attempted by type
d %>%
  group_by(shot_zone_type_concat) %>%
  summarise(shot_attempted = n(),
            shot_made = sum(SHOT_MADE_FLAG),
            shot_percentage = shot_made / shot_attempted) %>%
  gather(shot_type, shot_value, c(shot_attempted, shot_made)) %>%
  ggplot(aes(x = shot_zone_type_concat, y = shot_value, fill = shot_type)) +
    geom_bar(stat = "identity", position = "dodge")

ggplot(d, aes(x = total_sec_remaining, y = SHOT_ATTEMPTED_FLAG, col = as.factor(GAME_ID), size = SHOT_DISTANCE)) +
  geom_point(alpha = 0.5, position = position_jitter(height = 0.005)) +
  ylim(0.95, 1.05)
  
names(d)
