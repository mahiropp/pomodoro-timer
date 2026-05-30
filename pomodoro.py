import time
import sys
import os
import json
from datetime import datetime

# Windows対応のカラーコード有効化
if sys.platform == "win32":
    os.system("")

# カラーコード
RED    = "\033[91m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

STATS_FILE = os.path.join(os.path.dirname(__file__), "stats.json")

WORK_MINUTES  = 25
SHORT_BREAK   = 5
LONG_BREAK    = 15
SESSIONS_UNTIL_LONG = 4


def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r") as f:
            return json.load(f)
    return {"total_sessions": 0, "total_minutes": 0, "history": []}


def save_stats(stats):
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)


def clear_line():
    sys.stdout.write("\r\033[K")
    sys.stdout.flush()


def format_time(seconds):
    m, s = divmod(seconds, 60)
    return f"{m:02d}:{s:02d}"


def countdown(total_seconds, label, color):
    print()
    if total_seconds <= 0:
        return
    for remaining in range(total_seconds, -1, -1):
        bar_len = 30
        filled = int(bar_len * (total_seconds - remaining) / total_seconds)
        bar = "█" * filled + "░" * (bar_len - filled)
        sys.stdout.write(
            f"\r  {color}{BOLD}{label}{RESET}  "
            f"[{color}{bar}{RESET}]  "
            f"{color}{BOLD}{format_time(remaining)}{RESET}"
        )
        sys.stdout.flush()
        if remaining > 0:
            time.sleep(1)
    print()


def beep(times=3):
    for _ in range(times):
        print("\a", end="", flush=True)
        time.sleep(0.3)


def print_header():
    os.system("cls" if sys.platform == "win32" else "clear")
    print(f"\n{RED}{BOLD}  🍅 ポモドーロタイマー{RESET}\n")
    print(f"  {CYAN}作業:{RESET} {WORK_MINUTES}分  |  "
          f"{GREEN}短い休憩:{RESET} {SHORT_BREAK}分  |  "
          f"{YELLOW}長い休憩:{RESET} {LONG_BREAK}分")
    print(f"  {'-'*45}")


def show_stats(stats):
    print(f"\n  {BOLD}📊 本日の記録{RESET}")
    print(f"  完了セッション: {CYAN}{BOLD}{stats['total_sessions']}{RESET} ポモドーロ")
    print(f"  集中時間合計:   {CYAN}{BOLD}{stats['total_minutes']}{RESET} 分")
    if stats["history"]:
        print(f"  最終セッション: {stats['history'][-1]}")
    print()


def main():
    stats = load_stats()
    session_count = 0

    print_header()
    show_stats(stats)
    print(f"  {BOLD}Ctrl+C で終了{RESET}\n")
    input(f"  {GREEN}Enterキーを押してスタート！{RESET} ")

    try:
        while True:
            session_count += 1
            stats["total_sessions"] += 1

            print_header()
            show_stats(stats)
            print(f"  {RED}{BOLD}▶ セッション #{session_count} 開始！{RESET}\n")

            countdown(WORK_MINUTES * 60, f"作業中 #{session_count}", RED)
            beep(2)

            stats["total_minutes"] += WORK_MINUTES
            stats["history"].append(
                datetime.now().strftime("%Y-%m-%d %H:%M") + f" (セッション#{session_count})"
            )
            save_stats(stats)

            # 長い休憩 or 短い休憩
            if session_count % SESSIONS_UNTIL_LONG == 0:
                break_min = LONG_BREAK
                break_label = f"🌟 長い休憩 ({LONG_BREAK}分)"
                color = YELLOW
            else:
                break_min = SHORT_BREAK
                break_label = f"☕ 短い休憩 ({SHORT_BREAK}分)"
                color = GREEN

            print(f"\n  {color}{BOLD}お疲れ様！{break_label}をどうぞ{RESET}")
            input(f"  {color}Enterで休憩スタート...{RESET} ")

            print_header()
            show_stats(stats)
            countdown(break_min * 60, break_label, color)
            beep(3)

            print(f"\n  {CYAN}{BOLD}休憩終了！次のセッションへ{RESET}")
            input(f"  {GREEN}Enterで続ける...{RESET} ")

    except KeyboardInterrupt:
        print(f"\n\n  {YELLOW}{BOLD}お疲れ様でした！{RESET}")
        show_stats(stats)
        print(f"  また頑張りましょう 🍅\n")


if __name__ == "__main__":
    main()
