"""This file encapsulates logic to working with helix editor.""" 

import sys
import subprocess

from .cfg import console

def open_editor(file_path) -> list | None:
    """Opens the file in Helix editor."""
    
    input_data = []
    

    if sys.platform in ['linux']:
        from pyntercept.process import PTYProcess
        from pyntercept.draw import draw_data
        from pyntercept.tty_utils import enter_raw_mode, exit_raw_mode, switch_echo
        
        stdin_fd = sys.stdin.fileno()
        stdout_fd = sys.stdin.fileno()
        
        def on_in_upd(process: PTYProcess) -> bytes:
            data = process.on_in_fd_upd()
            input_data.append(data)
            
            return data
        
        def on_out_upd(process: PTYProcess) -> bytes:
            data = process.on_out_fd_upd()
            draw_data(data, stdout_fd)
            
            return data
        try:
            switch_echo(stdin_fd, False)
            old_stdin = enter_raw_mode(stdin_fd)
            old_stdout = enter_raw_mode(stdout_fd)
            
            pty_process = PTYProcess(
                ['hx', file_path], 
                in_upd_callback=on_in_upd,
                out_upd_callback=on_out_upd
            )
            
            draw_data(pty_process.on_out_fd_upd())
            
            while pty_process.update(): 
                pass
        except OSError: # this happens when child process dies
            pass
        except FileNotFoundError:
            console.print("[red]Error: Helix editor ('hx') not found. Please install Helix.[/red]")
        except Exception as e:
            console.print(f"[yellow]Error opening the challenge from {file_path}![/yellow] {e}")
        finally:
            exit_raw_mode(stdin_fd, old_stdin)
            exit_raw_mode(stdout_fd, old_stdout)
            switch_echo(stdin_fd, True)
    else:
        try:
            subprocess.run(["hx", file_path])
        except FileNotFoundError:
            console.print("[red]Error: Helix editor ('hx') not found. Please install Helix.[/red]")
        except Exception as e:
            console.print(f"[yellow]Error opening the challenge from {file_path}![/yellow] {e}")
        
    
    return input_data