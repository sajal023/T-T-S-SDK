**Multi-Language Text-to-Speech (TTS) System**

This project provides a multi-language text-to-speech (TTS) system using Facebook's MMS-TTS models. The system can automatically detect the language of the input text and generate speech in that language.

**🚀 Features:-**
   1 - Supports multiple languages: Hindi, English, Tamil, Punjabi, Bengali, Marathi, Gujarati, Kannada, Malayalam, Telugu, and more foreign languages.
   2 - Automatic language detection using langdetect and langid.
   3 - On-the-fly model loading to generate high-quality speech.
   4 - Outputs WAV audio format stored in memory for easy playback or saving.

**📌 Supported Languages:-**
    Hindi (hi)
    English (en)
    Tamil (ta)
    Punjabi (pa)
    Bengali (bn)
    Marathi (mr)
    Gujarati (gu)
    Kannada (kn)
    Malayalam (ml)
    Telugu (te)
    French (fr)
    German (de)
    Spanish (es)
    Italian (it)
    Portuguese (pt)
    Russian (ru)
    Chinese (Mandarin) (zh)
    Japanese (ja)


**🛠 Installation**
1️⃣ Prerequisites
    Ensure you have Python 3.8+ installed along with pip.
    You can also use conda or any virtual environment as per your need

2️⃣ Install Required Dependencies
    pip install torch numpy soundfile transformers langdetect langid



**📜 Steps to implement**
    1) Download the zip folder.

    2) Open an IDE (any) and create a new working space or folder using mkdir.

    3) Extract the tts.py, setup.py, and init.py files in the folder.

    4) Create a new file, in which you will pass your input, and import the detect_lang, speak_with_lang functions after installing the TTS folder in your environment  (virtual or system environment) and installing the necessary Python libraries.

    5) After these steps, simply pass your text (input) and the speed of the speaking in the function detect_lang and speak_with_lang, and run the file.

    6) A speech will be streamed in real time at the specified speed.


**📌 How It Works**
   1) Detects the language of the input text using langdetect and langid.
   2) Loads the appropriate TTS model for the detected language.
   3) Generates speech using the model and applies speed modifications.
   4) Streams the audio in real-time for immediate playback.




**⚠️ Error Handling**
If a language is not supported, it prints a warning.
If a model fails to load, it skips that language.

**📜 License**
This project is open-source and available under the MIT License.

