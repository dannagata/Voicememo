import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from datetime import datetime
from pathlib import Path

# 録音設定
FS = 16000
CHANNELS = 1

# 保存先
BASE_DIR = Path("../data")

# 現在日時
now = datetime.now()

# 年/月/日のフォルダを作成
save_dir = (
    BASE_DIR
    / now.strftime("%Y")
    / now.strftime("%m")
    / now.strftime("%d")
)

save_dir.mkdir(parents=True, exist_ok=True)

# ファイル名
filename = now.strftime("%H-%M-%S") + ".wav"
filepath = save_dir / filename

# 録音データを保存するリスト
recorded_data = []

def callback(indata, frames, time, status):
    if status:
        print(status)

    recorded_data.append(indata.copy())


print("録音開始")
print("Enterキーを押すと録音を終了して保存します")

# 録音開始
with sd.InputStream(
    samplerate=FS,
    channels=CHANNELS,
    dtype="int16",
    callback=callback
):
    input()

# 録音データを結合
audio = np.concatenate(recorded_data, axis=0)

# 保存
write(filepath, FS, audio)

print(f"保存しました: {filepath}")
