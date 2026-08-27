from faster_whisper import WhisperModel
import time

# モデル読み込み
print("モデル読み込み開始")
t0 = time.time()

MODEL_DIR = "/home/dan/Voicememo/models/my_whisper_tiny_ct2"
audio_file = "../data/2026/08/24/12-16-35.wav"

print("モデル読み込み中...")

model = WhisperModel(
    MODEL_DIR,
    device="cpu",
    compute_type="int8"
)

t1 = time.time()
print(f"モデル読み込み: {t1 - t0:.2f} 秒")


# 文字起こし
print("文字起こし開始")
t2 = time.time()

segments, info = model.transcribe(
    audio_file,
    language="ja"
)

# 結果表示
for segment in segments:
    print(
        f"[{segment.start:.2f} --> {segment.end:.2f}] "
        f"{segment.text}"
    )

t3 = time.time()

print()
print(f"文字起こし時間: {t3 - t2:.2f} 秒")
print(f"合計時間: {t3 - t0:.2f} 秒")
