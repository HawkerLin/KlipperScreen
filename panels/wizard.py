import logging

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gtk, Pango

from ks_includes.screen_panel import ScreenPanel



class WizardPanel(ScreenPanel):
    def __init__(self, screen, title):
        super().__init__(screen, title)
        self.show_wizard_1()

    def show_wizard_1(self):
        image = self._gtk.Image("sovoler", self._gtk.content_width * .2, self._gtk.content_height * .5)
        self.logo = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.logo.set_size_request(120, 80)
        self.logo.pack_start(image, False, True, 8)
        self.logo.pack_end(image, True, True, 8)

        self.wizard_1_lbl = Gtk.Label()
        self.wizard_1_lbl.set_hexpand(True)#水平扩展填充
        self.wizard_1_lbl.set_halign(Gtk.Align.END)#水平对齐,CENTER设置为中心
        self.wizard_1_lbl.set_valign(Gtk.Align.START)
        self.wizard_1_lbl.set_ellipsize(Pango.EllipsizeMode.END)#文本末尾空间不够的话以省略号显示
        #self.wizard_1_lbl.set_label("Wizard")
        self.wizard_1_lbl.set_markup("<span font='DejaVu Sans-bold 38'>Your Languages</span>")
        self.wizard_1_title = Gtk.Box()
        self.wizard_1_title.get_style_context().add_class("title_bar")
        self.wizard_1_title.set_size_request(360, 80)
        self.wizard_1_title.set_valign(Gtk.Align.START)
        self.wizard_1_title.add(self.wizard_1_lbl)

        self.first_nex = self._gtk.Button("arrow-right","Next", f"color3")
        self.first_nex.connect("clicked", self.first_next)
        self.wizard_1_next = Gtk.Box()
        self.wizard_1_next.get_style_context().add_class('button_active')
        self.wizard_1_next.set_size_request(470, 80)
        self.wizard_1_next.add(self.first_nex)


        self.language_menu = Gtk.Label()
        self.language_menu.set_hexpand(True)
        self.language_menu.set_halign(Gtk.Align.CENTER)
        self.language_menu.set_valign(Gtk.Align.START)
        self.language = Gtk.Box()
        self.language.set_size_request(470, 600)
        self.language.add(self.language_menu)

        self.wizard_page_1 = Gtk.Grid()
        self.wizard_page_1.attach(self.logo, 0,0,1,1)
        self.wizard_page_1.attach(self.wizard_1_title, 1, 0, 1, 1)
        self.wizard_page_1.attach(self.language, 0, 1, 1, 1)
        self.wizard_page_1.attach(self.wizard_1_next, 0, 2, 1, 1)

    def show_wizard_2(self):
        self.wizard_2_lbl = Gtk.Label()
        self.wizard_2_lbl.set_hexpand(True)
        #self.wizard_2_lbl.set_halign(Gtk.Align.CENTER)
        self.wizard_1_lbl.set_valign(Gtk.Align.START)
        self.wizard_2_lbl.set_ellipsize(Pango.EllipsizeMode.END)
        self.wizard_2_lbl.set_label("Wizard")
        self.wizard_2_title = Gtk.Box()
        self.wizard_2_title.get_style_context().add_class("title_bar")
        self.wizard_2_title.set_size_request(240, 680)
        self.wizard_2_title.set_valign(Gtk.Align.CENTER)
        self.wizard_2_title.add(self.wizard_2_lbl)

        self.second_nex = self._gtk.Button(label="End")
        self.second_nex.connect("clicked", self.final_next)
        self.wizard_2_next = Gtk.Box()
        self.wizard_2_next.get_style_context().add_class('button_active')
        self.wizard_2_next.set_size_request(230, 80)
        self.wizard_2_next.add(self.second_nex)

        self.second_bac = self._gtk.Button(label="Back")
        self.second_bac.connect("clicked", self.second_back)
        self.wizard_2_back = Gtk.Box()
        self.wizard_2_back.get_style_context().add_class('button_active')
        self.wizard_2_back.set_size_request(230, 80)
        self.wizard_2_back.add(self.second_bac)

        self.wizard_page_2 = Gtk.Grid()
        self.wizard_page_2.attach(self.wizard_2_title, 0, 0, 1, 1)
        self.wizard_page_2.attach(self.wizard_2_back, 0, 1, 1, 1)
        self.wizard_page_2.attach(self.wizard_2_next, 1, 1, 1, 1)
        self._screen.add(self._screen.wizard.wizard_page_2)
        self._screen.show_all()

    def first_next(self, widget):
        self._screen.remove(self.wizard_page_1)
        self.show_wizard_2()

    def second_back(self,widget):
        self._screen.remove(self.wizard_page_2)
        self.show_wizard_1()
        self._screen.add(self._screen.wizard.wizard_page_1)
        self._screen.show_all()
        

    # def second_next(self, widget):
    #     self._screen.remove()

    def final_next(self, widget):
        #self._screen.remove(self.wizard_page)#如果只是remove这个而没有再次add、show_all则是黑屏
        self._screen.remove(self.wizard_page_2)
        self._screen.add(self._screen.base_panel.main_grid)
        self._screen.show_all()

