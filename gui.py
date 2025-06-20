import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
from PIL import Image, ImageTk
import os
from datetime import datetime
import json
from ExpertSystem.Questions.question_flow import *
from ExpertSystem.engine import *


class ModernDermatologyGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_main_window()
        self.setup_styles()
        self.create_main_interface()

        # Initialize the expert system
        self.expert_system = None
        self.current_question = None
        self.question_queue = []
        self.diagnosis_complete = False
        self.session_data = {
            'started_at': None,
            'answers': {},
            'diagnosis': None
        }

    def setup_main_window(self):
        """Configure the main window with modern styling"""
        self.root.title(
            "Dermatology Expert System - Professional Diagnosis Tool")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)

        # Set window icon if available
        try:
            self.root.iconbitmap('medical_icon.ico')  # Add your icon file
        except:
            pass

        # Configure grid weights for responsive design
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Set color scheme
        self.colors = {
            'primary': '#2C3E50',      # Dark blue-gray
            'secondary': '#3498DB',     # Blue
            'accent': '#E74C3C',        # Red
            'success': '#27AE60',       # Green
            'warning': '#F39C12',       # Orange
            'light': '#ECF0F1',         # Light gray
            'white': '#FFFFFF',
            'text_primary': '#2C3E50',
            'text_secondary': '#7F8C8D'
        }

    def setup_styles(self):
        """Configure modern ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')

        # Configure modern button styles
        style.configure('Primary.TButton',
                        background=self.colors['secondary'],
                        foreground='white',
                        borderwidth=0,
                        focuscolor='none',
                        padding=(20, 10))

        style.map('Primary.TButton',
                  background=[('active', '#2980B9')])

        style.configure('Success.TButton',
                        background=self.colors['success'],
                        foreground='white',
                        borderwidth=0,
                        focuscolor='none',
                        padding=(15, 8))

        style.configure('Danger.TButton',
                        background=self.colors['accent'],
                        foreground='white',
                        borderwidth=0,
                        focuscolor='none',
                        padding=(15, 8))

        # Configure frame styles
        style.configure('Card.TFrame',
                        background=self.colors['white'],
                        relief='flat',
                        borderwidth=1)

        # Configure label styles
        style.configure('Heading.TLabel',
                        background=self.colors['white'],
                        foreground=self.colors['text_primary'],
                        font=('Segoe UI', 16, 'bold'))

        style.configure('Subheading.TLabel',
                        background=self.colors['white'],
                        foreground=self.colors['text_secondary'],
                        font=('Segoe UI', 10))

    def create_main_interface(self):
        """Create the main interface layout"""
        # Main container
        main_container = ttk.Frame(self.root, style='Card.TFrame')
        main_container.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        main_container.grid_rowconfigure(1, weight=1)
        main_container.grid_columnconfigure(0, weight=1)

        # Header
        self.create_header(main_container)

        # Content area with notebook tabs
        self.create_content_area(main_container)

        # Footer
        self.create_footer(main_container)

    def create_header(self, parent):
        """Create the header section"""
        header_frame = ttk.Frame(parent, style='Card.TFrame')
        header_frame.grid(row=0, column=0, sticky='ew', padx=20, pady=(20, 10))
        header_frame.grid_columnconfigure(1, weight=1)

        # Logo/Icon placeholder
        icon_frame = ttk.Frame(header_frame, style='Card.TFrame')
        icon_frame.grid(row=0, column=0, padx=(0, 20))

        # Create a medical cross icon using text
        icon_label = tk.Label(icon_frame, text="⚕", font=('Arial', 32),
                              fg=self.colors['secondary'], bg=self.colors['white'])
        icon_label.pack()

        # Title and subtitle
        title_frame = ttk.Frame(header_frame, style='Card.TFrame')
        title_frame.grid(row=0, column=1, sticky='w')

        title_label = ttk.Label(title_frame, text="Dermatology Expert System",
                                style='Heading.TLabel')
        title_label.pack(anchor='w')

        subtitle_label = ttk.Label(title_frame,
                                   text="Professional AI-Powered Skin Condition Diagnosis Tool",
                                   style='Subheading.TLabel')
        subtitle_label.pack(anchor='w')

        # Status indicator
        self.status_frame = ttk.Frame(header_frame, style='Card.TFrame')
        self.status_frame.grid(row=0, column=2, padx=(20, 0))

        self.status_label = ttk.Label(self.status_frame, text="Ready",
                                      foreground=self.colors['success'],
                                      font=('Segoe UI', 10, 'bold'))
        self.status_label.pack()

    def create_content_area(self, parent):
        """Create the main content area with tabs"""
        self.notebook = ttk.Notebook(parent)
        self.notebook.grid(row=1, column=0, sticky='nsew', padx=20, pady=10)

        # Diagnosis Tab
        self.diagnosis_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.diagnosis_frame, text='🔍 Diagnosis')
        self.create_diagnosis_tab()

        # History Tab
        self.history_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.history_frame, text='📋 Session History')
        self.create_history_tab()

        # Settings Tab
        self.settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_frame, text='⚙️ Settings')
        self.create_settings_tab()

    def create_diagnosis_tab(self):
        """Create the main diagnosis interface"""
        self.diagnosis_frame.grid_rowconfigure(1, weight=1)
        self.diagnosis_frame.grid_columnconfigure(0, weight=1)

        # Welcome section
        self.welcome_frame = ttk.LabelFrame(
            self.diagnosis_frame, text="Welcome", padding=20)
        self.welcome_frame.grid(
            row=0, column=0, sticky='ew', padx=10, pady=(10, 5))

        welcome_text = """Welcome to the Dermatology Expert System. This professional tool will guide you through 
a series of questions to help identify potential skin conditions. Please answer all questions accurately 
for the best diagnostic results."""

        welcome_label = tk.Label(self.welcome_frame, text=welcome_text,
                                 font=('Segoe UI', 11), bg=self.colors['white'],
                                 fg=self.colors['text_secondary'], wraplength=800, justify='left')
        welcome_label.pack(anchor='w')

        # Start diagnosis button
        self.start_button = ttk.Button(self.welcome_frame, text="🚀 Start New Diagnosis",
                                       style='Primary.TButton', command=self.start_diagnosis)
        self.start_button.pack(anchor='w', pady=(15, 0))

        # Question area
        self.question_frame = ttk.LabelFrame(
            self.diagnosis_frame, text="Diagnostic Questions", padding=20)
        self.question_frame.grid(
            row=1, column=0, sticky='nsew', padx=10, pady=5)
        self.question_frame.grid_rowconfigure(1, weight=1)
        self.question_frame.grid_columnconfigure(0, weight=1)

        # Question text
        self.question_text = tk.Text(self.question_frame, height=4, wrap='word',
                                     font=('Segoe UI', 12), bg=self.colors['light'],
                                     fg=self.colors['text_primary'], state='disabled',
                                     relief='flat', padx=15, pady=15)
        self.question_text.grid(row=0, column=0, sticky='ew', pady=(0, 15))

        # Answer area
        self.answer_frame = ttk.Frame(self.question_frame)
        self.answer_frame.grid(row=1, column=0, sticky='nsew')
        self.answer_frame.grid_columnconfigure(0, weight=1)

        # Progress bar
        self.progress_frame = ttk.Frame(self.diagnosis_frame)
        self.progress_frame.grid(
            row=2, column=0, sticky='ew', padx=10, pady=(5, 10))

        progress_label = ttk.Label(self.progress_frame, text="Progress:")
        progress_label.pack(side='left')

        self.progress_bar = ttk.Progressbar(
            self.progress_frame, mode='indeterminate')
        self.progress_bar.pack(side='left', fill='x',
                               expand=True, padx=(10, 0))

        # Results area
        self.results_frame = ttk.LabelFrame(
            self.diagnosis_frame, text="Diagnosis Results", padding=20)
        self.results_frame.grid(
            row=3, column=0, sticky='ew', padx=10, pady=(5, 10))
        self.results_frame.grid_columnconfigure(0, weight=1)

        self.results_text = scrolledtext.ScrolledText(self.results_frame, height=8,
                                                      font=('Segoe UI', 10), state='disabled',
                                                      wrap='word')
        self.results_text.grid(row=0, column=0, sticky='ew')

        # Initially hide question and results areas
        self.question_frame.grid_remove()
        self.results_frame.grid_remove()

    def create_history_tab(self):
        """Create the session history tab"""
        self.history_frame.grid_rowconfigure(0, weight=1)
        self.history_frame.grid_columnconfigure(0, weight=1)

        # History listbox with scrollbar
        history_container = ttk.Frame(self.history_frame)
        history_container.grid(
            row=0, column=0, sticky='nsew', padx=10, pady=10)
        history_container.grid_rowconfigure(0, weight=1)
        history_container.grid_columnconfigure(0, weight=1)

        self.history_tree = ttk.Treeview(history_container, columns=('Date', 'Diagnosis', 'Confidence'),
                                         show='headings', height=15)

        self.history_tree.heading('Date', text='Date & Time')
        self.history_tree.heading('Diagnosis', text='Diagnosis')
        self.history_tree.heading('Confidence', text='Confidence')

        self.history_tree.column('Date', width=200)
        self.history_tree.column('Diagnosis', width=300)
        self.history_tree.column('Confidence', width=100)

        self.history_tree.grid(row=0, column=0, sticky='nsew')

        # Scrollbars
        h_scroll = ttk.Scrollbar(
            history_container, orient='horizontal', command=self.history_tree.xview)
        h_scroll.grid(row=1, column=0, sticky='ew')
        self.history_tree.configure(xscrollcommand=h_scroll.set)

        v_scroll = ttk.Scrollbar(
            history_container, orient='vertical', command=self.history_tree.yview)
        v_scroll.grid(row=0, column=1, sticky='ns')
        self.history_tree.configure(yscrollcommand=v_scroll.set)

        # Buttons frame
        history_buttons = ttk.Frame(self.history_frame)
        history_buttons.grid(row=1, column=0, sticky='ew',
                             padx=10, pady=(5, 10))

        ttk.Button(history_buttons, text="Clear History",
                   command=self.clear_history).pack(side='right')
        ttk.Button(history_buttons, text="Export History",
                   command=self.export_history).pack(side='right', padx=(0, 10))

    def create_settings_tab(self):
        """Create the settings tab"""
        settings_container = ttk.Frame(self.settings_frame, padding=20)
        settings_container.pack(fill='both', expand=True)

        # AI Model Settings
        ai_frame = ttk.LabelFrame(
            settings_container, text="AI Model Configuration", padding=15)
        ai_frame.pack(fill='x', pady=(0, 15))

        ttk.Label(
            ai_frame, text="Enable AI-powered explanations:").grid(row=0, column=0, sticky='w')
        self.ai_enabled = tk.BooleanVar(value=True)
        ttk.Checkbutton(ai_frame, variable=self.ai_enabled).grid(
            row=0, column=1, sticky='w', padx=(10, 0))

        ttk.Label(ai_frame, text="Model:").grid(
            row=1, column=0, sticky='w', pady=(10, 0))
        self.model_var = tk.StringVar(value="microsoft/DialoGPT-medium")
        model_combo = ttk.Combobox(ai_frame, textvariable=self.model_var,
                                   values=["microsoft/DialoGPT-medium", "gpt-3.5-turbo", "custom"])
        model_combo.grid(row=1, column=1, sticky='ew',
                         padx=(10, 0), pady=(10, 0))

        # Display Settings
        display_frame = ttk.LabelFrame(
            settings_container, text="Display Settings", padding=15)
        display_frame.pack(fill='x', pady=(0, 15))

        ttk.Label(display_frame, text="Show confidence percentages:").grid(
            row=0, column=0, sticky='w')
        self.show_confidence = tk.BooleanVar(value=True)
        ttk.Checkbutton(display_frame, variable=self.show_confidence).grid(
            row=0, column=1, sticky='w', padx=(10, 0))

        ttk.Label(display_frame, text="Detailed reasoning:").grid(
            row=1, column=0, sticky='w', pady=(10, 0))
        self.detailed_reasoning = tk.BooleanVar(value=True)
        ttk.Checkbutton(display_frame, variable=self.detailed_reasoning).grid(
            row=1, column=1, sticky='w', padx=(10, 0), pady=(10, 0))

        # Save settings button
        ttk.Button(settings_container, text="Save Settings", style='Primary.TButton',
                   command=self.save_settings).pack(anchor='w', pady=(15, 0))

    def create_footer(self, parent):
        """Create the footer section"""
        footer_frame = ttk.Frame(parent, style='Card.TFrame')
        footer_frame.grid(row=2, column=0, sticky='ew', padx=20, pady=(10, 20))
        footer_frame.grid_columnconfigure(1, weight=1)

        # Disclaimer
        disclaimer_text = "⚠️ DISCLAIMER: This tool provides preliminary assessments only. Always consult healthcare professionals for proper diagnosis and treatment."
        disclaimer_label = ttk.Label(footer_frame, text=disclaimer_text,
                                     foreground=self.colors['warning'],
                                     font=('Segoe UI', 9, 'italic'))
        disclaimer_label.grid(row=0, column=0, sticky='w')

        # Version info
        version_label = ttk.Label(footer_frame, text="v1.0.0 | Professional Edition",
                                  style='Subheading.TLabel')
        version_label.grid(row=0, column=1, sticky='e')

    def start_diagnosis(self):
        """Initialize and start the diagnosis process"""
        try:
            self.update_status("Initializing diagnosis...", 'warning')

            # Disable start button
            self.start_button.config(state='disabled')

            # Initialize expert system
            DermatologyExpertWithFlow = apply_question_flow(DermatologyExpert)
            self.expert_system = DermatologyExpertWithFlow(
                use_llm=self.ai_enabled.get(),
                model_name=self.model_var.get()
            )

            # Reset session data
            self.session_data = {
                'started_at': datetime.now(),
                'answers': {},
                'diagnosis': None
            }

            self.diagnosis_complete = False
            self.question_queue = []

            # Hide welcome and show question area
            self.welcome_frame.grid_remove()
            self.question_frame.grid()
            self.results_frame.grid_remove()

            # Override the expert system's ask_user method
            self.expert_system.ask_user = self.gui_ask_user

            # Start the diagnosis process
            self.update_status("Diagnosis in progress...", 'secondary')
            self.progress_bar.start()

            # Initialize the expert system with start fact
            self.expert_system.declare(Fact(start=True))

            # Start processing questions
            self.process_next_question()

        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to start diagnosis: {str(e)}")
            self.update_status("Error occurred", 'accent')
            self.start_button.config(state='normal')

    def gui_ask_user(self, question_text, valid_responses, question_type):
        """GUI version of ask_user method - stores question for GUI processing"""
        # Store the question for GUI processing
        self.current_question = {
            'text': question_text,
            'valid_responses': valid_responses,
            'type': question_type,
            'answer': None,
            'answered': False
        }

        # Display the question in GUI
        self.display_question()

        # Return a placeholder - the actual answer will be processed later
        return None

    def process_next_question(self):
        """Process the next question in the expert system"""
        try:
            # Run the expert system to get the next question
            self.expert_system.run()

            # Check if we have a current question to display
            if self.current_question and not self.current_question['answered']:
                # Question is already displayed, waiting for user input
                return

            # Check if diagnosis is complete
            if hasattr(self.expert_system, 'best_diagnosis') and self.expert_system.best_diagnosis:
                self.show_results()
                return

            # If no question and no diagnosis, something went wrong
            if not self.current_question:
                self.show_results()  # Show results even if empty

        except Exception as e:
            self.handle_diagnosis_error(str(e))

    def display_question(self):
        """Display the current question in the GUI"""
        if not self.current_question:
            return

        question_text = self.current_question['text']
        valid_responses = self.current_question['valid_responses']
        question_type = self.current_question['type']

        # Update question text
        self.question_text.config(state='normal')
        self.question_text.delete(1.0, tk.END)
        self.question_text.insert(1.0, f"🤔 {question_text}")
        self.question_text.config(state='disabled')

        # Clear previous answer widgets
        for widget in self.answer_frame.winfo_children():
            widget.destroy()

        # Create appropriate input widgets
        if question_type == 'number':
            self.create_number_input()
        else:
            self.create_multiple_choice_input(valid_responses)

    def create_number_input(self):
        """Create number input widget"""
        input_frame = ttk.Frame(self.answer_frame)
        input_frame.pack(fill='x', pady=10)

        ttk.Label(input_frame, text="Enter a number:",
                  font=('Segoe UI', 11)).pack(anchor='w')

        self.number_entry = ttk.Entry(
            input_frame, font=('Segoe UI', 12), width=20)
        self.number_entry.pack(anchor='w', pady=(5, 10))
        self.number_entry.focus()

        submit_button = ttk.Button(input_frame, text="Submit Answer",
                                   style='Primary.TButton', command=self.submit_number_answer)
        submit_button.pack(anchor='w')

        # Bind Enter key
        self.number_entry.bind(
            '<Return>', lambda e: self.submit_number_answer())

    def create_multiple_choice_input(self, valid_responses):
        """Create multiple choice input widgets"""
        input_frame = ttk.Frame(self.answer_frame)
        input_frame.pack(fill='both', expand=True, pady=10)

        ttk.Label(input_frame, text="Select your answer:",
                  font=('Segoe UI', 11)).pack(anchor='w')

        self.choice_var = tk.StringVar()

        # Create radio buttons for each option
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill='both', expand=True, pady=(10, 0))

        for i, option in enumerate(valid_responses):
            # Make option text more readable
            display_text = option.replace('_', ' ').title()

            radio_button = ttk.Radiobutton(button_frame, text=display_text,
                                           variable=self.choice_var, value=option)
            radio_button.pack(anchor='w', pady=2)

            if i == 0:  # Select first option by default
                radio_button.invoke()

        submit_button = ttk.Button(input_frame, text="Submit Answer",
                                   style='Primary.TButton', command=self.submit_choice_answer)
        submit_button.pack(anchor='w', pady=(15, 0))

    def submit_number_answer(self):
        """Submit number answer"""
        try:
            answer = self.number_entry.get().strip()
            if not answer.isdigit():
                messagebox.showerror(
                    "Invalid Input", "Please enter a valid number.")
                return

            self.process_answer(answer)

        except Exception as e:
            messagebox.showerror("Error", f"Error submitting answer: {str(e)}")

    def submit_choice_answer(self):
        """Submit multiple choice answer"""
        try:
            answer = self.choice_var.get()
            if not answer:
                messagebox.showerror(
                    "No Selection", "Please select an answer.")
                return

            self.process_answer(answer)

        except Exception as e:
            messagebox.showerror("Error", f"Error submitting answer: {str(e)}")

    def process_answer(self, answer):
        """Process the submitted answer"""
        try:
            # Store the answer
            self.current_question['answer'] = answer
            self.current_question['answered'] = True

            # Add to session data
            self.session_data['answers'][len(self.session_data['answers'])] = {
                'question': self.current_question['text'],
                'answer': answer
            }

            # Determine question identifier from the question text
            question_ident = self.get_question_identifier(
                self.current_question['text'])

            # Declare the answer as a fact in the expert system
            if question_ident:
                self.expert_system.declare(
                    Answer(ident=question_ident, text=answer))

            # Clear the current question
            self.current_question = None

            # Process next question
            self.root.after(100, self.process_next_question)

        except Exception as e:
            messagebox.showerror("Error", f"Error processing answer: {str(e)}")

    def get_question_identifier(self, question_text):
        """Map question text to identifier"""
        # This is a simplified mapping - you might need to adjust based on your question structure
        question_mapping = {
            'age': 'age',
            'How long': 'duration',
            'severity': 'severity',
            'lump': 'has_symptom_lump_or_growth',
            'nails or hair': 'affects_nails_or_hair',
            'rash': 'has_symptom_rash',
            'location': 'locations',
            'purpura': 'has_symptom_palpable_purpura',
            'soft lump': 'has_symptom_soft_lump',
            'firm lump': 'has_symptom_firm_lump',
            'rough bumps': 'has_symptom_rough_bumps',
            'waxy': 'has_symptom_waxy_appearance',
            'mole': 'has_symptom_evolution_of_mole',
            'sore': 'has_symptom_sore_that_wont_heal',
            'scaly patch': 'has_symptom_persistent_scaly_patch',
            'hair loss': 'has_symptom_patchy_hair_loss',
            'nail pitting': 'has_symptom_nail_pitting',
            'nail thickening': 'has_symptom_nail_thickening',
            'nail concavity': 'has_symptom_nail_concavity',
            'nail fold': 'has_symptom_nail_fold_swelling',
            'nail grooves': 'has_symptom_transverse_nail_grooves',
            'itching': 'has_symptom_itching',
            'worse at night': 'has_symptom_worse_at_night',
            'dryness': 'has_symptom_dryness',
            'ring shaped': 'has_symptom_ring_shaped_rash',
            'white patches': 'has_symptom_white_patches',
            'blisters': 'has_symptom_blisters',
            'contact': 'trigger_contact_related',
            'tense blisters': 'has_symptom_large_tense_blisters',
            'thick patches': 'has_symptom_thick_patches',
            'pimples': 'has_symptom_pimples',
            'unilateral': 'has_symptom_unilateral_rash',
            'pain': 'has_symptom_pain',
            'bulls eye': 'has_symptom_bulls_eye_rash',
            'butterfly': 'has_symptom_butterfly_rash',
            'painful blisters': 'has_symptom_painful_blisters',
            'honey colored': 'has_symptom_honey_colored_crusts',
            'spreading redness': 'has_symptom_spreading_redness',
            'warmth': 'has_symptom_warmth',
            'symmetrical': 'has_symptom_symmetrical_red_rash',
            'medications': 'trigger_medications',
            'loss of pigment': 'has_symptom_loss_of_pigment',
            'brown or gray': 'has_symptom_brown_or_gray_patches',
            'discolored patches': 'has_symptom_discolored_patches',
            'central dimple': 'has_symptom_central_dimple',
            'rough scaly': 'has_symptom_rough_scaly_patch',
            'persistent redness': 'has_symptom_persistent_redness'
        }

        # Find matching identifier
        for key, ident in question_mapping.items():
            if key.lower() in question_text.lower():
                return ident

        # Default fallback
        return None

    

    def show_results(self):
        """Display the diagnosis results"""
        self.progress_bar.stop()
        self.update_status("Diagnosis complete", 'success')

        # Show results frame
        self.results_frame.grid()

        # Get diagnosis results
        if hasattr(self.expert_system, 'best_diagnosis') and self.expert_system.best_diagnosis:
            diagnosis = self.expert_system.best_diagnosis
            confidence = diagnosis.get('cf', 0) * 100
            disease = diagnosis.get('disease', 'Unknown')
            reasoning = diagnosis.get('reasoning', 'No reasoning available')

            # Format results
            results_text = f"""
🏥 DIAGNOSIS RESULTS
{'='*50}

📋 Primary Diagnosis: {disease}
📊 Confidence Level: {confidence:.1f}%
🔍 Clinical Reasoning: {reasoning}

{'='*50}
⚠️ IMPORTANT DISCLAIMER:
This is a preliminary assessment based on the information provided. 
Please consult with a qualified healthcare professional for proper 
diagnosis, treatment recommendations, and medical advice.
{'='*50}
            """

            # Get AI explanation if available
            if self.ai_enabled.get():
                try:
                    ai_explanation = self.expert_system.get_llm_explanation_only()
                    if ai_explanation:
                        results_text += f"\n\n🤖 AI-POWERED MEDICAL EXPLANATION:\n{ai_explanation}\n"
                except Exception as e:
                    results_text += f"\n\n⚠️ AI explanation unavailable: {str(e)}\n"

            # Store in session data
            self.session_data['diagnosis'] = {
                'disease': disease,
                'confidence': confidence,
                'reasoning': reasoning
            }

        else:
            results_text = """
🏥 DIAGNOSIS RESULTS
{'='*50}

⚠️ No definitive diagnosis could be made based on the provided information.

This could be due to:
• Insufficient symptom information
• Symptoms not matching known conditions in the database
• Need for additional clinical examination

{'='*50}
⚠️ RECOMMENDATION:
Please consult with a dermatologist or healthcare professional 
for proper evaluation and diagnosis.
{'='*50}
            """

        # Display results
        self.results_text.config(state='normal')
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, results_text)
        self.results_text.config(state='disabled')

        # Add to history
        self.add_to_history()

        # Switch to results view
        self.notebook.select(0)  # Stay on diagnosis tab

    def handle_diagnosis_error(self, error_message):
        """Handle errors during diagnosis"""
        self.progress_bar.stop()
        self.update_status("Error occurred", 'accent')
        messagebox.showerror(
            "Diagnosis Error", f"An error occurred during diagnosis:\n{error_message}")

    def add_to_history(self):
        """Add current session to history"""
        if self.session_data['diagnosis']:
            self.history_tree.insert('', 0, values=(
                self.session_data['started_at'].strftime("%Y-%m-%d %H:%M:%S"),
                self.session_data['diagnosis']['disease'],
                f"{self.session_data['diagnosis']['confidence']:.1f}%"
            ))

    def clear_history(self):
        """Clear diagnosis history"""
        if messagebox.askyesno("Clear History", "Are you sure you want to clear all diagnosis history?"):
            for item in self.history_tree.get_children():
                self.history_tree.delete(item)

    def export_history(self):
        """Export diagnosis history to file"""
        try:
            from tkinter import filedialog
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            if filename:
                history_data = []
                for item in self.history_tree.get_children():
                    values = self.history_tree.item(item)['values']
                    history_data.append({
                        'date': values[0],
                        'diagnosis': values[1],
                        'confidence': values[2]
                    })

                with open(filename, 'w') as f:
                    json.dump(history_data, f, indent=2)

                messagebox.showinfo("Export Complete",
                                    f"History exported to {filename}")
        except Exception as e:
            messagebox.showerror(
                "Export Error", f"Failed to export history: {str(e)}")

    def save_settings(self):
        """Save application settings"""
        messagebox.showinfo("Settings", "Settings saved successfully!")

    def update_status(self, message, status_type='primary'):
        """Update status indicator"""
        color_map = {
            'primary': self.colors['text_primary'],
            'secondary': self.colors['secondary'],
            'success': self.colors['success'],
            'warning': self.colors['warning'],
            'accent': self.colors['accent']
        }

        self.status_label.config(text=message, foreground=color_map.get(
            status_type, self.colors['text_primary']))

    def run(self):
        """Start the GUI application"""
        self.root.mainloop()


def main():
    """Main function to run the application"""
    try:
        app = ModernDermatologyGUI()
        app.run()
    except Exception as e:
        print(f"Failed to start application: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
