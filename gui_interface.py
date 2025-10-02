import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from ai_models import SentimentAnalysisModel, DigitRecognitionModel 

# Tkinter GUI

class AIGUI:
    
    def __init__(self, master):
        self.master = master
        master.title("Tkinter AI GUI")
        
        # Initialize models
        self.models = {
            "Sentiment Analyzer": SentimentAnalysisModel(),
            "MNIST Digit Recognizer": DigitRecognitionModel()
        }
        self.current_model = None
        self.current_image_path = "" 

        # --- GUI Setup ---
        self.create_menu_bar()
        
        # 1. SETUP INFO FIRST: Ensures labels exist before update_model_info is called.
        self.setup_info_section(master) 

        # 2. SETUP model section
        self.setup_model_selection(master)
        
        # 3. Setup Main I/O
        self.setup_main_io_section(master)
        
        # --- 5. Notes/References Section ---
        tk.Label(master, text="Notes: Model 1 is Sentiment Analysis (Text). Model 2 is Digit Recognition (Image).", anchor='w', padx=10, pady=5).pack(fill='x')

    # --- GUI Creation Methods ---
    
    def create_menu_bar(self):
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New")
        file_menu.add_command(label="Open...")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        models_menu = tk.Menu(menubar, tearoff=0)
        models_menu.add_command(label="Manage Models")
        menubar.add_cascade(label="Models", menu=models_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About")
        menubar.add_cascade(label="Help", menu=help_menu)

    def setup_model_selection(self, master):
        model_selection_frame = tk.Frame(master, padx=10, pady=5)
        model_selection_frame.pack(fill='x')

        tk.Label(model_selection_frame, text="Model Selection:").pack(side='left', padx=(0, 5))

        # Model Category (Mapped to Run Model 1/2)
        model_names = list(self.models.keys())
        self.model_name_var = tk.StringVar(value=model_names[0] if model_names else "No Models")
        model_name_combo = ttk.Combobox(model_selection_frame, textvariable=self.model_name_var, values=model_names, width=25, state="readonly")
        model_name_combo.pack(side='left', padx=5)
        model_name_combo.bind("<<ComboboxSelected>>", self.update_model_info)

        tk.Button(model_selection_frame, text="Load Model", command=self.load_model).pack(side='left', padx=10)

        # Initialize info display
        self.update_model_info()

    def setup_main_io_section(self, master):
        main_section_frame = tk.Frame(master, padx=10, pady=5)
        main_section_frame.pack(fill='both', expand=True)

        # Left Column: User Input
        input_frame = tk.LabelFrame(main_section_frame, text="User Input Section", padx=5, pady=5)
        input_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))

        # Radio Buttons for Text/Image
        self.input_type = tk.StringVar(value="Text")
        tk.Radiobutton(input_frame, text="Text", variable=self.input_type, value="Text").pack(side='left')
        tk.Radiobutton(input_frame, text="Image", variable=self.input_type, value="Image").pack(side='left')
        tk.Button(input_frame, text="Browse", command=self.browse_file).pack(side='right')

        self.input_text = tk.Text(input_frame, height=10, width=40)
        self.input_text.pack(fill='both', expand=True, pady=5)
        self.input_text.insert(tk.END, "Enter text for sentiment analysis here...\n\n(For image model, select 'Image' and click 'Browse')")

        button_frame = tk.Frame(input_frame)
        button_frame.pack(fill='x', pady=5)
        tk.Button(button_frame, text="Run Model 1 (Text)", command=lambda: self.run_model(self.models["Sentiment Analyzer"])).pack(side='left', padx=5)
        tk.Button(button_frame, text="Run Model 2 (Image)", command=lambda: self.run_model(self.models["MNIST Digit Recognizer"])).pack(side='left', padx=5)
        tk.Button(button_frame, text="Clear Screen", command=self.clear_output).pack(side='left', padx=10)
        tk.Button(button_frame, text="help", command=self.show_help).pack(side='left', padx=5)

        # Right Column: Model Output
        output_frame = tk.LabelFrame(main_section_frame, text="Model Output Section", padx=5, pady=5)
        output_frame.pack(side='right', fill='both', expand=True)

        tk.Label(output_frame, text="Output Display:").pack(anchor='nw')
        self.output_text = tk.Text(output_frame, height=10, width=40)
        self.output_text.pack(fill='both', expand=True, pady=5)

    def clear_output(self):
        
        # Clear the output display area
        self.output_text.delete(1.0, tk.END) 
        
        # Clear the input area and restore the placeholder text
        self.input_text.delete(1.0, tk.END)
        self.input_text.insert(tk.END, "Enter text for sentiment analysis here...\n\n(For image model, select 'Image' and click 'Browse')")

        messagebox.showinfo("Clear", "Input and Output screens cleared.")

    def setup_info_section(self, master):
        info_frame = tk.LabelFrame(master, text="Model Information & Explanation", padx=10, pady=5)
        info_frame.pack(fill='x', padx=10, pady=5)

        # Left side: Model Info
        model_info_frame = tk.Frame(info_frame)
        model_info_frame.pack(side='left', fill='y', padx=(0, 20))
        tk.Label(model_info_frame, text="Selected Model Info:", font=('Arial', 10, 'bold')).pack(anchor='nw')
        self.model_name_label = tk.Label(model_info_frame, text="• Model Name: N/A", anchor='w')
        self.model_name_label.pack(anchor='nw')
        self.model_category_label = tk.Label(model_info_frame, text="• Category: N/A", anchor='w')
        self.model_category_label.pack(anchor='nw')
        self.model_desc_label = tk.Label(model_info_frame, text="• Short Description: N/A", anchor='w')
        self.model_desc_label.pack(anchor='nw')


        # Right side: OOP Explanation (Static text)
        oop_frame = tk.Frame(info_frame)
        oop_frame.pack(side='left', fill='y', expand=True)
        tk.Label(oop_frame, text="OOP Concepts Explanation (Static):", font=('Arial', 10, 'bold')).pack(anchor='nw')
        oop_points = [
            "• Multiple Inheritance (Conceptual)",
            "• Encapsulation (Model attributes are private)",
            "• Polymorphism/Method Overriding (All models have a 'predict' method)",
            "• Decorators (Not explicitly used, placeholder concept)"
        ]
        for point in oop_points:
            tk.Label(oop_frame, text=point).pack(anchor='nw')


    # --- Functionality Methods ---

    def update_model_info(self, event=None):
        selected_name = self.model_name_var.get()
        if selected_name in self.models:
            model = self.models[selected_name]
            self.model_name_label.config(text=f"• Model Name: {model.name}")
            self.model_category_label.config(text=f"• Category: {model.category}")
            self.model_desc_label.config(text=f"• Short Description: {model.description}")
        else:
            self.model_name_label.config(text="• Model Name: N/A")
            self.model_category_label.config(text="• Category: N/A")
            self.model_desc_label.config(text="• Short Description: N/A")
            
    def load_model(self):
        selected_name = self.model_name_var.get()
        if selected_name in self.models:
            model = self.models[selected_name]
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"Attempting to load: {model.name}...\n")
            
            # Use threading for large models in a real app to prevent freezing
            try:
                message = model.load()
                self.current_model = model
                self.output_text.insert(tk.END, message + "\n")
                messagebox.showinfo("Model Load", message)
            except Exception as e:
                self.output_text.insert(tk.END, f"Model loading failed: {e}\n")
                messagebox.showerror("Model Load Error", f"Failed to load model: {e}")
        else:
            messagebox.showwarning("Warning", "Please select a model to load.")

    def browse_file(self):
        if self.input_type.get() == "Image":
            file_path = filedialog.askopenfilename(
                title="Select Image File",
                filetypes=[("Image files", "*.png *.jpg *.jpeg")]
            )
            if file_path:
                self.current_image_path = file_path
                self.input_text.delete(1.0, tk.END)
                self.input_text.insert(tk.END, f"Image file selected:\n{file_path}")
        else:
            messagebox.showinfo("Info", "Input Type is 'Text'. Click 'Browse' only when 'Image' is selected.")

    def run_model(self, model_instance):
        self.output_text.insert(tk.END, f"\n--- Running {model_instance.name} ---")

        if model_instance.category == "Text":
            if self.input_type.get() != "Text":
                self.output_text.insert(tk.END, "\nError: Selected model requires Text input. Change the radio button.")
                return
            input_data = self.input_text.get(1.0, tk.END).strip()
            
        elif model_instance.category == "Vision":
            if self.input_type.get() != "Image":
                self.output_text.insert(tk.END, "\nError: Selected model requires Image input. Change the radio button.")
                return
            input_data = self.current_image_path # Use the stored image path
        else:
            self.output_text.insert(tk.END, f"\nError: Unsupported model category: {model_instance.category}")
            return
            
        # Perform prediction
        try:
            prediction_result = model_instance.predict(input_data)
            self.output_text.insert(tk.END, f"\nInput: '{input_data[:30]}...'")
            self.output_text.insert(tk.END, f"\nResult: {prediction_result}\n")
        except Exception as e:
            self.output_text.insert(tk.END, f"\nPrediction failed: {e}\n")


    def show_help(self):
        messagebox.showinfo(
            "Help/Info",
            "Model 1: Sentiment Analysis (Requires Text input).\n"
            "Model 2: MNIST Digit Recognition (Requires Image input, 28x28 B/W preferred).\n"
            "Steps:\n1. Select Model from dropdown.\n2. Click 'Load Model'.\n3. Select 'Text' or 'Image' radio button.\n4. Enter text or 'Browse' for an image.\n5. Click 'Run Model 1' or 'Run Model 2'."
        )