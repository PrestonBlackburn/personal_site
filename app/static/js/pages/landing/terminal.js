    const nordTheme = {
        foreground: "#9ECE6A",
        background: "rgba(41,46,63,0.0)",
        cursor: "#9ECE6A",
        selection: "rgba(136,192,208,0.3)",

        black:   "#3B4252",
        red:     "#BF616A",
        green:   "#A3BE8C",
        yellow:  "#EBCB8B",
        blue:    "#81A1C1",
        magenta: "#B48EAD",
        cyan:    "#88C0D0",
        white:   "#9ECE6A",

        brightBlack:   "#4C566A",
        brightRed:     "#BF616A",
        brightGreen:   "#A3BE8C",
        brightYellow:  "#EBCB8B",
        brightBlue:    "#81A1C1",
        brightMagenta: "#B48EAD",
        brightCyan:    "#8FBCBB",
        brightWhite:   "#ECEFF4"
        };

    const term = new Terminal({ 
        cursorBlink: true, 
        convertEol: true, 
        theme: nordTheme,
        scrollback: 0   // disables scrollback buffer
    });
    const fit = new FitAddon.FitAddon(); // note the namespace
    term.loadAddon(fit);
    term.open(document.getElementById("terminal"));
    fit.fit();


    const PROMPT = "preston@blackburn:~$ ";
    let buffer = "";

    function prompt() {
        term.write("\r\n" + PROMPT);
        buffer = "";
    }

    // Initial prompt
    term.writeln("try running `help` for more info");
    prompt();


    term.onData(data => {
        if (data === "\x1b[A" || data === "\x1b[B" || data === "\x1b[C" || data === "\x1b[D") {
            return; // skip up/down/left/right arrows
        }

        for (const ch of data) {
        if (ch === "\r") {
            // Enter pressed → echo back
            term.writeln("");
            handleCommand(buffer.trim());
            prompt();
        } else if (ch === "\u007F") {
            // Backspace
            if (buffer.length > 0) {
            buffer = buffer.slice(0, -1);
            term.write("\b \b");
            }
        } else {
            buffer += ch;
            term.write(ch);
        }
        }
    });

    function handleCommand(cmdLine) {
        if (cmdLine.length === 0) return;

        const [cmd, ...args] = cmdLine.split(/\s+/);

        switch (cmd) {
            case "help":
            term.writeln("Available commands:");
            term.writeln("  ls                - list pages and blogs");
            term.writeln("  ls blogs          - list blogs");
            term.writeln("  ls pages          - list blogs");
            term.writeln("  goto <page>        - go to tab (ex: goto 'videos')");
            term.writeln("  goto blog <blog>  - go to blog (ex: goto 'Example Blog')");
            term.writeln("  echo <text>       - echo arguments");
            term.writeln("  clear             - clear the terminal");
            term.writeln("  help              - show this help");
            break;

            case "clear":
            term.clear();
            break;


            case "ls":
            term.writeln("'Blog title a' 'Blog title b'");
            break;

            case "goto":
            if (args.length === 0) {
                term.writeln("Usage: goto <target>");
            } else {
                const target = args.join(" "); // <-- join all parts back
                // You can implement your custom logic here
                if (target === "'Blog title a'" || target === "Blog title a") {
                term.writeln("Navigating to 'Blog title a'...");
                setTimeout(() => {
                    term.write(".");
                }, 150);
                setTimeout(() => {
                    term.write(".");
                }, 300);
                setTimeout(() => {
                    term.write(".\r\n"); // finish with newline
                    // then actually navigate to the new tab
                    // Example: window.location.href = `/blog/${encodeURIComponent(target)}`;
                }, 500);
                // e.g. trigger navigation in your app:
                // window.location.href = `/blog/${target}`;
                } else {
                term.writeln(`Unknown target: ${target}`);
                }
            }
            break;


            case "echo":
            term.writeln(args.join(" "));
            break;

            default:
            term.writeln(`${cmd}: command not found`);
        }
        }

    // refit on resize
    addEventListener("resize", () => fit.fit());