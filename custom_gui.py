"""
Custom GUI for Phishing Email Detector
Implements the user interface using customtkinter
"""

import os
import json
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox
import customtkinter as ctk
from predict import PhishingPredictor
from parser_util import EmailParser

# Set appearance mode and default color theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class PhishingDetectorApp(ctk.CTk):
    """Main application window for the Phishing Email Detector"""
    
    def __init__(self):
        super().__init__()
        
        # Initialize predictor and parser
        self.predictor = PhishingPredictor()
        self.email_parser = EmailParser()
        
        # Configure window
        self.title("Phishing Email Detector")
        self.geometry("1000x800")
        self.minsize(800, 600)
        
        # Initialize history
        self.history = self.load_history()
        
        # Create the UI elements
        self.create_ui()
        
        # Result variables
        self.result_shown = False
        
    def create_ui(self):
        """Create all UI elements"""
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)  # Sidebar
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=1)  # Main content
        
        # Create header
        self.create_header()
        
        # Create main content area
        self.create_main_content()
        
        # Create sidebar
        self.create_sidebar()
        
    def create_header(self):
        """Create header section"""
        self.header_frame = ctk.CTkFrame(self, corner_radius=0, height=80)
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.header_frame.grid_columnconfigure(0, weight=1)
        self.header_frame.grid_columnconfigure(1, weight=0)
        
        # Title and subtitle
        title_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        title_frame.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        
        self.title_label = ctk.CTkLabel(
            title_frame,
            text="Phishing Email Detector",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.grid(row=0, column=0, sticky="w")
        
        self.subtitle_label = ctk.CTkLabel(
            title_frame,
            text="AI-powered email analysis",
            font=ctk.CTkFont(size=14)
        )
        self.subtitle_label.grid(row=1, column=0, sticky="w")
        
        # Theme toggle
        self.theme_button = ctk.CTkButton(
            self.header_frame,
            text="Toggle Theme",
            width=120,
            command=self.toggle_theme
        )
        self.theme_button.grid(row=0, column=1, padx=20, pady=10)
        
    def create_main_content(self):
        """Create main content area"""
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        # Email input section
        self.create_email_input()
        
        # Results section
        self.create_results_section()
        
    def create_email_input(self):
        """Create email input section"""
        # Input label
        self.input_label = ctk.CTkLabel(
            self.main_frame,
            text="Email Content",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.input_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        
        # Text area
        self.email_text = ctk.CTkTextbox(self.main_frame, height=300)
        self.email_text.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        # Buttons
        button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        button_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        button_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        self.load_button = ctk.CTkButton(
            button_frame,
            text="Load .eml File",
            command=self.load_eml_file,
            font=ctk.CTkFont(size=14)
        )
        self.load_button.grid(row=0, column=0, padx=5)
        
        self.clear_button = ctk.CTkButton(
            button_frame,
            text="Clear Text",
            command=self.clear_text,
            font=ctk.CTkFont(size=14),
            fg_color="gray"
        )
        self.clear_button.grid(row=0, column=1, padx=5)
        
        self.analyze_button = ctk.CTkButton(
            button_frame,
            text="Analyze Email",
            command=self.analyze_email,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.analyze_button.grid(row=0, column=2, padx=5)
        
        self.export_button = ctk.CTkButton(
            button_frame,
            text="Export Results",
            command=self.export_results,
            font=ctk.CTkFont(size=14),
            state="disabled"
        )
        self.export_button.grid(row=0, column=3, padx=5)
        
    def create_results_section(self):
        """Create results section"""
        self.result_frame = ctk.CTkFrame(self.main_frame)
        self.result_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        self.result_frame.grid_columnconfigure(0, weight=1)
        self.result_frame.grid_propagate(False)
        self.result_frame.configure(height=0)
        
        # Main result
        self.status_label = ctk.CTkLabel(
            self.result_frame,
            text="",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        
        # Confidence
        self.confidence_label = ctk.CTkLabel(
            self.result_frame,
            text="",
            font=ctk.CTkFont(size=16)
        )
        
        self.confidence_bar = ctk.CTkProgressBar(self.result_frame)
        self.confidence_bar.set(0)
        
        # Analysis details
        self.details_text = ctk.CTkTextbox(self.result_frame, height=100)
        self.details_text.configure(state="disabled")
        
    def create_sidebar(self):
        """Create sidebar with history"""
        self.sidebar = ctk.CTkFrame(self, width=250)
        self.sidebar.grid(row=1, column=1, padx=(0, 20), pady=10, sticky="nsew")
        self.sidebar.grid_propagate(False)
        
        # History label
        history_label = ctk.CTkLabel(
            self.sidebar,
            text="Analysis History",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        history_label.pack(padx=10, pady=10)
        
        # History list
        self.history_frame = ctk.CTkScrollableFrame(self.sidebar)
        self.history_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Load history items
        self.update_history_display()
        
    def toggle_theme(self):
        """Toggle between light and dark mode"""
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("Light")
        else:
            ctk.set_appearance_mode("Dark")
    
    def load_eml_file(self):
        """Open file dialog to load an .eml file"""
        file_path = filedialog.askopenfilename(
            title="Select Email File",
            filetypes=[("Email files", "*.eml"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                email_content = self.email_parser.parse_eml_file(file_path)
                self.clear_text()
                self.email_text.insert("1.0", email_content)
                if self.result_shown:
                    self.hide_result()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load email file: {str(e)}")
    
    def clear_text(self):
        """Clear the text area"""
        self.email_text.delete("1.0", tk.END)
        if self.result_shown:
            self.hide_result()
        self.export_button.configure(state="disabled")
    
    def analyze_email(self):
        """Analyze the email content for phishing"""
        email_content = self.email_text.get("1.0", tk.END).strip()
        
        if not email_content:
            messagebox.showwarning("Warning", "Please enter or load email content first.")
            return
        
        self.analyze_button.configure(state="disabled", text="Analyzing...")
        self.update_idletasks()
        
        try:
            is_phishing, confidence = self.predictor.predict(email_content)
            self.show_result(is_phishing, confidence)
            self.add_to_history(email_content[:100], is_phishing, confidence)
            self.export_button.configure(state="normal")
        except Exception as e:
            messagebox.showerror("Error", f"Analysis failed: {str(e)}")
        
        self.analyze_button.configure(state="normal", text="Analyze Email")
    
    def show_result(self, is_phishing, confidence):
        """Display the analysis result"""
        confidence_pct = f"{confidence:.1f}%"
        
        if is_phishing:
            status_text = "⚠️ PHISHING DETECTED"
            status_color = "#b22222"
            details = self.generate_phishing_details(confidence)
        else:
            status_text = "✅ EMAIL APPEARS SAFE"
            status_color = "#2e8b57"
            details = self.generate_safe_details(confidence)
        
        # Configure result widgets
        self.status_label.configure(text=status_text, text_color=status_color)
        self.status_label.grid(row=0, column=0, padx=20, pady=(15, 5))
        
        self.confidence_label.configure(text=f"Confidence: {confidence_pct}")
        self.confidence_label.grid(row=1, column=0, padx=20, pady=(0, 5))
        
        self.confidence_bar.configure(progress_color=status_color)
        self.confidence_bar.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.confidence_bar.set(confidence / 100)
        
        # Show details
        self.details_text.configure(state="normal")
        self.details_text.delete("1.0", tk.END)
        self.details_text.insert("1.0", details)
        self.details_text.configure(state="disabled")
        self.details_text.grid(row=3, column=0, padx=20, pady=(0, 15), sticky="ew")
        
        # Show the result frame
        self.result_frame.configure(height=250)
        self.result_shown = True
    
    def hide_result(self):
        """Hide the result section"""
        self.result_frame.configure(height=0)
        self.result_shown = False
    
    def generate_phishing_details(self, confidence):
        """Generate detailed analysis for phishing emails"""
        risk_level = "High" if confidence > 80 else "Medium" if confidence > 60 else "Low"
        
        details = f"""Risk Level: {risk_level}

Recommendations:
• Do not click any links in this email
• Do not download any attachments
• Do not reply or provide any information
• Report this email to your IT department
• Delete the email from your inbox

Analysis completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
        
        return details
    
    def generate_safe_details(self, confidence):
        """Generate detailed analysis for safe emails"""
        details = f"""Safety Analysis:
• No immediate phishing indicators detected
• Email appears to be legitimate
• Normal communication patterns observed

Note: While this email appears safe, always remain vigilant
and follow your organization's security guidelines.

Analysis completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
        
        return details
    
    def load_history(self):
        """Load analysis history from file"""
        history_file = "analysis_history.json"
        if os.path.exists(history_file):
            try:
                with open(history_file, "r") as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_history(self):
        """Save analysis history to file"""
        history_file = "analysis_history.json"
        try:
            with open(history_file, "w") as f:
                json.dump(self.history, f)
        except Exception as e:
            print(f"Failed to save history: {e}")
    
    def add_to_history(self, email_preview, is_phishing, confidence):
        """Add an analysis result to history"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        entry = {
            "timestamp": timestamp,
            "preview": email_preview + "...",
            "is_phishing": is_phishing,
            "confidence": confidence
        }
        
        self.history.insert(0, entry)
        if len(self.history) > 50:  # Keep last 50 entries
            self.history.pop()
            
        self.save_history()
        self.update_history_display()
    
    def update_history_display(self):
        """Update the history display in the sidebar"""
        # Clear existing history items
        for widget in self.history_frame.winfo_children():
            widget.destroy()
        
        # Add history items
        for entry in self.history:
            item_frame = ctk.CTkFrame(self.history_frame)
            item_frame.pack(fill="x", padx=5, pady=2)
            
            status_color = "#b22222" if entry["is_phishing"] else "#2e8b57"
            status_text = "⚠️ Phishing" if entry["is_phishing"] else "✅ Safe"
            
            status = ctk.CTkLabel(
                item_frame,
                text=status_text,
                text_color=status_color,
                font=ctk.CTkFont(size=12, weight="bold")
            )
            status.pack(anchor="w")
            
            preview = ctk.CTkLabel(
                item_frame,
                text=entry["preview"],
                font=ctk.CTkFont(size=10),
                wraplength=200
            )
            preview.pack(anchor="w")
            
            details = ctk.CTkLabel(
                item_frame,
                text=f"{entry['confidence']:.1f}% confidence • {entry['timestamp']}",
                font=ctk.CTkFont(size=10),
                text_color="gray"
            )
            details.pack(anchor="w")
    
    def export_results(self):
        """Export analysis results to a text file"""
        if not self.result_shown:
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Export Analysis Results"
        )
        
        if file_path:
            try:
                with open(file_path, "w") as f:
                    # Write email content
                    f.write("=== Email Content ===\n\n")
                    f.write(self.email_text.get("1.0", tk.END))
                    f.write("\n\n=== Analysis Results ===\n\n")
                    
                    # Write analysis results
                    f.write(f"Status: {self.status_label.cget('text')}\n")
                    f.write(f"Confidence: {self.confidence_label.cget('text')}\n\n")
                    f.write(self.details_text.get("1.0", tk.END))
                    
                messagebox.showinfo("Success", "Results exported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export results: {str(e)}")

# For testing the GUI independently
if __name__ == "__main__":
    app = PhishingDetectorApp()
    app.mainloop()