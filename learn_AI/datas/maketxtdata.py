from pathlib import Path
import re

# 元のtxtファイル
input_file = Path("input.txt")

# 保存先
output_dir = Path("labels")
output_dir.mkdir(exist_ok=True)

# 読み込み
text = input_file.read_text(encoding="utf-8")

# 「、」「。」「！」「？」で分割
sentences = re.split(r"(?<=[、。！？])", text)

# 空行・空文字を除去
sentences = [
    sentence.strip()
    for sentence in sentences
    if sentence.strip()
]

# 保存
for i, sentence in enumerate(sentences, start=1):
    output_file = output_dir / f"{i:04d}.txt"

    output_file.write_text(
        sentence,
        encoding="utf-8"
    )

print(f"{len(sentences)}個のファイルを作成しました。")
