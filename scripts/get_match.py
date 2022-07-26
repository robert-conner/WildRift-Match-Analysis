#!/usr/bin/env python
# coding: utf-8

def get_match(user_match):
    #import required libs
    import numpy as np
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd
    import requests
    import urllib3 #(URL handling)
    from bs4 import BeautifulSoup as bs #(in case Selenium couldn’t handle everything)
    from functools import reduce
    import re

    url = 'https://na.wildstats.gg/en/profile/hpa8E2ZKnC0YSzeMyPxP/battle/826722972629841284'
    page = requests.get(url)

    # create table cols, table skeleton
    cols = [
        'Position Played', 'Champion Level', 'Team MVP', 'Game Points',
        'Experience Points', 'Rejected Surrender', 'Kills', 'Assists', 'Deaths',
        'Double Kills', 'Triple Kills', 'Consecutive Five Kill', 'Kill Streaks',
        'Assist Streaks', 'Number of Aces', 'Total Damage Dealt by Abilities',
        'Total Damage dealt by Attacks',
        'Damage to Champions Dealt with Abilities',
        'Damage to Champions Dealt with Attacks', 'Total Damage to Champions',
        'Total Damage Dealt to Towers', 'Total Damage Dealt to Towers',
        'Total Damage Dealt', 'Damage Taken by Champions', 'Total Damage Tanked',
        'Towers Destroyed', 'Tower Kill Participation', 'Joined Tower Kills',
        'Kill Participation Rate', 'Seconds to First Blood', 'First Blood Assist',
        'Seconds to First Tower Destroyed', 'Gold', 'Gold for Kills',
        'Remaining Gold', 'Seconds in Game', 'Minions Killed',
        'Jungle Monster Kills', 'Seconds to First Dragon Kill', 'Dragons Killed',
        'Seconds to First Baron Kill', 'Barons Killed',
        'Seconds to Call Rift Herald', 'Max Trail Kill Number',
        'Low Power Kill Number', 'Joined Baron Kills', 'Joined Dragon Kills',
        'Red Buff Kills', 'Red Buffs Used', 'Blue Buff Kills', 'Blue Buffs Used',
        'Raptor Kills', 'Krug Kills', 'Gromp Kills', 'Wolf Kills',
        'Scuttlers Kills', 'Nashor Kills', 'Epic Kills', 'Total Wards',
        'Boots Upgrade', 'Total Healing in Alleys', 'Total Healing Received',
        'Total Monster Kills', 'Wards Destroyed', 'Emoji', 'Signals',
        'Ancient Dragon Kills', 'Honeyfruits Picked', 'Total Honeyfruit Used',
        'Health Recovered from honeyfruits', 'Explosive Fruits Moved (?)',
        'Enemies Found using Scryer Blooms', 'Scryer Blooms Used',
        'Blast Cones Used', 'Total Shield', 'Shield Used',
        'Seconds to Herald Kill', 'Seconds to Elder Dragon Kill', 'Herald Kills',
        'Total Self Healing', 'Active Skill Equipped', 'Summoner Spells Used',
        'Shoe Enchantments Purchased', 'Hang Time', 'Hits using Skill 1',
        'Hits using Skill 2', 'Hits using Skill 3', 'Hits using Skill 4',
        'Skill 4 Count', 'Dragon Steals', 'Herald Tower Kills',
        'Enemies Controlled','Team Win'
    ]
    a = [1] * len(cols)
    df = pd.DataFrame(data=a).T
    df = pd.DataFrame(data=df, columns=cols)
    df_build = pd.DataFrame(data=df).reset_index()

    html_content = page.text
    total_headings = []
    # Parse HTML code for the entire site
    soup = bs(html_content, "lxml")
    #print(soup.prettify()) # print the parsed data of html    

    # On site there is 1 table in gdp
    # The following line will generate a list of HTML content for each table
    gdp = soup.find_all(
        "table", attrs={"class": "w-100 table-primary table-hover bg-feature"})
    win = soup.find("div",
                    attrs={"class": "col-12 text-center text-uppercase"})

    # Lets go ahead and scrape first table with HTML code gdp[0]
    table1 = gdp[0]
    # the head will form our column names
    body = table1.find_all("tr")
    # Head values (Column names) are the first items of the body list
    head = body[0]  # 0th item is the header row
    body_rows = body[1:]  # All other items becomes the rest of the rows

    # Lets now iterate through the head HTML code and make list of clean headings

    # Declare empty list to keep Columns names
    headings = []
    for item in head.find_all("div"):  # loop through all th elements
        # convert the th elements to text and strip "\n"
        aa = item.get('title')
        aa = re.sub('^[^:\r\n]+:', "", aa)
        aa = re.sub(r"^\s+", "", aa)

        #.rstrip("\n")
        # append the clean column name to headings
        headings.append(aa)
    total_headings.append(headings)

    ## -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

    # Next is now to loop though the rest of the rows
    all_rows = []  # will be a list for list for all rows
    team_win = []
    for row_num in range(len(body_rows)):  # A row at a time
        row = []  # this will old entries for one row
        for row_item in body_rows[row_num].find_all(
                "td"):  #loop through all row entries
            # row_item.text removes the tags from the entries
            # the following regex is to remove \xa0 and \n and comma from row_item.text
            # xa0 encodes the flag, \n is the newline and comma separates thousands in numbers
            bb = re.sub(r"^\s+|\s+$", "", row_item.text)
            aa = re.sub("(\xa0)|(\n)|,", "", bb)
            cc = re.sub(r'\w*Wins\w*', '', win.text)
            cc = re.sub(r"^\s+|\s+$", "", cc)
            cc = re.sub("(\xa0)|(\n)|,", "", cc)

            #append aa to row - note one row entry is being appended
            row.append(aa)

    # append one row to all_rows
        all_rows.append(row)


    # We can now use the data on all_rows and headings to make a table

    total_rows = pd.DataFrame(all_rows).reset_index(drop=True)
    total_rows = total_rows.T
    total_rows.columns = total_rows.iloc[0]
    total_rows = total_rows.drop([0])

    total_rows = total_rows.loc[:,~total_rows.columns.duplicated()].copy()
    total_rows['Team Win'] = cc
    total_rows['Match_Num'] = 1
    df_build = df_build.loc[:,~df_build.columns.duplicated()].copy()
    df_build = pd.concat([df_build, total_rows], join = 'outer', axis = 0, sort = False)

    ### Add headings to data

    # fix headings
    df = df_build.copy()
    headings = total_headings.copy()
    heading = reduce(lambda xs, ys: xs + ys, headings)
    heading.insert(0, 'Not a Champ')
    df['Champion'] = heading
    df = df.drop(columns={'index'})

    ### Add Position Played and Team

    # player position and team
    df.reset_index(inplace=True)
    df['Position Played'] = df['index'].values

    def position_played(row):
        # 
        if row['Position Played'] == 1 or row['Position Played'] == 6:
            row['Position Played'] = 'Middle'
        elif row['Position Played'] == 0:
            row['Position Played'] = ''
        elif row['Position Played'] == 2 or row['Position Played'] == 7:
            row['Position Played'] = 'Top'
        elif row['Position Played'] == 3 or row['Position Played'] == 8:
            row['Position Played'] = 'AD Carry'
        elif row['Position Played'] == 4 or row['Position Played'] == 9:
            row['Position Played'] = 'Jungle'
        else:
            row['Position Played'] = 'Support'
        return row['Position Played']

    df['Position Played'] = df.apply(position_played, axis=1)

    # create team
    list_index = list(map(int, df['index'].values))
    team = [1] * (len(list_index))

    for i in range(len(list_index)):

        # replace hardik with shardul
        if list_index[i] >= 6:
            team[i] = 'Red'

        # replace pant with ishan
        if list_index[i] <= 5:
            team[i] = 'Blue'

    #set team as df['team']
    df['team'] = team
    df = df.drop(columns={'index'}).drop([0])
    return df

