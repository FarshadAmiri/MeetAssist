# assembly_transcriber.py

import assemblyai as aai

def assembly_stt_diarization(api_key, speakers_expected, audio_path, output_path):
    aai.settings.api_key = api_key

    config = aai.TranscriptionConfig(
        speech_model=aai.SpeechModel.best,
        speaker_labels=True,
        speakers_expected=speakers_expected
    )

    transcript = aai.Transcriber(config=config).transcribe(audio_path)

    if transcript.status == "error":
        raise RuntimeError(f"Transcription failed: {transcript.error}")

    with open(output_path, "w", encoding="utf-8") as f:
        for utterance in transcript.utterances:
            f.write(f"Speaker {utterance.speaker}: {utterance.text}\n")

    print(f"Transcription saved to: {output_path}")
    return transcript.text
