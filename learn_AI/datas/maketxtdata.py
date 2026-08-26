from pathlib import Path
import re

input_file = Path("input.txt")
output_dir = Path("labels")
output_dir.mkdir(exist_ok=True)

text = input_file.read_text(encoding="utf-8")

# 日本語の句点で分割
sentences = re.split(r"、。,.(?<=[。！？])", text)

sentences = [
    sentence.strip()
    for sentence in sentences
    if sentence.strip()
]

for i, sentence in enumerate(sentences, start=1):

    output_file = output_dir / f"{i:03d}.txt"

    output_file.write_text(
        sentence,
        encoding="utf-8"
    )

print(f"{len(sentences)}個のラベルを作成しました。")
