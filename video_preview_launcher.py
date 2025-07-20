"""
Viral Video Factory Preview Launcher
====================================

This launcher lets you preview all your viral ball physics video concepts.
Use arrow keys or number keys to switch between different videos instantly.

Controls:
- LEFT/RIGHT arrows: Navigate between videos
- SPACE: Launch current video
- ESC: Exit
- Number keys (1-9, 0): Jump to specific video
- R: Random video
- ENTER: Launch selected video

Each folder represents a different viral video concept optimized for maximum viewer engagement!
"""

import os
import sys
import subprocess
import pygame
import time
import random
from pathlib import Path

class VideoPreviewLauncher:
    def __init__(self):
        pygame.init()
        
        # Screen setup
        self.screen_width = 900
        self.screen_height = 800
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("🎥 Viral Ball Video Factory - Preview Launcher")
        
        # Set window icon (optional - uses default if no icon file)
        try:
            icon = pygame.Surface((32, 32))
            icon.fill((255, 100, 100))
            pygame.display.set_icon(icon)
        except:
            pass
        
        # Font setup with fallbacks
        try:
            self.title_font = pygame.font.Font(None, 56)
            self.subtitle_font = pygame.font.Font(None, 36)
            self.text_font = pygame.font.Font(None, 28)
            self.small_font = pygame.font.Font(None, 22)
            self.tiny_font = pygame.font.Font(None, 18)
        except:
            # Fallback to default font
            self.title_font = pygame.font.Font(None, 48)
            self.subtitle_font = pygame.font.Font(None, 32)
            self.text_font = pygame.font.Font(None, 24)
            self.small_font = pygame.font.Font(None, 20)
            self.tiny_font = pygame.font.Font(None, 16)
        
        # Colors
        self.bg_color = (20, 25, 35)
        self.card_color = (35, 42, 55)
        self.title_color = (255, 120, 120)
        self.subtitle_color = (120, 180, 255)
        self.text_color = (220, 220, 220)
        self.highlight_color = (255, 200, 80)
        self.button_color = (60, 70, 90)
        self.button_hover_color = (80, 95, 120)
        self.accent_color = (100, 255, 150)
        self.warning_color = (255, 100, 100)
        
        # Get all video folders
        self.base_path = Path(__file__).parent
        self.video_folders = self.get_video_folders()
        self.current_index = 0
        self.current_process = None
        
        # UI state
        self.scroll_offset = 0
        self.mouse_pos = (0, 0)
        self.animation_time = 0
        self.status_message = ""
        self.status_timer = 0
        
        # Sound
        pygame.mixer.init()
        
        print(f"Viral Video Factory Initialized!")
        print(f"Found {len(self.video_folders)} video concepts")
        
    def get_video_folders(self):
        """Get all folders that contain video concepts (have main.py)"""
        folders = []
        try:
            for item in self.base_path.iterdir():
                if item.is_dir() and not item.name.startswith('.') and not item.name.startswith('__'):
                    main_py = item / "main.py"
                    if main_py.exists():
                        folders.append({
                            'name': item.name,
                            'path': item,
                            'description': self.get_video_description(item.name),
                            'status': 'ready'
                        })
            
            if not folders:
                print("No video folders found! Make sure each folder has a main.py file.")
                
        except Exception as e:
            print(f"Error scanning folders: {e}")
            
        return sorted(folders, key=lambda x: x['name'])
    
    def get_video_description(self, folder_name):
        """Generate engaging descriptions for each video concept"""
        descriptions = {
            '4 balls competing': 'EPIC BATTLE! Balls shrink on impact - Last one standing WINS!',
            'Ball Escape 20 rings 1': 'ESCAPE CHALLENGE! Navigate 20 spinning rings before time runs out!',
            'ball escape verticle_ destroy rings 2': 'DESTRUCTION MODE! Vertical escape course with ring demolition!',
            'ball have n second to escape': 'TIME ATTACK! Race against the clock to escape!',
            'Ball txt': 'TEXT BALLS! Typography meets physics in this unique concept!',
            'ball XMoney': 'MONEY BALLS! Collect currencies from around the world!',
            'BallNC2': 'POLITICAL SHOWDOWN! Biden vs Trump in ball form!',
            'BallNC6': 'GEOMETRIC MADNESS! Polygons and squares collision fest!',
            'BallNC8': 'SHAPE SYMPHONY! Advanced geometric interactions!',
            'BallNC9': 'POLYGON PARADISE! Multi-sided mayhem!',
            'BasketBall': 'SPORTS ACTION! Classic basketball physics simulation!',
            'BasketBall 2 (1)': 'BASKETBALL 2.0! Enhanced sports mechanics!',
            'BasketBall 3 (1)': 'TRIPLE THREAT! Advanced basketball gameplay!',
            'BasketBall 4': 'BASKETBALL FINALE! Ultimate sports physics!',
            'Black hole vs balls': 'COSMIC TERROR! Black hole devours everything in sight!',
            'Black hole vs balls Image': 'VISUAL BLACK HOLE! Image-enhanced cosmic destruction!',
            'Circle Piano': 'MUSICAL MAGIC! Balls create music on impact!',
            'Control inner square': 'PRECISION CONTROL! Master the inner square challenge!',
            'emoji escape': 'EMOJI MADNESS! Emojis trying to escape the funnel!',
            'fill the hunger': 'FEED THE VOID! Satisfy the hungry black hole!',
            'minecraft hoe': 'MINECRAFT PHYSICS! Block-world ball mechanics!',
            'Rocket Leauge': 'CAR SOCCER! Rocket League style ball physics!',
            'Spin Cannon shoot balls': 'CANNON CHAOS! Rotating cannons firing balls everywhere!',
            
            # AI-Generated Viral Concepts (50 new videos)
            'ai-generated-1': 'SPEED ACCELERATION LOOP! Ball gets 5% faster each bounce until impossibly fast!',
            'ai-generated-2': 'COLOR EXPLOSION CHAIN! Collisions create particle explosions spawning more balls!',
            'ai-generated-3': 'GRAVITY FLIP SYMPHONY! Gravity changes rhythmically creating mesmerizing dance!',
            'ai-generated-4': 'SIZE DOUBLING MADNESS! Ball doubles every 5 seconds until it fills screen!',
            'ai-generated-5': 'RAINBOW TRAIL PAINTER! Ball paints entire screen with rainbow trails!',
            'ai-generated-6': 'MIRROR BALL UNIVERSE! 4 synchronized balls create kaleidoscope patterns!',
            'ai-generated-7': 'QUANTUM TELEPORT CHAOS! Ball teleports randomly leaving ghost trails!',
            'ai-generated-8': 'MAGNETIC ATTRACTION STORM! Multiple balls swirl hypnotically around cursor!',
            'ai-generated-9': 'FIBONACCI SPIRAL BOUNCE! Perfect mathematical spiral - absolutely satisfying!',
            'ai-generated-10': 'BEAT DROP PHYSICS! Ball bounces sync to music changing colors!',
            'ai-generated-11': 'INFINITE BALL SPLIT! Every collision splits ball into 2 smaller ones!',
            'ai-generated-12': 'PENDULUM HYPNOSIS! Perfect pendulum with gradually increasing amplitude!',
            'ai-generated-13': 'VORTEX CONSUMPTION! Spinning center slowly consumes everything!',
            'ai-generated-14': 'LIQUID METAL MORPH! Ball morphs between liquid and solid states!',
            'ai-generated-15': 'DNA HELIX TRACE! Two balls create perfect double helix pattern!',
            'ai-generated-16': 'PARTICLE MAGNETISM! Ball attracts thousands of particles into shapes!',
            'ai-generated-17': 'TIME REVERSE ECHO! Time-delayed copies follow exact same path!',
            'ai-generated-18': 'ELASTIC COLLISION ART! Multiple balls create perfect collision patterns!',
            'ai-generated-19': 'ORBITAL MECHANICS! Balls orbit each other in planetary motion!',
            'ai-generated-20': 'CRYSTALLINE GROWTH! Balls stack forming growing crystal structures!',
            'ai-generated-21': 'WAVE INTERFERENCE! Multiple ripple waves interfere beautifully!',
            'ai-generated-22': 'GOLDEN RATIO SPIRAL! Movement follows golden ratio perfection!',
            'ai-generated-23': 'MOMENTUM CONSERVATION! Perfect physics momentum transfer demo!',
            'ai-generated-24': 'FLUID SIMULATION! Hundreds of tiny balls behave like liquid!',
            'ai-generated-25': 'MANDALA CREATION! Balls automatically trace intricate mandalas!',
            'ai-generated-26': 'CHAOS THEORY DEMO! Tiny changes create dramatically different paths!',
            'ai-generated-27': 'HARMONIC OSCILLATOR! Perfect harmonic motion at different frequencies!',
            'ai-generated-28': 'FRACTAL TREE GROWTH! Balls branch creating fractal tree patterns!',
            'ai-generated-29': 'ENERGY CONSERVATION! Height converts to speed in perfect demo!',
            'ai-generated-30': 'LISSAJOUS CURVES! Beautiful mathematical curve patterns!',
            'ai-generated-31': 'PARTICLE ACCELERATOR! Balls spiral inward at increasing speeds!',
            'ai-generated-32': 'TESSELLATION BUILDER! Perfect geometric tessellation formation!',
            'ai-generated-33': 'DOPPLER EFFECT VISUAL! Color changes based on speed!',
            'ai-generated-34': 'CONWAY GAME OF LIFE! Balls follow Game of Life rules!',
            'ai-generated-35': 'MAGNETIC FIELD LINES! Trace magnetic field patterns!',
            'ai-generated-36': 'PERFECT PACKING! Optimal circle packing configurations!',
            'ai-generated-37': 'BROWNIAN MOTION! Realistic particle physics simulation!',
            'ai-generated-38': 'FOURIER TRANSFORM! Visual math transformation demo!',
            'ai-generated-39': 'DOUBLE PENDULUM! Chaotic motion with beautiful trails!',
            'ai-generated-40': 'PHASE SPACE PORTRAIT! Mathematical attractor patterns!',
            'ai-generated-41': 'LATTICE VIBRATIONS! Crystal lattice vibration modes!',
            'ai-generated-42': 'PERCOLATION THEORY! Statistical physics demonstration!',
            'ai-generated-43': 'STRANGE ATTRACTOR! Lorenz butterfly pattern creation!',
            'ai-generated-44': 'REACTION DIFFUSION! Natural pattern formation simulation!',
            'ai-generated-45': 'QUANTUM TUNNELING! Ball tunnels through barriers mysteriously!',
            'ai-generated-46': 'CYMATICS PATTERNS! Sound frequency visualization patterns!',
            'ai-generated-47': 'VORONOI TESSELLATION! Dynamic geometric diagram evolution!',
            'ai-generated-48': 'GALTON BOARD EVOLUTION! Advanced probability distributions!',
            'ai-generated-49': 'EMERGENCE FLOCKING! Individual balls create flocking behavior!',
            'ai-generated-50': 'HOLOGRAPHIC UNIVERSE! Holographic interference patterns!'
        }
        return descriptions.get(folder_name, f'{folder_name.upper()}! Unique ball physics concept!')
    
    def draw_background(self):
        """Draw animated background"""
        self.screen.fill(self.bg_color)
        
        # Draw animated gradient
        current_time = time.time()
        self.animation_time = current_time
        
        # Animated particles
        for i in range(15):
            t = current_time + i * 0.5
            x = (self.screen_width * 0.5) + (200 * pygame.math.Vector2(1, 0).rotate(t * 30 + i * 24).x)
            y = (self.screen_height * 0.5) + (150 * pygame.math.Vector2(0, 1).rotate(t * 20 + i * 36).y)
            
            # Keep particles on screen
            x = max(10, min(self.screen_width - 10, x))
            y = max(10, min(self.screen_height - 10, y))
            
            # Color animation
            hue = (t * 50 + i * 30) % 360
            color = pygame.Color(0)
            color.hsva = (hue, 40, 30, 100)
            
            pygame.draw.circle(self.screen, color, (int(x), int(y)), 3)
    
    def set_status_message(self, message, duration=3.0):
        """Set a temporary status message"""
        self.status_message = message
        self.status_timer = time.time() + duration
    
    def draw_header(self):
        """Draw the header section"""
        # Main title with glow effect
        title_text = "VIRAL VIDEO FACTORY"
        title_surface = self.title_font.render(title_text, True, self.title_color)
        title_rect = title_surface.get_rect(centerx=self.screen_width//2, y=30)
        
        # Glow effect
        glow_surface = self.title_font.render(title_text, True, (100, 50, 50))
        for offset in [(2, 2), (-2, -2), (2, -2), (-2, 2)]:
            glow_rect = title_rect.copy()
            glow_rect.x += offset[0]
            glow_rect.y += offset[1]
            self.screen.blit(glow_surface, glow_rect)
        
        self.screen.blit(title_surface, title_rect)
        
        # Subtitle
        subtitle_text = "Ball Physics Video Preview System"
        subtitle_surface = self.subtitle_font.render(subtitle_text, True, self.subtitle_color)
        subtitle_rect = subtitle_surface.get_rect(centerx=self.screen_width//2, y=85)
        self.screen.blit(subtitle_surface, subtitle_rect)
        
        # Video counter and status
        if self.video_folders:
            counter_text = f"Video {self.current_index + 1} of {len(self.video_folders)}"
            counter_surface = self.text_font.render(counter_text, True, self.highlight_color)
            counter_rect = counter_surface.get_rect(centerx=self.screen_width//2, y=125)
            self.screen.blit(counter_surface, counter_rect)
            
            # Status message
            if self.status_message and time.time() < self.status_timer:
                status_surface = self.small_font.render(self.status_message, True, self.accent_color)
                status_rect = status_surface.get_rect(centerx=self.screen_width//2, y=150)
                self.screen.blit(status_surface, status_rect)
        else:
            no_videos_surface = self.text_font.render("No video folders found!", True, self.warning_color)
            no_videos_rect = no_videos_surface.get_rect(centerx=self.screen_width//2, y=125)
            self.screen.blit(no_videos_surface, no_videos_rect)
    
    def draw_current_video_info(self):
        """Draw information about the current video"""
        if not self.video_folders:
            # Draw help message when no videos found
            help_rect = pygame.Rect(50, 200, self.screen_width - 100, 300)
            pygame.draw.rect(self.screen, self.card_color, help_rect, border_radius=15)
            
            help_lines = [
                "No video folders found!",
                "",
                "Make sure each folder contains:",
                "• main.py (entry point)",
                "• game.py (game logic)", 
                "• Ball.py (ball physics)",
                "",
                "Check the folder structure and try again."
            ]
            
            y_pos = 230
            for line in help_lines:
                color = self.warning_color if "No video" in line else self.text_color
                font = self.text_font if "No video" in line else self.small_font
                
                line_surface = font.render(line, True, color)
                line_rect = line_surface.get_rect(centerx=self.screen_width//2, y=y_pos)
                self.screen.blit(line_surface, line_rect)
                y_pos += 35 if "No video" in line else 25
            return
            
        video = self.video_folders[self.current_index]
        
        # Main video info card
        card_rect = pygame.Rect(50, 180, self.screen_width - 100, 250)
        pygame.draw.rect(self.screen, self.card_color, card_rect, border_radius=15)
        pygame.draw.rect(self.screen, self.highlight_color, card_rect, width=2, border_radius=15)
        
        # Video name
        name_text = video['name']
        if len(name_text) > 35:  # Truncate long names
            name_text = name_text[:32] + "..."
            
        name_surface = self.subtitle_font.render(name_text, True, self.highlight_color)
        name_rect = name_surface.get_rect(centerx=self.screen_width//2, y=210)
        self.screen.blit(name_surface, name_rect)
        
        # Description with better word wrapping
        description = video['description']
        words = description.split(' ')
        lines = []
        current_line = []
        max_width = self.screen_width - 140
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if self.text_font.size(test_line)[0] < max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))
        
        # Limit to 4 lines
        if len(lines) > 4:
            lines = lines[:3] + [lines[3][:50] + "..."]
        
        y_pos = 260
        for line in lines:
            line_surface = self.text_font.render(line, True, self.text_color)
            line_rect = line_surface.get_rect(centerx=self.screen_width//2, y=y_pos)
            self.screen.blit(line_surface, line_rect)
            y_pos += 30
        
        # Launch button visual
        button_rect = pygame.Rect(self.screen_width//2 - 100, 380, 200, 40)
        button_color = self.button_hover_color if self.is_mouse_over_rect(button_rect) else self.button_color
        pygame.draw.rect(self.screen, button_color, button_rect, border_radius=10)
        
        button_text = "PRESS SPACE TO LAUNCH"
        button_surface = self.small_font.render(button_text, True, self.text_color)
        button_text_rect = button_surface.get_rect(center=button_rect.center)
        self.screen.blit(button_surface, button_text_rect)
    
    def is_mouse_over_rect(self, rect):
        """Check if mouse is over a rectangle"""
        return rect.collidepoint(self.mouse_pos)
    
    def draw_controls(self):
        """Draw control instructions"""
        if not self.video_folders:
            return
            
        controls_rect = pygame.Rect(50, 450, self.screen_width - 100, 120)
        pygame.draw.rect(self.screen, self.card_color, controls_rect, border_radius=10)
        
        y_start = 470
        controls = [
            "CONTROLS",
            "LEFT/RIGHT Navigate    SPACE Launch    R Random    ESC Exit",
            "Numbers 1-9,0: Jump to video    ENTER Launch selected"
        ]
        
        for i, control in enumerate(controls):
            if i == 0:  # Title
                color = self.highlight_color
                font = self.text_font
            else:  # Controls
                color = self.text_color
                font = self.small_font
            
            control_surface = font.render(control, True, color)
            control_rect = control_surface.get_rect(centerx=self.screen_width//2, y=y_start + i * 25)
            self.screen.blit(control_surface, control_rect)
        
        # Tip
        tip_surface = self.tiny_font.render("TIP: Each video is optimized for viral engagement!", True, self.accent_color)
        tip_rect = tip_surface.get_rect(centerx=self.screen_width//2, y=y_start + 75)
        self.screen.blit(tip_surface, tip_rect)
    
    def draw_video_list(self):
        """Draw a scrollable list of all videos"""
        if not self.video_folders:
            return
            
        y_start = 590
        visible_videos = 6
        
        # Background for video list
        list_rect = pygame.Rect(50, y_start - 15, self.screen_width - 100, visible_videos * 30 + 30)
        pygame.draw.rect(self.screen, self.card_color, list_rect, border_radius=10)
        
        # Title
        title_surface = self.text_font.render("Video Library", True, self.highlight_color)
        title_rect = title_surface.get_rect(centerx=self.screen_width//2, y=y_start - 5)
        self.screen.blit(title_surface, title_rect)
        
        # Video list
        start_index = max(0, self.current_index - visible_videos // 2)
        end_index = min(len(self.video_folders), start_index + visible_videos)
        
        for i in range(start_index, end_index):
            y_pos = y_start + 25 + (i - start_index) * 30
            video = self.video_folders[i]
            
            # Highlight current video
            if i == self.current_index:
                highlight_rect = pygame.Rect(60, y_pos - 3, self.screen_width - 120, 26)
                pygame.draw.rect(self.screen, self.highlight_color, highlight_rect, border_radius=8)
                text_color = self.bg_color
                prefix = "▶"
            else:
                text_color = self.text_color
                prefix = " "
            
            # Video name with number
            text = f"{prefix} {i+1:2d}. {video['name']}"
            if len(text) > 60:  # Truncate very long names
                text = text[:57] + "..."
                
            text_surface = self.small_font.render(text, True, text_color)
            self.screen.blit(text_surface, (75, y_pos))
        
        # Scroll indicators
        if start_index > 0:
            up_surface = self.small_font.render("More above", True, self.accent_color)
            self.screen.blit(up_surface, (60, y_start + 20))
            
        if end_index < len(self.video_folders):
            down_surface = self.small_font.render("More below", True, self.accent_color)
            down_rect = down_surface.get_rect(right=self.screen_width - 60, y=y_start + visible_videos * 30)
            self.screen.blit(down_surface, down_rect)
    
    def launch_video(self, video_path):
        """Launch a specific video"""
        if self.current_process:
            try:
                self.current_process.terminate()
                self.current_process.wait(timeout=2)
            except:
                try:
                    self.current_process.kill()
                except:
                    pass
            self.current_process = None
        
        try:
            # Get the python executable path from venv
            python_exe = self.base_path / ".venv" / "Scripts" / "python.exe"
            if not python_exe.exists():
                # Fallback to system python
                python_exe = "python"
                
            main_py = video_path / "main.py"
            
            if not main_py.exists():
                self.set_status_message(f"❌ main.py not found in {video_path.name}", 5.0)
                return False
            
            print(f"Launching: {video_path.name}")
            self.set_status_message(f"Launching {video_path.name}...", 3.0)
            
            self.current_process = subprocess.Popen(
                [str(python_exe), str(main_py)],
                cwd=str(video_path),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0
            )
            return True
            
        except Exception as e:
            error_msg = f"Error launching video: {str(e)[:50]}"
            print(error_msg)
            self.set_status_message(error_msg, 5.0)
            return False
    
    def handle_input(self, event):
        """Handle user input"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            
            if not self.video_folders:
                return True
            
            if event.key == pygame.K_LEFT or event.key == pygame.K_UP:
                self.current_index = (self.current_index - 1) % len(self.video_folders)
                self.set_status_message(f"Selected: {self.video_folders[self.current_index]['name'][:30]}", 2.0)
            
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_DOWN:
                self.current_index = (self.current_index + 1) % len(self.video_folders)
                self.set_status_message(f"Selected: {self.video_folders[self.current_index]['name'][:30]}", 2.0)
            
            elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                if self.video_folders:
                    self.launch_video(self.video_folders[self.current_index]['path'])
            
            elif event.key == pygame.K_r:
                self.current_index = random.randint(0, len(self.video_folders) - 1)
                self.set_status_message(f"Random: {self.video_folders[self.current_index]['name'][:30]}", 2.0)
            
            elif event.key == pygame.K_h:
                self.show_help()
            
            # Number keys for direct selection
            elif event.key >= pygame.K_0 and event.key <= pygame.K_9:
                num = event.key - pygame.K_0
                if num == 0:
                    num = 10
                if 1 <= num <= len(self.video_folders):
                    self.current_index = num - 1
                    self.set_status_message(f"Jumped to #{num}: {self.video_folders[self.current_index]['name'][:25]}", 2.0)
            
            # Function keys for quick launch
            elif event.key >= pygame.K_F1 and event.key <= pygame.K_F12:
                f_num = event.key - pygame.K_F1
                if f_num < len(self.video_folders):
                    self.current_index = f_num
                    self.launch_video(self.video_folders[self.current_index]['path'])
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                self.handle_mouse_click(event.pos)
        
        return True
    
    def handle_mouse_click(self, pos):
        """Handle mouse clicks"""
        # Check if clicked on video list
        if not self.video_folders:
            return
            
        y_start = 615
        visible_videos = 6
        start_index = max(0, self.current_index - visible_videos // 2)
        end_index = min(len(self.video_folders), start_index + visible_videos)
        
        for i in range(start_index, end_index):
            y_pos = y_start + (i - start_index) * 30
            list_rect = pygame.Rect(60, y_pos - 3, self.screen_width - 120, 26)
            
            if list_rect.collidepoint(pos):
                self.current_index = i
                self.set_status_message(f"Clicked: {self.video_folders[i]['name'][:30]}", 2.0)
                break
    
    def show_help(self):
        """Show help message"""
        help_text = "HELP: Use LEFT/RIGHT to navigate, SPACE to launch, R for random, ESC to exit"
        self.set_status_message(help_text, 5.0)
    
    def run(self):
        """Main launcher loop"""
        clock = pygame.time.Clock()
        running = True
        
        print("Viral Video Factory Launcher Started!")
        if self.video_folders:
            print(f"Found {len(self.video_folders)} video concepts")
            print("Use arrow keys to navigate, SPACE to launch, ESC to exit")
            print("Press H for help, R for random video")
        else:
            print("No video folders found!")
            print("   Make sure each folder has a main.py file")
        
        try:
            while running:
                # Handle events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    else:
                        running = self.handle_input(event)
                
                # Update mouse position
                self.mouse_pos = pygame.mouse.get_pos()
                
                # Draw everything
                self.draw_background()
                self.draw_header()
                self.draw_current_video_info()
                self.draw_controls()
                self.draw_video_list()
                
                # Update display
                pygame.display.flip()
                clock.tick(60)
                
        except KeyboardInterrupt:
            print("\nLauncher interrupted by user")
        except Exception as e:
            print(f"Launcher error: {e}")
        finally:
            # Cleanup
            if self.current_process:
                try:
                    self.current_process.terminate()
                    self.current_process.wait(timeout=2)
                except:
                    try:
                        self.current_process.kill()
                    except:
                        pass
            
            pygame.quit()
            print("Video Factory Launcher closed. Happy content creating!")

if __name__ == "__main__":
    launcher = VideoPreviewLauncher()
    launcher.run()
