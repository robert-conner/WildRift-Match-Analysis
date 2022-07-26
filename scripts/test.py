#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def test(df_wildstats):
    #import libs

    from sklearn.model_selection import cross_val_score
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import confusion_matrix, classification_report
    from sklearn.metrics import precision_score, recall_score
    from sklearn.metrics import plot_confusion_matrix
    from sklearn.metrics import roc_curve, roc_auc_score
    from sklearn.metrics import f1_score
    from numpy import arange

    # import train_test_split and apply to dataset
    from sklearn.model_selection import train_test_split
    import pickle

    #Create X, y
    X = df_wildstats[[
        'Team', 'rp_AD_Carry', 'rp_Jungle', 'rp_Middle',
        'rp_Support', 'Champion_Level', 'Experience_Points', 'Kills',
        'Kill_Participation_Rate', 'Assists', 'Deaths', 'Gold', 'Gold_for_Kills',
        'Minions_Killed', 'Jungle_Monster_Kills', 'Signals', 'Kill_Streaks',
        'Assist_Streaks', 'Total_Damage_Dealt_by_Abilities',
        'Total_Damage_dealt_by_Attacks',
        'Damage_to_Champions_Dealt_with_Abilities',
        'Damage_to_Champions_Dealt_with_Attacks', 'Total_Damage_to_Champions',
        'Total_Damage_Dealt_to_Towers', 'Total_Damage_Dealt',
        'Damage_Taken_by_Champions', 'Total_Damage_Tanked', 'Towers_Destroyed',
        'Tower_Kill_Participation', 'Red_Buff_Kills', 'Blue_Buff_Kills',
        'Raptor_Kills', 'Krug_Kills', 'Gromp_Kills', 'Wolf_Kills',
        'Scuttlers_Kills', 'Total_Wards', 'Boots_Upgrade',
        'Total_Healing_in_Allies', 'Total_Monster_Kills',
        'Wards_Destroyed', 'Total_Shield', 'Shield_Used', 'Total_Self_Healing',
        'Active_Skill_Equipped', 'Summoner_Spells_Used',
        'Shoe_Enchantments_Purchased', 'Enemies_Controlled',
        'Max_Trail_Kill_Number', 'Quick_Chats_Sent', 'Remaining_Gold',
        'Game_Length', 'gl_0_1', 'lc_Controller', 'lc_Mage', 'lc_Marksman',
        'lc_Slayer', 'lc_Specialist', 'lc_Tank', 'sc_Artillery', 'sc_Assassin',
        'sc_Battlemage', 'sc_Burst', 'sc_Catcher', 'sc_Diver', 'sc_Enchanter',
        'sc_Juggernaut', 'sc_Skirmisher', 'sc_Vanguard', 'sc_Warden', 'KDA',
        'tt_Kills', 'tt_Deaths', 'tt_Gold', 'tt_Signals', 'tt_Towers_Destroyed',
        'tt_Dragons_Killed', 'tt_Barons_Killed', 'tt_Nashor_Kills',
        'tt_Ancient_Dragon_Kills', 'tt_Herald_Kills'
    ]]
    y = df_wildstats['Team_Win']
    
    #Predict with the model
    #2) Fit the model with training data

    # load the model from disk
    model = pickle.load(open('final_dec_model.sav', 'rb'))   
    return X, y, model

