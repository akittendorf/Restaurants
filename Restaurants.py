# module import
import pandas as pd

# load files
places = pd.read_csv('geoplaces2.csv') # placeID, name
rPayments = pd.read_csv('chefmozaccepts.csv') # placeID, Rpayment
rCuisines = pd.read_csv('chefmozcuisine.csv') # placeID, Rcuisine
parking = pd.read_csv('chefmozparking.csv') # placeID, parking_lot
ratings = pd.read_csv('rating_final.csv') # userID, placeID, rating, food_rating, service_rating
users = pd.read_csv('userprofile.csv') # userID, religion, activity, interest, drink_level
userPayments = pd.read_csv('userpayment.csv') # userID, Upayment
Ucuisines = pd.read_csv('usercuisine.csv') # userID, Rcuisine

# get relevant columns
places = places[['placeID', 'name']]
users = users[['userID', 'religion', 'activity', 'interest', 'drink_level']]

# rename cuisine column in Ucuisines
Ucuisines.rename(columns={'Rcuisine':'Ucuisine'},inplace=True)

# merge objects
places = places.merge(rPayments,how='inner',on='placeID') # add Rpayment
places = places.merge(rCuisines,how='inner',on='placeID') # add Rcuisine
places = places.merge(parking,how='inner',on='placeID') # add parking
users = users.merge(userPayments,how='inner',on='userID') # add uPayment
users = users.merge(Ucuisines,how='inner',on='userID') # add Rcuisine
users = users.merge(ratings,how='inner',on='userID') # add ratings
merged = users.merge(places,how='inner',on='placeID') # combine users and places objects

# What are all the supported payment methods for each place?
placePayments = merged[['name', 'Rpayment']].groupby('name')['Rpayment'].apply(set)
print(placePayments.head())

# What are the parking statuses for each place?
placeParking = merged[['name', 'parking_lot']].groupby('name')['parking_lot'].apply(set)
print(placeParking.head())

# What are the cuisines for each place?
cuisines = merged[['name', 'Rcuisine']].groupby('name')['Rcuisine'].apply(set)
print(cuisines.head())

# What is avg rating: rating, food, service,
#          min. rating: food, service
#           max. rating: service by cuisine?
avgRating = merged.groupby('Rcuisine')['rating'].mean(list) 
print(avgRating)
avgFood = merged.groupby('Rcuisine')['food_rating'].mean(list)
print(avgFood)
avgService = merged.groupby('Rcuisine')['service_rating'].mean(list)
print(avgService)
avgService = merged.groupby('Rcuisine')['rating'].mean(list)
print(avgService)
minFood = merged.groupby('Rcuisine')['food_rating'].min(list)
print(minFood)
minService = merged.groupby('Rcuisine')['service_rating'].min(list)
print(minService)
maxService = merged.groupby('Rcuisine')['service_rating'].max(list)
print(maxService)

# What are the preferred payment methods for social drinkers?
social = merged[['drink_level', 'Rpayment']][merged.drink_level=='social drinker'].value_counts()
print(social)
# drinker = merged[['drink_level', 'Rpayment']].set_index('drink_level').loc['social drinker'].value_counts()
# print(drinker)

# What are preferred cuisines by eco-friendly users?
eco = merged[['Ucuisine']][merged.interest=='eco-friendly'].value_counts()
print(eco)

# What are the preferred payment methods for students?
students = merged['Rpayment'][merged.activity=='student'].value_counts()
print(students)

# What cuisines are preferred by Catholic students?
catholic = merged[merged.religion=='Catholic']
catholicStudents = catholic['Ucuisine'][merged.activity=='student'].value_counts()
print(catholicStudents)

# What are some of the demographics of the users rating Mexican service ratings a 2?
Mex = merged[merged.Rcuisine=='Mexican']
Mex2 = Mex[Mex.rating==2]
dems = Mex2[['religion', 'activity', 'interest']].value_counts()
print(dems)