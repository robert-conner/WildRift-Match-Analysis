#!/usr/bin/env python
# coding: utf-8

def clean_text(df):
    #import required libs
    import numpy as np
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd

    """ Clean all the raw_html """

    ## start
    #change up df col order
    a = [
        'Match_Num', 'Champion', 'team', 'Team Win', 'Position Played',
        'Champion Level', 'Team MVP', 'Game Points', 'Experience Points',
        'Rejected Surrender', 'Kills', 'Assists', 'Deaths', 'Gold',
        'Gold for Kills', 'Remaining Gold', 'Seconds in Game', 'Minions Killed',
        'Jungle Monster Kills', 'Signals', 'Kill Streaks', 'Assist Streaks',
        'Number of Aces', 'Total Damage Dealt by Abilities',
        'Total Damage dealt by Attacks',
        'Damage to Champions Dealt with Abilities',
        'Damage to Champions Dealt with Attacks', 'Total Damage to Champions',
        'Total Damage Dealt to Towers', 'Total Damage Dealt',
        'Damage Taken by Champions', 'Total Damage Tanked', 'Towers Destroyed',
        'Tower Kill Participation', 'Joined Tower Kills',
        'Kill Participation Rate', 'Seconds to First Blood', 'First Blood Assist',
        'Seconds to First Tower Destroyed', 'Seconds to First Dragon Kill',
        'Dragons Killed', 'Seconds to First Baron Kill', 'Barons Killed',
        'Seconds to Call Rift Herald', 'Max Trail Kill Number',
        'Low Power Kill Number', 'Joined Baron Kills', 'Joined Dragon Kills',
        'Red Buff Kills', 'Red Buffs Used', 'Blue Buff Kills', 'Blue Buffs Used',
        'Raptor Kills', 'Krug Kills', 'Gromp Kills', 'Wolf Kills',
        'Scuttlers Kills', 'Nashor Kills', 'Epic Kills', 'Total Wards',
        'Boots Upgrade', 'Total Healing in Alleys', 'Total Healing Received',
        'Total Monster Kills', 'Wards Destroyed', 'Emoji', 'Ancient Dragon Kills',
        'Honeyfruits Picked', 'Total Honeyfruit Used',
        'Health Recovered from honeyfruits', 'Explosive Fruits Moved (?)',
        'Enemies Found using Scryer Blooms', 'Scryer Blooms Used',
        'Blast Cones Used', 'Total Shield', 'Shield Used',
        'Seconds to Herald Kill', 'Seconds to Elder Dragon Kill', 'Herald Kills',
        'Total Self Healing', 'Active Skill Equipped', 'Summoner Spells Used',
        'Shoe Enchantments Purchased', 'Hang Time', 'Hits using Skill 1',
        'Hits using Skill 2', 'Hits using Skill 3', 'Hits using Skill 4',
        'Skill 4 Count', 'Dragon Steals', 'Herald Tower Kills',
        'Enemies Controlled', 'Joined Red Buff Kills', 'Joined Blue Buff Kills',
        'Legendary', 'Destroyed Enemy Nexus', 'Quad Kills', 'Penta Kills',
        'Quick Chats Sent', 'Hang Count', 'Baron Steals', 'Double Kills',
        'Triple Kills', 'Consecutive Five Kill'
    ]

    b = df.columns.tolist()
    set_difference = set(a) - set(b)
    list_difference = list(set_difference)

    for x in range(len(list_difference)):
        c = list_difference[x]
        df[c] = 0

    df = df[[
        'Match_Num', 'Champion', 'team', 'Team Win', 'Position Played',
        'Champion Level', 'Team MVP', 'Game Points', 'Experience Points',
        'Rejected Surrender', 'Kills', 'Assists', 'Deaths', 'Gold',
        'Gold for Kills', 'Remaining Gold', 'Seconds in Game', 'Minions Killed',
        'Jungle Monster Kills', 'Signals', 'Kill Streaks', 'Assist Streaks',
        'Number of Aces', 'Total Damage Dealt by Abilities',
        'Total Damage dealt by Attacks',
        'Damage to Champions Dealt with Abilities',
        'Damage to Champions Dealt with Attacks', 'Total Damage to Champions',
        'Total Damage Dealt to Towers', 'Total Damage Dealt',
        'Damage Taken by Champions', 'Total Damage Tanked', 'Towers Destroyed',
        'Tower Kill Participation', 'Joined Tower Kills',
        'Kill Participation Rate', 'Seconds to First Blood', 'First Blood Assist',
        'Seconds to First Tower Destroyed', 'Seconds to First Dragon Kill',
        'Dragons Killed', 'Seconds to First Baron Kill', 'Barons Killed',
        'Seconds to Call Rift Herald', 'Max Trail Kill Number',
        'Low Power Kill Number', 'Joined Baron Kills', 'Joined Dragon Kills',
        'Red Buff Kills', 'Red Buffs Used', 'Blue Buff Kills', 'Blue Buffs Used',
        'Raptor Kills', 'Krug Kills', 'Gromp Kills', 'Wolf Kills',
        'Scuttlers Kills', 'Nashor Kills', 'Epic Kills', 'Total Wards',
        'Boots Upgrade', 'Total Healing in Alleys', 'Total Healing Received',
        'Total Monster Kills', 'Wards Destroyed', 'Emoji', 'Ancient Dragon Kills',
        'Honeyfruits Picked', 'Total Honeyfruit Used',
        'Health Recovered from honeyfruits', 'Explosive Fruits Moved (?)',
        'Enemies Found using Scryer Blooms', 'Scryer Blooms Used',
        'Blast Cones Used', 'Total Shield', 'Shield Used',
        'Seconds to Herald Kill', 'Seconds to Elder Dragon Kill', 'Herald Kills',
        'Total Self Healing', 'Active Skill Equipped', 'Summoner Spells Used',
        'Shoe Enchantments Purchased', 'Hang Time', 'Hits using Skill 1',
        'Hits using Skill 2', 'Hits using Skill 3', 'Hits using Skill 4',
        'Skill 4 Count', 'Dragon Steals', 'Herald Tower Kills',
        'Enemies Controlled', 'Joined Red Buff Kills', 'Joined Blue Buff Kills',
        'Legendary', 'Destroyed Enemy Nexus', 'Quad Kills', 'Penta Kills',
        'Quick Chats Sent', 'Hang Count', 'Baron Steals', 'Double Kills',
        'Triple Kills', 'Consecutive Five Kill'
    ]]

    ### Fix columns to fill NAN, -, and d/K

    # Fix Many of the Columns to fill NAN, '-', and thousands

    df[[
        'Team MVP', 'Experience Points', 'Rejected Surrender', 'Gold',
        'Gold for Kills', 'Remaining Gold', 'Total Damage Dealt by Abilities',
        'Total Damage dealt by Attacks', 'Total Shield', 'Shield Used',
        'Herald Kills', 'Total Self Healing', 'Dragon Steals', 'Game Points',
        'Herald Tower Kills', 'Enemies Controlled',
        'Damage to Champions Dealt with Abilities',
        'Damage to Champions Dealt with Attacks', 'Total Damage to Champions',
        'Total Damage Dealt to Towers', 'Total Damage Dealt',
        'Damage Taken by Champions', 'Total Damage Tanked', 'Towers Destroyed',
        'Tower Kill Participation', 'Joined Tower Kills', 'Dragons Killed',
        'Barons Killed', 'Joined Baron Kills', 'Joined Dragon Kills',
        'Red Buff Kills', 'Red Buffs Used', 'Blue Buff Kills', 'Blue Buffs Used',
        'Raptor Kills', 'Krug Kills', 'Gromp Kills', 'Wolf Kills',
        'Scuttlers Kills', 'Nashor Kills', 'Epic Kills', 'Total Wards',
        'Boots Upgrade', 'Total Healing in Alleys', 'Total Healing Received',
        'Total Monster Kills', 'Wards Destroyed', 'Emoji', 'Kills', 'Assists',
        'Deaths', 'Minions Killed', 'Jungle Monster Kills', 'Signals',
        'Kill Streaks', 'Assist Streaks', 'Seconds in Game',
        'Active Skill Equipped', 'Summoner Spells Used',
        'Shoe Enchantments Purchased'
    ]] = df[[
        'Team MVP', 'Experience Points', 'Rejected Surrender', 'Gold',
        'Gold for Kills', 'Remaining Gold', 'Total Damage Dealt by Abilities',
        'Total Damage dealt by Attacks', 'Total Shield', 'Shield Used',
        'Herald Kills', 'Total Self Healing', 'Dragon Steals', 'Game Points',
        'Herald Tower Kills', 'Enemies Controlled',
        'Damage to Champions Dealt with Abilities',
        'Damage to Champions Dealt with Attacks', 'Total Damage to Champions',
        'Total Damage Dealt to Towers', 'Total Damage Dealt',
        'Damage Taken by Champions', 'Total Damage Tanked', 'Towers Destroyed',
        'Tower Kill Participation', 'Joined Tower Kills', 'Dragons Killed',
        'Barons Killed', 'Joined Baron Kills', 'Joined Dragon Kills',
        'Red Buff Kills', 'Red Buffs Used', 'Blue Buff Kills', 'Blue Buffs Used',
        'Raptor Kills', 'Krug Kills', 'Gromp Kills', 'Wolf Kills',
        'Scuttlers Kills', 'Nashor Kills', 'Epic Kills', 'Total Wards',
        'Boots Upgrade', 'Total Healing in Alleys', 'Total Healing Received',
        'Total Monster Kills', 'Wards Destroyed', 'Emoji', 'Kills', 'Assists',
        'Deaths', 'Minions Killed', 'Jungle Monster Kills', 'Signals',
        'Kill Streaks', 'Assist Streaks', 'Seconds in Game',
        'Active Skill Equipped', 'Summoner Spells Used',
        'Shoe Enchantments Purchased'
    ]].replace({
        '-': '0',
        '': '0',
        r'k$': '000',
        '✔': '1'
    }, regex=True).astype(float)  #replace - and blanks

    # fix some more values
    df[[
        'Quick Chats Sent', 'Nashor Kills', 'Shoe Enchantments Purchased',
        'Wards Destroyed', 'Gromp Kills', 'Wolf Kills', 'Krug Kills',
        'Total Damage Dealt to Towers', 'Total Shield'
    ]] = df[[
        'Quick Chats Sent', 'Nashor Kills', 'Shoe Enchantments Purchased',
        'Wards Destroyed', 'Gromp Kills', 'Wolf Kills', 'Krug Kills',
        'Total Damage Dealt to Towers', 'Total Shield'
    ]].replace({
        '-': '0',
        '': '0',
        r'k$': '000',
        '✔': '1'
    }, regex=True).astype(float)

    # Fix some more columns in the same way
    df[[
        'Hang Time', 'Hits using Skill 1', 'Hits using Skill 2',
        'Hits using Skill 3', 'Hits using Skill 4', 'Skill 4 Count',
        'Herald Tower Kills', 'Enemies Controlled', 'First Blood Assist',
        'Max Trail Kill Number', 'Quick Chats Sent', 'Hang Count',
        'Remaining Gold', 'Total Healing in Alleys', 'Total Healing Received'
    ]] = df[[
        'Hang Time', 'Hits using Skill 1', 'Hits using Skill 2',
        'Hits using Skill 3', 'Hits using Skill 4', 'Skill 4 Count',
        'Herald Tower Kills', 'Enemies Controlled', 'First Blood Assist',
        'Max Trail Kill Number', 'Quick Chats Sent', 'Hang Count',
        'Remaining Gold', 'Total Healing in Alleys', 'Total Healing Received'
    ]].replace({
        '-': '0',
        '': '0',
        r'k$': '000',
        '✔': '1'
    }, regex=True).astype(float)

    ### Fill Nan with (0)

    # fill some nan with (0)
    df[[
        'Quick Chats Sent', 'Nashor Kills', 'Shoe Enchantments Purchased',
        'Wards Destroyed', 'Gromp Kills', 'Wolf Kills', 'Krug Kills',
        'Total Damage Dealt to Towers', 'Total Shield'
    ]] = df[[
        'Quick Chats Sent', 'Nashor Kills', 'Shoe Enchantments Purchased',
        'Wards Destroyed', 'Gromp Kills', 'Wolf Kills', 'Krug Kills',
        'Total Damage Dealt to Towers', 'Total Shield'
    ]].fillna(0)

    # Fill NAN with 0 for some columns
    df['Towers Destroyed'] = df['Towers Destroyed'].fillna(0)
    df['Tower Kill Participation'] = df['Tower Kill Participation'].fillna(0)
    df['Baron Steals'] = df['Baron Steals'].fillna(0)
    df['Dragon Steals'] = df['Dragon Steals'].fillna(0)
    df['Ancient Dragon Kills'] = df['Ancient Dragon Kills'].fillna(0)

    ### Fix Role

    # fix Role
    ### One-hot encoding Land Contour
    # Group and retreive value_count() for Land Contour
    # Drop the largest feature to avoid multi-collinearity
    # Create dummy variables for Land Contour to binarize

    #Create dummy variables
    dummies_rp = pd.get_dummies(df['Position Played'],
                                drop_first=False,
                                prefix='rp',
                                dtype='int')
    dummies_rp = pd.DataFrame(dummies_rp)

    #drop largest column
    dummies_rp.drop(['rp_Top'], axis=1, inplace=True)

    df = pd.concat([df, dummies_rp], axis=1)
    df = df[[
        'Match_Num', 'Champion', 'team', 'Team Win', 'Position Played',
        'rp_AD Carry', 'rp_Jungle', 'rp_Middle', 'rp_Support', 'Champion Level',
        'Team MVP', 'Game Points', 'Experience Points', 'Rejected Surrender',
        'Kills', 'Kill Participation Rate', 'Assists', 'Deaths', 'Gold',
        'Gold for Kills', 'Seconds in Game', 'Minions Killed',
        'Jungle Monster Kills', 'Signals', 'Kill Streaks', 'Assist Streaks',
        'Total Damage Dealt by Abilities', 'Total Damage dealt by Attacks',
        'Damage to Champions Dealt with Abilities',
        'Damage to Champions Dealt with Attacks', 'Total Damage to Champions',
        'Total Damage Dealt to Towers', 'Total Damage Dealt',
        'Damage Taken by Champions', 'Total Damage Tanked', 'Towers Destroyed',
        'Tower Kill Participation', 'Joined Tower Kills', 'Dragons Killed',
        'Barons Killed', 'Joined Baron Kills', 'Joined Dragon Kills',
        'Red Buff Kills', 'Red Buffs Used', 'Blue Buff Kills', 'Blue Buffs Used',
        'Raptor Kills', 'Krug Kills', 'Gromp Kills', 'Wolf Kills',
        'Scuttlers Kills', 'Nashor Kills', 'Epic Kills', 'Total Wards',
        'Boots Upgrade', 'Total Healing in Alleys', 'Total Healing Received',
        'Total Monster Kills', 'Wards Destroyed', 'Emoji', 'Ancient Dragon Kills',
        'Total Shield', 'Shield Used', 'Herald Kills', 'Total Self Healing',
        'Active Skill Equipped', 'Summoner Spells Used',
        'Shoe Enchantments Purchased', 'Hang Time', 'Hits using Skill 1',
        'Hits using Skill 2', 'Hits using Skill 3', 'Hits using Skill 4',
        'Skill 4 Count', 'Dragon Steals', 'Herald Tower Kills',
        'Enemies Controlled', 'Legendary', 'Destroyed Enemy Nexus',
        'Number of Aces', 'Seconds to First Blood', 'First Blood Assist',
        'Seconds to First Tower Destroyed', 'Seconds to First Dragon Kill',
        'Seconds to First Baron Kill', 'Seconds to Herald Kill',
        'Seconds to Elder Dragon Kill', 'Seconds to Call Rift Herald',
        'Max Trail Kill Number', 'Low Power Kill Number', 'Quad Kills',
        'Penta Kills', 'Quick Chats Sent', 'Hang Count', 'Baron Steals',
        'Double Kills', 'Triple Kills', 'Consecutive Five Kill', 'Remaining Gold',
        'Honeyfruits Picked', 'Total Honeyfruit Used',
        'Health Recovered from honeyfruits', 'Explosive Fruits Moved (?)',
        'Enemies Found using Scryer Blooms', 'Scryer Blooms Used',
        'Blast Cones Used', 'Joined Red Buff Kills', 'Joined Blue Buff Kills'
    ]]

    ### Fix kill participation Rate

    # fix Kill Participation Rate
    df['Kill Participation Rate'] = df['Kill Participation Rate'].replace(
        {
            '-': '0',
            '': '0',
            r'k$': '000',
            '✔': '1'
        }, regex=True)  #replace - and blanks

    df['Kill Participation Rate'] = df['Kill Participation Rate'].fillna('0')
    df['Kill Participation Rate'] = df['Kill Participation Rate'].str.replace(
        r'\D+', '', regex=True)
    df['Kill Participation Rate'] = df['Kill Participation Rate'].astype(float)
    df['Kill Participation Rate'] = (df['Kill Participation Rate'] / 100)
    ### Fix Ancient Dragon Kills

    # fix Ancient Dragon Kills
    df['Ancient Dragon Kills'] = df['Ancient Dragon Kills'].replace(
        {
            '-': '0',
            '': '0',
            r'k$': '000',
            '✔': '1'
        }, regex=True).astype(float)  #replace - and blanks

    ### Fix Team and Team Win

    # set team to 0 or 1 : 0 = blue 1 = red
    df['team'] = np.where(df['team'] == 'Blue', 0, 1)
    df = df.rename(columns={'team': 'Team'})

    # set team win to 0 for loss and 1 for win

    df.loc[(df['Team Win'] == 'Blue') & (df['Team'] == 0), 'Team Win'] = '1'
    df.loc[(df['Team Win'] == 'Red') & (df['Team'] == 1), 'Team Win'] = '1'
    df.loc[df['Team Win'] != '1', 'Team Win'] = '0'
    df['Team Win'] = df['Team Win'].astype(int)

    ### Fix total healing in allies

    # fix total healing in allies
    df = df.rename(columns={'Total Healing in Alleys': 'Total Healing in Allies'})
    df['Total Healing in Allies'] = df['Total Healing in Allies'].fillna(0)

    ### Fix total healing recieved

    # fix total healing recieved
    df['Total Healing Received'] = df['Total Healing Received'].fillna(0)

    ### Fix seconds in game and split into 2 groups

    # fix seconds in game
    ## convert to a category with 3 levels

    # Drop long games and change the values of the other games
    df = df[df['Seconds in Game'] <
            2000]  # drop rows that are longer or equal to 2000

    df['Game_Length'] = 0
    df['Game_Length'] = np.where(df['Seconds in Game'] <= 999, '0_1',
                                 df['Game_Length'])
    df['Game_Length'] = np.where(df['Seconds in Game'] == 1000, '1_2',
                                 df['Game_Length'])
    df['gl_0_1'] = np.where(df['Game_Length'] == '0_1', 1, 0)

    ### Classify Champion Type and create dummy variables

    champ_keys = df['Champion'].tolist()
    champ_dict = dict.fromkeys(champ_keys)

    champ_dict['Ahri'] = 'Burst'
    champ_dict['Akali'] = 'Assassin'
    champ_dict['Akshan'] = 'Marksman', 'Assassin'
    champ_dict['Alistar'] = 'Vanguard'
    champ_dict['Amumu'] = 'Vanguard'
    champ_dict['Annie'] = 'Burst'
    champ_dict['Ashe'] = 'Marksman'
    champ_dict['Aurelion Sol'] = 'Battlemage'
    champ_dict['Blitzcrank'] = 'Catcher'
    champ_dict['Brand'] = 'Burst'
    champ_dict['Braum'] = 'Warden'
    champ_dict['Caitlyn'] = 'Marksman'
    champ_dict['Camille'] = 'Diver'
    champ_dict['Corki'] = 'Marksman'
    champ_dict['Darius'] = 'Juggernaut'
    champ_dict['Diana'] = 'Assassin', 'Diver'
    champ_dict['Dr. Mundo'] = 'Juggernaut'
    champ_dict['Draven'] = 'Marksman'
    champ_dict['Ekko'] = 'Assassin'
    champ_dict['Evelynn'] = 'Assassin'
    champ_dict['Ezreal'] = 'Marksman'
    champ_dict['Fiora'] = 'Skirmisher'
    champ_dict['Fizz'] = 'Assassin'
    champ_dict['Galio'] = 'Warden'
    champ_dict['Garen'] = 'Juggernaut'
    champ_dict['Gragas'] = 'Vanguard'
    champ_dict['Graves'] = 'Specialist'
    champ_dict['Irelia'] = 'Diver'
    champ_dict['Janna'] = 'Enchanter'
    champ_dict['Jarvan IV'] = 'Diver'
    champ_dict['Jax'] = 'Skirmisher'
    champ_dict['Jayce'] = 'Artillery'
    champ_dict['Jhin'] = 'Marksman', 'Catcher'
    champ_dict['Jinx'] = 'Marksman'
    champ_dict["Kai'Sa"] = 'Marksman'
    champ_dict['Karma'] = 'Burst', 'Enchanter'
    champ_dict["Katarina"] = 'Assassin'
    champ_dict["Kayle"] = 'Specialist'
    champ_dict["Kennen"] = 'Specialist'
    champ_dict["Kha'Zix"] = 'Assassin'
    champ_dict["Lee Sin"] = 'Diver'
    champ_dict["Leona"] = 'Vanguard'
    champ_dict["Lucian"] = 'Marksman'
    champ_dict["Lulu"] = 'Enchanter'
    champ_dict["Lux"] = 'Burst', 'Artillery'
    champ_dict["Malphite"] = 'Vanguard'
    champ_dict["Master Yi"] = 'Skirmisher'
    champ_dict["Miss Fortune"] = 'Marksman'
    champ_dict["Morgana"] = 'Catcher'
    champ_dict["Nami"] = 'Enchanter'
    champ_dict["Nasus"] = 'Juggernaut'
    champ_dict["Nunu & Willump"] = 'Vanguard'
    champ_dict["Olaf"] = 'Diver'
    champ_dict["Orianna"] = 'Burst'
    champ_dict["Pantheon"] = 'Diver'
    champ_dict["Rakan"] = 'Catcher'
    champ_dict["Rammus"] = 'Vanguard'
    champ_dict["Renekton"] = 'Diver'
    champ_dict["Rengar"] = 'Assassin', 'Diver'
    champ_dict["Riven"] = 'Skirmisher'
    champ_dict["Senna"] = 'Marksman', 'Enchanter'
    champ_dict["Seraphine"] = 'Burst', 'Enchanter'
    champ_dict["Sett"] = 'Juggernaut'
    champ_dict["Shen"] = 'Warden'
    champ_dict["Singed"] = 'Specialist'
    champ_dict["Sona"] = 'Enchanter'
    champ_dict["Shyvana"] = 'Juggernaut'
    champ_dict["Soraka"] = 'Enchanter'
    champ_dict["Teemo"] = 'Specialist'
    champ_dict["Thresh"] = 'Catcher'
    champ_dict["Tristana"] = 'Marksman'
    champ_dict["Tryndamere"] = 'Skirmisher'
    champ_dict["Twisted Fate"] = 'Burst'
    champ_dict["Varus"] = 'Marksman', 'Artillery'
    champ_dict["Vayne"] = 'Marksman'
    champ_dict["Veigar"] = 'Burst'
    champ_dict["Vi"] = 'Diver'
    champ_dict["Wukong"] = 'Diver'
    champ_dict["Xayah"] = 'Marksman'
    champ_dict["Xin Zhao"] = 'Diver'
    champ_dict["Yasuo"] = 'Skirmisher'
    champ_dict["Yuumi"] = 'Enchanter'
    champ_dict["Zed"] = 'Assassin'
    champ_dict["Ziggs"] = 'Artillery'
    champ_dict["unknown"] = 'unknown'

    #  turn the dictionary of champion subclasses and convert to dataframe for merge
    champ = pd.DataFrame.from_dict(champ_dict)
    champ = champ.T.reset_index()
    champ.columns = ['Champion', 'Subclass1', 'Subclass2']

    # convert df['Champion'] to a df and merge with the champion subclass dictionary to get the champion subclasses for the actual matches
    champ1 = pd.DataFrame(df['Champion'])
    champ = champ1.merge(champ, how='left', on='Champion')

    # create a dictionary to define subclasses into a level up (Classes), map the subclass columns to dictionary
    champ_classes = {
        'Controller': ['Enchanter', 'Catcher'],
        'Fighter': ['Juggernaut', 'Diver'],
        'Mage': ['Burst', 'Battlemage', 'Artillery'],
        'Marksman': ['Marksman'],
        'Slayer': ['Assassin', 'Skirmisher'],
        'Tank': ['Vanguard', 'Warden'],
        'Specialist': ['Specialist']
    }

    d = {val: key for key, lst in champ_classes.items() for val in lst}

    champ['Class1'] = champ.Subclass1.map(d)
    champ['Class2'] = champ.Subclass2.map(d)

    ### One-hot encoding class1

    #Create dummy variables
    dummies_c1 = pd.get_dummies(champ['Class1'],
                                drop_first=False,
                                prefix='lc',
                                dtype='int')
    dummies_c1 = pd.DataFrame(dummies_c1)

    ### One-hot encoding class2

    dummies_c2 = pd.get_dummies(champ['Class2'],
                                drop_first=False,
                                prefix='sc',
                                dtype='int')
    dummies_c2 = pd.DataFrame(dummies_c2)

    dummies_lc = pd.concat([dummies_c1, dummies_c2], axis=1)
    digit = int(len(dummies_lc.columns) / 2)

    # combine dummies tables and only keep the list class
    for col in range(digit):
        for row in range(len(champ.index)):
            if dummies_lc.iloc[row, col] < dummies_lc.iloc[row, int(col + digit)]:
                dummies_lc.iloc[row, col] = 1

    a = [
        'lc_Mage', 'lc_Specialist', 'lc_Controller', 'lc_Fighter', 'lc_Marksman',
        'lc_Slayer', 'lc_Tank', 'sc_Controller', 'sc_Fighter', 'sc_Mage',
        'sc_Marksman', 'sc_Slayer', 'sc_Specialist', 'sc_Tank'
    ]
    b = dummies_lc.columns.tolist()

    set_difference = set(a) - set(b)
    list_difference = list(set_difference)

    for x in range(len(list_difference)):
        c = list_difference[x]
        dummies_lc[c] = 0

    dummies_lc = dummies_lc.drop(columns=[
        'sc_Controller', 'sc_Fighter', 'sc_Mage', 'sc_Marksman', 'sc_Slayer',
        'sc_Specialist', 'sc_Tank'
    ])

    ### One-hot encoding subclass1

    #Create dummy variables
    dummies_s1 = pd.get_dummies(champ['Subclass1'],
                                drop_first=False,
                                prefix='sc',
                                dtype='int')
    dummies_s1 = pd.DataFrame(dummies_s1)

    ### One-hot encoding subclass2

    dummies_s2 = pd.get_dummies(champ['Subclass2'],
                                drop_first=False,
                                prefix='2c',
                                dtype='int')
    dummies_s2 = pd.DataFrame(dummies_s2)

    dummies_sc = pd.concat([dummies_s1, dummies_s2], axis=1)
    digit = int(len(dummies_sc.columns) / 2)

    # combine dummies tables and only keep the list class
    for col in range(digit):
        for row in range(len(champ.index)):
            if dummies_sc.iloc[row, col] < dummies_sc.iloc[row, int(col + digit)]:
                dummies_sc.iloc[row, col] = 1

    #drop largest column

    a = [
        'sc_Enchanter', 'sc_Catcher', 'sc_Juggernaut', 'sc_Diver', 'sc_Burst',
        'sc_Battlemage', 'sc_Artillery', 'sc_Marksman', 'sc_Assassin', 'sc_Skirmisher',
        'sc_Vanguard', 'sc_Warden', 'sc_Specialist', '2c_Artillery', '2c_Assassin',
        '2c_Battlemage', '2c_Burst', '2c_Catcher', '2c_Diver', '2c_Enchanter',
        '2c_Juggernaut', '2c_Marksman', '2c_Skirmisher', '2c_Specialist',
        '2c_Vanguard', '2c_Warden', '2c_unknown'
    ]
    b = dummies_sc.columns.tolist()

    set_difference = set(a) - set(b)
    list_difference = list(set_difference)

    for x in range(len(list_difference)):
        c = list_difference[x]
        dummies_sc[c] = 0
        
    dummies_sc = dummies_sc.drop(columns=[
        '2c_Artillery', '2c_Assassin', '2c_Battlemage', '2c_Burst', '2c_Catcher',
        '2c_Diver', '2c_Enchanter', '2c_Juggernaut', '2c_Marksman',
        '2c_Skirmisher', '2c_Specialist', '2c_Vanguard', '2c_Warden', '2c_unknown'
    ])

    # add new dummies (Champion Class and Subclass) to df
    l1 = df.values.tolist()
    l2 = dummies_lc.values.tolist()
    for i in range(len(l1)):
        l1[i].extend(l2[i])

    df = pd.DataFrame(l1,
                      columns=df.columns.tolist() + dummies_lc.columns.tolist())

    # add new dummies (Champion Class and Subclass) to df
    l1 = df.values.tolist()
    l2 = dummies_sc.values.tolist()
    for i in range(len(l1)):
        l1[i].extend(l2[i])

    df = pd.DataFrame(l1,
                      columns=df.columns.tolist() + dummies_sc.columns.tolist())

    ### Create KDA (kills+assists/deaths)

    # Create KDA (kills+assists/deaths)
    df['KDA'] = np.where(df['Deaths'] == 0, (df['Kills'] + df['Assists']),
                         (df['Kills'] + df['Assists']) / df['Deaths'])

    ## Delete Columns
    df_col = df.columns.tolist()

    # Create df_wildstats without removed columns
    df_wildstats = df[[
        'Match_Num', 'Champion', 'Team', 'Team Win', 'Position Played',
        'rp_AD Carry', 'rp_Jungle', 'rp_Middle', 'rp_Support', 'Champion Level',
        'Game Points', 'Experience Points', 'Kills', 'Kill Participation Rate',
        'Assists', 'Deaths', 'Gold', 'Gold for Kills', 'Minions Killed',
        'Jungle Monster Kills', 'Signals', 'Kill Streaks', 'Assist Streaks',
        'Total Damage Dealt by Abilities', 'Total Damage dealt by Attacks',
        'Damage to Champions Dealt with Abilities',
        'Damage to Champions Dealt with Attacks', 'Total Damage to Champions',
        'Total Damage Dealt to Towers', 'Total Damage Dealt',
        'Damage Taken by Champions', 'Total Damage Tanked', 'Towers Destroyed',
        'Tower Kill Participation', 'Dragons Killed', 'Barons Killed',
        'Red Buff Kills', 'Blue Buff Kills', 'Raptor Kills', 'Krug Kills',
        'Gromp Kills', 'Wolf Kills', 'Scuttlers Kills', 'Nashor Kills',
        'Total Wards', 'Boots Upgrade', 'Total Healing in Allies',
        'Total Healing Received', 'Total Monster Kills', 'Wards Destroyed',
        'Total Shield', 'Shield Used', 'Ancient Dragon Kills', 'Herald Kills',
        'Total Self Healing', 'Active Skill Equipped', 'Summoner Spells Used',
        'Shoe Enchantments Purchased', 'Enemies Controlled',
        'Max Trail Kill Number', 'Quick Chats Sent', 'Remaining Gold',
        'Game_Length', 'gl_0_1', 'lc_Controller', 'lc_Mage', 'lc_Marksman',
        'lc_Slayer', 'lc_Specialist', 'lc_Tank', 'sc_Artillery', 'sc_Assassin',
        'sc_Battlemage', 'sc_Burst', 'sc_Catcher', 'sc_Diver', 'sc_Enchanter',
        'sc_Juggernaut', 'sc_Skirmisher', 'sc_Vanguard', 'sc_Warden', 'sc_Marksman', 'KDA'
    ]]

    #Replace spaces in column names to _
    col_list = df_wildstats.columns.tolist()
    converter = lambda x: x.replace(' ', '_')
    col_list = list(map(converter, col_list))

    #swap new column names
    df_wildstats.columns = col_list
    df_wildstats = df_wildstats.rename(columns={'team': 'Team'})

    ## Create Team Totals
    # sum up team totals
    df_wildstats_grpsum = df_wildstats.groupby(['Match_Num', 'Team'],
                                               as_index=False).sum()

    # create DF to merge team totals
    df_tt = df_wildstats_grpsum[[
        'Match_Num', 'Team', 'Game_Points', 'Kills', 'Deaths', 'Gold', 'Signals',
        'Towers_Destroyed', 'Dragons_Killed', 'Barons_Killed', 'Nashor_Kills',
        'Ancient_Dragon_Kills', 'Herald_Kills'
    ]]
    df_tt = df_tt.rename(
        columns={
            'Game_Points': 'tt_Game_Points',
            'Kills': 'tt_Kills',
            'Deaths': 'tt_Deaths',
            'Gold': 'tt_Gold',
            'Signals': 'tt_Signals',
            'Towers_Destroyed': 'tt_Towers_Destroyed',
            'Dragons_Killed': 'tt_Dragons_Killed',
            'Barons_Killed': 'tt_Barons_Killed',
            'Nashor_Kills': 'tt_Nashor_Kills',
            'Ancient_Dragon_Kills': 'tt_Ancient_Dragon_Kills',
            'Herald_Kills': 'tt_Herald_Kills'
        })

    # merge team totals onto main df
    df_wildstats = df_wildstats.merge(df_tt, on=['Match_Num', 'Team'])

    # drop columns that are included in the Team Totals
    df_wildstats = df_wildstats.drop(columns=[
        'Barons_Killed', 'Dragons_Killed', 'Herald_Kills', 'Nashor_Kills'
    ])

    return df_wildstats

