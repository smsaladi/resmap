'''
ResMap: Tkinter GUI wrapper for ResMap algorithm. (Alp Kucukelbir, 2013)
             
Please see ResMap_algorithm.py for details and documentation.

'''
import Tkinter as tk
from tkFileDialog import askopenfilename
from tkMessageBox import showerror
from tkMessageBox import showinfo

from ResMap_fileIO import *
from ResMap_algorithm import ResMap_algorithm

def load_file(fileNameStringVar):
	options =  {}
	# options['filetypes'] = [ ("All files", ".*"), ("MRC map", ".map,.mrc") ]
	options['title'] = "ResMap - Select data file"
	fname = askopenfilename(**options)
	if fname:
		try:
			fileNameStringVar.set(fname)
		except:                     # <- naked except is a bad idea
			showerror("Open Source File", "Failed to read file\n'%s'" % fname)
		return  

def checkInputs():

	# Check volume file name and try loading MRC file
	if volFileName.get() == "":
		showerror("Check Inputs", "'volFileName' is not set. Please select a MRC volume to analyze.")
		return
	else:
		try:
			inputFileName = volFileName.get()
			data = mrc_image(inputFileName)
			data.read(asBool=0)
			data = data.image_data
		except:
			showerror("Check Inputs", "The MRC volume could not be read.")
			return

	# Check voxel size
	if voxelSize.get() == "":
		showerror("Check Inputs", "'voxelSize' is not set. Please input a voxel size in Angstroms.")
		return
	else:
		try:
			vxSize = float(voxelSize.get())
		except ValueError:
			showerror("Check Inputs", "'voxelSize' is not a valid number. Please input a valid voxel size in Angstroms.")
			return

		if vxSize <= 0:
			showerror("Check Inputs", "'voxelSize' is not a positive number. Please input a positive voxel size in Angstroms.")
			return

	# Check confidence level
	if alphaValue.get() == "":
		showerror("Check Inputs", "'alphaValue' is not set. Please input a valid confidence level.")
		return
	else:
		try:
			pValue = float(alphaValue.get())
		except ValueError:
			showerror("Check Inputs", "'alphaValue' is not a valid number. Please input a valid confidence level.")
			return

		if pValue <= 0 or pValue > 0.05:
			showerror("Check Inputs", "'alphaValue' is outside of (0, 0.05]. Please input a valid confidence level.")
			return

	# Check min resolution
	if minRes.get() == "":
		showerror("Check Inputs", "'minRes' is not set. Please input a valid minimum resolution in Angstroms.")
		return
	else:
		try:
			Mbegin = float(minRes.get())
		except ValueError:
			showerror("Check Inputs", "'minRes' is not a valid number. Please input a valid minimum resolution in Angstroms.")
			return

		if Mbegin < 0.0:
			showerror("Check Inputs", "'minRes' is not a positive number. Please input a positive minimum resolution in Angstroms.")
			return

	# Check max resolution
	if maxRes.get() == "":
		showerror("Check Inputs", "'maxRes' is not set. Please input a valid maximum resolution in Angstroms.")
		return
	else:
		try:
			Mmax = float(maxRes.get())
		except ValueError:
			showerror("Check Inputs", "'maxRes' is not a valid number. Please input a valid maximum resolution in Angstroms.")
			return

		if Mmax < 0.0:
			showerror("Check Inputs", "'maxRes' is not a positive number. Please input a positive maximum resolution in Angstroms.")
			return	

	# Check step size
	if stepRes.get() == "":
		showerror("Check Inputs", "'stepRes' is not set. Please input a valid step size in Angstroms.")
		return
	else:
		try:
			Mstep = float(stepRes.get())
		except ValueError:
			showerror("Check Inputs", "'stepRes' is not a valid number. Please input a valid step size in Angstroms.")
			return

		if Mstep < 0.5:
			showerror("Check Inputs", "'stepRes' is too small. Please input a step size greater than 0.5 in Angstroms.")
			return	

	# Check mask file name and try loading MRC file
	if maskFileName.get() == "":
		showerror("Check Inputs", "'maskFileName' is not set. Please type (None;) without the parantheses.")
		return
	elif maskFileName.get().split(';',1)[0] == "None":
		dataMask = 0
	else:
		try:
			maskVolFileName = maskFileName.get()
			dataMask = mrc_image(maskVolFileName)
			dataMask.read(asBool=1)
			dataMask = dataMask.image_data
		except:
			showerror("Check Inputs", "The MRC mask file could not be read.")
			return

	showinfo("ResMap","Inputs are all valid!\n\nPress OK to close GUI and RUN.\n\nCheck console for progress.")

	root.destroy()

	# Call ResMap
	ResMap_algorithm(
			inputFileName = inputFileName,
			data          = data,
			vxSize        = vxSize,
			pValue        = pValue,
			Mbegin        = Mbegin,
			Mmax          = Mmax,
			Mstep         = Mstep,
			dataMask      = dataMask
		 )

	raw_input("\n:: DONE :: Press any key or close window to EXIT.")

	return

def showDocumentation():
	showinfo("ResMap Documentation","Please visit http://sf.net/p/resmap for help.")
	return

def showAbout():
	showinfo("About ResMap",
		("This is ResMap v1.0.2.\n\n"
		 "If you use ResMap in your work, please cite the following paper:\n\n" 
		 "A. Kucukelbir, F.J. Sigworth, H.D. Tagare, The Local Resolution of Cryo-EM Density Maps, In Review, 2013.\n\n"
		 "This package is released under the Creative Commons Attribution-NonCommercial-NoDerivs CC BY-NC-ND License (http://creativecommons.org/licenses/by-nc-nd/3.0/)\n\n"
		 "Please send comments, suggestions, and bug reports to alp.kucukelbir@yale.edu or hemant.tagare@yale.edu"))
	return

# Create root window 
root = tk.Tk()
root.title("Local Resolution Map (ResMap)")

# Create frame widget that holds everything 
mainframe = tk.Frame(root)
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(   0, weight=1)

# Create menubar
menubar = tk.Menu(root)
root.config(menu=menubar)

helpMenu = tk.Menu(menubar)
helpMenu.add_command(label="Documentation", command=showDocumentation)
helpMenu.add_command(label="About ResMap",  command=showAbout)
menubar.add_cascade(label="Help", menu=helpMenu)

# Create tk StringVars 
volFileName  = tk.StringVar()
voxelSize    = tk.StringVar()
alphaValue   = tk.StringVar(value="0.05")
minRes       = tk.StringVar(value="0.0")
maxRes       = tk.StringVar(value="0.0")
stepRes      = tk.StringVar(value="1.0")
maskFileName = tk.StringVar(value="None; ResMap will automatically compute a mask. Load File to override.")

# ROW 0
tk.Label(mainframe, text="Required Inputs", font = "Helvetica 12 bold").grid(column=1, row=0, columnspan=10, sticky=tk.W)

# ROW 1
tk.Label(mainframe, text="Volume:").grid(column=1, row=1, sticky=tk.E)

volFileName_entry = tk.Entry(mainframe, width=100, textvariable=volFileName)
volFileName_entry.grid(column=2, columnspan=10, row=1, sticky=(tk.W, tk.E))

tk.Button(mainframe, text="Load File", command=(lambda: load_file(volFileName))).grid(column=12, row=1, sticky=tk.W)

# ROW 2
tk.Label(mainframe, text="Voxel Size:").grid(column=1, row=2, sticky=tk.E)

voxelSize_entry = tk.Entry(mainframe, width=5, textvariable=voxelSize)
voxelSize_entry.grid(column=2, row=2, sticky=tk.W)

tk.Label(mainframe, text="in Angstroms (A/voxel)").grid(column=3, row=2, sticky=tk.W)

# ROW 3
tk.Label(mainframe, text="Optional Inputs", font = "Helvetica 12 bold").grid(column=1, row=3, columnspan=8, sticky=tk.W)

# ROW 4
tk.Label(mainframe, text="Confidence Level:").grid(column=1, row=4, sticky=tk.E)

alphaValue_entry = tk.Entry(mainframe, width=5, textvariable=alphaValue)
alphaValue_entry.grid(column=2, row=4, sticky=tk.W)

tk.Label(mainframe, text="usually between (0, 0.05]").grid(column=3, row=4, sticky=tk.W)

# ROW 5
tk.Label(mainframe, text="Min Resolution:").grid(column=1, row=5, sticky=tk.E)

minRes_entry = tk.Entry(mainframe, width=5, textvariable=minRes)
minRes_entry.grid(column=2, row=5, sticky=tk.W)

tk.Label(mainframe, text="in Angstroms (default: 0; algorithm will start at just above 2.0 * voxelSize)").grid(column=3, row=5, sticky=tk.W)

# ROW 6
tk.Label(mainframe, text="Max Resolution:").grid(column=1, row=6, sticky=tk.E)

maxRes_entry = tk.Entry(mainframe, width=5, textvariable=maxRes)
maxRes_entry.grid(column=2, row=6, sticky=tk.W)

tk.Label(mainframe, text="in Angstroms (default: 0, algorithm will stop at Nyquist/4)").grid(column=3, row=6, sticky=tk.W)

# ROW 7
tk.Label(mainframe, text="Step Size:").grid(column=1, row=7, sticky=tk.E)

stepRes_entry = tk.Entry(mainframe, width=6, textvariable=stepRes)
stepRes_entry.grid(column=2, row=7, sticky=tk.W)

tk.Label(mainframe, text="in Angstroms (min: 0.5, default: 1.0, decrease if finer step size is desired)").grid(column=3, row=7, sticky=tk.W)

# ROW 8
tk.Label(mainframe, text="Mask Volume:").grid(column=1, row=8, sticky=tk.E)

maskFileName_entry = tk.Entry(mainframe, width=100, textvariable=maskFileName, fg="gray")
maskFileName_entry.grid(column=2, columnspan=10, row=8, sticky=(tk.W, tk.E))

tk.Button(mainframe, text="Load File", command=(lambda: load_file(maskFileName))).grid(column=12, row=8, sticky=tk.W)

# ROW 9
tk.Button(mainframe, text="Check Inputs and RUN", font = "Helvetica 12 bold", command=checkInputs).grid(column=9, columnspan=4, row=9, sticky=tk.W)

# Setup grid with padding
for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=10)
volFileName_entry.focus()

root.mainloop()