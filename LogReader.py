import pandas as pd
import os
import math

import tkinter as tk
from tkinter import filedialog


def read_file(file_name, skirmish):
    with open(file_name, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        pilot = lines[2].strip(' Listener: ')
        pilot = pilot.strip('\n')

        for line in lines[3:]:
            new_row = pd.DataFrame({'pilot': pilot, 'linetext': line.strip('\n')}, index=[0])
            skirmish = pd.concat([skirmish, new_row], ignore_index=True)

    return skirmish


def select_files():
    root = tk.Tk()
    return root.tk.splitlist(filedialog.askopenfilenames(parent=root, title='Choose a file'))


def process_lines(skirmish):
    timed_lines = skirmish[skirmish.linetext.str.contains('^\[\s\d*.\d*.\d*\s\d*:\d*:\d*\s\]')]
    
    skirmish['timestamp'] = timed_lines['linetext'].str[:24].str.strip('[ ').str.strip(' ]')
    skirmish['timestamp'] = pd.to_datetime(skirmish['timestamp'], format='%Y.%m.%d %H:%M:%S')
    skirmish['linetext'] = timed_lines['linetext'].str[24:]
    skirmish.dropna(inplace=True)

    skirmish = skirmish[~skirmish.linetext.str.contains("(hint)")]
    skirmish = skirmish[~skirmish.linetext.str.contains("(question)")]
    skirmish = skirmish[~skirmish.linetext.str.contains("(notify)")]
    skirmish = skirmish[~skirmish.linetext.str.contains("(warning)")]
    skirmish = skirmish[~skirmish.linetext.str.contains("(info)")]
    skirmish = skirmish[~skirmish.linetext.str.contains("Warp scramble attempt")]
    skirmish = skirmish[~skirmish.linetext.str.contains("Warp disruption attempt")]
    
    # remote HTML tags
    skirmish['linetext'] = skirmish['linetext'].str[8:]
    skirmish['linetext'] = skirmish['linetext'].str.replace(r'<[^<>]*>', '', regex=True)
    skirmish['module_ammo'] = ''
    skirmish['hit_quality'] = ''
    skirmish['target_pilot'] = pd.NA
    skirmish['shiptype'] = ''
    skirmish['neut_in'] = pd.NA

    # complete misses outgoing
    mask = (skirmish['linetext'].str.contains('Your\s.*misses\s.*completely'))
    complete_misses = skirmish['linetext'].str.split("-")[mask]
    skirmish['hit_quality'] = complete_misses.apply(lambda x: "miss")
    skirmish['module_ammo'] = complete_misses.apply(lambda x: x[1])
    skirmish['target_pilot'] = complete_misses.apply(lambda x: ' '.join(x[0].split("misses")[1].split()[:-1]))

    # neut_in
    mask = (skirmish['linetext'].str.split("GJ energy neutralized").apply(len) > 1)
    energy_neutralized = skirmish['linetext'].str.split("GJ energy neutralized")[mask]
    mask = (skirmish['linetext'].str.split("GJ energy drained to").apply(len) > 1)
    energy_drained = skirmish['linetext'].str.split("GJ energy drained to")[mask]
    
    skirmish['neut_in'] = energy_drained.apply(lambda x: abs(int(x[0])) if int(x[0]) < 0 else 0.1)
    tmp_neut_in_1 = skirmish['neut_in'].copy()
    skirmish['neut_in'] = energy_neutralized.apply(lambda x: int(x[0]))
    tmp_neut_in_2 = skirmish['neut_in'].copy()
 
    skirmish['neut_in'] = skirmish.apply(lambda x: tmp_neut_in_1[x.name] if pd.isna(x.neut_in) else x.neut_in, axis=1)
    skirmish['neut_in'] = skirmish.apply(lambda x: tmp_neut_in_2[x.name] if pd.isna(x.neut_in) else x.neut_in, axis=1)
    
    skirmish['linetext'] = skirmish['linetext'].str.replace(r'\d*\sGJ\s\w*\sneutralized', '', regex=True)
    skirmish['linetext'] = skirmish['linetext'].str.replace(r'-\d*\sGJ\s\w*\sdrained\sto', '', regex=True)

    skirmish['shiptype'] = skirmish.apply(lambda x: x.linetext.split()[0] if x.neut_in > 0 else x.shiptype, axis=1)
    skirmish['linetext'] = skirmish.apply(lambda x: ' '.join(x.linetext.split()[1:]) if x.neut_in > 0 else x.linetext, axis=1)
    skirmish['module_ammo'] = skirmish.apply(lambda x: ''.join(x.linetext.split("-")[1:]) if x.neut_in > 0 else x.module_ammo, axis=1)
    skirmish['linetext'] = skirmish.apply(lambda x: '' if x.neut_in > 0 else x.linetext, axis=1)
    skirmish['neut_in'] = skirmish['neut_in'].fillna(0).astype(int)

    # remote repair outgoing
    mask = (skirmish['linetext'].str.split("remote armor repaired to").apply(len) > 1)
    remote_repair_outgoing = skirmish['linetext'].str.split("remote armor repaired to")[mask]

    skirmish['armor_repair_outgoing'] = remote_repair_outgoing.apply(lambda x: int(x[0]) if int(x[0]) > 0 else 0.1)

    skirmish['linetext'] = skirmish['linetext'].str.replace(r'\d*\sremote\sarmor\srepaired\sto', '', regex=True)
    skirmish['shiptype'] = skirmish.apply(lambda x: x.linetext.split()[0] if x.armor_repair_outgoing > 0 else x.shiptype, axis=1)

    skirmish['linetext'] = skirmish.apply(lambda x: ' '.join(x.linetext.split()[1:]) if x.armor_repair_outgoing > 0 else x.linetext, axis=1)
    skirmish['module_ammo'] = skirmish.apply(lambda x: ''.join(x.linetext.split("-")[1:]) if x.armor_repair_outgoing > 0 else x.module_ammo, axis=1)
    skirmish['linetext'] = skirmish.apply(lambda x: '' if x.armor_repair_outgoing > 0 else x.linetext, axis=1)
    skirmish['armor_repair_outgoing'] = skirmish['armor_repair_outgoing'].fillna(0).astype(int)

    # remote repair incoming
    mask = (skirmish['linetext'].str.split("remote armor repaired by").apply(len) > 1)
    remote_repair_incoming = skirmish['linetext'].str.split("remote armor repaired by")[mask]

    skirmish['armor_repair_incoming'] = remote_repair_incoming.apply(lambda x: int(x[0]) if int(x[0]) > 0 else 0.1)

    skirmish['linetext'] = skirmish['linetext'].str.replace(r'\d*\sremote\sarmor\srepaired\sby', '', regex=True)
    skirmish['shiptype'] = skirmish.apply(lambda x: x.linetext.split()[0] if x.armor_repair_incoming > 0 else x.shiptype, axis=1)

    skirmish['linetext'] = skirmish.apply(lambda x: ' '.join(x.linetext.split()[1:]) if x.armor_repair_incoming > 0 else x.linetext, axis=1)
    skirmish['module_ammo'] = skirmish.apply(lambda x: ''.join(x.linetext.split("-")[1:]) if x.armor_repair_incoming > 0 else x.module_ammo, axis=1)
    skirmish['linetext'] = skirmish.apply(lambda x: '' if x.armor_repair_incoming > 0 else x.linetext, axis=1)
    skirmish['armor_repair_incoming'] = skirmish['armor_repair_incoming'].fillna(0).astype(int)

    # damage incoming
    mask = (skirmish['linetext'].str.split("from").apply(len) > 1)
    damage_incoming = skirmish['linetext'].str.split("from")[mask]

    skirmish['damage_incoming'] = damage_incoming.apply(lambda x: int(x[0]))
    skirmish['linetext'] = skirmish['linetext'].str.replace(r'\d+\sfrom\s', '', regex=True)

    tmp = skirmish['linetext'].str.split("-")[mask]
    tmp_module = skirmish['module_ammo'].copy()
    tmp_quality = skirmish['hit_quality'].copy()
    tmp_pilots = skirmish['target_pilot'].copy()

    skirmish['module_ammo'] = tmp.apply(lambda x: x[1] if len(x) > 2 else '')
    skirmish['hit_quality'] = tmp.apply(lambda x: x[2] if len(x) > 2 else x[1])
    skirmish['target_pilot'] = tmp.apply(lambda x: x[0] if len(x) < 3 else pd.NA)

    skirmish['hit_quality'] = skirmish.apply(lambda x: tmp_quality[x.name] if pd.isna(x.hit_quality) else x.hit_quality, axis=1)
    skirmish['module_ammo'] = skirmish.apply(lambda x: tmp_module[x.name] if pd.isna(x.module_ammo) else x.module_ammo, axis=1)
    skirmish['target_pilot'] = skirmish.apply(lambda x: tmp_pilots[x.name] if pd.isna(x.target_pilot) else x.target_pilot, axis=1)

    skirmish['linetext'] = skirmish.apply(lambda x: ''.join(x.linetext.split('-')[0]) if x.damage_incoming > 0 else x.linetext, axis=1)
    skirmish['shiptype'] = skirmish.apply(lambda x: x.linetext.split("(")[1].strip(") ") if x.damage_incoming > 0 and len(x.linetext.split("(")) > 1 else x.shiptype, axis=1)

    skirmish['target_pilot'] = skirmish.apply(lambda x: x.linetext.split("(")[0].strip(") ") if x.damage_incoming > 0 and len(x.linetext.split("(")) > 1 else x.target_pilot, axis=1)
    skirmish['linetext'] = skirmish.apply(lambda x: '' if x.damage_incoming > 0 and len(x.linetext.split("(")) > 1 else x.linetext, axis=1)
    
    # damage outgoing
    mask = (skirmish['linetext'].str.split("to").apply(lambda x: True if len(x) > 1 and "ISK" not in x[0] else False))
    damage_outgoing = skirmish['linetext'].str.split("to")[mask]

    skirmish['damage_outgoing'] = damage_outgoing.apply(lambda x: int(x[0]))
    skirmish['linetext'] = skirmish['linetext'].str.replace(r'\d+\sto\s', '', regex=True)

    tmp = skirmish['linetext'].str.split("-")[mask]

    tmp_module = skirmish['module_ammo'].copy()
    tmp_quality = skirmish['hit_quality'].copy()
    tmp_pilots = skirmish['target_pilot'].copy()

    skirmish['module_ammo'] = tmp.apply(lambda x: x[1] if len(x) > 2 else '')
    skirmish['hit_quality'] = tmp.apply(lambda x: x[2] if len(x) > 2 else x[1])
    skirmish['target_pilot'] = tmp.apply(lambda x: x[0] if len(x) < 3 else pd.NA)

    skirmish['hit_quality'] = skirmish.apply(lambda x: tmp_quality[x.name] if pd.isna(x.hit_quality) else x.hit_quality, axis=1)
    skirmish['module_ammo'] = skirmish.apply(lambda x: tmp_module[x.name] if pd.isna(x.module_ammo) else x.module_ammo, axis=1)
    skirmish['target_pilot'] = skirmish.apply(lambda x: tmp_pilots[x.name] if pd.isna(x.target_pilot) else x.target_pilot, axis=1)

    skirmish['linetext'] = skirmish.apply(lambda x: ''.join(x.linetext.split('-')[0]) if x.damage_outgoing > 0 else x.linetext, axis=1)
    skirmish['shiptype'] = skirmish.apply(lambda x: x.linetext.split("(")[1].strip(") ") if x.damage_outgoing > 0 and len(x.linetext.split("(")) > 1 else x.shiptype, axis=1)

    skirmish['target_pilot'] = skirmish.apply(lambda x: x.linetext.split("(")[0].strip(") ") if x.damage_outgoing > 0 and len(x.linetext.split("(")) > 1 else x.target_pilot, axis=1)
    skirmish['linetext'] = skirmish.apply(lambda x: '' if x.damage_outgoing > 0 and len(x.linetext.split("(")) > 1 else x.linetext, axis=1)

    skirmish.drop(columns='linetext', inplace=True)
    skirmish.to_csv("test.csv")

    print(skirmish.head(10))



def new_skirmish():
    files = select_files()

    skirmish = pd.DataFrame()

    for file in files:
        skirmish = read_file(file, skirmish)

    process_lines(skirmish)
    

if __name__ == '__main__':
    new_skirmish()
