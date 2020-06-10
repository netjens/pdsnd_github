import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june','july','august','september','october','november','december']

DAYS =  ['monday', 'tuesday', 'wednesday','thursday','friday','saturday','sunday']

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
    while True:
        try:
            city = input('Enter the name of the city to analyze:').lower()
            if city in ['new york city','chicago','washington']:
                break
            else:
                print('you entered an unknown city, please choose between chicago, new york city and washington')
        except KeyboardInterrupt:
            print('aboard input')
            break
    
    while True:
        try:
            month = input('Enter the name of the months (january to december) to analyze, or enter all for all months:').lower()
            if month in MONTHS or month == 'all':
                break
            else:
                print('you entered an unknown month,  enter (january to december) to analyze, or enter all for all months')
        except KeyboardInterrupt:
            print('aboard input')
            break
        except ValueError:
            print('Your input is invalid! ')

    while True:
        try:
            day = input('Enter the day of week (all, monday, tuesday, ... sunday)').lower()
            if day in DAYS or day =='all':
                break
            else:
                print('you entered an unknown day,  valid are all, monday, tuesday, ... sunday')
        except KeyboardInterrupt:
            print('aboard input')
            break
        except ValueError:
            print('Your input is invalid! It has to be a day of week (all, monday, tuesday, ... sunday)')
 



    print('-'*40)
    return city, month, day


def load_data(city, month, day):
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

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        
        month =MONTHS.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
  
    # display the most common month
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract hour from the Start Time column to create an hour column
    df['month'] = df['Start Time'].dt.month
    # find the most popular month
    popular_month = df['month'].mode()[0]
    print('Most Popular Month:', MONTHS[popular_month-1])

    #display the most common day of week
    # extract day from the Start Time column to create an hour column
    df['dayofweek'] = df['Start Time'].dt.dayofweek
    # find the most popular hour
    popular_dayofweek = df['dayofweek'].mode()[0]
    print('Most Popular Day of Week:', DAYS[popular_dayofweek])

    #display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    # find the most popular hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station:',popular_start_station)

    #display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station:',popular_end_station)

    #display most frequent combination of start station and end station trip
    df_combination = df['Start Station'] + df['End Station']
    popular_combination = df_combination.mode()[0]
    print('Most Popular combination of start station and end station trip:',popular_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #display total travel time
    df['Travel Time'] = pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])
    total_travel_time = df['Travel Time'].sum()
    print('Total Travel Time:', total_travel_time)
    

    #display mean travel time
    mean_travel_time = df['Travel Time'].mean()
    print('Mean Travel Time:', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    for x in range(len(user_types.axes[0])):     
        print('user type %s has %s counts' % (user_types.axes[0][x] ,user_types.values[x]))
    

    #Display counts of gender
    if 'Gender' in df.keys():
        genders = df['Gender'].value_counts()
        for x in range(len(genders.axes[0])):     
            print('gender %s has %s counts' % (genders.axes[0][x] ,genders.values[x]))
    else:
        print('no Gender-data available in data')

    if 'Birth Year' in df.keys():
        #Display earliest, most recent, and most common year of birth
        earliest_birthyear = df['Birth Year'].min()
        print('earliest birthyear is %s' % int(earliest_birthyear))

        mostrecent_birthyear = df['Birth Year'].max()
        print('most recent birthyear is %s' % int(mostrecent_birthyear))

        mostcommon_birthyear = df['Birth Year'].mode()
        print('most common birthyear is %s' % int(mostcommon_birthyear))
    else:
        print('no Birth Year data available')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def display_data(df):
    """Displays raw data on bikeshare users."""
    print(df.iloc[:5])


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
    
    while True:
        wantToSeeRawData = input('\nDo you want to see 5 lines of raw data? Enter yes or no.\n')
        if wantToSeeRawData.lower() == 'no':
            break
        #to clear up own data-frame columns, fresh data load
        df = load_data(city, month, day)
        display_data(df)

if __name__ == "__main__":
	main()
