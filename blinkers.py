#https://www.codespeedy.com/create-a-text-editor-in-python/

# Importing Required libraries & Modules
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter.font import Font
# Defining TextEditor Class
class TextEditor:
  TITLE = "Blinkers | Extremism Research Text Editor"

  # Used to identify if is filtering and what the current path to the filter file is
  filter_file = None

  FONT_COLOR_RANGE = ["#FFFFFF","#F8F8F8","#F5F5F5","#F0F0F0","#E8E8E8","#E0E0E0","#DCDCDC","#D8D8D8","#D3D3D3","#D0D0D0","#C8C8C8","#C0C0C0","#BEBEBE","#B8B8B8","#B0B0B0","#A9A9A9","#A8A8A8","#A0A0A0","#989898","#909090","#888888","#808080","#787878","#707070","#696969","#686868","#606060","#585858","#505050","#484848","#404040","#383838","#303030","#282828","#202020","#181818","#101010","#080808","#000000"]
  CURRENT_COLOR_VAL = int(len(FONT_COLOR_RANGE) / 2)

  # Defining Constructor
  def __init__(self,root):
    # Assigning root
    self.root = root
    # Title of the window
    self.root.title(self.TITLE)
    # Window Geometry
    self.root.geometry("1200x700+200+150")
    # Initializing filename
    self.filename = None
    # Declaring Title variable
    self.title = StringVar()
    # Declaring Status variable
    self.status = StringVar()
    # Creating Titlebar
    self.titlebar = Label(self.root,textvariable=self.title,font=("times new roman",15,"bold"),bd=2,relief=GROOVE)
    # Packing Titlebar to root window
    self.titlebar.pack(side=TOP,fill=BOTH)
    # Calling Settitle Function
    self.settitle()
    # Creating Statusbar
    self.statusbar = Label(self.root,textvariable=self.status,font=("times new roman",15,"bold"),bd=2,relief=GROOVE)
    # Packing status bar to root window
    self.statusbar.pack(side=BOTTOM,fill=BOTH)
    # Initializing Status
    self.status.set(self.TITLE)
    # Creating Menubar
    self.menubar = Menu(self.root,font=("times new roman",15,"bold"),activebackground="skyblue")
    # Configuring menubar on root window
    self.root.config(menu=self.menubar)
    # Creating File Menu
    self.filemenu = Menu(self.menubar,font=("times new roman",12,"bold"),activebackground="skyblue",tearoff=0)
    # Adding New file Command
    self.filemenu.add_command(label="New",accelerator="Ctrl+N",command=self.newfile)
    # Adding Open file Command
    self.filemenu.add_command(label="Open",accelerator="Ctrl+O",command=self.openfile)
    # Adding Save File Command
    self.filemenu.add_command(label="Save",accelerator="Ctrl+S",command=self.savefile)
    # Adding Save As file Command
    self.filemenu.add_command(label="Save As",accelerator="Ctrl+A",command=self.saveasfile)
    # Adding Seprator
    self.filemenu.add_separator()
    # Adding Exit window Command
    self.filemenu.add_command(label="Exit",accelerator="Ctrl+E",command=self.exit)
    # Cascading filemenu to menubar
    self.menubar.add_cascade(label="File", menu=self.filemenu)
    # Creating Edit Menu
    self.editmenu = Menu(self.menubar,font=("times new roman",12,"bold"),activebackground="skyblue",tearoff=0)
    # Adding Cut text Command
    self.editmenu.add_command(label="Cut",accelerator="Ctrl+X",command=self.cut)
    # Adding Copy text Command
    self.editmenu.add_command(label="Copy",accelerator="Ctrl+C",command=self.copy)
    # Adding Paste text command
    self.editmenu.add_command(label="Paste",accelerator="Ctrl+V",command=self.paste)
    # Adding Undo text Command
    self.editmenu.add_command(label="Undo",accelerator="Ctrl+U",command=self.undo)
    # Adding Seprator
    self.editmenu.add_separator()
    # Cascading editmenu to menubar
    self.menubar.add_cascade(label="Edit", menu=self.editmenu)
    # Creating Help Menu
    self.helpmenu = Menu(self.menubar,font=("times new roman",12,"bold"),activebackground="skyblue",tearoff=0)
    # Adding About Command
    self.helpmenu.add_command(label="About",command=self.infoabout)
    # Cascading helpmenu to menubar
    self.menubar.add_cascade(label="Help", menu=self.helpmenu)
    # Creating Scrollbar
    scrol_y = Scrollbar(self.root,orient=VERTICAL)
    # Fonts
    self.FILTERED_FONT = Font(family="times new roman", size=14, weight="bold")
    self.NORMAL_FONT = Font(family="times new roman", size=15, weight="normal")
    # Creating Text Area
    self.txtarea = Text(self.root,yscrollcommand=scrol_y.set,foreground=self.FONT_COLOR_RANGE[self.CURRENT_COLOR_VAL],font=self.NORMAL_FONT,state="normal",relief=GROOVE)
    # Adding filter text command
    self.editmenu.add_command(label="Add Filter File",accelerator="Ctrl+F", command=self.choose_filter)
    # Adding clear filter text command
    self.editmenu.add_command(label="Remove Filters",accelerator="Ctrl+R", command=self.clear_filter)
    # Add and remove string to filter file
    self.editmenu.add_command(label="Add String To Filter", accelerator="Ctrl+P",command=self.add_to_filter)
    self.editmenu.add_command(label="Remove String From Filter", accelerator="Ctrl+B", command=self.remove_from_filter)
    # Adding Seprator
    self.editmenu.add_separator()
    self.editmenu.add_command(label="Increase Color Saturation", accelerator="Alt+U", command=self.increase_font_color)
    self.editmenu.add_command(label="Decrease Color Saturation", accelerator="Alt+D", command=self.decrease_font_color)
    # Packing scrollbar to root window
    scrol_y.pack(side=RIGHT,fill=Y)
    # Adding Scrollbar to text area
    scrol_y.config(command=self.txtarea.yview)
    # Packing Text Area to root window
    self.txtarea.pack(fill=BOTH,expand=1)
    # Calling shortcuts funtion
    self.shortcuts()

  # Defining settitle function
  def settitle(self):
    # Checking if Filename is not None
    if self.filename:
      # Updating Title as filename
      self.title.set(self.filename)
    else:
      # Updating Title as Untitled
      self.title.set("Untitled")
  # Defining New file Function
  def newfile(self,*args):
    # Clearing the Text Area
    self.txtarea.delete("1.0",END)
    # Updating filename as None
    self.filename = None
    # Calling settitle funtion
    self.settitle()
    # updating status
    self.status.set("New File Created")
  # Defining Open File Funtion
  def openfile(self,*args):
    # Exception handling
    try:
      # Asking for file to open
      self.filename = filedialog.askopenfilename(title = "Select file",filetypes = (("All Files","*.*"),("Text Files","*.txt"),("Python Files","*.py")))
      # checking if filename not none
      if self.filename:
        # opening file in readmode
        infile = open(self.filename,"r")
        # Clearing text area
        self.txtarea.delete("1.0",END)
        # Inserting data Line by line into text area
        for line in infile:
          self.txtarea.insert(END,line)
        # Closing the file
        infile.close()
        # Calling Set title
        self.settitle()
        self.txtarea.tag_add("NORMAL", '1.0', END)
        # Updating Status
        self.status.set("Opened Successfully")

        if self.filter_file is not None:
          self.filter(self.filter_file)
    except Exception as e:
      messagebox.showerror("Exception",e)
  # Defining Save File Funtion
  def savefile(self,*args):
    # Exception handling
    try:
      # checking if filename not none
      if self.filename:
        # Reading the data from text area
        data = self.txtarea.get("1.0",END)
        # opening File in write mode
        outfile = open(self.filename,"w")
        # Writing Data into file
        outfile.write(data)
        # Closing File
        outfile.close()
        # Calling Set title
        self.settitle()
        # Updating Status
        self.status.set("Saved Successfully")
      else:
        self.saveasfile()
    except Exception as e:
      messagebox.showerror("Exception",e)
  # Defining Save As File Funtion
  def saveasfile(self,*args):
    # Exception handling
    try:
      # Asking for file name and type to save
      untitledfile = filedialog.asksaveasfilename(title = "Save file As",defaultextension=".txt",initialfile = "Untitled.txt",filetypes = (("All Files","*.*"),("Text Files","*.txt"),("Python Files","*.py")))
      # Reading the data from text area
      data = self.txtarea.get("1.0",END)
      # opening File in write mode
      outfile = open(untitledfile,"w")
      # Writing Data into file
      outfile.write(data)
      # Closing File
      outfile.close()
      # Updating filename as Untitled
      self.filename = untitledfile
      # Calling Set title
      self.settitle()
      # Updating Status
      self.status.set("Saved Successfully")
    except Exception as e:
      messagebox.showerror("Exception",e)
  # Defining Exit Funtion
  def exit(self,*args):
    op = messagebox.askyesno("WARNING","Your Unsaved Data May be Lost!!")
    if op>0:
      self.root.destroy()
    else:
      return
  # Define filter file
  def choose_filter(self, *args):
    file_name = filedialog.askopenfilename(title="Select file", filetypes=(
          ("All Files", "*.*"), ("Text Files", "*.txt"), ("Python Files", "*.py")))
    self.filter(file_name)
    self.status.set("Set Filters Sucessfully")

  def decrease_font_color(self, *args):
    if len(self.txtarea.get("1.0", END)) > 1:
      self.txtarea.tag_add("NORMAL", '1.0', END)
      self.CURRENT_COLOR_VAL = self.CURRENT_COLOR_VAL - 1
      if self.CURRENT_COLOR_VAL < 0:
        self.CURRENT_COLOR_VAL = 0

      self.txtarea.tag_configure("NORMAL", font=self.NORMAL_FONT, foreground=self.FONT_COLOR_RANGE[self.CURRENT_COLOR_VAL])
      self.filter(self.filter_file)
      self.status.set("Color Saturation {} of {}".format(self.CURRENT_COLOR_VAL, len(self.FONT_COLOR_RANGE)-1))

  def increase_font_color(self, *args):

    if len(self.txtarea.get("1.0",END)) > 1:

      self.txtarea.tag_add("NORMAL", '1.0', END)
      self.CURRENT_COLOR_VAL = self.CURRENT_COLOR_VAL + 1
      if self.CURRENT_COLOR_VAL > len(self.FONT_COLOR_RANGE)-1:
        self.CURRENT_COLOR_VAL = len(self.FONT_COLOR_RANGE)-1

      self.txtarea.tag_configure("NORMAL", font=self.NORMAL_FONT, foreground=self.FONT_COLOR_RANGE[self.CURRENT_COLOR_VAL])
      self.filter(self.filter_file)
      self.status.set("Color Saturation {} of {}".format(self.CURRENT_COLOR_VAL, len(self.FONT_COLOR_RANGE)-1))

  # Clear all filters
  def clear_filter(self, *args):
    # Used to clear all filters
    if self.txtarea:
      self.txtarea.tag_remove("BOLD", '1.0', END)
      self.txtarea.tag_configure("NORMAL", font=self.NORMAL_FONT)
      # Set normal text to
      self.txtarea.tag_add("NORMAL", '1.0', END)
      self.filter_file = None
      self.status.set("Removed Filters Sucessfully")

  def filter(self, filename):

      try:

          # loop through file adding words on each line to a list
          list_of_filter_words = []
          if filename:

             self.txtarea.tag_add("NORMAL", '1.0', END)
             self.filter_file = filename
             file_contents = open(filename, "r")
             for word in file_contents.readlines():
                 list_of_filter_words.append(word.strip().lower())

             self.txtarea.tag_configure("BOLD", font=self.FILTERED_FONT,foreground="red")

          # loop through the words to highlight and if they're found highlights them
          for word in list_of_filter_words:
            list_of_idxs = self.find(word)
            for idx_dict in list_of_idxs:
              idx = idx_dict["idx"]
              last_idx = idx_dict["lastidx"]
              if idx and last_idx:
                self.txtarea.tag_add("BOLD", idx, last_idx)


      except Exception as e:
          messagebox.showerror("Exception", e)

  def add_to_filter(self, *args):
    # Used to add a selected string to the filter file

    keywords = []
    if self.filter_file is None:
      self.filter_file = ".filter_file.txt"

    else:
      with open(self.filter_file, 'r') as file:
        for word in file.readlines():
          keywords.append(word.strip())

    selected_text = self.txtarea.selection_get()

    # Read file, add new word, and write to file. Appending wasn't wokrking as expected

    if selected_text.strip().lower() not in keywords:
      keywords.append(selected_text.strip().lower())
      with open(self.filter_file, 'w') as file:
        for word in keywords:
          file.write(word + "\n")

      self.filter(self.filter_file)
      self.status.set("Added Word '{}' To Filter File".format(selected_text))

    else:
      self.status.set("Word '{}' Already In Filter File".format(selected_text))


  def remove_from_filter(self, *args):
    # Used to remove a string from the filter

    if self.filter_file is not None:
      selected_text = self.txtarea.selection_get().lower()

      # Read file, add new word, and write to file. Appending wasn't wokrking as expected
      keywords = []
      with open(self.filter_file, 'r') as file:
        for word in file.readlines():
          keywords.append(word.strip().lower())

      if selected_text in keywords:
        keywords.remove(selected_text)

        keywords = list(set(keywords))

        with open(self.filter_file, 'w') as file:
          for word in keywords:
            file.write(word + "\n")

        self.txtarea.tag_remove("BOLD", '1.0', END)
        self.filter(self.filter_file)
        self.status.set("Removed Word '{}' From Filter File".format(selected_text))
      else:
        self.status.set("Couldn't Remove Text From Filter, As '{}' Is Not In Filter File".format(selected_text))

    else:
      self.status.set("Couldn't Remove Text From Filter, As No Filter File Is Set")

  def find(self, text_to_find):
    # returns the idex and the last idex for a given string in the text area. returns None if not found.

    list_of_found_words = []

    number_of_occurances = self.txtarea.get("1.0",END).lower().count(text_to_find)
    idx = '1.0'

    for iterator in range(0,number_of_occurances+1):
      self.txtarea.tag_remove('found', '1.0', END)

      idx = self.txtarea.search(text_to_find, idx, nocase=1,
                          stopindex=END)
      if idx:
        lastidx = '%s+%dc' % (idx, len(text_to_find))
      else:
        lastidx = None
        idx = None

      list_of_found_words.append({"idx":idx,"lastidx":lastidx})
      idx = lastidx

    return list_of_found_words

  # Defining Cut Funtion
  def cut(self,*args):
    self.txtarea.event_generate("<<Cut>>")
  # Defining Copy Funtion
  def copy(self,*args):
          self.txtarea.event_generate("<<Copy>>")
  # Defining Paste Funtion
  def paste(self,*args):
    self.txtarea.event_generate("<<Paste>>")
  # Defining Undo Funtion
  def undo(self,*args):
    # Exception handling
    try:
      # checking if filename not none
      if self.filename:
        # Clearing Text Area
        self.txtarea.delete("1.0",END)
        # opening File in read mode
        infile = open(self.filename,"r")
        # Inserting data Line by line into text area
        for line in infile:
          self.txtarea.insert(END,line)
        # Closing File
        infile.close()
        # Calling Set title
        self.settitle()
        # Updating Status
        self.status.set("Undone Successfully")
      else:
        # Clearing Text Area
        self.txtarea.delete("1.0",END)
        # Updating filename as None
        self.filename = None
        # Calling Set title
        self.settitle()
        # Updating Status
        self.status.set("Undone Successfully")
    except Exception as e:
      messagebox.showerror("Exception",e)
  # Defining About Funtion
  def infoabout(self):
    messagebox.showinfo("About {}".format(self.TITLE),"Blinkers is a simple text editor and viewer written in Python.\nThe purpose of Blinkers is to give extreamism researchers a simple text editor that allows for filtering out violent or sensative strings. www.github.com/CartographerLabs/Blinkers")
  # Defining shortcuts Funtion
  def shortcuts(self):
    # Binding Ctrl+F
    self.txtarea.bind("<Control-f>", self.choose_filter)
    # Binding Ctrl+F+C
    self.txtarea.bind("<Control-r>", self.clear_filter)
    # Binding Ctrl+P
    self.txtarea.bind("<Control-p>", self.add_to_filter)
    # Binding Ctrl+s
    self.txtarea.bind("<Control-b>", self.remove_from_filter)
    # Bind up and down arrows
    self.txtarea.bind("<Alt-u>", self.increase_font_color)
    self.txtarea.bind("<Alt-d>", self.decrease_font_color)
    # Binding Ctrl+n to newfile funtion
    self.txtarea.bind("<Control-n>",self.newfile)
    # Binding Ctrl+o to openfile funtion
    self.txtarea.bind("<Control-o>",self.openfile)
    # Binding Ctrl+s to savefile funtion
    self.txtarea.bind("<Control-s>",self.savefile)
    # Binding Ctrl+a to saveasfile funtion
    self.txtarea.bind("<Control-a>",self.saveasfile)
    # Binding Ctrl+e to exit funtion
    self.txtarea.bind("<Control-e>",self.exit)
    # Binding Ctrl+x to cut funtion
    self.txtarea.bind("<Control-x>",self.cut)
    # Binding Ctrl+c to copy funtion
    self.txtarea.bind("<Control-c>",self.copy)
    # Binding Ctrl+v to paste funtion
    self.txtarea.bind("<Control-v>",self.paste)
    # Binding Ctrl+u to undo funtion
    self.txtarea.bind("<Control-u>",self.undo)
# Creating TK Container
root = Tk()
# Passing Root to TextEditor Class
TextEditor(root)
# Root Window Looping
root.mainloop()