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
        image = self._gtk.Image("sovoler", self._gtk.content_width * .1, self._gtk.content_height * .1)
        self.logo = Gtk.Box()
        #self.logo.set_halign(Gtk.Align.END)
        #self.logo.set_valign(Gtk.Align.END)
        self.logo.set_size_request(80, 80)
        #self.logo.pack_start(image, False, True, 8)#将image添加到self.logo的起始位置
        self.logo.pack_end(image, True, False, 10)#将image添加到self.logo的末尾位置

        self.wizard_1_lbl = Gtk.Label()
        self.wizard_1_lbl.set_hexpand(True)#水平扩展填充
        #self.wizard_1_lbl.set_halign(Gtk.Align.END)#水平对齐,CENTER设置为中心
        #self.wizard_1_lbl.set_valign(Gtk.Align.START)
        self.wizard_1_lbl.set_ellipsize(Pango.EllipsizeMode.END)#文本末尾空间不够的话以省略号显示
        #self.wizard_1_lbl.set_label("Wizard")
        self.wizard_1_lbl.set_markup("<span font='DejaVu Sans-bold 30'>Your Languages</span>")
        self.wizard_1_title = Gtk.Box()
        #self.wizard_1_title.get_style_context().add_class("title_bar")
        self.wizard_1_title.set_size_request(240, 80)
        #self.wizard_1_title.set_valign(Gtk.Align.START)
        self.wizard_1_title.add(self.wizard_1_lbl)

        self.first_nex = self._gtk.Button("arrow-right","Next", f"color3")
        self.first_nex.connect("clicked", self.first_next)
        self.first_nex.set_size_request(440, 40)
        self.first_nex.set_halign(Gtk.Align.CENTER)
        self.first_nex.set_valign(Gtk.Align.CENTER)
        self.wizard_1_next = Gtk.Box()
        self.wizard_1_next.pack_start(self.first_nex, False, False, 15)
        #self.wizard_1_next.set_halign(Gtk.Align.CENTER)
        #self.wizard_1_next.set_valign(Gtk.Align.CENTER)
        #self.wizard_1_next.get_style_context().add_class('button_active')
        self.wizard_1_next.set_size_request(480, 80)
        self.wizard_1_next.add(self.first_nex)


        self.language_menu = Gtk.Label()
        self.language_menu.set_markup("<span font='DejaVu Sans-bold 28'>ENGLISH</span>")
        #self.language_menu.set_hexpand(True)
        self.language_menu.set_size_request(240, 40)
        self.language_menu.set_halign(Gtk.Align.CENTER)
        self.language_menu.set_valign(Gtk.Align.START)
        self.language = Gtk.Box()
        self.language.set_halign(Gtk.Align.CENTER)
        self.language.pack_start(self.language_menu, False, False, 20)
        self.language.set_size_request(480, 600)
        self.language.add(self.language_menu)

        self.wizard_page_1 = Gtk.Grid()
        self.wizard_page_1.attach(self.logo, 0,0,1,1)
        self.wizard_page_1.attach(self.wizard_1_title, 1, 0, 1, 1)
        self.wizard_page_1.attach(self.language, 0, 1, 2, 1)
        self.wizard_page_1.attach(self.wizard_1_next, 0, 2, 2, 1)
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.add_named(self.wizard_page_1, "page-1")
        self.stack.set_visible_child_name("page-1")

    def show_wizard_2(self):
        self.wizard_2_lbl = Gtk.Label()
        self.wizard_2_lbl.set_hexpand(True)
        self.wizard_2_lbl.set_halign(Gtk.Align.CENTER)
        self.wizard_2_lbl.set_valign(Gtk.Align.CENTER)
        #self.wizard_2_lbl.set_ellipsize(Pango.EllipsizeMode.END)
        #self.wizard_2_lbl.set_label("Wizard")
        self.wizard_2_lbl.set_markup("<span font='DejaVu Sans-bold 30'>Connect Network</span>")
        self.wizard_2_title = Gtk.Box()
        #self.wizard_2_title.get_style_context().add_class("title_bar")
        self.wizard_2_title.set_size_request(480, 80)
        self.wizard_2_title.set_valign(Gtk.Align.START)
        self.wizard_2_title.add(self.wizard_2_lbl)

        image = self._gtk.Image("wifi", self._gtk.content_width * .5, self._gtk.content_height * .5)
        self.wifi_logo = Gtk.Box()
        #self.wifi_logo.set_halign(Gtk.Align.CENTER)
        #self.wifi_logo.set_valign(Gtk.Align.CENTER)
        self.wifi_logo.set_size_request(480, 640)
        self.wifi_logo.pack_end(image, True, True, 20)#将image添加到self.logo的起始位置
        #self.logo.pack_end(image, False, False, 10)#将image添加到self.logo的末尾位置

        self.second_nex = self._gtk.Button("arrow-right","Next", f"color2")
        self.second_nex.connect("clicked", self.second_next)
        self.second_nex.set_size_request(210, 35)
        self.second_nex.set_halign(Gtk.Align.CENTER)
        self.second_nex.set_valign(Gtk.Align.CENTER)
        self.wizard_2_next = Gtk.Box()
        self.wizard_2_next.pack_start(self.second_nex, False, False, 10)
        #self.wizard_2_next.get_style_context().add_class('button_active')
        self.wizard_2_next.set_size_request(240, 80)
        self.wizard_2_next.add(self.second_nex)

        self.second_bac = self._gtk.Button("arrow-left","Back", f"color1")
        self.second_bac.connect("clicked", self.second_back)
        self.second_bac.set_size_request(210, 35)
        self.second_bac.set_halign(Gtk.Align.CENTER)
        self.second_bac.set_valign(Gtk.Align.CENTER)
        self.wizard_2_back = Gtk.Box()
        self.wizard_2_back.pack_start(self.second_bac, False, False, 10)
        #self.wizard_2_back.get_style_context().add_class('button_active')
        self.wizard_2_back.set_size_request(240, 80)
        self.wizard_2_back.add(self.second_bac)

        self.wizard_page_2 = Gtk.Grid()
        self.wizard_page_2.attach(self.wizard_2_title, 0, 0, 2, 1)
        self.wizard_page_2.attach(self.wifi_logo, 0, 1, 2, 1)
        self.wizard_page_2.attach(self.wizard_2_back, 0, 3, 1, 1)
        self.wizard_page_2.attach(self.wizard_2_next, 1, 3, 1, 1)
        self._screen.add(self._screen.wizard.wizard_page_2)
        self._screen.show_all()

    def show_wizard_3(self):
        self.wizard_3_lbl = Gtk.Label()
        self.wizard_3_lbl.set_hexpand(True)
        self.wizard_3_lbl.set_halign(Gtk.Align.CENTER)
        self.wizard_3_lbl.set_valign(Gtk.Align.CENTER)
        #self.wizard_3_lbl.set_ellipsize(Pango.EllipsizeMode.END)
        #self.wizard_3_lbl.set_label("Wizard")
        self.wizard_3_lbl.set_markup("<span font='DejaVu Sans-bold 30'>Leveling Calibration</span>")
        self.wizard_3_title = Gtk.Box()
        #self.wizard_3_title.get_style_context().add_class("title_bar")
        self.wizard_3_title.set_size_request(480, 80)
        self.wizard_3_title.set_valign(Gtk.Align.START)
        self.wizard_3_title.add(self.wizard_3_lbl)

        image = self._gtk.Image("level", self._gtk.content_width * .3, self._gtk.content_height * .3)
        self.level_logo = Gtk.Box()
        #self.level_logo.set_halign(Gtk.Align.CENTER)
        #self.level_logo.set_valign(Gtk.Align.CENTER)
        self.level_logo.set_size_request(480, 640)
        self.level_logo.pack_end(image, True, True, 20)#将image添加到self.logo的起始位置
        #self.logo.pack_end(image, False, False, 10)#将image添加到self.logo的末尾位置

        self.third_nex = self._gtk.Button("","Finish", f"color1")
        self.third_nex.connect("clicked", self.final_next)
        self.third_nex.set_size_request(210, 35)
        self.third_nex.set_halign(Gtk.Align.CENTER)
        self.third_nex.set_valign(Gtk.Align.CENTER)
        self.wizard_3_next = Gtk.Box()
        self.wizard_3_next.pack_start(self.third_nex, False, False, 10)
        #self.wizard_3_next.get_style_context().add_class('button_active')
        self.wizard_3_next.set_size_request(240, 80)
        self.wizard_3_next.add(self.third_nex)

        self.third_bac = self._gtk.Button("arrow-left","Back", f"color4")
        self.third_bac.connect("clicked", self.third_back)
        self.third_bac.set_size_request(210, 35)
        self.third_bac.set_halign(Gtk.Align.CENTER)
        self.third_bac.set_valign(Gtk.Align.CENTER)
        self.wizard_3_back = Gtk.Box()
        self.wizard_3_back.pack_start(self.third_bac, False, False, 10)
        #self.wizard_3_back.get_style_context().add_class('button_active')
        self.wizard_3_back.set_size_request(240, 80)
        self.wizard_3_back.add(self.third_bac)

        self.wizard_page_3 = Gtk.Grid()
        self.wizard_page_3.attach(self.wizard_3_title, 0, 0, 2, 1)
        self.wizard_page_3.attach(self.level_logo, 0, 1, 2, 1)
        self.wizard_page_3.attach(self.wizard_3_back, 0, 3, 1, 1)
        self.wizard_page_3.attach(self.wizard_3_next, 1, 3, 1, 1)
        self._screen.add(self._screen.wizard.wizard_page_3)
        self._screen.show_all()

    def first_next(self, widget):
        self._screen.remove(self.wizard_page_1)
        self.show_wizard_2()

    def second_back(self,widget):
        self._screen.remove(self.wizard_page_2)
        self.show_wizard_1()
        self._screen.add(self._screen.wizard.wizard_page_1)
        self._screen.show_all()

    def second_next(self,widget):
        self._screen.remove(self.wizard_page_2)
        self.show_wizard_3()

    def third_back(self,widget):
        self._screen.remove(self.wizard_page_3)
        self.show_wizard_2()
        

    # def second_next(self, widget):
    #     self._screen.remove()

    def final_next(self, widget):
        #self._screen.remove(self.wizard_page)#如果只是remove这个而没有再次add、show_all则是黑屏
        self._screen.remove(self.wizard_page_3)
        self._screen.add(self._screen.base_panel.main_grid)
        self._screen.show_all()

