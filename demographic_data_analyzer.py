import pandas as pd


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv('adult.data.csv')

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df.groupby('race').race.count().sort_values(ascending = False)

    # What is the average age of men?
    average_age_men = round(df.groupby('sex').age.mean()["Male"], 1)

    # What is the percentage of people who have a Bachelor's degree?
    percentage_bachelors = round(df.groupby('education').education.count()['Bachelors'] / df.shape[0] * 100, 1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    df_high_ed = df[(df['education'] == 'Bachelors') | (df['education'] == 'Masters') | (df['education'] == 'Doctorate')]

    df_high_ed_sal = df_high_ed[df_high_ed['salary'] == '>50K']
    # What percentage of people without advanced education make more than 50K?
    df_low_ed = df[(df['education'] != 'Bachelors') & (df['education'] != 'Masters') & (df['education'] != 'Doctorate')]

    df_low_ed_sal = df_low_ed[df_low_ed['salary'] == '>50K']

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_education = df_high_ed.shape[0]
    lower_education = df_low_ed.shape[0]

    # percentage with salary >50K
    higher_education_rich = round(df_high_ed_sal.shape[0] / df_high_ed.shape[0] * 100, 1)

    lower_education_rich = round(df_low_ed_sal.shape[0] / df_low_ed.shape[0] * 100, 1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df['hours-per-week'].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    num_min_workers = df[df['hours-per-week'] == 1]
    num_min_rich = num_min_workers[num_min_workers['salary'] == '>50K']


    rich_percentage = round(num_min_rich.shape[0] / num_min_workers.shape[0] * 100, 1)

    # What country has the highest percentage of people that earn >50K?
    countries_sal_sum = df.groupby(['native-country', 'salary']).age.count().reset_index()

    countries_pivot = countries_sal_sum.pivot(index='native-country', columns='salary', values='age')
    countries_pivot['>50K'] = countries_pivot['>50K'].fillna(0.0)

    countries_pivot['rich_per'] = round(countries_pivot['>50K'] / (countries_pivot['<=50K'] + countries_pivot['>50K']) * 100, 1)

    highest_earning_country = countries_pivot[countries_pivot['rich_per'] == countries_pivot['rich_per'].max()].index.values[0]
    
    highest_earning_country_percentage = countries_pivot['rich_per'].max()

    # Identify the most popular occupation for those who earn >50K in India.
    india = df[(df['native-country'] == 'India') & (df['salary'] == '>50K')]

    india_occ = india.groupby('occupation').salary.count().reset_index()

    top_IN_index = india_occ[india_occ['salary'] == india_occ['salary'].max()].index.values[0]

    top_IN_occupation = india_occ['occupation'].iloc[top_IN_index]

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
