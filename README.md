# Slitherlink
Code slitherlink by python use satencoding. To run file slitherlink.py you must setting minisat. 
"
To install MiniSat on windows you will need cygwin.
Go to cygwin.com.
1. Follow the "install cygwin" link.
2. Download the file "setup.exe"
3. Put it in a place where you'll remember, because if you ever want to update cygwin, the same program will remember the current state and assist you in the update process.
4. Double click on "setup.exe", follow the instructions, the minimal installation will work.
5. The process will create a series of directories rooted at ../cygwin/... Most people place this the cygwin root on drive C, so C:/cygwin/... is the root.

Go to the MinSat page.
1. Get the precomplied binary for Cygwin/windows.
2. Move this to the bin directory of the cygwin root. For example the directory "C:/cygwin/bin/" .
3. Rename the file to "minisat.exe" in this directory.
4. Add "C:/cygwin/bin" to the windows path. Go to the control panel and search for "path". Then click on "edit environment variables for your account".

You can start up Minisat by
1. double clicking on "minisat.exe"
2. type "minisat" in a cygwin window
3. type the full path "c:\cygwin\bin\minisat.exe" in a windows command window.

I have seen other directions that tell you to place the binary in "cygwin/usr/local/bin/ " This works fine if you only want to call MiniSat from a cygwin window, but to call it from a windows command window, one needs the cygwin DLL's which are all in cygwin\bin\ . So placing the executable there makes it much easier since all the cygwin DLLs are in the same directory.
"(source http://web.cecs.pdx.edu/~hook/logicw11/Assignments/MinisatOnWindows.html)
