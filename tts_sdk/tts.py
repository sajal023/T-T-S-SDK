import torch
import numpy as np
import io
import soundfile as sf
from transformers import VitsModel, AutoTokenizer
from langdetect import detect
from langid.langid import classify
import sounddevice as sd

supported_languages = {
    # 🌍 Indian Languages
    "hi": "facebook/mms-tts-hin",  # Hindi
    "en": "facebook/mms-tts-eng",  # English
    "ta": "facebook/mms-tts-tam",  # Tamil
    "pa": "facebook/mms-tts-pan",  # Punjabi
    "bn": "facebook/mms-tts-ben",  # Bengali
    "mr": "facebook/mms-tts-mar",  # Marathi
    "gu": "facebook/mms-tts-guj",  # Gujarati
    "kn": "facebook/mms-tts-kan",  # Kannada
    "ml": "facebook/mms-tts-mal",  # Malayalam
    "te": "facebook/mms-tts-tel",  # Telugu
    "or": "facebook/mms-tts-ory",  # Odia
    "as": "facebook/mms-tts-asm",  # Assamese
    "ur": "facebook/mms-tts-urd",  # Urdu
    "sd": "facebook/mms-tts-snd",  # Sindhi
    "kok": "facebook/mms-tts-kok", # Konkani
    "sa": "facebook/mms-tts-san",  # Sanskrit
    "doi": "facebook/mms-tts-doi", # Dogri
    "ne": "facebook/mms-tts-nep",  # Nepali
    "mai": "facebook/mms-tts-mai", # Maithili
    "brx": "facebook/mms-tts-brx", # Bodo
    "mni": "facebook/mms-tts-mni", # Manipuri
    "sat": "facebook/mms-tts-sat", # Santali

    # 🌎 European Languages
    "fr": "facebook/mms-tts-fra",  # French
    "de": "facebook/mms-tts-deu",  # German
    "es": "facebook/mms-tts-spa",  # Spanish
    "it": "facebook/mms-tts-ita",  # Italian
    "pt": "facebook/mms-tts-por",  # Portuguese
    "ru": "facebook/mms-tts-rus",  # Russian
    "nl": "facebook/mms-tts-nld",  # Dutch
    "pl": "facebook/mms-tts-pol",  # Polish
    "sv": "facebook/mms-tts-swe",  # Swedish
    "da": "facebook/mms-tts-dan",  # Danish
    "fi": "facebook/mms-tts-fin",  # Finnish
    "no": "facebook/mms-tts-nor",  # Norwegian
    "el": "facebook/mms-tts-ell",  # Greek

    # 🌏 Asian Languages
    "zh": "facebook/mms-tts-zho",  # Chinese (Mandarin)
    "ja": "facebook/mms-tts-jpn",  # Japanese
    "ko": "facebook/mms-tts-kor",  # Korean
    "th": "facebook/mms-tts-tha",  # Thai
    "vi": "facebook/mms-tts-vie",  # Vietnamese
    "ms": "facebook/mms-tts-msa",  # Malay
    "id": "facebook/mms-tts-ind",  # Indonesian
    "fil": "facebook/mms-tts-tgl", # Filipino (Tagalog)

    # 🌍 Middle Eastern & African Languages
    "ar": "facebook/mms-tts-ara",  # Arabic
    "tr": "facebook/mms-tts-tur",  # Turkish
    "fa": "facebook/mms-tts-fas",  # Persian (Farsi)
    "he": "facebook/mms-tts-heb",  # Hebrew
    "am": "facebook/mms-tts-amh",  # Amharic
    "sw": "facebook/mms-tts-swa",  # Swahili
    "yo": "facebook/mms-tts-yor",  # Yoruba
    "ha": "facebook/mms-tts-hau",  # Hausa
    "ig": "facebook/mms-tts-ibo",  # Igbo

    # 🌎 Other Languages
    "hu": "facebook/mms-tts-hun",  # Hungarian
    "cs": "facebook/mms-tts-ces",  # Czech
    "ro": "facebook/mms-tts-ron",  # Romanian
    "bg": "facebook/mms-tts-bul",  # Bulgarian
    "uk": "facebook/mms-tts-ukr",  # Ukrainian
    "sr": "facebook/mms-tts-srp",  # Serbian
    "hr": "facebook/mms-tts-hrv",  # Croatian
    "sk": "facebook/mms-tts-slk",  # Slovak
}

loaded_models = {}

def get_model(lang):
    """
    Loads the text-to-speech (TTS) model for the given language.

    Args:
        lang (str): Language code (e.g., "hi" for Hindi, "en" for English).

    Returns:
        tuple: (model, tokenizer) if successful, otherwise (None, None).
    """
    try:
        if lang not in loaded_models:
            print(f"🚀 Loading model for {lang}...")
            model = VitsModel.from_pretrained(supported_languages[lang])
            tokenizer = AutoTokenizer.from_pretrained(supported_languages[lang])

            model.eval()  # Set model to evaluation mode
            loaded_models[lang] = (model, tokenizer)

        return loaded_models[lang]

    except KeyError:
        print(f"❌ Model for language '{lang}' is not available.")
    except Exception as e:
        print(f"⚠️ Failed to load model {lang}: {e}")
    
    return None, None  # Return None if model loading fails


def detect_language(text):
    """
    Detects the language of the given text.

    Args:
        text (str): The input text for language detection.

    Returns:
        str: Detected language code (e.g., "hi" for Hindi) or "unknown" if detection fails.
    """
    try:
        lang, _ = classify(text)  # Fastest method
        if lang in supported_languages:
            return lang
        detected = detect(text)
        return detected if detected in supported_languages else "unknown"
    except Exception as e:
        print(f"⚠️ Language detection failed: {e}")
        return "unknown"


def time_stretch(waveform, speed):
    """
    Adjusts the speed of the audio waveform using time-stretching.

    Args:
        waveform (numpy.ndarray): The input audio waveform.
        speed (float): Speed factor (e.g., 1.0 for normal speed, 1.5 for faster speech).

    Returns:
        numpy.ndarray: The modified waveform with adjusted speed.
    """
    try:
        if speed == 1.0:
            return waveform  # No change to the waveform
        
        num_samples = int(len(waveform) / speed)
        indices = np.linspace(0, len(waveform) - 1, num_samples)
        stretched_waveform = np.interp(indices, np.arange(len(waveform)), waveform)

        return stretched_waveform

    except Exception as e:
        print(f"⚠️ Error adjusting speed: {e}")
        return waveform  # Return original waveform if an error occurs


def synthesize_audio(text, lang, speed=1.0):
    """
    Converts text into speech using the specified language model and applies speed modification.

    Args:
        text (str): The input text to be converted into speech.
        lang (str): The language code of the text.
        speed (float, optional): Speed factor (default is 1.0).

    Returns:
        io.BytesIO: A buffer containing the generated speech audio.
    """
    try:
        model, tokenizer = get_model(lang)
        if not model:
            return None

        inputs = tokenizer(text, return_tensors="pt")

        with torch.no_grad():
            output = model(**inputs).waveform.float()

        waveform = output.squeeze().cpu().numpy()
        waveform = time_stretch(waveform, speed)  # Adjust speed

        audio_buffer = io.BytesIO()
        sf.write(audio_buffer, waveform, 16000, format="WAV")
        audio_buffer.seek(0)

        return audio_buffer

    except Exception as e:
        print(f"❌ Failed to generate speech: {e}")
        return None


def speak(text, speed=1.0):
    """
    Detects the language of the text and generates speech.

    Args:
        text (str): The input text to be spoken.
        speed (float, optional): Speed factor (default is 1.0).

    Returns:
        io.BytesIO: A buffer containing the generated speech audio, or None if generation fails.
    """
    try:
        detected_lang = detect_language(text)
        print(f"🔍 Detected Language: {detected_lang}")

        if detected_lang in supported_languages:
            return synthesize_audio(text, detected_lang, speed)
        else:
            print("⚠️ Language not supported.")
            return None

    except Exception as e:
        print(f"⚠️ Error in speak function: {e}")
        return None


def speak_with_lang(lang, text, speed=1.0):
    """
    Generates speech using a specified language without detecting it first.

    Args:
        lang (str): The language code to use for speech synthesis.
        text (str): The input text to be spoken.
        speed (float, optional): Speed factor (default is 1.0).

    Returns:
        io.BytesIO: A buffer containing the generated speech audio, or None if generation fails.
    """
    try:
        if lang not in supported_languages:
            print(f"⚠️ Language '{lang}' not supported.")
            return None

        print(f"🎙️ Using pre-detected language: {lang}")
        return synthesize_audio(text, lang, speed)

    except Exception as e:
        print(f"⚠️ Error in speak_with_lang function: {e}")
        return None
