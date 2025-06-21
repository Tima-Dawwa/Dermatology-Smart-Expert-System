from ExpertSystem.engine import *
from ExpertSystem.Questions.question_flow import *
from tkinter import ttk, messagebox, scrolledtext
import tkinter as tk


class ModernDermatologyGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_main_window()
        self.setup_styles()
        self.create_main_interface()
        self.expert_system = None
        self.current_question = None
        self.diagnosis_complete = False
        self.waiting_for_answer = False  # Flag to manage GUI state

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
        """Initialize and start the diagnosis process."""
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

            self.expert_system.reset()
            self.diagnosis_complete = False
            self.waiting_for_answer = False  # Ensure this is False at start

            # Hide welcome and show question area
            self.welcome_frame.grid_remove()
            self.question_frame.grid()
            self.results_frame.grid_remove()

            # Start the diagnosis process
            self.update_status("Diagnosis in progress...", 'secondary')
            self.progress_bar.start()

            # Initialize the expert system with start fact
            self.expert_system.declare(Fact(start=True))

            # Begin the expert system processing loop
            self.root.after(100, self.process_expert_system)

        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to start diagnosis: {str(e)}")
            self.update_status("Error occurred", 'accent')
            self.start_button.config(state='normal')

    def process_expert_system(self):
        """
        Manages the expert system's execution cycle.
        This method is called periodically or after user input.
        """
        try:
            if self.waiting_for_answer:
                # If we are waiting for user input, do nothing until an answer is submitted.
                return

            # Run the expert system. It will halt itself if a NextQuestion is declared
            # or when the final results are processed.
            self.expert_system.run()

            # After running, check the state of the expert system
            next_question_fact = None
            for fact_id in self.expert_system.facts:
                fact = self.expert_system.facts[fact_id]
                if isinstance(fact, NextQuestion):
                    # Found a NextQuestion fact, check if it's already answered
                    is_answered = any(isinstance(f, Answer) and f['ident'] == fact['ident']
                                      for f_id, f in self.expert_system.facts.items())
                    if not is_answered:
                        next_question_fact = fact
                        break

            if next_question_fact:
                # If a new question needs to be asked
                self.handle_question(next_question_fact['ident'])
                self.waiting_for_answer = True  # Set flag, GUI is now waiting for user input
            elif not self.diagnosis_complete:
                # If no more questions are being asked, and diagnosis isn't complete yet,
                # it means the engine has reached its conclusion.
                self.diagnosis_complete = True  # Mark as complete to avoid re-entering this branch
                if hasattr(self.expert_system, 'best_diagnosis') and self.expert_system.best_diagnosis:
                    self.show_diagnosis_results()
                else:
                    self.show_no_diagnosis_message()

            # If diagnosis_complete is True, no further action is needed until reset.

        except Exception as e:
            self.handle_diagnosis_error(str(e))

    def handle_question(self, question_ident):
        """Handle a question by displaying it in the GUI."""
        try:
            question_data = get_question_by_ident(question_ident)
            if not question_data:
                raise ValueError(
                    f"Question with ident '{question_ident}' not found.")

            self.current_question = {
                'ident': question_ident,
                'text': question_data['text'],
                'valid_responses': question_data['valid'],
                'type': question_data['Type']
            }
            self.display_question()

        except Exception as e:
            messagebox.showerror("Error", f"Error handling question: {str(e)}")

    def display_question(self):
        """Display the current question in the GUI."""
        if not self.current_question:
            return

        question_text = self.current_question['text']
        valid_responses = self.current_question['valid_responses']
        question_type = self.current_question['type']

        self.question_text.config(state='normal')
        self.question_text.delete(1.0, tk.END)
        self.question_text.insert(1.0, f"🤔 {question_text}")
        self.question_text.config(state='disabled')

        for widget in self.answer_frame.winfo_children():
            widget.destroy()

        if question_type == 'number':
            self.create_number_input()
        elif "Select all that apply" in question_text:
            self.create_multiple_choice_input(
                valid_responses, allow_multiple=True)
        else:
            self.create_multiple_choice_input(
                valid_responses, allow_multiple=False)

    def create_number_input(self):
        """Create number input widget."""
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

        self.number_entry.bind(
            '<Return>', lambda e: self.submit_number_answer())

    def create_multiple_choice_input(self, valid_responses, allow_multiple=False):
        """Create multiple choice input widgets."""
        input_frame = ttk.Frame(self.answer_frame)
        input_frame.pack(fill='both', expand=True, pady=10)

        if allow_multiple:
            ttk.Label(input_frame, text="Select all that apply:",
                      font=('Segoe UI', 11)).pack(anchor='w')
        else:
            ttk.Label(input_frame, text="Select your answer:",
                      font=('Segoe UI', 11)).pack(anchor='w')

        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill='both', expand=True, pady=(10, 0))

        if allow_multiple:
            # Use checkboxes for multiple selection
            self.checkbox_vars = {}
            for option in valid_responses:
                display_text = option.replace('_', ' ').title()
                var = tk.BooleanVar()
                self.checkbox_vars[option] = var
                checkbox = ttk.Checkbutton(
                    button_frame, text=display_text, variable=var)
                checkbox.pack(anchor='w', pady=2)
        else:
            # Use radio buttons for single selection
            self.choice_var = tk.StringVar()
            for i, option in enumerate(valid_responses):
                display_text = option.replace('_', ' ').title()
                radio_button = ttk.Radiobutton(button_frame, text=display_text,
                                               variable=self.choice_var, value=option)
                radio_button.pack(anchor='w', pady=2)
                if i == 0:
                    radio_button.invoke()

        submit_button = ttk.Button(input_frame, text="Submit Answer",
                                   style='Primary.TButton', command=self.submit_choice_answer)
        submit_button.pack(anchor='w', pady=(15, 0))

    def submit_number_answer(self):
        """Submit number answer."""
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
        """Submit multiple choice answer."""
        try:
            if hasattr(self, 'checkbox_vars'):
                # Multiple selection - get all checked options
                selected_options = [option for option,
                                    var in self.checkbox_vars.items() if var.get()]
                if not selected_options:
                    messagebox.showerror(
                        "No Selection", "Please select at least one answer.")
                    return
                # Join multiple selections with commas
                answer = ",".join(selected_options)
            else:
                # Single selection
                answer = self.choice_var.get()
                if not answer:
                    messagebox.showerror(
                        "No Selection", "Please select an answer.")
                    return

            self.process_answer(answer)
        except Exception as e:
            messagebox.showerror("Error", f"Error submitting answer: {str(e)}")

    def process_answer(self, answer):
        """Process the submitted answer."""
        try:
            if not self.current_question:
                return

            question_ident = self.current_question['ident']

            # Declare the answer as a fact in the expert system
            self.expert_system.declare(
                Answer(ident=question_ident, text=answer))

            # Clear the current question state
            self.current_question = None
            self.waiting_for_answer = False  # Reset the flag

            # Schedule the next processing cycle for the expert system
            self.root.after(100, self.process_expert_system)

        except Exception as e:
            messagebox.showerror("Error", f"Error processing answer: {str(e)}")

    def handle_diagnosis_error(self, error_message):
        """Handle errors during diagnosis process."""
        self.progress_bar.stop()
        self.update_status("Error occurred", 'accent')
        messagebox.showerror(
            "Diagnosis Error", f"An error occurred during diagnosis: {error_message}")
        self.reset_diagnosis()

    def show_diagnosis_results(self):
        """Display the diagnosis results."""
        self.progress_bar.stop()
        self.update_status("Diagnosis complete", 'success')

        self.question_frame.grid_remove()
        self.results_frame.grid()

        best_diagnosis = self.expert_system.best_diagnosis

        self.results_text.config(state='normal')
        self.results_text.delete(1.0, tk.END)

        if best_diagnosis:
            disease = best_diagnosis.get('disease', 'Unknown condition')
            confidence = best_diagnosis.get('cf', 0.0) * 100
            reasoning = best_diagnosis.get(
                'reasoning', 'No reasoning available')

            self.results_text.insert(tk.END, "🏥 DIAGNOSIS RESULTS\n")
            self.results_text.insert(tk.END, "=" * 50 + "\n\n")
            self.results_text.insert(
                tk.END, f"📋 Primary Diagnosis: {disease}\n")
            if self.show_confidence.get():
                self.results_text.insert(
                    tk.END, f"   Confidence: {confidence:.1f}%\n")
            if self.detailed_reasoning.get():
                self.results_text.insert(
                    tk.END, f"   Reasoning: {reasoning}\n")
            self.results_text.insert(tk.END, "\n")

            # Add recommendations section
            self.results_text.insert(tk.END, "\n" + "=" * 50 + "\n")
            self.results_text.insert(tk.END, "📋 RECOMMENDATIONS\n")
            self.results_text.insert(tk.END, "=" * 50 + "\n\n")

            recommendations = self.get_recommendations([best_diagnosis])
            for rec in recommendations:
                self.results_text.insert(tk.END, f"• {rec}\n")

            # Get AI explanation if available
            if self.ai_enabled.get():
                try:
                    ai_explanation = self.expert_system.get_llm_explanation_only()
                    if ai_explanation:
                        self.results_text.insert(
                            tk.END, f"\n\n🤖 AI-POWERED MEDICAL EXPLANATION:\n{ai_explanation}\n")
                except Exception as e:
                    self.results_text.insert(
                        tk.END, f"\n\n⚠️ AI explanation unavailable: {str(e)}\n")

        self.results_text.config(state='disabled')
        self.create_results_buttons()
        self.notebook.select(0)  # Stay on diagnosis tab

    def show_no_diagnosis_message(self):
        """Show message when no diagnosis is available."""
        self.progress_bar.stop()
        self.update_status("No diagnosis available", 'warning')

        self.question_frame.grid_remove()
        self.results_frame.grid()

        self.results_text.config(state='normal')
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "⚠️ INSUFFICIENT INFORMATION\n")
        self.results_text.insert(tk.END, "=" * 50 + "\n\n")
        self.results_text.insert(
            tk.END, "Unable to make a diagnosis based on the provided information.\n\n")
        self.results_text.insert(tk.END, "Possible reasons:\n")
        self.results_text.insert(
            tk.END, "• Symptoms don't match known patterns\n")
        self.results_text.insert(
            tk.END, "• Additional information may be required\n")
        self.results_text.insert(
            tk.END, "• Condition may require professional examination\n\n")
        self.results_text.insert(
            tk.END, "Please consult with a dermatologist or healthcare provider for proper evaluation.")
        self.results_text.config(state='disabled')
        self.create_results_buttons()
        self.notebook.select(0)  # Stay on diagnosis tab

    def get_recommendations(self, diagnosis_results):
        """Generate recommendations based on diagnosis."""
        recommendations = []
        recommendations.append(
            "Consult with a dermatologist for professional confirmation and treatment plan")
        recommendations.append("Avoid scratching or picking at affected areas")
        recommendations.append("Keep the affected area clean and dry")

        for diag_info in diagnosis_results:
            condition = diag_info.get('disease', '').lower()

            if 'eczema' in condition or 'dermatitis' in condition:
                recommendations.extend([
                    "Use gentle, fragrance-free moisturizers regularly",
                    "Avoid known triggers (allergens, irritants)",
                    "Consider cool compresses for relief"
                ])
            elif 'psoriasis' in condition:
                recommendations.extend([
                    "Consider topical treatments as prescribed",
                    "Manage stress levels",
                    "Protect skin from injury"
                ])
            elif 'fungal' in condition or 'ringworm' in condition:
                recommendations.extend([
                    "Keep affected area dry",
                    "Avoid sharing personal items",
                    "Consider antifungal treatments"
                ])
            elif 'acne' in condition:
                recommendations.extend([
                    "Use gentle, non-comedogenic skincare products",
                    "Avoid excessive washing or harsh scrubbing",
                    "Consider topical treatments"
                ])
            elif 'cancer' in condition or 'melanoma' in condition or 'carcinoma' in condition:
                recommendations.extend([
                    "⚠️ URGENT: Seek immediate medical attention",
                    "Schedule appointment with dermatologist as soon as possible",
                    "Protect from sun exposure"
                ])
        return list(set(recommendations))

    def create_results_buttons(self):
        """Create action buttons for results screen."""
        button_frame = ttk.Frame(self.results_frame)
        button_frame.grid(row=1, column=0, sticky='ew', pady=(15, 0))

        ttk.Button(button_frame, text="🔄 Start New Diagnosis",
                   style='Primary.TButton', command=self.reset_diagnosis).pack(side='left', padx=(0, 10))
        ttk.Button(button_frame, text="💾 Save Results",
                   style='Success.TButton', command=self.save_results).pack(side='left', padx=(0, 10))
        ttk.Button(button_frame, text="🖨️ Print Results",
                   command=self.print_results).pack(side='left')

    def reset_diagnosis(self):
        """Reset the diagnosis interface for a new session."""
        self.expert_system = None
        self.current_question = None
        self.diagnosis_complete = False
        self.waiting_for_answer = False

        self.progress_bar.stop()
        self.update_status("Ready", 'success')

        self.welcome_frame.grid()
        self.question_frame.grid_remove()
        self.results_frame.grid_remove()

        self.start_button.config(state='normal')

        self.results_text.config(state='normal')
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state='disabled')

    def save_results(self):
        """Save diagnosis results to file."""
        try:
            from tkinter import filedialog
            import datetime

            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="Save Diagnosis Results"
            )

            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("DERMATOLOGY EXPERT SYSTEM - DIAGNOSIS REPORT\n")
                    f.write("=" * 50 + "\n")
                    f.write(
                        f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    results_content = self.results_text.get(1.0, tk.END)
                    f.write(results_content)
                    f.write("\n\n" + "=" * 50 + "\n")
                    f.write(
                        "DISCLAIMER: This report is generated by an AI-based expert system\n")
                    f.write(
                        "and should not replace professional medical consultation.\n")
                    f.write(
                        "Always consult qualified healthcare professionals for proper\n")
                    f.write("diagnosis and treatment.\n")
                messagebox.showinfo("Success", f"Results saved to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving results: {str(e)}")

    def print_results(self):
        """Print diagnosis results."""
        try:
            import tempfile
            import os
            import subprocess

            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
                html_content = self.generate_html_report()
                f.write(html_content)
                temp_filename = f.name

            if os.name == 'nt':
                os.startfile(temp_filename)
            elif os.name == 'posix':
                subprocess.run(['open', temp_filename] if os.uname().sysname == 'Darwin'
                               else ['xdg-open', temp_filename])
        except Exception as e:
            messagebox.showerror("Error", f"Error printing results: {str(e)}")

    def generate_html_report(self):
        """Generate HTML report for printing."""
        import datetime
        results_content = self.results_text.get(1.0, tk.END)
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Dermatology Diagnosis Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
                .header {{ text-align: center; border-bottom: 2px solid #2C3E50; padding-bottom: 20px; margin-bottom: 30px; }}
                .content {{ white-space: pre-wrap; }}
                .disclaimer {{ background-color: #f8f9fa; padding: 15px; border-left: 4px solid #F39C12; margin-top: 30px; }}
                @media print {{ body {{ margin: 20px; }} }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Dermatology Expert System</h1>
                <h2>Diagnosis Report</h2>
                <p>Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            <div class="content">
{results_content}
            </div>
            <div class="disclaimer">
                <strong>DISCLAIMER:</strong> This report is generated by an AI-based expert system
                and should not replace professional medical consultation. Always consult qualified
                healthcare professionals for proper diagnosis and treatment.
            </div>
        </body>
        </html>
        """
        return html

    def save_settings(self):
        """Save application settings."""
        try:
            messagebox.showinfo("Settings", "Settings saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving settings: {str(e)}")

    def update_status(self, message, status_type='secondary'):
        """Update the status display."""
        try:
            self.status_label.config(
                text=message, foreground=self.colors[status_type])
            self.root.update_idletasks()
        except Exception as e:
            print(f"Error updating status: {str(e)}")

    def run(self):
        """Start the GUI application."""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\nApplication terminated by user")
        except Exception as e:
            print(f"Application error: {str(e)}")
            messagebox.showerror(
                "Fatal Error", f"Application encountered a fatal error: {str(e)}")


def main():
    """Main function to run the application."""
    try:
        app = ModernDermatologyGUI()
        app.run()
    except Exception as e:
        print(f"Failed to start application: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
