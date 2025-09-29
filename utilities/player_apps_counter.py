##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2025 RDK Management
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##########################################################################

import os
import sys

# Define keyword groups for different player types
AAMP_KEYS = ["aamp"]
SHAKA_KEYS = ["shaka"]
HTML_KEYS = ["html"]
DASH_KEYS = ["dash"]
HLS_KEYS = ["hls"]
SDK_KEYS = ["mp4", "hdr", "hevc_mkv", "mkv", "4k_vp9", "4k_av1"]
SDK_EXCLUSIVE = ["4k_av1", "4k_vp9", "hevc_mkv"]  # Keywords exclusive to SDK, used to exclude DASH

# Rule 6 & 9: Dash extra codecs
DASH_EXTRA_KEYS = [
    "av1", "ec3", "ac3", "vp9", "audio_only", "ogg", "opus",
    "hevc", "aac", "h263", "mpeg", "vp8"]

# Rule 10: HLS extra keywords
HLS_EXTRA_KEYS = ["mpeg_ts"]


def identify_players(directory):
    # Initialize player apps count dictionary
    player_counts = {
        "aamp": 0,
        "shaka": 0,
        "html": 0,
        "sdk": 0,
        "dash": 0,
        "hls": 0
    }

    # Process each file in the directory
    for filename in sorted(os.listdir(directory)):
        file_path = os.path.join(directory, filename)

        # Skip if not a file
        if not os.path.isfile(file_path):
            continue

        name_lower = filename.lower()
        matched_players = set()

        # ---------------------------- Priority Rules ------------------------------
        # Rule 13: If filename contains AAMP keyword, assign only AAMP player
        if any(key in name_lower for key in AAMP_KEYS):
            matched_players = {"aamp"}
        # Rule 12: If filename contains Shaka keyword, assign only Shaka player
        elif any(key in name_lower for key in SHAKA_KEYS):
            matched_players = {"shaka"}
        # Rule 8: If filename contains HTML keyword, assign only HTML player
        elif any(key in name_lower for key in HTML_KEYS):
            matched_players = {"html"}
        # Rule 11: If filename contains 'fps' but not 'animation', assign SDK player
        elif "fps" in name_lower and "animation" not in name_lower:
            matched_players = {"sdk"}
        # --------------------------- Normal Matching ---------------------------
        else:
            if any(key in name_lower for key in SDK_KEYS):
                matched_players.add("sdk")
            if not any(ex in name_lower for ex in SDK_EXCLUSIVE):
                if any(key in name_lower for key in DASH_KEYS + DASH_EXTRA_KEYS):
                    matched_players.add("dash")
            if any(key in name_lower for key in HLS_KEYS + HLS_EXTRA_KEYS):
                matched_players.add("hls")

        # Update player counts
        for player in matched_players:
            player_counts[player] += 1

    # ----------------- Output Results -----------------
    print("\n Player Apps Count Summary")
    print(f" Scanned Directory : {directory}\n")
    total_count = sum(player_counts.values())
    # Print count for each player type
    for player, count in player_counts.items():
        print(f" {player.upper():<5} : {count}")
    print(f"\n Total Matched Files : {total_count}\n")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: Directory path missing.\nUsage: python player_apps_counter.py /path/to/your/directory")
        sys.exit(1)
    target_directory = sys.argv[1]
    if not os.path.isdir(target_directory):
        print(f" Error: '{target_directory}' is not a valid directory.")
        sys.exit(1)

    identify_players(target_directory)
