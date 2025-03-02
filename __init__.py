# Copyright (c) 2024 Harsh Narayan Jha

"""
This plugin allows you to quickly search through and switch to open windows on Hyprland

Disclaimer: This plugin has no affiliation with Hyprland.. The icons are used under the terms specified there.
"""

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from shutil import which
from typing import Any

from albert import (  # type: ignore
    Action,
    GlobalQueryHandler,
    Item,
    Matcher,
    PluginInstance,
    Query,
    RankItem,
    StandardItem,
    runDetachedProcess,
)

md_iid = "2.3"
md_version = "0.2"
md_name = "Hyprland Window Switcher"
md_description = "Switch to your open windows on Hyprland swiftly"
md_license = "MIT"
md_url = "https://github.com/HarshNarayanJha/albert_hypr_window_switcher"
md_authors = ["@HarshNarayanJha"]


@dataclass
class Window:
    address: str
    title: str
    classs: str
    initialTitle: str
    initialClass: str
    at: tuple[int, int]
    size: tuple[int, int]
    workspace: dict[str, Any]
    floating: bool
    hidden: bool
    monitor: int
    pid: int
    xwayland: bool
    pinned: bool
    fullscreen: bool
    grouped: list[str]
    focusHistoryID: int

    def __init__(
        self,
        address: str,
        title: str,
        initialTitle: str,
        initialClass: str,
        at: tuple[int, int],
        size: tuple[int, int],
        workspace: dict[str, Any],
        floating: bool,
        hidden: bool,
        monitor: int,
        pid: int,
        xwayland: bool,
        pinned: bool,
        fullscreen: bool,
        grouped: list[str],
        focusHistoryID: int,
        **kwargs,
    ) -> None:
        self.address = address
        self.title = title
        self.classs = kwargs["class"]
        self.initialTitle = initialTitle
        self.initialClass = initialClass
        self.at = at
        self.size = size
        self.workspace = workspace
        self.floating = floating
        self.hidden = hidden
        self.monitor = monitor
        self.pid = pid
        self.xwayland = xwayland
        self.pinned = pinned
        self.fullscreen = fullscreen
        self.grouped = grouped
        self.focusHistoryID = focusHistoryID

        self.parseDesktopFile()
        self.name = self.name or self.classs
        self.icon = self.icon or "binary"

    def parseDesktopFile(self) -> None:
        desktopFile = Path(f"/usr/share/applications/{self.classs}.desktop")
        self.name = ""
        self.icon = None

        current_section = ""

        if desktopFile.exists():
            with open(desktopFile, "r") as fp:
                while line := fp.readline():
                    line = line.strip()

                    if line.startswith("["):
                        current_section = line.strip("][")
                    elif (
                        not self.icon
                        and line.startswith("Icon=")
                        and current_section == "Desktop Entry"
                    ):
                        self.icon = line.split("=")[1]
                    elif (
                        not self.name
                        and line.startswith("Name=")
                        and current_section == "Desktop Entry"
                    ):
                        self.name = line.split("=")[1]

    @staticmethod
    def current_workspace_id() -> int:
        output = json.loads(
            subprocess.check_output(["hyprctl", "activeworkspace", "-j"])
        )
        id = output["id"]
        return id

    @staticmethod
    def list_windows() -> list["Window"]:
        windows = []
        for win_data in json.loads(
            subprocess.check_output(["hyprctl", "clients", "-j"])
        ):
            win = Window(**win_data)

            if win.classs == "albert":
                continue
            windows.append(win)

        return windows


class Plugin(PluginInstance, GlobalQueryHandler):
    def __init__(self):
        PluginInstance.__init__(self)
        GlobalQueryHandler.__init__(
            self, self.id, self.name, self.description, defaultTrigger="w "
        )

        if which("hyprctl") is None:
            raise Exception(
                "'hyprctl' not in $PATH, you sure you are running hyprland?"
            )

    def handleGlobalQuery(self, query: Query) -> list[RankItem]:
        rank_items = []

        windows = Window.list_windows()
        current_workspace = Window.current_workspace_id()

        m = Matcher(query.string)

        windows = [
            w
            for w in windows
            if m.match(w.classs)
            or m.match(w.name)
            or m.match(w.title)
            or m.match(w.initialClass)
            or m.match(w.initialTitle)
        ]

        # sort by focus history
        windows.sort(key=lambda x: x.focusHistoryID, reverse=True)

        rank_items.extend(
            [
                RankItem(self._make_item(current_workspace, window, query), 1)
                for window in windows
            ]
        )

        return rank_items

    def _make_item(self, workspace_id: int, window: Window, query: Query) -> Item:
        return StandardItem(
            id=str(window.address),
            text=f"Window: {window.name}",
            subtext=window.title,
            inputActionText=query.trigger + window.name,
            iconUrls=[f"xdg:{window.icon}"],
            actions=[
                Action(
                    "Switch",
                    "Switch to Window",
                    lambda: self._focus_window(window),
                ),
                Action(
                    "Move Here",
                    "Move to this Workspace",
                    lambda: self._move_window_here(window, workspace_id),
                ),
            ],
        )

    def _focus_window(self, window: Window) -> None:
        runDetachedProcess(
            [
                "hyprctl",
                "dispatch",
                "focuswindow",
                f"address:{window.address}",
            ]
        )

    def _move_window_here(self, window: Window, workspace_id: int) -> None:
        runDetachedProcess(
            [
                "hyprctl",
                "dispatch",
                "focuswindow",
                f"address:{window.address}",
            ]
        )

        runDetachedProcess(
            [
                "hyprctl",
                "dispatch",
                "movetoworkspace",
                str(workspace_id),
            ]
        )

    def configWidget(self):
        return [
            {
                "type": "label",
                "text": str(__doc__).strip(),
                "widget_properties": {"textFormat": "Qt::MarkdownText"},
            }
        ]
