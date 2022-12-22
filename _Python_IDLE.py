import os
import sys

from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

class App(Tk):
    def __init__(self):
        super(App, self).__init__()

        # Important attributes/variables
        self._input_box, self._output_box = None, None
        self._file_path = ''
        
        # Configure the App
        self._configure_app()

        # Set button frame
        self._button_frame()

        # Set IO frame
        self._IO_frame()
    
    
    def _configure_app(self):
        self.title('Python IDLE')
        self.geometry('630x680')
        self.resizable(False, False)
        self.configure(background='#0B0719')

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=20)
        self.columnconfigure(0, weight=1)

    def _button_frame(self):
        f = Frame(self, bg='#0B0719')
        f.grid(row=0, column=0, sticky=W+E+N+S)

        f.columnconfigure(2, weight=10)

        Button(f, text='Save', fg='red', command=self._save).grid(row=0, column=0, sticky=W)
        Button(f, text='Open', fg='blue', command=self._open).grid(row=0, column=1, sticky=W)
        Button(f, text='Run', fg='green', command=self._run).grid(row=0, column=2, sticky=E)

        for widget in f.winfo_children():
            widget.configure(relief='flat', font='Arial 15 bold')
            widget.grid(padx=15, pady=12, ipadx=4)

    def _save(self):
        if(not self._file_path):
            self._file_path = filedialog.asksaveasfilename(initialdir=os.getcwd(), filetypes=[('Python file', '*.py')])

        with open(self._file_path, 'w') as python_file:
            python_file.write( (self._input_box.get('1.0', END)).strip() )

    def _open(self):
        self._file_path = filedialog.askopenfilename(filetypes=[('Python files', '*.py')], initialdir=os.getcwd())
        
        with open(self._file_path, 'r') as python_file:
            python_code = (python_file.read()).strip()
            self._input_box.delete('1.0', END)
            self._input_box.insert('1.0', python_code)
    
    def _run(self):
        if(not self._file_path):
            messagebox.showwarning('Warning', 'Please, Save the file first!')
            return
        
        cmd = 'xterm -e \'{} {} ; read -p "******** hit ENTER to close the window ********"\''.format(sys.executable, self._file_path)
        os.system(cmd)

    def _IO_frame(self):
        f = Frame(self, bg='#0B0719')
        f.grid(row=1, column=0, sticky=E+W+N+S)

        f.grid_rowconfigure(0, weight=1)
        f.grid_columnconfigure(0, weight=1)

        # Set Input field
        self._input_field(f)

        for widget in f.winfo_children():
            widget.grid(padx=15, pady=15)
    
    def _input_field(self, f):
        self._input_box = Text(f, bg='lightgray', font='Consola 10')
        self._input_box.grid(row=0, column=0, sticky=N+S)


if __name__ == '__main__':
    app = App()
    app.mainloop()