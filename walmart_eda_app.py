import streamlit as st
import pandas as pd
import numpy as np
import base64 
import time
from datetime import date
import warnings
warnings.filterwarnings("ignore")
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

timestr = time.strftime("%Y%m%d-%H%M%S")

def csv_downloader(data, file_name):
    csvfile = data.to_csv()
    b64 = base64.b64encode(csvfile.encode()).decode()
    new_filename = "{}_{}.csv".format(file_name,timestr)
    st.markdown("#### Download File ###")
    href = f'<a href="data:file/csv;base64,{b64}" download="{new_filename}">Click Here!!</a>'
    st.markdown(href, unsafe_allow_html=True)

def read_csv(uploaded_file):
    df_read = pd.read_csv(uploaded_file)
    if 'Unnamed: 0' in df_read.columns:
        df_read.drop('Unnamed: 0', axis=1, inplace=True)
    return df_read

def find_outliers_range(data, factor):
    Q1 = np.percentile(data, 25)
    Q3 = np.percentile(data, 75)
    IQR = Q3 - Q1
    low_lim = Q1 - factor * IQR
    up_lim = Q3 + factor * IQR
    return low_lim, up_lim

def short_tactic_type(choice):
    return choice.split('_')[-1]

axis_name_dict = {'IMP': 'Impressions', 'CLK': 'Clicks', 'SPEND': 'Spends ($)'}
    

def main():
    menu = ['Plotting','Pre-processing & Summary', 'Exploratory Data Analysis','Miscellaneous']
    choice = st.sidebar.selectbox('Menu', menu)
    
    var_click = [
        'M_SP_AB_CLK', 'M_SP_KWB_CLK', 'M_SBA_CLK', 'M_SP_VIDEO_CLK'
    ]
    var_imp = [
        'M_ON_DIS_AT_IMP', 'M_ON_DIS_CT_IMP', 'M_ON_DIS_CATTO_IMP', 'M_ON_DIS_KW_IMP', 'M_ON_DIS_ROS_IMP',
        'M_ON_DIS_HPLO_IMP', 'M_ON_DIS_APP_HPLO_IMP', 'M_ON_DIS_HPTO_IMP', 'M_ON_DIS_HPGTO_IMP', 'M_ON_DIS_HP_IMP',
        'M_OFF_DIS_FB_IMP', 'M_OFF_DIS_PIN_IMP', 'M_OFF_DIS_DSP_CTV_IMP', 'M_OFF_DIS_WN_WITHOUTCTV_IMP', 'M_INSTORE_TV_WALL_IMP'
    ]
    var_spend = [
        'M_SP_AB_SPEND', 'M_SP_KWB_SPEND', 'M_SBA_SPEND', 'M_SP_VIDEO_SPEND', 'M_ON_DIS_AT_SPEND', 'M_ON_DIS_CT_SPEND',
        'M_ON_DIS_CATTO_SPEND', 'M_ON_DIS_KW_SPEND', 'M_ON_DIS_ROS_SPEND', 'M_ON_DIS_HPLO_SPEND', 'M_ON_DIS_APP_HPLO_SPEND',
        'M_ON_DIS_HPTO_SPEND', 'M_ON_DIS_HPGTO_SPEND', 'M_ON_DIS_HP_SPEND', 'M_OFF_DIS_FB_SPEND', 'M_OFF_DIS_PIN_SPEND',
        'M_OFF_DIS_DSP_CTV_SPEND', 'M_OFF_DIS_WN_WITHOUTCTV_SPEND', 'M_INSTORE_TV_WALL_SPEND'
    ]
    var_rate = [
        'M_SP_AB_CPC', 'M_SP_KWB_CPC', 'M_SBA_CPC', 'M_SP_VIDEO_CPC', 'M_ON_DIS_AT_CPM', 'M_ON_DIS_CT_CPM',
        'M_ON_DIS_CATTO_CPM', 'M_ON_DIS_KW_CPM', 'M_ON_DIS_ROS_CPM', 'M_ON_DIS_HPLO_CPD', 'M_ON_DIS_APP_HPLO_CPD',
        'M_ON_DIS_HPTO_CPD', 'M_ON_DIS_HPGTO_CPD', 'M_ON_DIS_HP_CPD', 'M_OFF_DIS_FB_CPM', 'M_OFF_DIS_PIN_CPM',
        'M_OFF_DIS_DSP_CTV_CPM', 'M_OFF_DIS_WN_WITHOUTCTV_CPM', 'M_INSTORE_TV_WALL_CPM'
    ]

    if choice == 'Plotting':
        st.subheader('Analyze Tactic')
        choice1 = st.multiselect('Clicks', var_click)
        choice2 = st.multiselect('Impressions', var_imp)
        choice3 = st.multiselect('Spends', var_spend)
        choice4 = st.multiselect('Rates', var_rate)

        uploaded_file1 = st.file_uploader("Upload Aggbrand Stack", type="csv")
        if uploaded_file1 is not None:
            dfa = read_csv(uploaded_file1)
            # st.write(dfa.head())

        if st.button('Plot'):
            # st.write(choice2)
            choices1 = list(set(choice1 + choice2 + choice3 + choice4))
          
            fig = make_subplots()
            colors = ['green', 'yellow', 'orange', 'blue', 'red', 'purple', 'brown', 'pink', 'gray', 'cyan']
            if len(choices1) > 0:
                # fig = px.line(dfa, x='INDEX', y=choices1)
                fig = px.line(dfa, x='INDEX', y=choices1)
                # for i, column in enumerate(choices1):
                #     fig.add_scatter(x=dfa['INDEX'], y=dfa[column], mode='lines', line=dict(color=colors[i % len(colors)]))
                fig.update_layout(
                    # title='Line Plot with Date Column as X-axis',
                    xaxis_title='Date',
                    yaxis_title='Value',
                    legend_title='Columns',
                    width=900,
                    height=600
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.write("Please select at least one column to display the plot.")

    elif choice == 'Pre-processing & Summary':
        with st.expander('Run Spends Rate fix'):
            uploaded_file7 = st.file_uploader("Upload Aggbrand Stack", type="csv")
            
            dfa = pd.DataFrame()
            if uploaded_file7 is not None:
                dfa = read_csv(uploaded_file7)
                st.success('Data uploaded successfully!')
            if st.button('Run'):
                with st.spinner('Running...'):
                    # Sleep for 5 seconds
                    time.sleep(2)
                st.success('Stack updated!!')
                csv_downloader(data=dfa, file_name='ABC'+' Modeling stack_spend_rate_fix')
                
        with st.expander('Generate EDA Summary'):
            col26,col27 = st.columns(2)
            with col26:
                modeling_start_date = st.date_input('Modeling Start Date', date(2021, 5, 1))
            with col27:
                modeling_end_date = st.date_input('Modeling End Date', date(2024, 1, 1))
            
            uploaded_file8 = st.file_uploader("Upload Aggbrand Stack ", type="csv")
            
            dfa = pd.DataFrame()
            if uploaded_file8 is not None:
                dfa = read_csv(uploaded_file8)
                st.success('Data uploaded successfully!')
            if st.button('Generate'):
                with st.spinner('Generating Summary...'):
                    # Sleep for 5 seconds
                    time.sleep(3)
                st.success('Summary is ready!')
                csv_downloader(data=dfa, file_name='ABC'+' Summary')

    elif choice == 'Exploratory Data Analysis':
        
        with st.expander('Outliers Analysis'):
            # st.subheader('Analyze Brands')
            col7,col8 = st.columns(2)
            with col7:   
                choice5 = st.selectbox('Select Clicks/Imp', var_click + var_imp)
            with col8:
                choice6 = st.selectbox('Select Spends', var_spend)

            col5, col6 = st.columns(2)
            with col5:
                modeling_start_date = st.date_input('Modeling Start Date', date(2021, 5, 1))
            with col6:
                modeling_end_date = st.date_input('Modeling End Date', date(2024, 1, 1))
            
            if 'uploaded_file2' not in st.session_state:
                st.session_state.uploaded_file2 = None
            if 'uploaded_file3' not in st.session_state:
                st.session_state.uploaded_file3 = None
            if 'fig' not in st.session_state:
                st.session_state.fig = None
            
            uploaded_file2 = st.file_uploader("Upload Aggbrand Stack", type="csv")
            
            dfa = pd.DataFrame()
            if uploaded_file2 is not None:
                dfa = read_csv(uploaded_file2)
                st.success('Data uploaded successfully!')
                dfa.columns = dfa.columns.str.upper()
                dfa['INDEX'] = pd.to_datetime(dfa['INDEX'])
                dfa = dfa[(dfa['INDEX'] >= pd.to_datetime(modeling_start_date)) & (dfa['INDEX'] <= pd.to_datetime(modeling_end_date))]
                # st.dataframe(dfa.head())
                st.session_state.uploaded_file2 = dfa

            if st.session_state.uploaded_file2 is not None:
                
                col9, col10, col11 = st.columns(3)
                with col9:
                    IQR_factor = st.number_input('Enter IQR factor', min_value=1.5,step=0.5)
                
                if len(dfa)!=0:    
                    imp_low, imp_up = find_outliers_range(dfa[choice5], factor=IQR_factor)
                    sp_low, sp_up = find_outliers_range(dfa[choice6], factor=IQR_factor)

                button1 = st.button('Plot')
                if button1:
                    
                    fig = make_subplots(specs=[[{"secondary_y": True}]])
                    fig.add_trace(go.Scatter(x=dfa['INDEX'], y=dfa[choice5], name=choice5, line=dict(color='#0071CE')), secondary_y=False)
                    fig.add_trace(go.Scatter(x=dfa['INDEX'], y=[imp_up] * len(dfa), name=axis_name_dict[short_tactic_type(choice5)] + ' Limit', line=dict(color='#0071CE', dash='dot')), secondary_y=False)
                    fig.add_trace(go.Scatter(x=dfa['INDEX'], y=dfa[choice6], name=choice6, line=dict(color='#FFC220')), secondary_y=True)
                    fig.add_trace(go.Scatter(x=dfa['INDEX'], y=[sp_up] * len(dfa), name=axis_name_dict[short_tactic_type(choice6)] + ' Limit', line=dict(color='#FFC220', dash='dot')), secondary_y=True)
                    fig.update_layout(
                        title="{} VS {}".format(axis_name_dict[short_tactic_type(choice5)], axis_name_dict[short_tactic_type(choice6)]),
                        xaxis_title="<b>Date<b>",
                        width=900,
                        height=600
                    )
                    # st.plotly_chart(fig, use_container_width=True)
        
                    st.session_state.fig = fig

                    if st.session_state.fig is not None:
                        st.plotly_chart(st.session_state.fig, use_container_width=True)

                
                    st.session_state.uploaded_file2 = dfa

                if st.session_state.uploaded_file2 is not None:
                    uploaded_file3 = st.file_uploader("Upload Cleanbrand Adv Stack", type="csv")
                    if uploaded_file3 is not None:
                        dfb = read_csv(uploaded_file3)
                        dfb.columns = dfb.columns.str.upper()
                        dfb['INDEX'] = pd.to_datetime(dfb['INDEX'])
                        dfb = dfb[(dfb['INDEX'] >= pd.to_datetime(modeling_start_date)) & (dfb['INDEX'] <= pd.to_datetime(modeling_end_date))]
                        # st.dataframe(dfb.head())
                        st.session_state.uploaded_file3 = dfb

                    if st.session_state.uploaded_file3 is not None:
                        # dfab = pd.merge(st.session_state.uploaded_file2, st.session_state.uploaded_file3, how='inner', on='INDEX')
                        # st.write("Dataframes Merged Successfully")
                        # st.dataframe(dfab.head())
                        # st.session_state.uploaded_file2 = dfab
                        df_temp = dfa[['INDEX','O_SALE',choice5,choice6]].copy()
                        
                        if short_tactic_type(choice5) == 'CLK':
                            df_temp['CPC ($)'] = df_temp[choice6]/df_temp[choice5]
                            rate_var = 'CPC'
                        
                        elif short_tactic_type(choice5) == 'IMP':
                            df_temp['CPM ($)'] = df_temp[choice6]/df_temp[choice5]*1000
                            rate_var = 'CPM'
                        # df_temp['Outlier'] = np.where(df_temp[choice5]>imp_up,'High '+axis_name_dict[short_tactic_type(choice5)],'')
                        
                        df_temp['Outlier'] = np.where((df_temp[choice5]>=imp_up)&(df_temp[choice6]>=sp_up),'High '+axis_name_dict[short_tactic_type(choice5)]+' & Spends',
                            
                            np.where(df_temp[choice5]>=imp_up,'High '+axis_name_dict[short_tactic_type(choice5)],\
                            np.where(df_temp[choice6]>=sp_up,'High '+axis_name_dict[short_tactic_type(choice6)],'')))
                        
                        
                        # uploaded_file3 = st.file_uploader("Upload Cleanbrand Stack", type="csv")
                        
                        # if uploaded_file3 is not None:
                        #     # file_details = {"FileName":uploaded_file2.name,"FileType":uploaded_file2.type}
                        #     dfb = read_csv(uploaded_file3)
                        #     st.dataframe(dfb.head())            
                        col12, col13, col14 = st.columns(3)
                        with col12:
                            num_brand = st.number_input('Num of Brands/Adv', min_value=3)
                        # button2 = st.checkbox('Analyze Brands')
                        
                        if st.button('Generate Summary'):
                                
                            outlier_dates = df_temp[df_temp['Outlier']!='']['INDEX'].tolist()
                            # st.write(outlier_dates)
                            
                            #a flag for adv_stack
                            adv_stack = False
                            if 'UNIQUE_ADV_NAME' in dfb.columns:
                                #for adv, creating other df
                                dfb = dfb[['INDEX','UNIQUE_BRAND_NAME','UNIQUE_ADV_NAME',choice5, choice6]]
                                adv_stack = True
                            else:
                                dfb = dfb[['INDEX','UNIQUE_BRAND_NAME',choice5, choice6]]
                            
                            with st.spinner('Generating Summary...'):
                                time.sleep(0.5)
                                # st.success('Forecast ready!')    
                            
                            
                            dfb = dfb[dfb['INDEX'].isin(outlier_dates)]
                            dfb_outlier_date = dfb[['INDEX',choice5, choice6]].groupby('INDEX',as_index=False).sum()   
                            dfb_outlier_date = dfb_outlier_date.rename(columns = {choice5:'Total '+choice5,choice6:'Total '+choice6}) 
                            # st.dataframe(df_temp_date)
                            dfb_outlier_brand = dfb.groupby(['INDEX','UNIQUE_BRAND_NAME'],as_index=False).sum()
                            
                            # st.dataframe(dfb_outlier_date)
                            # st.dataframe(dfb_outlier_brand)
                            df_temp2 = pd.merge(dfb_outlier_brand, dfb_outlier_date,on = 'INDEX',how='left')
                            
                            
                            #Finding top brands
                            df_temp2[choice5+ ' Share(%)'] = (df_temp2[choice5]/df_temp2['Total '+choice5])*100
                            
                            df_temp2[choice6+ ' Share(%)'] = (df_temp2[choice6]/df_temp2['Total '+choice6])*100
                            
                            df_temp2.sort_values(by=['INDEX',choice5+ ' Share(%)'],ascending=[True,False],inplace=True)
                            # st.dataframe(df_temp2)
                            #Finding top adv
                            if adv_stack:
                                dfb_outlier_adv = dfb.groupby(['INDEX','UNIQUE_ADV_NAME'],as_index=False).sum()
                                df_temp2_adv = pd.merge(dfb_outlier_adv, dfb_outlier_date,on = 'INDEX',how='left')
                                df_temp2_adv[choice6+ ' Share(%)'] = (df_temp2_adv[choice6]/df_temp2_adv['Total '+choice6])*100
                                df_temp2_adv.sort_values(by=['INDEX',choice6+ ' Share(%)'],ascending=[True,False],inplace=True)
                                topn_by_spend_adv = df_temp2_adv.groupby('INDEX').head(num_brand)
                                topn_by_spend_adv[choice6+ ' Share(%)'] = topn_by_spend_adv[choice6+ ' Share(%)'].fillna(0)
                                topn_by_spend_adv[choice6+ ' Share(%)'] = topn_by_spend_adv[choice6+ ' Share(%)'].apply(lambda x: '('+str(round(x))+'%)')
                            #Finding top brands
                            topn_by_imp = df_temp2.groupby('INDEX').head(num_brand)
                            df_temp2.sort_values(by=['INDEX',choice6+ ' Share(%)'],ascending=[True,False],inplace=True)
                            topn_by_spend = df_temp2.groupby('INDEX').head(num_brand)
                            topn_by_imp[choice5+ ' Share(%)'] = topn_by_imp[choice5+ ' Share(%)'].fillna(0)
                            topn_by_imp[choice6+ ' Share(%)'] = topn_by_imp[choice6+ ' Share(%)'].fillna(0)
                            topn_by_imp[choice5+ ' Share(%)'] = topn_by_imp[choice5+ ' Share(%)'].apply(lambda x: '('+str(round(x))+'%)')
                            topn_by_imp[choice6+ ' Share(%)'] = topn_by_imp[choice6+ ' Share(%)'].apply(lambda x: '('+str(round(x))+'%)')
                            
                            topn_by_spend[choice5+ ' Share(%)'] = topn_by_spend[choice5+ ' Share(%)'].fillna(0)
                            topn_by_spend[choice6+ ' Share(%)'] = topn_by_spend[choice6+ ' Share(%)'].fillna(0)
                            topn_by_spend[choice5+ ' Share(%)'] = topn_by_spend[choice5+ ' Share(%)'].apply(lambda x: '('+str(round(x))+'%)')
                            topn_by_spend[choice6+ ' Share(%)'] = topn_by_spend[choice6+ ' Share(%)'].apply(lambda x: '('+str(round(x))+'%)')
                            
                            # st.dataframe(topn_by_imp)
                            # st.dataframe(topn_by_spend)
                            
                            datewise_brand_imp_share_dict = {}
                            datewise_brand_spend_share_dict = {}
                            datewise_adv_spend_share_dict = {}
                            # for i in outlier_dates:
                            #     datewise_brand_imp_share[i] = (topn_by_imp[topn_by_imp['INDEX']==i]['UNIQUE_BRAND_NAME'].to_list(),topn_by_imp[topn_by_imp['INDEX']==i][choice5+ ' Share(%)'].to_list())
                            #     datewise_brand_spend_share[i] = (topn_by_spend[topn_by_spend['INDEX']==i]['UNIQUE_BRAND_NAME'].to_list(),topn_by_spend[topn_by_spend['INDEX']==i][choice6+ ' Share(%)'].to_list())

                            for i in outlier_dates:
                                # st.write(i)
                                brand_spend_share_lis = []
                                brand_imp_share_lis = []
                                adv_spend_share_lis = []
                                df_temp3_imp = topn_by_imp[topn_by_imp['INDEX']==i]
                                df_temp3_spend = topn_by_spend[topn_by_spend['INDEX']==i]
                                df_temp3_imp_brands = df_temp3_imp['UNIQUE_BRAND_NAME'].to_list()
                                df_temp3_spend_brands = df_temp3_spend['UNIQUE_BRAND_NAME'].to_list()
                                if adv_stack:
                                    df_temp3_spend_adv = topn_by_spend_adv[topn_by_spend_adv['INDEX']==i]
                                    
                                    df_temp3_spend_adv_names = df_temp3_spend_adv['UNIQUE_ADV_NAME'].to_list()
                                # st.dataframe(df_temp3_spend_adv)
                                for j in range(num_brand):
                                    # st.write(j)
                                    brand_imp_share_lis.append(df_temp3_imp_brands[j]+df_temp3_imp[choice5+ ' Share(%)'].to_list()[j])
                                    
                                    brand_spend_share_lis.append(df_temp3_spend_brands[j]+df_temp3_spend[choice6+ ' Share(%)'].to_list()[j])
                                    
                                    if adv_stack:
                                        adv_spend_share_lis.append(df_temp3_spend_adv_names[j]+df_temp3_spend_adv[choice6+ ' Share(%)'].to_list()[j])
                                
                                datewise_brand_imp_share_dict[i] = brand_imp_share_lis
                                datewise_brand_spend_share_dict[i] = brand_spend_share_lis
                                datewise_adv_spend_share_dict[i] = adv_spend_share_lis

                            # st.write(datewise_brand_imp_share_dict)
                            datewise_brand_imp_share_df = pd.DataFrame(datewise_brand_imp_share_dict.items(),columns = ['INDEX','Top Brands by '+axis_name_dict[short_tactic_type(choice5)]])#'Top Brands by Imp/Cliks'])
                            datewise_brand_spend_share_df = pd.DataFrame(datewise_brand_spend_share_dict.items(),columns = ['INDEX','Top Brands by Spends'])
                            
                            # st.dataframe(datewise_brand_imp_share_df)
                            # st.dataframe(datewise_brand_spend_share_df)
                            # st.write(df_imp[df_imp[choice5>imp_up]])
                            final_df = pd.merge(df_temp,datewise_brand_imp_share_df,on=['INDEX'],how='left')
                            final_df = pd.merge(final_df,datewise_brand_spend_share_df,on=['INDEX'],how='left')
                            # st.write(datewise_adv_spend_share_dict)
                            if adv_stack:
                                datewise_adv_spend_share_df = pd.DataFrame(datewise_adv_spend_share_dict.items(),columns = ['INDEX','Top Adv by Spends'])
                                # st.write(datewise_adv_spend_share_dict.items())
                                # datewise_adv_spend_share_df = pd.DataFrame(datewise_adv_spend_share_dict.keys(),datewise_adv_spend_share_dict.values(),columns = ['INDEX','Top Adv by Spends'])
                                final_df = pd.merge(final_df,datewise_adv_spend_share_df,on=['INDEX'],how='left')
                            final_df['INDEX'] = pd.to_datetime(final_df['INDEX']).dt.date
                            
                            st.success('Summary is ready!')
                            st.dataframe(final_df)
        
        
                                # csv_downloader(data=final_df, file_name=choice5+' adv_brand_analysis')
        with st.expander('Analyze Brands & Advertisers'):
            col17,col18 = st.columns(2)
            
            with col17:   
                choice7 = st.selectbox('Select Imp/Clicks', var_click + var_imp)
            with col18:
                choice8 = st.selectbox('Select Spends ', var_spend)

            col19, col20 = st.columns(2)
            
            with col19:
                start_date = st.date_input('Start Date', date(2021, 5, 1))
            with col20:
                end_date = st.date_input('End Date', date(2024, 1, 1))
            
            if 'uploaded_file6' not in st.session_state:
                st.session_state.uploaded_file6 = None
            # if 'uploaded_file3' not in st.session_state:
            #     st.session_state.uploaded_file3 = None
            # if 'fig' not in st.session_state:
            #     st.session_state.fig = None
            col24, col25 = st.columns(2)
            with col24:
                choice9 = st.radio("Choose an option",['Summarize','Plot'])
            uploaded_file6 = st.file_uploader("Upload Brand Adv Stack", type="csv")
            
            dfa = pd.DataFrame()
            
            if uploaded_file6 is not None:
                dfa = read_csv(uploaded_file6)
                st.success('Data uploaded successfully!')
                dfa.columns = dfa.columns.str.upper()
                dfa['INDEX'] = pd.to_datetime(dfa['INDEX'])
                
                # st.dataframe(dfa.head())
                st.session_state.uploaded_file6 = dfa

            
                button3 = st.button('Submit')
                if button3:
                    
                    dfa = dfa[(dfa['INDEX'] >= pd.to_datetime(start_date)) & (dfa['INDEX'] <= pd.to_datetime(end_date))]
                    # fig = make_subplots(specs=[[{"secondary_y": True}]])
                    # fig.add_trace(go.Scatter(x=dfa['INDEX'], y=dfa[choice7], name=choice7, line=dict(color='#0071CE')), secondary_y=False)
                    # fig.add_trace(go.Scatter(x=dfa['INDEX'], y=[imp_up] * len(dfa), name=axis_name_dict[short_tactic_type(choice7)] + ' Limit', line=dict(color='#0071CE', dash='dot')), secondary_y=False)
                    # fig.add_trace(go.Scatter(x=dfa['INDEX'], y=dfa[choice8], name=choice8, line=dict(color='#FFC220')), secondary_y=True)
                    # fig.add_trace(go.Scatter(x=dfa['INDEX'], y=[sp_up] * len(dfa), name=axis_name_dict[short_tactic_type(choice8)] + ' Limit', line=dict(color='#FFC220', dash='dot')), secondary_y=True)
                    # fig.update_layout(
                    #     title="{} VS {}".format(axis_name_dict[short_tactic_type(choice7)], axis_name_dict[short_tactic_type(choice8)]),
                    #     xaxis_title="<b>Date<b>",
                    #     width=900,
                    #     height=600
                    # )
                    # # st.plotly_chart(fig, use_container_width=True)
        
                    # st.session_state.fig = fig

                    # if st.session_state.fig is not None:
                    #     st.plotly_chart(st.session_state.fig, use_container_width=True)

                    if st.session_state.uploaded_file6 is not None:
                        # uploaded_file3 = st.file_uploader("Upload Cleanbrand Adv Stack", type="csv")
                        # if uploaded_file3 is not None:
                        #     dfb = read_csv(uploaded_file3)
                        #     dfb.columns = dfb.columns.str.upper()
                        #     dfb['INDEX'] = pd.to_datetime(dfb['INDEX'])
                        #     dfb = dfb[(dfb['INDEX'] >= pd.to_datetime(modeling_start_date)) & (dfb['INDEX'] <= pd.to_datetime(modeling_end_date))]
                        #     # st.dataframe(dfb.head())
                        #     st.session_state.uploaded_file3 = dfb

                        # if st.session_state.uploaded_file3 is not None:
                        #     # dfab = pd.merge(st.session_state.uploaded_file2, st.session_state.uploaded_file3, how='inner', on='INDEX')
                        #     # st.write("Dataframes Merged Successfully")
                        #     # st.dataframe(dfab.head())
                        #     # st.session_state.uploaded_file2 = dfab
                        df_temp = dfa[['INDEX','O_SALE',choice7,choice8]].copy()
                        
                        if choice9 == 'Summarize':
                            if short_tactic_type(choice7) == 'CLK':
                                df_temp['CPC ($)'] = df_temp[choice8]/df_temp[choice7]
                                rate_var = 'CPC'
                            
                            elif short_tactic_type(choice7) == 'IMP':
                                df_temp['CPM ($)'] = df_temp[choice8]/df_temp[choice7]*1000
                                rate_var = 'CPM'
                            # df_temp['Outlier'] = np.where(df_temp[choice7]>imp_up,'High '+axis_name_dict[short_tactic_type(choice7)],'')
                            
                            # df_temp['Outlier'] = np.where((df_temp[choice7]>=imp_up)&(df_temp[choice8]>=sp_up),'High '+axis_name_dict[short_tactic_type(choice7)]+' & Spends',
                                
                            #     np.where(df_temp[choice7]>=imp_up,'High '+axis_name_dict[short_tactic_type(choice7)],\
                            #     np.where(df_temp[choice8]>=sp_up,'High '+axis_name_dict[short_tactic_type(choice8)],'')))
                            
                            
                            # uploaded_file3 = st.file_uploader("Upload Cleanbrand Stack", type="csv")
                            
                            # if uploaded_file3 is not None:
                            #     # file_details = {"FileName":uploaded_file2.name,"FileType":uploaded_file2.type}
                            #     dfb = read_csv(uploaded_file3)
                            #     st.dataframe(dfb.head())            
                            col21, col22, col23 = st.columns(3)
                            with col22:
                                num_brand = st.number_input('Num of Brands/Adv', min_value=3)
                            # button2 = st.checkbox('Analyze Brands')
                            
                            if st.button('Generate Summary'):
                                date_range = pd.date_range(start=start_date, end=end_date)
                                selected_dates = date_range.strftime('%Y-%m-%d').tolist()
                                # selected_dates = df_temp[df_temp['Outlier']!='']['INDEX'].tolist()
                                # st.write(selected_dates)
                                
                                #a flag for adv_stack
                                adv_stack = False
                                if 'UNIQUE_ADV_NAME' in dfb.columns:
                                    #for adv, creating other df
                                    dfb = dfb[['INDEX','UNIQUE_BRAND_NAME','UNIQUE_ADV_NAME',choice7, choice8]]
                                    adv_stack = True
                                else:
                                    dfb = dfb[['INDEX','UNIQUE_BRAND_NAME',choice7, choice8]]
                                
                                with st.spinner('Generating Summary...'):
                                    time.sleep(0.5)
                                    # st.success('Forecast ready!')    
                                
                                
                                dfb = dfb[dfb['INDEX'].isin(selected_dates)]
                                
                                dfb_outlier_date = dfb[['INDEX',choice7, choice8]].groupby('INDEX',as_index=False).sum()   
                                dfb_outlier_date = dfb_outlier_date.rename(columns = {choice7:'Total '+choice7,choice8:'Total '+choice8}) 
                                # st.dataframe(df_temp_date)
                                dfb_outlier_brand = dfb.groupby(['INDEX','UNIQUE_BRAND_NAME'],as_index=False).sum()
                                
                                # st.dataframe(dfb_outlier_date)
                                # st.dataframe(dfb_outlier_brand)
                                df_temp2 = pd.merge(dfb_outlier_brand, dfb_outlier_date,on = 'INDEX',how='left')
                                
                                
                                #Finding top brands
                                df_temp2[choice7+ ' Share(%)'] = (df_temp2[choice7]/df_temp2['Total '+choice7])*100
                                
                                df_temp2[choice8+ ' Share(%)'] = (df_temp2[choice8]/df_temp2['Total '+choice8])*100
                                
                                df_temp2.sort_values(by=['INDEX',choice7+ ' Share(%)'],ascending=[True,False],inplace=True)
                                # st.dataframe(df_temp2)
                                #Finding top adv
                                if adv_stack:
                                    dfb_outlier_adv = dfb.groupby(['INDEX','UNIQUE_ADV_NAME'],as_index=False).sum()
                                    df_temp2_adv = pd.merge(dfb_outlier_adv, dfb_outlier_date,on = 'INDEX',how='left')
                                    df_temp2_adv[choice8+ ' Share(%)'] = (df_temp2_adv[choice8]/df_temp2_adv['Total '+choice8])*100
                                    df_temp2_adv.sort_values(by=['INDEX',choice8+ ' Share(%)'],ascending=[True,False],inplace=True)
                                    topn_by_spend_adv = df_temp2_adv.groupby('INDEX').head(num_brand)
                                    topn_by_spend_adv[choice8+ ' Share(%)'] = topn_by_spend_adv[choice8+ ' Share(%)'].fillna(0)
                                    topn_by_spend_adv[choice8+ ' Share(%)'] = topn_by_spend_adv[choice8+ ' Share(%)'].apply(lambda x: '('+str(round(x))+'%)')
                                #Finding top brands
                                topn_by_imp = df_temp2.groupby('INDEX').head(num_brand)
                                df_temp2.sort_values(by=['INDEX',choice8+ ' Share(%)'],ascending=[True,False],inplace=True)
                                topn_by_spend = df_temp2.groupby('INDEX').head(num_brand)
                                
                                topn_by_imp[choice7+ ' Share(%)'] = topn_by_imp[choice7+ ' Share(%)'].fillna(0)
                                topn_by_imp[choice8+ ' Share(%)'] = topn_by_imp[choice8+ ' Share(%)'].fillna(0)
                                topn_by_imp[choice7+ ' Share(%)'] = topn_by_imp[choice7+ ' Share(%)'].apply(lambda x: '('+str(round(x))+'%)')
                                topn_by_imp[choice8+ ' Share(%)'] = topn_by_imp[choice8+ ' Share(%)'].apply(lambda x: '('+str(round(x))+'%)')
                                
                                topn_by_spend[choice7+ ' Share(%)'] = topn_by_spend[choice7+ ' Share(%)'].fillna(0)
                                topn_by_spend[choice8+ ' Share(%)'] = topn_by_spend[choice8+ ' Share(%)'].fillna(0)
                                topn_by_spend[choice7+ ' Share(%)'] = topn_by_spend[choice7+ ' Share(%)'].apply(lambda x: '('+str(round(x))+'%)')
                                topn_by_spend[choice8+ ' Share(%)'] = topn_by_spend[choice8+ ' Share(%)'].apply(lambda x: '('+str(round(x))+'%)')
                                
                                # st.dataframe(topn_by_imp)
                                # st.dataframe(topn_by_spend)
                                
                                datewise_brand_imp_share_dict = {}
                                datewise_brand_spend_share_dict = {}
                                datewise_adv_spend_share_dict = {}
                                # for i in selected_dates:
                                #     datewise_brand_imp_share[i] = (topn_by_imp[topn_by_imp['INDEX']==i]['UNIQUE_BRAND_NAME'].to_list(),topn_by_imp[topn_by_imp['INDEX']==i][choice7+ ' Share(%)'].to_list())
                                #     datewise_brand_spend_share[i] = (topn_by_spend[topn_by_spend['INDEX']==i]['UNIQUE_BRAND_NAME'].to_list(),topn_by_spend[topn_by_spend['INDEX']==i][choice8+ ' Share(%)'].to_list())

                                for i in selected_dates:
                                    # st.write(i)
                                    brand_spend_share_lis = []
                                    brand_imp_share_lis = []
                                    adv_spend_share_lis = []
                                    df_temp3_imp = topn_by_imp[topn_by_imp['INDEX']==i]
                                    df_temp3_spend = topn_by_spend[topn_by_spend['INDEX']==i]
                                    df_temp3_imp_brands = df_temp3_imp['UNIQUE_BRAND_NAME'].to_list()
                                    df_temp3_spend_brands = df_temp3_spend['UNIQUE_BRAND_NAME'].to_list()
                                    if adv_stack:
                                        df_temp3_spend_adv = topn_by_spend_adv[topn_by_spend_adv['INDEX']==i]
                                        
                                        df_temp3_spend_adv_names = df_temp3_spend_adv['UNIQUE_ADV_NAME'].to_list()
                                    # st.dataframe(df_temp3_spend_adv)
                                    for j in range(num_brand):
                                        # st.write(j)
                                        brand_imp_share_lis.append(df_temp3_imp_brands[j]+df_temp3_imp[choice7+ ' Share(%)'].to_list()[j])
                                        
                                        brand_spend_share_lis.append(df_temp3_spend_brands[j]+df_temp3_spend[choice8+ ' Share(%)'].to_list()[j])
                                        
                                        if adv_stack:
                                            adv_spend_share_lis.append(df_temp3_spend_adv_names[j]+df_temp3_spend_adv[choice8+ ' Share(%)'].to_list()[j])
                                    
                                    datewise_brand_imp_share_dict[i] = brand_imp_share_lis
                                    datewise_brand_spend_share_dict[i] = brand_spend_share_lis
                                    datewise_adv_spend_share_dict[i] = adv_spend_share_lis

                                # st.write(datewise_brand_imp_share_dict)
                                datewise_brand_imp_share_df = pd.DataFrame(datewise_brand_imp_share_dict.items(),columns = ['INDEX','Top Brands by '+axis_name_dict[short_tactic_type(choice7)]])#'Top Brands by Imp/Cliks'])
                                datewise_brand_spend_share_df = pd.DataFrame(datewise_brand_spend_share_dict.items(),columns = ['INDEX','Top Brands by Spends'])
                                
                                # st.dataframe(datewise_brand_imp_share_df)
                                # st.dataframe(datewise_brand_spend_share_df)
                                # st.write(df_imp[df_imp[choice7>imp_up]])
                                final_df = pd.merge(df_temp,datewise_brand_imp_share_df,on=['INDEX'],how='left')
                                final_df = pd.merge(final_df,datewise_brand_spend_share_df,on=['INDEX'],how='left')
                                # st.write(datewise_adv_spend_share_dict)
                                if adv_stack:
                                    datewise_adv_spend_share_df = pd.DataFrame(datewise_adv_spend_share_dict.items(),columns = ['INDEX','Top Adv by Spends'])
                                    # st.write(datewise_adv_spend_share_dict.items())
                                    # datewise_adv_spend_share_df = pd.DataFrame(datewise_adv_spend_share_dict.keys(),datewise_adv_spend_share_dict.values(),columns = ['INDEX','Top Adv by Spends'])
                                    final_df = pd.merge(final_df,datewise_adv_spend_share_df,on=['INDEX'],how='left')
                                final_df['INDEX'] = pd.to_datetime(final_df['INDEX']).dt.date
                                
                                st.success('Summary is ready!')
                                st.dataframe(final_df)
                
                        else:
                            df_temp = dfa[['INDEX',choice7,choice8]].copy()
                            brands_list = df_temp['UNIQUE_BRAND_NAME'].unique().to_list()
                            choice10 = st.multiselect('Select Brands',brand_list)
                            
                            choice3 = st.multiselect('Spends', var_spend)
                            choice4 = st.multiselect('Rates', var_rate)

                            uploaded_file1 = st.file_uploader("Upload Aggbrand Stack", type="csv")
                            if uploaded_file1 is not None:
                                dfa = read_csv(uploaded_file1)
                                # st.write(dfa.head())

                            if st.button('Plot'):
                                # st.write(choice2)
                                choices1 = list(set(choice1 + choice2 + choice3 + choice4))
                            
                                fig = make_subplots()
                                colors = ['green', 'yellow', 'orange', 'blue', 'red', 'purple', 'brown', 'pink', 'gray', 'cyan']
                                if len(choices1) > 0:
                                    # fig = px.line(dfa, x='INDEX', y=choices1)
                                    fig = px.line(dfa, x='INDEX', y=choices1)
                                    # for i, column in enumerate(choices1):
                                    #     fig.add_scatter(x=dfa['INDEX'], y=dfa[column], mode='lines', line=dict(color=colors[i % len(colors)]))
                                    fig.update_layout(
                                        # title='Line Plot with Date Column as X-axis',
                                        xaxis_title='Date',
                                        yaxis_title='Value',
                                        legend_title='Columns',
                                        width=900,
                                        height=600
                                    )
                                    st.plotly_chart(fig, use_container_width=True)
                                else:
                                    st.write("Please select at least one column to display")
                                                
                                    
                
            

    elif choice == 'Miscellaneous':     
        
        with st.expander('Non-zero spending Advertisers Count'):
            col15, col16 = st.columns(2)
            
            with col15:
                start_date = st.date_input('Start Date', date(2021, 5, 1))
            with col16:
                end_date = st.date_input('End Date', date(2024, 1, 1))
            
            var = st.selectbox("Select Variable",var_spend + var_click + var_imp)
            
            uploaded_file5 = st.file_uploader("Upload Brand Adv Stack", type="csv")
            
            if uploaded_file5 is not None:
                dfa = read_csv(uploaded_file5)                   
            if st.button('Analyze'):
                df2 = dfa[dfa[var]>0][['INDEX','UNIQUE_ADV_NAME']].groupby('INDEX',as_index=False).count()
                df2['INDEX']= pd.to_datetime(df2['INDEX'])
                df2 = df2[(df2['INDEX'] >= pd.to_datetime(start_date)) & (df2['INDEX'] <= pd.to_datetime(end_date))]
                date_range = pd.date_range(start=start_date, end=end_date)

                # Convert the date range to a list of strings (optional)
                date_list = date_range.strftime('%Y-%m-%d').tolist()
                date_df = pd.DataFrame({'INDEX':date_list})
                date_df['INDEX'] = pd.to_datetime(date_df['INDEX'])
                adv_count_df = date_df.merge(df2,how='left',on='INDEX').fillna(0)
                adv_count_df['INDEX'] = adv_count_df['INDEX'].dt.date#pd.to_datetime(str(adv_count_df['INDEX'])[:10])
                adv_count_df.columns = ['Date','Num of Adv']    
                st.success('Non zero spending Adv summary is ready!')
                
                fig = make_subplots()
                colors = ['green', 'yellow', 'orange', 'blue', 'red', 'purple', 'brown', 'pink', 'gray', 'cyan']
            # if len(choices1) > 0:
                # fig = px.line(dfa, x='INDEX', y=choices1)
                fig = px.line(adv_count_df, x='Date', y="Num of Adv")
                # for i, column in enumerate(choices1):
                #     fig.add_scatter(x=dfa['INDEX'], y=dfa[column], mode='lines', line=dict(color=colors[i % len(colors)]))
                fig.update_layout(
                    # title='Line Plot with Date Column as X-axis',
                    xaxis_title='Date',
                    yaxis_title='# Advertisers',
                    # legend_title='Columns',
                    width=900,
                    height=600
                )
                st.plotly_chart(fig, use_container_width=True)
                st.dataframe(adv_count_df)
                # st.data_editor(adv_count_df)


if __name__ == '__main__':
    main()

                        