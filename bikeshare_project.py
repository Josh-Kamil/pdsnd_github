import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

#filters raw data based on selection of city, month and day
def get_filters():
    global city, month, day
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    city = input("To select one of the following cities - Chicago, Washington or New York City  - please type in the full name: ")
    while str.lower(city) not in ['new york city', 'washington', 'chicago']: 
        if str.lower(city) not in ['new york city', 'washington', 'chicago']:
            print("Please only enter one of the following: 'New York City', 'Chicago' or 'Washington'")
            print()
            city = input("Please re-type city name: ")

    # get user input for month (all, january, february, ... , june)
    month = input("Please select the month of interest for your analysis - this may be any month from January to June: ")
    while str.lower(month) not in ['january', 'february', 'march', 'april', 'may', 'june']: 
        if str.lower(month) not in ['january', 'february', 'march', 'april', 'may', 'june']:
            print("Please only enter one of the following: 'January', 'February', 'March', 'April', 'May', 'June'")
            print()
            month = input("Please re-type month name: ")


    #get user input for day of week (all, monday, tuesday, ... sunday)    
    day = input("Please select a day of the week for your analysis - this may be any day from Monday to Sunday: ")
    while str.lower(day) not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']: 
        if str.lower(month) not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            print("Please only enter a valid day of the week")
            print()
            day = input("Please re-type day name: ")
    
    city = str.lower(city)
    month = str.lower(month)
    day = str.lower(day)


    print('-'*40)
    return city, month, day


def load_data(city):
    global df
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[str.lower(city)])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].apply(lambda x: x.strftime("%B"))
    # extract month from Start Time to create a new column of month name
    df['Start Hour'] = df['Start Time'].apply(lambda x: x.strftime("%H"))+":00"
    # extract day of week from Start Time to create a new column of weekday name
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    # convert the Start Time column to datetime
    #filter by month
    if month != 'all':
        df = df.loc[df['month']  == str.title(month)]
        # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'] == str.lower(day)]
    
    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    # convert the Start Time column to datetime
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    frequent_month = df.groupby(['month'])['month'].count().nlargest(1)

    # display the most common day of week
    frequent_day = df.groupby(['day_of_week'])['day_of_week'].count().nlargest(1)

    # display the most common start hour
    frequent_start_hour = df.groupby(['Start Hour'])['Start Hour'].count().nlargest(1)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    print()
    print("This is the busiest month for bikeshare in {}:".format(city.title()))
    print(frequent_month)
    print()
    print("This is the busiest day for bikeshare in {}:".format(city.title()))
    print(frequent_day)
    print()
    print("This is the most common hour of the day for starting a bikeshare trip:")    
    print(frequent_start_hour)
    print()  

    return frequent_month, frequent_day, frequent_start_hour 



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    frequent_start_station = df.groupby(['Start Station'])['Start Station'].size().nlargest(1)

    # display most commonly used end station
    frequent_end_station = df.groupby(['End Station'])['End Station'].size().nlargest(1)

    # display most frequent combination of start station and end station trip
    frequent_start_end_station = df.groupby(['Start Station','End Station'])['Start Station'].count().nlargest(1)

    print()
    print("This is the starting station with most departures in {}:".format(city.title()))
    print()
    print(frequent_start_station.nlargest(1))

    print()
    print("This is the end station with most arrivals in {}:".format(city.title()))
    print()
    print(frequent_end_station.nlargest(1))
    
    print()
    print("This is the most common start and end stations combinations in {}:".format(city.title()))
    print()
    print(frequent_start_end_station.nlargest(1))
  
    print()
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)





def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['DiffTime'] = pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])
    hours = df['DiffTime'].sum().days/24 + df['DiffTime'].sum().seconds/(60*60) #converting days and seconds to hours

    # display mean travel time
    mean_tt = round(df['DiffTime'].mean().seconds/60,2) #converting to minutes

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    print()
    print("The total on-road time in hours for bikeshare bikes in {}".format(city.title())+" is:")
    print(str(round(hours,2)) + " hours")
    print()
    print("The average travel time in minutes for trips in {}".format(city.title())+" is:")
    print(str(mean_tt) + " minutes")


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df.groupby(['User Type'])['User Type'].count()

    # Display counts of gender
    if str.lower(city) != 'washington':
        subscriber_gen = df.groupby(['Gender'])['Gender'].count()
    else:
        print()
        subscriber_gen = "****Subscriber gender information is not available for {}:".format(city)
        
    # Display earliest, most recent, and most common year of birth
    if str.lower(city) != 'washington':
        subscriber_birth_year_top = df.groupby(['Birth Year'])['Birth Year'].count().nlargest(1)
        most_recent_year = df['Birth Year'].max()
        earliest_year = df['Birth Year'].min()
    else:
        print()
        subscriber_birth_year_top = "****Subscriber birth yeat information is not available for {}:".format(city)
        most_recent_year = "****Subscriber birth year information is not available for {}:".format(city)
        earliest_year = "****Subscriber birth year information is not available for {}:".format(city)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    print()
    print("The total number of Customers and Subscribers using bikeshare in {} is:".format(city.title()))
    print(user_types)
    print()
    print("The total number of male and female bikeshare who use the service in {} is:".format(city.title()))
    print(subscriber_gen)
    print()
    print("The top birth year for bikeshare subscribers who use the service in {} is:".format(city.title()))
    print(subscriber_birth_year_top)
    print()
    print("The most recent birth year for bikeshare subscribers who use the service in {} is:".format(city.title()))
    print(most_recent_year)
    print()
    print("The earliest birth year for bikeshare subscribers who use the service in {} is:".format(city.title()))
    print(earliest_year )


#counter variable is stored in the root object
#this function allows the user to progress 5 lines at a time through the raw data
counter = 0
def next_five_lines(df):
    global counter
    counter += 1
    view_limit = len(df['Start Time'])
    if (counter*5 > view_limit):
        printed_five_rows = df.iloc[ counter*5 - 5 : view_limit,]
        print('Filtered data rows {} to {}.'.format(counter*5 - 5,view_limit))
    else:
        printed_five_rows = df.iloc[ counter*5 - 5 : counter*5,]
        print('Filtered data rows {} to {}.'.format(counter*5 - 5,counter*5))
 
    if len(df.iloc[ counter*5 - 5 : view_limit,]) < 5: 
        print("No further raw data to show")
        counter = 0

    print(printed_five_rows)




def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city)
        
        viewtimestats = input('\nWould you like to view statistics by time period? Enter yes or no.\n')
        while str.lower(viewtimestats) not in ['yes', 'no']:
            viewtimestats = input("Please enter 'yes' or 'no'")
        if viewtimestats.lower() == 'yes':
            time_stats(df)
        

        viewstationstats = input('\nWould you like to view statistics by docking station? Enter yes or no.\n')
        while str.lower(viewstationstats) not in ['yes', 'no']:
            viewstationstats = input("Please enter 'yes' or 'no'")
        if viewstationstats.lower() == 'yes':
           station_stats(df)
           
        viewtripdurationstats = input('\nWould you like to view statistics about total sharebike\nhours travelled and average travel time? Enter yes or no.\n')
        while str.lower(viewtripdurationstats) not in ['yes', 'no']:
            viewtripdurationstats = input("Please enter 'yes' or 'no'")  
        if viewtripdurationstats.lower() == 'yes':    
            trip_duration_stats(df)
        
        viewuserstats = input('\nWould you like to view statistics about total use by male and female sharebike subscribers? Enter yes or no.\n')
        while str.lower(viewuserstats) not in ['yes', 'no']:
            viewuserstats = input("Please enter 'yes' or 'no'")  
        if viewuserstats.lower() == 'yes':    
            user_stats(df)


        viewfivelines= input('\nWould you like to view five lines of raw data? Enter yes or no.\n')
        while str.lower(viewfivelines) not in ['yes', 'no']:
            viewfivelines = input("Please enter 'yes' or 'no'")  
        while viewfivelines.lower() == 'yes':   
            next_five_lines(df)
            viewfivelines= input('\nWould you like to view five further lines of raw data? Enter yes or no.\n')
            while str.lower(viewfivelines) not in ['yes', 'no']:
                viewfivelines= input('\nEnter yes or no.\n')



        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

