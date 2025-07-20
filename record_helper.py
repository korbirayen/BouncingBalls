"""
Video Recording Helper for Viral Content Creation
===============================================

This script helps you quickly record your ball physics videos for social media.
Use this after previewing videos in the launcher to create viral content.
"""

import subprocess
import sys
from pathlib import Path
import time

class VideoRecorder:
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.python_exe = self.base_path / ".venv" / "Scripts" / "python.exe"
        
    def list_videos(self):
        """List all available video concepts"""
        folders = []
        for item in self.base_path.iterdir():
            if item.is_dir() and not item.name.startswith('.') and not item.name.startswith('__'):
                main_py = item / "main.py"
                if main_py.exists():
                    folders.append(item.name)
        return sorted(folders)
    
    def record_video(self, video_name, duration=30):
        """
        Launch a video concept for recording
        
        Args:
            video_name: Name of the video folder
            duration: How long to run (for reference)
        """
        video_path = self.base_path / video_name
        main_py = video_path / "main.py"
        
        if not main_py.exists():
            print(f"❌ Video '{video_name}' not found!")
            return False
        
        print(f"🎬 Launching '{video_name}' for recording...")
        print(f"⏱️  Suggested recording duration: {duration} seconds")
        print("📹 Start your screen recorder NOW!")
        print("⚠️  Press Ctrl+C to stop the video")
        print("-" * 50)
        
        try:
            process = subprocess.run(
                [str(self.python_exe), str(main_py)],
                cwd=str(video_path),
                timeout=duration if duration > 0 else None
            )
        except subprocess.TimeoutExpired:
            print(f"✅ Video recording session complete ({duration}s)")
        except KeyboardInterrupt:
            print("⏹️  Recording stopped by user")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        return True
    
    def batch_record_suggestions(self):
        """Suggest viral video recording combinations"""
        suggestions = [
            {
                'name': '4 balls competing',
                'duration': 45,
                'tips': 'Record until only 1 ball remains. Great for TikTok/Instagram Reels!'
            },
            {
                'name': 'Black hole vs balls',
                'duration': 30,
                'tips': 'Capture the mesmerizing absorption effect. Perfect for YouTube Shorts!'
            },
            {
                'name': 'Ball Escape 20 rings 1',
                'duration': 60,
                'tips': 'Record a full escape sequence. Satisfying content for all platforms!'
            },
            {
                'name': 'emoji escape',
                'duration': 25,
                'tips': 'Quick, fun content. Great for viral social media posts!'
            },
            {
                'name': 'Circle Piano',
                'duration': 40,
                'tips': 'Musical physics! Perfect for oddly satisfying compilations!'
            }
        ]
        
        print("🎯 VIRAL VIDEO RECORDING SUGGESTIONS")
        print("=" * 50)
        
        for i, suggestion in enumerate(suggestions, 1):
            print(f"\n{i}. {suggestion['name']}")
            print(f"   Duration: {suggestion['duration']}s")
            print(f"   💡 {suggestion['tips']}")
        
        print("\n" + "=" * 50)
        return suggestions

def main():
    recorder = VideoRecorder()
    
    print("🎥 VIRAL VIDEO FACTORY - RECORDING HELPER")
    print("=" * 50)
    
    while True:
        print("\nChoose an option:")
        print("1. 📋 List all video concepts")
        print("2. 🎬 Record specific video")
        print("3. 🎯 Show viral recording suggestions")
        print("4. 🚀 Quick record (30s)")
        print("5. ❌ Exit")
        
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == '1':
            videos = recorder.list_videos()
            print(f"\n📁 Found {len(videos)} video concepts:")
            for i, video in enumerate(videos, 1):
                print(f"{i:2d}. {video}")
        
        elif choice == '2':
            videos = recorder.list_videos()
            print(f"\n📁 Available videos:")
            for i, video in enumerate(videos, 1):
                print(f"{i:2d}. {video}")
            
            try:
                video_num = int(input(f"\nSelect video (1-{len(videos)}): ")) - 1
                if 0 <= video_num < len(videos):
                    duration = input("Duration in seconds (default 30): ").strip()
                    duration = int(duration) if duration.isdigit() else 30
                    recorder.record_video(videos[video_num], duration)
                else:
                    print("❌ Invalid selection!")
            except ValueError:
                print("❌ Please enter a valid number!")
        
        elif choice == '3':
            suggestions = recorder.batch_record_suggestions()
            try:
                suggestion_num = int(input(f"\nRecord suggestion (1-{len(suggestions)}, 0 to cancel): "))
                if 1 <= suggestion_num <= len(suggestions):
                    suggestion = suggestions[suggestion_num - 1]
                    recorder.record_video(suggestion['name'], suggestion['duration'])
            except ValueError:
                if suggestion_num != 0:
                    print("❌ Please enter a valid number!")
        
        elif choice == '4':
            videos = recorder.list_videos()
            print("🎲 Random video for quick 30s recording...")
            import random
            video = random.choice(videos)
            print(f"Selected: {video}")
            recorder.record_video(video, 30)
        
        elif choice == '5':
            print("👋 Happy content creating!")
            break
        
        else:
            print("❌ Invalid choice! Please select 1-5.")

if __name__ == "__main__":
    main()
