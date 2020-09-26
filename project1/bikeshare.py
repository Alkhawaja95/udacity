import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    possible_city_choices = ['a', 'b', 'c'] #list to simplify user_input choices
    mapped_cities = {'a':'chicago' , 'b': 'new york city', 'c': 'washington'} #dictionary to map user_city with CITY_DATA
    #takes user input and stores it in user_city
    user_city = input('kindly choose which city do you want to find it\'s statistics:\n (a) Chicago \n (b) New York City \n (c) Washington \n\n').lower()
    #creates a loop to validate user input
    while user_city not in possible_city_choices:
        print('\nWrong selection, please try again\n')
        user_city = input('kindly choose which city do you want to find it\'s statistics:\n (a) Chicago \n (b) New York City \n (c) Washington \n\n').lower()    # get user input for month (all, january, february, ... , june)
    #mappes user choice and stores it to variable :city" to be later used throughout the code
    city = mapped_cities[user_city]
    # get user input for month (all, january, february, ... , june)
    possible_month_choices = ['january' , 'february' , 'march' , 'april' , 'may' , 'june' , 'all']
    user_month = input('Kindly choose the prefered month based on the following list \nJanuary\nFebruary\nMarch\nApril\nMay\nJune\nAll\n\n').lower()
    #validate
    while user_month not in possible_month_choices:
        print('\nInvalid selection, please make sure you typed that correctly\n')
        user_month = input('Kindly choose the prefered month based on the following list \nJanuary\nFebruary\nMarch\nApril\nMay\nJune\nAll\n\n').lower()
    # get user input for day of week (all, monday, tuesday, ... sunday)
    possible_day_choices = ['monday', 'tuesday','wednessday','thursday','friday','saturday','sunday','all']
    user_day = input('Kindly choose the prefered day based on the following list \nMonday\nTuesday\nWednessday\nThursday\nFriday\nSaturday\nSunday\nAll\n\n').lower()
    #validate
    while user_day not in possible_day_choices:
        print('\nInvalid selection, please make sure you typed that correctly\n')
        user_day = input('Kindly choose the prefered day based on the following list \nMonday\nTuesday\nWednesday\nThursday\nFriday\nSaturday\nSunday\nAll\n\n').lower()
    print('Currently processing data from {} in {} in {}'.format(user_day.title(),user_month.title(),city.title()))
    print('-'*60)
    return city, user_month, user_day

def load_data(city,month,day):

    """
        Loads data for the specified city and filters by month and day if applicable.

        Args:
            (str) city - name of the city to analyze
            (str) month - name of the month to filter by, or "all" to apply no month filter
            (str) day - name of the day of week to filter by, or "all" to apply no day filter
        Returns:
            df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns in original df
    df['month'] = df['Start Time'].dt.month  #this is a column of month numbered from (1-6)
    df['day_of_week'] = df['Start Time'].dt.day_name() #this adds a column of day numbered from (1-31)

    # map selected month name to month number present in the df
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        #index(month) is the place of the user selected month in the months array starting from 0
        mon_number = months.index(month) + 1
        #makes the df contain only the rows with the month of the user choice
        df = df[df['month'] == mon_number]

    # filter by day of week if applicable
    if day != 'all':
        #makes the df contain only the rows with the day of the user choice
        df = df[df['day_of_week'] == day.title()]
    return df

def time_stats(df, user_month, user_day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #make sure not to view any meaningless data, if the user chose a month then ofcourse it is the most popular
    if user_month == 'all':
    # display the most common month
        popular_month = df['month'].mode()[0]
        print('The month with most rides is: ', popular_month)

    #make sure not to view any meaningless data, if the user chose a day then ofcourse it is the most popular
    if user_day == 'all':
    # display the most common day of week
        popular_day = df['day_of_week'].mode()[0]
        print('The day with most rides is: ', popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour #this adds a column of hours numbered from (00-24)
    popular_hour = df['hour'].mode()[0]
    print('Most people ride the bikes at: ', popular_hour)
    #calculate processing time of this block of the code
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0] #in dataframes, mode works on strings
    print('Most commonly used start station:', popular_start_station)
    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most commonly used end station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + ' ---> ' + df['End Station'] #merges the two columns together
    combination = df['trip'].mode()[0]
    print('the most common trip takes place between', combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel is {} days:' .format(total_travel_time/86400))
    # display average time a trip takes
    mean_travel_time = df['Trip Duration'].mean()
    print('The mean travel time is {} minutes:' .format(mean_travel_time/60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)

def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_counts =  df['User Type'].value_counts()
    print(user_counts, '\n')
    # Display counts of gender
    if city != 'washington':
        gender_counts = df['Gender'].value_counts()
        print(gender_counts, '\n')
    else:
        print('No gender count data for Washington\n')

    # Display earliest, most recent, and most common year of birth
    if city != 'washington':
        earliest_year = df['Birth Year'].min()
        recent_year = df['Birth Year'].max()
        common_year = df['Birth Year'].mode()[0]
        print('Oldest rider was born in {}'.format(int(earliest_year)))
        print('Youngest rider was born in {}'.format(int(recent_year)))
        print('Most riders were born in {}'.format(int(common_year)))
    else:
        print('No Year of Birth statistics for Washington')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)

def display_raw_data(city):
    """Displays raw data for user in chunks of 5 rows each time"""

    print('\nRaw data is available to check...\n')
    display_raw = input('\nWould you like to look on 5 lines of the raw data? Type yes or no\n')

    while display_raw == 'yes':
        try:
            for chunk in pd.read_csv(CITY_DATA[city], chunksize=5):
                print(chunk)
                display_raw = input('\nWould you like to look on the raw data? Type yes or no\n')
                if display_raw != 'yes':
                    break
            break
        except KeyboardInterrupt:
            print('\nOk, that will be it')

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_raw_data(city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('\nThank you!')
            break
if __name__ == "__main__":
	main()
