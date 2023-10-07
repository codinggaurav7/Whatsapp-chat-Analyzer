import pandas as pd
from collections import Counter
from urlextract import URLExtract
from wordcloud import WordCloud
import emoji

extractor = URLExtract()

def fetch_repo(member_selected,df):
    
    if member_selected != 'All Users':
        df = df[df['Member'] == member_selected]
        
    message_num = df.shape[0]   
    
    words = []
    for message in df['Message']:
        words.extend(message.split())

    media_num = df[df['Message'] == ' <Media omitted>\n'].shape[0]
        
    links = []
    for message in df['Message']:
        links.extend(extractor.find_urls(message))
        
    return message_num, len(words), media_num, len(links)


def fetch_busyMember(df):
    x = df['Member'].value_counts().head()
    df = round((df['Member'].value_counts() / df.shape[0])*100,2).reset_index().rename(columns={'index':'Name', 'Member':'%'})
    return x,df

def prep_wordcloud(member_selected,df):
    
    if member_selected != 'All Users':
        df = df[df['Member'] == member_selected]
        
    #df['Message'] = df['Message'].str.replace(' <Media omitted>\n', '') 
    temp1 = df[df['Member'] != 'Group Notification']
    temp1 = temp1[temp1['Message'] != ' <Media omitted>\n']
    
    if temp1.empty:
        return "No messages sent by member.\n(Media messages not included)" 
    else:
        wc = WordCloud(width=500,height=500,min_font_size=11,background_color='white')
        df_wc = wc.generate(temp1['Message'].str.cat(sep=" "))
        return df_wc
    

def mostCommon_words(member_selected,df):
    
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()
    
    if member_selected != 'All Users':
        df = df[df['Member'] == member_selected]
    
    temp = df[df['Member'] != 'Group Notification']
    temp = temp[temp['Message'] != ' <Media omitted>\n']
    
    words=[]
    
    for message in temp['Message']:
        message.replace(" ","")
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)   
                
    common_words_df = pd.DataFrame(Counter(words).most_common(25))
    return common_words_df
                
def emoji_count(member_selected,df):
    if member_selected != 'All Users':
        df = df[df['Member'] == member_selected]
        
    emojis =[]
    
    for message in df['Message']:
        emojis.extend([x for x in message if x in emoji.UNICODE_EMOJI['en']])
        
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    emoji_df.columns = ['Emoji','Count']
    return emoji_df

def year_timeline(member_selected,df):
    if member_selected != 'All Users':
        df = df[df['Member'] == member_selected]
        
    timeline = df.groupby(['Year','Month','Month_Name']).count()['Message'].reset_index()
    time = []
    
    for i in range(timeline.shape[0]):
        time.append(timeline['Month_Name'][i] + "-" + str(timeline['Year'][i]))
    
    timeline['Time'] = time
    
    return timeline


def week_timeline(member_selected,df):
    if member_selected != 'All Users':
        df = df[df['Member'] == member_selected]
        
    return df['Day_Name'].value_counts()


def month_timeline(member_selected,df):
    if member_selected != 'All Users':
        df = df[df['Member'] == member_selected]
        
    return df['Month_Name'].value_counts()

def activity_heatmap(member_selected,df):
    if member_selected != 'All Users':
        df = df[df['Member'] == member_selected]

    user_heatmap = df.pivot_table(index='Day_Name', columns='Period', values='Message', aggfunc='count').fillna(0)

    return user_heatmap