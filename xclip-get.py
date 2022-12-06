#!/usr/bin/env python3

import sys
from Xlib import X, display as Xdisplay

display = Xdisplay.Display()
window = display.screen().root.create_window(0,0, 1,1, 0, X.CopyFromParent)

window.change_attributes(event_mask = X.PropertyChangeMask)

sel_atom = display.get_atom("CLIPBOARD")
target_atom = display.get_atom('x-special/gnome-copied-files')
data_atom = display.get_atom('SEL_DATA')

def _on_error(data):
    print("ERROR:", data)

window.convert_selection(sel_atom, target_atom, data_atom, X.CurrentTime, onerror=_on_error)


while True:
    ev = display.next_event()
    
    if ev.type == X.SelectionNotify:
        break
    
if ev.property == X.NONE:
    pass

else:
    sel_atom = display.get_atom("CLIPBOARD")
    target_atom = display.get_atom('x-special/gnome-copied-files')
    data_atom = display.get_atom('SEL_DATA')
    data_got = window.get_full_property(data_atom, X.AnyPropertyType, sizehint = 10000)
    print("DATA:", data_got)
    
    sys.exit()
