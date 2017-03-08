from tkinter import *
import os
file_name = None
root = Tk()
root.geometry("600x700")
root.title("Kobani")

"""
color scheme is defined with dictionary elements like -
        theme_name : foreground_color.background_color
"""
color_schemes = {
    'Default': '#000000.#FFFFFF',
    'Greygarious': '#83406A.#D1D4D1',
    'Aquamarine': '#5B8340.#D1E7E0',
    'Bold Beige': '#4B4620.#FFF0E1',
    'Cobalt Blue': '#ffffBB.#3333aa',
    'Olive Green': '#D1E7E0.#5B8340',
    'Night Mode': '#FFFFFF.#000000',
}

#creating callbacks and adding Text widget built in functionality
def cut(event=None):
    content_text.event_generate("<<Cut>>")
    update_line_numbers()
    return "break"

def copy():
    content_text.event_generate("<<Copy>>")
    return "break"

def paste():
    content_text.event_generate("<<Paste>>")
    update_line_numbers()
    return "break"

def undo():
    content_text.event_generate("<<Undo>>")
    update_line_numbers()
    return "break"

def redo(event=None):
    content_text.event_generate("<<Redo>>")
    update_line_numbers()
    return "break"

def select_all(event=None):
    content_text.tag_add("sel",1.0, END)
    return "break"

def search_output(needle, ignore_case, content_text, toplevel, search_box):
    content_text.tag_remove("match", "1.0", END)
    match_found = 0
    if needle:
        start_pos = "1.0"
        while True:
            start_pos = content_text.search(needle, start_pos,
                                            nocase=ignore_case, stopindex=END)
            if not start_pos:
                break
            end_pos = "{}+{}c".format(start_pos, len(needle))
            content_text.tag_add("match", start_pos, end_pos)
            start_pos = end_pos
            match_found += 1
        content_text.tag_config("match", foreground="red", background="yellow")
        search_box.focus_set()
        toplevel.title("{} matches found".format(match_found))
        

def find_text(event=None):
    search_toplevel = Toplevel(root)
    search_toplevel.title("Find text")
    search_toplevel.transient(root)#set toplevel window on parent window
    search_toplevel.resizable(False, False)
    Label(search_toplevel, text="Find All:").grid(row =0, column=0,
                                                  sticky="e")
    search_entry = Entry(search_toplevel, width=35)
    search_entry.focus_set()
    search_entry.grid(row=0, column=1, padx=2, pady=2, sticky="we")
    ignore_case = IntVar()
    Checkbutton(search_toplevel, text="Ignore Case",
                variable=ignore_case).grid(row=1, column=1, sticky="e",
                                           padx=2, pady=2)
    Button(search_toplevel, text="Find All", underline=0,
           command= lambda: search_output(search_entry.get(),
                                          ignore_case.get(), content_text,
                                    search_toplevel,search_entry)).grid(row=0,
                                    column=2, sticky="we", padx=2, pady=2)
    #bind will pass the event as parameter to the callback , this why
    #we use lambda event, where even will not be used 
    search_entry.bind("<Return>",lambda event: search_output(search_entry.get(),
                                          ignore_case.get(), content_text,
                                    search_toplevel,search_entry)) 
    
    def close_search():
        content_text.tag_remove("match","1.0", END)
        search_toplevel.destroy()
    search_toplevel.protocol("WM_DELETE_WINDOW",
                             close_search)
    return "break"


def open_file(event=None):
    input_file_name = filedialog.askopenfilename(defaultextension=".text",
                                                 filetypes=[("All File","*.*"),
                                                    ("Text Document","*.text")])
    if input_file_name:
        global file_name
        file_name = input_file_name
        root.title("{}".format(os.path.basename(file_name)))
        content_text.delete(1.0, END)
        with open(file_name, "r") as _file:
            content_text.insert(1.0, _file.read())
    update_line_numbers()
    return "break"

def save(event=None):
    global file_name
    if not file_name:
        save_as()
    else:
        write_to_file(file_name)
    return "break"

def write_to_file(file_name):
    try:
        content = content_text.get(1.0, END)
        with open(file_name, "w") as _file:
            _file.write(content)
    except IOError:
        pass

def save_as(event=None):
    #input_file_name is a absulote path not only the file name 
    input_file_name = filedialog.asksaveasfilename(defaultextension=".txt",
                filetypes=[("All Files","*.*"), ("Text Documents", "*.txt")])
    if input_file_name:
        global file_name
        file_name = input_file_name
        write_to_file(file_name)
        root.title(os.path.basename(file_name))
    return "break"

def new_file(event=None):
    global file_name
    file_name = None
    content_text.delete(1.0, END)
    root.title("Untitled")
    return "break"

def display_about(event=None):
    messagebox.showinfo(title="About",
                        message="Kobani TextEditor\nDevelopment\nDlo Bagari")

def display_help(event=None):
    messagebox.showinfo("Help", "TKinter GUI application", icon="question")

def exit_editor(event=None):
    #askokcancel return boolean
    if messagebox.askokcancel("Quit?", "would you like to exit?"):
        root.destroy()

def on_content_changed (event=None):
    update_line_numbers()
    update_cursor_info()

def update_line_numbers(event=None):
    line_number = get_line_numbers()
    line_number_bar.config(state="normal")
    line_number_bar.delete(1.0, END)
    line_number_bar.insert(1.0, line_number)
    line_number_bar.config(state="disabled")
    line_number_bar.see(END)#to show list line number scroll up


def get_line_numbers():
    if show_line_no.get():
        indx = content_text.index(END).split(".")[0]
        return  " ~\n".join(str(line) for line in range(1, int(indx))) +" ~"
    return ""

def highlight(event=None):
    if highlight_line.get():
        to_highlight_line()
    else:
        undo_highlight_line()

def to_highlight_line(time=100):
    content_text.tag_remove("active_line", 1.0, END)
    content_text.tag_add("active_line", "insert linestart", "insert lineend+1c")
    #lineend is up to last character in the line
    #lineend+1c is up to the and of the line , the full line 
    content_text.after(time, highlight)

def undo_highlight_line():
    content_text.tag_remove("actine line", 1.0, END)

def update_cursor_info(event=None):
    row, col = content_text.index(INSERT).split(".")
    line, col_num = str(int(row)), str(int(col) + 1)#column start from 0
    cursor_info_bar.config(text="Line: {0} | Column: {1}".format(line, col_num))

def show_cursor_bar():
    value = show_cursor_info.get()
    if value:
        cursor_info_bar.pack(expand=NO, fill=None, side=RIGHT, anchor="se")
    else:
        cursor_info_bar.pack_forget()
        
    
def change_themes(event=None):
    choice = theme_choice.get()
    colors = color_schemes[choice]
    fg, bg = colors.split(".")
    content_text.config(background=bg, foreground=fg)

def show_popup_menu(event=None):
    popup_menu.tk_popup(event.x_root, event.y_root)


                                            
root.protocol("WM_DELETE_WINDOW", exit_editor)   
menu_bar = Menu(root)
#loading icons
new_file_icon = PhotoImage(file="icons/new_file.png")
open_file_icon = PhotoImage(file="icons/open_file.png")
save_file_icon = PhotoImage(file='icons/save.png')
cut_icon = PhotoImage(file='icons/cut.png')
copy_icon = PhotoImage(file='icons/copy.png')
paste_icon = PhotoImage(file='icons/paste.png')
undo_icon = PhotoImage(file='icons/undo.png')
redo_icon = PhotoImage(file='icons/redo.gif')

#treatoff is for separating the menu from the top , takes values true or false
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", accelerator="Ctrt+N",
                    compound="left", image=new_file_icon, underline=0,
                      command=new_file)          
file_menu.add_command(label="Open", accelerator="Ctrl+O",
                      compound="left", image=open_file_icon, underline=0,
                      command=open_file)
file_menu.add_command(label="Save", accelerator="Ctrl+S", compound="left",
                      image=save_file_icon, underline=0,
                      command=save)
file_menu.add_command(label='Save as', accelerator='Shift+Ctrl+S',
                        command=save_as)
file_menu.add_separator()#add separator space
file_menu.add_command(label='Exit', accelerator='Alt+F4', command=exit_editor)
menu_bar.add_cascade(label="File", menu=file_menu)


edit_menu = Menu(menu_bar, tearoff=0)
edit_menu.add_command(label='Undo', accelerator='Ctrl+Z',
                      compound='left', image=undo_icon, command=undo)
edit_menu.add_command(label='Redo', accelerator='Ctrl+Y',
                      compound='left', image=redo_icon, command=redo)
edit_menu.add_separator()
edit_menu.add_command(label='Cut', accelerator='Ctrl+X',
                      compound='left', image=cut_icon, command=cut)
edit_menu.add_command(label='Copy', accelerator='Ctrl+C',
                      compound='left', image=copy_icon, command=copy)
edit_menu.add_command(label='Paste', accelerator='Ctrl+V',
                      compound='left', image=paste_icon, command=paste)
edit_menu.add_separator()
edit_menu.add_command(label='Find', underline=0, accelerator='Ctrl+F',
                      command=find_text)
edit_menu.add_separator()
edit_menu.add_command(label='Select All', underline=7, accelerator='Ctrl+A'
                      , command=select_all)
menu_bar.add_cascade(label="Edit", menu=edit_menu)

view_menu = Menu(menu_bar, tearoff=0)
show_line_no = IntVar()
show_line_no.set(1)
view_menu.add_checkbutton(label="Show Line Number", variable=show_line_no,
                          command=on_content_changed)
show_cursor_info = IntVar()
show_cursor_info.set(1)
view_menu.add_checkbutton(label="Show Cursor Location at Bottom",
                          variable=show_cursor_info,
                          command=show_cursor_bar)
highlight_line = BooleanVar()
view_menu.add_checkbutton(label="Highlight Current Line", onvalue=1,
                          offvalue=0, variable=highlight_line,
                          command=highlight)
themes_menu = Menu(menu_bar, tearoff=0)
view_menu.add_cascade(label="Themes", menu= themes_menu)


theme_choice = StringVar()
theme_choice.set("Default")
for k in sorted(color_schemes):
    themes_menu.add_radiobutton(label=k, variable=theme_choice,
                                command=change_themes)

menu_bar.add_cascade(label="View", menu=view_menu)

about_menu = Menu(menu_bar, tearoff=0)
about_menu.add_command(label='About', command=display_about)
about_menu.add_command(label='Help', command= display_help)
menu_bar.add_cascade(label="About", menu=about_menu)

#set frames for shortcuts and Text line numbers
shortcut_bar = Frame(root, height=25, background="light sea green")
shortcut_bar.pack(expand="no", fill=X)
icons = ("new_file", "open_file", "save", "cut", "copy", "paste",
         "undo", "redo", "find_text")
for i, icon in enumerate(icons):
    tool_bar_icon = PhotoImage(file="icons/{}.gif".format(icon))
    cmd = eval(icon)
    tool_bar = Button(shortcut_bar, image=tool_bar_icon, command=cmd)
    tool_bar.image = tool_bar_icon
    tool_bar.pack(side="left")
#state is editable , disable is mean can not be edit
#wrap is to wrap at end of the line id the line is to long , takes values
#"none", "word", "char"
line_number_bar = Text(root, width=4, padx=3, takefocus=0, border=0, cursor="",
                            background="khaki", state="disabled", wrap="none")
line_number_bar.pack(side="left", fill=Y)

#create the text area
content_text = Text(root, wrap="word", undo=1)
content_text.tag_configure("active_line", background="ivory2")
content_text.pack(expand="yes", fill = "both")
#create scrollbar and and content_text to it
scroll_bar = Scrollbar(content_text, cursor="hand1")
#bind the content y and line_number_bar scroll to scroll_bar
content_text.configure(yscrollcommand = scroll_bar.set)
scroll_bar.config(command=content_text.yview)
scroll_bar.pack(side="right", fill=Y)
cursor_info_bar = Label(content_text, text="Line: 1 | Column 1")
cursor_info_bar.pack(expand=NO, fill=None, side=RIGHT, anchor="se")

popup_menu = Menu(content_text,tearoff=0 )
for i in ("cut", "copy", "paste", "undo", "redo"):
    cmd = eval(i)
    popup_menu.add_command(label=i, compound="left", command=cmd)
popup_menu.add_separator()
popup_menu.add_command(label="Select All",underline=7,command=select_all)
content_text.bind("<Button-3>", show_popup_menu)
content_text.bind("<Button-1>",update_cursor_info)
#ctrl+y is bounded to paste functionality we have to override this binding
#to make ctrl+y be binded to the redo functionality
content_text.bind("<Control-y>", redo)#this will call redo function andd pass event
content_text.bind("<Control-Y>", redo)#redo(event)
content_text.bind("<Control-f>", find_text)
content_text.bind("<Control-F>",find_text)
content_text.bind("<Any-KeyPress>", on_content_changed)
root.bind("<Control-s>", save)
root.bind("<Control-S>", save)
root.bind("<Control-o>", open_file)
root.bind("<Control-O>", open_file)
root.bind("<Control-Shift-s>", save_as)
root.bind("<Control-Shift-S>", save_as)
root.bind("<Control-n>", new_file)
root.bind("<Control-N>", new_file)
root.bind("<KeyPress-F1>", display_help)
root.bind("<Alt-e>", exit_editor)

#his will be called after the the system becomes idle , no n=more events to
#process in mainloop
#root.after_idle(display_help)

root.config(menu=menu_bar)
root.mainloop()

