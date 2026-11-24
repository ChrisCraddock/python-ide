#pip install ttkbootstrap
import tkinter
import ttkbootstrap
import subprocess,sys #for accessing your system and for def run()
import re #regular expressions.  Importing for syntax highlighting

#re patterns in a dictionary
patterns = {
    'keywords': r'\b(def|class|if|else|elif|for|while|in|import|from|\
        return|True|False|None|and|or|not|try|except|with|as|print)\b',
    'strings': r'(["\'])(?:\\.|(?!\1).)*\1',
    'comments': r'#.*'
}

#Create Highlight function for re
#Highlights keywords/strings/comments if the text matches but removes highlight if not
def highlight(event=None):
    text = editor.get('1.0', 'end')
    for tag in ('keywords', 'strings', 'comments'):
        editor.tag_remove(tag, '1.0', 'end')

    for tag, pattern in patterns.items():
        for m in re.finditer(pattern, text): #iterates through patterns
            editor.tag_add(tag, f'1.0+{m.start()}c', f'1.0+{m.end()}c')



#Create Run function
def run():
    process = subprocess.run(
        [#Uses same python interp that runs this python file runs inside the window
            sys.executable,
            '-c', #tells python to execute the string as code
            editor.get('1.0', 'end')#Pass the text inside the code editor from start to end
        ],
        capture_output= True,
        text= True #capture as Text instead of Bytes
    )
    console.insert('end', process.stdout + process.stderr)#Get output and Error message

#Create Open File function
#Create variable named file_path
#Create list with tuple inside
def open_file():
    file_path = tkinter.filedialog.askopenfilename(filetypes=[('Python', '*.py')])
    if file_path:
        editor.delete('1.0', 'end')
        editor.insert('1.0', open(file_path, encoding='utf-8').read())
    highlight() #applys highlights when opening files

#Create Save File
#Create variable named file_path
#Create list with tuple inside
#If button clicked named file_path then write from line 1 to the end 
def save_file():
    file_path = tkinter.filedialog.asksaveasfilename(
        defaultextension='.py', filetypes=[('Python', '*.py')]
    )
    if file_path:
        open(file_path, 'w', encoding='utf-8').write(editor.get('1.0', 'end'))


#variable 'window'. Change theme inside .Window()
window = ttkbootstrap.Window(themename='darkly') #same as doing tkinter.Tk()
#window Title
window.title('Python Editor')

#Add menu bar and specify what you want to put inside it
menubar = ttkbootstrap.Frame(window) #window is the Parent
#Pack() default centers unless specified. X = horizontal, Y = vertical
menubar.pack(fill='x')

#What we want to put inside of the menu bar. 
#Pack() default stacks vertically unless side specified
#Refernce the open_file function
ttkbootstrap.Button(menubar, text='📂 Open File', command=open_file).pack(side='left') #Menubar is the Parent and text is button title

#Refernce the save_file function
ttkbootstrap.Button(menubar, text='💾 Save', command=save_file).pack(side='left') #Menubar is the Parent and text is button title

#Reference the 'run' function
ttkbootstrap.Button(menubar, text='▶️ Run', command=run).pack(side='left') #Menubar is the Parent and text is button title

#Create paned (split in 2) window.  Parent window and orientation, background color, spliter width
panedwindow = tkinter.PanedWindow(window, orient='vertical', background='#333333', sashwidth=5)
panedwindow.pack(fill='both', expand=True)

#Create editor. Place editor inside paned window. Give editor a bg color and fg (text) color
#Specify the font, size, and allow users to Undo
editor = tkinter.Text(panedwindow, background='#1e1e1e', foreground='#d4d4d4',
                      insertbackground='#d4d4d4', font=('Consolas', 12), undo=True)

#Add console
#Editor is created before the console and takes up most of the height
console = tkinter.Text(panedwindow, background='#111111', foreground='#dddddd',
                       font=('Consolas', 12), height=10)

#Staring line of code and empty char
editor.insert('1.0', '')




#Add editor inside the paned window
panedwindow.add(editor)
#Add console to the paned window
panedwindow.add(console)

#If any text is tagged, change the foreground of the text
editor.tag_configure('keywords', foreground='#569cd6')
editor.tag_configure('strings', foreground='#ce9178')
editor.tag_configure('comments', foreground='#6a9955')

#Constantly run loop to check for patterns
#Bind to key typing
editor.bind('<KeyRelease>', highlight)

#Keep window
window.mainloop()

# TODO: #Learn to fix regex
# TODO: #Learn how to accept inputs
