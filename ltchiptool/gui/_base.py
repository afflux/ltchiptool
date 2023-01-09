#  Copyright (c) Kuba Szczodrzyński 2023-1-3.

from typing import Callable, List, Type

import wx
import wx.xrc

from .work.base import BaseThread


# noinspection PyPep8Naming
class BasePanel(wx.Panel):
    _components: List[wx.Window]
    _threads: List[BaseThread]

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self._components = []
        self._threads = []

    def update(self, target: wx.Window = None):
        pass

    def _update(self, event: wx.Event):
        self.update(event.EventObject)

    def start_work(self, thread: BaseThread):
        self._threads.append(thread)
        thread.on_stop = lambda t: self.on_work_stopped(t)
        thread.start()

    def stop_work(self, cls: Type[BaseThread]):
        for t in list(self._threads):
            if isinstance(t, cls):
                t.stop()

    def on_work_stopped(self, t: BaseThread):
        self._threads.remove(t)

    def LoadXRC(self, res: wx.xrc.XmlResource, name: str):
        panel = res.LoadPanel(self, name)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)

    def BindByName(self, event: int, name: str, handler: Callable[[wx.Event], None]):
        self.FindWindowByName(name).Bind(event, handler)

    def BindComboBox(self, name: str):
        window: wx.ComboBox = self.FindWindowByName(name)
        self._components.append(window)
        window.Bind(wx.EVT_COMBOBOX, self._update)
        return window

    def BindRadioButton(self, name: str):
        window: wx.RadioButton = self.FindWindowByName(name)
        self._components.append(window)
        window.Bind(wx.EVT_RADIOBUTTON, self._update)
        return window

    def BindCheckBox(self, name: str):
        window: wx.CheckBox = self.FindWindowByName(name)
        self._components.append(window)
        window.Bind(wx.EVT_CHECKBOX, self._update)
        return window

    def BindTextCtrl(self, name: str):
        window: wx.TextCtrl = self.FindWindowByName(name)
        self._components.append(window)
        window.Bind(wx.EVT_TEXT, self._update)
        return window

    def BindButton(self, name: str, func: Callable[[wx.Event], None]):
        window: wx.Button = self.FindWindowByName(name)
        self._components.append(window)
        window.Bind(wx.EVT_BUTTON, func)
        return window

    def FindStaticText(self, name: str):
        window: wx.StaticText = self.FindWindowByName(name)
        return window

    def EnableAll(self):
        for window in self._components:
            window.Enable()
        self.update()

    def DisableAll(self):
        for window in self._components:
            window.Disable()
