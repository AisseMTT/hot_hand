#####
##### inGlobalEnv()
##### -------------
##### boolean object presence in global env
#####
inGlobalEnv <- function(item) {
  item %in% ls(envir = .GlobalEnv)
}

#####
##### get_time_between_shots()
##### ------------------------
##### calculate time between shots within a quarter
#####
get_time_between_shots <- function(d) {
  quarter_data <- d %>% mutate(time_between_shots = NA) ## create new col
  
  for (row in 1:nrow(quarter_data)) {
    if (row == 1) {
      quarter_data[row, ]$time_between_shots <- NA
    }
    else {
      prev_row <- row - 1
      quarter_data[row, ]$time_between_shots <- quarter_data[prev_row, ]$TOTAL_TIME_REMAINING - quarter_data[row, ]$TOTAL_TIME_REMAINING
    }
  }
  quarter_data
}

#####
##### get_streaks()
##### -------------
##### find hit and miss streaks in data frame d
#####
get_streaks <- function(d) {
  
  ## Set-up df
  df <- d %>%
    mutate(prev_shot = lag(SHOT_MADE_FLAG),
           curr_hit_streak = NA,
           curr_miss_streak = NA)
 
   ## Store shot number
  df$shot_num <- seq(1, nrow(d))
  
  ## Store time between shots
  df <- plyr::ddply(df, .variables = c("PERIOD"), .fun = get_time_between_shots)
  
  ## Store streak data
  for (row in 1:nrow(df)) {
    ## First hot
    if (row == 1) {
      df[row, ]$curr_hit_streak <- 0
      df[row, ]$curr_miss_streak <- 0
    }
    ## Add to hit streak
    else if (df[row, ]$prev_shot == 1) {
      df[row, ]$curr_hit_streak <- df[row - 1, ]$curr_hit_streak + 1
      df[row, ]$curr_miss_streak <- 0
    }
    ## Add to miss streak
    else {
      df[row, ]$curr_miss_streak <- df[row - 1, ]$curr_miss_streak + 1
      df[row, ]$curr_hit_streak <- 0
    }
  }
  
  ## Return new df
  df
}

########
######## populate_prev_shots()
######## ---------------------
######## Populate new column with hit / miss streak data up to that point
########
populate_prev_shots <- function(d) {
  d_prev <-  plyr::ddply(d, .variables = c("PLAYER_ID", "GAME_ID"), .fun = get_streaks)
  
  d_prev
}
## Previous go
## ----------
# populate_prev_shots <- function(d) {
#   
#   ## Get previous shots
#   get_prev_shots <- function(d) {
#     d <- d %>% mutate(prev_shot1 = NA,
#                           prev_shot2 = NA,
#                           prev_shot3 = NA,
#                           prev_shot4 = NA)
#     
#     if (nrow(d) > 1) d$prev_shot1 <- c(NA, d$SHOT_MADE_FLAG[seq(1, length(d$SHOT_MADE_FLAG) - 1)])
#     if (nrow(d) > 2) d$prev_shot2 <- c(rep(NA, 2), d$SHOT_MADE_FLAG[seq(1, length(d$SHOT_MADE_FLAG) - 2)])
#     if (nrow(d) > 3) d$prev_shot3 <- c(rep(NA, 3), d$SHOT_MADE_FLAG[seq(1, length(d$SHOT_MADE_FLAG) - 3)])
#     if (nrow(d) > 4) d$prev_shot4 <- c(rep(NA, 4), d$SHOT_MADE_FLAG[seq(1, length(d$SHOT_MADE_FLAG) - 4)])
#     
#     d$shot_num <- seq(1, nrow(d))
#     
#     d
#   }
#   d_prev <-  plyr::ddply(d, .variables = c("PLAYER_ID", "GAME_ID"), .fun = get_prev_shots)
#   
#   ## Add in streak data
#   res_d <- d_prev %>%
#     mutate(
#       ## Made prev shots
#       made_last_1 = prev_shot1 == 1,
#       made_last_2 = made_last_1 & prev_shot2 == 1,
#       made_last_3 = made_last_2 & prev_shot3 == 1,
#       made_last_4 = made_last_3 & prev_shot4 == 1,
#       ## Missed prev shots
#       missed_last_1 = prev_shot1 == 0,
#       missed_last_2 = missed_last_1 & prev_shot2 == 0,
#       missed_last_3 = missed_last_2 & prev_shot3 == 0,
#       missed_last_4 = missed_last_3 & prev_shot4 == 0
#     )
#   
#   res_d
# }