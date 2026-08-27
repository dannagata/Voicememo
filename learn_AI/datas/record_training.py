import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from pathlib import Path
from datetime import datetime
import sys
import termios
import tty
import select


# =========================================================
# 設定
# =========================================================

FS = 16000
CHANNELS = 1

# 文章が入っているフォルダ
LABEL_DIR = Path("labels")

# 録音した音声の保存先
DATA_DIR = Path("training")

# 進捗を保存するファイル
PROGRESS_FILE = Path("progress.txt")


# =========================================================
# キー入力
# =========================================================

def key_pressed():
    """
    キーが押されたか確認する
    """
    return select.select([sys.stdin], [], [], 0)[0]


def get_key():
    """
    押されたキーを取得する
    """
    if key_pressed():
        return sys.stdin.read(1)
    return None


# =========================================================
# 進捗読み込み
# =========================================================

def load_progress():

    if not PROGRESS_FILE.exists():
        return 0

    try:
        return int(
            PROGRESS_FILE.read_text(encoding="utf-8").strip()
        )
    except:
        return 0


# =========================================================
# 進捗保存
# =========================================================

def save_progress(index):

    PROGRESS_FILE.write_text(
        str(index),
        encoding="utf-8"
    )


# =========================================================
# 録音
# =========================================================

def record_audio():

    recorded_data = []
    interrupted = False

    def callback(indata, frames, time, status):

        if status:
            print(f"\n[録音警告] {status}")

        recorded_data.append(indata.copy())

    print()
    print("録音中...")
    print()
    print("  Enter : 録音終了 → 保存して次の文章へ")
    print("  Space : 中断してプログラム終了")
    print()

    with sd.InputStream(
        samplerate=FS,
        channels=CHANNELS,
        dtype="int16",
        callback=callback
    ):

        while True:

            key = get_key()

            if key == "\n" or key == "\r":

                print("\n録音終了")
                break

            elif key == " ":

                print("\nSpaceキーが押されました。")
                print("録音を破棄してプログラムを終了します。")

                interrupted = True
                break

    if interrupted:
        return None

    if not recorded_data:
        return None

    audio = np.concatenate(
        recorded_data,
        axis=0
    )

    return audio


# =========================================================
# メイン
# =========================================================

def main():

    # labelフォルダ確認
    if not LABEL_DIR.exists():

        print(f"エラー: {LABEL_DIR} がありません。")
        return

    # txtファイル一覧
    label_files = sorted(
        LABEL_DIR.glob("*.txt")
    )

    if not label_files:

        print("labelフォルダにtxtファイルがありません。")
        return

    # 進捗読み込み
    start_index = load_progress()

    if start_index >= len(label_files):

        print("すべての文章の録音が完了しています。")
        return

    print("=" * 60)
    print(" 音声データ作成プログラム")
    print("=" * 60)
    print()
    print(f"文章数 : {len(label_files)}")
    print(f"開始位置 : {start_index + 1}")
    print()
    print("操作方法")
    print("  文章表示 → 自動的に録音開始")
    print("  Enter    → 録音終了・保存・次の文章へ")
    print("  Space    → 録音を破棄して中断")
    print()
    print("続行するにはEnterを押してください。")
    print("終了する場合はSpaceを押してください。")
    print("=" * 60)

    # Enterを待つ
    while True:

        key = get_key()

        if key == "\n" or key == "\r":
            break

        if key == " ":
            print("\n中断しました。")
            return

    # ターミナルをrawモードにする
    old_settings = termios.tcgetattr(sys.stdin)

    try:

        tty.setcbreak(sys.stdin.fileno())

        # =================================================
        # 文章を1つずつ処理
        # =================================================

        for index in range(start_index, len(label_files)):

            label_file = label_files[index]

            # 文章読み込み
            text = label_file.read_text(
                encoding="utf-8"
            ).strip()

            print()
            print("=" * 60)
            print(f"文章 {index + 1} / {len(label_files)}")
            print(f"ファイル : {label_file.name}")
            print("=" * 60)
            print()
            print(text)
            print()
            print("-" * 60)
            print("上の文章を読み上げてください。")
            print()
            print("録音を開始します...")
            print()
            print("Enter : 録音終了・保存")
            print("Space : 中断")
            print("-" * 60)

            # 録音
            audio = record_audio()

            # Spaceで中断
            if audio is None:

                print()
                print("プログラムを終了します。")
                print(
                    f"次回は {label_file.name} "
                    "から再開します。"
                )
                return

            # =================================================
            # 保存
            # =================================================

            DATA_DIR.mkdir(
                parents=True,
                exist_ok=True
            )

            # 文章番号をそのまま音声ファイル名にする
            wav_file = DATA_DIR / (
                label_file.stem + ".wav"
            )

            write(
                wav_file,
                FS,
                audio
            )

            print()
            print(f"保存しました:")
            print(f"  {wav_file}")

            # =================================================
            # 進捗更新
            # =================================================

            save_progress(index + 1)

            print()
            print(f"進捗: {index + 1} / {len(label_files)}")

        # =================================================
        # 全部終了
        # =================================================

        print()
        print("=" * 60)
        print("すべての文章の録音が完了しました。")
        print("=" * 60)

    finally:

        # ターミナル設定を元に戻す
        termios.tcsetattr(
            sys.stdin,
            termios.TCSADRAIN,
            old_settings
        )


# =========================================================
# 実行
# =========================================================

if __name__ == "__main__":
    main()
