## notes ##
# there appears to be no identifier in the paco responses, so we can't merge paco food diary responses to recruitment or followup data

## to do ##
# calculate ping time and response time
# parse mealList
# character count - do people write less on later pings?
# who are the kinds of people who dropped out?
# response quality (verbosity, etc) differs by education
# 


# ---- import packages ---- # 
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from numpy import nan
import seaborn as sns



# ---- set working directory ---- # 
path = '/Users/Krystal/Google Drive/AWAL/research-projects/current-projects/messaging-competition/mini-pilot'
os.chdir(path)
os.getcwd()


# ---- import recruitment data and inspect ---- #
recruit = pd.read_csv('raw-data/Meat_message_comp_Mini_pilot_Recruitment_Survey.csv', skiprows=[0])
recruit.head()
recruit.columns
# i used this to determine whether there were hidden characters in column names 
list(data.columns.values)

# --- import follow-up data ---- #
followup = pd.read_csv('raw-data/Meat_message_comp_Mini_pilot_Follow_Up.csv', skiprows=[0])
followup.head(10)
followup.columns
# i used this to determine whether there were hidden characters in column names 
list(followup.columns.values)

# --- import food diary data (mturk and survey signal groups) ---- #
diary = pd.read_csv('raw-data/Meat_message_comp_Mini_pilot_Food_Diary.csv', skiprows=[0])
diary.head(10)
diary.columns
# i used this to determine whether there were hidden characters in column names 
list(diary.columns.values)

# ---------------------------------------------------- #
# ---- DATA CLEANING ---- #
# ---- recruitment data ---- #
# ---------------------------------------------------- #

# ---- subsetting df to only relevant columns ---- #
colsKeep_recruit = [
    'IPAddress',
    'StartDate',
    'EndDate',
    'MID',
    """Do you intend to change your fruit and vegetable consumption over the next week?\xa0 "I intend to __...""",
    "Do you intend to change your meat consumption over the next week? Meat includes chicken, turkey,...",
    "What are the\xa0TWO\xa0most important things that you take into consideration when deciding what meat,...-Price of the product", 
    'What are the\xa0TWO\xa0most important things that you take into consideration when deciding what meat,...-Nutritional content of the product', 
    'What are the\xa0TWO\xa0most important things that you take into consideration when deciding what meat,...-Whether the product is antibiotic and/or hormone free', 
    "What are the\xa0TWO\xa0most important things that you take into consideration when deciding what meat,...-Whether the animals had a good standard of living", 
    'What are the\xa0TWO\xa0most important things that you take into consideration when deciding what meat,...-How the product tastes', 
    "What are the\xa0TWO\xa0most important things that you take into consideration when deciding what meat,...-The environmental impacts of the product",
    'What are the\xa0TWO\xa0most important things that you take into consideration when deciding what meat,...-Other (please specify):', 
    'What are the\xa0TWO\xa0most important things that you take into consideration when deciding what meat,...-Other (please specify):-TEXT', 
    'Do you currently eat a vegetarian or vegan diet? \xa0 A vegetarian diet includes egg and dairy, but...',
    '50 States, D.C. and Puerto Rico',
    "What is you gender",
    "What is the highest educational qualification you have obtained?",
    "What is the highest educational qualification you have obtained?-TEXT",
    "In which of these groups did your total PERSONAL income, from all sources, fall last year before...",
    "What is your age?",
    "Which of these best describes your political orientation?",
    "Thank you for completing the Recruitment Survey. On the next page you'll be asked to confirm your...",
    "Thank you for completing the Recruitment Survey. On the next page you'll be asked to confirm your....1",
    "Display Order: Block Randomizer FL_6"
]

recruit2 = recruit[colsKeep_recruit]
recruit2.head()
recruit2.columns
recruit2.shape

# ---- cleaning column names and renaming columns ---- #
colNamesClean_recruit = [
    'recruit_ipAddress',
    'recruit_startDate',
    'recruit_endDate',
    'mturkId',
    'recruit_intentionToChangeFruitAndVegConsumpOverNextWeek',
    'recruit_intentionToChangeMeatConsumpOverNextWeek',
    'recruit_meatConsideration_price',
    'recruit_meatCondsideration_nutrition',
    'recruit_meatCondsideration_antibiotics',
    'recruit_meatCondsideration_standardOfLiving',
    'recruit_meatCondsideration_taste',
    'recruit_meatCondsideration_environ',
    'recruit_meatCondsideration_other',
    'recruit_meatCondsideration_otherText',
    'recruit_currentDietVeg',
    'recruit_state',
    'recruit_gender',
    'recruit_education',
    'recruit_education_text',
    'recruit_income',
    'recruit_age',
    'recruit_politicalOrientation',
    'recruit_phoneNumber_mturk',
    'recruit_phoneNumber_surveySignal',
    'recruit_surveyPlatform'
]

recruit2.columns = colNamesClean_recruit
recruit2.head(20)
recruit2.columns

# drop first line which is '-99's
recruit2 = recruit2.drop(recruit2.index[0])


# ---- cleaning phone numbers ---- #
# remove hypens from phne numbers
recruit2['recruit_phoneNumber_mturk'].replace(regex=True,inplace=True,to_replace=r'\D',value=r'')
recruit2['recruit_phoneNumber_surveySignal'].replace(regex=True,inplace=True,to_replace=r'\D',value=r'')

# combining two phone number columns into one 
recruit2['phoneNumber'] = recruit2.recruit_phoneNumber_mturk.combine_first(recruit2.recruit_phoneNumber_surveySignal)

# ---- setting index ---- #
#recruit2 = recruit2.set_index(['recruit_mturkId', 'recruit_phoneNumber'])
#recruit2.index
#recruit2 = recruit2.reindex(recruit2.index.rename(['mturkId', 'phoneNumber']))
#recruit2.index

# ---------------------------------------------------- #
# ---- DATA CLEANING ---- #
# ----followup data ---- #
# ---------------------------------------------------- #
colsKeep_followup = [
    'IPAddress', 
    'StartDate', 
    'EndDate',
    'MID',
    'Were any parts of the study confusing or troublesome?',
    'How was completing the initial Recruitment Survey were you signed up for the food diary?',
    'Overall, how did you feel about the Recruitment Survey?',
    'How was completing the entries for the Food Diary?', 
    'How difficult or easy was it for you to recall what you had eaten for the prior meal in the Food...',
    'How convenient or inconvenient was it for you to complete an entry in the Food Diary?',
    'Overall, how did you feel about the Food Diary?', 
    'Would you participate in a study like this again?', 
    'The Food Diary you participated in lasted 1 week, had 3 entries, and paid $1. If the Food Diary h...', 'What time do you normally eat lunch?', 
    'What time do you normally eat dinner?',
    'Any other comments?',
    'What did you think the purpose of this study was?'
]

followup2 = followup[colsKeep_followup]
followup2.head()
followup2.columns
followup2.shape

# ---- cleaning column names and renaming columns ---- #
colNamesClean_followup = [
    'followup_ipAddress',
    'followup_startDate',
    'followup_endDate',
    'mturkId',
    'followup_studyConfusingOrTroublesome',
    'followup_howWasRecruitmentSurvey',
    'followup_overallFeelingRecruitmentSurvey',
    'followup_howWasFoodDiary',
    'followup_howDifficultToRecallMeals',
    'followup_howConvenientFoodDiary',
    'followup_overallFeelingFoodDiary',
    'followup_wouldYouParticipateAgain',
    'followup_wouldYouParticipateInLongerStudy',
    'followup_timeEatLunch',
    'followup_timeEatDinner',
    'followup_otherComments',
    'followup_purposeOfStudy'
]

followup2.columns = colNamesClean_followup
followup2.head(20)
followup2.columns

# checking overlap in mturk id's between recruitment and followup surveys
recruit2['mturkId'].isin(followup2['mturkId'])

# ---- setting index ---- #
#followup2 = followup2.set_index('followup_mturkId')
#followup2.index
#followup2 = followup2.reindex(followup2.index.rename('mturkId'))
#followup2.index

# ---------------------------------------------------- #
# ---- DATA CLEANING ---- #
# ---- food diary data ---- #
# ---------------------------------------------------- #
diary.columns

colsKeep_diary = [
    'IPAddress', 
    'StartDate', 
    'EndDate',
    'What was the most recent full meal you ate (as in something more than just snacking).',
    'Please list what you ate for this meal.Think carefully, and list every dish or part that was incl...',
    'Did any of the dishes contain the following? (Select all that apply)-Beef or other red meat (lamb, goat, etc.)',
    'Did any of the dishes contain the following? (Select all that apply)-Pork',
    'Did any of the dishes contain the following? (Select all that apply)-Chicken or other poultry',
    'Did any of the dishes contain the following? (Select all that apply)-Fish',
    'Did any of the dishes contain the following? (Select all that apply)-Shellfish (shrimp, crab, oysters, etc.)',
    'Did any of the dishes contain the following? (Select all that apply)-Dairy (milk, butter, cheese, etc.)',
    'Did any of the dishes contain the following? (Select all that apply)-Eggs',
    'Did any of the dishes contain the following? (Select all that apply)-Vegetables',
    'Did any of the dishes contain the following? (Select all that apply)-Fruit',
    'Did any of the dishes contain the following? (Select all that apply)-Beans',
    'Did any of the dishes contain the following? (Select all that apply)-Nuts',
    'Did any of the dishes contain the following? (Select all that apply)-Grains and cereals (wheat, rice, corn)',
    'Did any of the dishes contain the following? (Select all that apply)-Vegetarian meats / protein (tofu, etc)',
    'Did any of the dishes contain the following? (Select all that apply)-Sweets (cake, pie, candy, etc.)',
    'Did any of the dishes contain the following? (Select all that apply)-Other protein (if so, what?)',
    'Did any of the dishes contain the following? (Select all that apply)-Other protein (if so, what?)-TEXT',
    'To confirm your entry, please re-enter your phone number including the area code below (no spaces...',
]

diary2 = diary[colsKeep_diary]
diary2.head()
diary2.columns
diary2.shape

# ---- cleaning column names and renaming columns ---- #
colNamesClean_diary = [
    'diary_ipAddress',
    'diary_startDate',
    'diary_endDate',
    'diary_recentFullMeal',
    'diary_mealList',
    'diary_dishesContain_beef',
    'diary_dishesContain_pork',
    'diary_dishesContain_poultry',
    'diary_dishesContain_fish',
    'diary_dishesContain_shellfish',
    'diary_dishesContain_dairy',
    'diary_dishesContain_eggs',
    'diary_dishesContain_vegetables',
    'diary_dishesContain_fruit',
    'diary_dishesContain_beans',
    'diary_dishesContain_nuts',
    'diary_dishesContain_grains',
    'diary_dishesContain_vegMeat',
    'diary_dishesContain_sweets',
    'diary_dishesContain_otherProtein',
    'diary_dishesContain_otherProteinText',
    'phoneNumber'
]

diary2.columns = colNamesClean_diary
diary2.head(20)
diary2.columns

# ---- cleaning phone numbers ---- #
# remove hypens from phne numbers
diary2['phoneNumber'].replace(regex=True,inplace=True,to_replace=r'\D',value=r'')

# ---- setting index ---- #
#diary2 = diary2.set_index('diary_phoneNumber')
#diary2.index
#diary2 = diary2.reindex(diary2.index.rename('phoneNumber'))
#diary2.index



data = recruit2.merge(followup2,how='left', left_on='mturkId', right_on='mturkId')
data.shape
data.head(20)
data.tail


data2 = data.merge(diary2,how='left', left_on='phoneNumber', right_on='phoneNumber')
data2.shape
diary2.shape
data2.tail()