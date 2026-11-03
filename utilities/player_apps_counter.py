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
import re
import sys

# Maps a player engine to its reporting bucket.
PLAYER_BUCKET = {
    "dashjs": "dash",
    "hlsjs": "hls",
    "shaka": "shaka",
    "aamp": "aamp",
    "sdk": "sdk",
}

# Default player for each codec, mirroring the codec_*
CODEC_PLAYERS = {
    "codec_dash_h264": "dashjs",
    "codec_hls_h264": "hlsjs",
    "codec_dash_hevc": "dashjs",
    "codec_hls_hevc": "hlsjs",
    "codec_dash_aac": "dashjs",
    "codec_hls_aac": "hlsjs",
    "codec_mpeg_ts": "hlsjs",
    "codec_ac3": "dashjs",
    "codec_ec3": "dashjs",
    "codec_vp9": "dashjs",
    "codec_opus": "dashjs",
    "codec_av1": "dashjs",
    "codec_h263": "sdk",
    "codec_vp8": "sdk",
    "codec_mp4": "sdk",
    "codec_ogg": "sdk",
    "codec_webm": "sdk",
    "codec_mpeg": "sdk",
    "codec_audio_aac": "dashjs",
    "codec_audio_mp3": "sdk",
    "codec_audio_dts": "sdk",
    "codec_audio_m4a": "sdk",
    "codec_audio_wav_pcm": "sdk",
    "codec_mkv": "sdk",
    "codec_4k_av1": "sdk",
}

CODEC_REF_RE = re.compile(r"MediaValidationVariables\.(codec_[A-Za-z0-9_]+)")


def identify_players(directory):
    counts = {
        "total": 0,
        "lightning": 0,
        "lightning_animation": 0,
        "lightning_shaka": 0,
        "lightning_fps": 0,
        "lightning_dash": 0,
        "lightning_hls": 0,
        "lightning_sdk": 0,
        "lightning_aamp": 0,
        "html": 0,
        "html_dash": 0,
        "html_hls": 0,
        "html_shaka": 0,
        "html_successive": 0,
        "html_fps": 0,
        "html_aamp": 0,
        "eme": 0,
        "mse": 0,
        "corrupted": 0,
        "delay": 0,
    }

    for filename in sorted(os.listdir(directory)):
        file_path = os.path.join(directory, filename)

        if not os.path.isfile(file_path) or not filename.endswith(".py"):
            continue

        name_lower = filename.lower()
        counts["total"] += 1

        # A script is counted as either HTML or Lightning, never both.
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
            # Determine the player from the codec_* variables the script
            # actually uses, rather than relying on the filename.
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as handle:
                    content = handle.read()
            except OSError:
                content = ""

            referenced_codecs = set(CODEC_REF_RE.findall(content))
            engines = {CODEC_PLAYERS[codec] for codec in referenced_codecs if codec in CODEC_PLAYERS}
            buckets = {PLAYER_BUCKET[engine] for engine in engines if engine in PLAYER_BUCKET}

            is_animation = "animation" in name_lower
            is_shaka = "shaka" in name_lower
            is_aamp = "aamp" in name_lower or "uve" in name_lower
            name_dash = "dash" in name_lower
            name_hls = "hls" in name_lower or "mpeg_ts" in name_lower

            # Prefer the codec-resolved player; use filename tokens for scripts
            # that pin the player themselves (SHAKA, AAMP, DASH SegmentBase).
            has_dash = "dash" in buckets or name_dash
            has_hls = "hls" in buckets or name_hls
            has_sdk = "sdk" in buckets
            has_shaka = "shaka" in buckets or is_shaka
            has_aamp = "aamp" in buckets or is_aamp

            # Conformance scripts have no player signal; report them separately
            # instead of inflating the Lightning total.
            identified = (
                is_animation
                or is_shaka
                or is_aamp
                or bool(referenced_codecs)
                or has_dash
                or has_hls
                or has_sdk
            )

            if not identified:
                if "eme" in name_lower:
                    counts["eme"] += 1
                elif "mse" in name_lower:
                    counts["mse"] += 1
            else:
                counts["lightning"] += 1
                if is_animation:
                    counts["lightning_animation"] += 1
                if has_shaka:
                    counts["lightning_shaka"] += 1
                if "fps" in name_lower and not is_animation:
                    counts["lightning_fps"] += 1
                if has_dash:
                    counts["lightning_dash"] += 1
                if has_hls:
                    counts["lightning_hls"] += 1
                if has_sdk:
                    counts["lightning_sdk"] += 1
                if has_aamp:
                    counts["lightning_aamp"] += 1

        # These tags are counted independently of the HTML/Lightning split.
        if "corrupted" in name_lower:
            counts["corrupted"] += 1
        if "delay" in name_lower:
            counts["delay"] += 1

    print(f"\nTotal Scripts: {counts['total']}\n")

    print(f"Lightning Player Scripts: {counts['lightning']}\n")
    print(f"Lightning Animation Scripts: {counts['lightning_animation']}")
    print(f"Lightning SHAKA Scripts: {counts['lightning_shaka']}")
    print(f"Lightning FPS Scripts: {counts['lightning_fps']}")
    print(f"Lightning DASH Scripts: {counts['lightning_dash']}")
    print(f"Lightning HLS Scripts: {counts['lightning_hls']}")
    print(f"Lightning SDK Scripts: {counts['lightning_sdk']}")
    print(f"Lightning AAMP Scripts: {counts['lightning_aamp']}\n")

    print(f"HTML Player Scripts: {counts['html']}\n")
    print(f"HTML DASH Scripts: {counts['html_dash']}")
    print(f"HTML HLS Scripts: {counts['html_hls']}")
    print(f"HTML SHAKA Scripts: {counts['html_shaka']}")
    print(f"HTML Successive Scripts: {counts['html_successive']}")
    print(f"HTML FPS Scripts: {counts['html_fps']}")
    print(f"HTML AAMP Scripts: {counts['html_aamp']}\n")

    print(f"EME Scripts: {counts['eme']}")
    print(f"MSE Scripts: {counts['mse']}\n")

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

