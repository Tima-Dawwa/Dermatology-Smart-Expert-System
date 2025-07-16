import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import datetime
import os
import subprocess
import tempfile
import queue
from threading import Thread
import datetime
from AI.llm import explain_result_with_llm

# Re-import all necessary Experta and ExpertSystem components
from experta import Fact
from ExpertSystem.facts import Answer, NextQuestion
from ExpertSystem.Questions.question import get_question_by_ident


class ModernFreshDermatologyGUI:
    def __init__(self, engine_class):
        self.root = tk.Tk()
        self.setup_main_window()
        self.setup_modern_styles()
        self.create_main_interface()

        self.engine_class = engine_class
        self.expert_system = None
        self.current_question = None
        self.diagnosis_complete = False
        self.waiting_for_answer = False

        self.engine_queue = queue.Queue()
        self.root.after(100, self.process_engine_queue)

        self.ai_enabled = tk.BooleanVar(value=False)
        self.model_var = tk.StringVar(value="No AI Model (LLM Disabled)")
        self.show_confidence = tk.BooleanVar(value=True)
        self.detailed_reasoning = tk.BooleanVar(value=True)

        # --- NEW: Centralized Tkinter Variable Initialization ---
        # These will be the persistent Tkinter variables for input widgets.
        # For single-line text entry (like number inputs)
        self.answer_text_var = tk.StringVar()
        self.choice_radio_var = tk.StringVar()  # For single-choice radio buttons
        # A dictionary to hold BooleanVars for multi-select checkboxes
        self.checkbox_vars_dict = {}
        # --- END NEW ---

    def setup_main_window(self):
        self.root.title("🩺 Dermatology Expert System")
        self.root.geometry("1300x900")
        self.root.minsize(1100, 750)
        self.root.configure(bg='#F8FAFC')
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.colors = {
            'primary': '#6366F1', 'primary_hover': '#5B21B6', 'secondary': '#10B981', 'accent': '#F59E0B',
            'danger': '#EF4444', 'success': '#22C55E', 'warning': '#F97316', 'info': '#3B82F6',
            'white': '#FFFFFF', 'gray_50': '#F9FAFB', 'gray_100': '#F3F4F6', 'gray_200': '#E5E7EB',
            'gray_300': '#D1D5DB', 'gray_400': '#9CA3AF', 'gray_500': '#6B7280', 'gray_600': '#4B5563',
            'gray_700': '#374151', 'gray_800': '#1F2937', 'gray_900': '#111827',
            'bg_primary': '#F8FAFC', 'bg_secondary': '#F1F5F9', 'bg_card': '#FFFFFF',
            'text_primary': '#1E293B', 'text_secondary': '#64748B', 'text_muted': '#94A3B8'
        }

    def setup_modern_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        style.configure('ModernPrimary.TButton', background=self.colors['primary'], foreground='white', borderwidth=0, focuscolor='none', padding=(
            15, 10), font=('Segoe UI', 9, 'bold'))
        style.map('ModernPrimary.TButton', background=[
                  ('active', self.colors['primary_hover']), ('pressed', '#4C1D95')])

        style.configure('ModernSecondary.TButton', background=self.colors['secondary'], foreground='white', borderwidth=0, focuscolor='none', padding=(
            12, 8), font=('Segoe UI', 8, 'bold'))
        style.map('ModernSecondary.TButton',
                  background=[('active', '#059669')])

        style.configure('ModernDanger.TButton', background=self.colors['danger'], foreground='white', borderwidth=0, focuscolor='none', padding=(
            12, 8), font=('Segoe UI', 8, 'bold'))

        style.configure('ModernGhost.TButton', background=self.colors['gray_100'], foreground=self.colors[
                        'text_primary'], borderwidth=1, relief='flat', focuscolor='none', padding=(12, 8), font=('Segoe UI', 9))
        style.map('ModernGhost.TButton', background=[
                  ('active', self.colors['gray_200'])])

        style.configure(
            'ModernCard.TFrame', background=self.colors['bg_card'], relief='flat', borderwidth=0)
        style.configure(
            'ModernMain.TFrame', background=self.colors['bg_primary'], relief='flat', borderwidth=0)
        style.configure('ModernSection.TFrame',
                        background=self.colors['bg_secondary'], relief='flat', borderwidth=0)

        style.configure('ModernHeading.TLabel', background=self.colors['bg_card'], foreground=self.colors['text_primary'], font=(
            'Segoe UI', 16, 'bold'))
        style.configure('ModernSubheading.TLabel',
                        background=self.colors['bg_card'], foreground=self.colors['text_secondary'], font=('Segoe UI', 10))
        style.configure('ModernTitle.TLabel', background=self.colors['bg_card'], foreground=self.colors['text_primary'], font=(
            'Segoe UI', 12, 'bold'))
        style.configure('ModernMuted.TLabel',
                        background=self.colors['bg_card'], foreground=self.colors['text_muted'], font=('Segoe UI', 8))

        style.configure('ModernSuccess.TLabel', background=self.colors['bg_primary'], foreground=self.colors['success'], font=(
            'Segoe UI', 9, 'bold'))
        style.configure('ModernWarning.TLabel', background=self.colors['bg_primary'], foreground=self.colors['warning'], font=(
            'Segoe UI', 9, 'bold'))
        style.configure('ModernDanger.TLabel', background=self.colors['bg_primary'], foreground=self.colors['danger'], font=(
            'Segoe UI', 9, 'bold'))

        style.configure('Modern.TCheckbutton', background=self.colors['bg_card'], foreground=self.colors['text_primary'], font=(
            'Segoe UI', 9), focuscolor='none')
        style.configure('Modern.TRadiobutton', background=self.colors['bg_card'], foreground=self.colors['text_primary'], font=(
            'Segoe UI', 9), focuscolor='none')
        style.configure('Modern.TEntry', borderwidth=1,
                        relief='solid', padding=8, font=('Segoe UI', 10))

        style.configure('Modern.TLabelframe',
                        background=self.colors['bg_card'], borderwidth=0, relief='flat')
        style.configure('Modern.TLabelframe.Label',
                        background=self.colors['bg_card'], foreground=self.colors['text_primary'], font=('Segoe UI', 11, 'bold'))

        style.configure('Modern.TNotebook',
                        background=self.colors['bg_primary'], borderwidth=0)
        style.configure('Modern.TNotebook.Tab', background=self.colors['gray_200'], foreground=self.colors['text_primary'], padding=(
            15, 10), font=('Segoe UI', 9, 'bold'))
        style.map('Modern.TNotebook.Tab', background=[
                  ('selected', self.colors['bg_card']), ('active', self.colors['gray_300'])])

    def create_main_interface(self):
        main_container = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_container.grid(row=0, column=0, sticky='nsew', padx=15, pady=15)
        main_container.grid_rowconfigure(1, weight=1)
        main_container.grid_columnconfigure(0, weight=1)

        shadow_frame = tk.Frame(
            main_container, bg=self.colors['gray_300'], height=2)
        shadow_frame.grid(row=0, column=0, sticky='ew', padx=5, pady=(5, 0))

        content_frame = tk.Frame(main_container, bg=self.colors['bg_card'])
        content_frame.grid(row=1, column=0, sticky='nsew')
        content_frame.grid_rowconfigure(1, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)

        self.create_modern_header(content_frame)
        self.create_modern_content_area(content_frame)
        self.create_modern_footer(content_frame)

    def create_modern_header(self, parent):
        header_frame = tk.Frame(parent, bg=self.colors['bg_card'], height=70)
        header_frame.grid(row=0, column=0, sticky='ew', padx=30, pady=(20, 15))
        header_frame.grid_columnconfigure(1, weight=1)
        header_frame.grid_propagate(False)

        icon_frame = tk.Frame(
            header_frame, bg=self.colors['primary'], width=60, height=60)
        icon_frame.grid(row=0, column=0, padx=(0, 15), pady=5)
        icon_frame.grid_propagate(False)

        icon_label = tk.Label(icon_frame, text="🩺", font=(
            'Segoe UI Emoji', 24), fg='white', bg=self.colors['primary'])
        icon_label.place(relx=0.5, rely=0.5, anchor='center')

        title_frame = tk.Frame(header_frame, bg=self.colors['bg_card'])
        title_frame.grid(row=0, column=1, sticky='w', pady=5)

        title_label = tk.Label(title_frame, text="Dermatology Expert System",
                               bg=self.colors['bg_card'], fg=self.colors['text_primary'], font=('Segoe UI', 18, 'bold'))
        title_label.pack(anchor='w')

        subtitle_label = tk.Label(title_frame, text="AI-Powered Skin Condition Analysis & Diagnosis",
                                  bg=self.colors['bg_card'], fg=self.colors['text_secondary'], font=('Segoe UI', 10))
        subtitle_label.pack(anchor='w', pady=(0, 0))

        self.status_frame = tk.Frame(header_frame, bg=self.colors['bg_card'])
        self.status_frame.grid(row=0, column=2, padx=(15, 0), pady=5)

        status_container = tk.Frame(
            self.status_frame, bg=self.colors['success'], relief='flat', bd=0)
        status_container.pack()

        self.status_label = tk.Label(status_container, text="● Ready", fg='white',
                                     bg=self.colors['success'], font=('Segoe UI', 9, 'bold'), padx=12, pady=6)
        self.status_label.pack()

    def create_modern_content_area(self, parent):
        self.notebook = ttk.Notebook(parent, style='Modern.TNotebook')
        self.notebook.grid(row=1, column=0, sticky='nsew',
                           padx=20, pady=(5, 5))

        self.diagnosis_frame = ttk.Frame(
            self.notebook, style='ModernCard.TFrame')
        self.notebook.add(self.diagnosis_frame, text='   🔍 Diagnosis   ')
        self.create_modern_diagnosis_tab()

    def create_modern_diagnosis_tab(self):
        self.diagnosis_frame.grid_rowconfigure(1, weight=1)
        self.diagnosis_frame.grid_columnconfigure(0, weight=1)

        self.welcome_frame = tk.Frame(
            self.diagnosis_frame, bg=self.colors['bg_card'])
        self.welcome_frame.grid(
            row=0, column=0, sticky='ew', padx=20, pady=(15, 10))

        welcome_card = tk.Frame(
            self.welcome_frame, bg=self.colors['gray_50'], relief='flat', bd=0)
        welcome_card.pack(fill='x', padx=3, pady=3)

        welcome_inner = tk.Frame(welcome_card, bg='white', relief='flat', bd=0)
        welcome_inner.pack(fill='x', padx=1, pady=1)

        welcome_header = tk.Label(welcome_inner, text="🌟 Welcome to Your Personal Dermatology Assistant",
                                  bg='white', fg=self.colors['text_primary'], font=('Segoe UI', 14, 'bold'))
        welcome_header.pack(anchor='w', padx=20, pady=(15, 8))

        welcome_text = """Our advanced AI system will guide you through a comprehensive assessment to help identify potential skin conditions. Simply answer the questions honestly and thoroughly for the most accurate results."""

        welcome_label = tk.Label(welcome_inner, text=welcome_text, font=(
            'Segoe UI', 10), bg='white', fg=self.colors['text_secondary'], wraplength=900, justify='left')
        welcome_label.pack(anchor='w', padx=20, pady=(0, 15))

        button_frame = tk.Frame(welcome_inner, bg='white')
        button_frame.pack(anchor='w', padx=20, pady=(0, 20))

        self.start_button = ttk.Button(
            button_frame, text="🚀 Begin Assessment", style='ModernPrimary.TButton', command=self.start_diagnosis)
        self.start_button.pack(side='left')

        self.question_frame = tk.Frame(
            self.diagnosis_frame, bg=self.colors['bg_card'])
        self.question_frame.grid(
            row=1, column=0, sticky='nsew', padx=20, pady=5)
        self.question_frame.grid_rowconfigure(1, weight=1)
        self.question_frame.grid_columnconfigure(0, weight=1)

        question_card = tk.Frame(
            self.question_frame, bg='white', relief='flat', bd=0)
        question_card.grid(row=0, column=0, sticky='nsew', padx=3, pady=3)
        question_card.grid_rowconfigure(1, weight=1)
        question_card.grid_columnconfigure(0, weight=1)

        question_header = tk.Frame(
            question_card, bg=self.colors['primary'], height=40)
        question_header.grid(row=0, column=0, sticky='ew')
        question_header.grid_propagate(False)

        question_title = tk.Label(question_header, text="💭 Assessment Questions",
                                  bg=self.colors['primary'], fg='white', font=('Segoe UI', 12, 'bold'))
        question_title.place(relx=0.5, rely=0.5, anchor='center')

        question_content = tk.Frame(question_card, bg='white')
        question_content.grid(row=1, column=0, sticky='nsew', padx=20, pady=15)
        question_content.grid_rowconfigure(1, weight=1)
        question_content.grid_columnconfigure(0, weight=1)

        self.question_text = tk.Text(question_content, height=2, wrap='word', font=(
            'Segoe UI', 11), bg=self.colors['gray_50'], fg=self.colors['text_primary'], state='disabled', relief='flat', padx=15, pady=10, bd=0)
        self.question_text.grid(row=0, column=0, sticky='ew', pady=(0, 15))

        self.answer_frame = tk.Frame(question_content, bg='white')
        self.answer_frame.grid(row=1, column=0, sticky='nsew')
        self.answer_frame.grid_columnconfigure(0, weight=1)

        progress_section = tk.Frame(
            self.diagnosis_frame, bg=self.colors['bg_card'])
        progress_section.grid(
            row=2, column=0, sticky='ew', padx=20, pady=(5, 10))

        progress_card = tk.Frame(
            progress_section, bg='white', relief='flat', bd=0)
        progress_card.pack(fill='x', padx=3, pady=3)

        progress_inner = tk.Frame(progress_card, bg='white')
        progress_inner.pack(fill='x', padx=15, pady=10)

        progress_label = tk.Label(progress_inner, text="Assessment Progress",
                                  bg='white', fg=self.colors['text_primary'], font=('Segoe UI', 9, 'bold'))
        progress_label.pack(anchor='w')

        self.progress_bar = ttk.Progressbar(
            progress_inner, mode='indeterminate', style='TProgressbar')
        self.progress_bar.pack(fill='x', pady=(6, 0))

        self.results_frame = tk.Frame(
            self.diagnosis_frame, bg=self.colors['bg_card'])
        self.results_frame.grid(
            row=3, column=0, sticky='ew', padx=20, pady=(5, 20))
        self.results_frame.grid_columnconfigure(0, weight=1)

        results_card = tk.Frame(
            self.results_frame, bg='white', relief='flat', bd=0)
        results_card.grid(row=0, column=0, sticky='ew', padx=3, pady=3)
        results_card.grid_columnconfigure(0, weight=1)

        results_header = tk.Frame(
            results_card, bg=self.colors['secondary'], height=40)
        results_header.grid(row=0, column=0, sticky='ew')
        results_header.grid_propagate(False)

        results_title = tk.Label(results_header, text="📋 Assessment Results",
                                 bg=self.colors['secondary'], fg='white', font=('Segoe UI', 12, 'bold'))
        results_title.place(relx=0.5, rely=0.5, anchor='center')

        results_content = tk.Frame(results_card, bg='white')
        results_content.grid(row=1, column=0, sticky='ew', padx=20, pady=15)
        results_content.grid_columnconfigure(0, weight=1)

        self.results_text = scrolledtext.ScrolledText(results_content, height=8, font=(
            'Segoe UI', 9), state='disabled', wrap='word', bg=self.colors['gray_50'], relief='flat', bd=0, padx=10, pady=10)
        self.results_text.grid(row=0, column=0, sticky='ew')

        self.question_frame.grid_remove()
        self.results_frame.grid_remove()

    def create_modern_footer(self, parent):
        footer_frame = tk.Frame(parent, bg=self.colors['bg_card'], height=50)
        footer_frame.grid(row=2, column=0, sticky='ew', padx=20, pady=(15, 20))
        footer_frame.grid_columnconfigure(1, weight=1)
        footer_frame.grid_propagate(False)

        disclaimer_frame = tk.Frame(
            footer_frame, bg=self.colors['warning'], relief='flat', bd=0)
        disclaimer_frame.grid(row=0, column=0, sticky='w', pady=5)

        disclaimer_text = "⚠️ Medical Disclaimer: For assessment purposes only - Consult healthcare professionals"
        disclaimer_label = tk.Label(disclaimer_frame, text=disclaimer_text, fg='white',
                                    bg=self.colors['warning'], font=('Segoe UI', 8, 'bold'), padx=10, pady=6)
        disclaimer_label.pack()

        version_label = tk.Label(footer_frame, text="v2.0.0 | Modern Edition",
                                 bg=self.colors['bg_card'], fg=self.colors['text_muted'], font=('Segoe UI', 8))
        version_label.grid(row=0, column=1, sticky='e', pady=5)

    def start_diagnosis(self):
        try:
            self.update_status("Initializing assessment...", 'warning')
            self.start_button.config(state='disabled')

            self.expert_system = self.engine_class()
            self.expert_system.reset()
            self.diagnosis_complete = False
            self.waiting_for_answer = False

            self.results_text.config(state='normal')
            self.results_text.delete(1.0, tk.END)
            self.results_text.config(state='disabled')

            self.welcome_frame.grid_remove()
            self.question_frame.grid()
            self.results_frame.grid_remove()

            self.update_status("Assessment in progress...", 'info')
            self.progress_bar.start()
            self.progress_bar.pack()

            self.expert_system.declare(Fact(start=True))
            self.run_engine_in_thread()

        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to start assessment: {str(e)}")
            self.update_status("Error occurred", 'danger')
            self.start_button.config(state='normal')

    def run_engine_in_thread(self):
        def engine_task():
            try:
                self.expert_system.run()
                self.engine_queue.put({"type": "engine_halted"})
            except Exception as e:
                self.engine_queue.put(
                    {"type": "error", "message": f"Engine execution error: {str(e)}"})

        engine_thread = Thread(target=engine_task)
        engine_thread.daemon = True
        engine_thread.start()

    def process_engine_queue(self):
        try:
            while True:
                message = self.engine_queue.get_nowait()
                if message["type"] == "engine_halted":
                    self.process_engine_state()
                elif message["type"] == "error":
                    self.handle_diagnosis_error(message["message"])
                self.engine_queue.task_done()
        except queue.Empty:
            pass

        self.root.after(100, self.process_engine_queue)

    def process_engine_state(self):
        self.progress_bar.stop()
        self.progress_bar.pack_forget()

        self.update_log_from_engine()

        # --- EXPERT SYSTEM FACTS AT CHECKPOINT (from previous debug step) ---
        print("\n--- EXPERT SYSTEM FACTS AT CHECKPOINT ---")
        for fact_id, fact in self.expert_system.facts.items():
            print(f"  Fact ID {fact_id}: {fact}")
        print("-----------------------------------------\n")
        # ------------------------------------

        next_question_fact = next(
            (f for f in self.expert_system.facts.values() if isinstance(f, NextQuestion)), None)

        # --- CRITICAL FIX START ---
        # Correctly check for the 'results_processed' fact
        results_processed_fact = next(
            (f for f in self.expert_system.facts.values()
             if isinstance(f, Fact) and f.get('id') == 'results_processed'),
            None
        )
        # --- CRITICAL FIX END ---

        if next_question_fact:
            ident = next_question_fact['ident']
            self.handle_question(ident)
            self.waiting_for_answer = True
        # --- UPDATED CONDITION ---
        elif results_processed_fact:  # Now this condition will correctly evaluate if the fact exists
            self.diagnosis_complete = True
            self.show_diagnosis_results()
        # --- END UPDATED CONDITION ---
        else:
            messagebox.showinfo(
                "Diagnosis Complete", "The expert system has finished running, but no explicit diagnosis was found or question asked. This might indicate incomplete rules or a lack of relevant information.")
            self.reset_diagnosis()

    def update_log_from_engine(self):
        self.results_text.config(state='normal')
        for message in self.expert_system.fired_rules_log:
            self.results_text.insert(tk.END, message)
        self.expert_system.fired_rules_log.clear()
        self.results_text.see(tk.END)
        self.results_text.config(state='disabled')

    def handle_question(self, question_ident):
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
            self.reset_diagnosis()

    def display_question(self):
        if not self.current_question:
            return

        question_text = self.current_question['text']
        valid_responses = self.current_question['valid_responses']
        # This is where 'multi' is coming from for 'duration'
        question_type = self.current_question['type']
        question_ident = self.current_question['ident']

        self.question_text.config(state='normal')
        self.question_text.delete(1.0, tk.END)
        self.question_text.insert(1.0, f"💭 {question_text}")
        self.question_text.config(state='disabled')

        self.clear_input_widgets()  # Clear widgets and reset associated Tkinter variables

        # --- IMPORTANT: Reset specific Tkinter variables before new binding ---
        self.answer_text_var.set("")  # Clear for number/text entry
        self.choice_radio_var.set("")  # Clear for single-choice radio buttons
        self.checkbox_vars_dict = {}  # Clear and re-initialize the dict for checkboxes
        # --- END IMPORTANT ---

        if question_type == 'number':
            print(
                f"DEBUG_DISPLAY: Creating NUMBER input for '{question_ident}'")
            self.create_modern_number_input()
        elif question_type == 'multi':  # Now handle 'multi' type directly
            # Differentiate between single-choice 'multi' (like yes/no, duration, severity)
            # and actual multi-select 'multi' (like locations, triggers)
            if "Select all that apply" in question_text:
                print(
                    f"DEBUG_DISPLAY: Creating MULTI-CHOICE (checkboxes) input for '{question_ident}' (Type: '{question_type}')")
                self.create_modern_multiple_choice_input(
                    valid_responses, allow_multiple=True)
            # This covers 'duration', 'severity', 'has_symptom_...' (yes/no questions)
            else:
                print(
                    f"DEBUG_DISPLAY: Creating SINGLE-CHOICE (radio) input for '{question_ident}' (Type: '{question_type}')")
                self.create_modern_multiple_choice_input(
                    valid_responses, allow_multiple=False)
        else:  # This 'else' will now only trigger for truly unexpected types
            print(
                f"ERROR: Unknown question type '{question_type}' for '{question_ident}'")
            messagebox.showerror(
                "System Error", f"Unknown question type: {question_type} for '{question_ident}'")

    def create_modern_number_input(self):
        input_container = tk.Frame(self.answer_frame, bg='white')
        input_container.pack(fill='x', pady=10)

        tk.Label(input_container, text="Please enter a numerical value:", font=(
            'Segoe UI', 10), bg='white', fg=self.colors['text_primary']).pack(anchor='w', pady=(0, 5))

        # --- NEW: Use self.answer_text_var as textvariable ---
        self.number_entry = ttk.Entry(input_container, textvariable=self.answer_text_var,
                                      font=('Segoe UI', 11), width=30, style='Modern.TEntry')
        self.number_entry.pack(anchor='w', pady=(0, 10))
        self.number_entry.focus()

        submit_button = ttk.Button(input_container, text="Submit Answer",
                                   style='ModernPrimary.TButton', command=self.submit_number_answer)
        submit_button.pack(anchor='w')
        self.number_entry.bind(
            '<Return>', lambda e: self.submit_number_answer())

    def create_modern_multiple_choice_input(self, valid_responses, allow_multiple=False):
        input_container = tk.Frame(self.answer_frame, bg='white')
        input_container.pack(fill='both', expand=True, pady=10)

        if allow_multiple:
            tk.Label(input_container, text="Select all that apply:", font=(
                'Segoe UI', 10), bg='white', fg=self.colors['text_primary']).pack(anchor='w', pady=(0, 5))
        else:
            tk.Label(input_container, text="Select your answer:", font=(
                'Segoe UI', 10), bg='white', fg=self.colors['text_primary']).pack(anchor='w', pady=(0, 5))

        canvas = tk.Canvas(
            input_container, bg=self.colors['gray_50'], highlightthickness=0, relief='flat', bd=0)
        canvas.pack(side=tk.LEFT, fill='both', expand=True, pady=(5, 0))

        scrollbar = ttk.Scrollbar(
            input_container, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill='y', pady=(5, 0))

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")))

        button_frame_inner = tk.Frame(canvas, bg=self.colors['gray_50'])
        canvas.create_window((0, 0), window=button_frame_inner,
                             anchor="nw", width=canvas.winfo_width())

        def on_canvas_configure(event):
            canvas.itemconfig(canvas.find_withtag(
                "button_frame_inner_id"), width=event.width)
            canvas.config(scrollregion=canvas.bbox("all"))

        canvas.bind('<Configure>', on_canvas_configure)
        canvas.itemconfigure(canvas.create_window(
            (0, 0), window=button_frame_inner, anchor="nw"), tags="button_frame_inner_id")

        button_frame_inner.grid_columnconfigure(0, weight=1)

        if allow_multiple:
            # --- NEW: Use self.checkbox_vars_dict ---
            # self.checkbox_vars_dict is already cleared in display_question before this is called
            row_idx = 0
            for i, option in enumerate(valid_responses):
                display_text = option.replace('_', ' ').title()
                var = tk.BooleanVar()  # Create a new BooleanVar for each checkbox
                self.checkbox_vars_dict[option] = var  # Store it in the dict
                checkbox = ttk.Checkbutton(
                    button_frame_inner, text=display_text, variable=var, style='Modern.TCheckbutton')
                checkbox.grid(row=row_idx, column=0,
                              sticky='w', pady=3, padx=8)
                row_idx += 1
        else:
            # --- NEW: Use self.choice_radio_var ---
            # self.choice_radio_var is already cleared in display_question before this is called
            row_idx = 0
            for i, option in enumerate(valid_responses):
                display_text = option.replace('_', ' ').title()
                radio_button = ttk.Radiobutton(button_frame_inner, text=display_text,
                                               variable=self.choice_radio_var, value=option,  # Link to the persistent StringVar
                                               style='Modern.TRadiobutton')
                radio_button.grid(row=row_idx, column=0,
                                  sticky='w', pady=3, padx=8)
                if i == 0:
                    # Select the first option by default, setting the value of self.choice_radio_var
                    radio_button.invoke()
                row_idx += 1

        button_frame_inner.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        submit_button = ttk.Button(input_container, text="Submit Answer",
                                   style='ModernPrimary.TButton', command=self.submit_choice_answer)
        submit_button.pack(anchor='w', pady=(15, 0))

    def submit_number_answer(self):
        try:
            # --- NEW: Get value from self.answer_text_var ---
            answer = self.answer_text_var.get().strip()
            if not answer.isdigit():
                messagebox.showerror(
                    "Invalid Input", "Please enter a valid number.")
                return
            print(
                f"DEBUG_SUBMIT: Number submitted: '{answer}' for ident '{self.current_question['ident']}'")
            self.process_answer(answer)
        except Exception as e:
            messagebox.showerror("Error", f"Error submitting answer: {str(e)}")

    def submit_choice_answer(self):
        try:
            if self.current_question and "Select all that apply" in self.current_question['text']:
                # --- NEW: Get values from self.checkbox_vars_dict ---
                selected_options = [
                    option for option, var in self.checkbox_vars_dict.items() if var.get()]
                if not selected_options:
                    messagebox.showerror(
                        "No Selection", "Please select at least one answer.")
                    return
                answer = ",".join(selected_options)
                print(
                    f"DEBUG_SUBMIT: Multi-choice submitted: '{answer}' for ident '{self.current_question['ident']}'")
            else:
                # --- NEW: Get value from self.choice_radio_var ---
                answer = self.choice_radio_var.get()
                if not answer:
                    messagebox.showerror(
                        "No Selection", "Please select an answer.")
                    return
                print(
                    f"DEBUG_SUBMIT: Single-choice submitted: '{answer}' for ident '{self.current_question['ident']}'")
            self.process_answer(answer)
        except Exception as e:
            messagebox.showerror("Error", f"Error submitting answer: {str(e)}")

    def process_answer(self, answer):
        try:
            if not self.current_question:
                print("DEBUG_PROCESS: No current_question. Exiting process_answer.")
                return

            question_ident = self.current_question['ident']

            print(
                f"\nDEBUG_PROCESS: --- Entering process_answer for '{question_ident}' ---")
            print(f"DEBUG_PROCESS: Raw answer string from GUI: '{answer}'")
            print(
                f"DEBUG_PROCESS: Question Type: {self.current_question['type']}, Valid Responses: {self.current_question['valid_responses']}")

            self.clear_input_widgets()

            # --- Important: No changes to current_question, it's already set ---
            # The Tkinter variables are reset in display_question before creating widgets
            # This ensures they are clean before reading the new answer in submit_*_answer
            # The .get() calls in submit_*_answer now directly use the current state of these vars.

            self.question_text.config(state='normal')
            self.question_text.delete(1.0, tk.END)
            self.question_text.insert(1.0, "Processing your answer...")
            self.question_text.config(state='disabled')
            self.update_status("Processing answer...", 'info')
            self.progress_bar.start()
            self.progress_bar.pack()

            next_q_fact_id = None
            for fact_id, fact in self.expert_system.facts.items():
                if isinstance(fact, NextQuestion) and fact['ident'] == question_ident:
                    next_q_fact_id = fact_id
                    break
            if next_q_fact_id is not None:
                self.expert_system.retract(next_q_fact_id)
                print(
                    f"DEBUG_PROCESS: Retracted NextQuestion({question_ident}) with ID {next_q_fact_id}")
            else:
                print(
                    f"DEBUG_PROCESS: WARNING: No NextQuestion({question_ident}) found to retract.")

            # --- FACT DECLARATION LOGIC (UNCHANGED, relies on 'answer' being correct) ---
            # 'answer' string is now correctly populated by submit_*_answer based on fresh variable states.
            is_multi_select_question = (
                self.current_question['ident'] in [
                    'locations',  # Add other multi-select question 'ident's here if you have them
                    # Example: 'some_other_multi_select_question_ident'
                ]
            )

            if is_multi_select_question:
                individual_answers = [a.strip()
                                      for a in answer.split(',') if a.strip()]
                print(
                    f"DEBUG_PROCESS: Multi-select detected. Splitting '{answer}' into: {individual_answers}")
                for individual_ans in individual_answers:
                    # Ensure lowercase for engine rules!
                    self.expert_system.declare(
                        Answer(ident=question_ident, text=individual_ans.lower()))
                    print(
                        f"DEBUG_PROCESS: Declared individual Answer(ident='{question_ident}', text='{individual_ans.lower()}')")
            else:
                declared_answer_text = answer.lower(
                ) if self.current_question['type'] == 'text' else answer
                self.expert_system.declare(
                    Answer(ident=question_ident, text=declared_answer_text))
                print(
                    f"DEBUG_PROCESS: Declared single Answer(ident='{question_ident}', text='{declared_answer_text}')")
            # --- END FACT DECLARATION LOGIC ---

            print(f"DEBUG_PROCESS: Current facts AFTER declaration in Expert System:")
            for fact_id, fact in self.expert_system.facts.items():
                print(f"  Fact ID {fact_id}: {fact}")
            print(f"DEBUG_PROCESS: --- Exiting process_answer ---\n")

            self.waiting_for_answer = False
            self.run_engine_in_thread()

        except Exception as e:
            messagebox.showerror("Error", f"Error processing answer: {str(e)}")
            self.handle_diagnosis_error(str(e))

    def clear_input_widgets(self):
        """Removes all input widgets from the answer_frame."""
        print("DEBUG_CLEAR: Clearing input widgets in answer_frame.")
        for widget in self.answer_frame.winfo_children():
            widget.destroy()

    def handle_diagnosis_error(self, error_message):
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        self.update_status("Error occurred", 'danger')
        messagebox.showerror(
            "Diagnosis Error", f"An error occurred during diagnosis: {error_message}")
        self.reset_diagnosis()

    def show_diagnosis_results(self):
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
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
                    tk.END, f"    Confidence: {confidence:.1f}%\n")
            if self.detailed_reasoning.get():
                self.results_text.insert(
                    tk.END, f"    Reasoning: {reasoning}\n")
            self.results_text.insert(tk.END, "\n")

            # --- LLM Explanation ---
            # Build the result string to explain
            result_text = f"Primary Diagnosis: {disease}\nConfidence: {confidence:.1f}%\nReasoning: {reasoning}"

            def insert_llm_explanation():
                explanation = explain_result_with_llm(result_text)
                self.results_text.config(state='normal')
                self.results_text.insert(
                    tk.END, "\n🤖 AI Explanation:\n" + explanation + "\n")
                self.results_text.config(state='disabled')

            # Run in a thread so GUI doesn't freeze
            Thread(target=insert_llm_explanation).start()
        else:
            self.show_no_diagnosis_message()

        self.results_text.config(state='disabled')
        self.create_results_buttons()
        self.notebook.select(0)

    def show_no_diagnosis_message(self):
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
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
        self.notebook.select(0)

    def create_results_buttons(self):
        for widget in self.results_frame.winfo_children():
            if isinstance(widget, tk.Frame) and any(isinstance(c, ttk.Button) for c in widget.winfo_children()):
                widget.destroy()

        button_frame = tk.Frame(self.results_frame, bg='white')
        button_frame.grid(row=1, column=0, sticky='ew', padx=20, pady=(15, 0))

        ttk.Button(button_frame, text="🔄 Start New Assessment", style='ModernPrimary.TButton',
                   command=self.reset_diagnosis).pack(side='left', padx=(0, 10))
        ttk.Button(button_frame, text="💾 Save Results", style='ModernSecondary.TButton',
                   command=self.save_results).pack(side='left', padx=(0, 10))
        ttk.Button(button_frame, text="🖨️ Print Results",
                   style='ModernGhost.TButton', command=self.print_results).pack(side='left')

    def reset_diagnosis(self):
        self.expert_system = None
        self.current_question = None
        self.diagnosis_complete = False
        self.waiting_for_answer = False

        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        self.update_status("Ready", 'success')

        self.welcome_frame.grid()
        self.question_frame.grid_remove()
        self.results_frame.grid_remove()

        self.start_button.config(state='normal')

        self.results_text.config(state='normal')
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state='disabled')

        self.clear_input_widgets()

    def save_results(self):
        try:
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
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
                html_content = self.generate_html_report()
                f.write(html_content)
                temp_filename = f.name

            if os.name == 'nt':
                os.startfile(temp_filename)
            elif os.name == 'posix':
                if os.uname().sysname == 'Darwin':
                    subprocess.run(['open', temp_filename])
                else:
                    subprocess.run(['xdg-open', temp_filename])
            else:
                messagebox.showwarning(
                    "Print", "Printing not supported on this OS automatically. Report saved as HTML.")
        except Exception as e:
            messagebox.showerror("Error", f"Error printing results: {str(e)}")

    def generate_html_report(self):
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
        messagebox.showinfo(
            "Settings", "Settings saved successfully! (Functionality not fully implemented)")

    def update_status(self, message, status_type='info'):
        try:
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
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\nApplication terminated by user")
        except Exception as e:
            print(f"Application error: {str(e)}")
            messagebox.showerror(
                "Fatal Error", f"Application encountered a fatal error: {str(e)}")
