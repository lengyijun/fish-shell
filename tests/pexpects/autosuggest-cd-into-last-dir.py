#!/usr/bin/env python3
from pexpect_helper import SpawnedProc

# Verify follow-up autosuggestions based on the previously executed command.
# After running e.g. `mkdir foo`, the next empty prompt autosuggests `cd foo`.
sp = SpawnedProc()
send, sendline, sleep, expect_prompt, expect_re, expect_str = (
    sp.send,
    sp.sendline,
    sp.sleep,
    sp.expect_prompt,
    sp.expect_re,
    sp.expect_str,
)
expect_prompt()

# Bind a key to accept the whole autosuggestion (Ctrl+g).
sendline("bind \\cg accept-autosuggestion")
expect_prompt()


def expect_followup(run_cmd, expected):
    # Run a command, then check the autosuggestion on the next empty prompt.
    sendline(run_cmd)
    expect_prompt()
    # Give the debounced autosuggestion time to compute on the empty prompt.
    sleep(1.0)
    # Accept the autosuggestion with Ctrl+g.
    send("\x07")
    # Move to the start and kill the line so the killed text is echoed to the tty.
    send("\x01\x0b")
    expect_str(expected)


expect_followup("mkdir foo", "cd foo")
expect_followup("touch bar.txt", "vi bar.txt")
expect_followup("cargo new mycrate", "cd mycrate")
expect_followup("git clone https://github.com/foo/bar.git", "cd bar.git")
expect_followup("rustfmt x.rs", "rustc x.rs")
expect_followup("gcc a.c", "./a.out")

# The command line is empty after the kill above; press Enter on the empty line
# and confirm we get a clean prompt.
sendline("")
expect_prompt()
