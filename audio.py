#!/usr/bin/env python3
# =========================================================
# Unreal Engine Wwise Audio Extract Helper
# Author: Abyssrte
#
# Note:
# This script automates audio extraction from UE Wwise
# .wem and .bnk files using existing open-source tools.
#
# Credits:
# - ww2ogg by hcs64
# - vgmstream project
# - FFmpeg
#
# This is a helper script, not a re-implementation
# of the original tools.
# =========================================================

# ================= AUTO DEPENDENCY CHECK =================
import sys
import os
import subprocess

# ANSI COLORS (NO COLORAMA)
RED     = "\033[91m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
RESET   = "\033[0m"
BOLD    = "\033[1m"


def clear_screen():
    os.system("clear" if os.name != "nt" else "cls")


def _silent_ok(cmd):
    return subprocess.run(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    ).returncode == 0


def ensure_python_pkg(pkg):
    try:
        __import__(pkg)
        return True          # ✅ silent if already installed
    except ImportError:
        print(f"{YELLOW}[+]{RESET} Installing Python package: {BOLD}{pkg}{RESET}")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", pkg]
        )
        try:
            __import__(pkg)
            print(f"{GREEN}[✓]{RESET} {pkg} installed")
            return True
        except ImportError:
            return False


def ensure_system_pkg(cmd, pkg):
    if _silent_ok(["which", cmd]):
        return True          # ✅ silent if already installed

    print(f"{YELLOW}[+]{RESET} Installing system package: {BOLD}{pkg}{RESET}")
    subprocess.run(
        ["pkg", "install", "-y", pkg]
    )

    return _silent_ok(["which", cmd])


def check_dependencies():
    failed = False

    if not ensure_python_pkg("colorama"):
        print(f"{RED}[✗]{RESET} Failed to install colorama")
        failed = True

    if not ensure_system_pkg("vgmstream-cli", "vgmstream"):
        print(f"{RED}[✗]{RESET} Failed to install vgmstream")
        failed = True

    if not ensure_system_pkg("ffmpeg", "ffmpeg"):
        print(f"{RED}[✗]{RESET} Failed to install ffmpeg")
        failed = True

    if failed:
        print(f"\n{RED}{BOLD}[!] Dependency installation failed. Fix manually.{RESET}")
        sys.exit(1)


# ✅ RUN ONCE, SILENTLY
check_dependencies()
clear_screen()
# =========================================================

import sys
import os
import subprocess
import random
from colorama import Fore, Style, init

init(autoreset=True)

# ---------- CONFIG ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TOOLS_DIR = os.path.join(BASE_DIR, "tools")

fuck = os.path.join(TOOLS_DIR, "audio")
CODEBOOK = os.path.join(TOOLS_DIR, "packed_codebooks_aoTuV_603.bin")

OUTPUT_DIR = os.path.join(BASE_DIR, "UE_Audio")

BANNER_COLOR = "brightred"
# ----------------------------

BRIGHT_COLORS = {
    "brightred": Fore.LIGHTRED_EX,
    "brightgreen": Fore.LIGHTGREEN_EX,
    "brightyellow": Fore.LIGHTYELLOW_EX,
    "brightblue": Fore.LIGHTBLUE_EX,
    "brightmagenta": Fore.LIGHTMAGENTA_EX,
    "brightcyan": Fore.LIGHTCYAN_EX,
    "brightwhite": Fore.LIGHTWHITE_EX,
}

def print_banner():
    print()
    banner_text = [
        " █    ██ ▓█████     ▄▄▄       █    ██ ▓█████▄  ██▓ ▒█████  ",
        " ██  ▓██▒▓█   ▀    ▒████▄     ██  ▓██▒▒██▀ ██▌▓██▒▒██▒  ██▒",
        "▓██  ▒██░▒███      ▒██  ▀█▄  ▓██  ▒██░░██   █▌▒██▒▒██░  ██▒",
        "▓▓█  ░██░▒▓█  ▄    ░██▄▄▄▄██ ▓▓█  ░██░░▓█▄   ▌░██░▒██   ██░",
        "▒▒█████▓ ░▒████▒    ▓█   ▓██▒▒▒█████▓ ░▒████▓ ░██░░ ████▓▒░",
        "░▒▓▒ ▒ ▒ ░░ ▒░ ░    ▒▒   ▓▒█░░▒▓▒ ▒ ▒  ▒▒▓  ▒ ░▓  ░ ▒░▒░▒░ ",
        "░░▒░ ░ ░  ░ ░  ░     ▒   ▒▒ ░░░▒░ ░ ░  ░ ▒  ▒  ▒ ░  ░ ▒ ▒░ ",
        " ░░░ ░ ░    ░        ░   ▒    ░░░ ░ ░  ░ ░  ░  ▒ ░░ ░ ░ ▒  ",
        "   ░        ░  ░         ░  ░   ░        ░     ░      ░ ░  ",
    ]

    color = BRIGHT_COLORS.get(BANNER_COLOR, Fore.LIGHTRED_EX)
    for line in banner_text:
        print(color + Style.BRIGHT + line)
    print()
    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "[Tool By :- Abyssrte]")

def usage():
    print(Fore.LIGHTRED_EX + Style.BRIGHT + "[Unreal Engine Audio Extractor]")
    print(Fore.LIGHTCYAN_EX + Style.BRIGHT + "USAGE:")
    print("  python audio.py file.wem")
    print("  python audio.py -bnk file.bnk\n")
    print(Fore.LIGHTCYAN_EX + "NOTES:")
    print(Fore.LIGHTYELLOW_EX +Style.BRIGHT + "Work Only .bnk file and .wem")
    print(Fore.LIGHTYELLOW_EX +Style.BRIGHT + "Soon Replace .wem in .bnk file")
    sys.exit(0)

def run_cmd(cmd, error_hint):
    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    if result.returncode != 0:
        print(Fore.LIGHTRED_EX + Style.BRIGHT + "ERROR:")
        print(result.stderr.strip())
        print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + "HOW TO FIX:")
        print(error_hint)
        sys.exit(1)
    return result.stdout

def extract_bnk(bnk_file):
    if not os.path.isfile(bnk_file):
        print(Fore.LIGHTRED_EX + "ERROR: .bnk file not found")
        sys.exit(1)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    meta = run_cmd(
        ["vgmstream-cli", "-m", bnk_file],
        "vgmstream-cli not found. Install with: pkg install vgmstream"
    )

    stream_count = None
    for line in meta.splitlines():
        if "stream count:" in line:
            stream_count = int(line.split(":")[1].strip())
            break

    if stream_count is None:
        print(Fore.LIGHTRED_EX + "ERROR: Unable to detect stream count")
        sys.exit(1)

    base = os.path.splitext(os.path.basename(bnk_file))[0]

    for i in range(stream_count):
        out_wav = os.path.join(OUTPUT_DIR, f"{base}_{i}.wav")
        run_cmd(
            ["vgmstream-cli", "-s", str(i), "-o", out_wav, bnk_file],
            "Failed to extract audio stream"
        )

    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "SUCCESS:")
    print(Fore.LIGHTGREEN_EX + f"Extracted {stream_count} audio files to {OUTPUT_DIR}/")

def extract_wem(wem_file):
    if not os.path.isfile(wem_file):
        print(Fore.LIGHTRED_EX + "ERROR: .wem file not found")
        sys.exit(1)

    if not os.path.isfile(fuck):
        print(Fore.LIGHTRED_EX + "ERROR: audio tool not found")
        sys.exit(1)

    if not os.path.isfile(CODEBOOK):
        print(Fore.LIGHTRED_EX + "ERROR: packed_codebooks file missing")
        sys.exit(1)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    base = os.path.splitext(os.path.basename(wem_file))[0]
    ogg_file = base + ".ogg"
    wav_file = os.path.join(OUTPUT_DIR, base + ".wav")

    run_cmd(
        [fuck, wem_file, "--pcb", CODEBOOK],
        "WEM file may be encrypted or unsupported"
    )

    run_cmd(
        ["ffmpeg", "-y", "-i", ogg_file, wav_file],
        "FFmpeg not installed. Install with: pkg install ffmpeg"
    )

    # ✅ DELETE LOGIC — ONLY FOR OGG
    if os.path.isfile(ogg_file):
        try:
            os.remove(ogg_file)
        except:
            pass

    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "SUCCESS:")
    print(Fore.LIGHTGREEN_EX + f"Audio extracted -> {wav_file}")

def main():
    print_banner()

    if len(sys.argv) == 1:
        usage()

    if sys.argv[1] == "-bnk":
        if len(sys.argv) != 3:
            usage()
        extract_bnk(sys.argv[2])
        return

    extract_wem(sys.argv[1])

if __name__ == "__main__":
    main()