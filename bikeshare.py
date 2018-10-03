import time
import pandas as pd
import numpy as np
import calendar as cal
import matplotlib.pyplot as plt
pd.set_option('display.width', 1000)

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    '''This function is used to gather input from users. '''

    print('WELCOME TO BIKESHARE ANALYSIS')

    months = list(cal.month_name)[1:]
    cities = list(CITY_DATA.keys())
    days = list(cal.day_name)

    while True:
        try:
            city = input('Enter the name of the city to study its bikeshare data: Please choose from chicago / new york city / washington only:').strip().lower()
            if city not in cities:
                raise ValueError('Please enter cities from: {}'.format(cities))
            #end if
            month = input('Enter the month: ').strip().lower().title() # get user input for month (all, january, february, ... , june)
            if month != 'All' and month not in months:
                raise ValueError('Please enter months from: {}'.format(months))
            #end if
            day = input('Enter a day: ').strip().lower().title() # get user input for day of week (all, monday, tuesday, ... sunday)
            if day != 'All' and day not in days:
                raise ValueError('Please enter weekday from: {}'.format(days))
            #end if
            print('-'*40)
            return city.lower(), month.lower(), day.lower()
        except ValueError as ex:
            print (str(ex))

def load_data(city, month, day):

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['month_name'] = df['Start Time'].apply(lambda x: months[x.month -1].title()) #this will add an extra column for month name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month)
        # filter by month to create the new dataframe
        df = df.loc[df['month'] == (month + 1)]
    #end of if :

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df.loc[df['Start Time'].dt.weekday_name == day.title()]
    #end of if
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month_name'].mode()[0]
    print ('The most common month is {}'. format(most_common_month))

    # display the most common day of week
    most_common_day_of_week = df['day_of_week'].mode()[0]
    print ('The most common day of week is {}'. format(most_common_day_of_week))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_start_hour = df['hour'].mode()[0]
    print ('The most common start hour is {}'. format(most_common_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_commonly_used_start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station is: {}'.format(most_commonly_used_start_station))

    # display most commonly used end station
    most_commonly_used_end_station = df['End Station'].mode()[0]
    print('The most commonly used end station is: {}'.format(most_commonly_used_end_station))

    # display most frequent combination of start station and end station trip
    df['pair'] = (df['Start Station'] + ' ---> ' + df['End Station'])
    most_common_station_pair = df['pair'].mode()[0]
    print ('The most common station pair is: {}'.format(most_common_station_pair))

    # call function plot_station_usage to display Ridership for Most Popular Start & End Station
    plot_station_usage(df,most_commonly_used_start_station,most_commonly_used_end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
#end of function

def plot_station_usage(df,start_station,end_station):
    '''Displays a graph for Ridership for Most Popular Start & End Station'''

    fig = plt.figure() #Display the name of the graph in window title
    fig.canvas.set_window_title('Ridership for Most Popular Start & End Station')

    df['hour'] = df['Start Time'].dt.hour

    dfcopy = df[df['Start Station'] == start_station]
    start_stn_riders = dfcopy.groupby('hour').count()['User Type']

    dfcopy = df[df['End Station'] == end_station]
    end_stn_riders = dfcopy.groupby('hour').count()['User Type']

    line_riders = plt.plot(start_stn_riders, label = 'start station: {}'.format(start_station))
    line_eriders = plt.plot(end_stn_riders, label = 'end station: {}'.format(end_station))

    plt.title('Ridership for Most Popular Start & End Station')
    plt.xlabel('Hour of Day')
    plt.ylabel('Riders')
    plt.legend()
    plt.show()

#end of function

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['total_time'] = df['End Time'] - df['Start Time']
    total_travel_time = df['total_time'].sum()
    print ('Total Travel Time is: {}'.format(total_travel_time))

    # display mean travel time
    mean_travel_time = df['total_time'].mean()
    print ('Mean Travel Time is: {}'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
#end of function

def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print ('The User Types are:\n{}\n'.format(user_types))

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_type = df['Gender'].value_counts()
        print ('The gender types are:\n{}\n'.format(gender_type))
    else:
        print ('The city of {} does not record gender of riders'.format(city))

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        most_common_birth_year = df['Birth Year'].mode()[0]
        earliest_birth_year = df['Birth Year'].min()
        most_recent_birth_year = df['Birth Year'].max()
        print('Most Common Year of Birth is: {}'.format(most_common_birth_year))
        print ('Earliest Year of Birth is: {}'.format(earliest_birth_year))
        print('Most Recent Year of Birth is: {}'.format(most_recent_birth_year))
    else:
        print ('The city of {} does not record birth year of riders'.format(city))

    #hourly_gender_distribution function is called
    hourly_gender_distribution(df,city)

    print ("\nThis took %s seconds." % (time.time() - start_time))
    print ('-'*40)
#end of function

def hourly_gender_distribution(df,city):
    '''Display dataframe showing distribution of males and females hourly'''

    if 'Gender' in df.columns:
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['hour'] = df['Start Time'].dt.hour
        df['male'] = df['Gender'].apply(lambda x: 1 if x == 'Male' else 0)
        df['female'] = df['Gender'].apply(lambda x: 1 if x == 'Female' else 0)

        male_distribution = df.groupby('hour').sum()['male']
        female_distribution = df.groupby('hour').sum()['female']
        gender_distribution_df = pd.concat([male_distribution, female_distribution], axis=1)
        print('\nHourly Gender Distribution:')
        print (gender_distribution_df)

        #plot the distribution
        fig = plt.figure() #Display the name of the graph in window title
        fig.canvas.set_window_title('Hourly Gender Distribution')
        line_male = plt.plot(male_distribution, label='Male Riders')
        line_female = plt.plot(female_distribution, label='Female Riders')
        plt.title('Hourly Gender Distribution')
        plt.xlabel('Hour of Day')
        plt.ylabel('Riders')
        plt.legend()
        plt.show()

    else:
        print ('The city of {} does not record gender of riders'.format(city))
#end of function

def raw_data_view_optional(df):
    '''Display raw data in ten rows and ask the user wants to view next 10 rows.'''

    #drop extra columns added and display raw data properly
    df = df.copy()
    extra_cols = ['male', 'female', 'pair', 'total_time', 'hour', 'month_name', 'month', 'day_of_week']
    df = df.drop(extra_cols, errors='ignore', axis=1)

    raw_data = input('There are {} rows. Do you want to view raw data (y/n)?'.format(len(df)))
    next_row = 0
    blocksize = 10 #display rows in blocks of 10

    while raw_data == 'y':
        next_slice = df[next_row : next_row + blocksize]
        if len(next_slice) == 0:
            print ('No more raw data to print.')
            break
        next_row = next_row + blocksize
        print (next_slice)
        raw_data = input('Do you want to view more raw data (y/n)?')
        #print next 10 rows if there are no more rows to display else exit.
#end of function

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        #if statement handles missing columns for cities (example: Washington city has no records for riders gender and birth year)
        if len(df) == 0:
            print('There is no data for this selection.')
        else:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df,city)
            raw_data_view_optional(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
