#!/usr/bin/env python3
"""
Standalone Instance Manager for Smart Notes Widget
This manager can remain open independently of sticky note instances
"""

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
from auto_start_registry import AutoStartRegistry

class StandaloneInstanceManager:
    def __init__(self):
        self.instances = {}
        self.controller_window = None
        self.item_to_instance_map = {}  # Map treeview items to instance IDs
        self.max_instances = 10  # Maximum number of instances allowed
        self.running_instances = set()  # Track running instances
        self.auto_start_registry = AutoStartRegistry()  # Auto-start registry manager
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
        
        # Create the main window
        self.create_main_window()
        
    def create_main_window(self):
        """Create the main instance manager window"""
        self.controller_window = tk.Tk()
        self.controller_window.title("Smart Notes Instance Manager")
        self.controller_window.geometry("800x600")
        self.controller_window.configure(bg=self.colors['bg_dark'])
        
        # Make window stay on top
        self.controller_window.attributes('-topmost', True)
        
        # Create UI
        self.create_ui()
        
        # Center the window
        self.center_window()
        
        # Bind window close event
        self.controller_window.protocol("WM_DELETE_WINDOW", self.on_window_close)
        
    def create_ui(self):
        """Create the user interface"""
        # Main container
        main_frame = tk.Frame(self.controller_window, bg=self.colors['bg_dark'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame,
                              text="Smart Notes Instance Manager",
                              bg=self.colors['bg_dark'],
                              fg=self.colors['text_primary'],
                              font=('Segoe UI', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Control buttons frame
        control_frame = tk.Frame(main_frame, bg=self.colors['bg_dark'])
        control_frame.pack(fill='x', pady=(0, 20))
        
        # Create new instance button
        create_btn = tk.Button(control_frame,
                              text="Create New Instance",
                              command=self.create_instance,
                              bg=self.colors['accent'],
                              fg=self.colors['text_primary'],
                              bd=0,
                              padx=20,
                              pady=10,
                              font=('Segoe UI', 10, 'bold'))
        create_btn.pack(side='left', padx=(0, 10))
        
        # Enable/Disable global auto-start button
        self.auto_start_btn = tk.Button(control_frame,
                                       text="Enable Global Auto-Start",
                                       command=self.toggle_global_auto_start,
                                       bg=self.colors['success'],
                                       fg=self.colors['text_primary'],
                                       bd=0,
                                       padx=20,
                                       pady=10,
                                       font=('Segoe UI', 10, 'bold'))
        self.auto_start_btn.pack(side='left', padx=(0, 10))
        
        # Refresh button
        refresh_btn = tk.Button(control_frame,
                               text="Refresh List",
                               command=self.refresh_instance_list,
                               bg=self.colors['bg_medium'],
                               fg=self.colors['text_primary'],
                               bd=0,
                               padx=20,
                               pady=10,
                               font=('Segoe UI', 10))
        refresh_btn.pack(side='left', padx=(0, 10))
        
        # Update auto-start button text
        self.update_auto_start_button_text()
        
        # Instance list frame
        list_frame = tk.Frame(main_frame, bg=self.colors['bg_dark'])
        list_frame.pack(fill='both', expand=True)
        
        # Create Treeview with checkboxes
        columns = ('checkbox', 'name', 'status', 'created', 'last_modified', 'auto_start')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        self.tree.heading('checkbox', text='Auto-Start')
        self.tree.heading('name', text='Instance Name')
        self.tree.heading('status', text='Status')
        self.tree.heading('created', text='Created')
        self.tree.heading('last_modified', text='Last Modified')
        self.tree.heading('auto_start', text='Auto-Start Status')
        
        # Set column widths
        self.tree.column('checkbox', width=80, anchor='center')
        self.tree.column('name', width=150, anchor='w')
        self.tree.column('status', width=100, anchor='center')
        self.tree.column('created', width=100, anchor='center')
        self.tree.column('last_modified', width=120, anchor='center')
        self.tree.column('auto_start', width=120, anchor='center')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Bind double-click event
        self.tree.bind('<Double-1>', self.on_instance_double_click)
        
        # Action buttons frame
        action_frame = tk.Frame(main_frame, bg=self.colors['bg_dark'])
        action_frame.pack(fill='x', pady=(20, 0))
        
        # Launch instance button
        launch_btn = tk.Button(action_frame,
                              text="Launch Instance",
                              command=self.launch_selected_instance,
                              bg=self.colors['accent'],
                              fg=self.colors['text_primary'],
                              bd=0,
                              padx=20,
                              pady=10,
                              font=('Segoe UI', 10))
        launch_btn.pack(side='left', padx=(0, 10))
        
        # Rename instance button
        rename_btn = tk.Button(action_frame,
                              text="Rename Instance",
                              command=self.rename_selected_instance,
                              bg=self.colors['bg_medium'],
                              fg=self.colors['text_primary'],
                              bd=0,
                              padx=20,
                              pady=10,
                              font=('Segoe UI', 10))
        rename_btn.pack(side='left', padx=(0, 10))
        
        # Enable Auto-Start button
        enable_auto_start_btn = tk.Button(action_frame,
                                         text="Enable Auto-Start",
                                         command=self.enable_auto_start_selected_instance,
                                         bg=self.colors['success'],
                                         fg=self.colors['text_primary'],
                                         bd=0,
                                         padx=20,
                                         pady=10,
                                         font=('Segoe UI', 10))
        enable_auto_start_btn.pack(side='left', padx=(0, 10))
        
        # Disable Auto-Start button
        disable_auto_start_btn = tk.Button(action_frame,
                                          text="Disable Auto-Start",
                                          command=self.disable_auto_start_selected_instance,
                                          bg=self.colors['danger'],
                                          fg=self.colors['text_primary'],
                                          bd=0,
                                          padx=20,
                                          pady=10,
                                          font=('Segoe UI', 10))
        disable_auto_start_btn.pack(side='left', padx=(0, 10))
        
        # Delete instance button
        delete_btn = tk.Button(action_frame,
                              text="Delete Instance",
                              command=self.delete_selected_instance,
                              bg=self.colors['danger'],
                              fg=self.colors['text_primary'],
                              bd=0,
                              padx=20,
                              pady=10,
                              font=('Segoe UI', 10))
        delete_btn.pack(side='left', padx=(0, 10))
        
        # Status bar
        self.status_label = tk.Label(main_frame,
                                    text="Ready",
                                    bg=self.colors['bg_dark'],
                                    fg=self.colors['text_secondary'],
                                    font=('Segoe UI', 9))
        self.status_label.pack(side='bottom', anchor='w')
        
        # Populate the tree
        self.refresh_instance_list()
        
    def load_instances(self):
        """Load all existing instances from metadata files and auto-start registry"""
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
        
        # Also load instances from auto-start registry (in case metadata files are missing)
        try:
            auto_start_instances = self.auto_start_registry.get_auto_start_instances()
            for instance_id, metadata in auto_start_instances.items():
                if instance_id not in self.instances:
                    # Add auto-start instance even if metadata file is missing
                    print(f"Loading auto-start instance from registry: {metadata.get('name', instance_id)}")
                    self.instances[instance_id] = metadata
        except Exception as e:
            print(f"Error loading auto-start instances: {e}")
    
    def refresh_instance_list(self):
        """Refresh the instance list display"""
        print("🔄 Refreshing instance list...")
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Reload instances
        self.load_instances()
        
        # Populate tree
        for instance_id, metadata in self.instances.items():
            # Check if instance is running
            status = "Running" if instance_id in self.running_instances else "Stopped"
            
            # Check auto-start status
            auto_start_enabled = self.check_instance_auto_start(instance_id)
            auto_start_text = "Enabled" if auto_start_enabled else "Disabled"
            
            print(f"  Instance: {metadata.get('name', 'Unknown')} - Auto-start: {auto_start_text}")
            
            # Create item
            item = self.tree.insert('', 'end', values=(
                "☑" if auto_start_enabled else "☐",
                metadata.get('name', 'Unknown'),
                status,
                metadata.get('created_date', '')[:10] if metadata.get('created_date') else '',
                metadata.get('last_modified', '')[:10] if metadata.get('last_modified') else '',
                auto_start_text
            ))
            
            # Store mapping
            self.item_to_instance_map[item] = instance_id
        
        # Update status
        self.update_status()
        print(f"✅ Refresh complete. Auto-start count: {self.auto_start_registry.get_auto_start_count()}")
    
    def check_instance_auto_start(self, instance_id):
        """Check if auto-start is enabled for a specific instance"""
        return self.auto_start_registry.is_auto_start_enabled(instance_id)
    
    def toggle_instance_auto_start(self, instance_id):
        """Toggle auto-start for a specific instance"""
        try:
            if self.auto_start_registry.is_auto_start_enabled(instance_id):
                # Remove from auto-start
                success = self.auto_start_registry.remove_instance(instance_id)
                if success:
                    print(f"Auto-start disabled for instance {instance_id}")
                    return True
            else:
                # Add to auto-start
                instance_metadata = self.instances.get(instance_id, {})
                success = self.auto_start_registry.add_instance(instance_id, instance_metadata)
                if success:
                    print(f"Auto-start enabled for instance {instance_id}")
                    return True
        except Exception as e:
            print(f"Error toggling auto-start for instance {instance_id}: {e}")
        return False
    
    def enable_auto_start_selected_instance(self):
        """Enable auto-start for the selected instance"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Instance Selected", "Please select an instance first.")
            return
        
        # Get the instance ID from the selected item
        item_values = self.tree.item(selected_item[0])['values']
        instance_name = item_values[1]  # Instance name is in the second column
        
        # Find the instance ID by name
        instance_id = None
        for inst_id, metadata in self.instances.items():
            if metadata.get('name') == instance_name:
                instance_id = inst_id
                break
        
        if not instance_id:
            messagebox.showerror("Error", "Could not find the selected instance.")
            return
        
        # Check if auto-start is already enabled
        if self.auto_start_registry.is_auto_start_enabled(instance_id):
            messagebox.showinfo("Auto-Start Already Enabled", 
                              f"Auto-start is already enabled for '{instance_name}'.")
            return
        
        # Enable auto-start using the new registry
        try:
            print(f"🔧 Enabling auto-start for instance: {instance_id}")
            instance_metadata = self.instances.get(instance_id, {})
            success = self.auto_start_registry.add_instance(instance_id, instance_metadata)
            
            if success:
                print(f"✅ Auto-start enabled successfully for {instance_name}")
                # Refresh the display immediately
                self.refresh_instance_list()
                messagebox.showinfo("Success", f"Auto-start enabled for '{instance_name}'!")
            else:
                print(f"❌ Failed to enable auto-start for {instance_name}")
                messagebox.showerror("Error", "Could not enable auto-start.")
            
        except Exception as e:
            print(f"❌ Error enabling auto-start: {e}")
            messagebox.showerror("Error", f"Could not enable auto-start: {e}")
    
    def disable_auto_start_selected_instance(self):
        """Disable auto-start for the selected instance"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Instance Selected", "Please select an instance first.")
            return
        
        # Get the instance ID from the selected item
        item_values = self.tree.item(selected_item[0])['values']
        instance_name = item_values[1]  # Instance name is in the second column
        
        # Find the instance ID by name
        instance_id = None
        for inst_id, metadata in self.instances.items():
            if metadata.get('name') == instance_name:
                instance_id = inst_id
                break
        
        if not instance_id:
            messagebox.showerror("Error", "Could not find the selected instance.")
            return
        
        # Check if auto-start is already disabled
        if not self.auto_start_registry.is_auto_start_enabled(instance_id):
            messagebox.showinfo("Auto-Start Already Disabled", 
                              f"Auto-start is already disabled for '{instance_name}'.")
            return
        
        # Disable auto-start using the new registry
        try:
            success = self.auto_start_registry.remove_instance(instance_id)
            
            if success:
                # Refresh the display immediately
                self.refresh_instance_list()
                messagebox.showinfo("Success", f"Auto-start disabled for '{instance_name}'!")
            else:
                messagebox.showerror("Error", "Could not disable auto-start.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not disable auto-start: {e}")
    
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
                'auto_start': False,  # Default to disabled
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
            
            # Update instance registry
            self.update_instance_registry(instance_id, instance_metadata)
            
            # Refresh the display
            self.refresh_instance_list()
            
            messagebox.showinfo("Success", f"New instance '{instance_metadata['name']}' created!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not create instance: {e}")
    
    def update_instance_registry(self, instance_id, metadata):
        """Update the instance registry"""
        try:
            registry_file = os.path.join(os.path.expanduser('~'), '.smart_notes_instance_registry.json')
            
            if os.path.exists(registry_file):
                with open(registry_file, 'r') as f:
                    registry = json.load(f)
            else:
                registry = {}
            
            # Add/update instance
            registry[instance_id] = metadata
            
            # Save registry
            with open(registry_file, 'w') as f:
                json.dump(registry, f, indent=2)
                
        except Exception as e:
            print(f"Error updating instance registry: {e}")
    
    def launch_instance(self, instance_id):
        """Launch an existing instance"""
        try:
            # Check if instance is already running
            if instance_id in self.running_instances:
                messagebox.showinfo("Info", f"Instance '{self.instances.get(instance_id, {}).get('name', 'Unknown')}' is already running.")
                return
            
            # Add to running instances
            self.running_instances.add(instance_id)
            
            # Get the current script path
            script_path = os.path.join(os.path.dirname(__file__), 'other files', 'src', 'sticky_notes_widget.py')
            
            # Launch the instance with the instance ID as argument
            process = subprocess.Popen([sys.executable, script_path, '--instance-id', instance_id])
            
            # Monitor process to remove from running instances when it closes
            def monitor_process():
                process.wait()
                if instance_id in self.running_instances:
                    self.running_instances.remove(instance_id)
                    # Update display
                    self.controller_window.after(0, self.refresh_instance_list)
            
            monitor_thread = threading.Thread(target=monitor_process, daemon=True)
            monitor_thread.start()
            
            # Update display
            self.refresh_instance_list()
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not launch instance: {e}")
            if instance_id in self.running_instances:
                self.running_instances.remove(instance_id)
    
    def launch_selected_instance(self):
        """Launch the selected instance"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an instance to launch.")
            return
        
        item = selection[0]
        instance_id = self.item_to_instance_map.get(item)
        if instance_id:
            self.launch_instance(instance_id)
    
    def rename_selected_instance(self):
        """Rename the selected instance"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an instance to rename.")
            return
        
        item = selection[0]
        instance_id = self.item_to_instance_map.get(item)
        if instance_id:
            self.show_rename_dialog(instance_id)
    
    def delete_selected_instance(self):
        """Delete the selected instance"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an instance to delete.")
            return
        
        item = selection[0]
        instance_id = self.item_to_instance_map.get(item)
        if instance_id:
            self.delete_instance(instance_id)
    
    def delete_instance(self, instance_id):
        """Delete an instance"""
        instance = self.instances.get(instance_id)
        if not instance:
            return
        
        # Confirm deletion
        if not messagebox.askyesno("Confirm Delete", 
                                  f"Are you sure you want to delete instance '{instance['name']}'?\n\n"
                                  "This will permanently remove the instance and all its data."):
            return
        
        try:
            # Remove from running instances
            if instance_id in self.running_instances:
                self.running_instances.remove(instance_id)
            
            # Remove metadata file
            metadata_file = os.path.join(os.path.expanduser('~'), f'.smart_notes_{instance_id}_metadata.json')
            if os.path.exists(metadata_file):
                os.remove(metadata_file)
            
            # Remove from instances dict
            if instance_id in self.instances:
                del self.instances[instance_id]
            
            # Update instance registry
            self.remove_from_instance_registry(instance_id)
            
            # Refresh display
            self.refresh_instance_list()
            
            messagebox.showinfo("Success", f"Instance '{instance['name']}' deleted successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete instance: {e}")
    
    def remove_from_instance_registry(self, instance_id):
        """Remove instance from the registry"""
        try:
            registry_file = os.path.join(os.path.expanduser('~'), '.smart_notes_instance_registry.json')
            
            if os.path.exists(registry_file):
                with open(registry_file, 'r') as f:
                    registry = json.load(f)
                
                if instance_id in registry:
                    del registry[instance_id]
                    
                    # Save updated registry
                    with open(registry_file, 'w') as f:
                        json.dump(registry, f, indent=2)
                        
        except Exception as e:
            print(f"Error removing instance from registry: {e}")
    
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
            if self.rename_instance(instance_id, new_name):
                rename_window.destroy()
        
        def cancel_action():
            rename_window.destroy()
        
        tk.Button(button_frame,
                  text="Rename",
                  command=rename_action,
                  bg=self.colors['accent'],
                  fg=self.colors['text_primary'],
                  bd=0,
                  padx=20).pack(side='left', padx=(0, 10))
        
        tk.Button(button_frame,
                  text="Cancel",
                  command=cancel_action,
                  bg=self.colors['bg_medium'],
                  fg=self.colors['text_primary'],
                  bd=0,
                  padx=20).pack(side='left')
    
    def rename_instance(self, instance_id, new_name):
        """Rename an instance"""
        if not new_name or not new_name.strip():
            messagebox.showerror("Error", "Please enter a valid name!")
            return False
        
        try:
            # Update metadata
            if instance_id in self.instances:
                self.instances[instance_id]['name'] = new_name.strip()
                self.instances[instance_id]['last_modified'] = datetime.now().isoformat()
                
                # Save metadata file
                metadata_file = os.path.join(os.path.expanduser('~'), f'.smart_notes_{instance_id}_metadata.json')
                with open(metadata_file, 'w', encoding='utf-8') as f:
                    json.dump(self.instances[instance_id], f, indent=2)
                
                # Update instance registry
                self.update_instance_registry(instance_id, self.instances[instance_id])
                
                # Refresh display
                self.refresh_instance_list()
                
                messagebox.showinfo("Success", "Instance renamed successfully!")
                return True
                
        except Exception as e:
            messagebox.showerror("Error", f"Could not rename instance: {e}")
        
        return False
    
    def on_instance_double_click(self, event):
        """Handle double-click on instance"""
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            instance_id = self.item_to_instance_map.get(item)
            if instance_id:
                self.launch_instance(instance_id)
    
    def toggle_global_auto_start(self):
        """Toggle global auto-start"""
        if self.check_global_auto_start():
            if self.disable_global_auto_start():
                messagebox.showinfo("Success", "Global auto-start disabled!")
            else:
                messagebox.showerror("Error", "Could not disable global auto-start!")
        else:
            if self.enable_global_auto_start():
                messagebox.showinfo("Success", "Global auto-start enabled!")
            else:
                messagebox.showerror("Error", "Could not enable global auto-start!")
        
        # Update button text
        self.update_auto_start_button_text()
    
    def check_global_auto_start(self):
        """Check if global auto-start is enabled"""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                r"Software\Microsoft\Windows\CurrentVersion\Run",
                                0, winreg.KEY_READ)
            try:
                winreg.QueryValueEx(key, "SmartNotes_StartupManager")
                return True
            except:
                return False
            finally:
                winreg.CloseKey(key)
        except:
            return False
    
    def enable_global_auto_start(self):
        """Enable global auto-start"""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                r"Software\Microsoft\Windows\CurrentVersion\Run",
                                0, winreg.KEY_SET_VALUE)
            
            # Create auto-start entry for the new startup manager
            current_dir = os.path.dirname(os.path.abspath(__file__))
            startup_manager_path = os.path.join(current_dir, 'startup_manager.py')
            auto_start_value = f'"{sys.executable}" "{startup_manager_path}"'
            winreg.SetValueEx(key, "SmartNotes_StartupManager", 0, winreg.REG_SZ, auto_start_value)
            winreg.CloseKey(key)
            
            return True
            
        except Exception as e:
            print(f"Could not enable global auto-start: {e}")
            return False
    
    def disable_global_auto_start(self):
        """Disable global auto-start"""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                r"Software\Microsoft\Windows\CurrentVersion\Run",
                                0, winreg.KEY_SET_VALUE | winreg.KEY_QUERY_VALUE)
            
            # Remove the auto-start entry
            winreg.DeleteValue(key, "SmartNotes_StartupManager")
            winreg.CloseKey(key)
            
            return True
            
        except Exception as e:
            print(f"Could not disable global auto-start: {e}")
            return False
    
    def update_auto_start_button_text(self):
        """Update the auto-start button text"""
        if self.check_global_auto_start():
            self.auto_start_btn.config(text="Disable Global Auto-Start", bg=self.colors['danger'])
        else:
            self.auto_start_btn.config(text="Enable Global Auto-Start", bg=self.colors['success'])
    
    def update_status(self):
        """Update the status bar"""
        total_instances = len(self.instances)
        running_instances = len(self.running_instances)
        auto_start_instances = self.auto_start_registry.get_auto_start_count()
        
        status_text = f"Total: {total_instances} | Running: {running_instances} | Auto-Start: {auto_start_instances}"
        self.status_label.config(text=status_text)
    
    def center_window(self):
        """Center the window on screen"""
        self.controller_window.update_idletasks()
        width = self.controller_window.winfo_width()
        height = self.controller_window.winfo_height()
        x = (self.controller_window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.controller_window.winfo_screenheight() // 2) - (height // 2)
        self.controller_window.geometry(f"{width}x{height}+{x}+{y}")
    
    def on_window_close(self):
        """Handle window close event"""
        # Don't close the window, just hide it
        self.controller_window.withdraw()
        
        # Show system tray icon or minimize to taskbar
        # For now, just keep it hidden but running
    
    def show_manager(self):
        """Show the manager window"""
        if self.controller_window:
            self.controller_window.deiconify()
            self.controller_window.lift()
            self.controller_window.focus_force()
    
    def run(self):
        """Start the instance manager"""
        self.controller_window.mainloop()

def main():
    """Main entry point"""
    manager = StandaloneInstanceManager()
    manager.run()

if __name__ == "__main__":
    main() 