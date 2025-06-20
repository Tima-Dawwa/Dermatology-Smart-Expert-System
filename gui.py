import collections.abc
import collections
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, font, filedialog
import threading
from typing import Dict, Optional
import os
import datetime



class MockFact:
    pass


class MockDermatologyExpert:
    def __init__(self, use_llm=False, llm_instance=None):
        self.use_llm = use_llm
        self.llm_instance = llm_instance
        self.best_diagnosis = None
        self.questions = [
            "Do you have any redness on your skin?",
            "Is there any itching or burning sensation?",
            "How long have you had these symptoms?",
            "Are there any raised bumps or lesions?",
            "Have you noticed any scaling or flaking?"
        ]
        self.current_question_index = 0
        self.answers = []

    def reset(self):
        self.current_question_index = 0
        self.answers = []
        self.best_diagnosis = None

    def run(self):
        # Simulate diagnosis process
        if len(self.answers) >= len(self.questions):
            # Generate mock diagnosis
            self.best_diagnosis = {
                'disease': 'Dermatitis',
                'cf': 0.85,
                'reasoning': 'Based on the symptoms described, this appears to be a common skin inflammation.'
            }

    def ask_user(self, question, valid_responses=None, question_type='text'):
        return question  # This will be overridden by GUI


class MockLLM:
    def test_connection(self):
        return True

    def get_explanation(self, diagnosis):
        return {
            'detailed_explanation': 'This is a mock AI explanation of the diagnosis.',
            'causes': 'Common causes include allergens, stress, and environmental factors.',
            'symptoms_analysis': 'The symptoms align with typical dermatitis presentation.',
            'treatment_recommendations': 'Topical treatments and avoiding triggers are recommended.',
            'prognosis': 'Generally good with proper care and treatment.',
            'when_to_seek_help': 'Seek immediate care if symptoms worsen or spread rapidly.'
        }


def apply_question_flow(cls):
    return cls


def apply_diagnostic_rules(cls):
    return cls


def get_question_by_ident(ident):
    return {"text": "Mock question", "valid_responses": ["yes", "no"]}


# Fix for collections.Mapping deprecation
if not hasattr(collections, 'Mapping'):
    collections.Mapping = collections.abc.Mapping


class ModernButton(tk.Button):
    """Custom button with modern styling and animations"""

    def __init__(self, parent, **kwargs):
        # Default styling
        default_style = {
            'font': ('Segoe UI', 10, 'bold'),
            'relief': 'flat',
            'borderwidth': 0,
            'cursor': 'hand2',
            'padx': 20,
            'pady': 10,
            'activebackground': '#475569',
            'highlightthickness': 0
        }
        default_style.update(kwargs)
        super().__init__(parent, **default_style)

        # Hover effects
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)

        # Click effect
        self.bind('<Button-1>', self.on_click)
        self.bind('<ButtonRelease-1>', self.on_release)

        # Store original colors
        self.original_bg = self.cget('bg')
        self.original_fg = self.cget('fg')

        # Animation properties
        self.is_animating = False

    def on_enter(self, e):
        if not self.is_animating:
            self.config(bg=self.lighten_color(self.original_bg, 20))

    def on_leave(self, e):
        if not self.is_animating:
            self.config(bg=self.original_bg)

    def on_click(self, e):
        self.is_animating = True
        self.config(bg=self.darken_color(self.original_bg, 20))

    def on_release(self, e):
        self.after(200, lambda: self.config(bg=self.original_bg))
        self.is_animating = False

    def lighten_color(self, color, percent):
        """Lighten a color by a percentage"""
        try:
            # Convert hex to RGB
            color = color.lstrip('#')
            rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))

            # Lighten each component
            lightened = tuple(
                min(255, int(c + (255 - c) * percent / 100))
                for c in rgb
            )

            # Convert back to hex
            return f'#{lightened[0]:02x}{lightened[1]:02x}{lightened[2]:02x}'
        except:
            return color

    def darken_color(self, color, percent):
        """Darken a color by a percentage"""
        try:
            # Convert hex to RGB
            color = color.lstrip('#')
            rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))

            # Darken each component
            darkened = tuple(
                max(0, int(c * (100 - percent) / 100))
                for c in rgb
            )

            # Convert back to hex
            return f'#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}'
        except:
            return color


class DermatologyGUI:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_variables()
        self.setup_styles()
        self.create_widgets()
        self.center_window()

        # Initialize expert system components
        self.engine = None
        self.llm_instance = None
        self.current_question = None
        self.question_history = []
        self.answers = {}
        self.waiting_for_answer = False

        # Initialize LLM
        self.initialize_llm()

    def setup_window(self):
        """Configure the main window"""
        self.root.title("DermaExpert AI - Dermatology Diagnostic Assistant")
        self.root.geometry("1280x800")
        self.root.minsize(1024, 768)

        # Configure window style
        self.root.configure(bg='#F8FAFC')

    def setup_variables(self):
        """Initialize tkinter variables"""
        self.status_var = tk.StringVar(value="Ready to start diagnosis")
        self.progress_var = tk.DoubleVar()
        self.current_answer = tk.StringVar()
        self.llm_status = tk.StringVar(value="Initializing AI system...")
        self.user_name = tk.StringVar(value="Patient")
        self.diagnosis_active = tk.BooleanVar(value=False)

    def setup_styles(self):
        """Configure custom styles"""
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Define color scheme (modern healthcare palette)
        self.colors = {
            'primary': '#3B82F6',    # Blue
            'primary-dark': '#2563EB',
            'primary-light': '#93C5FD',
            'secondary': '#8B5CF6',   # Purple
            'success': '#10B981',     # Green
            'danger': '#EF4444',      # Red
            'warning': '#F59E0B',     # Amber
            'info': '#06B6D4',        # Cyan
            'light': '#F8FAFC',       # Lightest
            'lighter': '#F1F5F9',
            'light-gray': '#E2E8F0',
            'gray': '#94A3B8',
            'dark-gray': '#64748B',
            'dark': '#1E293B',
            'white': '#FFFFFF',
            'black': '#000000'
        }

        # Configure fonts
        self.fonts = {
            'heading': ('Segoe UI', 20, 'bold'),
            'subheading': ('Segoe UI', 14, 'bold'),
            'body': ('Segoe UI', 12),
            'small': ('Segoe UI', 10),
            'code': ('Consolas', 11)
        }

        # Configure ttk styles
        self.style.configure('TFrame', background=self.colors['light'])
        self.style.configure(
            'TLabel', background=self.colors['light'], font=self.fonts['body'])
        self.style.configure('TButton', font=self.fonts['body'], padding=6)
        self.style.configure('TEntry', padding=8)
        self.style.configure('TProgressbar', thickness=12)

    def create_widgets(self):
        """Create and arrange all GUI widgets"""
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['light'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Header
        self.create_header(main_frame)

        # Content area
        content_frame = tk.Frame(main_frame, bg=self.colors['light'])
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Left panel (questions)
        self.create_left_panel(content_frame)

        # Right panel (results)
        self.create_right_panel(content_frame)

        # Bottom status bar
        self.create_status_bar(main_frame)

    def create_header(self, parent):
        """Create the header section"""
        header_frame = tk.Frame(parent, bg=self.colors['primary'], height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        # Title
        title_label = tk.Label(
            header_frame,
            text="🩺 DermaExpert AI",
            font=self.fonts['heading'],
            fg=self.colors['white'],
            bg=self.colors['primary']
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=20)

        # User info
        user_frame = tk.Frame(header_frame, bg=self.colors['primary'])
        user_frame.pack(side=tk.RIGHT, padx=20, pady=15)

        tk.Label(
            user_frame,
            text="👤 Patient:",
            font=self.fonts['body'],
            fg=self.colors['white'],
            bg=self.colors['primary']
        ).pack(side=tk.LEFT, padx=(0, 5))

        self.user_entry = tk.Entry(
            user_frame,
            textvariable=self.user_name,
            font=self.fonts['body'],
            relief=tk.FLAT,
            bg=self.colors['white'],
            fg=self.colors['dark'],
            width=15,
            justify=tk.CENTER
        )
        self.user_entry.pack(side=tk.LEFT)

        # AI Status
        self.ai_status_label = tk.Label(
            header_frame,
            textvariable=self.llm_status,
            font=self.fonts['small'],
            fg=self.colors['white'],
            bg=self.colors['primary']
        )
        self.ai_status_label.pack(side=tk.RIGHT, padx=(0, 20), pady=20)

        # Progress bar
        self.progress_bar = ttk.Progressbar(
            header_frame,
            variable=self.progress_var,
            maximum=100,
            length=200
        )
        self.progress_bar.pack(side=tk.RIGHT, padx=(0, 20), pady=20)

    def create_left_panel(self, parent):
        """Create the left panel for questions"""
        left_frame = tk.Frame(
            parent,
            bg=self.colors['white'],
            relief=tk.RAISED,
            bd=1
        )
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        # Question section header
        question_header = tk.Frame(
            left_frame, bg=self.colors['primary'], height=50)
        question_header.pack(fill=tk.X)
        question_header.pack_propagate(False)

        tk.Label(
            question_header,
            text="🩺 Medical Assessment",
            font=self.fonts['subheading'],
            bg=self.colors['primary'],
            fg=self.colors['white']
        ).pack(side=tk.LEFT, padx=20, pady=15)

        # Question content
        question_content = tk.Frame(left_frame, bg=self.colors['white'])
        question_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Question text
        tk.Label(
            question_content,
            text="Question:",
            font=self.fonts['body'],
            bg=self.colors['white'],
            fg=self.colors['dark']
        ).pack(anchor=tk.W, pady=(0, 5))

        self.question_text = tk.Text(
            question_content,
            height=4,
            font=self.fonts['body'],
            wrap=tk.WORD,
            bg=self.colors['lighter'],
            relief=tk.FLAT,
            state=tk.DISABLED,
            padx=15,
            pady=15
        )
        self.question_text.pack(fill=tk.X, pady=(0, 20))

        # Answer input
        tk.Label(
            question_content,
            text="Your Answer:",
            font=self.fonts['body'],
            bg=self.colors['white'],
            fg=self.colors['dark']
        ).pack(anchor=tk.W, pady=(0, 5))

        self.answer_entry = tk.Entry(
            question_content,
            textvariable=self.current_answer,
            font=self.fonts['body'],
            relief=tk.FLAT,
            bg=self.colors['lighter'],
            fg=self.colors['dark']
        )
        self.answer_entry.pack(fill=tk.X, ipady=8, pady=(0, 20))
        self.answer_entry.bind('<Return>', lambda e: self.submit_answer())

        # Buttons
        buttons_frame = tk.Frame(question_content, bg=self.colors['white'])
        buttons_frame.pack(fill=tk.X, pady=(0, 20))

        self.start_btn = ModernButton(
            buttons_frame,
            text="Start Diagnosis",
            bg=self.colors['primary'],
            fg=self.colors['white'],
            command=self.start_diagnosis
        )
        self.start_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.submit_btn = ModernButton(
            buttons_frame,
            text="Submit Answer",
            bg=self.colors['success'],
            fg=self.colors['white'],
            command=self.submit_answer,
            state=tk.DISABLED
        )
        self.submit_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.reset_btn = ModernButton(
            buttons_frame,
            text="Reset",
            bg=self.colors['danger'],
            fg=self.colors['white'],
            command=self.reset_diagnosis
        )
        self.reset_btn.pack(side=tk.LEFT)

        # Question history
        tk.Label(
            question_content,
            text="📋 Question History:",
            font=self.fonts['subheading'],
            bg=self.colors['white'],
            fg=self.colors['dark']
        ).pack(anchor=tk.W, pady=(10, 5))

        self.history_text = scrolledtext.ScrolledText(
            question_content,
            font=self.fonts['small'],
            bg=self.colors['lighter'],
            relief=tk.FLAT,
            state=tk.DISABLED,
            height=8
        )
        self.history_text.pack(fill=tk.BOTH, expand=True)

    def create_right_panel(self, parent):
        """Create the right panel for results"""
        right_frame = tk.Frame(
            parent,
            bg=self.colors['white'],
            relief=tk.RAISED,
            bd=1
        )
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        # Results section header
        results_header = tk.Frame(
            right_frame, bg=self.colors['secondary'], height=50)
        results_header.pack(fill=tk.X)
        results_header.pack_propagate(False)

        tk.Label(
            results_header,
            text="📊 Diagnosis Results",
            font=self.fonts['subheading'],
            bg=self.colors['secondary'],
            fg=self.colors['white']
        ).pack(side=tk.LEFT, padx=20, pady=15)

        # Results content
        results_content = tk.Frame(right_frame, bg=self.colors['white'])
        results_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Results display
        self.results_text = scrolledtext.ScrolledText(
            results_content,
            font=self.fonts['body'],
            bg=self.colors['lighter'],
            relief=tk.FLAT,
            state=tk.DISABLED,
            wrap=tk.WORD
        )
        self.results_text.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        # Export buttons
        button_frame = tk.Frame(results_content, bg=self.colors['white'])
        button_frame.pack(fill=tk.X)

        self.export_btn = ModernButton(
            button_frame,
            text="📄 Export Report",
            bg=self.colors['info'],
            fg=self.colors['white'],
            command=self.export_results,
            state=tk.DISABLED
        )
        self.export_btn.pack(side=tk.LEFT, padx=(0, 10))

    def create_status_bar(self, parent):
        """Create the status bar"""
        status_frame = tk.Frame(parent, bg=self.colors['dark'], height=30)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        status_frame.pack_propagate(False)

        self.status_label = tk.Label(
            status_frame,
            textvariable=self.status_var,
            font=self.fonts['small'],
            bg=self.colors['dark'],
            fg=self.colors['white']
        )
        self.status_label.pack(side=tk.LEFT, padx=20, pady=5)

        version_label = tk.Label(
            status_frame,
            text="DermaExpert AI v1.0.0",
            font=self.fonts['small'],
            bg=self.colors['dark'],
            fg=self.colors['gray']
        )
        version_label.pack(side=tk.RIGHT, padx=20, pady=5)

    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def initialize_llm(self):
        """Initialize the LLM system"""
        def init_llm():
            try:
                self.llm_instance = MockLLM()
                if self.llm_instance.test_connection():
                    self.llm_status.set("🤖 AI System Ready")
                    self.update_status(
                        "AI explanation system initialized successfully")
                else:
                    self.llm_status.set("⚠️ AI System Offline")
                    self.update_status(
                        "Warning: AI system not available - basic diagnosis only")
            except Exception as e:
                self.llm_status.set("❌ AI System Error")
                self.update_status(f"AI system error: {str(e)}")

        thread = threading.Thread(target=init_llm, daemon=True)
        thread.start()

    def start_diagnosis(self):
        """Start the diagnosis process"""
        try:
            # Initialize expert system
            self.engine = MockDermatologyExpert(
                use_llm=self.llm_instance is not None,
                llm_instance=self.llm_instance
            )

            # Reset state
            self.answers = {}
            self.question_history = []
            self.current_question = None
            self.diagnosis_active.set(True)
            self.waiting_for_answer = False

            # Clear displays
            self.clear_results()
            self.clear_history()

            # Start first question
            self.ask_next_question()

            # Update UI
            self.start_btn.config(state=tk.DISABLED)
            self.submit_btn.config(state=tk.NORMAL)
            self.update_status(f"Diagnosis started for {self.user_name.get()}")

            # Show welcome message
            welcome_msg = f"👋 Welcome, {self.user_name.get()}!\n\n"
            welcome_msg += "The dermatology expert system will guide you through questions "
            welcome_msg += "to help diagnose your skin condition.\n\n"
            welcome_msg += "Please answer each question as accurately as possible."
            self.show_results(welcome_msg)

        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to start diagnosis: {str(e)}")
            self.update_status("Error starting diagnosis")

    def ask_next_question(self):
        """Ask the next question in the sequence"""
        if self.engine.current_question_index < len(self.engine.questions):
            question = self.engine.questions[self.engine.current_question_index]
            self.display_question(question)
            self.waiting_for_answer = True
        else:
            self.complete_diagnosis()

    def display_question(self, question_text):
        """Display a question in the GUI"""
        self.question_text.config(state=tk.NORMAL)
        self.question_text.delete(1.0, tk.END)
        self.question_text.insert(tk.END, question_text)
        self.question_text.config(state=tk.DISABLED)

        # Clear and focus answer entry
        self.current_answer.set("")
        self.answer_entry.focus()

        # Update progress
        progress = (self.engine.current_question_index /
                    len(self.engine.questions)) * 100
        self.progress_var.set(progress)

    def submit_answer(self):
        """Submit the current answer"""
        if not self.waiting_for_answer:
            return

        answer = self.current_answer.get().strip()
        if not answer:
            messagebox.showwarning("No Answer", "Please provide an answer")
            return

        # Store answer
        question = self.engine.questions[self.engine.current_question_index]
        self.engine.answers.append(answer)
        self.add_to_history(question, answer)

        # Move to next question
        self.engine.current_question_index += 1
        self.waiting_for_answer = False

        # Ask next question or complete diagnosis
        if self.engine.current_question_index < len(self.engine.questions):
            self.ask_next_question()
        else:
            self.complete_diagnosis()

    def complete_diagnosis(self):
        """Complete the diagnosis process"""
        try:
            # Run the engine
            self.engine.run()

            # Display results
            self.display_final_results()

            # Update UI
            self.submit_btn.config(state=tk.DISABLED)
            self.export_btn.config(state=tk.NORMAL)
            self.start_btn.config(state=tk.NORMAL)
            self.progress_var.set(100)
            self.update_status("Diagnosis completed successfully")

        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to complete diagnosis: {str(e)}")

    def display_final_results(self):
        """Display the final diagnosis results"""
        if not self.engine.best_diagnosis:
            self.show_results(
                "No diagnosis could be made based on the provided answers.")
            return

        diagnosis = self.engine.best_diagnosis
        results = f"🎯 DIAGNOSIS RESULTS\n{'='*50}\n\n"
        results += f"Patient: {self.user_name.get()}\n"
        results += f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        results += f"Most Likely Diagnosis: {diagnosis['disease']}\n"
        results += f"Confidence: {diagnosis['cf'] * 100:.1f}%\n"
        results += f"Reasoning: {diagnosis.get('reasoning', 'Based on expert system analysis')}\n\n"

        # Add AI explanation if available
        if self.engine.use_llm and self.llm_instance:
            try:
                explanation = self.llm_instance.get_explanation(diagnosis)
                results += "🤖 AI MEDICAL EXPLANATION\n" + "="*50 + "\n\n"
                results += f"📝 DETAILED EXPLANATION:\n{explanation['detailed_explanation']}\n\n"
                results += f"🔍 CAUSES & RISK FACTORS:\n{explanation['causes']}\n\n"
                results += f"🩺 SYMPTOM ANALYSIS:\n{explanation['symptoms_analysis']}\n\n"
                results += f"💊 TREATMENT RECOMMENDATIONS:\n{explanation['treatment_recommendations']}\n\n"
                results += f"📈 PROGNOSIS:\n{explanation['prognosis']}\n\n"
                results += f"🚨 WHEN TO SEEK CARE:\n{explanation['when_to_seek_help']}\n\n"
            except Exception as e:
                results += f"⚠️ AI explanation error: {str(e)}\n\n"

        results += "\n" + "="*50 + "\n"
        results += "⚠️  IMPORTANT DISCLAIMER:\n"
        results += "This AI explanation is for informational purposes only.\n"
        results += "Always consult with qualified healthcare professionals for\n"
        results += "proper medical diagnosis, treatment, and care.\n"
        results += "="*50

        self.show_results(results)

    def add_to_history(self, question, answer):
        """Add question and answer to history"""
        self.question_history.append((question, answer))

        self.history_text.config(state=tk.NORMAL)
        self.history_text.insert(tk.END, f"Q: {question}\nA: {answer}\n\n")
        self.history_text.see(tk.END)
        self.history_text.config(state=tk.DISABLED)

    def show_results(self, results):
        """Display results in the results panel"""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, results)
        self.results_text.config(state=tk.DISABLED)
        self.results_text.see(tk.END)

    def clear_results(self):
        """Clear the results panel"""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state=tk.DISABLED)

    def clear_history(self):
        """Clear the question history"""
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        self.history_text.config(state=tk.DISABLED)

    def reset_diagnosis(self):
        """Reset the diagnosis process"""
        # Reset variables
        self.engine = None
        self.current_question = None
        self.answers = {}
        self.question_history = []
        self.diagnosis_active.set(False)
        self.waiting_for_answer = False

        # Reset progress
        self.progress_var.set(0)

        # Clear displays
        self.clear_results()
        self.clear_history()

        # Clear question
        self.question_text.config(state=tk.NORMAL)
        self.question_text.delete(1.0, tk.END)
        self.question_text.config(state=tk.DISABLED)

        # Reset UI
        self.start_btn.config(state=tk.NORMAL)
        self.submit_btn.config(state=tk.DISABLED)
        self.export_btn.config(state=tk.DISABLED)
        self.current_answer.set("")

        self.update_status("Ready to start new diagnosis")

    def export_results(self):
        """Export results to a file"""
        try:
            default_filename = f"DermaExpert_Report_{self.user_name.get()}_{datetime.datetime.now().strftime('%Y%m%d')}.txt"

            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                initialfile=default_filename,
                filetypes=[
                    ("Text files", "*.txt"),
                    ("All files", "*.*")
                ],
                title="Save Diagnosis Report"
            )

            if filename:
                results = self.results_text.get(1.0, tk.END)
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(results)

                messagebox.showinfo(
                    "Export Successful", f"Report saved to {os.path.basename(filename)}")
                self.update_status(f"Results exported to {filename}")

        except Exception as e:
            messagebox.showerror(
                "Export Error", f"Failed to export results: {str(e)}")

    def update_status(self, message):
        """Update status bar message"""
        self.status_var.set(message)


def main():
    """Main function to run the GUI"""
    root = tk.Tk()
    app = DermatologyGUI(root)

    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit the application?"):
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
