"""This file encapsulates logic to working with helix editor.""" 

import sys

from .cfg import console

def open_editor_unix(file_path: str) -> list[str] | None:
    from pyntercept.processes.process import PTYProcess
    from pyntercept.renderers.unixRenderer import UnixRenderer
    
    res: list[str] = []
    
    def on_in_upd(data: bytes) -> bytes:        
        res.append(data.decode() + '\n')
        return data
    
    with PTYProcess(
        ['hx', file_path], 
        UnixRenderer(dest_raw=False),
        src_transforms=[on_in_upd]
    ) as pty_process:
        while pty_process.update():
            pass
    
    return res


def open_editor_legacy(file_path: str) -> list[str] | None:
    import subprocess
    
    res: list[str] = []
    
    subprocess.run(["hx", file_path])

    return res


def open_editor(file_path: str) -> list[str] | None:
    """Opens the file in Helix editor."""
    
    try:
        if sys.platform in ['linux', 'darwin', 'freebsd', 'android', 'ios', 'cygwin']:
            return open_editor_unix(file_path)
        else:
            return open_editor_legacy(file_path)
    except FileNotFoundError:
        console.print("[red]Error: Helix editor ('hx') not found. Please install Helix.[/red]")
    except Exception as e:
        console.print("[red]An error ocurred!\n" +
            f"Please information below to the developers: https://github.com/Jarrlist/LeetHelix/issues[/red]\n{e}"
        )