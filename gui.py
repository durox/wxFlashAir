#!/usr/bin/env python
# encoding: utf-8

import wx
import sys
from pyflashair import pyflashair
import pickle
import os.path


class Main(object):

    def __init__(self):
        """start main routine """
        self.app = wx.App()

        self.currentpath = "/"
        self.prevpath = "/"
        self.synclocal = ""
        self.syncremote = ""

        path = os.path.dirname(sys.argv[0]) + os.path.sep + "save.dat"
        if os.path.exists(path):
            obj = pickle.load(open(path, "rb"))
            self.synclocal = obj[0]
            self.syncremote = obj[1]
            self.currentpath = obj[2]
            self.prevpath = obj[3]

        self.createWidgets()
        self.verbinden()
        self.move(self.currentpath)

        self.app.MainLoop()

        obj = (self.synclocal, self.syncremote, self.currentpath, self.prevpath)
        pickle.dump(obj, open(path, "wb"))

    def createWidgets(self):
        """@todo: Docstring for createWidgets.
        Returns: @todo

        """
        self.frame = MainFrame(None)

        self.frame.Bind(wx.EVT_MENU, self.OnVerbinden, id=101)
        self.frame.Bind(wx.EVT_MENU, self.OnAktualisieren, id=102)
        self.frame.Bind(wx.EVT_BUTTON, self.OnChoose, id=201)
        self.frame.Bind(wx.EVT_BUTTON, self.OnUbernehmen, id=202)
        self.frame.Bind(wx.EVT_BUTTON, self.OnSync, id=203)
        self.frame.lcFiles.Bind(wx.EVT_LEFT_DCLICK, self.OnDClick)
        self.frame.txtLocalPath.SetValue(self.synclocal)
        self.frame.txtRemotePath.SetValue(self.syncremote)
        self.frame.Show()

    def verbinden(self, ip="192.168.0.1"):
        """verbinden
        Returns: @todo

        """
        self.fa = pyflashair.FlashAir(ip)

    def move(self, path):
        """move to folder

        Args:
            path (@todo): @todo

        Returns: @todo

        """
        self.prevpath = self.currentpath
        self.currentpath = path
        self.filelist = self.fa.GetFileList(self.currentpath)
        self.frame.setFilelist(self.filelist)

    def synchronisieren(self, arg1):
        """@todo: Docstring for synchronisieren.

        Args:
            arg1 (@todo): @todo

        Returns: @todo

        """
        pass

    def OnAktualisieren(self, event):
        """Dateiliste aktualisieren

        Args:
            event (@todo): Event

        Returns: True

        """
        self.move(self.currentpath)

    def OnVerbinden(self, event):
        dlg = wx.TextEntryDialog(self.frame, "IP-Adresse:", "Mit FlashAir Karte verbinden...", "192.168.0.1")
        if dlg.ShowModal():
            ip = dlg.GetValue()
            self.verbinden(ip)

    def OnDClick(self, event):
        """double click on list element

        Args:
            event (@todo): @todo

        Returns: @todo

        """
        index = self.frame.lcFiles.GetFirstSelected()
        if index == 0:
            path = self.prevpath
            self.move(path)
        else:
            selected = self.filelist[index - 1]
            if selected.size == 0:
                path = self.currentpath + "/" + selected.name
                self.move(path)

    def OnChoose(self, event):
        """@todo: Docstring for OnSyncSetuo.

        Args:
            event (@todo): @todo

        Returns: @todo

        """
        dlg = wx.DirDialog(self.frame, "Verzeichnis auswählen...")
        if dlg.ShowModal() == wx.ID_OK:
            self.synclocal = dlg.GetPath()
            self.frame.txtLocalPath.SetValue(self.synclocal)

    def OnUbernehmen(self, event):
        """@todo: Docstring for OnUbernehmen.

        Args:
            event (@todo): @todo

        Returns: @todo

        """
        self.syncremote = self.currentpath
        self.frame.txtRemotePath.SetValue(self.syncremote)

    def OnSync(self, event):
        """@todo: Docstring for OnSync.

        Args:
            event (@todo): @todo

        Returns: @todo

        """
        self.fa.Sync(self.syncremote, self.synclocal)


class MainFrame(wx.Frame):

    """Main window subclass"""

    def __init__(self, parent):
        """@todo: to be defined1.

        Args:
            parent (@todo): @todo


        """
        wx.Frame.__init__(self, parent)
        self.createWidgets()

    def createWidgets(self):
        """create widgets
        Returns: @todo

        """
        mb = wx.MenuBar()
        datei = wx.Menu()
        datei.Append(101, "Verbinden...")
        datei.Append(102, "Aktualisieren")
        mb.Append(datei, "Datei")
        self.SetMenuBar(mb)

        self.lcFiles = wx.ListCtrl(self, style=wx.LC_REPORT)
        self.lcFiles.InsertColumn(0, "Name")
        self.lcFiles.InsertColumn(1, "Verzeichnis")
        self.lcFiles.InsertColumn(2, "Groesse")
        self.lcFiles.InsertColumn(3, "Datum")

        box = wx.StaticBox(self, -1, "Synchronisieren")
        self.txtLocalPath = wx.TextCtrl(box)
        self.txtRemotePath = wx.TextCtrl(box)
        self.btnChoose = wx.Button(box, label="...", id=201)
        self.btnSet = wx.Button(box, label="Uebernehmen", id=202)
        self.btnSync = wx.Button(box, label="Synchronisieren", id=203)

        flag = wx.EXPAND
        s = wx.GridBagSizer()
        s.Add(wx.StaticText(box, -1, "Lokal:"), (0, 0))
        s.Add(self.txtLocalPath, (0, 1), flag=flag)
        s.Add(self.btnChoose, (0, 2), flag=flag)
        s.Add(wx.StaticText(box, -1, "Remote:"), (1, 0))
        s.Add(self.txtRemotePath, (1, 1), flag=flag)
        s.Add(self.btnSet, (1, 2), flag=flag)
        s.Add(self.btnSync, (2, 0), span=(1, 3), flag=flag)
        s.AddGrowableCol(1)
        box.SetSizer(s)


        flag = wx.EXPAND
        gbs = wx.GridBagSizer()
        gbs.Add(self.lcFiles, (0, 0), flag=flag)
        gbs.Add(box, (1, 0), flag=flag)
        gbs.AddGrowableCol(0)
        gbs.AddGrowableRow(0)
        gbs.AddGrowableRow(1)
        self.SetSizer(gbs)

    def setFilelist(self, files):
        """set files

        Args:
            files (@todo): @todo

        Returns: @todo

        """
        self.lcFiles.DeleteAllItems()
        self.lcFiles.Append(("..", "", ""))
        for f in files:
            self.lcFiles.Append((f.name, f.dir, f.size, f.datetime))


class RedirectObj(object):
    def __init__(self, tc):
        self.out = tc

    def write(self, s):
        self.out.WriteText(s)


if __name__ == '__main__':
    Main()
