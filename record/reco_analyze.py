import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from datetime import datetime
from pathlib import Path
from faster_whisper import WhisperModel

# =========================
# 録音設定
# =========================

FS = 16000
CHANNELS = 1

# =========================
# 保存先
# =========================

BASE_DIR = Path("../data")

now = datetime.now()

save_dir = (
    BASE_DIR
    / now.strftime("%Y")
    / now.strftime("%m")
    / now.strftime("%d")
)

save_dir.mkdir(parents=True, exist_ok=True)

filename = now.strftime("%H-%M-%S") + ".wav"
filepath = save_dir / filename

# =========================
# 録音
# =========================

recorded_data = []


def callback(indata, frames, time, status):

    if status:
        print(status)

    recorded_data.append(indata.copy())


print("録音開始")
print("Enterキーを押すと録音を終了して保存します")

with sd.InputStream(
    samplerate=FS,
    channels=CHANNELS,
    dtype="int16",
    callback=callback
):
    input()

# =========================
# 保存
# =========================

audio = np.concatenate(recorded_data, axis=0)

write(filepath, FS, audio)

print()
print(f"保存しました: {filepath}")

# =========================
# faster-whisperで解析するか
# =========================

answer = input(
    "\nfaster-whisperで文字起こししますか？ [y/N]: "
)

if answer.lower() != "y":
    print("文字起こしを行いません。")
    exit()


# =========================
# faster-whisper
# =========================

print()
print("faster-whisperモデルを読み込みます...")

model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)

print("文字起こし開始...")
print()

segments, info = model.transcribe(
    str(filepath),
    language="ja"
)

# =========================
# テキスト保存
# =========================

txt_filepath = filepath.with_suffix(".txt")

with open(txt_filepath, "w", encoding="utf-8") as f:

    for segment in segments:

        text = segment.text.strip()

        print(
            f"[{segment.start:.2f} --> {segment.end:.2f}] "
            f"{text}"
        )

        f.write(text + "\n")


print()
print(f"文字起こし結果を保存しました: {txt_filepath}")
