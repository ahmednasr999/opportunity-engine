#!/usr/bin/env python3
"""
Voice Transcription - Convert voice to text using Whisper API
For quick content creation, job application notes, and ideas
"""

import os
import sys
import json
import tempfile
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict
from dataclasses import dataclass

@dataclass
class TranscriptionResult:
    """Transcription result"""
    text: str
    language: str
    duration: float
    confidence: float
    timestamp: str
    source: str


class VoiceTranscriber:
    """Voice to text transcription"""
    
    def __init__(self, output_dir: str = "/root/.openclaw/workspace/tools/cv-optimizer/output/voice"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.transcriptions_file = self.output_dir / "transcriptions.json"
        self.history = self._load_history()
    
    def _load_history(self) -> list:
        """Load transcription history"""
        if self.transcriptions_file.exists():
            with open(self.transcriptions_file, 'r') as f:
                return json.load(f)
        return []
    
    def _save_history(self):
        """Save transcription history"""
        with open(self.transcriptions_file, 'w') as f:
            json.dump(self.history[-100:], f, indent=2)  # Keep last 100
    
    def transcribe_file(self, audio_path: str, language: str = "en") -> Optional[TranscriptionResult]:
        """Transcribe an audio file"""
        try:
            # Use OpenAI Whisper if API key available
            api_key = os.getenv("OPENAI_API_KEY")
            
            if api_key:
                return self._transcribe_whisper_api(audio_path, language)
            else:
                # Fallback to local whisper if installed
                return self._transcribe_local(audio_path, language)
        
        except Exception as e:
            print(f"❌ Transcription error: {e}")
            return None
    
    def _transcribe_whisper_api(self, audio_path: str, language: str) -> Optional[TranscriptionResult]:
        """Use OpenAI Whisper API"""
        import requests
        
        api_key = os.getenv("OPENAI_API_KEY")
        
        with open(audio_path, 'rb') as f:
            response = requests.post(
                "https://api.openai.com/v1/audio/transcriptions",
                headers={"Authorization": f"Bearer {api_key}"},
                files={"file": f},
                data={
                    "model": "whisper-1",
                    "language": language,
                    "response_format": "json"
                }
            )
        
        if response.status_code == 200:
            data = response.json()
            result = TranscriptionResult(
                text=data.get("text", ""),
                language=data.get("language", language),
                duration=0.0,  # Not provided by API
                confidence=0.95,  # Estimated
                timestamp=datetime.now().isoformat(),
                source=audio_path
            )
            self._save_result(result)
            return result
        else:
            print(f"API Error: {response.status_code} - {response.text}")
            return None
    
    def _transcribe_local(self, audio_path: str, language: str) -> Optional[TranscriptionResult]:
        """Use local whisper installation"""
        try:
            result = subprocess.run(
                ["whisper", audio_path, "--language", language, "--output_format", "json"],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                # Parse whisper output
                output_file = Path(audio_path).with_suffix('.json')
                if output_file.exists():
                    with open(output_file, 'r') as f:
                        data = json.load(f)
                    
                    text = data.get("text", "")
                    
                    transcribed = TranscriptionResult(
                        text=text,
                        language=language,
                        duration=data.get("duration", 0.0),
                        confidence=0.9,
                        timestamp=datetime.now().isoformat(),
                        source=audio_path
                    )
                    self._save_result(transcribed)
                    return transcribed
            
            else:
                print(f"Whisper error: {result.stderr}")
                return None
        
        except FileNotFoundError:
            print("❌ Whisper not installed. Install with: pip install openai-whisper")
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def _save_result(self, result: TranscriptionResult):
        """Save transcription to history"""
        self.history.append({
            "text": result.text,
            "language": result.language,
            "timestamp": result.timestamp,
            "source": result.source
        })
        self._save_history()
    
    def record_and_transcribe(self, duration: int = 60) -> Optional[TranscriptionResult]:
        """Record audio and transcribe (if recording capability available)"""
        print(f"🎙️ Recording for {duration} seconds...")
        print("(Press Ctrl+C to stop early)")
        
        # Create temp file
        temp_file = tempfile.mktemp(suffix=".wav")
        
        try:
            # Record audio using ffmpeg or arecord
            subprocess.run(
                ["ffmpeg", "-f", "alsa", "-i", "default", "-t", str(duration), "-ar", "16000", temp_file],
                check=True,
                capture_output=True
            )
            
            print("📝 Transcribing...")
            result = self.transcribe_file(temp_file)
            
            # Cleanup
            os.remove(temp_file)
            
            return result
        
        except subprocess.CalledProcessError:
            print("❌ Recording failed. Make sure microphone is connected.")
            return None
        except FileNotFoundError:
            print("❌ ffmpeg not found. Install with: apt install ffmpeg")
            return None
    
    def quick_transcribe(self, audio_file: str) -> str:
        """Quick transcribe - returns text only"""
        result = self.transcribe_file(audio_file)
        if result:
            return result.text
        return ""
    
    def create_content_from_voice(self, audio_file: str, content_type: str = "linkedin") -> Dict:
        """Transcribe voice and convert to formatted content"""
        print("🎙️ Transcribing voice note...")
        
        result = self.transcribe_file(audio_file)
        
        if not result:
            return {"error": "Transcription failed"}
        
        raw_text = result.text
        
        # Format based on content type
        if content_type == "linkedin":
            formatted = self._format_linkedin_post(raw_text)
        elif content_type == "note":
            formatted = raw_text
        elif content_type == "job_notes":
            formatted = self._format_job_notes(raw_text)
        else:
            formatted = raw_text
        
        # Save formatted content
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"voice_{content_type}_{timestamp}.txt"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w') as f:
            f.write(f"Original Transcription:\n{raw_text}\n\n")
            f.write(f"Formatted ({content_type}):\n{formatted}\n")
        
        return {
            "transcription": raw_text,
            "formatted": formatted,
            "content_type": content_type,
            "file": str(filepath),
            "word_count": len(formatted.split())
        }
    
    def _format_linkedin_post(self, text: str) -> str:
        """Format transcription as LinkedIn post"""
        # Clean up
        text = text.strip()
        
        # Add line breaks for readability
        sentences = text.replace('. ', '.\n').split('\n')
        formatted = '\n\n'.join([s.strip() for s in sentences if s.strip()])
        
        # Add hashtags
        hashtags = "\n\n#HealthTech #AI #DigitalTransformation #Leadership"
        
        # Add call to action
        cta = "\n\nWhat's your experience with this? Share below! 👇"
        
        return formatted + cta + hashtags
    
    def _format_job_notes(self, text: str) -> str:
        """Format transcription as job interview notes"""
        lines = text.split('.')
        formatted = []
        
        for line in lines:
            line = line.strip()
            if line:
                formatted.append(f"• {line}")
        
        return "\n".join(formatted)
    
    def get_history(self, limit: int = 10) -> list:
        """Get recent transcriptions"""
        return self.history[-limit:]


class VoiceContentPipeline:
    """Pipeline: Voice → Content → Publish"""
    
    def __init__(self):
        self.transcriber = VoiceTranscriber()
    
    def voice_to_linkedin(self, audio_file: str) -> Dict:
        """Full pipeline: Voice file → LinkedIn post"""
        # Step 1: Transcribe
        result = self.transcriber.create_content_from_voice(audio_file, "linkedin")
        
        if "error" in result:
            return result
        
        # Step 2: Save to content factory output
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        content_file = f"/root/.openclaw/workspace/tools/cv-optimizer/output/content/voice_linkedin_{timestamp}.txt"
        
        with open(content_file, 'w') as f:
            f.write(result["formatted"])
        
        result["content_file"] = content_file
        result["ready_to_post"] = True
        
        return result
    
    def voice_to_job_tracker(self, audio_file: str, job_id: str) -> Dict:
        """Pipeline: Voice note → Job notes"""
        result = self.transcriber.create_content_from_voice(audio_file, "job_notes")
        
        if "error" in result:
            return result
        
        # Here you would link to job tracker
        result["job_id"] = job_id
        result["notes_formatted"] = result["formatted"]
        
        return result


def main():
    """CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Voice Transcription")
    parser.add_argument("file", nargs="?", help="Audio file to transcribe")
    parser.add_argument("--type", default="note", choices=["linkedin", "note", "job_notes"], help="Content type")
    parser.add_argument("--record", action="store_true", help="Record from microphone")
    parser.add_argument("--duration", type=int, default=60, help="Recording duration in seconds")
    
    args = parser.parse_args()
    
    transcriber = VoiceTranscriber()
    pipeline = VoiceContentPipeline()
    
    if args.record:
        print("🎙️ Voice Recording Mode")
        print("=" * 50)
        result = transcriber.record_and_transcribe(args.duration)
        
        if result:
            print("\n📝 Transcription:")
            print("=" * 50)
            print(result.text)
            print("=" * 50)
    
    elif args.file:
        print(f"🎙️ Transcribing: {args.file}")
        
        if args.type == "linkedin":
            result = pipeline.voice_to_linkedin(args.file)
            print("\n✅ LinkedIn post created!")
            print(f"📄 Saved to: {result.get('content_file')}")
            print(f"📝 Word count: {result.get('word_count')}")
            print("\nPreview:")
            print("-" * 50)
            print(result.get('formatted', '')[:300] + "...")
        
        else:
            result = transcriber.create_content_from_voice(args.file, args.type)
            print("\n📝 Transcription:")
            print("-" * 50)
            print(result.get('formatted', result.get('transcription', '')))
    
    else:
        print("Voice Transcription Tool")
        print()
        print("Usage:")
        print("  python voice_transcription.py audio.mp3")
        print("  python voice_transcription.py audio.mp3 --type linkedin")
        print("  python voice_transcription.py --record --duration 120")
        print()
        print("Note: Requires OpenAI API key (OPENAI_API_KEY) or local Whisper install")


if __name__ == "__main__":
    main()
