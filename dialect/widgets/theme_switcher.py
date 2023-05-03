# Copyright 2020 Manuel Genovés
# Copyright 2022 Mufeed Ali
# Copyright 2022 Rafael Mardojai CM
# SPDX-License-Identifier: GPL-3.0-or-later

# Code modified from Apostrophe
# https://gitlab.gnome.org/World/apostrophe/-/blob/main/apostrophe/theme_switcher.py

from gi.repository import Adw, Gio, GObject, Gtk

from dialect.define import RES_PATH
from dialect.settings import Settings


@Gtk.Template(resource_path=f'{RES_PATH}/theme-switcher.ui')
class ThemeSwitcher(Gtk.Box):
    __gtype_name__ = 'ThemeSwitcher'

    # Properties
    show_system = GObject.property(type=bool, default=True)
    color_scheme = 'light'

    # Child widgets
    system = Gtk.Template.Child()
    light = Gtk.Template.Child()
    dark = Gtk.Template.Child()

    @GObject.Property(type=str)
    def selected_color_scheme(self):
        """Read-write integer property."""

        return self.color_scheme

    @selected_color_scheme.setter
    def selected_color_scheme(self, color_scheme):
        self.color_scheme = color_scheme

        if color_scheme == 'auto':
            self.system.props.active = True
            self.style_manager.props.color_scheme = Adw.ColorScheme.PREFER_LIGHT
        if color_scheme == 'light':
            self.light.props.active = True
            self.style_manager.props.color_scheme = Adw.ColorScheme.FORCE_LIGHT
        if color_scheme == 'dark':
            self.dark.props.active = True
            self.style_manager.props.color_scheme = Adw.ColorScheme.FORCE_DARK

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.style_manager = Adw.StyleManager.get_default()

        self.color_scheme = Settings.get().color_scheme

        Settings.get().bind(
            'color-scheme',
            self,
            'selected_color_scheme',
            Gio.SettingsBindFlags.DEFAULT
        )

        self.style_manager.bind_property(
            'system-supports-color-schemes',
            self, 'show_system',
            GObject.BindingFlags.SYNC_CREATE
        )

    @Gtk.Template.Callback()
    def _on_color_scheme_changed(self, _widget, _paramspec):
        """ Called on (self.system, self.light, self.dark)::notify::active signal """
        if self.system.props.active:
            self.selected_color_scheme = 'auto'
        if self.light.props.active:
            self.selected_color_scheme = 'light'
        if self.dark.props.active:
            self.selected_color_scheme = 'dark'
