import logging

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gtk, Pango

from ks_includes.screen_panel import ScreenPanel
# from base_panel import BasePanel


class WizardPanel(ScreenPanel):
    def __init__(self, screen, title):
        super().__init__(screen, title)

        self.wizardlbl = Gtk.Label()
        self.wizardlbl.set_hexpand(True)
        self.wizardlbl.set_halign(Gtk.Align.CENTER)
        self.wizardlbl.set_ellipsize(Pango.EllipsizeMode.END)
        self.wizardlbl.set_label("Wizard")
        self.wizardtitle = Gtk.Box()
        self.wizardtitle.get_style_context().add_class("wizardtitle")
        self.wizardtitle.set_size_request(100, 200)
        self.wizardtitle.set_valign(Gtk.Align.CENTER)
        self.wizardtitle.add(self.wizardlbl)

        self.button = self._gtk.Button(label="Next")
        self.button.connect("clicked", self.on_button_clicked)
        self.wizard_click = Gtk.Box()
        self.wizard_click.get_style_context().add_class('wizard')
        self.wizard_click.set_size_request(100, 200)
        self.wizard_click.add(self.button)
        #self.wizard_click.pack_end(self.button, False, False, 0)

        self.wizard_page = Gtk.Grid()
        self.wizard_page.attach(self.wizardtitle, 0, 0, 1, 1)
        self.wizard_page.attach(self.wizard_click, 0, 1, 1, 1)

    def on_button_clicked(self, widget):
        # self.base_panel = BasePanel(self, title="Base Panel")
        self._screen.hide(self.wizard_page)
        self._screen.get_toplevel().base_panel.show_all()
        # self._screen.base_panel.activate()

