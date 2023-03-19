import pandas as pd

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

        self.burst_jammed = pd.DataFrame()

    def select_files(self):
        root = tk.Tk()
        return root.tk.splitlist(
            filedialog.askopenfilenames(parent=root, title="Choose a file")
        )

    def read_files(self):
        for file_name in self.files:
            self.read_file(file_name)

        self.populate_frames()

        self.main_frame.to_csv("./all_csv/main_frame.csv")

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

        self.burst_jammed = self.main_frame[
            self.main_frame.linetext.str.contains(
                logrex[self.language]["locklost"], regex=True
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

        self.burst_jammed.to_csv(path + "burst_jammed.csv")

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
            self.damage_in["amount"] = self.damage_in.apply(
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
                    "amount",
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
            self.damage_out["amount"] = self.damage_out.apply(
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
                    "amount",
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

            self.capNeutralized_in["amount"] = self.capNeutralized_in.apply(
                lambda x: x.linetext.split(" ")[0], axis=1
            ).astype(int)

            self.capNeutralized_in["linetext"] = self.capNeutralized_in[
                "linetext"
            ].str.replace(r"\d*\sGJ\senergy\sneutralized\s", "", regex=True)

            self.capNeutralized_in["module_or_ammo"] = self.capNeutralized_in.apply(
                lambda x: x.linetext.rsplit(" - ", 1)[-1], axis=1
            )

            self.capNeutralized_in["linetext"] = self.capNeutralized_in.apply(
                lambda x: x.linetext.rsplit(" - ", 1)[0], axis=1
            )

            self.capNeutralized_in.rename(
                {"linetext": "brackets"}, axis=1, inplace=True
            )
            self.capNeutralized_in = self.capNeutralized_in[
                ["timestamp", "pilot", "brackets", "module_or_ammo", "amount"]
            ]

        if not self.capNeutralized_out.empty:
            self.capNeutralized_out["linetext"] = self.capNeutralized_out[
                "linetext"
            ].str.replace(r"<[^<>]*>", "", regex=True)
            self.capNeutralized_out["linetext"] = self.capNeutralized_out[
                "linetext"
            ].str.replace(r"\s*\(combat\)\s", "", regex=True)

            self.capNeutralized_out["amount"] = self.capNeutralized_out.apply(
                lambda x: x.linetext.split(" ")[0], axis=1
            ).astype(int)

            self.capNeutralized_out["linetext"] = self.capNeutralized_out[
                "linetext"
            ].str.replace(r"\d*\sGJ\senergy\sneutralized\s", "", regex=True)

            self.capNeutralized_out["module_or_ammo"] = self.capNeutralized_out.apply(
                lambda x: x.linetext.rsplit(" - ", 1)[-1], axis=1
            )

            self.capNeutralized_out["linetext"] = self.capNeutralized_out.apply(
                lambda x: x.linetext.rsplit(" - ", 1)[0], axis=1
            )

            self.capNeutralized_out.rename(
                {"linetext": "brackets"}, axis=1, inplace=True
            )
            self.capNeutralized_out = self.capNeutralized_out[
                ["timestamp", "pilot", "brackets", "module_or_ammo", "amount"]
            ]

    def process_nos(self):
        if not self.nosRecieved.empty:
            self.nosRecieved["linetext"] = self.nosRecieved["linetext"].str.replace(
                r"<[^<>]*>", "", regex=True
            )
            self.nosRecieved["linetext"] = self.nosRecieved["linetext"].str.replace(
                r"\s*\(combat\)\s", "", regex=True
            )

            self.nosRecieved["amount"] = self.nosRecieved.apply(
                lambda x: x.linetext.split(" ")[0], axis=1
            ).astype(int)

            self.nosRecieved["linetext"] = self.nosRecieved["linetext"].str.replace(
                r"\d*\sGJ\senergy\sdrained\sfrom\s", "", regex=True
            )

            self.nosRecieved["module_or_ammo"] = self.nosRecieved.apply(
                lambda x: x.linetext.rsplit(" - ", 1)[-1], axis=1
            )

            self.nosRecieved["linetext"] = self.nosRecieved.apply(
                lambda x: x.linetext.rsplit(" - ", 1)[0], axis=1
            )

            self.nosRecieved.rename({"linetext": "brackets"}, axis=1, inplace=True)
            self.nosRecieved = self.nosRecieved[
                ["timestamp", "pilot", "brackets", "module_or_ammo", "amount"]
            ]

        if not self.nosTaken.empty:
            self.nosTaken["linetext"] = self.nosTaken["linetext"].str.replace(
                r"<[^<>]*>", "", regex=True
            )
            self.nosTaken["linetext"] = self.nosTaken["linetext"].str.replace(
                r"\s*\(combat\)\s", "", regex=True
            )

            self.nosTaken["amount"] = self.nosTaken.apply(
                lambda x: x.linetext.split(" ")[0].strip("-"), axis=1
            ).astype(int)

            self.nosTaken["linetext"] = self.nosTaken["linetext"].str.replace(
                r"-\d*\sGJ\senergy\sdrained\sto\s", "", regex=True
            )

            self.nosTaken["module_or_ammo"] = self.nosTaken.apply(
                lambda x: x.linetext.rsplit(" - ", 1)[-1], axis=1
            )

            self.nosTaken["linetext"] = self.nosTaken.apply(
                lambda x: x.linetext.rsplit(" - ", 1)[0], axis=1
            )

            self.nosTaken.rename({"linetext": "brackets"}, axis=1, inplace=True)
            self.nosTaken = self.nosTaken[
                ["timestamp", "pilot", "brackets", "module_or_ammo", "amount"]
            ]

    def process_misses(self):
        pass

    def process_mining(self):
        pass

    def print_stats(self):
        if not self.damage_out.empty:
            print("Sum of damage done: " + str(self.damage_out["amount"].sum()))
        if not self.damage_in.empty:
            print("Sum of damage taken: " + str(self.damage_in["amount"].sum()))
        if not self.armorRepaired_out.empty:
            print(
                "Sum of remote armor repaired: "
                + str(self.armorRepaired_out["amount"].sum())
            )
        if not self.armorRepaired_in.empty:
            print(
                "Sum of remote armor recieved: "
                + str(self.armorRepaired_in["amount"].sum())
            )
        if not self.shieldBoosted_out.empty:
            print(
                "Sum of remote shield boosted: "
                + str(self.shieldBoosted_out["amount"].sum())
            )
        if not self.shieldBoosted_in.empty:
            print(
                "Sum of remote shield recieved: "
                + str(self.shieldBoosted_in["amount"].sum())
            )
        if not self.hullRepaired_out.empty:
            print(
                "Sum of remote hull repaired: "
                + str(self.hullRepaired_out["amount"].sum())
            )
        if not self.hullRepaired_in.empty:
            print(
                "Sum of remote hull recieved: "
                + str(self.hullRepaired_in["amount"].sum())
            )
        if not self.capTransfer_out.empty:
            print(
                "Sum of remote cap transfer sent: "
                + str(self.capTransfer_out["amount"].sum())
                + " GJ"
            )
        if not self.capTransfer_in.empty:
            print(
                "Sum of remote cap transfer recieved: "
                + str(self.capTransfer_in["amount"].sum())
                + " GJ"
            )
        if not self.capNeutralized_out.empty:
            print(
                "Sum of cap neutralization out: "
                + str(self.capNeutralized_out["amount"].sum())
                + " GJ"
            )
        if not self.capNeutralized_in.empty:
            print(
                "Sum of cap neutralization in: "
                + str(
                    self.capNeutralized_in["amount"].sum()
                    + self.nosTaken["amount"].sum()
                )
                + " GJ"
            )
        if not self.nosRecieved.empty:
            print(
                "Sum of nos recieved: " + str(self.nosRecieved["amount"].sum()) + " GJ"
            )

        if not self.burst_jammed.empty:
            print(
                "Amount of times burst jammed: "
                + str(len(logreader.burst_jammed.index))
            )
        # self.misses_out = pd.DataFrame()
        # self.misses_in = pd.DataFrame()

        # self.mined = pd.DataFrame()

        # self.burst_jammed = pd.DataFrame()


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


if __name__ == "__main__":
    # new_skirmish()

    logreader = AnalysingLogReader()
    logreader.read_files()

    logreader.process_frames()

    logreader.print_stats()

    # print("Sum of cap transfered: " + str(logreader.capTransfer_out["amount"].sum()) + " GJ")
    # print("Sum of cap recieved: " + str(logreader.capTransfer_in["amount"].sum()) + " GJ")
    # print("Sum of neut in: " + str(logreader.capNeutralized_in["amount"].sum()) + " GJ")
    # print("Sum of neut out: " + str(logreader.capNeutralized_out["amount"].sum()) + " GJ")
    # print("Amount of times burst jammed: " + str(len(logreader.burst_jammed.index)))

    logreader.export_frames()
