"""Auto Marker with a GUI"""
__author__ = 'Mikha Davids'
#14/05/2019
#If I want to use .grid within a frame I need to say in_=<frame> as the first parameter
#eliminate component variables where possible
#Maybe use a new class for the file being debugged and store script and script path and script dir in that. Perhaps even allow the user to save these objects and reload them
#DON'T USE A WILD CARD IMPORT. FIND EVERYTHING I AM USING FROM TKINTER AND IMPORT IT INDIVIDUALLY
from os.path import isfile
from tkinter import *
from tkinter import filedialog, scrolledtext, messagebox
#Changes the style of the widgets
import tkinter.ttk as ttk

#Internal window functions
def GUIwrite(sl_string, end='\n') :
    sctxt_output.configure(state='normal')
    sctxt_output.insert(INSERT, sl_string + end)
    sctxt_output.configure(state='disabled')

def GUIoverWrite(sl_string, end='\n') :
    sctxt_output.configure(state='normal')
    sctxt_output.delete(1.0,END)
    sctxt_output.insert(INSERT, sl_string + end)
    sctxt_output.configure(state='disabled')

def toggleFileNames() :
    if b_stdIO.get() :
        frm_IOfileNames.pack_forget()
    else:
        frm_IOfileNames.pack(padx=i_buffer*3, pady=i_buffer, side=TOP, anchor=W, fill=BOTH, expand=YES)

def togglePromptsInFile() :
    if b_inputPrompts.get() :
        frm_promptsInFile.pack(padx=i_buffer*3, pady=i_buffer, side=TOP, anchor=W, fill=BOTH, expand=YES)
    else:
        frm_promptsInFile.pack_forget()

def scriptBrowse() :
    s_filePath = filedialog.askopenfilename(filetypes=(('Python scripts', '*.py'), ('All files', '*.*')))
    if s_filePath:
        edt_script.delete(0,END)
        edt_script.insert(0, s_filePath)

def inputFileBrowse() :
    s_filePath = filedialog.askopenfilename(filetypes=(('Text files', '*.txt'), ('All files', '*.*')))
    if s_filePath:
        edt_inputFile.delete(0,END)
        edt_inputFile.insert(0, s_filePath)

def outputFileBrowse() :
    s_filePath = filedialog.askopenfilename(filetypes=(('Text files', '*.txt'), ('All files', '*.*')))
    if s_filePath:
        edt_outputFile.delete(0,END)
        edt_outputFile.insert(0, s_filePath)
    
def exitWindow() :
    if bs_settings.get() or bs_files.get():
        al_booleanVars = [var for var in globals().keys() if var[:2] == 'b_']
        with open(s_settingsFile, 'w') as fl_file :
            if bs_settings.get() :
                print('[settings]', file=fl_file)
                for var in al_booleanVars :
                    print(f'{var[2:]}={eval(var).get()}', file=fl_file)

            if bs_files.get() :
                print('[files]', file=fl_file)
                print(f'script={edt_script.get()}', file=fl_file)
                if not b_stdIO.get() :
                    print(f'inputFile={edt_inputFile.get()}', file=fl_file)
                    print(f'outputFile={edt_outputFile.get()}', file=fl_file)
    else:
        fl_file = open(s_settingsFile, 'w')
        fl_file.close()
    AM_window.destroy()


def run() :
    AM_window.scriptPath = edt_script.get()
    #Check that script has been entered and exists.
    if AM_window.scriptPath :
        if not isfile(AM_window.scriptPath):
            messagebox.showwarning('Script missing', 'The file you specified to mark does not exist or is incorrectly named.')
            return
        
        il_pathEnd = AM_window.scriptPath.rfind('/')
        if il_pathEnd == -1 :
            il_pathEnd = AM_window.scriptPath.rfind('\\')
        if il_pathEnd != -1 :
            AM_window.scriptDir = AM_window.scriptPath[:il_pathEnd + 1]
            AM_window.script = AM_window.scriptPath[il_pathEnd+1:]
        else:
            AM_window.script = AM_window.scriptPath

    else:
        messagebox.showwarning('Field missing', 'Please fill in the path of the script to mark')
        return
    #Check if default IO files are being used and that they exist
    if b_stdIO.get() :
        AM_window.inputFilePath = f'{AM_window.scriptPath}{s_inputFile}'
        AM_window.outputFilePath = f'{AM_window.scriptPath}{s_outputFile}'
    else:
        AM_window.inputFilePath = edt_inputFile.get()
        AM_window.outputFilePath = edt_outputFile.get()
        #Perhaps add more detail to this error message
        if not isfile(AM_window.inputFilePath) or not isfile(AM_window.outputFilePath):
            messagebox.showwarning('IO File missing', 'Your input and/or output file is missing from the specified directory or is incorrectly named.')
        return
    GUIoverWrite(f'Automarking {AM_window.script}...', end='\n\n')
    GUIwrite('Executing program')




#Fonts
fnt_label = ('Arial Narrow', 13, 'bold')
#Defaults
s_inputFile = 'sampleinput.txt'
s_outputFile = 'sampleoutput.txt'
s_browseButtonText = '. . .'
s_settingsFile = 'AM_settings.ini'
#Help messages
s_help_script = "Input the absolute or relative file path of the python script to mark."
s_help_IO = ''
s_help_inputFile = ''
s_help_outputFile = ''
s_help_inputPrompts = ''
s_help_promptsInFile = ''
s_help_showWhenWrong = ''

AM_window = Tk()
AM_window.title("Mikha's Auto Marker")
AM_window.wm_state('zoomed')

b_stdIO = BooleanVar(value=True)
b_inputPrompts = BooleanVar(value=False)
b_promptsInFile = BooleanVar(value=True)
b_expectedOut, b_yourOut, b_input, b_diffs = BooleanVar(value=True), BooleanVar(value=True), BooleanVar(value=True), BooleanVar(value=True)
bs_settings = BooleanVar(value=False)

a_settings = []
if isfile(s_settingsFile):
    with open(s_settingsFile, 'r') as f_file :
        a_settings = f_file.readlines()

if a_settings and '[settings]\n' in a_settings :
    bs_settings = BooleanVar(value=True)
    for line in a_settings[a_settings.index('[settings]\n')+1:] :
        if '=' not in line :
            break
        s_variable, s_value = line.split('=')
        if type(eval(s_value)) is bool :
            exec(f'b_{s_variable} = BooleanVar(value={s_value})')

screen_width = AM_window.winfo_screenwidth()
i_buffer = screen_width//150
frm_input = Frame(AM_window)

frm_script = Frame(frm_input)
lbl_script = Label(frm_script, text='Path of script to mark:', font=fnt_label, cursor='hand2')
lbl_script.bind('<Button-1>', lambda _ : messagebox.showinfo("Information", s_help_script))
lbl_script.pack(side=TOP, anchor=W)
edt_script = ttk.Entry(frm_script)
edt_script.pack(side=LEFT, anchor=W, fill=BOTH, expand=YES)
edt_script.focus()
btn_scriptBrowse = Button(frm_script, bg='white', text=s_browseButtonText, cursor='hand2', command=scriptBrowse)
btn_scriptBrowse.pack(side=LEFT, anchor=W)
frm_script.pack(side=TOP, anchor=W, fill=BOTH)

frm_IOfiles = Frame(frm_input)
lbl_IO = Label(frm_IOfiles, text='Use standard input and output files:', font=fnt_label, cursor='hand2')
lbl_IO.bind('<Button-1>', lambda _ : messagebox.showinfo('Information', s_help_IO))
lbl_IO.pack(side=TOP, anchor=W)
rbtn_stdIO = ttk.Radiobutton(frm_IOfiles, text='Yes', cursor='hand2', value=True, variable=b_stdIO, command=toggleFileNames)
rbtn_stdIO.pack(side=TOP, anchor=W)
rbtn_notStdIO = ttk.Radiobutton(frm_IOfiles, text='No', cursor='hand2', value=False, variable=b_stdIO, command=toggleFileNames)
rbtn_notStdIO.pack(side=TOP, anchor=W)

frm_IOfileNames = Frame(frm_IOfiles)
frm_InputFile = Frame(frm_IOfileNames)
lbl_inputFile = Label(frm_InputFile, text='Input file path:', font=fnt_label, cursor='hand2')
lbl_inputFile.bind('<Button-1>', lambda _ : messagebox.showinfo('Information', s_help_inputFile))
lbl_inputFile.pack(side=TOP, anchor=W)
edt_inputFile = ttk.Entry(frm_InputFile)
edt_inputFile.pack(side=LEFT, anchor=W, fill=BOTH, expand=YES)
btn_inputFileBrowse = Button(frm_InputFile, bg='white', text=s_browseButtonText, cursor='hand2', command=inputFileBrowse)
btn_inputFileBrowse.pack(side=LEFT, anchor=W)
frm_InputFile.pack(side=TOP, anchor=W, fill=BOTH)

frm_OutputFile = Frame(frm_IOfileNames)
lbl_outputFile = Label(frm_OutputFile, text='Output file path:', font=fnt_label, cursor='hand2')
lbl_outputFile.bind('<Button-1>', lambda _ : messagebox.showinfo('Information', s_help_outputFile))
lbl_outputFile.pack(side=TOP, anchor=W)
edt_outputFile = ttk.Entry(frm_OutputFile)
edt_outputFile.pack(side=LEFT, anchor=W, fill=BOTH, expand=YES)
btn_outputFileBrowse = Button(frm_OutputFile, bg='white', text=s_browseButtonText, cursor='hand2', command=outputFileBrowse)
btn_outputFileBrowse.pack(side=LEFT, anchor=W)
frm_OutputFile.pack(side=TOP, anchor=W, fill=BOTH)

if not b_stdIO.get():
    toggleFileNames()

frm_IOfiles.pack(side=TOP, anchor=W, fill=BOTH)

frm_inputPrompts = Frame(frm_input)
lbl_inputPrompts = Label(frm_inputPrompts, text='input() functions contain prompts:', font=fnt_label, cursor='hand2')
lbl_inputPrompts.bind('<Button-1>', lambda _ : messagebox.showinfo('Information', s_help_inputPrompts))
lbl_inputPrompts.pack(side=TOP, anchor=W)
rbtn_inputPrompts = ttk.Radiobutton(frm_inputPrompts, text='Yes', cursor='hand2', value=True, variable=b_inputPrompts, command=togglePromptsInFile)
rbtn_inputPrompts.pack(side=TOP, anchor=W)
rbtn_noInputPrompts = ttk.Radiobutton(frm_inputPrompts, text='No', cursor='hand2', value=False, variable=b_inputPrompts, command=togglePromptsInFile)
rbtn_noInputPrompts.pack(side=TOP, anchor=W)

frm_promptsInFile = Frame(frm_inputPrompts)
lbl_promptsInFile = Label(frm_promptsInFile, text='Input prompts in file', font=fnt_label, cursor='hand2')
lbl_promptsInFile.bind('<Button-1>', lambda _ : messagebox.showinfo('Information', s_help_promptsInFile))
lbl_promptsInFile.pack(side=TOP, anchor=W)
rbtn_promptsInFile = ttk.Radiobutton(frm_promptsInFile, text='Yes', cursor='hand2', value=True, variable=b_promptsInFile)
rbtn_promptsInFile.pack(side=TOP, anchor=W)
rbtn_promptsNotInFile = ttk.Radiobutton(frm_promptsInFile, text='No', cursor='hand2', value=False, variable=b_promptsInFile)
rbtn_promptsNotInFile.pack(side=TOP, anchor=W)

if b_inputPrompts.get():
    togglePromptsInFile()

frm_inputPrompts.pack(side=TOP, anchor=W, fill=BOTH)

frm_showOutput = Frame(frm_input)
lbl_showWhenWrong = Label(frm_showOutput, text='Show when output not correct:', font=fnt_label, cursor='hand2')
lbl_showWhenWrong.bind('<Button-1>', lambda _ : messagebox.showinfo('Information', s_help_showWhenWrong))
lbl_showWhenWrong.pack(side=TOP, anchor=W)
cbx_expectedOut = ttk.Checkbutton(frm_showOutput, text='Expected output', cursor='hand2', variable=b_expectedOut)
cbx_expectedOut.pack(side=TOP, anchor=W)
cbx_yourOut = ttk.Checkbutton(frm_showOutput, text='Your output', cursor='hand2', variable=b_yourOut)
cbx_yourOut.pack(side=TOP, anchor=W)
cbx_input = ttk.Checkbutton(frm_showOutput, text='Input', cursor='hand2', variable=b_input)
cbx_input.pack(side=TOP, anchor=W)
cbx_diffs = ttk.Checkbutton(frm_showOutput, text='Differences', cursor='hand2', variable=b_diffs)
cbx_diffs.pack(side=TOP, anchor=W)
frm_showOutput.pack(side=TOP, anchor=W, fill=BOTH)

bs_files = BooleanVar(value=False)
if a_settings and '[files]\n' in a_settings :
    bs_files = BooleanVar(value=True)
    for line in a_settings[a_settings.index('[files]\n')+1:] :
        if '=' not in line :
            break
        s_variable, s_value = line.split('=')
        if s_value[-1] == '\n' :
            s_value = s_value[:-1]
        exec(f'edt_{s_variable}.insert(0, "{s_value}")')

cbx_files = ttk.Checkbutton(frm_input, text='Remember files', cursor='hand2', variable=bs_files)
cbx_files.pack(side=BOTTOM, anchor=SW)
cbx_settings = ttk.Checkbutton(frm_input, text='Remember settings', cursor='hand2', variable=bs_settings)
cbx_settings.pack(side=BOTTOM, anchor=SW)

frm_input.pack(side=LEFT, anchor=W, padx=i_buffer, pady=i_buffer, fill=BOTH, expand=YES)

btn_run = Button(frm_input, height=i_buffer//4, bg='white', text='Run', font=('Arial', 12), cursor='hand2', command=run)
btn_run.pack(pady=i_buffer, anchor=CENTER, fill=X)

sctxt_output = scrolledtext.ScrolledText(AM_window, state='disabled')
sctxt_output.pack(side=RIGHT, anchor=E, padx=i_buffer, pady=i_buffer, fill=BOTH, expand=YES)

AM_window.protocol('WM_DELETE_WINDOW', exitWindow)
AM_window.mainloop()