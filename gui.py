import wx
import sys
from pyflashair import pyflashair


class Main(object):

    def __init__(self):
        """start main routine """
        self.app = wx.App()
        self.createWidgets()
        self.app.MainLoop()

    def createWidgets(self):
        """@todo: Docstring for createWidgets.
        Returns: @todo

        """
        self.frame = MainFrame(None)

        self.frame.Bind(wx.EVT_MENU, self.OnVerbinden, id=101)
        self.frame.Show()

    def verbinden(self, ip="192.168.0.1"):
        """verbinden
        Returns: @todo

        """

        self.fa = pyflashair.FlashAir(ip)

    def OnAktualisieren(self, event):
        """Dateiliste aktualisieren

        Args:
            event (@todo): Event

        Returns: True

        """
        self.filelist = self.fa.GetFileList("/")
        self.lcFiles.DeleteAllItems()
        for f in self.filelist:
            self.frame.lcFiles.Append((f.name, f.dir, f.datetime))

    def OnVerbinden(self, event):
        dlg = wx.TextEntryDialog(self.frame, "IP-Adresse:", "Mit FlashAir Karte verbinden...", "192.168.0.1")
        if dlg.ShowModal():
            ip = dlg.GetValue()
            self.verbinden(ip)


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
        self.lcFiles.InsertColumn(2, "Datum")

        flag = wx.EXPAND
        gbs = wx.GridBagSizer()
        gbs.Add(self.lcFiles, (0, 0), flag=flag)
        gbs.AddGrowableCol(0)
        gbs.AddGrowableRow(0)
        self.SetSizer(gbs)


class RedirectObj(object):
    def __init__(self, tc):
        self.out = tc

    def write(self, s):
        self.out.WriteText(s)


if __name__ == '__main__':
    Main()
