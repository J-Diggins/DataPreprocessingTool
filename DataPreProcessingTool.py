import os
import pandas as pd
import itertools
from scipy import stats 
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog,ttk
from tkinter.filedialog import askdirectory


# TKinter Root
root = tk.Tk()
root.minsize(width=800, height=600)
root.title("Data Processing Tool")

# Top Frame
t_frame = ttk.Frame(root)
t_frame = ttk.Frame(root, height = 50)
t_frame.grid(row=0,column=0, sticky='w')

b_frame = ttk.Frame(root)
b_frame.grid(row=1,column=0)

# Select folder at startup and append column names from excel files to a list
column_names = []
folder_path = ""
# Start row for excel sheet read and start row
row_skip = 0
# initialise counter
row_counter = 1
# pilot data
pilot_value = 0
# widgets 
widgets = {}
# Strings to ignore, if one of your column names contains one of these strings, and you would like to access it, delete it from this list
ignore_strings = ["expName","participant","OS","session","psychopyVersion","frameRate","date",".x",".y",".started",".stopped",".thisRepN","thisN","thisTrialN","thisIndex","Unnamed","leftButton","midButton","rightButton"]


# menu
menu = tk.Menu(root)

# Menu Functions
# Help menu information
def open_help_window():
    help_window = tk.Toplevel()
    help_window.title("Help")
    help_window.geometry("600x400")

    canvas = tk.Canvas(help_window)
    scrollbar = ttk.Scrollbar(help_window, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Mouse wheel scrolling support
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # Windows and Mac use different event formats
    canvas.bind_all("<MouseWheel>", _on_mousewheel)  # Windows and macOS
    canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))  # Linux scroll up
    canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))   # Linux scroll down

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def add_label(parent, text, bold=False, pad=(5, 2)):
        font = ("TkDefaultFont", 10, "bold" if bold else "normal")
        label = tk.Label(parent, text=text, anchor="w", justify="left", wraplength=560, font=font)
        label.pack(fill="x", padx=pad[0], pady=pad[1])

    # Help information
    add_label(scrollable_frame, "PsychoPy Data Extraction Tool Help", bold=True, pad=(5, 10))

    add_label(scrollable_frame, "Welcome to the PsychoPy Data Extraction Tool. This tool was created to help quickly run basic statistical analysis on a folder containing the .csv results files from a PsychoPy experiment. THIS PROGRAM CAN ONLY ACCEPT .CSV FILES.")

    add_label(scrollable_frame, "Getting Started", bold=True, pad=(5, 10))
    add_label(scrollable_frame, "The first step in the process of extracting your data is to locate your root folder. This will likely be a folder within your PsychoPy experiment folder called “data”. This folder will hold all of the .csv files from participant data collection.")
    add_label(scrollable_frame, "To get started press “Select” and then “Folder”. This will open a dialogue asking you to pick a folder. There will be popup dialogues reminding you of what you are doing.")

    add_label(scrollable_frame, "Selecting a starting line", bold=True, pad=(5, 10))
    add_label(scrollable_frame, "If your experiment has a practice session, or you don’t want to include the first number of rows, you can choose a different starting row. Choose “Select” and then “Starting Row”. In the starting row box, enter the row number you wish to start from, from the left of the excel sheet. If wish to use all rows, you can keep the default value as “0”.")

    add_label(scrollable_frame, "Selecting a folder", bold=True, pad=(5, 10))
    add_label(scrollable_frame, "The next dialogue box will be where you locate your folder. This will be the folder containing all of the .csv files you wish to use. If you have selected a folder the words “no folder selected” will change to your file path. If you have previously ran the program, you might wish to delete the original output file, so it does not load those columns into the tool.")

    add_label(scrollable_frame, "Trimming Values", bold=True, pad=(5, 10))
    add_label(scrollable_frame, "If you select the “Trim Values” option and then “Trim” you can add upper and lower bound cut off points for your data. You will first get a dialogue box asking for the cut off points, and then a second dialogue box will ask which column holds the data you wish to trim.")
    add_label(scrollable_frame, "IMPORTANT: Using the “Trim Values” function will add the trimmed values to the original .csv files, they are not held within the tool itself. If you use the “Trim Values” option, you will need to use the “Select Folder” option again, to refresh the columns. You should do this once you have trimmed all the required columns, and not after each trim.")

    add_label(scrollable_frame, "Statistics", bold=True, pad=(5, 10))
    add_label(scrollable_frame, "The first column you will see is statistics. Here you will find the basic statistics you can run. They include mean, median, sum, inter quartile range, N (count), standard deviation and percentage.")
    add_label(scrollable_frame, "A note on percentage: This option should only be used on columns containing 1s and 0s, such as a correct answer column.")

    add_label(scrollable_frame, "Excel Columns", bold=True, pad=(5, 10))
    add_label(scrollable_frame, "This dropdown menu allows you to select the column, in which the data you wish to use the statistical analysis, exists in.")

    add_label(scrollable_frame, "Adding Rows", bold=True, pad=(5, 10))
    add_label(scrollable_frame, "If you want to run multiple analysis, you can add additional rows. If you make a mistake, or decide you no longer need the row, there is a “delete row” button as well.")

    add_label(scrollable_frame, "Adding Conditions", bold=True, pad=(5, 10))
    add_label(scrollable_frame, "Using the add condition button will produce another dropdown menu with your excel columns. This way you can better tailor your analysis. Reading from left to right in the tool will make this make more sense.")
    add_label(scrollable_frame, "For example: Mean of Reaction Time using Condition Correct.")
    add_label(scrollable_frame, "You can add multiple conditions to a row, such as if you have different variables, and would like to compare against correct and incorrect answers.")

    add_label(scrollable_frame, "Running the Analysis", bold=True, pad=(5, 10))
    add_label(scrollable_frame, "To run the analysis select “Analysis” and then “Run”. It will first ask you for the folder in which you wish to save the data. It will then ask you for a filename for your data.")

    add_label(scrollable_frame, "If you run into any bugs or issues when using this program. Please contact the Psychology technician, Jake Diggins, so they can look into the problem.")

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    
# About menu information
def about_text():
    messagebox.showinfo("About", "This tool was created by Jake Diggins for Aston University Students.\n"
                        "Feel free to edit this code for your own institution, under open access.\n"
                        "Please remember to credit the author.\n"
                        "Jake Diggins, Aston University, 2025")

# Create Dataframes
def get_csv_dataframes(folder_path, skip_rows=0):
    #Return generator of (filename, dataframe) for each valid CSV in folder.
    for filename in os.listdir(folder_path):
        if not filename.endswith('.csv'):
            continue
        file_path = os.path.join(folder_path, filename)
        try:
            df = pd.read_csv(file_path, header=0, skiprows=range(1, skip_rows))
            if df.empty or df.shape[1] == 0:
                continue
            yield filename, df
        except pd.errors.EmptyDataError:
            continue
        except Exception:
            continue


# Button for row select
def select_start_row():
    # Create a new window for excluding values
    messagebox.showinfo("Row Info", "Select which row your main experiment starts from, using the cell value on the left in the excel sheet. If you do not have a practice task, you can can use 0.")
    dialog = tk.Toplevel(root)
    dialog.title("Select Start Row")
    dialog.geometry("200x200")

    starting_row_var = tk.IntVar()

    tk.Label(dialog, text="Enter Starting Row:").pack(pady=5)
    tk.Entry(dialog, textvariable=starting_row_var).pack(pady=5)
    
    def sel_next():
        dialog.destroy()
    tk.Button(dialog, text="Next", command=sel_next).pack(side="right", padx=10, pady=10)
    tk.Button(dialog, text="Cancel", command=dialog.destroy).pack(side="left", padx=10, pady=10)
    dialog.wait_window()
    
    global row_skip
    row_skip = 0
    row_skip = (starting_row_var.get() -1)

# Button to change folder selection
def select_folder():
    global folder_path, column_names, pilot_value
    folder_path = ''
    column_names = []
    
    # Choose pilot data
    pilot_dialog = tk.Toplevel(root)
    pilot_dialog.title("Pilot Data")
    pilot_dialog.geometry("200x200")
       
    pilot_var = tk.IntVar(value=1)
   
   
    tk.Label(pilot_dialog, text="Select which data to include").pack(pady=5)

    tk.Radiobutton(pilot_dialog, 
               text="Exclude Pilot Data",
               padx = 20, 
               variable=pilot_var, 
               value=1).pack(pady=5)

    tk.Radiobutton(pilot_dialog, 
               text="Include Pilot Data",
               padx = 20, 
               variable=pilot_var, 
               value=2).pack(pady=5)
    
    tk.Radiobutton(pilot_dialog, 
               text="Pilot Data Only",
               padx = 20, 
               variable=pilot_var, 
               value=3).pack(pady=5)
    
    def sel_next():
       #update pilot values
       global pilot_value
       val = pilot_var.get()
       if val == 1:
            pilot_value = 0
       elif val == 2:
            pilot_value = 1
       else:
            pilot_value = 2
        
       pilot_dialog.destroy()
   
    tk.Button(pilot_dialog, text="Next", command=sel_next).pack(side="right", padx=10, pady=10)
    tk.Button(pilot_dialog, text="Cancel", command=pilot_dialog.destroy).pack(side="left", padx=10, pady=10)
    
    pilot_dialog.wait_window()
    
   
    
    folder_path = askdirectory()
    for filename, df in get_csv_dataframes(folder_path, skip_rows=row_skip):
        for i in df.columns:
            if not any(s in i for s in ignore_strings) and i not in column_names:
                column_names.append(i)

    # Update dropdown only if we found valid column names
    if column_names:
        c2['values'] = column_names  
        c2.set("")  

    # Update folder path label
    path_label.config(text=folder_path)
  

    # Update the folder path label to show the current folder path
    path_label.config(text=folder_path)
    


# Function to exclude data within a range
def trim_values():
    # Create a new window for excluding values
    dialog = tk.Toplevel(root)
    dialog.title("Trim Values")
    dialog.geometry("200x200")

    low_value_var = tk.DoubleVar()
    high_value_var = tk.DoubleVar()

    tk.Label(dialog, text="Enter Low Value:").pack(pady=5)
    tk.Entry(dialog, textvariable=low_value_var).pack(pady=5)
    tk.Label(dialog, text="Enter High Value:").pack(pady=5)
    tk.Entry(dialog, textvariable=high_value_var).pack(pady=5)

    def next_button():
        # Fetch values after user input
        low_value = low_value_var.get()
        high_value = high_value_var.get()

        # Validate input
        if low_value >= high_value:
            messagebox.showerror("Error", "Low value must be less than high value.")
            return

        # Proceed to the column selection dialog
        col_dialog = tk.Toplevel(root)
        col_dialog.title("Select Column")
        col_dialog.geometry("200x200")

        tk.Label(col_dialog, text="Select Column to Trim").pack(pady=5)

        # Combobox for column selection
        c3 = ttk.Combobox(
            col_dialog,
            state="readonly",
            values=column_names
        )
        c3.pack(pady=5)
        
        def confirm_trim():
            # Get selected column and apply trimming
            column_choice = c3.get()
            if not column_choice:
                messagebox.showerror("Error", "No column selected.")
                return

            try:
                # Apply trimming
                for filename, df in get_csv_dataframes(folder_path):
                    if column_choice in df.columns:
                            column_data = df[column_choice].dropna()

                            # Trim data
                            trimmed_data = column_data[
                                (column_data > low_value) & (column_data < high_value)
                            ]

                            # Add trimmed column to DataFrame
                            new_column_name = f"trim_{column_choice}"
                            df[new_column_name] = trimmed_data

                            # Save updated DataFrame
                            df.to_csv(os.path.join(folder_path, filename), index=False)

                            # Update column_names dynamically
                            global column_names
                            column_names = list(df.columns)

                            # Update combobox options
                            c2["values"] = column_names

                messagebox.showinfo("Success", "Data trimmed and saved.")
                col_dialog.destroy()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to trim data: {e}")

        tk.Button(col_dialog, text="Confirm", command=confirm_trim).pack(side="right", padx=10, pady=10)
        tk.Button(col_dialog, text="Cancel", command=col_dialog.destroy).pack(side="left", padx=10, pady=10)

    tk.Button(dialog, text="Next", command=next_button).pack(side="right", padx=10, pady=10)
    tk.Button(dialog, text="Cancel", command=dialog.destroy).pack(side="left", padx=10, pady=10)    
    
# Function for the Run Analysis button, which will run the analysis and save the file

def run_analysis():
    # Allow user to select a folder and save 
    save_folder = filedialog.askdirectory(title="Select Folder to Save Results")
    if not save_folder:
        messagebox.showerror("Error", "No save folder selected.")
        return
    save_filename = simpledialog.askstring("Save File", "Enter a name for the result CSV file (without extension):")
    if not save_filename:
        messagebox.showerror("Error", "No file name provided.")
        return
    save_path = os.path.join(save_folder, f"{save_filename}.csv")
    
    # If file exists, confirm deletion to allow overwriting
    if os.path.exists(save_path):
        confirm_overwrite = messagebox.askyesno("Overwrite Confirmation", f"'{save_filename}.csv' already exists. Do you want to overwrite it?")
        if not confirm_overwrite:
            messagebox.showinfo("Cancelled", "File save operation cancelled.")
            return
        os.remove(save_path)

    # Initialize a list to store result rows
    results = []
    
    for filename, df in get_csv_dataframes(folder_path, skip_rows=row_skip):
    
            result_row = {"filename": filename}
    
            # Iterate over each widget configuration
            for widget_id, widget in widgets.items():
                comboboxes = widget['combos']
    
                if len(comboboxes) < 2:
                    continue  # Skip if insufficient selections
    
                analysis_choice = comboboxes[0].get()
                column_choice = comboboxes[1].get()
    
                # Make sure the chosen column exists
                if column_choice not in df.columns:
                    result_row[f"{analysis_choice}_{column_choice}"] = "Column not found"
                    continue

                # Conditions check
                conditions = comboboxes[2:]
                condition_filters = {}
                for condition_combo in conditions:
                    condition_column = condition_combo.get()
                    if condition_column and condition_column in df.columns:
                        unique_values = df[condition_column].dropna().unique()
                        condition_filters[condition_column] = unique_values
    
                # If no statistical analysis is selected, save data as comma-separated list with conditions applied
                if not analysis_choice:
                    if not condition_filters:
                        column_name = f"Data_{column_choice}"
                        try:
                            result = ", ".join(map(str, df[column_choice].dropna().tolist()))
                        except Exception:
                            result = "Error retrieving data"
                        result_row[column_name] = result
                    else:
                        condition_combinations = list(itertools.product(*condition_filters.values()))
                        condition_columns = list(condition_filters.keys())
    
                        for combination in condition_combinations:
                            filtered_df = df.copy()
                            condition_str = "_".join([f"{col}_{val}" for col, val in zip(condition_columns, combination)])
                            column_name = f"{analysis_choice}_{column_choice}_{condition_str}"
    
                            for col, val in zip(condition_columns, combination):
                                filtered_df = filtered_df[filtered_df[col] == val]
    
                            if not filtered_df.empty:
                                try:
                                    result = ", ".join(map(str, filtered_df[column_choice].dropna().tolist()))
                                except Exception:
                                    result = "Error retrieving data"
                                result_row[column_name] = result
                    continue  # Skip further processing for this file
    
                # If analysis is selected, calculate the chosen statistic
                if not condition_filters:
                    column_name = f"{analysis_choice}_{column_choice}"
                    try:
                        if analysis_choice == "Mean":
                            result = df[column_choice].mean()
                        elif analysis_choice == "Median":
                            result = df[column_choice].median()
                        elif analysis_choice == "Inter Quartile Range":
                            result = stats.iqr(df[column_choice])
                        elif analysis_choice == "S.D":
                            result = df[column_choice].std()
                        elif analysis_choice == "Sum":
                            result = df[column_choice].sum()
                        elif analysis_choice == "N":
                            result = df[column_choice].count()
                        elif analysis_choice == "Percentage":
                            result = (df[column_choice].sum() / df[column_choice].count()) * 100
                        else:
                            result = "Unknown Analysis"
                    except Exception:
                        result = "Error"
    
                    result_row[column_name] = result
    
                else:
                    # With conditions, iterate over all combinations
                    condition_combinations = list(itertools.product(*condition_filters.values()))
                    condition_columns = list(condition_filters.keys())
    
                    for combination in condition_combinations:
                        filtered_df = df.copy()
                        condition_str = "_".join([f"{col}_{val}" for col, val in zip(condition_columns, combination)])
                        column_name = f"{analysis_choice}_{column_choice}_{condition_str}"
    
                        for col, val in zip(condition_columns, combination):
                            filtered_df = filtered_df[filtered_df[col] == val]
    
                        if not filtered_df.empty:
                            try:
                                if analysis_choice == "Mean":
                                    result = filtered_df[column_choice].mean()
                                elif analysis_choice == "Median":
                                    result = filtered_df[column_choice].median()
                                elif analysis_choice == "Inter Quartile Range":
                                    result = stats.iqr(filtered_df[column_choice])
                                elif analysis_choice == "S.D":
                                    result = filtered_df[column_choice].std()
                                elif analysis_choice == "Sum":
                                    result = filtered_df[column_choice].sum()
                                elif analysis_choice == "N":
                                    result = filtered_df[column_choice].count()
                                elif analysis_choice == "Percentage":
                                    result = (filtered_df[column_choice].sum() / filtered_df[column_choice].count()) * 100
                                else:
                                    result = "Unknown Analysis"
                            except Exception:
                                result = "Error"
    
                            result_row[column_name] = result
    
            # After processing all widget configurations for this file, append the result_row to results
            results.append(result_row)
    
    # Convert the results list to a DataFrame and save
    if results:
        results_df = pd.DataFrame(results)
        results_df.to_csv(save_path, index=False)
        print(f"Analysis results saved to '{save_path}'.")
    else:
        messagebox.showinfo("No Results", "No valid data found in the CSV files.")

    
    
# Menus
# Select menu


select_menu = tk.Menu(root, tearoff = False)
select_menu.add_command(label = 'Start Row', command = select_start_row)
select_menu.add_command(label = 'Folder', command = select_folder)
menu.add_cascade(label = 'Select', menu = select_menu)


#Exclude Values
values_menu = tk.Menu(root, tearoff = False)
values_menu.add_command(label = 'Trim', command = trim_values)
menu.add_cascade(label = 'Trim Values', menu = values_menu)

#Run Analysis
analysis_menu = tk.Menu(root, tearoff = False)
analysis_menu.add_command(label = 'Run', command = run_analysis)
menu.add_cascade(label = 'Analysis', menu = analysis_menu)

# Help menu
help_menu = tk.Menu(root, tearoff = False)
help_menu.add_command(label = 'Help', command = open_help_window)
help_menu.add_command(label = 'About', command =about_text)
menu.add_cascade(label = 'Help', menu = help_menu)


root.configure(menu=menu)


# Create dropwdown boxes
def selection_changed(event):
    selection = event.widget.get()
    messagebox.showinfo(
        title="New Selection",
        message=f"Selected option: {selection}"
    )
                        
# Function for adding a new row
def add_row():
    global row_counter
    row_counter +=1
    
    # Create a dropdown menu for the statistics choices
    c1= ttk.Combobox(b_frame,
        state="readonly",
        values=["N","Mean","S.D", "Median","IQR", "Sum", "Percentage"]
    )
    c1.bind()
    c1.place(x=50,y=50)
    c1.grid(row=row_counter, column = 0)
    
    c2= ttk.Combobox(b_frame,
        state="readonly",
        values=column_names
    )
    c2.bind()
    c2.place(x=50,y=50)
    c2.grid(row=row_counter,column=1)
    
    # Button to dynamically add condition columns
    b = tk.Button(b_frame, text="Add Condition", command=lambda r=row_counter: add_con(r))
    b.grid(row=row_counter, column=2)
    
    # Button to remove last added condition
    b1 = tk.Button(b_frame, text="Remove Condition", command=lambda r=row_counter: remove_con(r))
    b1.grid(row=row_counter, column=3)
    
    b2 = tk.Button(b_frame, text="Delete Row", command=lambda r=row_counter: del_row(r))
    b2.grid(row=row_counter, column=b_frame.grid_size()[0]-1)

    widgets[f"{row_counter}"] = {"buttons": [b, b1, b2], "combos": [c1,c2]}

# Function for deleting a row
def del_row(row):
    for w in widgets[f"{row}"]["buttons"] + widgets[f"{row}"]["combos"]:
        w.destroy()
    del widgets[f"{row}"]

    # Remove labels
    max_combos = max([len(widgets[k]["combos"])+1 for k in widgets])
    labels = b_frame.grid_slaves(row=0)
    if max_combos < len(labels):
        for i in range(0, (len(labels)-1)-max_combos):
            labels[i].destroy()


# Function for adding a new condition
def add_con(row):
    combos = widgets[f"{row}"]["combos"]
    
    c = ttk.Combobox(b_frame,
        state="readonly",
        values=column_names
    )
    c.grid(row=row, column=1+len(combos))
    widgets[f"{row}"]["combos"].append(c)
    
    # move "Remove Condition" button
    widgets[f"{row}"]["buttons"][1].grid(column=widgets[f"{row}"]["buttons"][1].grid_info()["column"]+1)
    
    # move "Add Row", "Delete Row" buttons
    max_col = b_frame.grid_size()[0]
    last_buttons = [widgets[k]["buttons"][2] for k in widgets]
    for b in last_buttons:
        if b.grid_info()["column"] != max_col:
            b.grid(column=max_col)
 
        
    # add column name
    labels = [l["text"] for l in b_frame.grid_slaves(row=0) if isinstance(l, tk.Label)]
    if f"Condition {len(combos)}" in labels:
        return
    else:
        newcond_label=tk.Label(b_frame, text=f"Condition {len(combos)-2}")
        newcond_label.grid(row=0, column=len(widgets[f"{row}"]["combos"]))


# Function for removing a condition
def remove_con(row):
    combos = widgets[f"{row}"]["combos"]
    if not widgets[f"{row}"]["combos"]:
        return
    if len(combos) <= 2:
        return
    
    # remove last added condition
    widgets[f"{row}"]["combos"][-1].destroy()
    del widgets[f"{row}"]["combos"][-1]
    
    # move "Remove Condition" button
    widgets[f"{row}"]["buttons"][1].grid(column=widgets[f"{row}"]["buttons"][1].grid_info()["column"]-1)

    # move "Add Row", "Delete Row" buttons
    max_col = b_frame.grid_size()[0]
    last_buttons = [widgets[k]["buttons"][2] for k in widgets]
    for b in last_buttons:
        if b.grid_info()["column"] != max_col:
            b.grid(column=max_col)
            
    # Remove last added label
    max_combos = max([len(widgets[k]["combos"]) for k in widgets])
    labels = b_frame.grid_slaves(row=0)
    if max_combos < len(labels)-1:
        labels[0].destroy()
    


# Buttons, labels and drop downs

# Show file path
path_label = tk.Label(t_frame, text="No folder selected yet")
path_label.grid(row=0,column=0)

# Stats label
stat_label=tk.Label(b_frame, text = "Statistics")
stat_label.grid(row=0,column=0)

# Excel column label
excol_label=tk.Label(b_frame, text = "Excel Column")
excol_label.grid(row=0,column=1)

# Condition? label
cond_label=tk.Label(b_frame, text = "Condition?")
cond_label.grid(row=0,column=2)

# Create a dropdown menu for the statistics choices
c1= ttk.Combobox(b_frame,
    state="readonly",
    values=["Mean","Median","Inter Quartile Range", "S.D","Sum", "N", "Percentage"]
)
c1.place(x=50,y=50)
c1.grid(row=1, column = 0)

# Create a dropdown menu for the column names from the excel sheet
c2= ttk.Combobox(b_frame,
    state="readonly",
    values=column_names
)
c2.place(x=50,y=50)
c2.grid(row=1,column=1)

# Button to dynamically add condition columns
b = tk.Button(b_frame, text="Add Condition", command=lambda row=row_counter: add_con(row))
b.grid(row=1, column=2)


# Button to remove last added condition
b1 = tk.Button(b_frame, text="Remove Condition", command=lambda row=row_counter: remove_con(row))
b1.grid(row=1, column=3)

# Button to duplicate row 1
b2 = tk.Button(b_frame, text="Add Row", command=add_row)
b2.grid(row=1, column=4)

# set first row
widgets[f"{row_counter}"] = {"buttons": [b, b1, b2], "combos": [c1, c2]}



root.mainloop()
