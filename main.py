# This program should import the finished dataset and will provide statistics on each role + champion
# This program will be able to produce a model based on each champion where it will show prediction % for a win

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.metrics import plot_confusion_matrix
from sklearn.metrics import f1_score
from numpy import arange
from scripts import get_match
from scripts import clean_text
from scripts import test


from PIL import Image

# ----- Import the Data Here ----- #
df = pd.read_csv('data/final_cleaned_df.csv', index_col = 0, header=0)

# ------ Define functions and variables ----- #
champlist = df.Champion.unique().tolist()
champlist = sorted(champlist)
champlist[:0] = [' ']

# ----- Begin Building Page ----- #
#
placeholder = st.empty()
with placeholder.container():
    st.image('img/home.jpg', use_column_width=True)

# ----- SideBar ----- #
with st.form(key = 'WSQuery', clear_on_submit=True):
    with st.sidebar:
        st.sidebar.subheader('Query Parameters')
        champion = st.sidebar.selectbox('Pick Champion',
                                        champlist)
        role_chosen = st.sidebar.selectbox('Pick the Role',
                                           ['', 'Top','Middle','Jungle','AD Carry','Support'])
        if champion and role_chosen:
            championData_wins = df.loc[(df['Champion'] == champion) & (df['Position_Played'] == role_chosen) & (df['Team_Win'] == 1)]
            championData_wins = championData_wins.reset_index(drop=True).reset_index()
            championData_full = df.loc[(df['Champion'] == champion) & (df['Position_Played'] == role_chosen)]
            championData_allroles = df.loc[(df['Champion'] == champion)]


        query_submit = st.form_submit_button(label='Submit Query Parameters')
        st.sidebar.image('img/map.jpeg', caption='Wild Rift Map with Role Assignments', use_column_width=True)

        # input match url
        text = st.text_input("Match URL (https://...)", '')
        user_match = text
        import validators
        valid = validators.url(user_match)
        valid_str = st.info('')

        query_match = st.form_submit_button(label='Analysis of Match')

if query_match:
    ## MATCH ANALYSIS
    if valid == True:
        valid_str.info('Valid Match URL')

        placeholder.empty()
        st.image('img/match_banner.jpg', use_column_width=True)
        match_data = get_match(user_match)
        df_wildstats = clean_text(match_data)
        X, y, model = test(df_wildstats)

        ### Display Test Results
        model_pred = model.predict(X)
        model_prob = model.predict_proba(X)

        #### MATCH PREDICTIONS

        # create df to show results of predictions
        merged = pd.concat([X, df_wildstats['Match_Num'], df_wildstats['Champion']], axis=1)
        df_predicted = pd.DataFrame(merged[['Match_Num', 'Champion']])
        prob = pd.DataFrame(model_prob)  # change from np.array
        pred = pd.DataFrame(model_pred)  # change from np.array
        pred.columns = ['Pred']
        df_predicted = pd.concat([df_predicted, pred], axis=1)
        df_predicted['Prediction'] = np.where(df_predicted['Pred'] == 0, 'Loss',
                                              'Win')
        df_predicted = pd.concat([df_predicted, prob], axis=1)
        df_predicted['Actual'] = y
        df_predicted['Actual'] = np.where(df_predicted['Actual'] == 1, 'Win', 'Loss')
        df_predicted.columns = [
            'Match Number', 'Champion', 'Pred', 'Prediction', 'Probability: Loss',
            'Probability: Win', 'Actual'
        ]
        df_predicted['Match Number'] = df_predicted['Match Number'].astype(int)
        df_predicted = df_predicted.sort_values(by='Match Number',
                                                ascending=True).reset_index(drop=True)
        df_predicted = df_predicted[['Champion','Prediction','Probability: Loss','Probability: Win', 'Actual']]
        df_predicted[['Probability: Loss','Probability: Win']] = round((df_predicted[['Probability: Loss','Probability: Win']]* 100),4)

        from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

        ## highlight the focused champion in Analysis:

        gb = GridOptionsBuilder.from_dataframe(df_predicted)
        gb.configure_pagination(paginationAutoPageSize=True)  # Add pagination
        gb.configure_side_bar()  # Add a sidebar

        gridOptions = gb.build()

        grid_response = AgGrid(
            df_predicted,
            gridOptions=gridOptions,
            data_return_mode='AS_INPUT',
            update_mode='MODEL_CHANGED',
            fit_columns_on_grid_load=False,
            theme='blue',  # Add theme color to the table
            enable_enterprise_modules=True,
            height=350,
            width='100%',
            reload_data=True
        )

        data = grid_response['data']
        st.info('The Dataframe shown above displays the prediction results from the prediction model. Depending on the match results, some players may have resulted in a prediction that differed from the actual result.'+
                ' Typically, this is the result of that specific players statistics showing that if the game result was based solely off of their performance, they would have received the predicted result.')

        # show df of stats from game
        merged = merged[['Match_Num','Champion','Team','Champion_Level','Experience_Points','Kills','Deaths','Assists','KDA','Kill_Participation_Rate','Gold','Gold_for_Kills',
                         'Minions_Killed','Jungle_Monster_Kills','Signals','Kill_Streaks','Assist_Streaks','Total_Damage_Dealt_by_Abilities','Total_Damage_dealt_by_Attacks','Damage_to_Champions_Dealt_with_Abilities',
                         'Damage_to_Champions_Dealt_with_Attacks','Total_Damage_to_Champions','Total_Damage_Dealt_to_Towers','Total_Damage_Dealt','Damage_Taken_by_Champions','Total_Damage_Tanked','Towers_Destroyed',
                         'Tower_Kill_Participation','Red_Buff_Kills','Blue_Buff_Kills','Raptor_Kills','Krug_Kills','Gromp_Kills','Wolf_Kills','Scuttlers_Kills','Total_Wards','Boots_Upgrade','Total_Healing_in_Allies',
                         'Total_Monster_Kills','Wards_Destroyed','Total_Shield','Shield_Used','Total_Self_Healing','Active_Skill_Equipped','Summoner_Spells_Used','Shoe_Enchantments_Purchased','Enemies_Controlled',
                         'Max_Trail_Kill_Number','Quick_Chats_Sent','Remaining_Gold','tt_Kills','tt_Deaths','tt_Gold','tt_Signals','tt_Towers_Destroyed','tt_Dragons_Killed','tt_Barons_Killed','tt_Nashor_Kills',
                         'tt_Ancient_Dragon_Kills','tt_Herald_Kills']]
        merged[[
            'Match_Num', 'Team', 'Champion_Level', 'Experience_Points',
            'Kills', 'Deaths', 'Assists', 'Gold',
            'Gold_for_Kills', 'Minions_Killed', 'Jungle_Monster_Kills', 'Signals',
            'Kill_Streaks', 'Assist_Streaks', 'Total_Damage_Dealt_by_Abilities',
            'Total_Damage_dealt_by_Attacks',
            'Damage_to_Champions_Dealt_with_Abilities',
            'Damage_to_Champions_Dealt_with_Attacks', 'Total_Damage_to_Champions',
            'Total_Damage_Dealt_to_Towers', 'Total_Damage_Dealt',
            'Damage_Taken_by_Champions', 'Total_Damage_Tanked', 'Towers_Destroyed',
            'Tower_Kill_Participation', 'Red_Buff_Kills', 'Blue_Buff_Kills',
            'Raptor_Kills', 'Krug_Kills', 'Gromp_Kills', 'Wolf_Kills',
            'Scuttlers_Kills', 'Total_Wards', 'Boots_Upgrade',
            'Total_Healing_in_Allies', 'Total_Monster_Kills', 'Wards_Destroyed',
            'Total_Shield', 'Shield_Used', 'Total_Self_Healing',
            'Active_Skill_Equipped', 'Summoner_Spells_Used',
            'Shoe_Enchantments_Purchased', 'Enemies_Controlled',
            'Max_Trail_Kill_Number', 'Quick_Chats_Sent', 'Remaining_Gold', 'tt_Kills',
            'tt_Deaths', 'tt_Gold', 'tt_Signals', 'tt_Towers_Destroyed',
            'tt_Dragons_Killed', 'tt_Barons_Killed', 'tt_Nashor_Kills',
            'tt_Ancient_Dragon_Kills', 'tt_Herald_Kills'
        ]] = merged[[
            'Match_Num', 'Team', 'Champion_Level', 'Experience_Points', 'Kills',
            'Deaths', 'Assists', 'Gold', 'Gold_for_Kills', 'Minions_Killed',
            'Jungle_Monster_Kills', 'Signals', 'Kill_Streaks', 'Assist_Streaks',
            'Total_Damage_Dealt_by_Abilities', 'Total_Damage_dealt_by_Attacks',
            'Damage_to_Champions_Dealt_with_Abilities',
            'Damage_to_Champions_Dealt_with_Attacks', 'Total_Damage_to_Champions',
            'Total_Damage_Dealt_to_Towers', 'Total_Damage_Dealt',
            'Damage_Taken_by_Champions', 'Total_Damage_Tanked', 'Towers_Destroyed',
            'Tower_Kill_Participation', 'Red_Buff_Kills', 'Blue_Buff_Kills',
            'Raptor_Kills', 'Krug_Kills', 'Gromp_Kills', 'Wolf_Kills',
            'Scuttlers_Kills', 'Total_Wards', 'Boots_Upgrade',
            'Total_Healing_in_Allies', 'Total_Monster_Kills', 'Wards_Destroyed',
            'Total_Shield', 'Shield_Used', 'Total_Self_Healing',
            'Active_Skill_Equipped', 'Summoner_Spells_Used',
            'Shoe_Enchantments_Purchased', 'Enemies_Controlled',
            'Max_Trail_Kill_Number', 'Quick_Chats_Sent', 'Remaining_Gold', 'tt_Kills',
            'tt_Deaths', 'tt_Gold', 'tt_Signals', 'tt_Towers_Destroyed',
            'tt_Dragons_Killed', 'tt_Barons_Killed', 'tt_Nashor_Kills',
            'tt_Ancient_Dragon_Kills', 'tt_Herald_Kills'
        ]].astype(int)

        ## highlight the focused champion in Analysis:

        gb = GridOptionsBuilder.from_dataframe(merged)
        gb.configure_pagination(paginationAutoPageSize=True)  # Add pagination
        gb.configure_side_bar()  # Add a sidebar

        gridOptions = gb.build()

        grid_response = AgGrid(
            merged,
            gridOptions=gridOptions,
            data_return_mode='AS_INPUT',
            update_mode='MODEL_CHANGED',
            fit_columns_on_grid_load=False,
            theme='blue',  # Add theme color to the table
            enable_enterprise_modules=True,
            height=350,
            width='100%',
            reload_data=True
        )

        data = grid_response['data']
        st.info('The Dataframe shown above displays the statistics that were web scraped from the match URL. These are the majority of the metrics used by the model for the prediction.'+
                ' The Dataframe does not include all of the metrics used by the model, such as role played and champion classifications.')

    else:
        valid_str.info('Invalid Match URL')

if query_submit:
    placeholder.empty()
    # Edit DataFrame for Viewing
    champ_stats = championData_wins[['Champion','Position_Played','Game_Points',
                                'Kills','Kill_Participation_Rate',
                                'Assists', 'Deaths', 'Gold', 'Minions_Killed',
                                'Jungle_Monster_Kills', 'Signals',
                                'Total_Damage_Dealt_by_Abilities', 'Total_Damage_dealt_by_Attacks',
                                'Damage_to_Champions_Dealt_with_Abilities',
                                'Damage_to_Champions_Dealt_with_Attacks', 'Total_Damage_to_Champions',
                                'Total_Damage_Dealt_to_Towers', 'Total_Damage_Dealt',
                                'Damage_Taken_by_Champions', 'Total_Damage_Tanked', 'Towers_Destroyed',
                                'Tower_Kill_Participation', 'Red_Buff_Kills', 'Blue_Buff_Kills',
                                'Raptor_Kills', 'Krug_Kills', 'Gromp_Kills', 'Wolf_Kills',
                                'Scuttlers_Kills', 'Total_Wards',
                                'Total_Healing_in_Allies',
                                'Total_Monster_Kills', 'Wards_Destroyed', 'Total_Shield', 'Shield_Used',
                                'Ancient_Dragon_Kills', 'Total_Self_Healing', 'Active_Skill_Equipped',
                                'Enemies_Controlled', 'KDA', 'tt_Game_Points', 'tt_Kills',
                                'tt_Deaths', 'tt_Gold', 'tt_Signals', 'tt_Towers_Destroyed',
                                'tt_Dragons_Killed', 'tt_Barons_Killed', 'tt_Nashor_Kills',
                                'tt_Ancient_Dragon_Kills', 'tt_Herald_Kills'
                                ]]
    # Display DataFrame
    import streamlit.components.v1 as components
    url = 'https://ddragon.leagueoflegends.com/cdn/img/champion/splash/' + champion + '_0.jpg'
    components.html(
        f"""
        <div style="margin-bottom:1em; display:flow-root; position:relative; width:100%; max-width:min(1045px, calc(100% - 288px)); min-width:min(828px, 100%); min-height:180px; z-index:0; margin-left:auto; margin-right:auto;">
           <div style="position:absolute; top:0px; right:0px; bottom:0px; left:0px; overflow:hidden;">
               <div style="position: absolute; left: 0px; top: 0px; width: 100%; height: 100%; background: radial-gradient(100% 100% at 110% 0%, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0) 60%, rgba(1, 10, 19, 0.4) 100%, rgba(1, 10, 19, 0.55) 120%, rgba(1, 10, 19, 0.9) 150%); z-index: 1; --darkreader-inline-bgimage:radial-gradient(100% 100% at 110% 0%, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0) 60%, rgba(1, 8, 15, 0.4) 100%, rgba(1, 8, 15, 0.55) 120%, rgba(1, 8, 15, 0.9) 150%); --darkreader-inline-bgcolor: initial;" data-darkreader-inline-bgimage="" data-darkreader-inline-bgcolor=""></div>
               <div style="position:absolute; z-index:0; min-width:1000px; top:-65%; top:-45%; right:0%;">
                   <img alt="Ahri OriginalSkin WR.jpg" src="{url}" decoding="async" width="1024" height="568">
               </div>
           </div>
           <div style="z-index:2; position:relative; text-align:left; margin: 24px; display:flex; flex-flow: column nowrap; justify-content:space-between; min-height:132px;"><span style="font-family: Trebuchet MS, sans-serif; font-size: 48px; color: rgb(255, 255, 255); --darkreader-inline-color:#e8e6e3;" data-darkreader-inline-color="">{champion}</span></div>
        </div>
        """
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader('Match Averages for ' + champion + ' (Won Matches)')
        champ_mean = champ_stats.mean()
        champ_mean = pd.DataFrame(champ_mean)
        a = round(champ_mean.iloc[0:24].reset_index(), 2)
        b = round(champ_mean.iloc[25:51].reset_index(), 2)
        champ_mean = pd.concat([a, b], axis=1)
        champ_mean.columns = ['0', '1', '2', '3']
        champ_mean['4'] = ' '
        st.dataframe(champ_mean, height=800)
        st.info('Total Matches Won: ' + champ_stats['Champion'].count().astype(str))
        st.info('Total Matches: ' + championData_full['Champion'].count().astype(str))

    with col2:
        st.subheader('Various Graphs for ' + champion + ' (All Matches)')
        championData_allroles['Team_Win'] = championData_allroles['Team_Win'].astype(str)
        championData_allroles['Team_Win'] = np.where(championData_allroles['Team_Win'] == '0', 'Loss', 'Win')
        championData_full['Team_Win'] = championData_full['Team_Win'].astype(str)
        championData_full['Team_Win'] = np.where(championData_full['Team_Win'] == '0', 'Loss', 'Win')
        championData_full['Kill_Participation_Rate'] = championData_full['Kill_Participation_Rate'] * 100

        chart_title = ("Positions Played by " + champion)
        fig_bar = px.histogram(championData_allroles, x='Position_Played', color='Team_Win', barmode='group',
                               text_auto=True,
                               labels={  # replaces default labels by column name
                                   "Team_Win": "Win/Loss", "Position_Played": "Role", "count": "Number of Games"
                               },
                               color_discrete_map={  # replaces default color mapping by value
                                   "Loss": "#e79899", "Win": "#488f31"
                               },
                               category_orders={"Team_Win": ["Win", "Loss"]},
                               template="simple_white"
                               )
        fig_bar.update_layout(title_text=chart_title, title_x=0.5, yaxis_title="Number of Games",
                              font=dict(
                                  family="Helvetica",
                                  size=12,
                                  color="RebeccaPurple"
                              ))
        st.plotly_chart(fig_bar, use_containter_width=True)

        # change what charts are shown based on the role chosen
        if role_chosen == 'Jungle':

            championData_full = championData_full.sort_values('KDA', ascending=False)
            championData_full = championData_full.reset_index(drop=True).reset_index()
            chart_title = ("KDA of " + champion + " in Games")
            fig1 = px.scatter(championData_full, x=championData_full['index'], y='KDA', color='Team_Win',
                              labels={  # replaces default labels by column name
                                  "Team_Win": "Win/Loss", "index": "Match Number",
                                  "KDA": "KDA (kills + assists / deaths)"
                              },
                              color_discrete_map={  # replaces default color mapping by value
                                  "Loss": "#e79899", "Win": "#488f31"
                              },
                              category_orders={"Team_Win": ["Win", "Loss"]},
                              template="simple_white"
                              )
            fig1.update_layout(title_text=chart_title, title_x=0.5,
                               font=dict(
                                   family="Helvetica",
                                   size=12,
                                   color="RebeccaPurple"
                               ))
            st.plotly_chart(fig1, use_container_width=True)

            championData_full = championData_full.drop('index', axis=1)
            championData_full = championData_full.sort_values('Total_Monster_Kills', ascending=False)
            championData_full = championData_full.reset_index(drop=True).reset_index()
            chart_title = ("Total Monsters Killed for " + champion + " in Games")
            fig2 = px.scatter(championData_full, x=championData_full['index'], y='Total_Monster_Kills',
                              color='Team_Win',
                              labels={  # replaces default labels by column name
                                  "Team_Win": "Win/Loss", "index": "Match Number",
                                  "Total_Monster_Kills": "Total Monster Kills (including dragons, herald and baron)"
                              },
                              color_discrete_map={  # replaces default color mapping by value
                                  "Loss": "#e79899", "Win": "#488f31"
                              },
                              category_orders={"Team_Win": ["Win", "Loss"]},
                              template="simple_white"
                              )
            fig2.update_layout(title_text=chart_title, title_x=0.5,
                               font=dict(
                                   family="Helvetica",
                                   size=12,
                                   color="RebeccaPurple"
                               ))
            st.plotly_chart(fig2, use_container_width=True)

            championData_full = championData_full.drop('index', axis=1)
            championData_full = championData_full.sort_values('Wards_Destroyed', ascending=False)
            championData_full = championData_full.reset_index(drop=True).reset_index()

            chart_title = ("Number of Wards Destroyed by " + champion + " in Games")
            fig3 = px.scatter(championData_full, x=championData_full['index'], y='Wards_Destroyed', color='Team_Win',
                              labels={  # replaces default labels by column name
                                  "Team_Win": "Win/Loss", "index": "Match Number",
                                  "Wards_Destroyed": "Number of Wards Destroyed"
                              },
                              color_discrete_map={  # replaces default color mapping by value
                                  "Loss": "#e79899", "Win": "#488f31"
                              },
                              category_orders={"Team_Win": ["Win", "Loss"]},
                              template="simple_white"
                              )
            fig3.update_layout(title_text=chart_title, title_x=0.5,
                               font=dict(
                                   family="Helvetica",
                                   size=12,
                                   color="RebeccaPurple"
                               ))
            fig3.update_layout(title_text=chart_title, title_x=0.5,
                               font=dict(
                                   family="Helvetica",
                                   size=12,
                                   color="RebeccaPurple"
                               ))
            st.plotly_chart(fig3, use_container_width=True)

        elif role_chosen == 'Top':

            championData_full = championData_full.sort_values('KDA', ascending=False)
            championData_full = championData_full.reset_index(drop=True).reset_index()

            chart_title = ("KDA of " + champion + " in Games")
            fig1 = px.scatter(championData_full, x=championData_full['index'], y='KDA', color='Team_Win',
                              labels={  # replaces default labels by column name
                                  "Team_Win": "Win/Loss", "index": "Match Number",
                                  "KDA": "KDA (kills + assists / deaths)"
                              },
                              color_discrete_map={  # replaces default color mapping by value
                                  "Loss": "#e79899", "Win": "#488f31"
                              },
                              category_orders={"Team_Win": ["Win", "Loss"]},
                              template="simple_white"
                              )
            fig1.update_layout(title_text=chart_title, title_x=0.5,
                               font=dict(
                                   family="Helvetica",
                                   size=12,
                                   color="RebeccaPurple"
                               ))
            st.plotly_chart(fig1, use_container_width=True)

            championData_full = championData_full.drop('index', axis=1)
            championData_full = championData_full.sort_values('Kill_Participation_Rate', ascending=False)
            championData_full = championData_full.reset_index(drop=True).reset_index()

            chart_title = ("Kill Participation Rate of " + champion + " in Games")

            fig2 = px.scatter(championData_full, x=championData_full['index'], y='Kill_Participation_Rate',
                              color='Team_Win',
                              labels={  # replaces default labels by column name
                                  "Team_Win": "Win/Loss", "index": "Match Number",
                                  "Kill_Participation_Rate": "Kill Participation Rate (%)"
                              },
                              color_discrete_map={  # replaces default color mapping by value
                                  "Loss": "#e79899", "Win": "#488f31"
                              },
                              category_orders={"Team_Win": ["Win", "Loss"]},
                              template="simple_white"
                              )
            fig2.update_layout(title_text=chart_title, title_x=0.5,
                               font=dict(
                                   family="Helvetica",
                                   size=12,
                                   color="RebeccaPurple"
                               ))
            st.plotly_chart(fig2, use_container_width=True)

            championData_full = championData_full.drop('index', axis=1)
            championData_full = championData_full.sort_values('Game_Points', ascending=False)
            championData_full = championData_full.reset_index(drop=True).reset_index()

            chart_title = ("Game Points of " + champion + " in Games")

            fig3 = px.scatter(championData_full, x=championData_full['index'], y='Game_Points', color='Team_Win',
                              labels={  # replaces default labels by column name
                                  "Team_Win": "Win/Loss", "index": "Match Number", "Game_Points": "Game Points Awarded"
                              },
                              color_discrete_map={  # replaces default color mapping by value
                                  "Loss": "#e79899", "Win": "#488f31"
                              },
                              category_orders={"Team_Win": ["Win", "Loss"]},
                              template="simple_white"
                              )
            fig3.update_layout(title_text=chart_title, title_x=0.5,
                               font=dict(
                                   family="Helvetica",
                                   size=12,
                                   color="RebeccaPurple"
                               ))
            st.plotly_chart(fig3, use_container_width=True)

        elif role_chosen == 'AD Carry':

            championData_full = championData_full.sort_values('KDA', ascending=False)
            championData_full = championData_full.reset_index(drop=True).reset_index()

            chart_title = ("KDA of " + champion + " in Games")

            fig1 = px.scatter(championData_full, x=championData_full['index'], y='KDA', color='Team_Win',
                              labels={  # replaces default labels by column name
                                  "Team_Win": "Win/Loss", "index": "Match Number",
                                  "KDA": "KDA (kills + assists / deaths)"
                              },
                              color_discrete_map={  # replaces default color mapping by value
                                  "Loss": "#e79899", "Win": "#488f31"
                              },
                              category_orders={"Team_Win": ["Win", "Loss"]},
                              template="simple_white"
                              )
            fig1.update_layout(title_text=chart_title, title_x=0.5,
                               font=dict(
                                   family="Helvetica",
                                   size=12,
                                   color="RebeccaPurple"
                               ))
            st.plotly_chart(fig1, use_container_width=True)

            championData_full = championData_full.drop('index', axis=1)
            championData_full = championData_full.sort_values('Minions_Killed', ascending=False)
            championData_full = championData_full.reset_index(drop=True).reset_index()
            chart_title = ("Minion Kills of " + champion + " in Games")

            fig2 = px.scatter(championData_full, x=championData_full['index'], y='Minions_Killed', color='Team_Win',
                              labels={  # replaces default labels by column name
                                  "Team_Win": "Win/Loss", "index": "Match Number",
                                  "Minions_Killed": "Minions Killed by " + champion
                              },
                              color_discrete_map={  # replaces default color mapping by value
                                  "Loss": "#e79899", "Win": "#488f31"
                              },
                              category_orders={"Team_Win": ["Win", "Loss"]},
                              template="simple_white"
                              )
            fig2.update_layout(title_text=chart_title, title_x=0.5,
                               font=dict(
                                   family="Helvetica",
                                   size=12,
                                   color="RebeccaPurple"
                               ))
            st.plotly_chart(fig2, use_container_width=True)

            championData_full = championData_full.drop('index', axis=1)
            championData_full = championData_full.sort_values('Total_Damage_to_Champions', ascending=False)
            championData_full = championData_full.reset_index(drop=True).reset_index()
            chart_title = ("Total Damage Done to Champions by " + champion + " in Games")

            fig3 = px.scatter(championData_full, x=championData_full['index'], y='Total_Damage_to_Champions',
                              color='Team_Win',
                              labels={  # replaces default labels by column name
                                  "Team_Win": "Win/Loss", "index": "Match Number",
                                  "Total_Damage_to_Champions": "Total Damage Done by " + champion
                              },
                              color_discrete_map={  # replaces default color mapping by value
                                  "Loss": "#e79899", "Win": "#488f31"
                              },
                              category_orders={"Team_Win": ["Win", "Loss"]},
                              template="simple_white"
                              )
            fig3.update_layout(title_text=chart_title, title_x=0.5,
                               font=dict(
                                   family="Helvetica",
                                   size=12,
                                   color="RebeccaPurple"
                               ))
            st.plotly_chart(fig3, use_container_width=True)

        elif role_chosen == 'Support':

            championData_full = championData_full.sort_values('KDA', ascending=False)
            championData_full = championData_full.reset_index(drop=True).reset_index()
            chart_title = ("KDA of " + champion + " in Games")

            fig1 = px.scatter(championData_full, x=championData_full['index'], y='KDA', color='Team_Win',
                              labels={  # replaces default labels by column name
                                  "Team_Win": "Win/Loss", "index": "Match Number",
                                  "KDA": "KDA (kills + assists / deaths)"
                              },
                              color_discrete_map={  # replaces default color mapping by value
                                  "Loss": "#e79899", "Win": "#488f31"
                              },
                              category_orders={"Team_Win": ["Win", "Loss"]},
                              template="simple_white"
                              )
            fig1.update_layout(title_text=chart_title, title_x=0.5,
                               font=dict(
                                   family="Helvetica",
                                   size=12,
                                   color="RebeccaPurple"
                               ))
            st.plotly_chart(fig1, use_container_width=True)

            championData_full = championData_full.drop('index', axis=1)
            championData_full = championData_full.sort_values('Kill_Participation_Rate', ascending=False)
            championData_full = championData_full.reset_index(drop=True).reset_index()
            chart_title = ("Kill Participation Rate of " + champion + " in Games")

            fig2 = px.scatter(championData_full, x=championData_full['index'], y='Kill_Participation_Rate',
                              color='Team_Win',
                              labels={  # replaces default labels by column name
                                  "Team_Win": "Win/Loss", "index": "Match Number",
                                  "Kill_Participation_Rate": "Kill Participation Rate (%)"
                              },
                              color_discrete_map={  # replaces default color mapping by value
                                  "Loss": "#e79899", "Win": "#488f31"
                              },
                              category_orders={"Team_Win": ["Win", "Loss"]},
                              template="simple_white"
                              )
            fig2.update_layout(title_text=chart_title, title_x=0.5,
                               font=dict(
                                   family="Helvetica",
                                   size=12,
                                   color="RebeccaPurple"
                               ))
            st.plotly_chart(fig2, use_container_width=True)

            championData_full = championData_full.drop('index', axis=1)
            championData_full = championData_full.sort_values('Enemies_Controlled', ascending=False)
            championData_full = championData_full.reset_index(drop=True).reset_index()
            chart_title = ("Enemies Controlled by " + champion + " in Games")

            fig3 = px.scatter(championData_full, x=championData_full['index'], y='Enemies_Controlled', color='Team_Win',
                              labels={  # replaces default labels by column name
                                  "Team_Win": "Win/Loss", "index": "Match Number",
                                  "Enemies_Controlled": "Number of Enemies Controlled"
                              },
                              color_discrete_map={  # replaces default color mapping by value
                                  "Loss": "#e79899", "Win": "#488f31"
                              },
                              category_orders={"Team_Win": ["Win", "Loss"]},
                              template="simple_white"
                              )
            fig3.update_layout(title_text=chart_title, title_x=0.5,
                               font=dict(
                                   family="Helvetica",
                                   size=12,
                                   color="RebeccaPurple"
                               ))
            st.plotly_chart(fig3, use_container_width=True)

        elif role_chosen == 'Middle':

            championData_full = championData_full.sort_values('KDA', ascending=False)
            championData_full = championData_full.reset_index(drop=True).reset_index()
            chart_title = ("KDA of " + champion + " in Games")

            fig1 = px.scatter(championData_full, x=championData_full['index'], y='KDA', color='Team_Win',
                              labels={  # replaces default labels by column name
                                  "Team_Win": "Win/Loss", "index": "Match Number",
                                  "KDA": "KDA (kills + assists / deaths)"
                              },
                              color_discrete_map={  # replaces default color mapping by value
                                  "Loss": "#e79899", "Win": "#488f31"
                              },
                              category_orders={"Team_Win": ["Win", "Loss"]},
                              template="simple_white"
                              )
            fig1.update_layout(title_text=chart_title, title_x=0.5,
                               font=dict(
                                   family="Helvetica",
                                   size=12,
                                   color="RebeccaPurple"
                               ))
            st.plotly_chart(fig1, use_container_width=True)

            championData_full = championData_full.drop('index', axis=1)
            championData_full = championData_full.sort_values('Kill_Participation_Rate', ascending=False)
            championData_full = championData_full.reset_index(drop=True).reset_index()
            chart_title = ("Kill Participation Rate of " + champion + " in Games")

            fig2 = px.scatter(championData_full, x=championData_full['index'], y='Kill_Participation_Rate',
                              color='Team_Win',
                              labels={  # replaces default labels by column name
                                  "Team_Win": "Win/Loss", "index": "Match Number",
                                  "Kill_Participation_Rate": "Kill Participation Rate (%)"
                              },
                              color_discrete_map={  # replaces default color mapping by value
                                  "Loss": "#e79899", "Win": "#488f31"
                              },
                              category_orders={"Team_Win": ["Win", "Loss"]},
                              template="simple_white"
                              )
            fig2.update_layout(title_text=chart_title, title_x=0.5,
                               font=dict(
                                   family="Helvetica",
                                   size=12,
                                   color="RebeccaPurple"
                               ))
            st.plotly_chart(fig2, use_container_width=True)

            championData_full = championData_full.drop('index', axis=1)
            championData_full = championData_full.sort_values('Damage_to_Champions_Dealt_with_Abilities',
                                                              ascending=False)
            championData_full = championData_full.reset_index(drop=True).reset_index()
            chart_title = ("Damage to Champions Dealt with Abilities of " + champion + " in Games")

            fig3 = px.scatter(championData_full, x=championData_full['index'],
                              y='Damage_to_Champions_Dealt_with_Abilities', color='Team_Win',
                              labels={  # replaces default labels by column name
                                  "Team_Win": "Win/Loss", "index": "Match Number",
                                  "Damage_to_Champions_Dealt_with_Abilities": "Amount of Damage Dealt to Champions using Abilities"
                              },
                              color_discrete_map={  # replaces default color mapping by value
                                  "Loss": "#e79899", "Win": "#488f31"
                              },
                              category_orders={"Team_Win": ["Win", "Loss"]},
                              template="simple_white"
                              )
            fig3.update_layout(title_text=chart_title, title_x=0.5,
                               font=dict(
                                   family="Helvetica",
                                   size=12,
                                   color="RebeccaPurple"
                               ))
            st.plotly_chart(fig3, use_container_width=True)