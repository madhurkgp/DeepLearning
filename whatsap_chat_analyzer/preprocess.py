import numpy as np
import seaborn as sn
import pandas as pd
import re


def gettimeanddate(string):
    string = string.split(',')
    date, time = string[0], string[1]
    time = time.split('-')
    time = time[0].strip()
    
    # Remove AM/PM if present and clean up
    time = re.sub(r'\s*(am|pm|AM|PM)', '', time)
    
    # Handle special Unicode characters and normalize
    time = time.replace('\u202f', ' ')  # Replace narrow space with normal space
    
    return date+" "+time


def getstring(text):
    return text.split('\n')[0]


def preprocess(data):

    # Updated pattern to handle various WhatsApp formats including AM/PM and special characters
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s*(?:am|pm|AM|PM)?\s*-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_messages': messages,
                       'message_date': dates})

    df['message_date'] = df['message_date'].apply(
        lambda text: gettimeanddate(text))
    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []

    for message in df['user_messages']:
        # Handle multi-line messages and special characters
        message = message.strip()
        if not message:
            users.append('Group Notification')
            messages.append('')
            continue
            
        # Split on first colon to separate user and message
        parts = message.split(':', 1)
        if len(parts) >= 2:
            user = parts[0].strip()
            msg = parts[1].strip()
            
            # Clean up user names (remove special characters)
            user = re.sub(r'^[~\s]+', '', user)  # Remove ~ and spaces from start
            
            users.append(user)
            messages.append(msg)
        else:
            users.append('Group Notification')
            messages.append(message)

    df['User'] = users
    df['message'] = messages

    df['message'] = df['message'].apply(lambda text: getstring(text))

    df = df.drop(['user_messages'], axis=1)
    df = df[['message', 'date', 'User']]

    df = df.rename(columns={'message': 'Message',
                            'date': 'Date'})

    # Convert to datetime and extract features
    try:
        df['Only date'] = pd.to_datetime(df['Date']).dt.date
        df['Year'] = pd.to_datetime(df['Date']).dt.year
        df['Month_num'] = pd.to_datetime(df['Date']).dt.month
        df['Month'] = pd.to_datetime(df['Date']).dt.month_name()
        df['Day'] = pd.to_datetime(df['Date']).dt.day
        df['Day_name'] = pd.to_datetime(df['Date']).dt.day_name()
        df['Hour'] = pd.to_datetime(df['Date']).dt.hour
        df['Minute'] = pd.to_datetime(df['Date']).dt.minute
    except:
        # Fallback if datetime parsing fails
        df['Only date'] = None
        df['Year'] = None
        df['Month_num'] = None
        df['Month'] = None
        df['Day'] = None
        df['Day_name'] = None
        df['Hour'] = None
        df['Minute'] = None

    return df
