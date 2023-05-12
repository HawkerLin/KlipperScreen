import logging
import os
import gi
import netifaces

gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gtk, Pango
from signal import SIGTERM

from ks_includes.screen_panel import ScreenPanel
from ks_includes.widgets.keyboard import Keyboard



class WizardPanel(ScreenPanel):
    initialized = False
    keyboard = None
    def __init__(self, screen, title):
        super().__init__(screen, title)
        self.show_wizard_1()

    def ini_language_dic(self):
        options = self._config.get_configurable_options().copy()
        for option in options:
            if list(option)[0] == "language":
                languages = option['language']
        return languages

    def show_wizard_1(self):
        self.blank = Gtk.Box()
        self.blank.set_size_request(480, 60)

        image = self._gtk.Image("sovoler", self._gtk.content_width * .1, self._gtk.content_height * .1)
        self.logo = Gtk.Box()
        #self.logo.set_halign(Gtk.Align.END)
        #self.logo.set_valign(Gtk.Align.END)
        self.logo.set_size_request(80, 80)
        #self.logo.pack_start(image, False, True, 8)#将image添加到self.logo的起始位置
        self.logo.pack_end(image, True, False, 0)#将image添加到self.logo的末尾位置

        self.wizard_1_lbl = Gtk.Label()
        self.wizard_1_lbl.set_hexpand(True)#水平扩展填充
        #self.wizard_1_lbl.set_halign(Gtk.Align.END)#水平对齐,CENTER设置为中心
        #self.wizard_1_lbl.set_valign(Gtk.Align.START)
        self.wizard_1_lbl.set_ellipsize(Pango.EllipsizeMode.END)#文本末尾空间不够的话以省略号显示
        title = _("Your languages")
        self.wizard_1_lbl.set_markup("<span font='DejaVu Sans-bold 33'>{}</span>".format(title))
        self.wizard_1_title = Gtk.Box()
        self.wizard_1_title.set_size_request(240, 80)
        self.wizard_1_title.set_halign(Gtk.Align.START)
        self.wizard_1_title.pack_start(self.wizard_1_lbl, False, False, 30)

        self.first_nex = self._gtk.Button("arrow-right",_("Next"), f"color3")
        self.first_nex.connect("clicked", self.first_next)
        self.first_nex.set_size_request(440, 110)
        self.first_nex.set_halign(Gtk.Align.CENTER)
        self.first_nex.set_valign(Gtk.Align.CENTER)
        self.wizard_1_next = Gtk.Box()
        self.wizard_1_next.pack_start(self.first_nex, False, False, 15)
        #self.wizard_1_next.set_halign(Gtk.Align.CENTER)
        #self.wizard_1_next.set_valign(Gtk.Align.CENTER)
        #self.wizard_1_next.get_style_context().add_class('button_active')
        self.wizard_1_next.set_size_request(480, 110)
        self.wizard_1_next.add(self.first_nex)



        languages = self.ini_language_dic()
        self.language_menu = Gtk.ComboBoxText()
        #self.language_menu.set_markup("<span font='DejaVu Sans-bold 28'>ENGLISH</span>")
        #self.language_menu.set_hexpand(True)
        for key,value in enumerate(languages['options']):
            self.language_menu.append(value['value'], value['name'])
            if value['value'] == self._config.get_config()[languages['section']].get('language', languages['value']):
                self.language_menu.set_active(key)
        self.language_menu.connect("changed", self.on_dropdown_change, languages['section'], 'language', languages['callback'])
        self.language_menu.set_entry_text_column(0)
        self.language_menu.set_size_request(440, 80)
        self.language_menu.set_halign(Gtk.Align.CENTER)
        self.language_menu.set_valign(Gtk.Align.START)
        self.language = Gtk.Box()
        self.language.set_halign(Gtk.Align.CENTER)
        self.language.pack_start(self.language_menu, False, False, 15)
        self.language.set_size_request(480, 530)
        self.language.add(self.language_menu)

        self.wizard_page_1 = Gtk.Grid()
        self.wizard_page_1.attach(self.blank, 0, 0, 2, 1)
        self.wizard_page_1.attach(self.logo, 0,1,1,1)
        self.wizard_page_1.attach(self.wizard_1_title, 1, 1, 1, 1)
        self.wizard_page_1.attach(self.language, 0, 2, 2, 1)
        self.wizard_page_1.attach(self.wizard_1_next, 0, 3, 2, 1)

    def show_wizard_2(self):
        self.blank = Gtk.Box()
        self.blank.set_size_request(480, 60)

        self.wizard_2_lbl = Gtk.Label()
        self.wizard_2_lbl.set_hexpand(True)
        self.wizard_2_lbl.set_halign(Gtk.Align.CENTER)
        #self.wizard_2_lbl.set_valign(Gtk.Align.CENTER)
        #self.wizard_2_lbl.set_ellipsize(Pango.EllipsizeMode.END)
        #self.wizard_2_lbl.set_label("Wizard")
        title = _("Connect Network")
        self.wizard_2_lbl.set_markup("<span font='DejaVu Sans-bold 33'>{}</span>".format(title))
        self.wizard_2_title = Gtk.Box()
        #self.wizard_2_title.get_style_contitle().add_class("title_bar")
        self.wizard_2_title.set_size_request(480, 80)
        self.wizard_2_title.set_valign(Gtk.Align.END)
        self.wizard_2_title.add(self.wizard_2_lbl)

        image = self._gtk.Image("wifi", self._gtk.content_width * .4, self._gtk.content_height * .4)
        #self.wifi_logo = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        #self.wifi_logo.set_halign(Gtk.Align.CENTER)
        #self.wifi_logo.set_valign(Gtk.Align.CENTER)
        #self.wifi_logo.set_size_request(480, 100)
        #self.wifi_logo.pack_start(image, False, False, 0)#将image添加到self.logo的起始位置

        self.wizard_2_text = Gtk.Label()
        #self.wizard_2_text.set_hexpand(True)
        self.wizard_2_text.set_halign(Gtk.Align.CENTER)
        #self.wizard_2_text.set_valign(Gtk.Align.CENTER)
        self.wizard_2_text.set_line_wrap(True)
        self.wizard_2_text.set_justify(Gtk.Justification.CENTER)
        text = _("After the machine is connected to the network, devices using the same LAN can control the machine by accessing the IP")
        self.wizard_2_text.set_markup("<span font='DejaVu Sans 20'>{}</span>".format(text))
        self.wizard_2_txt_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.wizard_2_txt_box.set_halign(Gtk.Align.CENTER)
        self.wizard_2_txt_box.set_size_request(450, 420)
        self.wizard_2_txt_box.pack_start(image, False, False, 10)
        #self.wizard_2_txt_box.add(self.wizard_2_text)
        self.wizard_2_txt_box.pack_start(self.wizard_2_text, False, False, 10)

        gws = netifaces.gateways()
        logging.info("init:gws:" + str(gws))
        logging.info("init:netifaces.AF_INET:" + str(netifaces.AF_INET))
        if "default" in gws and netifaces.AF_INET in gws["default"]:
            self.interface = gws["default"][netifaces.AF_INET][1]
        else:
            ints = netifaces.interfaces()
            if 'lo' in ints:
                ints.pop(ints.index('lo'))
                ints.pop(ints.index('eth0'))
            if len(ints) > 0:
                self.interface = ints[0]
            else:
                self.interface = 'lo'
        logging.info("init:self.interface:" + str(self.interface))
        res = netifaces.ifaddresses(self.interface)
        if netifaces.AF_INET in res and len(res[netifaces.AF_INET]) > 0:
            ip = "IP: " + res[netifaces.AF_INET][0]['addr']
        else:
            ip = "Connect"
        self.connect_wifi = self._gtk.Button("", ip, f"color1")
        self.connect_wifi.connect("clicked", self.show_network)
        self.connect_wifi.set_size_request(450, 35)
        self.connect_wifi.set_halign(Gtk.Align.CENTER)
        self.connect_wifi.set_valign(Gtk.Align.CENTER)
        self.wizard_wifi_butt = Gtk.Box()
        self.wizard_wifi_butt.pack_start(self.connect_wifi, False, False, 10)
        self.wizard_wifi_butt.set_size_request(480, 80)

        self.second_nex = self._gtk.Button("arrow-right",_("Next"), f"color2")
        self.second_nex.connect("clicked", self.second_next)
        self.second_nex.set_size_request(210, 110)
        # self.second_nex.set_halign(Gtk.Align.CENTER)
        # self.second_nex.set_valign(Gtk.Align.CENTER)
        self.wizard_2_next = Gtk.Box()
        self.wizard_2_next.set_halign(Gtk.Align.CENTER)
        self.wizard_2_next.set_valign(Gtk.Align.CENTER)
        self.wizard_2_next.pack_start(self.second_nex, False, False, 0)
        #self.wizard_2_next.get_style_context().add_class('button_active')
        self.wizard_2_next.set_size_request(240, 110)
        self.wizard_2_next.add(self.second_nex)

        self.second_bac = self._gtk.Button("arrow-left",_("Back"), f"color1")
        self.second_bac.connect("clicked", self.second_back)
        self.second_bac.set_size_request(210, 110)
        # self.second_bac.set_halign(Gtk.Align.CENTER)
        # self.second_bac.set_valign(Gtk.Align.CENTER)
        self.wizard_2_back = Gtk.Box()
        self.wizard_2_back.set_halign(Gtk.Align.CENTER)
        self.wizard_2_back.set_valign(Gtk.Align.CENTER)
        self.wizard_2_back.pack_start(self.second_bac, False, False, 0)
        #self.wizard_2_back.get_style_context().add_class('button_active')
        self.wizard_2_back.set_size_request(240, 110)
        self.wizard_2_back.add(self.second_bac)

        self.wizard_page_2 = Gtk.Grid()
        self.wizard_page_2.attach(self.blank, 0, 0, 2, 1)
        self.wizard_page_2.attach(self.wizard_2_title, 0, 1, 2, 1)
        #self.wizard_page_2.attach(self.wifi_logo, 0, 1, 2, 1)
        self.wizard_page_2.attach(self.wizard_2_txt_box, 0, 2, 2, 1)
        self.wizard_page_2.attach(self.wizard_wifi_butt, 0, 3, 2, 1)
        self.wizard_page_2.attach(self.wizard_2_back, 0, 4, 1, 1)
        self.wizard_page_2.attach(self.wizard_2_next, 1, 4, 1, 1)
        self._screen.add(self._screen.wizard.wizard_page_2)
        self._screen.show_all()

    def show_wizard_3(self):
        self.blank = Gtk.Box()
        self.blank.set_size_request(480, 60)

        self.wizard_3_lbl = Gtk.Label()
        self.wizard_3_lbl.set_hexpand(True)
        self.wizard_3_lbl.set_halign(Gtk.Align.CENTER)
        self.wizard_3_lbl.set_valign(Gtk.Align.CENTER)
        #self.wizard_3_lbl.set_ellipsize(Pango.EllipsizeMode.END)
        #self.wizard_3_lbl.set_label("Wizard")
        title = _("Leveling Calibration")
        self.wizard_3_lbl.set_markup("<span font='DejaVu Sans-bold 33'>{}</span>".format(title))
        self.wizard_3_title = Gtk.Box()
        #self.wizard_3_title.get_style_context().add_class("title_bar")
        self.wizard_3_title.set_size_request(480, 80)
        self.wizard_3_title.set_valign(Gtk.Align.START)
        self.wizard_3_title.add(self.wizard_3_lbl)

        image = self._gtk.Image("level", self._gtk.content_width * .3, self._gtk.content_height * .3)
        #self.level_logo = Gtk.Box()
        #self.level_logo.set_halign(Gtk.Align.CENTER)
        #self.level_logo.set_valign(Gtk.Align.CENTER)
        #self.level_logo.set_size_request(480, 167)
        #self.level_logo.pack_end(image, True, True, 20)#将image添加到self.logo的起始位置
        #self.logo.pack_end(image, False, False, 10)#将image添加到self.logo的末尾位置

        self.wizard_3_text1 = Gtk.Label()
        #self.wizard_3_text1.set_hexpand(True)
        self.wizard_3_text1.set_halign(Gtk.Align.CENTER)
        self.wizard_3_text1.set_valign(Gtk.Align.CENTER)
        self.wizard_3_text1.set_line_wrap(True)
        self.wizard_3_text1.set_justify(Gtk.Justification.CENTER)
        text1 = _("Please follow the steps below to calibrate the machine, refer to the manual for details")
        self.wizard_3_text1.set_markup("<span font='DejaVu Sans 20'>{}</span>".format(text1))

        self.wizard_3_text2 = Gtk.Label()
        #self.wizard_3_text2.set_hexpand(True)
        self.wizard_3_text2.set_halign(Gtk.Align.CENTER)
        self.wizard_3_text2.set_valign(Gtk.Align.CENTER)
        self.wizard_3_text2.set_line_wrap(True)
        self.wizard_3_text2.set_justify(Gtk.Justification.CENTER)
        text2 = _("1.Operation Z Calibration Setting Offset")
        self.wizard_3_text2.set_markup("<span font='DejaVu Sans 20'>{}</span>".format(text2))

        self.wizard_3_text3 = Gtk.Label()
        #self.wizard_3_text3.set_hexpand(True)
        self.wizard_3_text3.set_halign(Gtk.Align.CENTER)
        self.wizard_3_text3.set_valign(Gtk.Align.CENTER)
        self.wizard_3_text3.set_line_wrap(True)
        self.wizard_3_text3.set_justify(Gtk.Justification.CENTER)
        text3 = _("2.Operate Bed Level to adjust the flatness of the bed")
        self.wizard_3_text3.set_markup("<span font='DejaVu Sans 20'>{}</span>".format(text3))

        self.wizard_3_text4 = Gtk.Label()
        #self.wizard_3_text4.set_hexpand(True)
        self.wizard_3_text4.set_halign(Gtk.Align.CENTER)
        self.wizard_3_text4.set_valign(Gtk.Align.CENTER)
        self.wizard_3_text4.set_line_wrap(True)
        self.wizard_3_text4.set_justify(Gtk.Justification.CENTER)
        text4 = _("3.Operate Bed Mesh automatic leveling")
        self.wizard_3_text4.set_markup("<span font='DejaVu Sans 20'>{}</span>".format(text4))

        self.wizard_3_txt_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.wizard_3_txt_box.set_size_request(480, 530)
        self.wizard_3_txt_box.pack_start(image, False, False, 20)
        self.wizard_3_txt_box.add(self.wizard_3_text1)
        self.wizard_3_txt_box.add(self.wizard_3_text2)
        self.wizard_3_txt_box.add(self.wizard_3_text3)
        self.wizard_3_txt_box.add(self.wizard_3_text4)

        self.third_nex = self._gtk.Button("complete",_("Finish"), f"color1")
        self.third_nex.connect("clicked", self.final_next)
        self.third_nex.set_size_request(210, 110)
        self.third_nex.set_halign(Gtk.Align.CENTER)
        self.third_nex.set_valign(Gtk.Align.CENTER)
        self.wizard_3_next = Gtk.Box()
        self.wizard_3_next.pack_start(self.third_nex, False, False, 10)
        #self.wizard_3_next.get_style_context().add_class('button_active')
        self.wizard_3_next.set_size_request(240, 110)
        self.wizard_3_next.add(self.third_nex)

        self.third_bac = self._gtk.Button("arrow-left",_("Back"), f"color4")
        self.third_bac.connect("clicked", self.third_back)
        self.third_bac.set_size_request(210, 110)
        self.third_bac.set_halign(Gtk.Align.CENTER)
        self.third_bac.set_valign(Gtk.Align.CENTER)
        self.wizard_3_back = Gtk.Box()
        self.wizard_3_back.pack_start(self.third_bac, False, False, 10)
        #self.wizard_3_back.get_style_context().add_class('button_active')
        self.wizard_3_back.set_size_request(240, 110)
        self.wizard_3_back.add(self.third_bac)

        self.wizard_page_3 = Gtk.Grid()
        self.wizard_page_3.attach(self.blank, 0, 0, 2, 1)
        self.wizard_page_3.attach(self.wizard_3_title, 0, 1, 2, 1)
        #self.wizard_page_3.attach(self.level_logo, 0, 1, 2, 1)
        self.wizard_page_3.attach(self.wizard_3_txt_box, 0, 2, 2, 1)
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

    def leave_wifi_page(self,widget):
        self._screen.remove(self.box)
        self.show_wizard_2()
        self._screen.add(self._screen.wizard.wizard_page_1)
        self._screen.show_all()

    def third_back(self,widget):
        self._screen.remove(self.wizard_page_3)
        self.show_wizard_2()
        

    # def second_next(self, widget):
    #     self._screen.remove()

    def final_next(self, widget):
        #self._screen.remove(self.wizard_page)#如果只是remove这个而没有再次add、show_all则是黑屏
        self._screen._config.set("main", "wizard_tag", "False")
        self._screen._config.save_user_config_options()
        self._screen.remove(self.wizard_page_3)
        self._screen.add(self._screen.base_panel.main_grid)
        self._screen.show_all()

    def show_network(self,widget):
        self._screen.remove(self.wizard_page_2)
        self.show_add = False
        self.networks = {}
        self.interface = None
        self.prev_network = None
        self.update_timeout = None
        self.network_interfaces = netifaces.interfaces()
        self.wireless_interfaces = [iface for iface in self.network_interfaces if iface.startswith('w')]
        self.wifi = None
        self.use_network_manager = os.system('systemctl is-active --quiet NetworkManager.service') == 0
        #self.use_network_manager = False
        if len(self.wireless_interfaces) > 0:
            logging.info(f"Found wireless interfaces: {self.wireless_interfaces}")
            if self.use_network_manager:
                logging.info("Using NetworkManager")
                from ks_includes.wifi_nm import WifiManager
            else:
                logging.info("Using wpa_cli")
                from ks_includes.wifi import WifiManager
            self.wifi = WifiManager(self.wireless_interfaces[0])

        # Get IP Address
        gws = netifaces.gateways()
        logging.info("init:gws:" + str(gws))
        logging.info("init:netifaces.AF_INET:" + str(netifaces.AF_INET))
        if "default" in gws and netifaces.AF_INET in gws["default"]:
            self.interface = gws["default"][netifaces.AF_INET][1]
        else:
            ints = netifaces.interfaces()
            if 'lo' in ints:
                ints.pop(ints.index('lo'))
                ints.pop(ints.index('eth0'))
            if len(ints) > 0:
                self.interface = ints[0]
            else:
                self.interface = 'lo'
        logging.info("init:self.interface:" + str(self.interface))
        res = netifaces.ifaddresses(self.interface)
        if netifaces.AF_INET in res and len(res[netifaces.AF_INET]) > 0:
            ip = res[netifaces.AF_INET][0]['addr']
        else:
            ip = None

        self.labels['networks'] = {}

        self.labels['interface'] = Gtk.Label()
        self.labels['interface'].set_text(" %s: %s  " % (_("Interface"), self.interface))
        self.labels['interface'].set_hexpand(True)
        self.labels['ip'] = Gtk.Label()
        self.labels['ip'].set_hexpand(True)
        reload_networks = self._gtk.Button("refresh", None, "color1", .66)
        reload_networks.connect("clicked", self.reload_networks)
        reload_networks.set_hexpand(False)
        back_to_page_2 = self._gtk.Button("arrow-left", None , "color2", .66)
        back_to_page_2.connect("clicked", self.leave_wifi_page)
        back_to_page_2.set_hexpand(False)

        sbox = Gtk.Box()
        sbox.set_hexpand(True)
        sbox.set_vexpand(False)
        sbox.add(self.labels['interface'])
        if ip is not None:
            self.labels['ip'].set_text(f"IP: {ip}  ")
            sbox.add(self.labels['ip'])
        sbox.add(reload_networks)
        sbox.add(back_to_page_2)

        scroll = self._gtk.ScrolledWindow()

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.box.set_vexpand(True)

        self.labels['networklist'] = Gtk.Grid()

        if self.wifi is not None and self.wifi.initialized:
            self.box.pack_start(sbox, False, False, 5)
            self.box.pack_start(scroll, True, True, 0)

            GLib.idle_add(self.load_networks)
            scroll.add(self.labels['networklist'])

            self.wifi.add_callback("connected", self.connected_callback)
            self.wifi.add_callback("scan_results", self.scan_callback)
            self.wifi.add_callback("popup", self.popup_callback)
            if self.update_timeout is None:
                self.update_timeout = GLib.timeout_add_seconds(5, self.update_all_networks)
        else:
            self.labels['networkinfo'] = Gtk.Label("")
            self.labels['networkinfo'].get_style_context().add_class('temperature_entry')
            self.box.pack_start(self.labels['networkinfo'], False, False, 0)
            self.update_single_network_info()
            if self.update_timeout is None:
                self.update_timeout = GLib.timeout_add_seconds(5, self.update_single_network_info)

        self._screen.add(self._screen.wizard.box)
        self.labels['main_box'] = self.box
        self.initialized = True

        self._screen.add(self._screen.wizard.box)
        self._screen.show_all()


#for network ↓
    def load_networks(self):
        networks = self.wifi.get_networks()
        if not networks:
            return
        for net in networks:
            self.add_network(net, False)
        self.update_all_networks()
        self._screen.show_all()

    def add_network(self, ssid, show=True):

        if ssid is None:
            return
        ssid = ssid.strip()
        if ssid in list(self.networks):
            return

        configured_networks = self.wifi.get_supplicant_networks()
        network_id = -1
        for net in list(configured_networks):
            if configured_networks[net]['ssid'] == ssid:
                network_id = net

        display_name = _("Hidden") if ssid.startswith("\x00") else f"{ssid}"
        #ssid_unicode = bytes(ssid.encode('utf-8')).decode('unicode_escape').encode('latin1').decode('utf-8')
        
        netinfo = self.wifi.get_network_info(ssid)
        connected_ssid = self.wifi.get_connected_ssid()
        if netinfo is None:
            logging.debug("Couldn't get netinfo")
            if connected_ssid == ssid:
                netinfo = {'connected': True}
            else:
                netinfo = {'connected': False}

        if connected_ssid == ssid:
            display_name += " (" + _("Connected") + ")"

        name = Gtk.Label("")
        name.set_markup(f"<big><b>{display_name}</b></big>")
        name.set_hexpand(True)
        name.set_halign(Gtk.Align.START)
        name.set_line_wrap(True)
        name.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR)

        info = Gtk.Label()
        info.set_halign(Gtk.Align.START)
        labels = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        labels.add(name)
        labels.add(info)
        labels.set_vexpand(True)
        labels.set_valign(Gtk.Align.CENTER)
        labels.set_halign(Gtk.Align.START)

        connect = self._gtk.Button("load", None, "color3", .66)
        connect.connect("clicked", self.connect_network, ssid)
        connect.set_hexpand(False)
        connect.set_halign(Gtk.Align.END)

        delete = self._gtk.Button("delete", None, "color3", .66)
        delete.connect("clicked", self.remove_wifi_network, ssid)
        delete.set_hexpand(False)
        delete.set_halign(Gtk.Align.END)

        network = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        network.get_style_context().add_class("frame-item")
        network.set_hexpand(True)
        network.set_vexpand(False)

        network.add(labels)

        buttons = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        if network_id != -1 or netinfo['connected']:
            buttons.pack_end(connect, False, False, 0)
            buttons.pack_end(delete, False, False, 0)
        else:
            buttons.pack_end(connect, False, False, 0)
        network.add(buttons)
        self.networks[ssid] = network

        nets = sorted(list(self.networks), reverse=False)
        if connected_ssid in nets:
            nets.remove(connected_ssid)
            nets.insert(0, connected_ssid)
        if nets.index(ssid) is not None:
            pos = nets.index(ssid)
        else:
            logging.info("Error: SSID not in nets")
            return

        self.labels['networks'][ssid] = {
            "connect": connect,
            "delete": delete,
            "info": info,
            "name": name,
            "row": network
        }

        self.labels['networklist'].insert_row(pos)
        self.labels['networklist'].attach(self.networks[ssid], 0, pos, 1, 1)
        if show:
            self.labels['networklist'].show()

    def add_new_network(self, widget, ssid, connect=False):
        self.remove_keyboard()
        psk = self.labels['network_psk'].get_text()
        logging.info("add new network:" + ssid)
        result = self.wifi.add_network(ssid, psk)

        self.close_add_network()

        if connect:
            if result:
                self.connect_network(widget, ssid, False)
            else:
                self._screen.show_popup_message(f"Error adding network {ssid}")

    def back(self):
        if self.show_add:
            self.close_add_network()
            return True
        return False

    def check_missing_networks(self):
        networks = self.wifi.get_networks()
        for net in list(self.networks):
            if net in networks:
                networks.remove(net)

        for net in networks:
            self.add_network(net, False)
        self.labels['networklist'].show_all()

    def close_add_network(self):
        if not self.show_add:
            return

        for child in self._screen.get_children():
            self._screen.remove(child)
        self._screen.add(self.labels['main_box'])
        self._screen.show()
        for i in ['add_network', 'network_psk']:
            if i in self.labels:
                del self.labels[i]
        self.show_add = False

    def popup_callback(self, msg):
        self._screen.show_popup_message(msg)

    def connected_callback(self, ssid, prev_ssid):
        logging.info("Now connected to a new network")
        if ssid is not None:
            self.remove_network(ssid)
        if prev_ssid is not None:
            self.remove_network(prev_ssid)

        self.check_missing_networks()

    def connect_network(self, widget, ssid, showadd=True):

        snets = self.wifi.get_supplicant_networks()
        isdef = False
        for netid, net in snets.items():
            if net['ssid'] == ssid:
                isdef = True
                break

        if not isdef:
            if showadd:
                self.show_add_network(widget, ssid)
            return
        self.prev_network = self.wifi.get_connected_ssid()

        buttons = [
            {"name": _("Close"), "response": Gtk.ResponseType.CANCEL}
        ]

        scroll = self._gtk.ScrolledWindow()
        self.labels['connecting_info'] = Gtk.Label(_("Starting WiFi Association"))
        self.labels['connecting_info'].set_halign(Gtk.Align.START)
        self.labels['connecting_info'].set_valign(Gtk.Align.START)
        scroll.add(self.labels['connecting_info'])
        dialog = self._gtk.Dialog(self._screen, buttons, scroll, self._gtk.remove_dialog)
        dialog.set_title(_("Starting WiFi Association"))
        self._screen.show_all()

        if ssid in list(self.networks):
            self.remove_network(ssid)
        if self.prev_network in list(self.networks):
            self.remove_network(self.prev_network)

        self.wifi.add_callback("connecting_status", self.connecting_status_callback)
        self.wifi.connect(ssid)

    def connecting_status_callback(self, msg):
        self.labels['connecting_info'].set_text(f"{self.labels['connecting_info'].get_text()}\n{msg}")
        self.labels['connecting_info'].show_all()

    def remove_network(self, ssid, show=True):
        if ssid not in list(self.networks):
            return
        for i in range(len(self.labels['networklist'])):
            if self.networks[ssid] == self.labels['networklist'].get_child_at(0, i):
                self.labels['networklist'].remove_row(i)
                self.labels['networklist'].show()
                del self.networks[ssid]
                del self.labels['networks'][ssid]
                return

    def remove_wifi_network(self, widget, ssid):
        self.wifi.delete_network(ssid)
        self.remove_network(ssid)
        self.check_missing_networks()

    def scan_callback(self, new_networks, old_networks):
        for net in old_networks:
            self.remove_network(net, False)
        for net in new_networks:
            self.add_network(net, False)
        self._screen.show_all()

    def show_add_network(self, widget, ssid):
        if self.show_add:
            return

        for child in self._screen.get_children():
            self._screen.remove(child)

        if "add_network" in self.labels:
            del self.labels['add_network']

        label = self._gtk.Label(_("PSK for") + ' ssid')
        label.set_hexpand(False)
        self.labels['network_psk'] = Gtk.Entry()
        self.labels['network_psk'].set_text('')
        self.labels['network_psk'].set_hexpand(True)
        self.labels['network_psk'].connect("activate", self.add_new_network, ssid, True)
        self.labels['network_psk'].connect("focus-in-event", self.show_keyboard)

        save = self._gtk.Button("sd", _("Save"), "color3")
        save.set_hexpand(False)
        save.connect("clicked", self.add_new_network, ssid, True)

        box = Gtk.Box()
        box.pack_start(self.labels['network_psk'], True, True, 5)
        box.pack_start(save, False, False, 5)

        self.labels['add_network'] = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.labels['add_network'].set_valign(Gtk.Align.CENTER)
        self.labels['add_network'].set_hexpand(True)
        self.labels['add_network'].set_vexpand(True)
        self.labels['add_network'].pack_start(label, True, True, 5)
        self.labels['add_network'].pack_start(box, True, True, 5)

        self._screen.add(self.labels['add_network'])
        self.labels['network_psk'].grab_focus_without_selecting()
        self._screen.show_all()
        self.show_add = True

    def update_all_networks(self):
        for network in list(self.networks):
            self.update_network_info(network)
        return True

    def update_network_info(self, ssid):
        
        info = freq = encr = chan = lvl = ipv4 = ipv6 = ""

        if ssid not in list(self.networks) or ssid not in self.labels['networks']:
            logging.info(f"Unknown SSID {ssid}")
            return
        
        netinfo = self.wifi.get_network_info(ssid)
        if "connected" in netinfo:
            connected = netinfo['connected']
        else:
            connected = False

        if connected or self.wifi.get_connected_ssid() == ssid:
            stream = os.popen('hostname -f')
            hostname = stream.read().strip()
            ifadd = netifaces.ifaddresses(self.interface)
            logging.info("self.interface:" + str(self.interface))
            logging.info("ifadd:" + str(ifadd))
            if netifaces.AF_INET in ifadd and len(ifadd[netifaces.AF_INET]) > 0:
                ipv4 = f"<b>IPv4:</b> {ifadd[netifaces.AF_INET][0]['addr']} "
                self.labels['ip'].set_text(f"IP: {ifadd[netifaces.AF_INET][0]['addr']}  ")
            if netifaces.AF_INET6 in ifadd and len(ifadd[netifaces.AF_INET6]) > 0:
                ipv6 = f"<b>IPv6:</b> {ifadd[netifaces.AF_INET6][0]['addr'].split('%')[0]} "
            info = '<b>' + _("Hostname") + f':</b> {hostname}\n{ipv4}\n{ipv6}\n'
        elif "psk" in netinfo:
            info = _("Password saved")
        if "encryption" in netinfo:
            if netinfo['encryption'] != "off":
                encr = netinfo['encryption'].upper()
        if "frequency" in netinfo:
            freq = "2.4 GHz" if netinfo['frequency'][0:1] == "2" else "5 Ghz"
        if "channel" in netinfo:
            chan = _("Channel") + f' {netinfo["channel"]}'
        if "signal_level_dBm" in netinfo:
            lvl = f'{netinfo["signal_level_dBm"]} ' + _("dBm")

        self.labels['networks'][ssid]['info'].set_markup(f"{info} <small>{encr}  {freq}  {chan}  {lvl}</small>")
        self.labels['networks'][ssid]['info'].show_all()

    def update_single_network_info(self):

        stream = os.popen('hostname -f')
        hostname = stream.read().strip()
        ifadd = netifaces.ifaddresses(self.interface)
        ipv4 = ""
        ipv6 = ""
        if netifaces.AF_INET in ifadd and len(ifadd[netifaces.AF_INET]) > 0:
            ipv4 = f"<b>IPv4:</b> {ifadd[netifaces.AF_INET][0]['addr']} "
            self.labels['ip'].set_text(f"IP: {ifadd[netifaces.AF_INET][0]['addr']}  ")
        if netifaces.AF_INET6 in ifadd and len(ifadd[netifaces.AF_INET6]) > 0:
            ipv6 = f"<b>IPv6:</b> {ifadd[netifaces.AF_INET6][0]['addr'].split('%')[0]} "
        connected = (
            f'<b>{self.interface}</b>\n\n'
            f'<small><b>' + _("Connected") + f'</b></small>\n'
            + '<b>' + _("Hostname") + f':</b> {hostname}\n'
            f'{ipv4}\n'
            f'{ipv6}\n'
        )

        self.labels['networkinfo'].set_markup(connected)
        self.labels['networkinfo'].show_all()

    def reload_networks(self, widget=None):
        self.networks = {}
        self.labels['networklist'].remove_column(0)
        if self.wifi is not None and self.wifi.initialized:
            self.wifi.rescan()
            GLib.idle_add(self.load_networks)

    def activate(self):
        if self.initialized:
            self.reload_networks()
            if self.update_timeout is None:
                if self.wifi is not None and self.wifi.initialized:
                    self.update_timeout = GLib.timeout_add_seconds(5, self.update_all_networks)
                else:
                    self.update_timeout = GLib.timeout_add_seconds(5, self.update_single_network_info)

    def deactivate(self):
        if self.update_timeout is not None:
            GLib.source_remove(self.update_timeout)
            self.update_timeout = None


#for key_board↓
    def show_keyboard(self, entry=None, event=None):
        if self.keyboard is not None:
            return

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.set_size_request(self._gtk.content_width, self._gtk.keyboard_height)

        if self._screen._config.get_main_config().getboolean("use-matchbox-keyboard", False):
            return self._screen._show_matchbox_keyboard(box)
        if entry is None:
            logging.debug("Error: no entry provided for keyboard")
            return
        box.get_style_context().add_class("keyboard_box")
        box.add(Keyboard(self, self.remove_keyboard, entry=entry))
        self.keyboard = {"box": box}
        self.pack_end(box, False, False, 0)
        self.show_all()

    def remove_keyboard(self, widget=None, event=None):
        if self.keyboard is None:
            return
        if 'process' in self.keyboard:
            os.kill(self.keyboard['process'].pid, SIGTERM)
        self.remove(self.keyboard['box'])
        self.keyboard = None
