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

# Usage: python player_apps_counter.py /path/to/scripts/directory

import os
import sys


def identify_players(directory):
    # Initialize category counters
    counts = {
        "total": 0,
        "lightning": 0,
        "lightning_animation": 0,
        "lightning_shaka": 0,
        "lightning_fps": 0,
        "lightning_dash": 0,
        "lightning_hls": 0,
        "lightning_aamp": 0,
        "html": 0,
        "html_dash": 0,
        "html_hls": 0,
        "html_shaka": 0,
        "html_successive": 0,
        "html_fps": 0,
        "html_aamp": 0,
        "corrupted": 0,
        "delay": 0,
    }

    # Process each script file in the directory
    for filename in sorted(os.listdir(directory)):
        file_path = os.path.join(directory, filename)

        # Skip if not a python test script file
        if not os.path.isfile(file_path) or not filename.endswith(".py"):
            continue

        name_lower = filename.lower()
        counts["total"] += 1

        # A script is counted as either HTML or Lightning, never both
        if "html" in name_lower:
            counts["html"] += 1
            if "dash" in name_lower:
                counts["html_dash"] += 1
            if "hls" in name_lower:
                counts["html_hls"] += 1
            if "shaka" in name_lower:
                counts["html_shaka"] += 1
            if "successive" in name_lower:
                counts["html_successive"] += 1
            if "fps" in name_lower:
                counts["html_fps"] += 1
            if "aamp" in name_lower:
                counts["html_aamp"] += 1
        else:
            counts["lightning"] += 1
            if "animation" in name_lower:
                counts["lightning_animation"] += 1
            if "shaka" in name_lower:
                counts["lightning_shaka"] += 1
            if "fps" in name_lower and "animation" not in name_lower:
                counts["lightning_fps"] += 1
            if "dash" in name_lower:
                counts["lightning_dash"] += 1
            if "hls" in name_lower or "mpeg_ts" in name_lower:
                counts["lightning_hls"] += 1
            if "aamp" in name_lower:
                counts["lightning_aamp"] += 1

        # These tags are counted independently of the HTML/Lightning classification
        if "corrupted" in name_lower:
            counts["corrupted"] += 1
        if "delay" in name_lower:
            counts["delay"] += 1

    # ----------------- Output Results -----------------
    print(f"\nTotal Scripts: {counts['total']}\n")

    print(f"Lightning Player Scripts: {counts['lightning']}\n")
    print(f"Lightning Animation Scripts: {counts['lightning_animation']}")
    print(f"Lightning SHAKA Scripts: {counts['lightning_shaka']}")
    print(f"Lightning FPS Scripts: {counts['lightning_fps']}")
    print(f"Lightning DASH Scripts: {counts['lightning_dash']}")
    print(f"Lightning HLS Scripts: {counts['lightning_hls']}")
    print(f"Lightning AAMP Scripts: {counts['lightning_aamp']}\n")

    print(f"HTML Player Scripts: {counts['html']}\n")
    print(f"HTML DASH Scripts: {counts['html_dash']}")
    print(f"HTML HLS Scripts: {counts['html_hls']}")
    print(f"HTML SHAKA Scripts: {counts['html_shaka']}")
    print(f"HTML Successive Scripts: {counts['html_successive']}")
    print(f"HTML FPS Scripts: {counts['html_fps']}")
    print(f"HTML AAMP Scripts: {counts['html_aamp']}\n")

    print(f"Corrupted Scripts: {counts['corrupted']}")
    print(f"Delay Scripts: {counts['delay']}\n")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: Directory path missing.\nUsage: python player_apps_counter.py /path/to/your/directory")
        sys.exit(1)
    target_directory = sys.argv[1]
    if not os.path.isdir(target_directory):
        print(f" Error: '{target_directory}' is not a valid directory.")
        sys.exit(1)

    identify_players(target_directory)

