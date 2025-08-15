import tkinter as tk
from tkinter import ttk, messagebox
import os
import json
import sys
import winreg

class DesktopWidget:
    def __init__(self):
        print("Initializing Desktop Widget...")
        
        # Store default size
        self.default_width = 300
        self.default_height = 400
        
        # Define color scheme
        self.colors = {
            'bg_dark': '#1e1e1e',
            'bg_medium': '#2d2d2d',
            'bg_light': '#363636',
            'text_primary': '#ffffff',
            'text_secondary': '#cccccc',
            'accent': '#007acc',
            'success': '#28a745'
        }
        
        # Initialize state variables
        self.is_locked = False
        self.is_minimized = False
        self.is_resizable = False
        
        # Default themes
        self.themes = {
            'dark': {
                'bg_dark': '#1e1e1e',
                'bg_medium': '#2d2d2d',
                'bg_light': '#363636',
                'text_primary': '#ffffff',
                'text_secondary': '#cccccc',
                'accent': '#007acc',
                'success': '#28a745'
            },
            'light': {
                'bg_dark': '#f0f0f0',
                'bg_medium': '#e1e1e1',
                'bg_light': '#ffffff',
                'text_primary': '#000000',
                'text_secondary': '#666666',
                'accent': '#0066cc',
                'success': '#28a745'
            },
            'blue': {
                'bg_dark': '#1a1a2e',
                'bg_medium': '#16213e',
                'bg_light': '#0f3460',
                'text_primary': '#ffffff',
                'text_secondary': '#a8a8a8',
                'accent': '#e94560',
                'success': '#48bb78'
            }
        }
        
        # Set default theme
        self.current_theme = 'dark'
        self.colors = self.themes[self.current_theme]
        
        # Define file paths
        self.settings_file = os.path.join(os.path.expanduser('~'), '.smart_notes_settings.json')
        self.notes_file = os.path.join(os.path.expanduser('~'), '.smart_notes.txt')
        self.position_file = os.path.join(os.path.expanduser('~'), '.smart_notes_position.json')
        self.mini_position_file = os.path.join(os.path.expanduser('~'), '.smart_notes_mini_position.json')
        
        # Create the main window
        self.root = tk.Tk()
        self.root.title("Smart Notes")
        
        # Set window attributes
        self.root.overrideredirect(True)  # Remove window decorations
        self.root.attributes('-topmost', True)  # Keep window on top
        self.root.attributes('-alpha', 0.85)  # Set transparency
        self.root.geometry("300x400")  # Set initial size
        
        # Create UI components
        self.create_widget_ui()
        
        # Set window attributes
        self.root.overrideredirect(True)  # Remove window decorations
        self.root.attributes('-topmost', True)  # Keep window on top
        self.root.attributes('-alpha', 0.85)  # Set transparency
        
        # Set initial size and position
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width - self.default_width) / 2)
        y = int((screen_height - self.default_height) / 2)
        self.root.geometry(f"{self.default_width}x{self.default_height}+{x}+{y}")
        
        # Load settings and position
        self.load_settings()
        self.load_position()
        
        # Make widget draggable
        self.make_draggable()
        
        # Load saved notes
        self.load_notes()
        
        # Ensure proper window sizing
        self.root.update_idletasks()
        
        print("Widget initialization complete")
    
    def create_widget_ui(self):
        """Create the modern UI components"""
        # Main container with rounded corners
        main_frame = tk.Frame(self.root, bg=self.colors['bg_dark'])
        main_frame.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Modern header with gradient effect
        header_frame = tk.Canvas(main_frame, height=40, bg=self.colors['bg_medium'], highlightthickness=0)
        header_frame.pack(fill='x', padx=0, pady=0)
        
        # Create gradient effect
        header_frame.create_rectangle(0, 0, self.default_width, 40, fill=self.colors['bg_medium'], width=0)
        
        # Title with modern font
        title_label = tk.Label(header_frame, 
                              text="📝 Smart Notes", 
                              bg=self.colors['bg_medium'],
                              fg=self.colors['text_primary'], 
                              font=('Segoe UI', 12, 'bold'))
        header_frame.create_window(10, 20, window=title_label, anchor='w')
        
        # Control buttons container
        controls_frame = tk.Frame(header_frame, bg=self.colors['bg_medium'])
        header_frame.create_window(self.default_width - 10, 20, window=controls_frame, anchor='e')
        
        # Modern button style with hover effects
        button_style = {
            'bg': self.colors['bg_medium'],
            'activebackground': self.colors['bg_light'],
            'bd': 0,
            'padx': 8
        }
        
        # Close button
        close_btn = tk.Button(controls_frame,
                            text="×",
                            command=self.close_widget,
                            fg='#ff4444',
                            activeforeground='#ff6666',
                            font=('Segoe UI', 14, 'bold'),
                            **button_style)
        close_btn.pack(side='right', padx=2)
        
        # Lock button with color feedback
        self.lock_btn = tk.Button(controls_frame, 
                                text="🔓", 
                                command=self.toggle_lock,
                                fg=self.colors['text_primary'],
                                font=('Segoe UI', 11),
                                **button_style)
        self.lock_btn.pack(side='left', padx=2)
        
        # Settings button
        self.settings_btn = tk.Button(controls_frame, 
                                    text="⚙️", 
                                    command=self.show_settings,
                                    fg=self.colors['text_primary'],
                                    font=('Segoe UI', 11),
                                    **button_style)
        self.settings_btn.pack(side='left', padx=2)
        
        # Minimize button
        minimize_btn = tk.Button(controls_frame, 
                                text="−", 
                                command=self.minimize_widget,
                                fg=self.colors['text_secondary'],
                                font=('Segoe UI', 11),
                                **button_style)
        minimize_btn.pack(side='left', padx=2)
        
        # Notes area
        self.text = tk.Text(main_frame,
                           wrap="word",
                           bg=self.colors['bg_light'],
                           fg=self.colors['text_primary'],
                           insertbackground=self.colors['accent'],
                           font=('Segoe UI', 11),
                           bd=0,
                           padx=10,
                           pady=10)
        self.text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create modern custom scrollbar
        self.create_modern_scrollbar(main_frame)
        
        # Create resize handle in bottom-right corner
        self.create_resize_handle(main_frame)
    
    def toggle_lock(self):
        """Toggle widget lock state"""
        self.is_locked = not self.is_locked
        if self.is_locked:
            self.root.unbind("<Button-1>")
            self.root.unbind("<B1-Motion>")
            self.root.unbind("<Control-Button-1>")
            # Also lock minimize widget if it exists
            if hasattr(self, 'mini_window') and self.mini_window.winfo_exists():
                self.drag_handle.unbind("<Button-1>")
                self.drag_handle.unbind("<B1-Motion>")
                self.drag_handle.unbind("<ButtonRelease-1>")
            # Lock resize handle
            if hasattr(self, 'resize_canvas'):
                self.resize_canvas.unbind("<Button-1>")
                self.resize_canvas.unbind("<B1-Motion>")
                self.resize_canvas.unbind("<ButtonRelease-1>")
            self.lock_btn.configure(text="🔒", fg=self.colors['success'])
        else:
            self.make_draggable()
            self.enable_resize()
            # Also unlock minimize widget if it exists
            if hasattr(self, 'mini_window') and self.mini_window.winfo_exists():
                self.drag_handle.bind("<Button-1>", self.start_mini_move)
                self.drag_handle.bind("<B1-Motion>", self.on_mini_move)
                self.drag_handle.bind("<ButtonRelease-1>", self.stop_mini_move)
            # Unlock resize handle
            if hasattr(self, 'resize_canvas'):
                self.resize_canvas.bind("<Button-1>", self.start_resize)
                self.resize_canvas.bind("<B1-Motion>", self.on_resize)
                self.resize_canvas.bind("<ButtonRelease-1>", self.stop_resize)
            self.lock_btn.configure(text="🔓", fg=self.colors['text_primary'])
        self.save_settings()

    def create_resize_handle(self, parent):
        """Create a visual resize handle in the bottom-right corner"""
        # Create resize handle frame
        self.resize_handle = tk.Frame(parent, width=20, height=20, bg=self.colors['bg_dark'])
        self.resize_handle.pack(side='bottom', anchor='se', padx=0, pady=0)
        
        # Create canvas for the resize handle
        self.resize_canvas = tk.Canvas(self.resize_handle, 
                                     width=20, 
                                     height=20, 
                                     bg=self.colors['bg_dark'],
                                     highlightthickness=0)
        self.resize_canvas.pack()
        
        # Draw resize handle (corner triangle with dots)
        self.resize_canvas.create_polygon(0, 20, 20, 20, 20, 0, 
                                        fill=self.colors['accent'],
                                        outline=self.colors['text_primary'],
                                        width=1,
                                        tags="resize_handle")
        
        # Add dots to indicate resize functionality
        self.resize_canvas.create_oval(12, 12, 16, 16, 
                                     fill=self.colors['text_primary'],
                                     outline='',
                                     tags="resize_dots")
        self.resize_canvas.create_oval(8, 8, 12, 12, 
                                     fill=self.colors['text_primary'],
                                     outline='',
                                     tags="resize_dots")
        self.resize_canvas.create_oval(4, 4, 8, 8, 
                                     fill=self.colors['text_primary'],
                                     outline='',
                                     tags="resize_dots")
        
        # Add hover effects
        self.resize_canvas.bind("<Enter>", self.resize_handle_enter)
        self.resize_canvas.bind("<Leave>", self.resize_handle_leave)
        
        # Bind resize events to the handle
        if not self.is_locked:
            self.resize_canvas.bind("<Button-1>", self.start_resize)
            self.resize_canvas.bind("<B1-Motion>", self.on_resize)
            self.resize_canvas.bind("<ButtonRelease-1>", self.stop_resize)
        
        # Change cursor when hovering over resize handle
        self.resize_canvas.bind("<Enter>", lambda e: self.resize_canvas.configure(cursor="sizing"))
        self.resize_canvas.bind("<Leave>", lambda e: self.resize_canvas.configure(cursor=""))

    def resize_handle_enter(self, event):
        """Handle resize handle hover enter"""
        self.resize_canvas.configure(cursor="sizing")
        # Highlight the resize handle
        self.resize_canvas.itemconfig("resize_handle", fill=self.colors['success'])
        self.resize_canvas.itemconfig("resize_dots", fill=self.colors['bg_light'])

    def resize_handle_leave(self, event):
        """Handle resize handle hover leave"""
        self.resize_canvas.configure(cursor="")
        # Restore normal colors
        self.resize_canvas.itemconfig("resize_handle", fill=self.colors['accent'])
        self.resize_canvas.itemconfig("resize_dots", fill=self.colors['text_primary'])

    def create_modern_scrollbar(self, parent):
        """Create a modern, sleek scrollbar"""
        # Create scrollbar frame
        self.scrollbar_frame = tk.Frame(parent, width=12, bg=self.colors['bg_dark'])
        self.scrollbar_frame.pack(side='right', fill='y', padx=(0, 5))
        
        # Create scrollbar canvas
        self.scrollbar_canvas = tk.Canvas(self.scrollbar_frame, 
                                        width=12, 
                                        bg=self.colors['bg_dark'],
                                        highlightthickness=0,
                                        relief='flat')
        self.scrollbar_canvas.pack(fill='y', expand=True)
        
        # Create scrollbar track (background)
        self.scrollbar_canvas.create_rectangle(0, 0, 12, 400, 
                                             fill=self.colors['bg_medium'],
                                             outline='',
                                             width=0)
        
        # Create scrollbar thumb (the draggable part)
        self.scrollbar_thumb = self.scrollbar_canvas.create_rectangle(2, 0, 10, 50,
                                                                    fill=self.colors['accent'],
                                                                    outline='',
                                                                    width=0)
        
        # Bind scrollbar events
        self.scrollbar_canvas.bind("<Button-1>", self.scrollbar_click)
        self.scrollbar_canvas.bind("<B1-Motion>", self.scrollbar_drag)
        self.scrollbar_canvas.bind("<MouseWheel>", self.scrollbar_wheel)
        
        # Bind text widget to update scrollbar
        self.text.configure(yscrollcommand=self.update_scrollbar)
        
        # Configure text widget to use custom scrolling
        self.text.configure(yscrollcommand=self.update_scrollbar)
        
        # Initial scrollbar update
        self.update_scrollbar()

    def scrollbar_click(self, event):
        """Handle scrollbar click"""
        if not self.is_locked:
            # Get scrollbar position
            scrollbar_height = self.scrollbar_canvas.winfo_height()
            click_y = event.y
            
            # Calculate scroll position
            content_height = float(self.text.index('end-1c').split('.')[0])
            visible_height = self.text.winfo_height() // 20  # Approximate line height
            
            if content_height > visible_height:
                scroll_ratio = click_y / scrollbar_height
                target_line = int(scroll_ratio * content_height)
                self.text.yview_moveto(scroll_ratio)

    def scrollbar_drag(self, event):
        """Handle scrollbar drag"""
        if not self.is_locked:
            scrollbar_height = self.scrollbar_canvas.winfo_height()
            drag_y = max(0, min(event.y, scrollbar_height))
            
            scroll_ratio = drag_y / scrollbar_height
            self.text.yview_moveto(scroll_ratio)

    def scrollbar_wheel(self, event):
        """Handle mouse wheel scrolling"""
        if not self.is_locked:
            # Windows mouse wheel
            if event.delta:
                delta = -event.delta / 120
            else:
                # Linux mouse wheel
                delta = event.num
                if delta == 4:
                    delta = -1
                elif delta == 5:
                    delta = 1
                else:
                    delta = 0
            
            self.text.yview_scroll(int(delta), "units")

    def update_scrollbar(self, first=None, last=None):
        """Update scrollbar position and size"""
        try:
            # Get text widget scroll info
            first, last = self.text.yview()
            
            # Calculate scrollbar dimensions
            scrollbar_height = self.scrollbar_canvas.winfo_height()
            if scrollbar_height <= 0:
                return
            
            # Calculate thumb size and position
            content_ratio = last - first
            thumb_height = max(20, int(scrollbar_height * content_ratio))
            thumb_y = int(scrollbar_height * first)
            
            # Update thumb position and size
            self.scrollbar_canvas.coords(self.scrollbar_thumb, 
                                       2, thumb_y, 
                                       10, thumb_y + thumb_height)
            
            # Show/hide scrollbar based on content
            if content_ratio < 1.0:
                self.scrollbar_frame.pack(side='right', fill='y', padx=(0, 5))
            else:
                self.scrollbar_frame.pack_forget()
                
        except Exception as e:
            # Fallback to default scrollbar if custom one fails
            pass

    def enable_resize(self):
        """Enable resize functionality"""
        if hasattr(self, 'resize_canvas'):
            self.resize_canvas.bind("<Button-1>", self.start_resize)
            self.resize_canvas.bind("<B1-Motion>", self.on_resize)
            self.resize_canvas.bind("<ButtonRelease-1>", self.stop_resize)

    def start_resize(self, event):
        """Start resize operation"""
        if not self.is_locked:
            self.resize_x = event.x_root
            self.resize_y = event.y_root
            self.resize_w = self.root.winfo_width()
            self.resize_h = self.root.winfo_height()
            # Bind to root window for global mouse tracking
            self.root.bind("<B1-Motion>", self.on_resize)
            self.root.bind("<ButtonRelease-1>", self.stop_resize)

    def on_resize(self, event):
        """Handle resize operation"""
        if not self.is_locked:
            dx = event.x_root - self.resize_x
            dy = event.y_root - self.resize_y
            new_width = max(200, self.resize_w + dx)
            new_height = max(300, self.resize_h + dy)
            
            # Smooth resize with immediate visual feedback
            self.root.geometry(f"{new_width}x{new_height}")
            
            # Update resize handle position
            if hasattr(self, 'resize_handle'):
                self.resize_handle.pack_forget()
                self.resize_handle.pack(side='bottom', anchor='se', padx=0, pady=0)
            
            # Force update for smooth visual feedback
            self.root.update_idletasks()

    def stop_resize(self, event):
        """Stop resize operation"""
        self.root.unbind("<B1-Motion>")
        self.root.unbind("<ButtonRelease-1>")
        self.save_size()
        
        # Final update to ensure smooth completion
        self.root.update_idletasks()

    def save_size(self):
        """Save current window size"""
        with open(self.position_file, 'r+') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
            data['width'] = self.root.winfo_width()
            data['height'] = self.root.winfo_height()
            f.seek(0)
            json.dump(data, f)
            f.truncate()
    
    def save_mini_position(self):
        """Save minimize widget position"""
        if hasattr(self, 'mini_window') and self.mini_window.winfo_exists():
            try:
                with open(self.mini_position_file, 'w') as f:
                    data = {
                        'x': self.mini_window.winfo_x(),
                        'y': self.mini_window.winfo_y()
                    }
                    json.dump(data, f)
            except Exception as e:
                print(f"Could not save mini position: {e}")
    
    def load_mini_position(self):
        """Load minimize widget position or use default"""
        try:
            if os.path.exists(self.mini_position_file):
                with open(self.mini_position_file, 'r') as f:
                    data = json.load(f)
                    self.mini_x = data.get('x', 100)
                    self.mini_y = data.get('y', 100)
            else:
                # Default position (bottom right corner)
                screen_width = self.root.winfo_screenwidth()
                screen_height = self.root.winfo_screenheight()
                self.mini_x = screen_width - 80
                self.mini_y = screen_height - 100
        except Exception as e:
            print(f"Could not load mini position: {e}")
            # Fallback to default position
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            self.mini_x = screen_width - 80
            self.mini_y = screen_height - 100
    
    def minimize_widget(self):
        """Minimize the widget"""
        self.root.withdraw()
        self.is_minimized = True
        self.create_minimized_button()
    
    def create_minimized_button(self):
        """Create a modern floating circular button when minimized"""
        self.mini_window = tk.Toplevel()
        self.mini_window.overrideredirect(True)
        self.mini_window.attributes('-topmost', True)
        self.mini_window.attributes('-alpha', 0.9)

        # Create main frame with larger size to accommodate drag handle
        size = 50
        self.mini_frame = tk.Frame(self.mini_window, 
                                  width=size, 
                                  height=size, 
                                  bg=self.colors['bg_medium'])
        self.mini_frame.pack()

        # Create canvas for the main icon area
        icon_size = 40
        self.icon_canvas = tk.Canvas(self.mini_frame, 
                                    width=icon_size, 
                                    height=icon_size, 
                                    bg=self.colors['bg_medium'],
                                    highlightthickness=0)
        self.icon_canvas.place(x=5, y=5)  # Center the icon

        # Draw circular background
        self.icon_canvas.create_oval(2, 2, icon_size-2, icon_size-2, 
                                   fill=self.colors['bg_medium'],
                                   outline=self.colors['accent'],
                                   width=2)

        # Load and display the icon.png
        try:
            from PIL import Image, ImageTk
            # Look for icon in assets folder
            icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'icon.png')
            if os.path.exists(icon_path):
                # Load and resize icon
                icon_img = Image.open(icon_path)
                icon_img = icon_img.resize((24, 24), Image.Resampling.LANCZOS)
                self.icon_photo = ImageTk.PhotoImage(icon_img)
                # Place icon in center
                self.icon_canvas.create_image(icon_size//2, icon_size//2, 
                                            image=self.icon_photo)
            else:
                # Fallback to text icon
                self.icon_canvas.create_text(icon_size//2, icon_size//2,
                                           text="📝",
                                           font=("Segoe UI", 14),
                                           fill=self.colors['text_primary'])
        except ImportError:
            # PIL not available, use text icon
            self.icon_canvas.create_text(icon_size//2, icon_size//2,
                                       text="📝",
                                       font=("Segoe UI", 14),
                                       fill=self.colors['text_primary'])
        except Exception as e:
            print(f"Could not load icon: {e}")
            # Fallback to text icon
            self.icon_canvas.create_text(icon_size//2, icon_size//2,
                                       text="📝",
                                       font=("Segoe UI", 14),
                                       fill=self.colors['text_primary'])

        # Create drag handle in lower left corner (small triangle)
        self.drag_handle = tk.Canvas(self.mini_frame, 
                                    width=15, 
                                    height=15, 
                                    bg=self.colors['bg_medium'],
                                    highlightthickness=0)
        self.drag_handle.place(x=0, y=size-15)  # Position in lower left

        # Draw drag handle (small triangle)
        self.drag_handle.create_polygon(0, 15, 15, 15, 0, 0, 
                                      fill=self.colors['accent'],
                                      outline=self.colors['text_primary'],
                                      width=1)

        # Bind click to restore (only on the main icon area)
        self.icon_canvas.bind("<Button-1>", lambda e: self.restore_widget())
        
        # Bind drag functionality to the drag handle (only if not locked)
        if not self.is_locked:
            self.drag_handle.bind("<Button-1>", self.start_mini_move)
            self.drag_handle.bind("<B1-Motion>", self.on_mini_move)
            self.drag_handle.bind("<ButtonRelease-1>", self.stop_mini_move)
        
        # Set initial position - load saved position or use default
        self.load_mini_position()
        self.mini_window.geometry(f"{size}x{size}+{self.mini_x}+{self.mini_y}")

    def start_mini_move(self, event):
        """Start moving minimized button"""
        self.mini_x = event.x
        self.mini_y = event.y
        self.move_time = event.time

    def on_mini_move(self, event):
        """Handle minimized button movement"""
        if not self.is_locked:
            dx = event.x - self.mini_x
            dy = event.y - self.mini_y
            x = self.mini_window.winfo_x() + dx
            y = self.mini_window.winfo_y() + dy
            self.mini_window.geometry(f"+{x}+{y}")
            self.save_mini_position()

    def stop_mini_move(self, event):
        """Stop moving minimized button"""
        self.save_mini_position()
    
    def restore_widget(self):
        """Restore the widget from minimized state"""
        if hasattr(self, 'mini_window'):
            self.save_mini_position()  # Save position before destroying
            self.mini_window.destroy()
        self.root.deiconify()
        self.is_minimized = False
    
    def make_draggable(self):
        """Make the widget draggable and resizable"""
        if not self.is_locked:
            self.root.bind("<Button-1>", self.start_move)
            self.root.bind("<B1-Motion>", self.on_move)
            # Bind resize events
            self.root.bind("<Control-Button-1>", self.start_resize)
            self.root.bind("<Control-B1-Motion>", self.on_resize)
        
    def start_resize(self, event):
        """Start widget resizing"""
        if not self.is_locked:
            self.x = event.x
            self.y = event.y
            self.width = self.root.winfo_width()
            self.height = self.root.winfo_height()
    
    def on_resize(self, event):
        """Handle widget resizing"""
        if not self.is_locked:
            dx = event.x - self.x
            dy = event.y - self.y
            new_width = max(200, self.width + dx)
            new_height = max(300, self.height + dy)
            self.root.geometry(f"{new_width}x{new_height}")
            self.save_size()
    
    def save_size(self):
        """Save widget size"""
        try:
            size_data = {
                'width': self.root.winfo_width(),
                'height': self.root.winfo_height()
            }
            with open(self.position_file, 'r+') as f:
                data = json.load(f)
                data.update(size_data)
                f.seek(0)
                json.dump(data, f)
                f.truncate()
        except Exception as e:
            print(f"Could not save size: {e}")
    
    def close_widget(self):
        """Close the widget"""
        if messagebox.askyesno("Confirm Exit", "Are you sure you want to close Smart Notes?"):
            self.save_notes()
            self.save_position()
            self.save_settings()
            self.root.quit()
    
    def start_move(self, event):
        """Start widget movement"""
        if not self.is_locked:
            self.x = event.x
            self.y = event.y
    
    def on_move(self, event):
        """Handle widget movement"""
        if not self.is_locked:
            deltax = event.x - self.x
            deltay = event.y - self.y
            x = self.root.winfo_x() + deltax
            y = self.root.winfo_y() + deltay
            self.root.geometry(f"+{x}+{y}")
            self.save_position()
    
    def save_position(self):
        """Save widget position and size"""
        try:
            position_data = {
                'x': self.root.winfo_x(),
                'y': self.root.winfo_y(),
                'width': self.root.winfo_width(),
                'height': self.root.winfo_height(),
                'is_locked': self.is_locked,
                'is_minimized': self.is_minimized
            }
            with open(self.position_file, 'w') as f:
                json.dump(position_data, f)
        except Exception as e:
            print(f"Could not save position: {e}")
    
    def load_position(self):
        """Load saved widget position and size"""
        try:
            if os.path.exists(self.position_file):
                with open(self.position_file, 'r') as f:
                    position_data = json.load(f)
                
                # Load position
                x = position_data.get('x', 100)
                y = position_data.get('y', 100)
                
                # Load size
                width = position_data.get('width', self.default_width)
                height = position_data.get('height', self.default_height)
                
                # Apply geometry
                self.root.geometry(f"{width}x{height}+{x}+{y}")
                
                # Load state
                self.is_locked = position_data.get('is_locked', False)
                if position_data.get('is_minimized', False):
                    self.minimize_widget()
        except Exception as e:
            print(f"Could not load position: {e}")
            self.center_window()
    
    def save_settings(self):
        """Save widget settings"""
        try:
            settings = {
                'is_locked': self.is_locked,
                'auto_start': self.check_auto_start(),
                'theme': self.current_theme,
                'transparency': self.root.attributes('-alpha'),
                'width': self.root.winfo_width(),
                'height': self.root.winfo_height()
            }
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f)
        except Exception as e:
            print(f"Could not save settings: {e}")
    
    def load_settings(self):
        """Load widget settings"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                
                # Load theme
                theme = settings.get('theme', 'dark')
                if theme in self.themes:
                    self.current_theme = theme
                    self.colors = self.themes[theme]
                
                # Load window attributes
                self.root.attributes('-alpha', settings.get('transparency', 0.85))
                width = settings.get('width', self.default_width)
                height = settings.get('height', self.default_height)
                self.root.geometry(f"{width}x{height}")
                
                # Load state
                self.is_locked = settings.get('is_locked', False)
                
                # Apply theme
                self.apply_theme()
        except Exception as e:
            print(f"Could not load settings: {e}")
    
    def show_settings(self):
        """Show settings dialog"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x500")
        settings_window.configure(bg=self.colors['bg_dark'])
        
        # Theme section
        theme_frame = tk.LabelFrame(settings_window,
                                  text="Theme Options",
                                  bg=self.colors['bg_dark'],
                                  fg=self.colors['text_primary'])
        theme_frame.pack(fill='x', padx=10, pady=10)
        
        for theme in self.themes:
            btn = tk.Radiobutton(theme_frame,
                                text=theme.capitalize(),
                                value=theme,
                                variable=tk.StringVar(value=self.current_theme),
                                command=lambda t=theme: self.change_theme(t),
                                bg=self.colors['bg_dark'],
                                fg=self.colors['text_primary'],
                                selectcolor=self.colors['bg_medium'])
            btn.pack(pady=5)
        
        # Transparency section
        transparency_frame = tk.LabelFrame(settings_window,
                                         text="Transparency",
                                         bg=self.colors['bg_dark'],
                                         fg=self.colors['text_primary'])
        transparency_frame.pack(fill='x', padx=10, pady=10)
        
        transparency_scale = tk.Scale(transparency_frame,
                                     from_=0.3,
                                     to=1.0,
                                     resolution=0.05,
                                     orient='horizontal',
                                     command=self.change_transparency,
                                     bg=self.colors['bg_dark'],
                                     fg=self.colors['text_primary'])
        transparency_scale.set(self.root.attributes('-alpha'))
        transparency_scale.pack(fill='x', padx=10, pady=5)
        
        # Auto-start section
        auto_start_frame = tk.LabelFrame(settings_window,
                                       text="Startup Options",
                                       bg=self.colors['bg_dark'],
                                       fg=self.colors['text_primary'])
        auto_start_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(auto_start_frame,
                  text="Enable Auto-start",
                  command=self.enable_auto_start,
                  bg=self.colors['bg_medium'],
                  fg=self.colors['text_primary']).pack(pady=5)
        
        tk.Button(auto_start_frame,
                  text="Disable Auto-start",
                  command=self.disable_auto_start,
                  bg=self.colors['bg_medium'],
                  fg=self.colors['text_primary']).pack(pady=5)
    
    def change_theme(self, theme_name):
        """Change the widget theme"""
        self.current_theme = theme_name
        self.colors = self.themes[theme_name]
        self.apply_theme()
        self.save_settings()
    
    def apply_theme(self):
        """Apply the current theme to all widgets"""
        self.root.configure(bg=self.colors['bg_dark'])
        for widget in self.root.winfo_children():
            if isinstance(widget, (tk.Frame, tk.Label, tk.Button)):
                widget.configure(bg=self.colors['bg_medium'])
                if isinstance(widget, (tk.Label, tk.Button)):
                    widget.configure(fg=self.colors['text_primary'])
        if hasattr(self, 'text'):
            self.text.configure(
                bg=self.colors['bg_light'],
                fg=self.colors['text_primary'],
                insertbackground=self.colors['accent'])
    
    def change_transparency(self, value):
        """Change widget transparency"""
        self.root.attributes('-alpha', float(value))
        self.save_settings()
    
    def check_auto_start(self):
        """Check if auto-start is enabled"""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                r"Software\Microsoft\Windows\CurrentVersion\Run",
                                0, winreg.KEY_READ)
            try:
                winreg.QueryValueEx(key, "SmartNotes")
                return True
            except:
                return False
            finally:
                winreg.CloseKey(key)
        except:
            return False
    
    def enable_auto_start(self):
        """Enable auto-start"""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                r"Software\Microsoft\Windows\CurrentVersion\Run",
                                0, winreg.KEY_SET_VALUE)
            script_path = os.path.abspath(sys.argv[0])
            winreg.SetValueEx(key, "SmartNotes", 0, winreg.REG_SZ, f'"{sys.executable}" "{script_path}"')
            winreg.CloseKey(key)
            messagebox.showinfo("Success", "Auto-start enabled!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not enable auto-start: {e}")
    
    def disable_auto_start(self):
        """Disable auto-start"""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                r"Software\Microsoft\Windows\CurrentVersion\Run",
                                0, winreg.KEY_SET_VALUE)
            winreg.DeleteValue(key, "SmartNotes")
            winreg.CloseKey(key)
            messagebox.showinfo("Success", "Auto-start disabled!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not disable auto-start: {e}")
    
    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def save_notes(self):
        """Save notes content"""
        try:
            with open(self.notes_file, 'w', encoding='utf-8') as f:
                f.write(self.text.get('1.0', 'end-1c'))
        except Exception as e:
            print(f"Could not save notes: {e}")
    
    def load_notes(self):
        """Load saved notes"""
        try:
            if os.path.exists(self.notes_file):
                with open(self.notes_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                if hasattr(self, 'text'):
                    self.text.delete('1.0', 'end')
                    self.text.insert('1.0', content)
        except Exception as e:
            print(f"Could not load notes: {e}")
    
    def run(self):
        """Start the application"""
        print("Widget initialized, starting main loop...")
        
        # Print debug info
        print(f"Widget geometry: {self.root.winfo_width()}x{self.root.winfo_height()}+{self.root.winfo_x()}+{self.root.winfo_y()}")
        print(f"Widget visible: {self.root.winfo_viewable()}")
        
        # Auto-save notes periodically (every 30 seconds)
        def auto_save():
            self.save_notes()
            self.root.after(30000, auto_save)
        
        self.root.after(30000, auto_save)
        
        # Start the main event loop
        self.root.mainloop()

if __name__ == "__main__":
    print("Starting Desktop Widget...")
    widget = DesktopWidget()
    widget.run()
