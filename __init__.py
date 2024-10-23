# Copyright (c) 2024 Harsh Narayan Jha

"""
This plugin allows you to quickly search through and switch to open windows on Hyprland

Disclaimer: This plugin has no affiliation with Hyprland.. The icons are used under the terms specified there.
"""

from albert import (
    Action,
    Item, Matcher, Query, StandardItem,
    GlobalQueryHandler, TriggerQueryHandler, PluginInstance
)

md_iid = '2.3'
md_version = "0.1"
md_name = "Hyprland Window Switcher"
md_description = "Switch to your open windows on Hyprland swiftly"
md_license = "MIT"
md_url = "https://github.com/HarshNarayanJha/albert_hypr_window_switcher"
md_authors = ["@HarshNarayanJha"]

class Plugin(PluginInstance, GlobalQueryHandler, TriggerQueryHandler):
    pass
