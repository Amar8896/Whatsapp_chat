import re
import pandas as pd

#function which create dataframe and extract useful data and return the dataframe

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # creating a new dataframe for user and date
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Converting the msg datatype into date format
    df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %H:%M - ')

    # renaming the 'message_date to date'
    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['users'] = users
    df['message'] = messages
    # removing the old column 'user_message'
    df.drop(columns=['user_message'], inplace=True)

    df['daily_date'] = df['date'].dt.date
    # creating new column in df
    df['Year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    # creating new column in df as month
    df['Month'] = df['date'].dt.month_name()
    # creating new column as Day
    df['Day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df
