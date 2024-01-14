#!/usr/bin/env python3

from Xlib import X, display, Xatom, Xutil, protocol
import pathlib

sel_atom = display.Display().get_atom("CLIPBOARD")
target_atom = display.Display().get_atom('x-special/gnome-copied-files')
data_atom = display.Display().get_atom('SEL_DATA')


class Window:
    def __init__(self, display, msg):
        self.display = display
        self.msg = msg
        
        self.screen = self.display.screen()
        
        mask = (X.PropertyChangeMask | X.PointerMotionMask | X.ExposureMask 
        | X.KeyPressMask | X.SubstructureNotifyMask | X.ButtonPressMask
        | X.SubstructureRedirectMask)
        
        self.window = self.screen.root.create_window(
            10, 10, 300, 300, 1,
            self.screen.root_depth,
            background_pixel=self.screen.white_pixel,
            event_mask=mask,
            )
        self.gc = self.window.create_gc(
            foreground = self.screen.black_pixel,
            background = self.screen.white_pixel,
            )
        ###############
        # step 0: Windows announce that they support the XDND protocol by creating a window property XdndAware.
        xdnd = self.display.get_atom('XdndAware')
        # 
        self.d = self.display
        self.WM_DELETE_WINDOW = self.d.intern_atom('WM_DELETE_WINDOW')
        self.WM_PROTOCOLS = self.d.intern_atom('WM_PROTOCOLS')

        self.window.set_wm_name('Xlib example: xdnd-drop.py')
        self.window.set_wm_icon_name('xdnd-drop.py')
        self.window.set_wm_class('xdnd-drop', 'XlibExample')

        self.window.set_wm_protocols([self.WM_DELETE_WINDOW])
        self.window.set_wm_hints(
            flags=Xutil.StateHint,
            initial_state=Xutil.NormalState
            )
            
        #############
        self.window.map()
        
        self.window.change_property(
            xdnd,
            Xatom.ATOM,
            32,
            [5],
            X.PropModeReplace,
        )
        self.display.sync()
        # XdndEnter
        self.xdndenter = self.display.get_atom('XdndEnter')
        # text/uri-list
        self.ulist = self.display.get_atom('text/uri-list')
        #
        self.sel_atom = self.display.get_atom("CLIPBOARD")
        self.target_atom = self.display.get_atom('x-special/gnome-copied-files')
        self.data_atom = self.display.get_atom('SEL_DATA')
        #
        # XdndStatus
        self.dndstatus = self.display.get_atom('XdndStatus')
        # directsave
        self.xds = self.display.get_atom('XdndDirectSave0')
        # XdndActionDirectSave
        self.xds2 = self.display.get_atom('XdndActionDirectSave')
        # window source
        self.win_source = None
        # drop operation
        self.drop_op = None
        
    def loop(self):
        while True:
            e = self.display.next_event()
                
            if e.type == X.Expose:
                self.window.fill_rectangle(self.gc, 20, 20, 10, 10)
                self.window.draw_text(self.gc, 10, 50, self.msg)
            elif e.type == X.KeyPress:
                raise SystemExit
            #
            elif e.type == X.PropertyNotify:
                pass
            elif e.type == X.ConfigureRequest:
                pass
            #
            elif e.type == X.ClientMessage:
                # step 1 and 2
                # step 3 and 4
                if e.client_type == self.display.get_atom('XdndEnter'):
                    fmt, data = e.data
                    self.win_source = data[0]
                #
                if e.client_type == self.display.get_atom('XdndPosition'):
                    fmt, data_tmp = e.data
                    data = data_tmp.tolist()
                    #
                    if data[4] in [self.display.get_atom('XdndActionCopy'), self.display.get_atom('XdndActionMove'), self.display.get_atom('XdndActionLink')]:
                        self.drop_op = data[4]
                    else:
                        self.drop_op = None
                    #
                    # step 5
                    geom = self.window.get_geometry()
                    ewindow = self.display.create_resource_object('window', self.win_source)
                    
                    _can_drop = 0
                    if self.drop_op:
                        _can_drop = 1
                    # rectangle?
                    data = (32, [self.window.id, _can_drop, 0, 0, self.drop_op])
                    sevent = protocol.event.ClientMessage(
                    window = ewindow,
                    client_type = self.dndstatus,
                    data = data
                    )
                    #
                    ewindow.send_event(sevent)
                #
                # step 7
                if e.client_type == self.display.get_atom('XdndLeave'):
                    # reset everything
                    self.drop_op = None
                    self.win_source = None
                #
                # step 8
                if e.client_type == self.display.get_atom('XdndDrop'):
                    #
                    fmt, data_tmp = e.data
                    data = data_tmp.tolist()
                    ######## xds
                    ewindowx = self.display.create_resource_object('window', data[0])
                    propx = ewindowx.get_full_property(self.xds, X.AnyPropertyType, sizehint = 10000)
                    # 
                    if propx:
                        data_url_to_send2 = pathlib.Path("/tmp/{}".format(propx.value.decode())).as_uri()
                        data_url_to_send = data_url_to_send2.encode()
                        #
                        ewindowx.change_property(
                            self.xds,
                            propx.property_type,
                            8,
                            data_url_to_send,
                            X.PropModeReplace,
                        )
                        #
                        dndsel = self.display.get_atom('XdndSelection')
                        self.window.convert_selection(dndsel, self.xds, self.data_atom, X.CurrentTime)
                        continue
                    ##########
                    dndsel = self.display.get_atom('XdndSelection')
                    self.window.convert_selection(dndsel, self.ulist, self.data_atom, X.CurrentTime)
                    
            #
            elif e.type == X.SelectionNotify:
                prop = self.window.get_full_property(self.data_atom, X.AnyPropertyType, sizehint = 10000)
                #
                if not prop:
                    continue
                #
                if prop.property_type == self.display.get_atom('text/uri-list'):
                    data = prop.value
                    # the data
                    print("DATA GOT:", data)
                # xds
                elif prop.property_type == self.xds:
                    print("XSD data:", prop.value)
                #
                # step 8 -> send XdndFinished
                ewindow = self.display.create_resource_object('window', self.win_source)
                # to verify
                data = (32, [self.window.id, 1, self.drop_op, 0,0])
                sevent = protocol.event.ClientMessage(
                window = ewindow,
                client_type = self.display.get_atom('XdndFinished'),
                data = data
                )
                #
                ewindow.send_event(sevent)
                
            #
            elif e.type == X.ButtonPress:
                pass
                

                
if __name__ == "__main__":
    Window(display.Display(), "Hello, World!").loop()
    
