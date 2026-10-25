"""bpm_extractor のテスト。"""

import contextlib
import io
import os
import tempfile
import unittest

import numpy as np
import soundfile as sf

from bpm_extractor import extract_bpm

SAMPLE_RATE = 22050

def write_click_track(path: str, bpm: float, seconds: float = 20.0) -> None:
  """一定のテンポでクリック音が鳴る WAV ファイルを書き出す。

  引数:
    path: 書き出す WAV ファイルのパス
    bpm: クリックのテンポ（1 分あたりの拍数）
    seconds: 音声の長さ（秒）

  戻り値:
    なし
  """
  signal = np.zeros(int(SAMPLE_RATE * seconds), dtype=np.float32)
  click_length = int(SAMPLE_RATE * 0.03)
  t = np.arange(click_length) / SAMPLE_RATE
  click = (np.sin(2 * np.pi * 1000 * t) * np.exp(-t * 200)).astype(np.float32)
  interval = 60.0 / bpm
  for beat_time in np.arange(0, seconds - 0.05, interval):
    start = int(beat_time * SAMPLE_RATE)
    signal[start : start + click_length] += click[: len(signal) - start]
  sf.write(path, signal, SAMPLE_RATE)

class ExtractBpmTest(unittest.TestCase):
  """extract_bpm のテスト。"""

  def setUp(self) -> None:
    """一時ディレクトリを作る。

    引数:
      なし

    戻り値:
      なし
    """
    self.tmpdir = tempfile.TemporaryDirectory()
    self.addCleanup(self.tmpdir.cleanup)

  def extract_quietly(self, path: str) -> float:
    """標準出力を捨てながら extract_bpm を呼ぶ。

    引数:
      path: 解析する音声ファイルのパス

    戻り値:
      extract_bpm の戻り値
    """
    with contextlib.redirect_stdout(io.StringIO()):
      return extract_bpm(path)

  def test_estimates_tempo_of_click_track(self) -> None:
    """クリック音のテンポを ±3% 以内で推定できること。

    librosa はフレーム単位でテンポを測るので、120 BPM 付近の推定値は
    117.45 か 123.05 のような飛び飛びの値になる。その刻み幅が収まる許容誤差にする。

    引数:
      なし

    戻り値:
      なし
    """
    for bpm in [90, 120, 150]:
      with self.subTest(bpm=bpm):
        path = os.path.join(self.tmpdir.name, f"click_{bpm}.wav")
        write_click_track(path, bpm)
        self.assertAlmostEqual(self.extract_quietly(path), bpm, delta=bpm * 0.03)

  def test_returns_python_float(self) -> None:
    """戻り値が numpy の配列ではなく Python の float であること。

    引数:
      なし

    戻り値:
      なし
    """
    path = os.path.join(self.tmpdir.name, "click.wav")
    write_click_track(path, 120)
    self.assertIs(type(self.extract_quietly(path)), float)

  def test_exits_when_file_is_missing(self) -> None:
    """ファイルがないときは終了コード 1 で終わること。

    引数:
      なし

    戻り値:
      なし
    """
    path = os.path.join(self.tmpdir.name, "missing.mp3")
    with self.assertRaises(SystemExit) as cm:
      self.extract_quietly(path)
    self.assertEqual(cm.exception.code, 1)

if __name__ == "__main__":
  unittest.main()
