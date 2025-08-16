import tkinter as tk
from tkinter import ttk, messagebox
import os
import json
import uuid
from datetime import datetime
import subprocess
import sys
import threading
import winreg

class InstanceController:
    def __init__(self):
        self.instances = {}
        self.controller_window = None
        self.item_to_instance_map = {}  # Map treeview items to instance IDs
        self.max_instances = 10  # Maximum number of instances allowed
        self.running_instances = set()  # Track running instances
        self.colors = {
            'bg_dark': '#1e1e1e',
            'bg_medium': '#2d2d2d',
            'bg_light': '#363636',
            'text_primary': '#ffffff',
            'text_secondary': '#cccccc',
            'accent': '#007acc',
            'success': '#28a745',
            'danger': '#dc3545'
        }
        
        # Load existing instances
        self.load_instances()
        
    def load_instances(self):
        """Load all existing instances from metadata files"""
        self.instances = {}
        home_dir = os.path.expanduser('~')
        
        try:
            # Scan for all metadata files
            for filename in os.listdir(home_dir):
                if filename.startswith('.smart_notes_') and filename.endswith('_metadata.json'):
                    try:
                        with open(os.path.join(home_dir, filename), 'r', encoding='utf-8') as f:
                            metadata = json.load(f)
                            instance_id = metadata.get('instance_id')
                            if instance_id:
                                self.instances[instance_id] = metadata
                    except Exception as e:
                        print(f"Error loading instance metadata {filename}: {e}")
        except Exception as e:
            print(f"Error scanning for instances: {e}")
    
    def create_instance(self):
        """Create a new instance"""
        try:
            # Check instance limit
            if len(self.instances) >= self.max_instances:
                messagebox.showwarning(
                    "Instance Limit Reached",
                    f"You can only create up to {self.max_instances} instances.\n"
                    "Please delete some instances before creating new ones."
                )
                return
            
            # Generate new instance ID
            instance_id = str(uuid.uuid4())
            
            # Create instance metadata
            instance_metadata = {
                'instance_id': instance_id,
                'name': f"New Instance {len(self.instances) + 1}",
                'created_date': datetime.now().isoformat(),
                'last_modified': datetime.now().isoformat(),
                'theme': 'dark',
                'files': {
                    'settings': f'~/.smart_notes_{instance_id}_settings.json',
                    'notes': f'~/.smart_notes_{instance_id}_notes.txt',
                    'position': f'~/.smart_notes_{instance_id}_position.json',
                    'mini_position': f'~/.smart_notes_{instance_id}_mini_position.json'
                }
            }
            
            # Save metadata
            metadata_file = os.path.join(os.path.expanduser('~'), f'.smart_notes_{instance_id}_metadata.json')
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(instance_metadata, f, indent=2)
            
            # Add to instances dict
            self.instances[instance_id] = instance_metadata
            
            # Enable auto-start for new instance
            self.enable_auto_start_for_instance(instance_id)
            
            # Launch new instance
            self.launch_instance(instance_id)
            
            # Refresh the controller UI
            if self.controller_window:
                self.refresh_instance_list()
                
            messagebox.showinfo("Success", f"New instance '{instance_metadata['name']}' created!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not create instance: {e}")
    
    def launch_instance(self, instance_id):
        """Launch an existing instance"""
        try:
            # Check if instance is already running
            if instance_id in self.running_instances:
                # Create popup above the controller window
                popup = tk.Toplevel(self.controller_window)
                popup.title("Instance Already Open")
                popup.geometry("400x150")
                popup.configure(bg=self.colors['bg_dark'])
                popup.attributes('-topmost', True)
                popup.transient(self.controller_window)
                popup.grab_set()
                
                # Position above the controller window
                popup.update_idletasks()
                controller_x = self.controller_window.winfo_rootx()
                controller_y = self.controller_window.winfo_rooty()
                x = controller_x + (self.controller_window.winfo_width() // 2) - 200
                y = controller_y - 170  # Above the controller
                
                # Ensure window is on screen
                if y < 0:
                    y = controller_y + 50  # Below if not enough space above
                
                popup.geometry(f"400x150+{x}+{y}")
                
                # Content
                main_frame = tk.Frame(popup, bg=self.colors['bg_dark'])
                main_frame.pack(fill='both', expand=True, padx=20, pady=20)
                
                # Icon and message
                icon_label = tk.Label(main_frame,
                                    text="ℹ️",
                                    bg=self.colors['bg_dark'],
                                    fg=self.colors['accent'],
                                    font=('Segoe UI', 24))
                icon_label.pack(pady=(0, 10))
                
                message_label = tk.Label(main_frame,
                                       text=f"Instance '{self.instances.get(instance_id, {}).get('name', 'Unknown')}' is already running.",
                                       bg=self.colors['bg_dark'],
                                       fg=self.colors['text_primary'],
                                       font=('Segoe UI', 10),
                                       wraplength=350)
                message_label.pack(pady=(0, 20))
                
                # OK button
                ok_button = tk.Button(main_frame,
                                    text="OK",
                                    command=popup.destroy,
                                    bg=self.colors['accent'],
                                    fg=self.colors['text_primary'],
                                    bd=0,
                                    padx=30)
                ok_button.pack()
                
                # Auto-close after 3 seconds
                popup.after(3000, popup.destroy)
                
                return
            
            # Add to running instances
            self.running_instances.add(instance_id)
            
            # Get the current script path
            script_path = os.path.join(os.path.dirname(__file__), 'sticky_notes_widget.py')
            
            # Launch the instance with the instance ID as argument
            process = subprocess.Popen([sys.executable, script_path, '--instance-id', instance_id])
            
            # Monitor process to remove from running instances when it closes
            def monitor_process():
                process.wait()
                if instance_id in self.running_instances:
                    self.running_instances.remove(instance_id)
                    # Check if controller window still exists before refreshing
                    if self.controller_window and self.controller_window.winfo_exists():
                        try:
                            self.refresh_instance_list()
                            self.update_status_labels()
                        except Exception as e:
                            print(f"Error refreshing UI after process close: {e}")
            
            # Start monitoring in background thread
            monitor_thread = threading.Thread(target=monitor_process, daemon=True)
            monitor_thread.start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not launch instance: {e}")
            if instance_id in self.running_instances:
                self.running_instances.remove(instance_id)
    
    def clone_instance(self, instance_id):
        """Clone an existing instance"""
        try:
            source_instance = self.instances.get(instance_id)
            if not source_instance:
                messagebox.showerror("Error", "Source instance not found!")
                return
            
            # Generate new instance ID
            new_instance_id = str(uuid.uuid4())
            
            # Create cloned metadata
            cloned_metadata = {
                'instance_id': new_instance_id,
                'name': f"{source_instance['name']} (Copy)",
                'created_date': datetime.now().isoformat(),
                'last_modified': datetime.now().isoformat(),
                'theme': source_instance.get('theme', 'dark'),
                'files': {
                    'settings': f'~/.smart_notes_{new_instance_id}_settings.json',
                    'notes': f'~/.smart_notes_{new_instance_id}_notes.txt',
                    'position': f'~/.smart_notes_{new_instance_id}_position.json',
                    'mini_position': f'~/.smart_notes_{new_instance_id}_mini_position.json'
                }
            }
            
            # Copy notes content if source exists
            source_notes_file = os.path.expanduser(source_instance['files']['notes'])
            if os.path.exists(source_notes_file):
                try:
                    with open(source_notes_file, 'r', encoding='utf-8') as f:
                        notes_content = f.read()
                    
                    # Save to new instance
                    new_notes_file = os.path.expanduser(cloned_metadata['files']['notes'])
                    with open(new_notes_file, 'w', encoding='utf-8') as f:
                        f.write(notes_content)
                except Exception as e:
                    print(f"Could not copy notes content: {e}")
            
            # Save cloned metadata
            metadata_file = os.path.join(os.path.expanduser('~'), f'.smart_notes_{new_instance_id}_metadata.json')
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(cloned_metadata, f, indent=2)
            
            # Add to instances dict
            self.instances[new_instance_id] = cloned_metadata
            
            # Enable auto-start for cloned instance
            self.enable_auto_start_for_instance(new_instance_id)
            
            # Refresh the controller UI
            if self.controller_window:
                self.refresh_instance_list()
                self.update_status_labels()
                
            messagebox.showinfo("Success", f"Instance cloned as '{cloned_metadata['name']}'!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not clone instance: {e}")
    
    def delete_instance(self, instance_id):
        """Delete an instance and all its files"""
        try:
            instance = self.instances.get(instance_id)
            if not instance:
                messagebox.showerror("Error", "Instance not found!")
                return
            
            # Check if instance is running
            if instance_id in self.running_instances:
                messagebox.showwarning(
                    "Cannot Delete Running Instance",
                    f"Cannot delete '{instance['name']}' while it's running.\n"
                    "Please close the instance first, then try deleting again."
                )
                return
            
            # Create custom delete confirmation dialog
            confirm_window = tk.Toplevel(self.controller_window)
            confirm_window.title("Confirm Deletion")
            confirm_window.geometry("500x300")  # Increased height from 200 to 300
            confirm_window.configure(bg=self.colors['bg_dark'])
            confirm_window.attributes('-topmost', True)
            confirm_window.transient(self.controller_window)
            confirm_window.grab_set()
            
            # Position above the controller window
            confirm_window.update_idletasks()
            controller_x = self.controller_window.winfo_rootx()
            controller_y = self.controller_window.winfo_rooty()
            x = controller_x + (self.controller_window.winfo_width() // 2) - 250
            y = controller_y - 320  # Adjusted for new height
            
            # Ensure window is on screen
            if y < 0:
                y = controller_y + 50  # Below if not enough space above
            
            confirm_window.geometry(f"500x300+{x}+{y}")
            
            # Content
            main_frame = tk.Frame(confirm_window, bg=self.colors['bg_dark'])
            main_frame.pack(fill='both', expand=True, padx=20, pady=30)  # Increased vertical padding
            
            # Icon and message
            icon_label = tk.Label(main_frame,
                                text="⚠️",
                                bg=self.colors['bg_dark'],
                                fg='#ffa500',
                                font=('Segoe UI', 32))  # Made icon bigger
            icon_label.pack(pady=(0, 20))  # Increased spacing
            
            message_label = tk.Label(main_frame,
                                   text=f"Are you sure you want to delete '{instance['name']}'?\n\n"
                                        "This will permanently delete all notes, settings, and data.\n"
                                        "This action cannot be undone!",
                                   bg=self.colors['bg_dark'],
                                   fg=self.colors['text_primary'],
                                   font=('Segoe UI', 12),  # Made text bigger
                                   wraplength=450)
            message_label.pack(pady=(0, 30))  # Increased spacing
            
            # Buttons frame
            button_frame = tk.Frame(main_frame, bg=self.colors['bg_dark'])
            button_frame.pack(fill='x')
            
            def confirm_delete():
                confirm_window.destroy()
                self.perform_delete(instance_id, instance)
            
            def cancel_delete():
                confirm_window.destroy()
            
            # Cancel button (left side)
            cancel_btn = tk.Button(button_frame,
                                 text="Cancel",
                                 command=cancel_delete,
                                 bg=self.colors['bg_medium'],
                                 fg=self.colors['text_primary'],
                                 font=('Segoe UI', 11),  # Made text bigger
                                 bd=0,
                                 padx=25,  # Increased padding
                                 pady=8)   # Increased padding
            cancel_btn.pack(side='left')
            
            # Delete button (right side)
            delete_btn = tk.Button(button_frame,
                                 text="🗑️ Delete Permanently",
                                 command=confirm_delete,
                                 bg=self.colors['danger'],
                                 fg=self.colors['text_primary'],
                                 font=('Segoe UI', 11, 'bold'),  # Made text bigger
                                 bd=0,
                                 padx=25,  # Increased padding
                                 pady=8)   # Increased padding
            delete_btn.pack(side='right')
            
            # Bind Escape key to cancel
            confirm_window.bind('<Escape>', lambda e: cancel_delete())
            
            # Focus on cancel button for safety
            cancel_btn.focus()
            
            return  # Exit early, deletion will be handled by confirm_delete
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete instance: {e}")
    
    def rename_instance(self, instance_id, new_name):
        """Rename an instance"""
        try:
            instance = self.instances.get(instance_id)
            if not instance:
                messagebox.showerror("Error", "Instance not found!")
                return False
            
            if not new_name or not new_name.strip():
                messagebox.showerror("Error", "Please enter a valid name!")
                return False
            
            # Update instance name
            old_name = instance['name']
            instance['name'] = new_name.strip()
            instance['last_modified'] = datetime.now().isoformat()
            
            # Save updated metadata
            metadata_file = os.path.join(os.path.expanduser('~'), f'.smart_notes_{instance_id}_metadata.json')
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(instance, f, indent=2)
            
            # Refresh the controller UI
            if self.controller_window:
                self.refresh_instance_list()
                
            messagebox.showinfo("Success", f"Instance renamed from '{old_name}' to '{new_name}'!")
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not rename instance: {e}")
            return False
    
    def rename_instance_in_controller(self, instance_id, new_name):
        """Rename an instance from the controller"""
        try:
            instance = self.instances.get(instance_id)
            if not instance:
                messagebox.showerror("Error", "Instance not found!")
                return False
            
            if not new_name or not new_name.strip():
                messagebox.showerror("Error", "Please enter a valid name!")
                return False
            
            # Update instance name
            old_name = instance['name']
            instance['name'] = new_name.strip()
            instance['last_modified'] = datetime.now().isoformat()
            
            # Save updated metadata
            metadata_file = os.path.join(os.path.expanduser('~'), f'.smart_notes_{instance_id}_metadata.json')
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(instance, f, indent=2)
            
            # Refresh the controller UI
            if self.controller_window:
                self.refresh_instance_list()
                
            messagebox.showinfo("Success", f"Instance renamed from '{old_name}' to '{new_name}'!")
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not rename instance: {e}")
            return False
    
    def show_controller(self):
        """Show the instance controller window"""
        if self.controller_window and self.controller_window.winfo_exists():
            self.controller_window.lift()
            self.controller_window.focus_force()
            return
        
        # Create controller window
        self.controller_window = tk.Toplevel()
        self.controller_window.title("Instance Controller")
        self.controller_window.geometry("800x700")  # Made wider and taller
        self.controller_window.configure(bg=self.colors['bg_dark'])
        self.controller_window.attributes('-topmost', True)
        
        # Make it resizable
        self.controller_window.resizable(True, True)
        
        # Create UI
        self.create_controller_ui()
        
        # Load instances
        self.load_instances()
        self.refresh_instance_list()
        self.update_status_labels()
        
        # Center window
        self.center_window()
    
    def create_controller_ui(self):
        """Create the controller UI"""
        # Main container
        main_frame = tk.Frame(self.controller_window, bg=self.colors['bg_dark'])
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Header
        header_frame = tk.Frame(main_frame, bg=self.colors['bg_dark'])
        header_frame.pack(fill='x', pady=(0, 10))
        
        title_label = tk.Label(header_frame,
                              text="📝 Instance Controller",
                              bg=self.colors['bg_dark'],
                              fg=self.colors['text_primary'],
                              font=('Segoe UI', 16, 'bold'))
        title_label.pack(side='left')
        
        # New Instance button
        new_btn = tk.Button(header_frame,
                           text="+ New Instance",
                           command=self.create_instance,
                           bg=self.colors['accent'],
                           fg=self.colors['text_primary'],
                           font=('Segoe UI', 10, 'bold'),
                           bd=0,
                           padx=20,
                           pady=5)
        new_btn.pack(side='right')
        
        # Instances list frame
        list_frame = tk.LabelFrame(main_frame,
                                 text="Instances",
                                 bg=self.colors['bg_dark'],
                                 fg=self.colors['text_primary'])
        list_frame.pack(fill='both', expand=True)
        
        # Create scrollable frame for instances
        self.canvas = tk.Canvas(list_frame, bg=self.colors['bg_light'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.colors['bg_light'])
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Configure canvas to expand with content
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        # Pack canvas and scrollbar
        self.canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Status bar
        status_frame = tk.Frame(main_frame, bg=self.colors['bg_medium'])
        status_frame.pack(fill='x', pady=(10, 0))
        
        self.status_label = tk.Label(status_frame,
                                    text="Ready",
                                    bg=self.colors['bg_medium'],
                                    fg=self.colors['text_secondary'],
                                    font=('Segoe UI', 9))
        self.status_label.pack(side='left', padx=5, pady=2)
        
        # Instance count and limit
        self.count_label = tk.Label(status_frame,
                                   text="",
                                   bg=self.colors['bg_medium'],
                                   fg=self.colors['text_secondary'],
                                   font=('Segoe UI', 9))
        self.count_label.pack(side='left', padx=20, pady=2)
        
        # Refresh button
        refresh_btn = tk.Button(status_frame,
                               text="🔄 Refresh",
                               command=self.refresh_instances,
                               bg=self.colors['bg_medium'],
                               fg=self.colors['text_primary'],
                               bd=0,
                               padx=10)
        refresh_btn.pack(side='right', padx=5, pady=2)

    def refresh_instance_list(self):
        """Refresh the instances list in the UI"""
        # Clear existing widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Add instances to the scrollable frame
        for instance_id, instance in self.instances.items():
            self.create_instance_row(instance_id, instance)
        
        # Update status labels
        self.update_status_labels()
    
    def create_instance_row(self, instance_id, instance):
        """Create a row for an instance with action buttons"""
        # Create row frame
        row_frame = tk.Frame(self.scrollable_frame, bg=self.colors['bg_light'], relief='flat', bd=1)
        row_frame.pack(fill='x', padx=5, pady=2)
        
        # Instance name (left side)
        name_frame = tk.Frame(row_frame, bg=self.colors['bg_light'])
        name_frame.pack(side='left', fill='y', padx=(10, 0))
        
        name_label = tk.Label(name_frame,
                             text=instance.get('name', 'Unnamed'),
                             bg=self.colors['bg_light'],
                             fg=self.colors['text_primary'],
                             font=('Segoe UI', 11, 'bold'),
                             anchor='w')
        name_label.pack(anchor='w')
        
        # Instance ID (small text below name)
        id_label = tk.Label(name_frame,
                           text=f"ID: {instance_id[:8]}...",
                           bg=self.colors['bg_light'],
                           fg=self.colors['text_secondary'],
                           font=('Segoe UI', 8),
                           anchor='w')
        id_label.pack(anchor='w')
        
        # Dates frame (center)
        dates_frame = tk.Frame(row_frame, bg=self.colors['bg_light'])
        dates_frame.pack(side='left', fill='y', padx=(20, 0))
        
        # Created date
        created_date = instance.get('created_date', '')[:10] if instance.get('created_date') else 'Unknown'
        created_label = tk.Label(dates_frame,
                               text=f"Created: {created_date}",
                               bg=self.colors['bg_light'],
                               fg=self.colors['text_secondary'],
                               font=('Segoe UI', 9),
                               anchor='w')
        created_label.pack(anchor='w')
        
        # Last modified date
        last_modified = instance.get('last_modified', '')[:10] if instance.get('last_modified') else 'Unknown'
        modified_label = tk.Label(dates_frame,
                                 text=f"Modified: {last_modified}",
                                 bg=self.colors['bg_light'],
                                 fg=self.colors['text_secondary'],
                                 font=('Segoe UI', 9),
                                 anchor='w')
        modified_label.pack(anchor='w')
        
        # Status frame (center-right)
        status_frame = tk.Frame(row_frame, bg=self.colors['bg_light'])
        status_frame.pack(side='left', fill='y', padx=(20, 0))
        
        # Check if instance is running
        is_running = instance_id in self.running_instances
        status_text = "🟢 Running" if is_running else "⚪ Stopped"
        status_color = self.colors['success'] if is_running else self.colors['text_secondary']
        
        status_label = tk.Label(status_frame,
                               text=status_text,
                               bg=self.colors['bg_light'],
                               fg=status_color,
                               font=('Segoe UI', 10, 'bold'),
                               anchor='w')
        status_label.pack(anchor='w')
        
        # Actions frame (right side)
        actions_frame = tk.Frame(row_frame, bg=self.colors['bg_light'])
        actions_frame.pack(side='right', fill='y', padx=(0, 10))
        
        # Button style
        button_style = {
            'font': ('Segoe UI', 12),  # Made text bigger
            'bd': 0,
            'width': 8,  # Made buttons much wider to show all text
            'height': 2,  # Made buttons taller
            'relief': 'flat',
            'cursor': 'hand2'  # Add hand cursor
        }
        
        # Open button
        open_btn = tk.Button(actions_frame,
                           text="📖 Open",
                           command=lambda: self.launch_instance(instance_id),
                           bg=self.colors['accent'],
                           fg=self.colors['text_primary'],
                           **button_style)
        open_btn.pack(side='left', padx=3)
        
        # Rename button
        rename_btn = tk.Button(actions_frame,
                             text="✏️ Rename",
                             command=lambda: self.show_rename_dialog(instance_id),
                             bg=self.colors['success'],
                             fg=self.colors['text_primary'],
                             **button_style)
        rename_btn.pack(side='left', padx=3)
        
        # Clone button
        clone_btn = tk.Button(actions_frame,
                            text="📋 Clone",
                            command=lambda: self.clone_instance(instance_id),
                            bg=self.colors['accent'],
                            fg=self.colors['text_primary'],
                            **button_style)
        clone_btn.pack(side='left', padx=3)
        
        # Delete button
        delete_btn = tk.Button(actions_frame,
                             text="🗑️ Delete",
                             command=lambda: self.delete_instance(instance_id),
                             bg=self.colors['danger'],
                             fg=self.colors['text_primary'],
                             **button_style)
        delete_btn.pack(side='left', padx=3)
        
        # Add separator line
        separator = tk.Frame(row_frame, height=1, bg=self.colors['bg_medium'])
        separator.pack(fill='x', pady=(5, 0))
    
    def refresh_instances(self):
        """Refresh instances from disk"""
        self.load_instances()
        self.refresh_instance_list()
        self.update_status_labels()
    
    def update_status_labels(self):
        """Update status and count labels"""
        total_instances = len(self.instances)
        running_count = len(self.running_instances)
        
        self.status_label.config(text=f"Ready - {running_count} running")
        self.count_label.config(text=f"Instances: {total_instances}/{self.max_instances}")
        
        # Color coding for count
        if total_instances >= self.max_instances:
            self.count_label.config(fg=self.colors['danger'])
        elif total_instances >= self.max_instances * 0.8:
            self.count_label.config(fg='#ffa500')  # Orange
        else:
            self.count_label.config(fg=self.colors['text_secondary'])
    
    def on_instance_double_click(self, event):
        """Handle double-click on instance to open it"""
        # This method is no longer needed with the new UI
        pass
    
    def show_context_menu(self, event):
        """Show context menu for instance actions"""
        # This method is no longer needed with the new UI
        pass

    def enable_auto_start_for_instance(self, instance_id):
        """Enable auto-start for a specific instance"""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                r"Software\Microsoft\Windows\CurrentVersion\Run",
                                0, winreg.KEY_SET_VALUE)
            
            # Create auto-start entry with instance ID
            script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'sticky_notes_widget.py'))
            auto_start_value = f'"{sys.executable}" "{script_path}" --instance-id {instance_id}'
            winreg.SetValueEx(key, f"SmartNotes_{instance_id[:8]}", 0, winreg.REG_SZ, auto_start_value)
            winreg.CloseKey(key)
            
        except Exception as e:
            print(f"Could not enable auto-start for instance {instance_id}: {e}")
    
    def center_window(self):
        """Center the controller window on screen"""
        self.controller_window.update_idletasks()
        width = self.controller_window.winfo_width()
        height = self.controller_window.winfo_height()
        x = (self.controller_window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.controller_window.winfo_screenheight() // 2) - (height // 2)
        self.controller_window.geometry(f"{width}x{height}+{x}+{y}")

    def show_rename_dialog(self, instance_id):
        """Show dialog to rename an instance"""
        instance = self.instances.get(instance_id)
        if not instance:
            return
        
        # Create rename dialog
        rename_window = tk.Toplevel(self.controller_window)
        rename_window.title("Rename Instance")
        rename_window.geometry("400x150")
        rename_window.configure(bg=self.colors['bg_dark'])
        rename_window.attributes('-topmost', True)
        rename_window.transient(self.controller_window)
        rename_window.grab_set()
        
        # Position above the controller window
        rename_window.update_idletasks()
        controller_x = self.controller_window.winfo_rootx()
        controller_y = self.controller_window.winfo_rooty()
        x = controller_x + (self.controller_window.winfo_width() // 2) - 200
        y = controller_y - 170  # Above the controller
        
        # Ensure window is on screen
        if y < 0:
            y = controller_y + 50  # Below if not enough space above
        
        rename_window.geometry(f"400x150+{x}+{y}")
        
        # Content
        main_frame = tk.Frame(rename_window, bg=self.colors['bg_dark'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Current name label
        tk.Label(main_frame,
                text=f"Current name: {instance['name']}",
                bg=self.colors['bg_dark'],
                fg=self.colors['text_secondary'],
                font=('Segoe UI', 10)).pack(anchor='w', pady=(0, 10))
        
        # New name entry
        name_frame = tk.Frame(main_frame, bg=self.colors['bg_dark'])
        name_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(name_frame,
                text="New name:",
                bg=self.colors['bg_dark'],
                fg=self.colors['text_primary']).pack(side='left')
        
        name_entry = tk.Entry(name_frame,
                             bg=self.colors['bg_light'],
                             fg=self.colors['text_primary'],
                             insertbackground=self.colors['accent'])
        name_entry.insert(0, instance['name'])
        name_entry.pack(side='right', fill='x', expand=True, padx=(10, 0))
        name_entry.focus()
        name_entry.select_range(0, tk.END)
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg=self.colors['bg_dark'])
        button_frame.pack(fill='x')
        
        def rename_action():
            new_name = name_entry.get().strip()
            if self.rename_instance_in_controller(instance_id, new_name):
                rename_window.destroy()
        
        def cancel_action():
            rename_window.destroy()
        
        tk.Button(button_frame,
                  text="Rename",
                  command=rename_action,
                  bg=self.colors['accent'],
                  fg=self.colors['text_primary'],
                  bd=0,
                  padx=20).pack(side='right', padx=(10, 0))
        
        tk.Button(button_frame,
                  text="Cancel",
                  command=cancel_action,
                  bg=self.colors['bg_medium'],
                  fg=self.colors['text_primary'],
                  bd=0,
                  padx=20).pack(side='right')
        
        # Bind Enter key to rename
        rename_window.bind('<Return>', lambda e: rename_action())
        rename_window.bind('<Escape>', lambda e: cancel_action())

    def perform_delete(self, instance_id, instance):
        """Actually perform the deletion after confirmation"""
        try:
            # Remove auto-start entry
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                    r"Software\Microsoft\Windows\CurrentVersion\Run",
                                    0, winreg.KEY_SET_VALUE)
                winreg.DeleteValue(key, f"SmartNotes_{instance_id[:8]}")
                winreg.CloseKey(key)
            except Exception as e:
                print(f"Could not remove auto-start entry: {e}")
            
            # Delete all instance files
            home_dir = os.path.expanduser('~')
            files_to_delete = [
                f'.smart_notes_{instance_id}_metadata.json',
                f'.smart_notes_{instance_id}_settings.json',
                f'.smart_notes_{instance_id}_notes.txt',
                f'.smart_notes_{instance_id}_position.json',
                f'.smart_notes_{instance_id}_mini_position.json'
            ]
            
            for filename in files_to_delete:
                file_path = os.path.join(home_dir, filename)
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                    except Exception as e:
                        print(f"Could not delete {filename}: {e}")
            
            # Remove from instances dict
            del self.instances[instance_id]
            
            # Refresh the controller UI
            if self.controller_window:
                self.refresh_instance_list()
                self.update_status_labels()
                
            messagebox.showinfo("Success", f"Instance '{instance['name']}' deleted successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete instance: {e}")

if __name__ == "__main__":
    controller = InstanceController()
    controller.show_controller()
    controller.controller_window.mainloop() 