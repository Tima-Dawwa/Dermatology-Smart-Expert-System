from ExpertSystem.engine import *
from ExpertSystem.Questions.question_flow import *
from tkinter import ttk, messagebox, scrolledtext
import tkinter as tk


class ModernFreshDermatologyGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_main_window()
        self.setup_modern_styles()
        self.create_main_interface()
        self.expert_system = None
        self.current_question = None
        self.diagnosis_complete = False
        self.waiting_for_answer = False

        # These variables are kept as they are used by expert_system initialization or result display.
        self.ai_enabled = tk.BooleanVar(value=True)
        self.model_var = tk.StringVar(value="microsoft/DialoGPT-medium")
        self.show_confidence = tk.BooleanVar(value=True)
        self.detailed_reasoning = tk.BooleanVar(value=True)

    def setup_main_window(self):
        """Configure the main window with modern fresh styling"""
        self.root.title("🩺 Dermatology Expert System")
        self.root.geometry("1300x900")
        self.root.minsize(1100, 750)

        # Modern gradient background
        self.root.configure(bg='#F8FAFC')

        # Configure grid weights for responsive design
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Modern fresh color palette
        self.colors = {
            'primary': '#6366F1',           # Indigo
            'primary_hover': '#5B21B6',      # Purple hover
            'secondary': '#10B981',         # Emerald
            'accent': '#F59E0B',            # Amber
            'danger': '#EF4444',            # Red
            'success': '#22C55E',           # Green
            'warning': '#F97316',           # Orange
            'info': '#3B82F6',              # Blue

            # Neutrals
            'white': '#FFFFFF',
            'gray_50': '#F9FAFB',
            'gray_100': '#F3F4F6',
            'gray_200': '#E5E7EB',
            'gray_300': '#D1D5DB',
            'gray_400': '#9CA3AF',
            'gray_500': '#6B7280',
            'gray_600': '#4B5563',
            'gray_700': '#374151',
            'gray_800': '#1F2937',
            'gray_900': '#111827',

            # Background
            'bg_primary': '#F8FAFC',
            'bg_secondary': '#F1F5F9',
            'bg_card': '#FFFFFF',

            # Text
            'text_primary': '#1E293B',
            'text_secondary': '#64748B',
            'text_muted': '#94A3B8'
        }

    def setup_modern_styles(self):
        """Configure modern fresh ttk styles"""
        style = ttk.Style()

        # Use clam as base for better customization
        style.theme_use('clam')

        # Modern Primary Button
        style.configure('ModernPrimary.TButton',
                        background=self.colors['primary'],
                        foreground='white',
                        borderwidth=0,
                        focuscolor='none',
                        padding=(15, 10),  # Adjusted padding
                        font=('Segoe UI', 9, 'bold'))  # Adjusted font size

        style.map('ModernPrimary.TButton',
                  background=[('active', self.colors['primary_hover']),
                              ('pressed', '#4C1D95')])

        # Modern Secondary Button
        style.configure('ModernSecondary.TButton',
                        background=self.colors['secondary'],
                        foreground='white',
                        borderwidth=0,
                        focuscolor='none',
                        padding=(12, 8),  # Adjusted padding
                        font=('Segoe UI', 8, 'bold'))  # Adjusted font size

        style.map('ModernSecondary.TButton',
                  background=[('active', '#059669')])

        # Modern Danger Button
        style.configure('ModernDanger.TButton',
                        background=self.colors['danger'],
                        foreground='white',
                        borderwidth=0,
                        focuscolor='none',
                        padding=(12, 8),  # Adjusted padding
                        font=('Segoe UI', 8, 'bold'))  # Adjusted font size

        # Modern Ghost Button
        style.configure('ModernGhost.TButton',
                        background=self.colors['gray_100'],
                        foreground=self.colors['text_primary'],
                        borderwidth=1,
                        relief='flat',
                        focuscolor='none',
                        padding=(12, 8),  # Adjusted padding
                        font=('Segoe UI', 9))

        style.map('ModernGhost.TButton',
                  background=[('active', self.colors['gray_200'])])

        # Modern Card Frame
        style.configure('ModernCard.TFrame',
                        background=self.colors['bg_card'],
                        relief='flat',
                        borderwidth=0)

        # Modern Main Frame
        style.configure('ModernMain.TFrame',
                        background=self.colors['bg_primary'],
                        relief='flat',
                        borderwidth=0)

        # Modern Section Frame
        style.configure('ModernSection.TFrame',
                        background=self.colors['bg_secondary'],
                        relief='flat',
                        borderwidth=0)

        # Modern Labels
        style.configure('ModernHeading.TLabel',
                        background=self.colors['bg_card'],
                        foreground=self.colors['text_primary'],
                        font=('Segoe UI', 16, 'bold'))  # Adjusted font size

        style.configure('ModernSubheading.TLabel',
                        background=self.colors['bg_card'],
                        foreground=self.colors['text_secondary'],
                        font=('Segoe UI', 10))  # Adjusted font size

        style.configure('ModernTitle.TLabel',
                        background=self.colors['bg_card'],
                        foreground=self.colors['text_primary'],
                        font=('Segoe UI', 12, 'bold'))  # Adjusted font size

        style.configure('ModernMuted.TLabel',
                        background=self.colors['bg_card'],
                        foreground=self.colors['text_muted'],
                        font=('Segoe UI', 8))  # Adjusted font size

        # Modern Status Labels
        style.configure('ModernSuccess.TLabel',
                        background=self.colors['bg_primary'],
                        foreground=self.colors['success'],
                        font=('Segoe UI', 9, 'bold'))  # Adjusted font size

        style.configure('ModernWarning.TLabel',
                        background=self.colors['bg_primary'],
                        foreground=self.colors['warning'],
                        font=('Segoe UI', 9, 'bold'))  # Adjusted font size

        style.configure('ModernDanger.TLabel',
                        background=self.colors['bg_primary'],
                        foreground=self.colors['danger'],
                        font=('Segoe UI', 9, 'bold'))  # Adjusted font size

        # Modern Input Styles
        style.configure('Modern.TCheckbutton',
                        background=self.colors['bg_card'],
                        foreground=self.colors['text_primary'],
                        font=('Segoe UI', 9),  # Adjusted font size
                        focuscolor='none')

        style.configure('Modern.TRadiobutton',
                        background=self.colors['bg_card'],
                        foreground=self.colors['text_primary'],
                        font=('Segoe UI', 9),  # Adjusted font size
                        focuscolor='none')

        style.configure('Modern.TEntry',
                        borderwidth=1,
                        relief='solid',
                        padding=8,  # Adjusted padding
                        font=('Segoe UI', 10))  # Adjusted font size

        # Modern LabelFrame
        style.configure('Modern.TLabelframe',
                        background=self.colors['bg_card'],
                        borderwidth=0,
                        relief='flat')

        style.configure('Modern.TLabelframe.Label',
                        background=self.colors['bg_card'],
                        foreground=self.colors['text_primary'],
                        font=('Segoe UI', 11, 'bold'))  # Adjusted font size

        # Modern Notebook
        style.configure('Modern.TNotebook',
                        background=self.colors['bg_primary'],
                        borderwidth=0)

        style.configure('Modern.TNotebook.Tab',
                        background=self.colors['gray_200'],
                        foreground=self.colors['text_primary'],
                        padding=(15, 10),  # Adjusted padding
                        font=('Segoe UI', 9, 'bold'))  # Adjusted font size

        style.map('Modern.TNotebook.Tab',
                  background=[('selected', self.colors['bg_card']),
                              ('active', self.colors['gray_300'])])

    def create_main_interface(self):
        """Create the main interface layout with modern design"""
        # Main container with shadow effect simulation
        main_container = tk.Frame(self.root, bg=self.colors['bg_primary'])
        # Reduced padx/pady from 20 to 15
        main_container.grid(row=0, column=0, sticky='nsew', padx=15, pady=15)
        main_container.grid_rowconfigure(1, weight=1)
        main_container.grid_columnconfigure(0, weight=1)

        # Create shadow effect
        shadow_frame = tk.Frame(
            main_container, bg=self.colors['gray_300'], height=2)
        shadow_frame.grid(row=0, column=0, sticky='ew', padx=5, pady=(5, 0))

        # Main content frame
        content_frame = tk.Frame(main_container, bg=self.colors['bg_card'])
        content_frame.grid(row=1, column=0, sticky='nsew')
        content_frame.grid_rowconfigure(1, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)

        # Header
        self.create_modern_header(content_frame)

        # Content area with notebook tabs
        self.create_modern_content_area(content_frame)

        # Footer
        self.create_modern_footer(content_frame)

    def create_modern_header(self, parent):
        """Create the modern header section"""
        # Reduced height from 90 to 70 for more vertical space
        header_frame = tk.Frame(parent, bg=self.colors['bg_card'], height=70)
        # Reduced pady from (30, 20) to (20, 15)
        header_frame.grid(row=0, column=0, sticky='ew', padx=30, pady=(20, 15))
        header_frame.grid_columnconfigure(1, weight=1)
        header_frame.grid_propagate(False)

        # Medical icon with modern styling
        icon_frame = tk.Frame(
            header_frame, bg=self.colors['primary'], width=60, height=60)  # Adjusted size
        icon_frame.grid(row=0, column=0, padx=(0, 15),
                        pady=5)  # Adjusted padx/pady
        icon_frame.grid_propagate(False)

        icon_label = tk.Label(icon_frame, text="🩺", font=('Segoe UI Emoji', 24),  # Adjusted font size
                              fg='white', bg=self.colors['primary'])
        icon_label.place(relx=0.5, rely=0.5, anchor='center')

        # Title section
        title_frame = tk.Frame(header_frame, bg=self.colors['bg_card'])
        title_frame.grid(row=0, column=1, sticky='w', pady=5)  # Adjusted pady

        title_label = tk.Label(title_frame, text="Dermatology Expert System",
                               bg=self.colors['bg_card'], fg=self.colors['text_primary'],
                               font=('Segoe UI', 18, 'bold'))  # Adjusted font size
        title_label.pack(anchor='w')

        subtitle_label = tk.Label(title_frame,
                                  text="AI-Powered Skin Condition Analysis & Diagnosis",
                                  bg=self.colors['bg_card'], fg=self.colors['text_secondary'],
                                  font=('Segoe UI', 10))  # Adjusted font size
        subtitle_label.pack(anchor='w', pady=(0, 0))

        # Status section with modern badge
        self.status_frame = tk.Frame(header_frame, bg=self.colors['bg_card'])
        self.status_frame.grid(row=0, column=2, padx=(
            15, 0), pady=5)  # Adjusted padx/pady

        status_container = tk.Frame(self.status_frame, bg=self.colors['success'],
                                    relief='flat', bd=0)
        status_container.pack()

        self.status_label = tk.Label(status_container, text="● Ready",
                                     fg='white', bg=self.colors['success'],
                                     font=('Segoe UI', 9, 'bold'), padx=12, pady=6)  # Adjusted padx/pady/font
        self.status_label.pack()

    def create_modern_content_area(self, parent):
        """Create the modern content area with tabs"""
        self.notebook = ttk.Notebook(parent, style='Modern.TNotebook')
        self.notebook.grid(row=1, column=0, sticky='nsew',
                           padx=20, pady=(5, 5))  # Adjusted padx/pady

        # Diagnosis Tab
        self.diagnosis_frame = ttk.Frame(
            self.notebook, style='ModernCard.TFrame')
        self.notebook.add(self.diagnosis_frame, text='   🔍 Diagnosis   ')
        self.create_modern_diagnosis_tab()

    def create_modern_diagnosis_tab(self):
        """Create the modern diagnosis interface"""
        self.diagnosis_frame.grid_rowconfigure(1, weight=1)
        self.diagnosis_frame.grid_columnconfigure(0, weight=1)

        # Welcome section with modern card design
        self.welcome_frame = tk.Frame(
            self.diagnosis_frame, bg=self.colors['bg_card'])
        # Adjusted pady to (15, 10)
        self.welcome_frame.grid(
            row=0, column=0, sticky='ew', padx=20, pady=(15, 10))

        # Welcome card with gradient-like effect
        welcome_card = tk.Frame(
            self.welcome_frame, bg=self.colors['gray_50'], relief='flat', bd=0)
        welcome_card.pack(fill='x', padx=3, pady=3)  # Adjusted padx/pady

        welcome_inner = tk.Frame(welcome_card, bg='white', relief='flat', bd=0)
        welcome_inner.pack(fill='x', padx=1, pady=1)  # Adjusted padx/pady

        # Welcome header
        welcome_header = tk.Label(welcome_inner, text="🌟 Welcome to Your Personal Dermatology Assistant",
                                  bg='white', fg=self.colors['text_primary'],
                                  font=('Segoe UI', 14, 'bold'))  # Adjusted font size
        # Adjusted padx/pady
        welcome_header.pack(anchor='w', padx=20, pady=(15, 8))

        welcome_text = """Our advanced AI system will guide you through a comprehensive assessment to help identify potential skin conditions. Simply answer the questions honestly and thoroughly for the most accurate results."""

        welcome_label = tk.Label(welcome_inner, text=welcome_text,
                                 # Adjusted font size
                                 font=('Segoe UI', 10), bg='white',
                                 fg=self.colors['text_secondary'], wraplength=900,
                                 justify='left')
        welcome_label.pack(anchor='w', padx=20, pady=(0, 15)
                           )  # Adjusted padx/pady

        # Start button with modern styling
        button_frame = tk.Frame(welcome_inner, bg='white')
        button_frame.pack(anchor='w', padx=20, pady=(0, 20)
                          )  # Adjusted padx/pady

        self.start_button = ttk.Button(button_frame, text="🚀 Begin Assessment",
                                       style='ModernPrimary.TButton',
                                       command=self.start_diagnosis)
        self.start_button.pack(side='left')

        # Question area with modern card
        self.question_frame = tk.Frame(
            self.diagnosis_frame, bg=self.colors['bg_card'])
        self.question_frame.grid(
            row=1, column=0, sticky='nsew', padx=20, pady=5)  # Adjusted padx/pady
        self.question_frame.grid_rowconfigure(1, weight=1)
        self.question_frame.grid_columnconfigure(0, weight=1)

        # Question card
        question_card = tk.Frame(
            self.question_frame, bg='white', relief='flat', bd=0)
        question_card.grid(row=0, column=0, sticky='nsew',
                           padx=3, pady=3)  # Adjusted padx/pady
        question_card.grid_rowconfigure(1, weight=1)
        question_card.grid_columnconfigure(0, weight=1)

        # Question header
        question_header = tk.Frame(
            question_card, bg=self.colors['primary'], height=40)  # Reduced height
        question_header.grid(row=0, column=0, sticky='ew')
        question_header.grid_propagate(False)

        question_title = tk.Label(question_header, text="💭 Assessment Questions",
                                  bg=self.colors['primary'], fg='white',
                                  font=('Segoe UI', 12, 'bold'))  # Adjusted font size
        question_title.place(relx=0.5, rely=0.5, anchor='center')

        # Question content
        question_content = tk.Frame(question_card, bg='white')
        question_content.grid(row=1, column=0, sticky='nsew',
                              padx=20, pady=15)  # Adjusted padx/pady
        question_content.grid_rowconfigure(1, weight=1)
        question_content.grid_columnconfigure(0, weight=1)

        # Question text with modern styling
        self.question_text = tk.Text(question_content, height=2, wrap='word',  # Reduced height
                                     # Adjusted font size
                                     font=('Segoe UI', 11), bg=self.colors['gray_50'],
                                     fg=self.colors['text_primary'], state='disabled',
                                     relief='flat', padx=15, pady=10, bd=0)  # Adjusted padx/pady
        self.question_text.grid(
            row=0, column=0, sticky='ew', pady=(0, 15))  # Adjusted pady

        # Answer area
        self.answer_frame = tk.Frame(question_content, bg='white')
        self.answer_frame.grid(row=1, column=0, sticky='nsew')
        self.answer_frame.grid_columnconfigure(0, weight=1)

        # Progress section
        progress_section = tk.Frame(
            self.diagnosis_frame, bg=self.colors['bg_card'])
        progress_section.grid(row=2, column=0, sticky='ew',
                              padx=20, pady=(5, 10))  # Adjusted padx/pady

        progress_card = tk.Frame(
            progress_section, bg='white', relief='flat', bd=0)
        progress_card.pack(fill='x', padx=3, pady=3)  # Adjusted padx/pady

        progress_inner = tk.Frame(progress_card, bg='white')
        progress_inner.pack(fill='x', padx=15, pady=10)  # Adjusted padx/pady

        progress_label = tk.Label(progress_inner, text="Assessment Progress",
                                  bg='white', fg=self.colors['text_primary'],
                                  font=('Segoe UI', 9, 'bold'))  # Adjusted font size
        progress_label.pack(anchor='w')

        self.progress_bar = ttk.Progressbar(progress_inner, mode='indeterminate',
                                            style='TProgressbar')
        self.progress_bar.pack(fill='x', pady=(6, 0))  # Adjusted pady

        # Results area with modern design
        self.results_frame = tk.Frame(
            self.diagnosis_frame, bg=self.colors['bg_card'])
        self.results_frame.grid(
            row=3, column=0, sticky='ew', padx=20, pady=(5, 20))  # Adjusted padx/pady
        self.results_frame.grid_columnconfigure(0, weight=1)

        results_card = tk.Frame(
            self.results_frame, bg='white', relief='flat', bd=0)
        results_card.grid(row=0, column=0, sticky='ew',
                          padx=3, pady=3)  # Adjusted padx/pady
        results_card.grid_columnconfigure(0, weight=1)

        # Results header
        results_header = tk.Frame(
            results_card, bg=self.colors['secondary'], height=40)  # Reduced height
        results_header.grid(row=0, column=0, sticky='ew')
        results_header.grid_propagate(False)

        results_title = tk.Label(results_header, text="📋 Assessment Results",
                                 bg=self.colors['secondary'], fg='white',
                                 font=('Segoe UI', 12, 'bold'))  # Adjusted font size
        results_title.place(relx=0.5, rely=0.5, anchor='center')

        # Results content
        results_content = tk.Frame(results_card, bg='white')
        results_content.grid(row=1, column=0, sticky='ew',
                             padx=20, pady=15)  # Adjusted padx/pady
        results_content.grid_columnconfigure(0, weight=1)

        self.results_text = scrolledtext.ScrolledText(results_content, height=8,  # Reduced height
                                                      # Adjusted font size
                                                      font=('Segoe UI', 9), state='disabled',
                                                      wrap='word', bg=self.colors['gray_50'],
                                                      relief='flat', bd=0, padx=10, pady=10)  # Adjusted padx/pady
        self.results_text.grid(row=0, column=0, sticky='ew')

        # Initially hide question and results areas
        self.question_frame.grid_remove()
        self.results_frame.grid_remove()

    def create_modern_footer(self, parent):
        """Create the modern footer section"""
        footer_frame = tk.Frame(
            parent, bg=self.colors['bg_card'], height=50)  # Reduced height
        # Adjusted pady to (15, 20)
        footer_frame.grid(row=2, column=0, sticky='ew', padx=20, pady=(15, 20))
        footer_frame.grid_columnconfigure(1, weight=1)
        footer_frame.grid_propagate(False)

        # Disclaimer with modern styling
        disclaimer_frame = tk.Frame(
            footer_frame, bg=self.colors['warning'], relief='flat', bd=0)
        disclaimer_frame.grid(row=0, column=0, sticky='w',
                              pady=5)  # Adjusted pady

        disclaimer_text = "⚠️ Medical Disclaimer: For assessment purposes only - Consult healthcare professionals"
        disclaimer_label = tk.Label(disclaimer_frame, text=disclaimer_text,
                                    fg='white', bg=self.colors['warning'],
                                    font=('Segoe UI', 8, 'bold'), padx=10, pady=6)  # Adjusted padx/pady/font
        disclaimer_label.pack()

        # Version info
        version_label = tk.Label(footer_frame, text="v2.0.0 | Modern Edition",
                                 bg=self.colors['bg_card'], fg=self.colors['text_muted'],
                                 font=('Segoe UI', 8))  # Adjusted font size
        version_label.grid(row=0, column=1, sticky='e',
                           pady=5)  # Adjusted pady

    def start_diagnosis(self):
        """Initialize and start the diagnosis process."""
        try:
            self.update_status("Initializing assessment...", 'warning')

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
            self.waiting_for_answer = False

            # Hide welcome and show question area
            self.welcome_frame.grid_remove()
            self.question_frame.grid()
            self.results_frame.grid_remove()

            # Start the diagnosis process
            self.update_status("Assessment in progress...", 'info')
            self.progress_bar.start()

            # Initialize the expert system with start fact
            self.expert_system.declare(Fact(start=True))

            # Begin the expert system processing loop
            self.root.after(100, self.process_expert_system)

        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to start assessment: {str(e)}")
            self.update_status("Error occurred", 'danger')
            self.start_button.config(state='normal')

    def process_expert_system(self):
        """Manages the expert system's execution cycle."""
        try:
            if self.waiting_for_answer:
                return

            self.expert_system.run()

            next_question_fact = None
            for fact_id in self.expert_system.facts:
                fact = self.expert_system.facts[fact_id]
                if isinstance(fact, NextQuestion):
                    is_answered = any(isinstance(f, Answer) and f['ident'] == fact['ident']
                                      for f_id, f in self.expert_system.facts.items())
                    if not is_answered:
                        next_question_fact = fact
                        break

            if next_question_fact:
                self.handle_question(next_question_fact['ident'])
                self.waiting_for_answer = True
            elif not self.diagnosis_complete:
                self.diagnosis_complete = True
                if hasattr(self.expert_system, 'best_diagnosis') and self.expert_system.best_diagnosis:
                    self.show_diagnosis_results()
                else:
                    self.show_no_diagnosis_message()

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
        """Display the current question in the GUI with modern styling."""
        if not self.current_question:
            return

        question_text = self.current_question['text']
        valid_responses = self.current_question['valid_responses']
        question_type = self.current_question['type']

        self.question_text.config(state='normal')
        self.question_text.delete(1.0, tk.END)
        self.question_text.insert(1.0, f"💭 {question_text}")
        self.question_text.config(state='disabled')

        for widget in self.answer_frame.winfo_children():
            widget.destroy()

        if question_type == 'number':
            self.create_modern_number_input()
        elif "Select all that apply" in question_text:
            self.create_modern_multiple_choice_input(
                valid_responses, allow_multiple=True)
        else:
            self.create_modern_multiple_choice_input(
                valid_responses, allow_multiple=False)

    def create_modern_number_input(self):
        """Create modern number input widget."""
        input_container = tk.Frame(self.answer_frame, bg='white')
        input_container.pack(fill='x', pady=10)  # Adjusted pady

        tk.Label(input_container, text="Please enter a numerical value:",
                 font=('Segoe UI', 10), bg='white', fg=self.colors['text_primary']).pack(anchor='w', pady=(0, 5))  # Adjusted font/pady

        self.number_entry = ttk.Entry(
            input_container, font=('Segoe UI', 11), width=30, style='Modern.TEntry')  # Adjusted font size
        self.number_entry.pack(anchor='w', pady=(0, 10))  # Adjusted pady
        self.number_entry.focus()

        submit_button = ttk.Button(input_container, text="Submit Answer",
                                   style='ModernPrimary.TButton', command=self.submit_number_answer)
        submit_button.pack(anchor='w')

        self.number_entry.bind(
            '<Return>', lambda e: self.submit_number_answer())

    def create_modern_multiple_choice_input(self, valid_responses, allow_multiple=False):
        """Create modern multiple choice input widgets with scrolling for many options."""
        input_container = tk.Frame(self.answer_frame, bg='white')
        input_container.pack(fill='both', expand=True,
                             pady=10)  # Adjusted pady

        if allow_multiple:
            tk.Label(input_container, text="Select all that apply:",
                     font=('Segoe UI', 10), bg='white', fg=self.colors['text_primary']).pack(anchor='w', pady=(0, 5))  # Adjusted font/pady
        else:
            tk.Label(input_container, text="Select your answer:",
                     font=('Segoe UI', 10), bg='white', fg=self.colors['text_primary']).pack(anchor='w', pady=(0, 5))  # Adjusted font/pady

        # Use a Canvas and Scrollbar for potentially many options
        canvas = tk.Canvas(
            input_container, bg=self.colors['gray_50'], highlightthickness=0, relief='flat', bd=0)
        canvas.pack(side=tk.LEFT, fill='both', expand=True,
                    pady=(5, 0))  # Adjusted pady

        scrollbar = ttk.Scrollbar(
            input_container, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill='y', pady=(5, 0))  # Adjusted pady

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")))

        # Frame to hold the actual buttons inside the canvas
        button_frame_inner = tk.Frame(
            canvas, bg=self.colors['gray_50'])  # Match canvas background
        canvas.create_window((0, 0), window=button_frame_inner,
                             anchor="nw", width=canvas.winfo_width())

        # Make the inner frame responsive to canvas width changes
        def on_canvas_configure(event):
            canvas.itemconfig(canvas.find_withtag(
                "button_frame_inner_id"), width=event.width)
            # Also update scrollregion explicitly after width changes might affect layout
            canvas.config(scrollregion=canvas.bbox("all"))

        canvas.bind('<Configure>', on_canvas_configure)
        canvas.itemconfigure(canvas.create_window(
            (0, 0), window=button_frame_inner, anchor="nw"), tags="button_frame_inner_id")

        # Configure button_frame_inner for responsive grid
        button_frame_inner.grid_columnconfigure(
            0, weight=1)  # Allow column to expand

        if allow_multiple:
            self.checkbox_vars = {}
            row_idx = 0
            for i, option in enumerate(valid_responses):
                display_text = option.replace('_', ' ').title()
                var = tk.BooleanVar()
                self.checkbox_vars[option] = var
                checkbox = ttk.Checkbutton(
                    button_frame_inner, text=display_text, variable=var,
                    style='Modern.TCheckbutton'
                )
                checkbox.grid(row=row_idx, column=0, sticky='w',
                              pady=3, padx=8)  # Adjusted pady/padx
                row_idx += 1
        else:
            self.choice_var = tk.StringVar()
            row_idx = 0
            for i, option in enumerate(valid_responses):
                display_text = option.replace('_', ' ').title()
                radio_button = ttk.Radiobutton(button_frame_inner, text=display_text,
                                               variable=self.choice_var, value=option,
                                               style='Modern.TRadiobutton'
                                               )
                # Adjusted pady/padx
                radio_button.grid(row=row_idx, column=0,
                                  sticky='w', pady=3, padx=8)
                if i == 0:
                    radio_button.invoke()
                row_idx += 1

        # Update scrollregion after all widgets are placed
        button_frame_inner.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        submit_button = ttk.Button(input_container, text="Submit Answer",
                                   style='ModernPrimary.TButton', command=self.submit_choice_answer)
        submit_button.pack(anchor='w', pady=(15, 0))  # Adjusted pady

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
        self.update_status("Error occurred", 'danger')
        messagebox.showerror(
            "Diagnosis Error", f"An error occurred during diagnosis: {error_message}")
        self.reset_diagnosis()

    def show_diagnosis_results(self):
        """Display the diagnosis results."""
        self.progress_bar.stop()
        self.update_status("Assessment complete", 'success')

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

    def create_results_buttons(self):
        """Create action buttons for results screen."""
        button_frame = tk.Frame(self.results_frame, bg='white')
        button_frame.grid(row=1, column=0, sticky='ew',
                          padx=20, pady=(15, 0))  # Adjusted padx/pady

        ttk.Button(button_frame, text="🔄 Start New Assessment",
                   style='ModernPrimary.TButton', command=self.reset_diagnosis).pack(side='left', padx=(0, 10))  # Adjusted padx
        ttk.Button(button_frame, text="💾 Save Results",
                   style='ModernSecondary.TButton', command=self.save_results).pack(side='left', padx=(0, 10))  # Adjusted padx

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

    def update_status(self, message, status_type='info'):
        """Update the status display with modern fresh styles."""
        try:
            # Update background and foreground based on status_type
            if status_type == 'success':
                bg_color = self.colors['success']
            elif status_type == 'warning':
                bg_color = self.colors['warning']
            elif status_type == 'danger':
                bg_color = self.colors['danger']
            elif status_type == 'info':
                bg_color = self.colors['info']
            else:
                bg_color = self.colors['gray_500']

            self.status_label.config(
                text=f"● {message}", fg='white', bg=bg_color)
            self.status_label.master.config(bg=bg_color)
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
        app = ModernFreshDermatologyGUI()
        app.run()
    except Exception as e:
        print(f"Failed to start application: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
