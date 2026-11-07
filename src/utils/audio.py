"""Simple built-in sound effects and background music for the game."""

import math
import os
import sys  # Idinagdag para sa sys._MEIPASS
import wave
import pygame

# Idinagdag ang get_path function para sa PyInstaller .exe compatibility
def get_path(relative_path):
    try:
        # Ito ang temporary folder na ginagawa ng PyInstaller tuwing ino-open ang .exe
        base_path = sys._MEIPASS
    except Exception:
        # Kapag ni-run mo lang sa PyCharm, babalik ito sa main project folder
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class AudioManager:
    """Manage generated effects and optional real music tracks."""

    def __init__(self):
        self.enabled = True
        self.background_music = None
        self.background_music_path = None

        # In-update ang _audio_dir para gamitin ang get_path()
        self._audio_dir = get_path(os.path.join("assets", "audio"))
        os.makedirs(self._audio_dir, exist_ok=True)
        self._initialize()

    def _find_background_music(self):
        supported_exts = (".mp3", ".wav", ".ogg", ".flac")
        preferred_names = (
            "game_music.wav",
            "game_music.mp3",
            "theme_music.wav",
            "theme_music.mp3",
            "background_music.wav",
            "background_music.mp3",
            "music.wav",
            "music.mp3",
            "bgm_loop.wav",
            "bgm_loop.mp3",
        )

        for name in preferred_names:
            path = os.path.join(self._audio_dir, name)
            if os.path.exists(path):
                return path

        for entry in sorted(os.listdir(self._audio_dir)):
            lower = entry.lower()
            if any(lower.endswith(ext) for ext in supported_exts):
                return os.path.join(self._audio_dir, entry)

        return None

    def _initialize(self):
        try:
            pygame.mixer.init()
            self.enabled = True
        except Exception:
            self.enabled = False

    def set_enabled(self, enabled):
        if enabled:
            self._initialize()
            self.play_background_music()
        else:
            self.enabled = False
            if self.background_music is not None:
                self.background_music.stop()
            try:
                pygame.mixer.music.stop()
            except Exception:
                pass
            try:
                pygame.mixer.quit()
            except Exception:
                pass

    def toggle(self):
        self.set_enabled(not self.enabled)
        return self.enabled

    def _write_wave(self, name, freqs, duration, volume):
        path = os.path.join(self._audio_dir, f"{name}.wav")
        sample_rate = 22050
        frames = int(sample_rate * duration)
        raw = []
        for i in range(frames):
            t = i / sample_rate
            value = 0.0
            for freq in freqs:
                # Inayos ang syntax error dito (nilagyan ng * pagkatapos ng 2)
                value += math.sin(2 * math.pi * freq * t)

            value /= len(freqs)
            value *= volume
            value = max(-1.0, min(1.0, value))
            raw.append(int(max(-32768, min(32767, value * 32767))))

        with wave.open(path, "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(b"".join(v.to_bytes(2, byteorder="little", signed=True) for v in raw))
        return path

    def _get_sound(self, name, freqs, duration=0.24, volume=0.22):
        if not self.enabled:
            return None
        path = os.path.join(self._audio_dir, f"{name}.wav")
        if not os.path.exists(path):
            self._write_wave(name, freqs, duration, volume)
        try:
            return pygame.mixer.Sound(path)
        except Exception:
            return None

    def _play(self, freq_list, duration=0.24, volume=0.22):
        if not self.enabled:
            return
        sound = self._get_sound("tmp", freq_list, duration, volume)
        if sound is not None:
            sound.play()

    def play_background_music(self):
        if not self.enabled:
            return

        if self.background_music_path is None:
            self.background_music_path = self._find_background_music()

        if self.background_music_path is not None:
            try:
                pygame.mixer.music.load(self.background_music_path)
                pygame.mixer.music.play(-1)
                return
            except Exception:
                self.background_music_path = None

        if self.background_music is None:
            self.background_music = self._get_sound("bgm_loop", [196, 220, 246.94, 220], 0.55, 0.12)
        if self.background_music is not None:
            self.background_music.play(loops=-1)

    def play_click(self):
        self._play([540], 0.08, 0.12)

    def play_correct(self):
        self._play([660, 880], 0.18, 0.16)

    def play_error(self):
        self._play([180, 120], 0.16, 0.18)

    def play_win(self):
        self._play([660, 880, 1100], 0.26, 0.18)

    def play_lose(self):
        self._play([220, 180, 140], 0.25, 0.18)