## to do ##
# calculate ping time and response time
# parse mealList
# figure out what numbers are for 'dishesContain' and parse it (possibly create a dict?)


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


# ---- import data and inspect ---- #
paco = pd.read_csv('raw-data/paco.csv')
paco.head()
paco.columns


# ---------------------------------------------------- #
# ---- DATA CLEANING ---- #
# ---------------------------------------------------- #

# ---- remove blank rows where 'joined' does not equal True or False ---- #
# these rows are instances where the participant joined the study and do not contain any data
paco2 = paco[(paco['joined'] != True) & (paco['joined'] != False)]
paco2.head()
paco2.columns


# ---- subsetting df to only relevant columns ---- #
colsKeep = ['who', 'when', 'appId', 'responseTime', 'scheduledTime', 'timeZone', 'recentFullMeal', 'mealList', 'dishesContain', 'otherProtein', 'Form Duration']
paco3 = paco2[colsKeep]
paco3.head()
paco3.columns
paco3.shape


# ---- cleaning column names and renaming columns ---- #
colNamesClean = ['email', 'timeStamp', 'operatingSystem', 'responseTime', 'scheduledTime', 'timeZone', 'recentFullMeal', 'mealList', 'dishesContain', 'otherProtein', 'formDuration']
paco3.columns = colNamesClean
paco3.head()
paco3.columns


# ---- creating a text variable of recentFullMeal ---- #
recentFullMealDict = {
    1.0: "breakfast",
    2.0: "lunch",
    3.0: "dinner"
}


def map_recentFullMeal(df):
    mapping = recentFullMealDict
    return mapping.get(df['recentFullMeal'])


paco3['recentFullMeal_text'] = paco3.apply(map_recentFullMeal, axis=1)
paco3['recentFullMeal_text'].fillna(value=nan, inplace=True)
paco3.head(10)
paco3.columns


# ---- creating binary indicator variables from dishesContain ---- #
paco3['dishesContain_beef'] = paco3['dishesContain'].str.contains(r"\b1\b")*1
paco3['dishesContain_pork'] = paco3['dishesContain'].str.contains(r"\b2\b")*1
paco3['dishesContain_poultry'] = paco3['dishesContain'].str.contains(r"\b3\b")*1
paco3['dishesContain_fish'] = paco3['dishesContain'].str.contains(r"\b4\b")*1
paco3['dishesContain_shellfish'] = paco3['dishesContain'].str.contains(r"\b5\b")*1
paco3['dishesContain_dairy'] = paco3['dishesContain'].str.contains(r"\b6\b")*1
paco3['dishesContain_eggs'] = paco3['dishesContain'].str.contains(r"\b7\b")*1
paco3['dishesContain_vegetables'] = paco3['dishesContain'].str.contains(r"\b8\b")*1
paco3['dishesContain_fruit'] = paco3['dishesContain'].str.contains(r"\b9\b")*1
paco3['dishesContain_beans'] = paco3['dishesContain'].str.contains(r"\b10\b")*1
paco3['dishesContain_nuts'] = paco3['dishesContain'].str.contains(r"\b11\b")*1
paco3['dishesContain_grains'] = paco3['dishesContain'].str.contains(r"\b12\b")*1
paco3['dishesContain_sweets'] = paco3['dishesContain'].str.contains(r"\b13\b")*1
paco3['dishesContain_vegMeat'] = paco3['dishesContain'].str.contains(r"\b14\b")*1
paco3['dishesContain_otherProtein'] = paco3['dishesContain'].str.contains(r"\b15\b")*1

paco3.head(10)
paco3[['dishesContain', 'dishesContain_eggs']] # should only see 1's where there are 7's
paco3[['dishesContain', 'dishesContain_grains']] # should only see 1's where there are 12's


dishesContainDict = {
    "1": "Beef or other red meat (lamb, goat, etc.)",
    "2": "Pork",
    "3": "Chicken or turkey",
    "4": "Fish",
    "5": "Shellfish (shrimp, crab, oysters, etc.)",
    "6": "Dairy (milk, butter, cheese, etc.)",
    "7": "Eggs",
    "8": "Vegetables",
    "9": "Fruit",
    "10": "Beans",
    "11": "Nuts",
    "12": "Grains and cereals (wheat, rice, corn)",
    "13": "Sweets (cake, pie, candy, etc.)",
    "14": "Vegetarian meats/protein (tofu, etc.)",
    "15": "Other protein"
}

paco3.columns
paco3.iloc[:,12:].dropna().plot(kind='hist', subplots=True)
plt.show()

# ---- create df where mealList does not equal NaN ---- #
paco4 = paco3[paco3['mealList'].notnull()]
paco4.head(10)
paco4.shape

# ---- get a random subset of paco4 to determine accuracy of food descriptions ---- #




# ---- making plots to show frequency of foods in meals ---- # 

sns.countplot(x="dishesContain_dairy", data=paco4, palette="Greens_d")
plt.show()


means = paco4.iloc[:,12:].mean()
data = means
names = list(data.keys())
values = list(data.values)


fig, axs = plt.plot(1, 3, figsize=(9, 3), sharey=True)
axs[0].bar(names, values)
axs[1].scatter(names, values)
axs[2].plot(names, values)
fig.suptitle('Categorical Plotting')
plt.show()


# ---------------------------------------------------- #
# ---- EXPLORING RESPONSE TIMES ---- #
# ---------------------------------------------------- #

# ---- creating dataset with no null observations ---- #
# only taking observations where there is an instance of a responseTime and a scheduledTime
# it's unclear why there are so many observations that only have a responseTime and
# others that only have a scheduledTime
paco3_times = paco3[paco3[['responseTime', 'scheduledTime']].notnull()]
paco3_times.head()
paco3_times.shape


# ---- creating a 'timeToRespond' variable that calculates response time ---- #
# subtracts the scheduledTime from responseTime
# then creates a new variable 'timeToResponse_seconds' variables that converts to seconds
paco3_times['timeToRespond'] = paco3_times['responseTime'] - paco3_times['scheduledTime']
paco3_times['timeToResond_seconds'] = paco3_times['timeToRespond'] / np.timedelta64(1, 's')
paco3_times.dtypes


# ---- creates histogram  and boxplot of time to respond ---- # 
plt.hist(paco3_times['timeToResond_seconds'], bins=100)
plt.show()

plt.boxplot(paco3_times['timeToResond_seconds'])
plt.show()






