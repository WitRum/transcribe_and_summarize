# Audio Transcriber & Summarizer

Turns `.mp3` / `.wav` recordings into a dated Markdown note. Each recording is transcribed locally with [OpenAI Whisper](https://github.com/openai/whisper), then given a short title and a three-sentence summary by the [Mistral](https://ollama.com/library/mistral) model running through [Ollama](https://ollama.com). Everything runs on your machine, with no cloud API.

The output is formatted for note-taking tools like Obsidian or Notion. It works well for dictating homework, recording lectures, or voice memos (it pairs nicely with iPhone Shortcuts).

## Features

- Transcribes audio with Whisper (`base` model by default)
- Generates a 3-4 word title and a 3-sentence summary per recording
- Combines all results into one dated Markdown file, e.g. `Nov. 21, 26.md`
- Deletes each audio file after it is processed

## Requirements

- Python 3.8+
- [ffmpeg](https://ffmpeg.org/download.html)
- [Ollama](https://ollama.com) with the Mistral model: `ollama pull mistral`

```bash
pip install -r requirements.txt
```

## Usage

```bash
python transcribe.py --audio "path/to/audio" --vault "path/to/notes" --ffmpeg "path/to/ffmpeg/bin"
```

| Flag | Meaning |
|------|---------|
| `--audio`, `-a` | Folder containing `.mp3` / `.wav` files |
| `--vault`, `-v` | Folder where the Markdown file is saved |
| `--ffmpeg`, `-f` | Path to the ffmpeg `bin` folder |

On Windows, edit the paths in `transcribe.bat` and double-click it to run.

## Customizing

Edit the prompt in `summarize_with_ollama()` in `transcribe.py` to change the summary style or length. Change `"base"` in `whisper.load_model()` to `small`, `medium` or `large` for better accuracy at the cost of speed.

> **Note:** audio files are deleted after processing, so keep a copy if you need the originals.
