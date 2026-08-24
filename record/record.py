import sounddevice as sd
from scipy.io.wavfile import write
from datetime import datetime
from pathlib import Path

# 録音設定
FS = 16000          # サンプリング周波数
SECONDS = 10        # 録音時間（秒）

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

print(f"録音開始: {filepath}")

# 録音
audio = sd.rec(
    int(SECONDS * FS),
    samplerate=FS,
    channels=1,
    dtype="int16"
)

sd.wait()

# 保存
write(filepath, FS, audio)

print(f"保存しました: {filepath}")
