1. latter is relative import... [i could not fully understand which matters when] 
2. direct file execution tells python to forget the folder structure and just execute __main__.py file but -m stand for module which tells it about the package architecture 
3. treats folder as a package... yes it can be 
4. it stands for enclosing... EX... x is enclosing here 
	def f1():
		x = 2
			def f2():
				y=3
5. args was a local variable to main() it can only survive inside it. If we pass it to a different function(build_paerser()) it would not recognize it. LEGB... L is local meaning defined inside a function... E means that the variable is outside of a defined function but enclosed in an outer function... G is a variable defined at the top of a python script outside of all function... B are the built in functions.
6. it is just an optional path variable. other modules take notes_file as variable and are not globally dependent on NOTES_FILE.
 if NOTES_FILE were still read globally inside cmd_add... then main() would have to specially have to pass args.file for it to be read... (here ig it is prevented by the use of variable "notes_file")[PLEASE TELL WHAT IS THE PRECISE EXPLANATION]
7. sys.path contains the directory from which you ran the script , venv's site packages and the standard library. python looks at the current directory... first it would look forcli it would see week1 and ingnore it... now terminal directly opens from cli and finds cli sitting there.      
			
  