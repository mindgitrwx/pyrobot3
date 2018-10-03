# DEBUG
# import tkinter, string
import tkinter as tk
from tkinter.ttk import *
import string
from functools import reduce

def roundStr(item, places=3):
   """If item is a float, rounds to N places; otherwise just makes item a string."""
   values = []
   if type(item) == list:
      for v in item:
         if type(v) == float:
            values.append(('%%.%df'% places) % v)
         else:
            values.append(str(v))
      # return '[%s]' % string.join(values, ", ") DEBUG
      return '[%s]' % values.join(", ")
   else:
      return str(item)

class StatusBar(tk.Frame):
   def __init__(self, master):
      tk.Frame.__init__(self, master)
      self.label = tk.Label(self, bd=1, relief=tk.SUNKEN, anchor=tk.W)
      self.label.pack(fill=tk.X)

   def set(self, format, *args):
      self.label.config(text=format % args)
      self.label.update_idletasks()

   def clear(self):
      self.label.config(text="")
      self.label.update_idletasks()


####
#	Class Dialog
#
#	Purpose
#	Base class for many dialog box classes.
####

class Dialog:

	def __init__(self, master):
		self.master = master
		self.top = tk.Toplevel(self.master)
		self.top.title(self.__class__.__name__)
		self.top.minsize(1, 1)
		self.myWaitVar = repr(self.top) + 'EndDialogVar'

	def Show(self):
		self.SetupDialog()
		self.CenterDialog()
		self.top.deiconify()
		self.top.focus()

	def TerminateDialog(self, withValue):
		print("gui/widgets/TKwidgets Terminate Dialog") # DEBUG
		self.top.setvar(self.myWaitVar, withValue)
		self.top.withdraw()

	def DialogCleanup(self):
		self.top.destroy()
		self.master.focus()

	def SetupDialog(self):
		pass

	def CenterDialog(self):
		self.top.withdraw()
		self.top.update_idletasks()
		w = self.top.winfo_screenwidth()
		h = self.top.winfo_screenheight()
		reqw = self.top.winfo_reqwidth()
		reqh = self.top.winfo_reqheight()
		centerx = repr((w-reqw)/2)
		centery = repr((h-reqh)/2 - 100)
		geomStr = "+" + centerx + "+" + centery
		self.top.geometry("%dx%d%+d%+d" % (500, 500, 500, 500)) #DEBUG - not as i thin
		#self.top.geometry(geomStr) # DEBUG : REMOVED
####
#	Class ModalDialog
#
#	Purpose
#	Base class for many modal dialog box classes.
####

class ModalDialog(Dialog):

	def __init__(self, master):
		Dialog.__init__(self, master)

	def Show(self):
		import string
		self.SetupDialog()
		print("SetupDialog error log") # DEBUG
		self.CenterDialog()
		print("CenterDialog error log") # DEBUG
		#self.top.grab_set()
		print("top.grab_set error log") # DEBUG
		#self.top.focus()
		print("top.focus error log") # DEBUG
		self.top.deiconify()
		self.top.waitvar(self.myWaitVar)
                #print "waitvar =", self.top.getvar(self.myWaitVar), type(self.top.getvar(self.myWaitVar))
		result = self.top.getvar(self.myWaitVar)
                #print "result =", result, type(result)
		if type(result) == type(1):
		    return self.top.getvar(self.myWaitVar)
		else:
		    return string.atoi(self.top.getvar(self.myWaitVar))

####
#	Class AlertDialog
#
#	Purpose
#	-------
#
#	AlertDialog's are widgets that allow one to pop up warnings, one line
#	questions etc. They return a set of standard action numbers being :-
#	0 => Cancel was pressed
#	1 => Yes was pressed
#	2 => No was pressed
#
#	Standard Usage
#	--------------
#
#	F = AlertDialog(widget, message)
#	action = F.Show()
####

class AlertDialog(ModalDialog):

	def __init__(self, widget, msg):
		self.widget = widget
		self.msgString = msg
		Dialog.__init__(self, widget)

	def SetupDialog(self):
		import string
		upperFrame = tk.Frame(self.top)
		upperFrame['relief'] = 'raised'
		upperFrame['bd']	 = 1
		upperFrame.pack({'expand':'yes', 'side':'top', 'fill':'both' })
		self.bitmap = tk.Label(upperFrame)
		self.bitmap.pack({'side':'left'})
		# FIXED: jonghyeon
		#msgList = str.splitfields(self.msgString, "\n")
		msgList = str.split(self.msgString, "\n")
		for i in range(len(msgList)):
			msgText = tk.Label(upperFrame)
			msgText["text"]	  = msgList[i]
			msgText.pack({'expand':'yes', 'side':'top', 'anchor':'nw',
				'fill':'x' })
		self.lowerFrame = tk.Frame(self.top)
		self.lowerFrame['relief'] = 'raised'
		self.lowerFrame['bd']	 = 1
		self.lowerFrame.pack({'expand':'yes', 'side':'top', 'pady':'2',
			'fill':'both' })

	def OkPressed(self):
		self.TerminateDialog(1)

	def CancelPressed(self):
		self.TerminateDialog(0)

	def NoPressed(self):
		self.TerminateDialog(2)

	def CreateButton(self, text, command):
		self.button = tk.Button(self.lowerFrame)
		self.button["text"]	  = text
		self.button["command"]   = command
		self.button.pack({'expand':'yes', 'pady':'2', 'side':'left'})

	def CreateTextBox(self, text, width = 30, default = ""):
		frame = tk.Frame(self.lowerFrame)
		frame.pack({'expand':'yes', 'side' :'top', 'pady' :'2',
			'fill' :'x'})
		frame['relief'] = 'raised'
		frame['bd']	 = '2'
		label = tk.Label(frame)
		label['text'] = text
		label.pack({'side':'left', 'expand':'no', 'anchor':'w',
                            'fill':'none'})
		textbox = tk.Entry(frame, width=width, bg="white")
		textbox.insert(0, default)
		textbox.pack({'expand':'no', 'side':'right', 'fill':'x'})
		self.textbox[text] = textbox
		return textbox
####
#	Class ErrorDialog
#
#	Purpose
#	-------
#
#	To pop up an error message
####

class ErrorDialog(AlertDialog):

	def SetupDialog(self):
		AlertDialog.SetupDialog(self)
		self.bitmap['bitmap'] = 'error'
		self.CreateButton("OK", self.OkPressed)
                #self.CreatePickListBox("Something", lambda: "Click!")


####
#	Class WarningDialog
#
#	Purpose
#	-------
#
#	To pop up a warning message.
####

class WarningDialog(AlertDialog):

	def SetupDialog(self):
		AlertDialog.SetupDialog(self)
		self.bitmap['bitmap'] = 'warning'
		self.CreateButton("Yes", self.OkPressed)
		self.CreateButton("No", self.CancelPressed)

####
#	Class QuestionDialog
#
#	Purpose
#	-------
#
#	To pop up a simple question
####

class QuestionDialog(AlertDialog):

	def SetupDialog(self):
		AlertDialog.SetupDialog(self)
		self.bitmap['bitmap'] = 'question'
		self.CreateButton("Yes", self.OkPressed)
		self.CreateButton("No", self.NoPressed)
		self.CreateButton("Cancel", self.CancelPressed)


class AskDialog(AlertDialog):
   def __init__(self, root, title, qlist):
      AlertDialog.__init__(self, root, title)
      self.title = title
      self.qlist = qlist
      self.textbox = {}

   def SetupDialog(self):
      AlertDialog.SetupDialog(self)
      self.bitmap['bitmap'] = 'question'
      self.CreateButton("Ok", self.OkPressed)
      self.CreateButton("Cancel", self.CancelPressed)
      for (text, default) in self.qlist:
         self.CreateTextBox(text, width=30, default=default)

class Watcher(tk.Toplevel):
   def __init__(self, root):
      tk.Toplevel.__init__(self, root)
      self.winfo_toplevel().title("Pyrobot Expression Watcher")
      self.data = []
      self.winfo_toplevel().protocol('WM_DELETE_WINDOW',self.minimize)

   def minimize(self):
      self.withdraw()

   def unwatch(self, exp):
      i = 0
      for (oldExp, textbox) in self.data:
         if oldExp == exp:
            self.data.pop(i)
            textbox.destroy()
            return
         i += 1
      raise AttributeError("expression not found: '%s'" % exp)

   def watch(self, exp):
      self.deiconify()
      for (oldExp, textbox) in self.data:
         if oldExp == exp:
            return # don't watch the same expression more than once
      frame = self.CreateTextBox(exp, width=30, default="")
      self.data.append( (exp, frame))

   def update(self, locals = None):
      if locals == None:
         locals = globals()
      for exp, frame in self.data:
         try:
            value = roundStr(eval(exp, locals))
         except:
            value = "<Undefined>"
         frame.textbox.delete(0, 'end')
         frame.textbox.insert(0, value)

   def CreateTextBox(self, text, width = 30, default = ""):
      frame = tk.Frame(self)
      frame.pack({'expand':'no', 'side' :'top', 'pady' :'2',
                  'fill' :'x'})
      frame['relief'] = 'raised'
      frame['bd']	 = '2'
      label = tk.Label(frame)
      label['text'] = text
      label.pack({'side':'left', 'expand':'no', 'anchor':'w',
                  'fill':'none'})
      textbox = tk.Entry(frame, width=width, bg="white")
      textbox.insert(0, default)
      textbox.pack({'expand':'yes', 'side':'right', 'fill':'x'})
      label.bind("<1>", lambda event: self.unwatch(text))
      frame.textbox = textbox
      return frame

####
#	Class MessageDialog
#
#	Purpose
#	-------
#
#	To pop up a message.
####

class MessageDialog(AlertDialog):

	def SetupDialog(self):
		AlertDialog.SetupDialog(self)
		self.bitmap['bitmap'] = 'warning'
		self.CreateButton("Dismiss", self.CancelPressed)

####
#	Class FileDialog
#
#	Purpose
#	-------
#
#	FileDialog's are widgets that allow one to select file names by
#	clicking on file names, directory names, filters, etc.
#
#	Standard Usage
#	--------------
#
#	F = FileDialog(widget, some_title, some_filter)
#	if F.Show() != 1:
#		F.DialogCleanup()
#	return
#		file_name = F.GetFileName()
#		F.DialogCleanup()
####

class FileDialog(ModalDialog):

	#	constructor

	def __init__(self, widget, title, filter="*", pyro_dir = ''):
		from os import getcwd
        # FIXED: jonghyeon
		import string

		self.widget = widget
		self.filter = str.strip(filter)
		self.orig_dir = getcwd()
		self.pyro_dir = pyro_dir
		self.cwd = getcwd()
		self.lastCwd = self.cwd
		self.defaultFilename =""
                #	the logical current working directory
		Dialog.__init__(self, widget)

	#	setup routine called back from Dialog

	def HomePressed(self):
		from os import getenv
		print("HomePressed error log") # DEBUG
		if self.goHomeButton['text'] == 'Home':
		#if self.cwd != getenv('HOME') and \
		#       self.cwd != self.pyro_dir:
		    self.lastCwd = self.cwd
		    self.cwd = getenv('HOME')
		    self.goHomeButton['text'] = 'Pyrobot'
		    self.UpdateListBoxes()
		elif self.goHomeButton['text'] == 'Last':
		    tmp = self.cwd
		    self.cwd = self.lastCwd
		    #if tmp != getenv('HOME') and \
		    #       tmp != self.pyro_dir:
		    self.lastCwd = tmp
		    self.goHomeButton['text'] = 'Home'
		    self.UpdateListBoxes()
		elif self.goHomeButton['text'] == 'Pyrobot':
		    #if self.lastCwd != getenv('HOME') and \
		    #       self.lastCwd != self.pyro_dir:jjjj
		    #   self.goHomeButton['text'] = 'Last'
		    #else:
		    self.goHomeButton['text'] = 'Home'
		    self.lastCwd = self.cwd
		    self.cwd = self.pyro_dir
		    self.UpdateListBoxes()

	def SetupDialog(self):

		print("gui/widgets/TKwidgets/__init__ SetupDialog") # DEBUG
		# directory label

		self.dirFrame = tk.Frame(self.top)
		self.dirFrame['relief'] = 'raised'
		self.dirFrame['bd']	 = '2'
		self.dirFrame.pack({'expand':'no', 'side':'top', 'fill':'both'})
		self.dirLabel = tk.Label(self.dirFrame)
		self.dirLabel["text"] = "Directory:"
		self.dirLabel.pack({'expand':'no', 'side':'left', 'fill':'none'})
		# editable filter

		self.filterFrame = tk.Frame(self.top)
		self.filterFrame['relief'] = 'raised'
		self.filterFrame['bd']	 = '2'
		self.filterFrame.pack({'expand':'no', 'side':'top', 'fill':'both'})
		self.filterLabel = tk.Label(self.filterFrame)
		self.filterLabel["text"] = "Filter:"
		self.filterLabel.pack({'expand':'no', 'side':'left', 'fill':'none'})
		self.goHomeButton = tk.Button(self.filterFrame)
		self.goHomeButton["text"]	  = "Home"
		self.goHomeButton["command"]   = self.HomePressed
		self.goHomeButton["width"] = 8
		self.goHomeButton.pack({'expand':'yes', 'pady':'2', 'side':'right'})

		self.filterEntry = tk.Entry(self.filterFrame)
		self.filterEntry.bind('<Return>', self.FilterReturnKey)
		self.filterEntry["width"]  = "40"
		self.filterEntry["relief"] = "ridge"
		self.filterEntry.pack({'expand':'yes', 'side':'right', 'fill':'x'})
		self.filterEntry.insert(0, self.filter)

		# the directory and file listboxes

		self.listBoxFrame = tk.Frame(self.top)
		self.listBoxFrame['relief'] = 'raised'
		self.listBoxFrame['bd']	 = '2'
		self.listBoxFrame.pack({'expand':'no', 'side' :'top',
			'pady' :'2', 'padx': '0', 'fill' :'x'})
		self.CreateDirListBox()
		print("gui/widgets/TKwidgets/__init__ CreateDirListBox") # DEBUG
		self.CreateFileListBox()
		print("gui/widgets/TKwidgets/__init__ CreateFileListBox") # DEBUG
		self.UpdateListBoxes()
		print("gui/widgets/TKwidgets/__init__ CreateUpdateListFileListBox") # DEBUG

		# editable filename

		self.fileNameFrame = tk.Frame(self.top)
		self.fileNameFrame.pack({'expand':'no', 'side':'top', 'fill':'both'})
		self.fileNameFrame['relief'] = 'raised'
		self.fileNameFrame['bd']	 = '2'
		self.fileNameLabel = tk.Label(self.fileNameFrame)
		self.fileNameLabel["text"] = "File:"
		self.fileNameLabel.pack({'expand':'no', 'side':'left', 'fill':'none'})
		self.fileNameEntry = tk.Entry(self.fileNameFrame)
		self.fileNameEntry["width"]  = "40"
		self.fileNameEntry["relief"] = "ridge"
		self.fileNameEntry.pack({'expand':'yes', 'side':'right', 'fill':'x'})
		self.fileNameEntry.bind('<Return>', self.FileNameReturnKey)
		if self.defaultFilename:
		   self.fileNameEntry.insert(0, self.defaultFilename)

# help text:
		helpFrame = tk.Frame(self.top)
		scrollBar = tk.Scrollbar(helpFrame, {'orient':'vertical'})
		scrollBar.pack({'expand':'no', 'side':'right', 'fill':'y'})
		self.helpText = tk.Text(helpFrame, state="disabled",
		                             yscroll = scrollBar.set,
		                             height = 5, width = 50)
		self.helpText.pack({'expand':'yes', 'side' :'top',
		                    'pady' :'1','fill' :'both'})
		helpFrame.pack({'side':'top', 'expand':'yes', 'fill':'both'})
		scrollBar['command'] = self.helpText.yview

		#	buttons - ok, filter, cancel

		self.buttonFrame = tk.Frame(self.top)
		self.buttonFrame['relief'] = 'raised'
		self.buttonFrame['bd']	 = '2'
		self.buttonFrame.pack({'expand':'no', 'side':'top', 'fill':'x'})
		self.okButton = tk.Button(self.buttonFrame)
		self.okButton["text"]	  = "OK"
		self.okButton["command"]   = self.OkPressed
		self.okButton["width"] = 8
		self.okButton.pack({'expand':'yes', 'pady':'2', 'side':'left'})
		self.filterButton = tk.Button(self.buttonFrame)
		self.filterButton["text"]	  = "Filter"
		self.filterButton["command"]   = self.FilterPressed
		self.filterButton["width"] = 8
		self.filterButton.pack({'expand':'yes', 'pady':'2', 'side':'left'})
		button = tk.Button(self.buttonFrame)
		button["text"] = "Cancel"
		button["command"] = self.CancelPressed
		button["width"] = 8
		button.pack({'expand':'yes', 'pady':'2', 'side':'left'})

		button = tk.Button(self.buttonFrame)
		button["text"] = "Edit"
		button["command"] = self.EditPressed
		button["width"] = 8
		button.pack({'expand':'yes', 'pady':'2', 'side':'left'})

		button = tk.Button(self.buttonFrame)
		button["text"] = "My Copy"
		button["command"] = self.CopyPressed
		button["width"] = 8
		button.pack({'expand':'yes', 'pady':'2', 'side':'left'})

	#	create the directory list box

	def CreateDirListBox(self):
		frame = tk.Frame(self.listBoxFrame)
		frame.pack({'expand':'yes', 'side' :'left', 'pady' :'1',
			'fill' :'both'})
		frame['relief'] = 'raised'
		frame['bd']	 = '2'
		filesFrame = tk.Frame(frame)
		filesFrame['relief'] = 'flat'
		filesFrame['bd']	 = '2'
		filesFrame.pack({'side':'top', 'expand':'no', 'fill':'x'})
		label = tk.Label(filesFrame)
		label['text'] = 'Directories:'
		label.pack({'side':'left', 'expand':'yes', 'anchor':'w',
			'fill':'none'})
		scrollBar = tk.Scrollbar(frame, {'orient':'vertical'})
		scrollBar.pack({'expand':'no', 'side':'right', 'fill':'y'})
		self.dirLb = tk.Listbox(frame, {'yscroll':scrollBar.set})
		self.dirLb.pack({'expand':'yes', 'side' :'top', 'pady' :'1',
			'fill' :'both'})
		self.dirLb.bind('<Double-Button-1>', self.DoDoubleClickDir)
		scrollBar['command'] = self.dirLb.yview

	#	create the files list box

	def CreateFileListBox(self):
		frame = tk.Frame(self.listBoxFrame)
		frame['relief'] = 'raised'
		frame['bd']	 = '2'
		frame.pack({'expand':'yes', 'side' :'left', 'pady' :'1', 'padx' :'1',
			'fill' :'both'})
		filesFrame = tk.Frame(frame)
		filesFrame['relief'] = 'flat'
		filesFrame['bd']	 = '2'
		filesFrame.pack({'side':'top', 'expand':'no', 'fill':'x'})
		label = tk.Label(filesFrame)
		label['text'] = 'Files:'
		label.pack({'side':'left', 'expand':'yes', 'anchor':'w',
			'fill':'none'})
		scrollBar = tk.Scrollbar(frame, {'orient':'vertical'})
		scrollBar.pack({'side':'right', 'fill':'y'})
		self.fileLb = tk.Listbox(frame, {'yscroll':scrollBar.set})
		self.fileLb.pack({'expand':'yes', 'side' :'top', 'pady' :'0',
			'fill' :'both'})
		self.fileLb.bind('<1>', self.DoSelection)
                # This causes some problems on Debian computers
		self.fileLb.bind('<Double-Button-1>', self.DoDoubleClickFile)
		scrollBar['command'] = self.fileLb.yview

	#	update the listboxes and directory label after a change of directory

	def UpdateListBoxes(self):
        # FIXED
		import os
		#import commands
		#from subprocess import getoutput
		import subprocess

		# FIXED: cannot import name splitfields
		# from string import splitfields
		import string
		cwd = self.cwd
		self.fileLb.delete(0, self.fileLb.size())
		filter = self.filterEntry.get() # '*' will list recurively, we don't want that.

		if filter == '*':
		    filter = ''
		if os.name in ['nt', 'dos', 'os2']:
			cmd = "dir /b \"" + os.path.join(cwd, filter) + "\""
			pipe = os.popen(cmd + ' 2>&1', 'r')
			cmdOutput = pipe.read()
			pipe.close()
		elif os.name in ['posix']:
			print("gui/widgets/TKwidgets/__init__ cwd: %s?" % cwd) # DEBUG
			print("gui/widgets/TKwidgets/__init__ cmd?") # DEBUG
			cmd = "ls " + os.path.join(cwd, filter) + " | grep -v __init__.py"
			# FIXED
			print("gui/widgets/TKwidgets/__init__ cmd output?") # DEBUG
			cmdOutput = subprocess.getoutput(cmd)
			print("gui/widgets/TKwidgets/__init__/ UpdateListBoxes cmd") # DEBUG
			print("cmd: %s" % cmd) # DEBUG
			#cmdOutput = getoutput(cmd)
			# subprocess.check_output(cmd)
			# cmdOutput = subprocess.check_output(cmd)
			# cmdOutput = check_output()
		else:
			raise AttributeError("your OS (%s) is not supported" % os.name)

		# FIXED: cannot import name splitfields
		# files = splitfields(cmdOutput, "\n")
		print("gui/wigets/TKwidgets/__init__ cmdOutput: %s " % cmdOutput) # DEBUG
		files = cmdOutput.split("\n")
		files.sort()
		for i in range(len(files)):
		   if os.path.isfile(os.path.join(cwd, files[i])):
		      self.fileLb.insert('end', os.path.basename(files[i]))
		files = os.listdir(cwd)
		if cwd != '/':
		   files.append('..')
		files.sort()
		self.dirLb.delete(0, self.dirLb.size())
		for i in range(len(files)):
                   if os.path.isdir(os.path.join(cwd, files[i])):
                      if files[i] != 'CVS' and (files[i][0] != '.' or files[i] == '..'):
                         self.dirLb.insert('end', files[i])
		self.dirLabel['text'] = "Directory:" + self.cwd_print()
		print("gui/wigets/TKwidgets/__init__    sorted files") # DEBUG

	#	selection handlers

	def DoSelection(self, event):
		from posixpath import join
		import string
		print("gui/widgets/TKwidgets/__init__ DoSelection") # DEBUG
		lb = event.widget
		field = self.fileNameEntry
		# DEBUG : ERRROR OCCURED
		print("gui/widgets/TKwidgets/__init__ before get simulator") # DEBUG
		#field.delete(0, tk.AtEnd()) #DEBUG
		field.delete(0,'end') #DEBUG
		#field.delete(0, tk.End())
		print("gui/widgets/TKwidgets/__init__ cwd_print and nearest event y") # DEBUG
		print(self.cwd_print) # DEBUG
		print(lb.nearest(event.y)) # DEBUG
		field.insert(0, join(self.cwd_print(), lb.get(lb.nearest(event.y))))
		lb.select_clear(0, "end")
		lb.select_anchor(lb.nearest(event.y))
                # ------------------------------------
                # Get some help from the file
                # this could be the __docs__ string from
                # the module, but that would require us to load it
                # and that seems like not a good idea. Maybe better
                # to get data from a text file, or top of .py file
		if field.get()[-3:] == ".py" or field.get()[-6:] == ".world":
		   print("gui/widgets/TKwidgets/__init__ before field.get (get simulator name)") # DEBUG
		   print(field.get()) # DEBUG
		   fp = open(field.get(), "r")
		   lines = fp.readlines()
		   # DEBUG
		   # stringlines = string.join(lines, '')
		   stringlines = ''.join(lines)
		   print("gui/widgets/TKwidgets/__init__ print stringline") # DEBUG
		   print("gui/widgets/TKwidgets/__init__ stringline seems to cotennts of simulator file") # DEBUG
		   print(stringlines) # DEBUG
		   fp.close()
		else:
		   stringlines = "Click the 'OK' button to load."
		self.helpText.config(state='normal')
		self.helpText.delete(1.0, 'end')
		self.helpText.insert('end', stringlines )
		self.helpText.config(state='disabled')

	def DoDoubleClickDir(self, event):
		from posixpath import join
		lb = event.widget
		self.cwd = join(self.cwd, lb.get(lb.nearest(event.y)))
		print("DoDoubleClickDir error log") # DEBUG
		self.UpdateListBoxes()

	def DoDoubleClickFile(self, event):
		self.OkPressed()

	def OkPressed(self):
		self.TerminateDialog(1)

	def FileNameReturnKey(self, event):
		from posixpath import isabs, expanduser, join
		# FIXED:jonghyeon
		import string
		#	if its a relative path then include the cwd in the name
		name = str.strip(self.fileNameEntry.get())
		if not isabs(expanduser(name)):
			self.fileNameEntry.delete(0, 'end')
			self.fileNameEntry.insert(0, join(self.cwd_print(), name))
		self.okButton.flash()
		self.OkPressed()

	def FilterReturnKey(self, event):
		# FIXED:jonghyeon
		# from string import strip
		import string
		filter = str.strip(self.filterEntry.get())
		self.filterEntry.delete(0, 'end')
		self.filterEntry.insert(0, filter)
		self.filterButton.flash()
		print("FilterReturnKey error log") # DEBUG
		self.UpdateListBoxes()

	def FilterPressed(self):
		print("FilterPressed error log") # DEBUG
		self.UpdateListBoxes()

	def CancelPressed(self):
		self.TerminateDialog(0)

	def CopyPressed(self):
	   import os
	   filename = self.fileNameEntry.get()
	   myfilename = os.getenv("HOME") + "/my" + filename.split("/")[-1]
	   if os.name in ['nt', 'dos', 'os2'] :
	      os.system("copy %s %s" %(filename, myfilename))
	   else:
	      os.system("cp -i %s %s" %(filename, myfilename))
	   self.fileNameEntry.delete(0, 'end')
	   self.fileNameEntry.insert(0, myfilename)
	   self.EditPressed(myfilename, 1)

	def EditPressed(self, filename = None, selectIt = 0):
	   import os
	   if filename == None:
	      filename = self.fileNameEntry.get()
	   if os.getenv("EDITOR"):
	      editor = os.getenv("EDITOR")
	   else:
	      editor = "vim"
	   os.system("%s %s &" % (editor, filename))
	   self.TerminateDialog(0) #selectIt)

    # FIXME: LoadFileDialog has no attribute fileNameEntry
	def GetFileName(self):
		return self.fileNameEntry.get()

	#	return the logical current working directory in a printable form
	#	ie. without all the X/.. pairs. The easiest way to do this is to
	#	chdir to cwd and get the path there.

	def cwd_print(self):
		from os import chdir, getcwd
		chdir(self.cwd)
		p = getcwd()
		chdir(self.orig_dir)
		return p

####
#	Class LoadFileDialog
#
#	Purpose
#	-------
#
#	Specialisation of FileDialog for loading files.
####

class LoadFileDialog(FileDialog):

	def __init__(self, master, title, filter, pyro_dir = ''):
	   FileDialog.__init__(self, master, title, filter, pyro_dir)
	   self.top.title(title)

	def OkPressed(self):
		fileName = self.GetFileName()
		if file_exists(fileName) == 0:
			str = 'File ' + fileName + ' not found.'
			errorDlg = ErrorDialog(self.top, str)
			errorDlg.Show()
			errorDlg.DialogCleanup()
			return
		FileDialog.OkPressed(self)

####
#	Class SaveFileDialog
#
#	Purpose
#	-------
#
#	Specialisation of FileDialog for saving files.
####

class SaveFileDialog(FileDialog):
	def __init__(self, master, title, filter, defaultFilename=""):
		FileDialog.__init__(self, master, title, filter)
		self.defaultFilename = defaultFilename
		self.top.title(title)

	def OkPressed(self):
		fileName = self.GetFileName()
		if file_exists(fileName) == 1:
			str = 'File ' + fileName + ' exists.\nDo you wish to overwrite it?'
			warningDlg = WarningDialog(self.top, str)
			if warningDlg.Show() == 0:
				warningDlg.DialogCleanup()
				return
			warningDlg.DialogCleanup()
		FileDialog.OkPressed(self)

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)


        self.button = tk.Button(self)
        self.button['text'] = 'Load File...'
        self.button['command'] = self.Press
        self.button.pack({"side": "top"})

        self.pack()

    def Press(self):
        fileDlg = filedlg.LoadFileDialog(app, "Load File", "*", '')
        if fileDlg.Show() != 1:
            fileDlg.DialogCleanup()
            return
        fname = fileDlg.GetFileName()
        self.button['text'] = 'File: ' + fname
        fileDlg.DialogCleanup()

#
#	Return whether a file exists or not.
#	The file "" is deemed to not exist
#

def file_exists(file_name):
	from posixpath import exists
	import string
	if len(file_name) == 0:
		return 0
	else:
		return exists(file_name)

#
#	read the lines from a file and strip them of their trailing newlines
#

def readlines(fd):
	# FIXED: jonghyeon
	import string
	return list(map(lambda s, f=str.strip: f(s), fd.readlines()))

#
#	Various set operations on sequence arguments.
#	in joins the values in 'a' take precedence over those in 'b'
#

def seq_join(a, b):
	res = a[:]
	for x in b:
		if x not in res:
			res.append(x)
	return res

def seq_meet(a, b):
	res = []
	for x in a:
		if x in b:
			res.append(x)
	return res

def seq_diff(a, b):
	res = []
	for x in a:
		if x not in b:
			res.append(x)
	return res

#
#	Various set operations on map arguments.
#	The values in 'a' take precedence over those in 'b' in all cases.
#

def map_join(a, b):
	res = {}
	for x in list(a.keys()):
		res[x] = a[x]
	for x in list(b.keys()):
		if x not in res:
			res[x] = b[x]
	return res

def map_meet(a, b):
	res = {}
	for x in list(a.keys()):
		if x in b:
			res[x] = a[x]
	return res

def map_diff(a, b):
	res = {}
	for x in list(a.keys()):
		if x not in b:
			res[x] = a[x]
	return res

#
#	Join a map of defaults values with a map of set values. The defaults
#	map is taken to be total, and hence any keys not in the defaults, but
#	in the settings, must be errors.
#

def map_join_total(settings, defaults):
	res = map_join(settings, defaults)
	for x in list(settings.keys()):
		if x not in defaults:
			raise "merge_defaults"
	return res

#
#	Return a string being the concatenation of a sequence of objects
#	NOTE: we apply the routine recursively to sequences of sequences
#

def seq_to_str(s):
	if type(s) == type((1,)) or type(s) == type([]):
		return reduce(lambda sum, a: sum + seq_to_str(a), s, "")
	else:
		return str(s)

#
#	a dummy function for any number of arguments
#

def dummy(*args):
	pass

#
#	the true and false functions for any number of args
#

def true(*args):
	return 1

def false(*args):
	return 0

#
#	return whether a char is printable or not
#

def is_printable(c):
	o = ord(c)
	return c == "\n" or (o >= 32 and o <= 126)

#
#	return a printable version of a given string
#	by simply omitting non printable characters
#

def string_printable(s):
	length = len(s)
	ok = 1
	res = ""
	l = 0
	for i in range(length):
		if not is_printable(s[i]):
			res = res + s[l:i]
			l = i+1
			ok = 0
	if ok:
		return s
	else:
		return res + s[l:length]


if __name__ == "__main__":
   from tkinter import Tk
   tk = Tk()
   w = Watcher(tk)
   w.watch("w")
   w.mainloop()
