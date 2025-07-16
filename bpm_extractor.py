import sys
import librosa

def extract_bpm(filename: str) -> float:
  print(f"ファイルを読み込み中: {filename}")
  try:
    y, sr = librosa.load(filename)
  except Exception as e:
    print(f"エラー: ファイルの読み込みに失敗しました。\n詳細: {e}")
    sys.exit(1)

  tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
  return float(tempo)

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("使い方: python bpm_extractor.py <mp3ファイル名>")
    sys.exit(1)

  filename = sys.argv[1]
  bpm = extract_bpm(filename)
  print(f"推定BPM: {bpm:.2f}")
