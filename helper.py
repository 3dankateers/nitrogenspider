## file contains random helper functions
import datetime

month_dict = {
	"January" : 1,
	"February" : 2,
	"March" : 3,
	"April" : 4,
	"May" : 5,
	"June" : 6,
	"July" : 7,
	"August" : 8,
	"September" : 9,
	"October" : 10,
	"November" : 11,
	"December" : 12}


## takes in date in scraped format and returns date in 2016-06-09 format
## scraped format is : Saturday, June 11, 2016 1:00am 
def parse_date(date_string):
	parsed_date = date_string.split(",")
	month_day = parsed_date[1]
	year_time = parsed_date[2]
	month_str = month_day.split(" ")[1]
	month = month_dict[month_str]
	day = int(month_day.split(" ")[2])
	year = int(year_time.split(" ")[1])
	return datetime.date(year, month, day)

## takes in team name and map # in format: Immortals (map 3)
## returns team name  in format : Immortals
def parse_team_name(team_map_str):
	return team_map_str.split(" (")[0]

## takes in team name and map # in format: Immortals (map 3)
##returns map number: 3
def parse_map_number(team_map_str):
	map_location = team_map_str.find("map")
	return int(team_map_str[map_location + 4])


## takes in ML in format: ML 1.879 (-114) 
## returns integer -114
def parse_ML(ML_str):
	if ML_str.find("(") > 0:
		cut_one = ML_str.split("(")[1]
		return int(cut_one.split(")")[0])
	else: 
		return ML_str


