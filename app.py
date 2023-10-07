import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import chat_preprocess, report_generator

st.sidebar.title("WhatsApp Chat Analyzer")

timestamp_list = ['DD/MM/YYYY','MM/DD/YYYY','YYYY/MM/DD','YYYY/DD/MM','DD/MM/YY','MM/DD/YY','YY/MM/DD','YY/DD/MM']

timestamp_type = st.sidebar.selectbox("Choose Timestamp format",timestamp_list)

time_format_list = ["24 hr","12 hr"]

time_format = st.sidebar.selectbox("Choose Time format",time_format_list)

uploaded_file = st.sidebar.file_uploader("Choose a file")

try:

    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode("utf-8")
        df = chat_preprocess.chat_preprocessor(data,timestamp_type,time_format)
        
        member_list = df['Member'].unique().tolist()
        for i in member_list:
           if (i=='Group Notification'): 
               member_list.remove('Group Notification')
        member_list.sort()
        member_list.insert(0,'All Users')
        
        member_selected = st.sidebar.selectbox("Analyze chat with particular user", member_list)
        
        if st.sidebar.button("Show Report"):
            
            st.title("TOP STATS")
            message_num,t_words,t_media,t_links = report_generator.fetch_repo(member_selected,df)
            
            col1, col2, col3, col4 = st.columns(4)
            
            #general Stats
            
            with col1:
                st.header('Messages')
                st.title(message_num)
            
            with col2:
                st.header('Words')
                st.title(t_words)
                
            with col3:
                st.header('Media')
                st.title(t_media)
                
            with col4:
                st.header('Links')
                st.title(t_links)
             
            
            #Data - Yearwise
            st.title("Monthly Time-Line")
            timeline = report_generator.year_timeline(member_selected, df)
            fig,ax = plt.subplots()
            ax.plot(timeline['Time'],timeline['Message'],color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            
            
            st.title("Activity")
            col1, col2 = st.columns(2)
            
            #week wise
            with col1:
                st.header("Most Active Day")
                active_day = report_generator.week_timeline(member_selected, df)
                fig,ax = plt.subplots()
                ax.bar(active_day.index, active_day.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
                
            #month wise
            with col2:
                st.header("Most Active Month")
                active_month = report_generator.month_timeline(member_selected, df)
                fig,ax = plt.subplots()
                ax.bar(active_month.index, active_month.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            
            st.header("Activity map wrt Time & Day")
            user_heatmap = report_generator.activity_heatmap(member_selected,df)
            fig,ax = plt.subplots()
            ax = sns.heatmap(user_heatmap)
            st.pyplot(fig)
                
            #Busy members
            
            if member_selected == 'All Users':
                st.title('Most Active Member')
                x,per_df = report_generator.fetch_busyMember(df)
                fig, ax = plt.subplots()
                
                col1, col2 = st.columns(2)
                
                with col1:
                    ax.bar(x.index, x.values,color='orange')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)
                
                with col2:
                    st.dataframe(per_df)
             
            #wordcloud   
            
            st.title('Word Cloud')
            df_wc = report_generator.prep_wordcloud(member_selected, df)
            if (df_wc == "No messages sent by member.\n(Media messages not included)"):
                st.header("No messages sent by member.\n(Media messages not included)")
            else:
                fig, ax = plt.subplots()
                ax.imshow(df_wc)
                st.pyplot(fig)
            
            #Common words
            
            st.title("Most Common Words")
            common_words_df = report_generator.mostCommon_words(member_selected, df)
            fig,ax = plt.subplots()
            ax.barh(common_words_df[0],common_words_df[1],color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            
            #Emoji count
            
            st.title("Emoji Count")
            emoji_df = report_generator.emoji_count(member_selected, df)
            if emoji_df.empty:
                st.header("No emoji sent by user")
            else:
                st.dataframe(emoji_df)

except:
    st.error("Time-Stamp format error")
    st.header("Time-Stamp format error")
    st.header("Possible Reasons:")
    st.header("1.Time stamp format chosen incorrectly.")
    st.header("2.File does not have a time-stamp.")
    st.stop()