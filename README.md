# Xorg-clipboard-xdnd
Some scripts around Xorg protocols.

- xclip-get.py returns the file names after a copy/cut operation has been performed on them, e.g. from a file manager, through the atom 'x-special/gnome-copied-files' and the clipboard.

![My image](https://github.com/frank038/Xorg-clipboard-xdnd/blob/main/xclip-get-screenshot.png)


- xdnd-drop.py is the implementation in python of the xdnd protocol, for files dragged from a file manager, as explained in freedesktop specifications. The atom 'x-special/gnome-copied-files' is used. Execute the program and drop a file (or some files) onto it; read the terminal for the data returned. Press any key from the keyboard to close the window.

![My image](https://github.com/frank038/Xorg-clipboard-xdnd/blob/main/xdnd-drop-screenshot.png)
