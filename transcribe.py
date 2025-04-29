print("let's get going")

import os
import sys
import subprocess
import whisper
import argparse
from pathlib import Path
from datetime import datetime

# Ollama minstral prompt for summarization and title creation

def summarize_with_ollama(text: str) -> tuple[str, str]:
    # Truncate if transcript is longer (1000 words)
    if len(text.split()) > 1000:
        text = " ".join(text.split()[:1000])

    prompt = (
        "Respond with ONLY the 3–4 word title on the first line (no 'Title:' label), do not include quotation marks. "
        "Give a short 3–4 word title. Then, summarize what the speaker said in exactly 3 sentences. Do not act or respond as AI. \n\n"
        f"{text}"
    )

    try:
        result = subprocess.run(
            ["ollama", "run", "mistral"],
            input=prompt,
            text=True,
            capture_output=True,
            check=True
        )
        response = result.stdout.strip()
        lines = response.split("\n")

        # Clean the title and remove known prefixes or formatting
        title = lines[0].lower().replace("title:", "").strip("# ").strip().capitalize()
        summary = "\n".join(lines[1:]).strip() if len(lines) > 1 else "(No summary generated)"

        if not summary:
            summary = "(No summary generated)"

        return title, summary
    except subprocess.CalledProcessError as e:
        print(f"[Summarization Error]: {e}")
        return "Untitled", "(Summary error)"

# Makes bat file relevant

def parse_args():
    parser = argparse.ArgumentParser(description="Transcribe audio to Markdown using Whisper.")
    parser.add_argument("--audio", "-a", required=True, help="Folder containing .mp3 or .wav files")
    parser.add_argument("--vault", "-v", required=True, help="Folder to save markdown files")
    parser.add_argument("--ffmpeg", "-f", required=True, help="Path to ffmpeg/bin folder")
    return parser.parse_args()

# Transcription

def setup_ffmpeg_path(ffmpeg_path: Path):
    os.environ["PATH"] = str(ffmpeg_path) + os.pathsep + os.environ["PATH"]

def transcribe_audio(model, audio_path: Path):
    try:
        result = model.transcribe(str(audio_path))
        return result["text"]
    except Exception as e:
        print(f"[Transcription Error] {audio_path.name}: {e}")
        return None

def process_audio_folder(audio_folder: Path, vault_folder: Path):
    if not audio_folder.exists():
        print(f"[Error] Audio folder does not exist: {audio_folder}")
        return

    vault_folder.mkdir(parents=True, exist_ok=True)
    audio_files = list(audio_folder.glob("*.mp3")) + list(audio_folder.glob("*.wav"))
    if not audio_files:
        print("[Info] No audio files found.")
        return

    model = whisper.load_model("base")
    print(f"[Info] Found {len(audio_files)} audio file(s).\n")

# Saves md. file with date in the vault folder

    today = datetime.now()
    date_str = today.strftime("%b.") + f" {today.day}, " + today.strftime("%y")
    filename = f"{date_str}.md"
    output_path = vault_folder / filename

    full_markdown = ""

    for audio_file in audio_files:
        print(f"[>>] Processing: {audio_file.name}")
        transcript = transcribe_audio(model, audio_file)
        if not transcript:
            print("[Skipped] Transcription failed.\n")
            continue

        title, summary = summarize_with_ollama(transcript)

        full_markdown += (
        f"## {title}\n\n"
        f"{summary}\n\n"
        f"**Full Transcription:**\n\n{transcript.strip()}\n\n---\n\n"
)

# Delete audio files after processing
        try:
            audio_file.unlink()
            print(f"[✓] Processed and deleted: {audio_file.name}\n")
        except Exception as e:
            print(f"[Error] Couldn't delete {audio_file.name}: {e}")

    try:
        with output_path.open("w", encoding="utf-8") as f:
            f.write(full_markdown.strip())
        print(f"[✓] Saved all transcriptions to: {filename}\n")
    except Exception as e:
        print(f"[Error] Failed to write final markdown file: {e}\n")

    print("[Done] All audio files processed.\n")

if __name__ == "__main__":
    try:
        args = parse_args()
        setup_ffmpeg_path(Path(args.ffmpeg))
        process_audio_folder(Path(args.audio), Path(args.vault))
        print("finished")
    except Exception as fatal:
        print(f"[Fatal Error] {fatal}")
        sys.exit(1)