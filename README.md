
# Audio Transcriber & Summarizer

This project transcribes `.mp3` or `.wav` audio files into Markdown format using [OpenAI Whisper](https://github.com/openai/whisper), then summarizes each transcript and generates a short title using the [Mistral](https://ollama.com/library/mistral) language model via [Ollama](https://ollama.com).

Each transcription is saved to a single dated Markdown file, formatted for use in note-taking tools like Obsidian or Notion. 

This works especially well for students who want to record an audio in completing their homework, rather than typing it out, for time or simplicity. It can be integrated pretty seamlessly with iPhone shortcuts. 

Should work pretty well with class lectures too. 

Basically all you need to do is fine tune the prompt in transcribe.py, and enter your file locations in the .bat file, and download what's under requirements. 
---

## Features

- Transcribes audio using Whisper (`base` model by default)
- Summarizes transcription in 1–3 sentences
- Generates a 3–4 word title
- Combines all results into a single Markdown file
- Deletes audio files after processing

---

## Requirements

### Python 3.8 or newer

Install required Python packages:
```bash
pip install openai-whisper torch torchvision torchaudio
