#!/usr/bin/env python3
"""
===========================================================================
🤖 AI OS - MACOS STYLE
===========================================================================
"""

import os
import sys
import time
import json
import random
import threading
import subprocess
from datetime import datetime
from pathlib import Path

# GUI Libraries (install: pip install tkinter pillow)
try:
    import tkinter as tk
    from tkinter import ttk, scrolledtext, messagebox, filedialog
    import PIL.Image, PIL.ImageTk
    GUI_OK = True
except:
    GUI_OK = False
    print("⚠ GUI libraries not available")
    print("  Run: pip install pillow")
    print("  (tkinter comes with Python)")

# Voice
try:
    from gtts import gTTS
    import tempfile
    VOICE_OK = True
except:
    VOICE_OK = False

class AIOS:
    def __init__(self):
        self.name = "AI OS"
        self.version = "1.0"
        self.build = "2025.02"
        self.boot_time = datetime.now()
        self.running = True
        
        # Users
        self.users = {
            "admin": {"password": "admin", "home": "/Users/admin", "level": "root"},
            "guest": {"password": "", "home": "/Users/guest", "level": "guest"}
        }
        self.current_user = "guest"
        
        # Apps
        self.apps = {
            "finder": FinderApp,
            "terminal": TerminalApp,
            "notes": NotesApp,
            "calculator": CalculatorApp,
            "weather": WeatherApp,
            "ai": AIAssistantApp,
            "settings": SettingsApp
        }
        self.running_apps = []
        
        # Desktop
        self.desktop_files = []
        self.wallpaper = None
        
        # Start GUI if available
        if GUI_OK:
            self.start_gui()
        else:
            self.start_cli()
    
    def start_gui(self):
        """Start GUI mode"""
        self.root = tk.Tk()
        self.root.title(f"{self.name} - {self.current_user}")
        self.root.geometry("1280x720")
        self.root.configure(bg='#1e1e1e')
        
        # Menu bar (like macOS)
        self.create_menu()
        
        # Desktop icons area
        self.create_desktop()
        
        # Dock (like macOS)
        self.create_dock()
        
        # Menu bar (top)
        self.create_topbar()
        
        self.root.mainloop()
    
    def create_menu(self):
        """Create macOS style menu"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Apple menu
        apple_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="🍎", menu=apple_menu)
        apple_menu.add_command(label=f"About {self.name}", command=self.about)
        apple_menu.add_separator()
        apple_menu.add_command(label="System Settings...", command=self.settings)
        apple_menu.add_separator()
        apple_menu.add_command(label="Sleep", command=self.sleep)
        apple_menu.add_command(label="Restart...", command=self.restart)
        apple_menu.add_command(label="Shut Down...", command=self.shutdown)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Finder Window", command=self.new_finder)
        file_menu.add_command(label="New Folder", command=self.new_folder)
        file_menu.add_separator()
        file_menu.add_command(label="Open...", command=self.open_file)
        file_menu.add_command(label="Close Window", command=self.close_window)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", accelerator="Cmd+Z")
        edit_menu.add_command(label="Redo", accelerator="Cmd+Shift+Z")
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", accelerator="Cmd+X")
        edit_menu.add_command(label="Copy", accelerator="Cmd+C")
        edit_menu.add_command(label="Paste", accelerator="Cmd+V")
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="as Icons", command=lambda: self.view_mode("icons"))
        view_menu.add_command(label="as List", command=lambda: self.view_mode("list"))
        view_menu.add_command(label="as Columns", command=lambda: self.view_mode("columns"))
        view_menu.add_separator()
        view_menu.add_command(label="Show View Options", command=self.view_options)
        
        # Go menu
        go_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Go", menu=go_menu)
        go_menu.add_command(label="Home", command=self.go_home)
        go_menu.add_command(label="Documents", command=self.go_documents)
        go_menu.add_command(label="Downloads", command=self.go_downloads)
        go_menu.add_separator()
        go_menu.add_command(label="Applications", command=self.go_applications)
        go_menu.add_command(label="Utilities", command=self.go_utilities)
        
        # Window menu
        window_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Window", menu=window_menu)
        window_menu.add_command(label="Minimize", accelerator="Cmd+M")
        window_menu.add_command(label="Zoom", accelerator="Cmd+Option+Z")
        window_menu.add_separator()
        window_menu.add_command(label="Bring All to Front")
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label=f"{self.name} Help", command=self.help)
        help_menu.add_command(label="Keyboard Shortcuts", command=self.shortcuts)
    
    def create_topbar(self):
        """Create macOS style top bar"""
        topbar = tk.Frame(self.root, bg='#2d2d2d', height=25)
        topbar.pack(fill='x', side='top')
        topbar.pack_propagate(False)
        
        # Left side - Apple menu is already in menubar
        
        # Center - App name
        app_name = tk.Label(topbar, text="Finder", bg='#2d2d2d', fg='white', font=('Helvetica', 12))
        app_name.pack(side='left', padx=10)
        
        # Right side - Status items
        status_frame = tk.Frame(topbar, bg='#2d2d2d')
        status_frame.pack(side='right', padx=10)
        
        # Time
        self.time_label = tk.Label(status_frame, text="", bg='#2d2d2d', fg='white')
        self.time_label.pack(side='left', padx=5)
        self.update_time()
        
        # Battery/WiFi icons (placeholder)
        tk.Label(status_frame, text="🔋 100%", bg='#2d2d2d', fg='white').pack(side='left', padx=5)
        tk.Label(status_frame, text="📶", bg='#2d2d2d', fg='white').pack(side='left', padx=5)
    
    def update_time(self):
        """Update clock"""
        current = datetime.now().strftime("%I:%M %p")
        self.time_label.config(text=current)
        self.root.after(1000, self.update_time)
    
    def create_desktop(self):
        """Create desktop area"""
        self.desktop = tk.Frame(self.root, bg='#1e1e1e')
        self.desktop.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Desktop icons grid
        self.icon_frame = tk.Frame(self.desktop, bg='#1e1e1e')
        self.icon_frame.pack(anchor='nw')
        
        # Sample icons
        icons = [
            ("📁", "Documents", self.open_documents),
            ("📁", "Downloads", self.open_downloads),
            ("📁", "Applications", self.open_applications),
            ("🗑️", "Trash", self.open_trash),
            ("💻", "Terminal", lambda: self.launch_app("terminal")),
            ("🤖", "AI Assistant", lambda: self.launch_app("ai")),
            ("📝", "Notes", lambda: self.launch_app("notes")),
            ("🧮", "Calculator", lambda: self.launch_app("calculator")),
        ]
        
        row, col = 0, 0
        for icon, label, command in icons:
            self.create_desktop_icon(icon, label, command, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1
    
    def create_desktop_icon(self, icon, label, command, row, col):
        """Create a desktop icon"""
        frame = tk.Frame(self.icon_frame, bg='#1e1e1e', width=80, height=80)
        frame.grid(row=row, column=col, padx=10, pady=10)
        frame.pack_propagate(False)
        
        btn = tk.Button(frame, text=icon, font=('Helvetica', 30), 
                       bg='#1e1e1e', fg='white', bd=0,
                       command=command)
        btn.pack(expand=True)
        
        lbl = tk.Label(frame, text=label, bg='#1e1e1e', fg='white', font=('Helvetica', 10))
        lbl.pack()
    
    def create_dock(self):
        """Create macOS style dock"""
        dock = tk.Frame(self.root, bg='#2d2d2d', height=80)
        dock.pack(fill='x', side='bottom')
        dock.pack_propagate(False)
        
        # Dock icons
        dock_icons = [
            ("📁", "Finder", self.new_finder),
            ("💻", "Terminal", lambda: self.launch_app("terminal")),
            ("🤖", "AI", lambda: self.launch_app("ai")),
            ("📝", "Notes", lambda: self.launch_app("notes")),
            ("🧮", "Calc", lambda: self.launch_app("calculator")),
            ("🌤️", "Weather", lambda: self.launch_app("weather")),
            ("⚙️", "Settings", lambda: self.launch_app("settings")),
            ("🗑️", "Trash", self.open_trash),
        ]
        
        for icon, label, command in dock_icons:
            self.create_dock_icon(dock, icon, label, command)
    
    def create_dock_icon(self, parent, icon, label, command):
        """Create a dock icon"""
        frame = tk.Frame(parent, bg='#2d2d2d')
        frame.pack(side='left', padx=5, pady=10)
        
        btn = tk.Button(frame, text=icon, font=('Helvetica', 25),
                       bg='#3d3d3d', fg='white', bd=0,
                       command=command, width=2)
        btn.pack()
        
        lbl = tk.Label(frame, text=label, bg='#2d2d2d', fg='#aaaaaa', font=('Helvetica', 8))
        lbl.pack()
    
    def launch_app(self, app_name):
        """Launch an application"""
        if app_name in self.apps:
            app_window = tk.Toplevel(self.root)
            app_window.title(app_name.capitalize())
            app_window.geometry("800x600")
            self.apps[app_name](app_window)
            self.running_apps.append(app_name)
    
    def start_cli(self):
        """Start CLI mode if GUI not available"""
        print("\n" + "="*60)
        print(f"  {self.name} v{self.version} - CLI Mode")
        print("="*60)
        print("\nType 'help' for commands")
        print("Type 'gui' to install GUI dependencies")
        print("-"*60)
        
        while self.running:
            try:
                cmd = input(f"\n{self.current_user}@aios:~$ ").strip().lower()
                
                if cmd == 'exit':
                    self.shutdown()
                    break
                elif cmd == 'help':
                    self.cli_help()
                elif cmd == 'gui':
                    print("\n📦 Installing GUI dependencies...")
                    os.system('pip install pillow')
                    print("\nRestart with GUI mode")
                elif cmd == 'time':
                    print(f"\n{datetime.now().strftime('%I:%M %p')}")
                elif cmd == 'date':
                    print(f"\n{datetime.now().strftime('%B %d, %Y')}")
                elif cmd == 'whoami':
                    print(f"\n{self.current_user}")
                elif cmd == 'sysinfo':
                    self.cli_sysinfo()
                else:
                    print(f"\nUnknown command: {cmd}")
                    
            except KeyboardInterrupt:
                print("\n\nUse 'exit' to shutdown")
    
    def cli_help(self):
        """CLI help"""
        print("""
╔════════════════════════════════════════════════════════════════╗
║                    AI OS CLI COMMANDS                          ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  time     - Show current time                                 ║
║  date     - Show today's date                                 ║
║  whoami   - Current user                                      ║
║  sysinfo  - System information                                ║
║  gui      - Install GUI mode                                  ║
║  exit     - Shutdown                                          ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
        """)
    
    def cli_sysinfo(self):
        """CLI system info"""
        uptime = datetime.now() - self.boot_time
        print(f"\n{'='*40}")
        print(f" OS: {self.name} v{self.version}")
        print(f" Build: {self.build}")
        print(f" Uptime: {str(uptime).split('.')[0]}")
        print(f" User: {self.current_user}")
        print(f" GUI: {'Available' if GUI_OK else 'Not installed'}")
        print(f" Voice: {'Enabled' if VOICE_OK else 'Disabled'}")
        print(f"{'='*40}")
    
    # App classes
    class FinderApp:
        def __init__(self, window):
            self.window = window
            self.window.configure(bg='white')
            text = scrolledtext.ScrolledText(window, wrap=tk.WORD)
            text.pack(fill='both', expand=True)
            text.insert('1.0', "Finder - Browse your files")
    
    class TerminalApp:
        def __init__(self, window):
            self.window = window
            self.window.configure(bg='black')
            text = scrolledtext.ScrolledText(window, bg='black', fg='green', insertbackground='green')
            text.pack(fill='both', expand=True)
            text.insert('1.0', "Terminal v1.0\n$ ")
    
    class NotesApp:
        def __init__(self, window):
            self.window = window
            self.window.configure(bg='white')
            text = scrolledtext.ScrolledText(window)
            text.pack(fill='both', expand=True)
    
    class CalculatorApp:
        def __init__(self, window):
            self.window = window
            self.window.geometry("300x400")
            self.window.configure(bg='#2d2d2d')
            
            display = tk.Entry(window, font=('Helvetica', 20), justify='right')
            display.pack(fill='x', padx=10, pady=10)
            
            buttons = [
                ['7','8','9','/'],
                ['4','5','6','*'],
                ['1','2','3','-'],
                ['0','.','=','+']
            ]
            
            for row in buttons:
                frame = tk.Frame(window, bg='#2d2d2d')
                frame.pack(fill='x')
                for btn in row:
                    b = tk.Button(frame, text=btn, font=('Helvetica', 15),
                                 width=5, height=2)
                    b.pack(side='left', padx=2, pady=2)
    
    class WeatherApp:
        def __init__(self, window):
            self.window = window
            self.window.geometry("400x300")
            self.window.configure(bg='#87CEEB')
            label = tk.Label(window, text="☀️ 72°F", font=('Helvetica', 40), bg='#87CEEB')
            label.pack(expand=True)
    
    class AIAssistantApp:
        def __init__(self, window):
            self.window = window
            self.window.geometry("600x400")
            self.window.configure(bg='#1e1e1e')
            
            chat = scrolledtext.ScrolledText(window, bg='#2d2d2d', fg='white')
            chat.pack(fill='both', expand=True, padx=10, pady=10)
            
            entry = tk.Entry(window, bg='#3d3d3d', fg='white')
            entry.pack(fill='x', padx=10, pady=10)
    
    class SettingsApp:
        def __init__(self, window):
            self.window = window
            self.window.geometry("600x400")
            self.window.configure(bg='white')
            label = tk.Label(window, text="System Settings", font=('Helvetica', 20))
            label.pack(pady=20)
    
    # System functions
    def about(self):
        messagebox.showinfo(f"About {self.name}", 
                           f"{self.name} v{self.version}\n"
                           f"Build {self.build}\n"
                           f"© 2025 AI Systems")
    
    def settings(self):
        self.launch_app("settings")
    
    def sleep(self):
        self.root.iconify()
    
    def restart(self):
        if messagebox.askyesno("Restart", "Are you sure you want to restart?"):
            self.root.destroy()
            self.__init__()
    
    def shutdown(self):
        if messagebox.askyesno("Shut Down", "Are you sure you want to shut down?"):
            self.root.quit()
            sys.exit(0)
    
    def new_finder(self):
        self.launch_app("finder")
    
    def new_folder(self):
        print("New folder")
    
    def open_file(self):
        filename = filedialog.askopenfilename()
        if filename:
            messagebox.showinfo("Open", f"Opening {filename}")
    
    def close_window(self):
        self.root.quit()
    
    def view_mode(self, mode):
        print(f"View mode: {mode}")
    
    def view_options(self):
        messagebox.showinfo("View Options", "View options coming soon")
    
    def go_home(self):
        print("Go home")
    
    def go_documents(self):
        print("Go documents")
    
    def go_downloads(self):
        print("Go downloads")
    
    def go_applications(self):
        print("Go applications")
    
    def go_utilities(self):
        print("Go utilities")
    
    def help(self):
        messagebox.showinfo("Help", "AI OS Help System\n\nType 'help' in terminal for commands")
    
    def shortcuts(self):
        messagebox.showinfo("Keyboard Shortcuts", 
                           "Cmd+C - Copy\n"
                           "Cmd+V - Paste\n"
                           "Cmd+X - Cut\n"
                           "Cmd+Z - Undo\n"
                           "Cmd+M - Minimize")
    
    def open_documents(self):
        self.launch_app("finder")
    
    def open_downloads(self):
        self.launch_app("finder")
    
    def open_applications(self):
        self.launch_app("finder")
    
    def open_trash(self):
        messagebox.showinfo("Trash", "Trash is empty")

# ===== MAIN =====
if __name__ == "__main__":
    os.system('clear' if os.name == 'posix' else 'cls')
    
    if not GUI_OK:
        print("\n📦 To install GUI support:")
        print("  pip install pillow")
        print("  (tkinter comes with Python)\n")
    
