from __future__ import annotations

import os
from typing import Callable

from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, ScrollableContainer
from textual.screen import ModalScreen, Screen
from textual.widgets import (
    Button,
    Input,
    Label,
    ListItem,
    ListView,
    Static,
)

from lockbox.vault import loadVault, saveVault, vaultFile
from lockbox.generator import generatePassword


def copyText(text: str) -> bool:
    try:
        import pyperclip
        pyperclip.copy(text)
        return True
    except Exception:
        return False


APP_CSS = """
Screen {
    background: #0d1117;
}

Button {
    background: #21262d;
    border: tall #30363d;
    color: #c9d1d9;
    min-width: 10;
    height: 3;
}
Button:hover {
    background: #30363d;
    border: tall #58a6ff;
    color: #e6edf3;
}
Button:focus {
    background: #30363d;
    border: tall #58a6ff;
    color: #e6edf3;
}
Button.-primary {
    background: #1f6feb;
    border: tall #388bfd;
    color: #ffffff;
}
Button.-primary:hover {
    background: #388bfd;
    border: tall #58a6ff;
}
Button.-danger {
    background: #21262d;
    border: tall #f85149;
    color: #f85149;
}
Button.-danger:hover {
    background: #f85149;
    color: #ffffff;
    border: tall #f85149;
}

Input {
    background: #0d1117;
    border: tall #30363d;
    color: #e6edf3;
    height: 3;
    padding: 0 1;
}
Input:focus {
    border: tall #388bfd;
}

#topbar {
    height: 5;
    background: #161b22;
    border-bottom: solid #21262d;
    padding: 0 2;
    align: left middle;
}
#topbar-title {
    color: #58a6ff;
    text-style: bold;
    width: auto;
    padding: 0 1;
    margin-right: 1;
    content-align: left middle;
    height: 3;
}
#topbar-div {
    color: #30363d;
    width: 1;
    height: 3;
    content-align: center middle;
    margin-right: 1;
}
#btn-new {
    background: #1f6feb;
    border: tall #388bfd;
    color: #ffffff;
    min-width: 9;
    margin-right: 1;
}
#btn-new:hover {
    background: #388bfd;
    border: tall #58a6ff;
}
#btn-gen {
    min-width: 12;
    margin-right: 1;
}
#btn-lock {
    min-width: 8;
    margin-right: 1;
}
#search {
    width: 22;
    margin-left: 1;
}

#layout {
    height: 1fr;
}

#sidebar {
    width: 22;
    border-right: solid #21262d;
    background: #161b22;
    height: 1fr;
}
#sidebar-hd {
    height: 2;
    background: #0d1117;
    color: #c9d1d9;
    padding: 0 2;
    content-align: left middle;
    border-bottom: solid #21262d;
}
#svc-list {
    height: 1fr;
    background: #161b22;
    border: none;
    padding: 1 0;
}
#svc-list > ListItem {
    background: #161b22;
    color: #8b949e;
    padding: 0 2;
    height: 2;
    content-align: left middle;
}
#svc-list > ListItem:hover {
    background: #21262d;
    color: #c9d1d9;
}
#svc-list > ListItem.--highlight {
    background: #21262d;
    color: #58a6ff;
}
#svc-list:focus > ListItem.--highlight {
    background: #21262d;
    color: #58a6ff;
}

#detail {
    width: 1fr;
    padding: 1 2;
    height: 1fr;
}
#detail-scroll {
    height: 1fr;
}
#empty-hint, .empty-hint {
    color: #484f58;
    text-align: center;
    margin-top: 6;
    width: 100%;
}

#statusbar {
    height: 1;
    background: #161b22;
    border-top: solid #21262d;
    color: #484f58;
    padding: 0 2;
    content-align: left middle;
}

EntryCard {
    border: solid #21262d;
    padding: 1 2;
    margin-bottom: 1;
    background: #161b22;
    height: auto;
}
EntryCard:focus-within {
    border: solid #388bfd;
}
.card-svc {
    color: #58a6ff;
    text-style: bold;
    height: 1;
    margin-bottom: 1;
}
.card-row {
    height: 1;
}
.card-key {
    color: #484f58;
    width: 12;
}
.card-val {
    color: #c9d1d9;
}
.card-actions {
    margin-top: 1;
    height: 3;
    align: left middle;
}
.card-btn {
    min-width: 8;
    margin-right: 1;
    height: 3;
}

UnlockScreen {
    align: center middle;
    background: #0d1117;
}
#lock-wrap {
    width: 50;
    height: auto;
    border: solid #30363d;
    padding: 3 4;
    background: #161b22;
}
#lock-logo {
    text-align: center;
    color: #58a6ff;
    text-style: bold;
    height: 2;
    content-align: center middle;
    margin-bottom: 1;
}
#lock-sub {
    text-align: center;
    color: #8b949e;
    height: 1;
    margin-bottom: 2;
}
#lock-err {
    color: #f85149;
    text-align: center;
    height: 1;
}
#btn-unlock {
    width: 100%;
    margin-top: 1;
    background: #1f6feb;
    border: tall #388bfd;
    color: #ffffff;
}
#btn-unlock:hover {
    background: #388bfd;
    border: tall #58a6ff;
}

ConfirmModal {
    align: center middle;
}
#confirm-wrap {
    width: 44;
    height: auto;
    border: solid #30363d;
    padding: 2 3;
    background: #161b22;
}
#confirm-msg {
    text-align: center;
    color: #c9d1d9;
    margin-bottom: 2;
    height: 2;
    content-align: center middle;
}
#confirm-btns {
    height: 3;
    align: center middle;
}
#btn-cancel {
    margin: 0 1;
    width: 12;
}
#btn-ok {
    margin: 0 1;
    width: 12;
    border: tall #f85149;
    color: #f85149;
}
#btn-ok:hover {
    background: #f85149;
    color: #ffffff;
}

EntryModal {
    align: center middle;
}
#entry-wrap {
    width: 56;
    height: auto;
    border: solid #30363d;
    padding: 2 3;
    background: #161b22;
}
#entry-title {
    text-align: center;
    color: #58a6ff;
    text-style: bold;
    margin-bottom: 2;
    height: 1;
}
.f-label {
    color: #8b949e;
    height: 1;
}
.f-input {
    margin-bottom: 1;
}
.f-input:disabled {
    color: #484f58;
    background: #0d1117;
    border: tall #21262d;
}
#btn-gen-pw {
    width: 100%;
    margin-top: 0;
    margin-bottom: 1;
}
#gen-preview {
    color: #3fb950;
    height: 1;
    margin-bottom: 1;
    text-align: center;
}
#entry-err {
    color: #f85149;
    height: 1;
    margin-bottom: 1;
    text-align: center;
}
#entry-btns {
    margin-top: 1;
    height: 3;
    align: center middle;
}
#btn-entry-cancel {
    margin: 0 1;
    width: 12;
}
#btn-entry-save {
    margin: 0 1;
    width: 12;
    background: #1f6feb;
    border: tall #388bfd;
    color: #ffffff;
}
#btn-entry-save:hover {
    background: #388bfd;
    border: tall #58a6ff;
}
"""


class UnlockScreen(Screen):
    CSS = APP_CSS

    def __init__(self, onSuccess: Callable[[str, dict], None], initMode: bool = False) -> None:
        super().__init__()
        self._onSuccess = onSuccess
        self._initMode = initMode

    def compose(self) -> ComposeResult:
        with Vertical(id="lock-wrap"):
            yield Label("LockBox", id="lock-logo")
            if self._initMode:
                yield Label("Create a master password to get started.", id="lock-sub")
            else:
                yield Label("Enter your master password to unlock.", id="lock-sub")
            yield Input(placeholder="Master password", password=True, id="lock-pw")
            if self._initMode:
                yield Input(placeholder="Confirm master password", password=True, id="lock-confirm")
            yield Label("", id="lock-err")
            yield Button("Create Vault" if self._initMode else "Unlock", id="btn-unlock")

    def on_mount(self) -> None:
        self.query_one("#lock-pw", Input).focus()

    def _attempt(self) -> None:
        pw = self.query_one("#lock-pw", Input).value
        errLabel = self.query_one("#lock-err", Label)
        if not pw:
            errLabel.update("Password cannot be empty.")
            return
        if self._initMode:
            try:
                confirm = self.query_one("#lock-confirm", Input).value
            except Exception:
                confirm = pw
            if pw != confirm:
                errLabel.update("Passwords do not match.")
                return
            saveVault(pw, {})
            self._onSuccess(pw, {})
            return
        data = loadVault(pw)
        if data is None:
            errLabel.update("Wrong password.")
            self.query_one("#lock-pw", Input).value = ""
            self.query_one("#lock-pw", Input).focus()
            return
        self._onSuccess(pw, data)

    @on(Button.Pressed, "#btn-unlock")
    def _btnUnlock(self) -> None:
        self._attempt()

    @on(Input.Submitted, "#lock-pw")
    def _pwSubmitted(self) -> None:
        if self._initMode:
            try:
                self.query_one("#lock-confirm", Input).focus()
            except Exception:
                self._attempt()
        else:
            self._attempt()

    @on(Input.Submitted, "#lock-confirm")
    def _confirmSubmitted(self) -> None:
        self._attempt()


class ConfirmModal(ModalScreen):
    CSS = APP_CSS

    def __init__(self, message: str) -> None:
        super().__init__()
        self._message = message

    def compose(self) -> ComposeResult:
        with Vertical(id="confirm-wrap"):
            yield Label(self._message, id="confirm-msg")
            with Horizontal(id="confirm-btns"):
                yield Button("Cancel", id="btn-cancel")
                yield Button("Delete", id="btn-ok")

    @on(Button.Pressed, "#btn-ok")
    def _ok(self) -> None:
        self.dismiss(True)

    @on(Button.Pressed, "#btn-cancel")
    def _cancel(self) -> None:
        self.dismiss(False)


class EntryModal(ModalScreen):
    CSS = APP_CSS

    def __init__(
        self,
        title: str,
        service: str = "",
        username: str = "",
        label: str = "",
        password: str = "",
        lockService: bool = False,
    ) -> None:
        super().__init__()
        self._title = title
        self._service = service
        self._username = username
        self._label = label
        self._password = password
        self._lockService = lockService

    def compose(self) -> ComposeResult:
        with Vertical(id="entry-wrap"):
            yield Label(self._title, id="entry-title")
            yield Label("Service", classes="f-label")
            yield Input(
                value=self._service,
                placeholder="e.g. github",
                id="f-service",
                classes="f-input",
                disabled=self._lockService,
            )
            yield Label("Username / Email", classes="f-label")
            yield Input(value=self._username, placeholder="me@example.com", id="f-user", classes="f-input")
            yield Label("Label  (optional)", classes="f-label")
            yield Input(value=self._label, placeholder="work, personal ...", id="f-label-in", classes="f-input")
            yield Label("Password", classes="f-label")
            yield Input(
                value=self._password,
                placeholder="type or generate below",
                password=True,
                id="f-pass",
                classes="f-input",
            )
            yield Button("Generate strong password", id="btn-gen-pw")
            yield Label("", id="gen-preview")
            yield Label("", id="entry-err")
            with Horizontal(id="entry-btns"):
                yield Button("Cancel", id="btn-entry-cancel")
                yield Button("Save",   id="btn-entry-save")

    def on_mount(self) -> None:
        target = "#f-user" if self._lockService else "#f-service"
        self.query_one(target, Input).focus()

    @on(Button.Pressed, "#btn-gen-pw")
    def _generate(self) -> None:
        pw = generatePassword(20, True)
        self.query_one("#f-pass", Input).value = pw
        copied = copyText(pw)
        self.query_one("#gen-preview", Label).update(
            "Generated and copied to clipboard." if copied else "Generated."
        )

    def _save(self) -> None:
        svc  = self.query_one("#f-service",  Input).value.strip().lower()
        user = self.query_one("#f-user",      Input).value.strip()
        lbl  = self.query_one("#f-label-in", Input).value.strip().lower()
        pw   = self.query_one("#f-pass",      Input).value
        err  = self.query_one("#entry-err",   Label)
        if not svc:
            err.update("Service name is required.")
            return
        if not user:
            err.update("Username or email is required.")
            return
        if not pw:
            err.update("Password is required.")
            return
        result: dict = {"service": svc, "username": user, "password": pw}
        if lbl:
            result["label"] = lbl
        self.dismiss(result)

    @on(Button.Pressed, "#btn-entry-save")
    def _btnSave(self) -> None:
        self._save()

    @on(Button.Pressed, "#btn-entry-cancel")
    def _btnCancel(self) -> None:
        self.dismiss(None)

    @on(Input.Submitted)
    def _fieldSubmitted(self, event: Input.Submitted) -> None:
        order = ["#f-service", "#f-user", "#f-label-in", "#f-pass"]
        ids   = [i for i in order if not (i == "#f-service" and self._lockService)]
        cur   = f"#{event.input.id}"
        try:
            idx = ids.index(cur)
            if idx + 1 < len(ids):
                self.query_one(ids[idx + 1], Input).focus()
            else:
                self._save()
        except ValueError:
            self._save()


class EntryCard(Vertical):
    DEFAULT_CSS = APP_CSS

    def __init__(self, svc: str, idx: int, entry: dict) -> None:
        super().__init__()
        self.svc = svc
        self.idx = idx
        self.entry = entry
        self._pwVisible = False

    def compose(self) -> ComposeResult:
        lbl   = self.entry.get("label", "")
        title = f"{self.svc}  ({lbl})" if lbl else self.svc
        yield Label(title, classes="card-svc")
        with Horizontal(classes="card-row"):
            yield Label("username", classes="card-key")
            yield Label(self.entry["username"], classes="card-val")
        with Horizontal(classes="card-row"):
            yield Label("password", classes="card-key")
            yield Label("*" * 14, classes="card-val", id=f"cv-pw-{self.svc}-{self.idx}")
        with Horizontal(classes="card-actions"):
            yield Button("Show",   id=f"cv-show-{self.svc}-{self.idx}", classes="card-btn")
            yield Button("Copy",   id=f"cv-copy-{self.svc}-{self.idx}", classes="card-btn")
            yield Button("Edit",   id=f"cv-edit-{self.svc}-{self.idx}", classes="card-btn")
            yield Button("Delete", id="card-del",                        classes="card-btn -danger")

    def togglePw(self) -> None:
        pwLbl  = self.query_one(f"#cv-pw-{self.svc}-{self.idx}",   Label)
        showBt = self.query_one(f"#cv-show-{self.svc}-{self.idx}", Button)
        self._pwVisible = not self._pwVisible
        if self._pwVisible:
            pwLbl.update(self.entry["password"])
            showBt.label = "Hide"
        else:
            pwLbl.update("*" * 14)
            showBt.label = "Show"


class LockBoxApp(App):
    TITLE = "LockBox"
    CSS   = APP_CSS

    BINDINGS = [
        Binding("n",      "newEntry",    "New"),
        Binding("ctrl+l", "lockVault",   "Lock"),
        Binding("ctrl+f", "focusSearch", "Search", show=False),
        Binding("q",      "lockVault",   "Quit",   show=False),
    ]

    def __init__(self) -> None:
        super().__init__()
        self._master:      str  = ""
        self._data:        dict = {}
        self._filter:      str  = ""
        self._selectedSvc: str  = ""

    def on_mount(self) -> None:
        initMode = not os.path.exists(vaultFile)
        self.push_screen(UnlockScreen(self._afterUnlock, initMode=initMode))

    def _afterUnlock(self, master: str, data: dict) -> None:
        self._master = master
        self._data   = data
        self.pop_screen()
        self._refreshSidebar()
        count = sum(len(v) for v in data.values())
        svcs  = len(data)
        self._setStatus(
            f"{count} entr{'y' if count == 1 else 'ies'} in {svcs} service{'s' if svcs != 1 else ''}"
        )

    def compose(self) -> ComposeResult:
        with Horizontal(id="topbar"):
            yield Static("LockBox", id="topbar-title")
            yield Static("|",       id="topbar-div")
            yield Button("New",      id="btn-new")
            yield Button("Generate", id="btn-gen")
            yield Button("Lock",     id="btn-lock")
            yield Input(placeholder="Search...", id="search")
        with Horizontal(id="layout"):
            with Vertical(id="sidebar"):
                yield Static("  Services", id="sidebar-hd")
                yield ListView(id="svc-list")
            with Vertical(id="detail"):
                yield ScrollableContainer(id="detail-scroll")
        yield Static("  Ready", id="statusbar")

    @on(Button.Pressed, "#btn-new")
    def _btnNew(self) -> None:
        self.action_newEntry()

    @on(Button.Pressed, "#btn-gen")
    def _btnGen(self) -> None:
        pw     = generatePassword(20, True)
        copied = copyText(pw)
        note   = "copied" if copied else "clipboard unavailable"
        self._setStatus(f"Generated: {pw}  ({note})")

    @on(Button.Pressed, "#btn-lock")
    def _btnLock(self) -> None:
        self.action_lockVault()

    @on(Input.Changed, "#search")
    def _search(self, event: Input.Changed) -> None:
        self._filter = event.value
        self._refreshSidebar()

    def _refreshSidebar(self) -> None:
        lv       = self.query_one("#svc-list", ListView)
        filt     = self._filter.strip().lower()
        services = sorted(k for k in self._data if filt in k)
        lv.clear()
        for svc in services:
            count = len(self._data[svc])
            badge = f"  [{count}]" if count > 1 else ""
            lv.append(ListItem(Label(f"  {svc}{badge}"), id=f"svc-{svc}"))
        if not self._selectedSvc and services:
            self._selectedSvc = services[0]
        if self._selectedSvc in self._data:
            self._renderDetail(self._selectedSvc)
        else:
            self._renderEmpty()

    def _renderDetail(self, svc: str) -> None:
        scroll = self.query_one("#detail-scroll", ScrollableContainer)
        scroll.remove_children()
        for i, entry in enumerate(self._data.get(svc, [])):
            scroll.mount(EntryCard(svc, i, entry))

    def _renderEmpty(self) -> None:
        scroll = self.query_one("#detail-scroll", ScrollableContainer)
        scroll.remove_children()
        scroll.mount(Static(
            "\n\n  No entries yet.\n  Press [bold]N[/bold] or New to add one.",
            classes="empty-hint",
        ))

    @on(ListView.Selected, "#svc-list")
    def _svcSelected(self, event: ListView.Selected) -> None:
        raw = event.item.id or ""
        if raw.startswith("svc-"):
            svc = raw[4:]
            self._selectedSvc = svc
            self._renderDetail(svc)

    @on(Button.Pressed)
    def _cardButtons(self, event: Button.Pressed) -> None:
        btnId: str = event.button.id or ""

        if btnId.startswith("cv-show-"):
            svc, idx = self._parseCardId(btnId[len("cv-show-"):])
            card = self._findCard(svc, idx)
            if card:
                card.togglePw()
            event.stop()

        elif btnId.startswith("cv-copy-"):
            svc, idx = self._parseCardId(btnId[len("cv-copy-"):])
            entries  = self._data.get(svc, [])
            if idx < len(entries):
                ok = copyText(entries[idx]["password"])
                self._setStatus(f"Password for '{svc}' copied." if ok else "Clipboard unavailable.")
            event.stop()

        elif btnId.startswith("cv-edit-"):
            svc, idx = self._parseCardId(btnId[len("cv-edit-"):])
            entries  = self._data.get(svc, [])
            if idx < len(entries):
                e = entries[idx]
                self.push_screen(
                    EntryModal(
                        title=f"Edit  {svc}",
                        service=svc,
                        username=e["username"],
                        label=e.get("label", ""),
                        password=e["password"],
                        lockService=True,
                    ),
                    callback=lambda res, s=svc, i=idx: self._saveEdit(s, i, res),
                )
            event.stop()

        elif btnId == "card-del":
            targetCard = None
            for node in event.button.ancestors_with_self:
                if isinstance(node, EntryCard):
                    targetCard = node
                    break
            if targetCard:
                lbl  = targetCard.entry.get("label", "")
                name = f"{targetCard.svc} ({lbl})" if lbl else targetCard.svc
                self.push_screen(
                    ConfirmModal(f"Delete '{name}'?"),
                    callback=lambda ok, s=targetCard.svc, i=targetCard.idx: self._doDelete(s, i, bool(ok)),
                )
            event.stop()

    def _parseCardId(self, rest: str) -> tuple[str, int]:
        parts = rest.rsplit("-", 1)
        return parts[0], int(parts[1])

    def _findCard(self, svc: str, idx: int) -> EntryCard | None:
        for card in self.query(EntryCard):
            if card.svc == svc and card.idx == idx:
                return card
        return None

    def action_newEntry(self) -> None:
        self.push_screen(EntryModal(title="New Entry"), callback=self._saveNew)

    def action_lockVault(self) -> None:
        self._master      = ""
        self._data        = {}
        self._selectedSvc = ""
        self._filter      = ""
        try:
            self.query_one("#svc-list",      ListView).clear()
            self.query_one("#detail-scroll", ScrollableContainer).remove_children()
            self.query_one("#search",        Input).value = ""
        except Exception:
            pass
        initMode = not os.path.exists(vaultFile)
        self.push_screen(UnlockScreen(self._afterUnlock, initMode=initMode))

    def action_focusSearch(self) -> None:
        self.query_one("#search", Input).focus()

    def _saveNew(self, result: dict | None) -> None:
        if result is None:
            return
        svc   = result["service"]
        entry: dict = {"username": result["username"], "password": result["password"]}
        lbl   = result.get("label", "")
        if lbl:
            entry["label"] = lbl
        self._data.setdefault(svc, []).append(entry)
        saveVault(self._master, self._data)
        self._selectedSvc = svc
        self._refreshSidebar()
        self._setStatus(f"Saved '{svc}'.")

    def _saveEdit(self, svc: str, idx: int, result: dict | None) -> None:
        if result is None:
            return
        entry = self._data[svc][idx]
        entry["username"] = result["username"]
        entry["password"] = result["password"]
        lbl = result.get("label", "")
        if lbl:
            entry["label"] = lbl
        elif "label" in entry:
            del entry["label"]
        saveVault(self._master, self._data)
        self._refreshSidebar()
        self._renderDetail(svc)
        self._setStatus(f"Updated '{svc}'.")

    def _doDelete(self, svc: str, idx: int, ok: bool) -> None:
        if not ok:
            return
        entries = self._data.get(svc, [])
        if idx < len(entries):
            entries.pop(idx)
        if not entries:
            del self._data[svc]
            self._selectedSvc = ""
        else:
            self._data[svc] = entries
        saveVault(self._master, self._data)
        self._refreshSidebar()
        if self._selectedSvc and self._selectedSvc in self._data:
            self._renderDetail(self._selectedSvc)
        else:
            self._renderEmpty()
        self._setStatus(f"Deleted from '{svc}'.")

    def _setStatus(self, msg: str) -> None:
        try:
            self.query_one("#statusbar", Static).update(f"  {msg}")
        except Exception:
            pass
