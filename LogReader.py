import pandas as pd
import re

import tkinter as tk
from tkinter import filedialog

from logfile_regex import _logLanguageRegex as logrex


# this is inspired by https://github.com/ArtificialQualia/PyEveLiveDPS/blob/master/PyEveLiveDPS/logreader.py
class AnalysingLogReader:
    def __init__(self):
        self.files = self.select_files()
        self.language = "english"

        self.main_frame = pd.DataFrame()

        self.damage_out = pd.DataFrame()
        self.damage_in = pd.DataFrame()

        self.armorRepaired_out = pd.DataFrame()
        self.armorRepaired_in = pd.DataFrame()

        self.shieldBoosted_out = pd.DataFrame()
        self.shieldBoosted_in = pd.DataFrame()

        self.hullRepaired_out = pd.DataFrame()
        self.hullRepaired_in = pd.DataFrame()

        self.capTransfer_out = pd.DataFrame()
        self.capTransfer_in = pd.DataFrame()

        self.capNeutralized_out = pd.DataFrame()
        self.capNeutralized_in = pd.DataFrame()

        self.nosRecieved = pd.DataFrame()
        self.nosTaken = pd.DataFrame()

        self.misses_out = pd.DataFrame()
        self.misses_in = pd.DataFrame()

        self.mined = pd.DataFrame()

    def select_files(self):
        root = tk.Tk()
        return root.tk.splitlist(
            filedialog.askopenfilenames(parent=root, title="Choose a file")
        )

    def read_files(self):
        for file_name in self.files:
            self.read_file(file_name)

        self.populate_frames()

    def read_file(self, file_name):
        with open(file_name, "r", encoding="utf-8") as f:
            lines = f.readlines()
            pilot = lines[2].strip(" Listener: ")
            pilot = pilot.strip("\n")

            for line in lines[3:]:
                new_row = pd.DataFrame(
                    {"pilot": pilot, "linetext": line.strip("\n")}, index=[0]
                )
                self.main_frame = pd.concat(
                    [self.main_frame, new_row], ignore_index=True
                )

    def populate_frames(self):
        # strip lines without timestamps
        timed_lines = self.main_frame[
            self.main_frame.linetext.str.contains("^\[\s\d*.\d*.\d*\s\d*:\d*:\d*\s\]")
        ]

        self.main_frame["timestamp"] = (
            timed_lines["linetext"].str[:24].str.strip("[ ").str.strip(" ]")
        )
        self.main_frame["timestamp"] = pd.to_datetime(
            self.main_frame["timestamp"], format="%Y.%m.%d %H:%M:%S"
        )
        self.main_frame["linetext"] = timed_lines["linetext"].str[24:]
        self.main_frame.dropna(inplace=True)

        self.damage_out = self.main_frame[
            self.main_frame.linetext.str.contains(
                logrex[self.language]["damageOut"], regex=True
            )
        ].copy()
        self.damage_in = self.main_frame[
            self.main_frame.linetext.str.contains(
                logrex[self.language]["damageIn"], regex=True
            )
        ].copy()

        self.armorRepaired_out = self.main_frame[
            self.main_frame.linetext.str.contains(
                logrex[self.language]["armorRepairedOut"], regex=True
            )
        ].copy()
        self.armorRepaired_in = self.main_frame[
            self.main_frame.linetext.str.contains(
                logrex[self.language]["armorRepairedIn"], regex=True
            )
        ].copy()

        self.shieldBoosted_out = self.main_frame[
            self.main_frame.linetext.str.contains(
                logrex[self.language]["shieldBoostedOut"], regex=True
            )
        ].copy()
        self.shieldBoosted_in = self.main_frame[
            self.main_frame.linetext.str.contains(
                logrex[self.language]["shieldBoostedIn"], regex=True
            )
        ].copy()

        self.hullRepaired_out = self.main_frame[
            self.main_frame.linetext.str.contains(
                logrex[self.language]["hullRepairedOut"], regex=True
            )
        ].copy()
        self.hullRepaired_in = self.main_frame[
            self.main_frame.linetext.str.contains(
                logrex[self.language]["hullRepairedIn"], regex=True
            )
        ].copy()

        self.capTransfer_out = self.main_frame[
            self.main_frame.linetext.str.contains(
                logrex[self.language]["capTransferedOut"], regex=True
            )
        ].copy()
        self.capTransfer_in = self.main_frame[
            self.main_frame.linetext.str.contains(
                logrex[self.language]["capTransferedIn"], regex=True
            )
        ].copy()

        self.capNeutralized_out = self.main_frame[
            self.main_frame.linetext.str.contains(
                logrex[self.language]["capNeutralizedOut"], regex=True
            )
        ].copy()
        self.capNeutralized_in = self.main_frame[
            self.main_frame.linetext.str.contains(
                logrex[self.language]["capNeutralizedIn"], regex=True
            )
        ].copy()

        self.nosRecieved = self.main_frame[
            self.main_frame.linetext.str.contains(
                logrex[self.language]["nosRecieved"], regex=True
            )
        ].copy()
        self.nosTaken = self.main_frame[
            self.main_frame.linetext.str.contains(
                logrex[self.language]["nosTaken"], regex=True
            )
        ].copy()

        self.misses_out = pd.DataFrame()
        self.misses_in = pd.DataFrame()

        self.mined = self.main_frame[
            self.main_frame.linetext.str.contains(
                logrex[self.language]["mined"], regex=True
            )
        ].copy()

    def export_frames(self, path="./all_csv/"):
        self.damage_out.to_csv(path + "damage_out.csv")
        self.damage_in.to_csv(path + "damage_in.csv")

        self.armorRepaired_out.to_csv(path + "armorRepaired_out.csv")
        self.armorRepaired_in.to_csv(path + "armorRepaired_in.csv")

        self.shieldBoosted_out.to_csv(path + "shieldBoosted_out.csv")
        self.shieldBoosted_in.to_csv(path + "shieldBoosted_in.csv")

        self.hullRepaired_out.to_csv(path + "hullRepaired_out.csv")
        self.hullRepaired_in.to_csv(path + "hullRepaired_in.csv")

        self.capTransfer_out.to_csv(path + "capTransfer_out.csv")
        self.capTransfer_in.to_csv(path + "capTransfer_in.csv")

        self.capNeutralized_out.to_csv(path + "capNeutralized_out.csv")
        self.capNeutralized_in.to_csv(path + "capNeutralized_in.csv")

        self.nosRecieved.to_csv(path + "nosRecieved.csv")
        self.nosTaken.to_csv(path + "nosTaken.csv")

        self.misses_out.to_csv(path + "misses_out.csv")
        self.misses_in.to_csv(path + "misses_in.csv")

        self.mined.to_csv(path + "mined.csv")

    def process_frames(self):
        self.process_damage()
        self.process_remoteArmor()
        self.process_shieldBoost()
        self.process_hullRepair()
        self.process_capTransfer()
        self.process_capNeutralization()
        self.process_nos()
        self.process_misses()
        self.process_mining()

    def process_damage(self):
        if not self.damage_in.empty:
            self.damage_in["linetext"] = self.damage_in["linetext"].str.replace(
                r"<[^<>]*>", "", regex=True
            )
            self.damage_in["linetext"] = self.damage_in["linetext"].str.replace(
                r"\s*\(combat\)\s", "", regex=True
            )

            self.damage_in["hit_quality"] = self.damage_in.apply(
                lambda x: x.linetext.rsplit(
                    "- ",
                )[-1],
                axis=1,
            )
            self.damage_in["dmg"] = self.damage_in.apply(
                lambda x: x.linetext.split(" ")[0], axis=1
            ).astype(int)

            self.damage_in["linetext"] = self.damage_in["linetext"].str.replace(
                r"\d*\sfrom\s", "", regex=True
            )

            self.damage_in["module_or_ammo"] = self.damage_in.apply(
                lambda x: x.linetext.rsplit(" - ", 2)[-2]
                if len(x.linetext.rsplit(" - ", 2)) > 2
                else pd.NA,
                axis=1,
            )
            self.damage_in["shiptype"] = self.damage_in.apply(
                lambda x: x.linetext.rsplit(" - ", 2)[0].rsplit("(")[-1].strip(")")
                if len(x.linetext.rsplit(" - ", 2)) > 2
                else x.linetext.rsplit(" - ", 1)[0],
                axis=1,
            )

            self.damage_in["linetext"] = self.damage_in.apply(
                lambda x: x.linetext.rsplit(" - ", 2)[0], axis=1
            )
            self.damage_in["linetext"] = self.damage_in.apply(
                lambda x: x.linetext.rsplit("(", 1)[0], axis=1
            )
            self.damage_in["linetext"] = self.damage_in.apply(
                lambda x: x.linetext.rsplit("[", 1)[0], axis=1
            )

            self.damage_in.rename({"linetext": "aggressor"}, axis=1, inplace=True)
            self.damage_in = self.damage_in[
                [
                    "timestamp",
                    "pilot",
                    "aggressor",
                    "shiptype",
                    "module_or_ammo",
                    "dmg",
                    "hit_quality",
                ]
            ]

        if not self.damage_out.empty:
            self.damage_out["linetext"] = self.damage_out["linetext"].str.replace(
                r"<[^<>]*>", "", regex=True
            )
            self.damage_out["linetext"] = self.damage_out["linetext"].str.replace(
                r"\s*\(combat\)\s", "", regex=True
            )

            self.damage_out["hit_quality"] = self.damage_out.apply(
                lambda x: x.linetext.rsplit(
                    "- ",
                )[-1],
                axis=1,
            )
            self.damage_out["dmg"] = self.damage_out.apply(
                lambda x: x.linetext.split(" ")[0], axis=1
            ).astype(int)

            self.damage_out["linetext"] = self.damage_out["linetext"].str.replace(
                r"\d*\sto\s", "", regex=True
            )

            self.damage_out["module_or_ammo"] = self.damage_out.apply(
                lambda x: x.linetext.rsplit(" - ", 2)[-2]
                if len(x.linetext.rsplit(" - ", 2)) > 2
                else pd.NA,
                axis=1,
            )
            self.damage_out["shiptype"] = self.damage_out.apply(
                lambda x: x.linetext.rsplit(" - ", 2)[0].rsplit("(")[-1].strip(")")
                if len(x.linetext.rsplit(" - ", 2)) > 2
                else x.linetext.rsplit(" - ", 1)[0],
                axis=1,
            )

            self.damage_out["linetext"] = self.damage_out.apply(
                lambda x: x.linetext.rsplit(" - ", 2)[0], axis=1
            )
            self.damage_out["linetext"] = self.damage_out.apply(
                lambda x: x.linetext.rsplit("(", 1)[0], axis=1
            )
            self.damage_out["linetext"] = self.damage_out.apply(
                lambda x: x.linetext.rsplit("[", 1)[0], axis=1
            )

            self.damage_out.rename({"linetext": "target"}, axis=1, inplace=True)
            self.damage_out = self.damage_out[
                [
                    "timestamp",
                    "pilot",
                    "target",
                    "shiptype",
                    "module_or_ammo",
                    "dmg",
                    "hit_quality",
                ]
            ]

    def process_remoteArmor(self):
        if not self.armorRepaired_in.empty:
            # in
            self.armorRepaired_in["linetext"] = self.armorRepaired_in[
                "linetext"
            ].str.replace(r"<[^<>]*>", "", regex=True)
            self.armorRepaired_in["linetext"] = self.armorRepaired_in[
                "linetext"
            ].str.replace(r"\s*\(combat\)\s", "", regex=True)

            self.armorRepaired_in["amount"] = self.armorRepaired_in.apply(
                lambda x: x.linetext.split(" ")[0], axis=1
            ).astype(int)

            self.armorRepaired_in["linetext"] = self.armorRepaired_in[
                "linetext"
            ].str.replace(r"\d*\sremote\sarmor\srepaired\sby\s", "", regex=True)
            self.armorRepaired_in["module_or_ammo"] = self.armorRepaired_in.apply(
                lambda x: x.linetext.rsplit(" - ", 1)[-1], axis=1
            )
            self.armorRepaired_in["linetext"] = self.armorRepaired_in.apply(
                lambda x: x.linetext.rsplit(" - ", 1)[0], axis=1
            )

            self.armorRepaired_in.rename({"linetext": "brackets"}, axis=1, inplace=True)
            self.armorRepaired_in = self.armorRepaired_in[
                ["timestamp", "pilot", "brackets", "module_or_ammo", "amount"]
            ]

        if not self.armorRepaired_out.empty:
            # out
            self.armorRepaired_out["linetext"] = self.armorRepaired_out[
                "linetext"
            ].str.replace(r"<[^<>]*>", "", regex=True)
            self.armorRepaired_out["linetext"] = self.armorRepaired_out[
                "linetext"
            ].str.replace(r"\s*\(combat\)\s", "", regex=True)

            self.armorRepaired_out["amount"] = self.armorRepaired_out.apply(
                lambda x: x.linetext.split(" ")[0], axis=1
            ).astype(int)

            self.armorRepaired_out["linetext"] = self.armorRepaired_out[
                "linetext"
            ].str.replace(r"\d*\sremote\sarmor\srepaired\sto\s", "", regex=True)
            self.armorRepaired_out["module_or_ammo"] = self.armorRepaired_out.apply(
                lambda x: x.linetext.rsplit(" - ", 1)[-1], axis=1
            )
            self.armorRepaired_out["linetext"] = self.armorRepaired_out.apply(
                lambda x: x.linetext.rsplit(" - ", 1)[0], axis=1
            )

            self.armorRepaired_out.rename(
                {"linetext": "brackets"}, axis=1, inplace=True
            )
            self.armorRepaired_out = self.armorRepaired_out[
                ["timestamp", "pilot", "brackets", "module_or_ammo", "amount"]
            ]

    def process_shieldBoost(self):
        if not self.shieldBoosted_in.empty:
            # incoming
            self.shieldBoosted_in["linetext"] = self.shieldBoosted_in[
                "linetext"
            ].str.replace(r"<[^<>]*>", "", regex=True)
            self.shieldBoosted_in["linetext"] = self.shieldBoosted_in[
                "linetext"
            ].str.replace(r"\s*\(combat\)\s", "", regex=True)

            self.shieldBoosted_in["amount"] = self.shieldBoosted_in.apply(
                lambda x: x.linetext.split(" ")[0], axis=1
            ).astype(int)

            self.shieldBoosted_in["linetext"] = self.shieldBoosted_in[
                "linetext"
            ].str.replace(r"\d*\sremote\sshield\sboosted\sby\s", "", regex=True)
            self.shieldBoosted_in["module_or_ammo"] = self.shieldBoosted_in.apply(
                lambda x: x.linetext.rsplit(" - ", 1)[-1], axis=1
            )
            self.shieldBoosted_in["linetext"] = self.shieldBoosted_in.apply(
                lambda x: x.linetext.rsplit(" - ", 1)[0], axis=1
            )

            self.shieldBoosted_in.rename({"linetext": "brackets"}, axis=1, inplace=True)
            self.shieldBoosted_in = self.shieldBoosted_in[
                ["timestamp", "pilot", "brackets", "module_or_ammo", "amount"]
            ]

        if not self.shieldBoosted_out.empty:
            # outgoing
            self.shieldBoosted_out["linetext"] = self.shieldBoosted_out[
                "linetext"
            ].str.replace(r"<[^<>]*>", "", regex=True)
            self.shieldBoosted_out["linetext"] = self.shieldBoosted_out[
                "linetext"
            ].str.replace(r"\s*\(combat\)\s", "", regex=True)

            self.shieldBoosted_out["amount"] = self.shieldBoosted_out.apply(
                lambda x: x.linetext.split(" ")[0], axis=1
            ).astype(int)

            self.shieldBoosted_out["linetext"] = self.shieldBoosted_out[
                "linetext"
            ].str.replace(r"\d*\sremote\sshield\sboosted\sto\s", "", regex=True)
            self.shieldBoosted_out["module_or_ammo"] = self.shieldBoosted_out.apply(
                lambda x: x.linetext.rsplit(" - ", 1)[-1], axis=1
            )
            self.shieldBoosted_out["linetext"] = self.shieldBoosted_out.apply(
                lambda x: x.linetext.rsplit(" - ", 1)[0], axis=1
            )

            self.shieldBoosted_out.rename(
                {"linetext": "brackets"}, axis=1, inplace=True
            )
            self.shieldBoosted_out = self.shieldBoosted_out[
                ["timestamp", "pilot", "brackets", "module_or_ammo", "amount"]
            ]

    def process_hullRepair(self):
        if not self.hullRepaired_in.empty:
            # in
            self.hullRepaired_in["linetext"] = self.hullRepaired_in[
                "linetext"
            ].str.replace(r"<[^<>]*>", "", regex=True)
            self.hullRepaired_in["linetext"] = self.hullRepaired_in[
                "linetext"
            ].str.replace(r"\s*\(combat\)\s", "", regex=True)

            self.hullRepaired_in["amount"] = self.hullRepaired_in.apply(
                lambda x: x.linetext.split(" ")[0], axis=1
            ).astype(int)

            self.hullRepaired_in["linetext"] = self.hullRepaired_in[
                "linetext"
            ].str.replace(r"\d*\sremote\shull\srepaired\sby\s", "", regex=True)
            self.hullRepaired_in["module_or_ammo"] = self.hullRepaired_in.apply(
                lambda x: x.linetext.rsplit(" - ", 1)[-1], axis=1
            )
            self.hullRepaired_in["linetext"] = self.hullRepaired_in.apply(
                lambda x: x.linetext.rsplit(" - ", 1)[0], axis=1
            )

            self.hullRepaired_in.rename({"linetext": "brackets"}, axis=1, inplace=True)
            self.hullRepaired_in = self.hullRepaired_in[
                ["timestamp", "pilot", "brackets", "module_or_ammo", "amount"]
            ]

        if not self.hullRepaired_out.empty:
            # # out
            self.hullRepaired_out["linetext"] = self.hullRepaired_out[
                "linetext"
            ].str.replace(r"<[^<>]*>", "", regex=True)
            self.hullRepaired_out["linetext"] = self.hullRepaired_out[
                "linetext"
            ].str.replace(r"\s*\(combat\)\s", "", regex=True)

            self.hullRepaired_out["amount"] = self.hullRepaired_out.apply(
                lambda x: x.linetext.split(" ")[0], axis=1
            ).astype(int)

            self.hullRepaired_out["linetext"] = self.hullRepaired_out[
                "linetext"
            ].str.replace(r"\d*\sremote\shull\srepaired\sto\s", "", regex=True)
            self.hullRepaired_out["module_or_ammo"] = self.hullRepaired_out.apply(
                lambda x: x.linetext.rsplit(" - ", 1)[-1], axis=1
            )
            self.hullRepaired_out["linetext"] = self.hullRepaired_out.apply(
                lambda x: x.linetext.rsplit(" - ", 1)[0], axis=1
            )

            self.hullRepaired_out.rename({"linetext": "brackets"}, axis=1, inplace=True)
            self.hullRepaired_out = self.hullRepaired_out[
                ["timestamp", "pilot", "brackets", "module_or_ammo", "amount"]
            ]

    def process_capTransfer(self):
        if not self.capTransfer_in.empty:
            self.capTransfer_in["linetext"] = self.capTransfer_in[
                "linetext"
            ].str.replace(r"<[^<>]*>", "", regex=True)
            self.capTransfer_in["linetext"] = self.capTransfer_in[
                "linetext"
            ].str.replace(r"\s*\(combat\)\s", "", regex=True)
            
            self.capTransfer_in["amount"] = self.capTransfer_in.apply(
                lambda x: x.linetext.split(" ")[0], axis=1
            ).astype(int)

            self.capTransfer_in["linetext"] = self.capTransfer_in[
                "linetext"
            ].str.replace(r"\d*\sremote\scapacitor\stransmitted\sby\s", "", regex=True)
            self.capTransfer_in["module_or_ammo"] = self.capTransfer_in.apply(
                lambda x: x.linetext.rsplit(" - ", 1)[-1], axis=1
            )
            self.capTransfer_in["linetext"] = self.capTransfer_in.apply(
                lambda x: x.linetext.rsplit(" - ", 1)[0], axis=1
            )

            self.capTransfer_in.rename({"linetext": "brackets"}, axis=1, inplace=True)
            self.capTransfer_in = self.capTransfer_in[
                ["timestamp", "pilot", "brackets", "module_or_ammo", "amount"]
            ]

        if not self.capTransfer_out.empty:
            self.capTransfer_out["linetext"] = self.capTransfer_out[
                "linetext"
            ].str.replace(r"<[^<>]*>", "", regex=True)
            self.capTransfer_out["linetext"] = self.capTransfer_out[
                "linetext"
            ].str.replace(r"\s*\(combat\)\s", "", regex=True)

            self.capTransfer_out["amount"] = self.capTransfer_out.apply(
                lambda x: x.linetext.split(" ")[0], axis=1
            ).astype(int)

            self.capTransfer_out["linetext"] = self.capTransfer_out[
                "linetext"
            ].str.replace(r"\d*\sremote\scapacitor\stransmitted\sto\s", "", regex=True)
            self.capTransfer_out["module_or_ammo"] = self.capTransfer_out.apply(
                lambda x: x.linetext.rsplit(" - ", 1)[-1], axis=1
            )
            self.capTransfer_out["linetext"] = self.capTransfer_out.apply(
                lambda x: x.linetext.rsplit(" - ", 1)[0], axis=1
            )

            self.capTransfer_out.rename({"linetext": "brackets"}, axis=1, inplace=True)
            self.capTransfer_out = self.capTransfer_out[
                ["timestamp", "pilot", "brackets", "module_or_ammo", "amount"]
            ]

    def process_capNeutralization(self):
        if not self.capNeutralized_in.empty:
            self.capNeutralized_in["linetext"] = self.capNeutralized_in[
                "linetext"
            ].str.replace(r"<[^<>]*>", "", regex=True)
            self.capNeutralized_in["linetext"] = self.capNeutralized_in[
                "linetext"
            ].str.replace(r"\s*\(combat\)\s", "", regex=True)

        if not self.capNeutralized_out.empty:
            self.capNeutralized_out["linetext"] = self.capNeutralized_out[
                "linetext"
            ].str.replace(r"<[^<>]*>", "", regex=True)
            self.capNeutralized_out["linetext"] = self.capNeutralized_out[
                "linetext"
            ].str.replace(r"\s*\(combat\)\s", "", regex=True)


    def process_nos(self):
        if not self.nosRecieved.empty:
            self.nosRecieved["linetext"] = self.nosRecieved[
                "linetext"
            ].str.replace(r"<[^<>]*>", "", regex=True)
            self.nosRecieved["linetext"] = self.nosRecieved[
                "linetext"
            ].str.replace(r"\s*\(combat\)\s", "", regex=True)

        if not self.nosTaken.empty:
            self.nosTaken["linetext"] = self.nosTaken[
                "linetext"
            ].str.replace(r"<[^<>]*>", "", regex=True)
            self.nosTaken["linetext"] = self.nosTaken[
                "linetext"
            ].str.replace(r"\s*\(combat\)\s", "", regex=True)

    def process_misses(self):
        pass

    def process_mining(self):
        pass


def process_misses(skirmish):
    # complete misses outgoing
    mask = skirmish["linetext"].str.contains("Your\s.*misses\s.*completely")
    complete_misses = skirmish["linetext"].str.split("-")[mask]
    skirmish["hit_quality"] = complete_misses.apply(lambda x: "Miss")
    skirmish["module_ammo"] = complete_misses.apply(lambda x: x[1])
    skirmish["target_pilot"] = complete_misses.apply(
        lambda x: " ".join(x[0].split("misses")[1].split()[:-1])
    )
    skirmish["linetext"] = skirmish.apply(
        lambda x: x.linetext if pd.isna(x.hit_quality) else "", axis=1
    )

    tmp_quality = skirmish["hit_quality"].copy()
    tmp_module = skirmish["module_ammo"].copy()
    tmp_pilots = skirmish["target_pilot"].copy()

    mask = skirmish["linetext"].str.contains("misses\syou\scompletely")
    complete_misses = skirmish["linetext"].str.split("-")[mask]

    skirmish["hit_quality"] = complete_misses.apply(lambda x: "Miss")
    skirmish["module_ammo"] = complete_misses.apply(
        lambda x: x[1] if len(x) > 1 else pd.NA
    )
    skirmish["target_pilot"] = complete_misses.apply(
        lambda x: "".join(x[0].split("misses")[0])
    )

    skirmish["hit_quality"] = skirmish.apply(
        lambda x: tmp_quality[x.name] if pd.isna(x.hit_quality) else x.hit_quality,
        axis=1,
    )
    skirmish["module_ammo"] = skirmish.apply(
        lambda x: tmp_module[x.name] if pd.isna(x.module_ammo) else x.module_ammo,
        axis=1,
    )
    skirmish["target_pilot"] = skirmish.apply(
        lambda x: tmp_pilots[x.name] if pd.isna(x.target_pilot) else x.target_pilot,
        axis=1,
    )

    return skirmish


def process_neut_incoming(skirmish):
    # neut_in
    mask = skirmish["linetext"].str.split("GJ energy neutralized").apply(len) > 1
    energy_neutralized = skirmish["linetext"].str.split("GJ energy neutralized")[mask]
    mask = skirmish["linetext"].str.split("GJ energy drained to").apply(len) > 1
    energy_drained = skirmish["linetext"].str.split("GJ energy drained to")[mask]

    energy_neutralized = energy_neutralized.apply(
        lambda x: [x[0].strip(" in "), x[1]] if "in" in x[0] else pd.NA
    )
    energy_neutralized.dropna(inplace=True)

    energy_drained = energy_drained.apply(
        lambda x: [x[0].strip(" in "), x[1]] if "in" in x[0] else pd.NA
    )

    skirmish["neut_in"] = energy_drained.apply(
        lambda x: abs(int(x[0])) if int(x[0]) < 0 else 0.1
    )
    tmp_neut_in_1 = skirmish["neut_in"].copy()
    skirmish["neut_in"] = energy_neutralized.apply(lambda x: int(x[0]))
    tmp_neut_in_2 = skirmish["neut_in"].copy()

    skirmish["neut_in"] = skirmish.apply(
        lambda x: tmp_neut_in_1[x.name] if pd.isna(x.neut_in) else x.neut_in, axis=1
    )
    skirmish["neut_in"] = skirmish.apply(
        lambda x: tmp_neut_in_2[x.name] if pd.isna(x.neut_in) else x.neut_in, axis=1
    )

    skirmish["linetext"] = skirmish["linetext"].str.replace(
        r"\sin\s\d*\sGJ\s\w*\sneutralized", "", regex=True
    )
    skirmish["linetext"] = skirmish["linetext"].str.replace(
        r"-\d*\sGJ\s\w*\sdrained\sto", "", regex=True
    )

    skirmish["shiptype"] = skirmish.apply(
        lambda x: x.linetext.split()[0] if x.neut_in > 0 else x.shiptype, axis=1
    )
    skirmish["linetext"] = skirmish.apply(
        lambda x: " ".join(x.linetext.split()[1:]) if x.neut_in > 0 else x.linetext,
        axis=1,
    )
    skirmish["module_ammo"] = skirmish.apply(
        lambda x: "".join(x.linetext.rsplit("- ", 1)[-1])
        if x.neut_in > 0
        else x.module_ammo,
        axis=1,
    )
    skirmish["linetext"] = skirmish.apply(
        lambda x: "" if x.neut_in > 0 else x.linetext, axis=1
    )
    skirmish["neut_in"] = skirmish["neut_in"].fillna(0).astype(int)

    return skirmish


def process_neut_outgoing(skirmish):
    # neut_out
    mask = skirmish["linetext"].str.split("GJ energy neutralized").apply(len) > 1
    energy_neutralized = skirmish["linetext"].str.split("GJ energy neutralized")[mask]
    mask = skirmish["linetext"].str.split("GJ energy drained from").apply(len) > 1
    energy_drained = skirmish["linetext"].str.split("GJ energy drained from")[mask]

    energy_neutralized = energy_neutralized.apply(
        lambda x: [x[0].strip(" out "), x[1]] if "out" in x[0] else pd.NA
    )
    energy_neutralized.dropna(inplace=True)

    energy_drained = energy_drained.apply(
        lambda x: [x[0].strip(" out "), x[1]] if "out" in x[0] else pd.NA
    )

    skirmish["neut_out"] = energy_drained.apply(
        lambda x: abs(int(x[0])) if int(x[0]) > 0 else 0.1
    )
    tmp_neut_out_1 = skirmish["neut_out"].copy()
    skirmish["neut_out"] = energy_neutralized.apply(lambda x: int(x[0]))
    tmp_neut_out_2 = skirmish["neut_out"].copy()

    skirmish["neut_out"] = skirmish.apply(
        lambda x: tmp_neut_out_1[x.name] if pd.isna(x.neut_out) else x.neut_out, axis=1
    )
    skirmish["neut_out"] = skirmish.apply(
        lambda x: tmp_neut_out_2[x.name] if pd.isna(x.neut_out) else x.neut_out, axis=1
    )

    skirmish["linetext"] = skirmish["linetext"].str.replace(
        r"\sout\s\d*\sGJ\s\w*\sneutralized", "", regex=True
    )
    skirmish["linetext"] = skirmish["linetext"].str.replace(
        r"\sout\s\+\d*\sGJ\s\w*\sdrained\sfrom", "", regex=True
    )

    skirmish["shiptype"] = skirmish.apply(
        lambda x: x.linetext.split()[0] if x.neut_out > 0 else x.shiptype, axis=1
    )
    skirmish["linetext"] = skirmish.apply(
        lambda x: " ".join(x.linetext.split()[1:]) if x.neut_out > 0 else x.linetext,
        axis=1,
    )
    skirmish["module_ammo"] = skirmish.apply(
        lambda x: "".join(x.linetext.rsplit("- ", 1)[-1])
        if x.neut_out > 0
        else x.module_ammo,
        axis=1,
    )
    skirmish["linetext"] = skirmish.apply(
        lambda x: "" if x.neut_out > 0 else x.linetext, axis=1
    )
    skirmish["neut_out"] = skirmish["neut_out"].fillna(0).astype(int)

    return skirmish


def process_remote_capacitor_in(skirmish):
    mask = (
        skirmish["linetext"].str.split("remote capacitor transmitted by").apply(len) > 1
    )
    remote_cap_incoming = skirmish["linetext"].str.split(
        "remote capacitor transmitted by"
    )[mask]

    skirmish["cap_incoming"] = remote_cap_incoming.apply(
        lambda x: int(x[0]) if int(x[0]) > 0 else 0.1
    )

    skirmish["linetext"] = skirmish["linetext"].str.replace(
        r"\d*\sremote\scapacitor\stransmitted\sby", "", regex=True
    )
    skirmish["shiptype"] = skirmish.apply(
        lambda x: x.linetext.split()[0] if x.cap_incoming > 0 else x.shiptype, axis=1
    )

    skirmish["linetext"] = skirmish.apply(
        lambda x: " ".join(x.linetext.split()[1:])
        if x.cap_incoming > 0
        else x.linetext,
        axis=1,
    )
    skirmish["module_ammo"] = skirmish.apply(
        lambda x: "".join(x.linetext.rsplit("- ", 1)[-1])
        if x.cap_incoming > 0
        else x.module_ammo,
        axis=1,
    )
    skirmish["linetext"] = skirmish.apply(
        lambda x: "" if x.cap_incoming > 0 else x.linetext, axis=1
    )
    skirmish["cap_incoming"] = skirmish["cap_incoming"].fillna(0).astype(int)

    return skirmish


def process_remote_capacitor_out(skirmish):
    mask = (
        skirmish["linetext"].str.split("remote capacitor transmitted to").apply(len) > 1
    )
    remote_cap_outgoing = skirmish["linetext"].str.split(
        "remote capacitor transmitted to"
    )[mask]

    skirmish["cap_outgoing"] = remote_cap_outgoing.apply(
        lambda x: int(x[0]) if int(x[0]) > 0 else 0.1
    )

    skirmish["linetext"] = skirmish["linetext"].str.replace(
        r"\d*\sremote\scapacitor\stransmitted\sto", "", regex=True
    )
    skirmish["shiptype"] = skirmish.apply(
        lambda x: x.linetext.split()[0] if x.cap_outgoing > 0 else x.shiptype, axis=1
    )

    skirmish["linetext"] = skirmish.apply(
        lambda x: " ".join(x.linetext.split()[1:])
        if x.cap_outgoing > 0
        else x.linetext,
        axis=1,
    )
    skirmish["module_ammo"] = skirmish.apply(
        lambda x: "".join(x.linetext.rsplit("- ", 1)[-1])
        if x.cap_outgoing > 0
        else x.module_ammo,
        axis=1,
    )
    skirmish["linetext"] = skirmish.apply(
        lambda x: "" if x.cap_outgoing > 0 else x.linetext, axis=1
    )
    skirmish["cap_outgoing"] = skirmish["cap_outgoing"].fillna(0).astype(int)

    return skirmish


def process_lines(skirmish):
    timed_lines = skirmish[
        skirmish.linetext.str.contains("^\[\s\d*.\d*.\d*\s\d*:\d*:\d*\s\]")
    ]

    skirmish["timestamp"] = (
        timed_lines["linetext"].str[:24].str.strip("[ ").str.strip(" ]")
    )
    skirmish["timestamp"] = pd.to_datetime(
        skirmish["timestamp"], format="%Y.%m.%d %H:%M:%S"
    )
    skirmish["linetext"] = timed_lines["linetext"].str[24:]
    skirmish.dropna(inplace=True)

    skirmish = skirmish[~skirmish.linetext.str.contains("(hint)")]
    skirmish = skirmish[~skirmish.linetext.str.contains("(question)")]
    skirmish = skirmish[~skirmish.linetext.str.contains("(notify)")]
    skirmish = skirmish[~skirmish.linetext.str.contains("(warning)")]
    skirmish = skirmish[~skirmish.linetext.str.contains("(info)")]
    skirmish = skirmish[~skirmish.linetext.str.contains("(bounty)")]
    skirmish = skirmish[~skirmish.linetext.str.contains("(None)")]
    skirmish = skirmish[~skirmish.linetext.str.contains("Warp scramble attempt")]
    skirmish = skirmish[~skirmish.linetext.str.contains("Warp disruption attempt")]

    skirmish["linetext"] = skirmish["linetext"].str[8:]

    # change neut strings slightly to represent incoming and outgoing colors
    skirmish["linetext"] = skirmish["linetext"].str.replace(
        r"<color=0xffe57f7f>", "in ", regex=True
    )
    skirmish["linetext"] = skirmish["linetext"].str.replace(
        r"<color=0xff7fffff>", "out ", regex=True
    )

    # remove HTML tags
    skirmish["linetext"] = skirmish["linetext"].str.replace(r"<[^<>]*>", "", regex=True)

    skirmish["module_ammo"] = ""
    skirmish["hit_quality"] = ""
    skirmish["target_pilot"] = pd.NA
    skirmish["shiptype"] = ""
    skirmish["neut_in"] = pd.NA
    skirmish["neut_out"] = pd.NA
    skirmish["cap_out"] = pd.NA
    skirmish["cap_in"] = pd.NA

    skirmish = process_misses(skirmish)

    skirmish = process_neut_incoming(skirmish)
    skirmish = process_neut_outgoing(skirmish)

    skirmish = process_remote_repairs_outgoing(skirmish)
    skirmish = process_remote_repairs_incoming(skirmish)

    skirmish = process_remote_shield_outgoing(skirmish)
    skirmish = process_remote_shield_incoming(skirmish)

    skirmish = process_remote_capacitor_out(skirmish)
    skirmish = process_remote_capacitor_in(skirmish)

    skirmish.to_csv("skirmish_linetext.csv", encoding="utf-8", index=False)
    skirmish = process_damage_incoming(skirmish)
    skirmish = process_damage_outgoing(skirmish)

    skirmish["module_ammo"] = skirmish["module_ammo"].str.replace(
        r"^\W*", "", regex=True
    )
    skirmish["module_ammo"] = skirmish["module_ammo"].str.replace(
        r"\s+$", "", regex=True
    )

    skirmish["target_pilot"] = skirmish["target_pilot"].fillna("").astype(str)
    skirmish["target_pilot"] = skirmish["target_pilot"].str.replace(
        r"^\W*", "", regex=True
    )
    skirmish["target_pilot"] = skirmish["target_pilot"].str.replace(
        r"\s+$", "", regex=True
    )

    skirmish["hit_quality"] = skirmish["hit_quality"].fillna("").astype(str)
    skirmish["hit_quality"] = skirmish["hit_quality"].str.replace(
        r"^\W*", "", regex=True
    )

    skirmish.drop(columns="linetext", inplace=True)
    skirmish.to_csv("test.csv")

    print(skirmish.head(10))


def new_skirmish():
    files = select_files()

    skirmish = pd.DataFrame()

    for file in files:
        skirmish = read_file(file, skirmish)

    process_lines(skirmish)


if __name__ == "__main__":
    # new_skirmish()

    logreader = AnalysingLogReader()
    logreader.read_files()

    logreader.process_frames()

    logreader.export_frames()
