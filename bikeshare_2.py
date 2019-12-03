import time
import pandas as pd
import numpy as np

# Global variarbles ----------------------
# CITY_DATA stores a dictionary of cities as keys with their corresponding data files as values
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
    cities = ['chicago', 'Chicago', 'New York City', 'new york city', 'washington', 'Washington']
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while True:
        try:
            city = input('Please enter a city to search (Chicago, New York City, or Washington) ')
            if city in cities:
                break
            else:
                print('please enter a valid city name (Chicago, New York City, or Washington)')
        except ValueError:
            print('Please enter a valid city')

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input('Please enter a month or type "all" for full analysis ')
            if month in months:
                break
            else:
                print('please enter a valid month, you can choose from; january, february, march, april, may, june, or all')
        except ValueError:
            print('Please enter a valid month')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input('Please enter a day of the week or type "all" for full analysis ')
            if day in days:
                break
            else:
                print('please enter a valid day of the week, you can chose from; monday, tuesday, wednesday, thursday, friday, saturday, sunday, or all')
        except ValueError:
            print('Please enter a valid day of the week')


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
    # Loads the data for the city specified by the user
    df = pd.read_csv(CITY_DATA[city.lower()])

    # Converts the Start Time field into a datetime data type
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from datetime field for new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # Filter by Month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

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
    popular_month = df['month'].mode()[0]
    print('Most Frequent Month:', popular_month)

    # display the most common day of week
    popular_dow = df['day_of_week'].mode()[0]
    print('Most Frequent Day of the Week:', popular_dow)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Frequent Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station: ', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station: ', popular_end_station)

    # display most frequent combination of start station and end station trip
    df['start_stop'] = df['Start Station'] + ', ' + df['End Station']
    popular_combination = df['start_stop'].mode()[0]
    print('Most Popular Start and End Station combination: ', popular_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time: {0: .2f}'.format(total_travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean Travel Time: {0: .2f}'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Customers by type')
    print(user_types)

    # Display counts of gender
    try:
        genders = df['Gender'].value_counts()
        print('Customers by gender')
        print(genders)
    except:
        print('No gender data')

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_birth_year = df['Birth Year'].min()
        most_recent_year = df['Birth Year'].max()
        most_common_year = df['Birth Year'].mode()[0]
        print('Customer birth year statistics')
        print('Earliest Birth Year: ', int(earliest_birth_year))
        print('Most Recent Birth Year: ',int(most_recent_year))
        print('Most Common Birth Year: ', int(most_common_year))
    except:
        print('No birth year data')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_raw_data(df):
    """Displays raw trip data"""

    # reset the dataframe to original columns
    df = df.drop(columns=['start_stop'])

    x = 0
    # loop asks the user if they want to see trip data and displays 5 rows of data
    while True:
        try:
            choice = input('Would you like to see ride information? [yes/no] ')
            if choice in ['yes', 'no', 'Yes', 'No']:
                if choice.lower() != 'no':
                    for i in range(5):
                        print('\n', df.iloc[x])
                        x+=1
                else:
                    break

        except:
            print('please select [y/n] ')



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
