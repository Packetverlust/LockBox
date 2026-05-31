from __future__ import annotations

import getpass
import os

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.rule import Rule
from rich.prompt import Prompt
from rich import box

from lockbox import __version__
from lockbox.vault import loadVault, saveVault, vaultFile, firstRun
from lockbox.generator import generatePassword
from lockbox.docs import (
    DOCS_INDEX,
    DOCS_OVERVIEW,
    DOCS_COMMANDS,
    DOCS_USAGE,
    DOCS_ADVANCED,
    DOCS_SECURITY,
)


app = typer.Typer(
    add_completion=False,
    no_args_is_help=False,
    pretty_exceptions_enable=False,
    context_settings={"help_option_names": []},
)
console = Console()


def askMasterPw(prompt: str = "Master password") -> str:
    return Prompt.ask(f"  [dim]{prompt}[/dim]", password=True, console=console)


def openVault(masterPw: str) -> dict:
    data = loadVault(masterPw)
    if data is None:
        console.print(Panel(
            "[red]Wrong master password or vault is corrupted.[/red]",
            border_style="red", box=box.ROUNDED,
        ))
        raise typer.Exit(1)
    return data


def printFirstRun() -> None:
    console.print()
    console.print(Rule("[bold yellow]  FIRST TIME SETUP  [/bold yellow]", style="yellow", characters="━"))
    console.print(Panel(
        "  [bold white]Not sure where to start?[/bold white]\n\n"
        "     Run [bold cyan]lockbox ui[/bold cyan], it opens a visual interface where you\n"
        "     can create your vault and manage passwords [bold]without any commands[/bold].\n\n"
        "  [dim]Already know your way around? Use [cyan]lockbox init[/cyan] to set up via CLI.[/dim]",
        border_style="yellow",
        box=box.HEAVY,
    ))
    console.print(Rule(style="yellow", characters="━"))
    console.print()


def checkVault() -> None:
    if not os.path.exists(vaultFile):
        if firstRun():
            printFirstRun()
        else:
            console.print(Panel(
                "[yellow]No vault found.[/yellow]\n\n"
                "Run [bold cyan]lockbox init[/bold cyan] to create one via the CLI,\n"
                "or [bold cyan]lockbox ui[/bold cyan] to set it up visually.",
                title="LockBox", border_style="yellow", box=box.ROUNDED,
            ))
        raise typer.Exit(1)


def header(title: str) -> None:
    console.print(Rule(f"[bold cyan]LockBox[/bold cyan]  [dim]{title}[/dim]", style="bright_black"))


def silentCopy(text: str) -> bool:
    try:
        import pyperclip
        pyperclip.copy(text)
        return True
    except Exception:
        return False


def printHelp() -> None:
    console.print()
    console.print(Rule("[bold cyan]LockBox[/bold cyan]", style="bright_black"))

    if firstRun():
        printFirstRun()

    opts = Table(show_header=False, box=None, pad_edge=False, padding=(0, 2))
    opts.add_column("Option", style="cyan", no_wrap=True)
    opts.add_column("Description", style="dim")
    opts.add_row("--version", "Show version and exit.")
    opts.add_row("--help",    "Show this message and exit.")
    console.print(Panel(opts, title="[bold]Options[/bold]", border_style="bright_black", box=box.ROUNDED))

    cmds = Table(show_header=False, box=None, pad_edge=False, padding=(0, 2))
    cmds.add_column("Command", style="cyan", no_wrap=True)
    cmds.add_column("Description")
    cmds.add_row("init",         "Create a new encrypted vault.")
    cmds.add_row("add",          "Save a password (existing or new account).")
    cmds.add_row("get",          "Look up a saved entry by service name.")
    cmds.add_row("list",         "Show all saved entries.")
    cmds.add_row("update",       "Change the username or password for an entry.")
    cmds.add_row("delete",       "Remove an entry from the vault.")
    cmds.add_row("generate",     "Generate a strong password without saving it.")
    cmds.add_row("changemaster", "Change the master password.")
    cmds.add_row("docs",         "View documentation inside the CLI.")
    cmds.add_row("ui",           "Open the interactive TUI.")
    console.print(Panel(cmds, title="[bold]Commands[/bold]", border_style="bright_black", box=box.ROUNDED))
    console.print()


@app.callback(invoke_without_command=True)
def root(
    ctx: typer.Context,
    version: bool = typer.Option(False, "--version", is_eager=True),
    help: bool = typer.Option(False, "--help", is_eager=True),
) -> None:
    if version:
        console.print(f"[cyan]lockbox[/cyan] [bold]{__version__}[/bold]")
        raise typer.Exit(0)
    if help or ctx.invoked_subcommand is None:
        printHelp()
        raise typer.Exit(0)


@app.command()
def init() -> None:
    if os.path.exists(vaultFile):
        header("init")
        console.print(Panel("[yellow]A vault already exists.[/yellow]", border_style="yellow", box=box.ROUNDED))
        return
    header("init")
    console.print("[dim]Choose a master password. You will need it every time you use LockBox.[/dim]\n")
    pw = askMasterPw("Create master password")
    confirm = askMasterPw("Confirm master password")
    if pw != confirm:
        console.print(Panel("[red]Passwords do not match.[/red]", border_style="red", box=box.ROUNDED))
        raise typer.Exit(1)
    saveVault(pw, {})
    console.print(Panel(
        "[green]Vault created.[/green] You can now add entries with [bold cyan]lockbox add[/bold cyan].",
        border_style="green", box=box.ROUNDED,
    ))


@app.command()
def add(
    service: str = typer.Argument(..., help="Service name, e.g. github or netflix."),
    username: str = typer.Option("", "--username", "-u", metavar="EMAIL_OR_USER", help="Username or email for this account."),
    email: str = typer.Option("", "--email", "-e", metavar="EMAIL", help="Alias for --username."),
    label: str = typer.Option("", "--label", help="Label to tell accounts apart, e.g. 'work' or 'personal'."),
    generate: bool = typer.Option(False, "--generate", "-g", help="Auto-generate a strong password instead of typing one."),
    password_length: int = typer.Option(20, "--password-length", "-l", help="Length of the auto-generated password."),
    no_symbols: bool = typer.Option(False, "--no-symbols", help="Letters and numbers only, no special characters."),
) -> None:
    checkVault()
    header(f"add  [bold]{service}[/bold]")
    masterPw = askMasterPw()
    data = openVault(masterPw)

    svc = service.lower()
    lbl = label.strip().lower()
    existing = data.get(svc, [])

    resolvedUser = username or email

    if lbl:
        if any(e.get("label", "") == lbl for e in existing):
            console.print(Panel(
                f"[yellow]An entry for '{svc}' with label '{lbl}' already exists.[/yellow]\n"
                f"Use [bold cyan]lockbox update {svc} --label {lbl}[/bold cyan] to change it.",
                border_style="yellow", box=box.ROUNDED,
            ))
            return
    elif existing:
        console.print(Panel(
            f"[dim]There is already {len(existing)} account(s) saved for '{svc}'.[/dim]\n"
            f"Use [bold]--label[/bold] to add another one, e.g. [cyan]--label personal[/cyan] or [cyan]--label work[/cyan].\n"
            f"Or use [bold cyan]lockbox update {svc}[/bold cyan] to edit the existing entry.",
            border_style="bright_black", box=box.ROUNDED,
        ))
        return

    console.print()
    uname = resolvedUser or Prompt.ask("  [dim]Username or email[/dim]", console=console)

    if generate:
        pw = generatePassword(password_length, not no_symbols)
        copied = silentCopy(pw)
        copyNote = "  [green]✓ copied to clipboard[/green]" if copied else "  [yellow]clipboard unavailable[/yellow]"
        console.print(Panel(
            f"[bold cyan]{pw}[/bold cyan]\n{copyNote}",
            title="[bold]Generated Password[/bold]",
            subtitle=f"[dim]{password_length} characters{'  no symbols' if no_symbols else ''}[/dim]",
            border_style="bright_black", box=box.ROUNDED,
        ))
    else:
        console.print("  [dim]Tip: use [bold]--generate[/bold] if you want LockBox to create a password for you.[/dim]")
        pw = askMasterPw("Your existing password")
        confirm = askMasterPw("Confirm password")
        if pw != confirm:
            console.print(Panel("[red]Passwords do not match.[/red]", border_style="red", box=box.ROUNDED))
            raise typer.Exit(1)

    entry: dict = {"username": uname, "password": pw}
    if lbl:
        entry["label"] = lbl

    existing.append(entry)
    data[svc] = existing
    saveVault(masterPw, data)

    displayName = f"{svc}  [dim]({lbl})[/dim]" if lbl else svc
    console.print(Panel(f"[green]Saved[/green] {displayName}", border_style="green", box=box.ROUNDED))


@app.command()
def get(
    service: str = typer.Argument(..., help="Service name, e.g. github."),
    label: str = typer.Option("", "--label", help="Which account to show if there are multiple."),
    show_password: bool = typer.Option(False, "--show-password", "-s", help="Reveal the password in plain text."),
    copy_password: bool = typer.Option(False, "--copy-password", "-c", help="Copy the password to your clipboard."),
) -> None:
    checkVault()
    header(f"get  [bold]{service}[/bold]")
    masterPw = askMasterPw()
    data = openVault(masterPw)

    svc = service.lower()
    entries = data.get(svc)
    if not entries:
        console.print(Panel(f"[red]No entry found for '{svc}'.[/red]", border_style="red", box=box.ROUNDED))
        return

    lbl = label.strip().lower()
    if lbl:
        entries = [e for e in entries if e.get("label", "") == lbl]
        if not entries:
            console.print(Panel(
                f"[red]No entry for '{svc}' with label '{lbl}'.[/red]",
                border_style="red", box=box.ROUNDED,
            ))
            return

    for entry in entries:
        t = Table(show_header=False, box=None, pad_edge=False, padding=(0, 2))
        t.add_column("Key", style="dim", no_wrap=True)
        t.add_column("Value", style="bold")
        t.add_row("Service", svc)
        if entry.get("label"):
            t.add_row("Label", entry["label"])
        t.add_row("Username", entry["username"])

        if show_password:
            t.add_row("Password", f"[cyan]{entry['password']}[/cyan]")
        elif copy_password:
            t.add_row("Password", "[dim]copied to clipboard[/dim]")
        else:
            t.add_row("Password", "[dim]hidden  (--show-password or --copy-password)[/dim]")

        panelTitle = f"{svc} ({entry['label']})" if entry.get("label") else svc
        console.print(Panel(t, title=f"[bold]{panelTitle}[/bold]", border_style="bright_black", box=box.ROUNDED))

    if copy_password:
        if silentCopy(entries[0]["password"]):
            console.print("[green]Password copied to clipboard.[/green]")
        else:
            console.print("[yellow]Clipboard unavailable.[/yellow] Use [bold]--show-password[/bold] instead.")


@app.command(name="list")
def listEntries(
    show_passwords: bool = typer.Option(False, "--show-passwords", "-s", help="Reveal all passwords."),
) -> None:
    checkVault()
    header("list")
    masterPw = askMasterPw()
    data = openVault(masterPw)

    if not data:
        console.print(Panel(
            "[dim]Vault is empty.[/dim]\n\nAdd your first entry with [bold cyan]lockbox add <service>[/bold cyan].",
            border_style="bright_black", box=box.ROUNDED,
        ))
        return

    t = Table(show_header=True, header_style="bold", box=box.SIMPLE, padding=(0, 1))
    t.add_column("Service",  style="cyan",   no_wrap=True)
    t.add_column("Label",    style="dim",    no_wrap=True)
    t.add_column("Username", style="white")
    if show_passwords:
        t.add_column("Password", style="yellow")

    totalEntries = 0
    for svc, entries in sorted(data.items()):
        for entry in entries:
            lbl = entry.get("label", "")
            if show_passwords:
                t.add_row(svc, lbl, entry["username"], entry["password"])
            else:
                t.add_row(svc, lbl, entry["username"])
            totalEntries += 1

    totalServices = len(data)
    subtitle = f"{totalEntries} account(s) across {totalServices} service(s)"
    if show_passwords:
        subtitle += "  [yellow]passwords visible[/yellow]"
    console.print(Panel(
        t,
        title="[bold]Vault[/bold]",
        subtitle=f"[dim]{subtitle}[/dim]",
        border_style="bright_black",
        box=box.ROUNDED,
    ))


@app.command()
def update(
    service: str = typer.Argument(..., help="Service name."),
    label: str = typer.Option("", "--label", help="Which account to update if there are multiple."),
    username: str = typer.Option("", "--username", "-u", metavar="EMAIL_OR_USER", help="Set a new username or email."),
    email: str = typer.Option("", "--email", "-e", metavar="EMAIL", help="Alias for --username."),
    new_password: bool = typer.Option(False, "--new-password", "-p", help="Type a new password interactively."),
    generate: bool = typer.Option(False, "--generate", "-g", help="Auto-generate a new strong password."),
    password_length: int = typer.Option(20, "--password-length", "-l", help="Length of the auto-generated password."),
    no_symbols: bool = typer.Option(False, "--no-symbols", help="Letters and numbers only, no special characters."),
) -> None:
    checkVault()
    header(f"update  [bold]{service}[/bold]")
    masterPw = askMasterPw()
    data = openVault(masterPw)

    svc = service.lower()
    if svc not in data:
        console.print(Panel(
            f"[red]No entry found for '{svc}'.[/red]\nUse [bold cyan]lockbox add {svc}[/bold cyan] to create one.",
            border_style="red", box=box.ROUNDED,
        ))
        return

    entries = data[svc]
    lbl = label.strip().lower()

    if len(entries) > 1 and not lbl:
        t = Table(show_header=True, header_style="bold", box=box.SIMPLE)
        t.add_column("Label", style="cyan")
        t.add_column("Username")
        for e in entries:
            t.add_row(e.get("label", "[dim]no label[/dim]"), e["username"])
        console.print(Panel(t, title=f"Multiple accounts for '{svc}'", border_style="yellow", box=box.ROUNDED))
        console.print("[yellow]Use --label to specify which one to update.[/yellow]")
        return

    entry = next((e for e in entries if e.get("label", "") == lbl), entries[0]) if lbl else entries[0]

    if lbl and entry.get("label", "") != lbl:
        console.print(Panel(f"[red]No entry for '{svc}' with label '{lbl}'.[/red]", border_style="red", box=box.ROUNDED))
        return

    resolvedUser = username or email
    if resolvedUser:
        entry["username"] = resolvedUser

    if generate:
        pw = generatePassword(password_length, not no_symbols)
        entry["password"] = pw
        copied = silentCopy(pw)
        copyNote = "  [green]✓ copied to clipboard[/green]" if copied else "  [yellow]clipboard unavailable[/yellow]"
        console.print(Panel(
            f"[bold cyan]{pw}[/bold cyan]\n{copyNote}",
            title="[bold]Generated Password[/bold]",
            subtitle=f"[dim]{password_length} characters{'  no symbols' if no_symbols else ''}[/dim]",
            border_style="bright_black", box=box.ROUNDED,
        ))
    elif new_password:
        pw = askMasterPw("New password")
        confirm = askMasterPw("Confirm new password")
        if pw != confirm:
            console.print(Panel("[red]Passwords do not match.[/red]", border_style="red", box=box.ROUNDED))
            raise typer.Exit(1)
        entry["password"] = pw

    saveVault(masterPw, data)
    displayName = f"{svc} ({lbl})" if lbl else svc
    console.print(Panel(f"[green]Updated[/green] {displayName}", border_style="green", box=box.ROUNDED))


@app.command()
def delete(
    service: str = typer.Argument(..., help="Service name."),
    label: str = typer.Option("", "--label", help="Which account to delete if there are multiple."),
    confirm: bool = typer.Option(False, "--confirm", "-y", help="Skip the confirmation prompt."),
) -> None:
    checkVault()
    header(f"delete  [bold]{service}[/bold]")
    masterPw = askMasterPw()
    data = openVault(masterPw)

    svc = service.lower()
    if svc not in data:
        console.print(Panel(f"[red]No entry found for '{svc}'.[/red]", border_style="red", box=box.ROUNDED))
        return

    entries = data[svc]
    lbl = label.strip().lower()

    if len(entries) > 1 and not lbl:
        t = Table(show_header=True, header_style="bold", box=box.SIMPLE)
        t.add_column("Label", style="cyan")
        t.add_column("Username")
        for e in entries:
            t.add_row(e.get("label", "[dim]no label[/dim]"), e["username"])
        console.print(Panel(t, title=f"Multiple accounts for '{svc}'", border_style="yellow", box=box.ROUNDED))
        console.print("[yellow]Use --label to specify which one to delete.[/yellow]")
        return

    if lbl:
        remaining = [e for e in entries if e.get("label", "") != lbl]
        if len(remaining) == len(entries):
            console.print(Panel(f"[red]No entry for '{svc}' with label '{lbl}'.[/red]", border_style="red", box=box.ROUNDED))
            return
        target = f"'{svc}' (label: {lbl})"
    else:
        remaining = []
        target = f"all accounts for '{svc}'"

    if not confirm:
        ok = typer.confirm(f"  Delete {target}?", default=False)
        if not ok:
            console.print("[dim]Cancelled.[/dim]")
            return

    if remaining:
        data[svc] = remaining
    else:
        del data[svc]

    saveVault(masterPw, data)
    console.print(Panel(f"[green]Deleted[/green] {target}", border_style="green", box=box.ROUNDED))


@app.command()
def generate(
    length: int = typer.Option(20, "--length", "-l", help="How many characters long."),
    no_symbols: bool = typer.Option(False, "--no-symbols", help="Letters and numbers only, no special characters."),
    copy_password: bool = typer.Option(False, "--copy-password", "-c", help="Copy the result to your clipboard."),
) -> None:
    header("generate")
    pw = generatePassword(length, not no_symbols)
    console.print(Panel(
        f"[bold cyan]{pw}[/bold cyan]",
        title="[bold]Generated Password[/bold]",
        subtitle=f"[dim]{length} characters{'  no symbols' if no_symbols else ''}[/dim]",
        border_style="bright_black",
        box=box.ROUNDED,
    ))
    if copy_password:
        if silentCopy(pw):
            console.print("[green]Copied to clipboard.[/green]")
        else:
            console.print("[yellow]Clipboard unavailable.[/yellow]")


@app.command()
def changemaster() -> None:
    checkVault()
    header("changemaster")
    console.print("[dim]This will re-encrypt your entire vault with a new master password.[/dim]\n")
    masterPw = askMasterPw("Current master password")
    data = openVault(masterPw)

    newPw = askMasterPw("New master password")
    confirm = askMasterPw("Confirm new master password")
    if newPw != confirm:
        console.print(Panel("[red]Passwords do not match.[/red]", border_style="red", box=box.ROUNDED))
        raise typer.Exit(1)

    saveVault(newPw, data)
    console.print(Panel("[green]Master password updated.[/green]", border_style="green", box=box.ROUNDED))


@app.command()
def docs(
    topic: str = typer.Argument("index", help="overview | commands | usage | advanced | security"),
) -> None:
    topics = {
        "index":    DOCS_INDEX,
        "overview": DOCS_OVERVIEW,
        "commands": DOCS_COMMANDS,
        "usage":    DOCS_USAGE,
        "advanced": DOCS_ADVANCED,
        "security": DOCS_SECURITY,
    }
    content = topics.get(topic.strip().lower())
    if content is None:
        console.print(Panel(
            f"[red]Unknown topic '{topic}'.[/red]\n\nAvailable: overview, commands, usage, advanced, security",
            border_style="red", box=box.ROUNDED,
        ))
        raise typer.Exit(1)
    header(f"docs  [dim]{topic}[/dim]")
    console.print(Panel(content.strip(), border_style="bright_black", box=box.ROUNDED))


@app.command()
def ui() -> None:
    try:
        from lockbox.tui import LockBoxApp
    except ImportError:
        console.print(Panel(
            "[red]Textual is not installed.[/red]\n\nRun: [bold cyan]pip install textual[/bold cyan]",
            border_style="red", box=box.ROUNDED,
        ))
        raise typer.Exit(1)
    LockBoxApp().run()


def main() -> None:
    app()


if __name__ == "__main__":
    main()
