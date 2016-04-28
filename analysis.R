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

str(d)

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

d %>%
  group_by(shot_zone_type_concat) %>%
  summarise(shot_attempted = n(),
            shot_made = sum(SHOT_MADE_FLAG),
            shot_percentage = shot_made / shot_attempted) %>%
  gather(shot_type, shot_value, c(shot_attempted, shot_made)) %>%
  ggplot(aes(x = shot_zone_type_concat, y = shot_value, fill = shot_type)) +
    geom_bar(stat = "identity", position = "dodge")

player_shot_summary(d)



