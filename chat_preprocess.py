import pandas as pd
import re

def timeconvert(s):
    if s[-2:].upper() == "AM" :
        if s[:2] == '12':
            s = str('00' + s[2:-2])
        else:
            s = s[:-2]
    else:
        if s[:2] == '12':
            s = s[:-2]
        else:
            s = str(int(s[:2]) + 12)+s[2:-2]
    return s


def chat_preprocessor(file_data,timestamp_type,time_format):
    
    if(time_format == "24 hr"):
        msg_pattern = '\d{1,4}/\d{1,4}/\d{1,4},\s\d{1,2}:\d{2}\s-\s'
        messages = re.split(msg_pattern,file_data)[1:]
        dates = re.findall(msg_pattern, file_data)
    elif(time_format == "12 hr"):
        msg_pattern = '\d{1,4}/\d{1,4}/\d{1,4},\s\d{1,2}:\d{1,2}\s[aApP][mM]\s-\s'
        ampm_pattern = '\d{1,2}:\d{1,2}\s[aApP][mM]'
        messages = re.split(msg_pattern,file_data)[1:]
        dates = re.findall(msg_pattern,file_data)
        ampm_time = re.findall(ampm_pattern, str(dates))
        
        for i in range(len(messages)):
            string1 = dates[i]
            substring1 = ","
            if substring1 in string1:
                result = string1.index(substring1)
                dates[i] = dates[i][:result]
            string2 = ampm_time[i][:2]
            substring2 = ":"
            if substring2 in string2:
                var1 = "0"
                ampm_time[i] = "".join([var1, ampm_time[i]])
            ampm_time[i] = timeconvert(ampm_time[i])
            dates[i] = (dates[i] + ", " + ampm_time[i] + " - ")
                
        
        
                

    
    df = pd.DataFrame({'Member_Messages' : messages, 'message_date' : dates})
    
    if (timestamp_type == 'DD/MM/YYYY'):
        df['message_date'] = pd.to_datetime(df['message_date'], format= '%d/%m/%Y, %H:%M - ') 
    elif (timestamp_type == 'MM/DD/YYYY'):
        df['message_date'] = pd.to_datetime(df['message_date'], format= '%m/%d/%Y, %H:%M - ')
    elif (timestamp_type == 'YYYY/DD/MM'):
        df['message_date'] = pd.to_datetime(df['message_date'], format= '%Y/%d/%m, %H:%M - ')
    elif (timestamp_type == 'YYYY/MM/DD'):
        df['message_date'] = pd.to_datetime(df['message_date'], format= '%Y/%m/%d, %H:%M - ')   
    elif (timestamp_type == 'DD/MM/YY'):
        df['message_date'] = pd.to_datetime(df['message_date'], format= '%d/%m/%y, %H:%M - ')
    elif (timestamp_type == 'MM/DD/YY'):
        df['message_date'] = pd.to_datetime(df['message_date'], format= '%m/%d/%y, %H:%M - ')
    elif (timestamp_type == 'YY/MM/DD'):
        df['message_date'] = pd.to_datetime(df['message_date'], format= '%y/%m/%d, %H:%M - ')
    elif (timestamp_type == 'YY/DD/MM'):
        df['message_date'] = pd.to_datetime(df['message_date'], format= '%y/%d/%m, %H:%M - ')
    
    members = []
    messages = []
    for message in df['Member_Messages']:
        entry = re.split('([\w\W]+?):\s', message)
        if (entry[1:]):
            K = 1 #kth occurrence
            n, m = message.split(":", K)
            members.append(n)
            messages.append(m)
        else:
            members.append('Group Notification')
            messages.append(entry[0])
            
    df['Member'] = members
    df['Message'] = messages
    df.drop(columns=['Member_Messages'], inplace=True)
    
    df['Year'] = df['message_date'].dt.year
    df['Month'] = df['message_date'].dt.month
    df['Month_Name'] = df['message_date'].dt.month_name()
    df['Day'] = df['message_date'].dt.day
    df['Day_Name'] = df['message_date'].dt.day_name()
    df['Hours'] = df['message_date'].dt.hour
    df['Minute'] = df['message_date'].dt.minute
    
    df.drop(columns=['message_date'], inplace=True)
    
    period = []
    for hour in df[['Day_Name', 'Hours']]['Hours']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour+1))
        else:
            period.append(str(hour) + "-" + str(hour+1))
            
    df['Period'] = period
    
    return df