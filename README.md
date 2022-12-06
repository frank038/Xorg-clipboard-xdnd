# Xorg-clipboard-xdnd
Some script around Xorg protocols.

xclip-get.py return the files after a copy/cut operation has been performed on them, e.g. from a file manager, through the atom 'x-special/gnome-copied-files' and the clipboard.

![My image](https://github.com/frank038/Xorg-clipboard-xdnd/blob/main/xclip-get-screenshot.png)


xdnd-drop.py is the implementation in python of the xdnd protocol, for files dragged from a file manager, as explained in freedesktop specifications. Execute the program and drop a file over it; read the terminal for data got.

![My image](https://github.com/frank038/Xorg-clipboard-xdnd/blob/main/xdnd-drop-screenshot.png)
