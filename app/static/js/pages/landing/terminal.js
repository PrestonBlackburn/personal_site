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
    scrollback: 1000   // disables scrollback buffer
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

let blogsCache = [];

function handleCommand(cmdLine) {
    if (cmdLine.length === 0) return;

    const [cmd, subcmd, ...args] = cmdLine.trim().split(/\s+/);

    switch (cmd) {
        case "help":
        term.writeln("Available commands:");
        term.writeln("  ls                - list pages and blogs");
        term.writeln("  ls blogs          - list blogs");
        term.writeln("  ls pages          - list pages");
        term.writeln("  goto page <page>  - go to tab (ex: goto page 'videos')");
        term.writeln("  goto blog <blog>  - go to blog (ex: goto blog 'Example Blog' or goto blog 1)");
        term.writeln("  echo <text>       - echo arguments");
        term.writeln("  clear             - clear the terminal");
        term.writeln("  home              - go home");
        term.writeln("  help              - show this help");

        break;

        case "clear":
        term.clear();
        break;

        case "home":
            try {
            term.writeln(`Navigating to home...`);
            setTimeout(() => {
                term.write(".");
            }, 150);
            setTimeout(() => {
                term.write(".");
            }, 300);
            setTimeout(() => {
                term.write(".\r\n"); // finish with newline
                // then actually navigate to the new tab
                window.location.href = "/";
            }, 500);
            // e.g. trigger navigation in your app:
            // window.location.href = `/blog/${target}`;
            } catch (e) {
            term.writeln(`Oops something went wrong, just type in / in the url bar!`);
            prompt();
            };
        break;

        case "ls":
            if (subcmd === "pages") {
                fetch("/api/v1/pages").then(r=> r.json()).then(pages => {
                    term.writeln("\n");
                    term.writeln(pages.pages.join("\n"));
                    prompt();
                }).catch(err => {
                    term.writeln(`Error fetching pages. ${err}`);
                });
                return;
            } else if (subcmd === "blogs") {
                fetch("/api/v1/blogs").then(r=> r.json()).then(blogs => {
                    blogsCache = blogs.blogs;
                    term.writeln("\n");
                    blogs.blogs.forEach((b, i) => {
                        term.writeln(`  ${i+1}. ${b}`);
                    });
                    // term.writeln(blogs.blogs.join("\n"));
                    prompt();
                }).catch(err => {
                    term.writeln(`Error fetching blogs. ${err}`);
                    prompt();
                });
                return;
            } else {
                Promise.all([
                    fetch("/api/v1/pages").then(r => r.json()),
                    fetch("/api/v1/blogs").then(r => r.json())
                ]).then(([pages, blogs]) => {
                    blogsCache = blogs.blogs;
                    term.writeln("Pages:");
                    term.writeln(pages.pages.join("\n"));
                    term.writeln("");
                    term.writeln("Blogs:");
                    blogs.blogs.forEach((b, i) => {
                        term.writeln(`  ${i+1}. ${b}`);
                    });
                    // term.writeln(blogs.blogs.join("\n"));
                    prompt();
                }).catch(err => {
                    term.writeln(`Error fetching pages and blogs. ${err}`);
                    prompt();
                });
                return;

            }
        break;

        case "goto":
            if (subcmd === "page") {
                if (args.length === 0) {
                    term.writeln("Usage: goto page <page> or goto blog <blog>");
                    prompt();
                    return;
                } else {
                    try {
                const target = args.join(" "); // <-- join all parts back
                // You can implement your custom logic here
                let cleaned_target = target.toLowerCase();
                cleaned_target = cleaned_target.replace(/'/g, "");
                cleaned_target = cleaned_target.replace(/ /g, "-");
                term.writeln(`Navigating to ${cleaned_target}...`);
                setTimeout(() => {
                    term.write(".");
                }, 150);
                setTimeout(() => {
                    term.write(".");
                }, 300);
                setTimeout(() => {
                    term.write(".\r\n"); // finish with newline
                    // then actually navigate to the new tab
                    window.location.href = `/${cleaned_target}`;
                }, 500);
                // e.g. trigger navigation in your app:
                // window.location.href = `/blog/${target}`;
                } catch (e) {
                term.writeln(`Unknown target: ${target}`);
                prompt();
                };
            }
        } else if (subcmd === "blog") {
                if (args.length === 0) {
                    term.writeln("Usage: goto page <page> or goto blog <blog>");
                    prompt();
                    return;
                } else {
                    try {
                let target = args.join(" "); // <-- join all parts back
                if (/^\d+$/.test(target)) {
                    const idx = parseInt(target, 10) - 1;
                    if (blogsCache[idx]) {
                        target = blogsCache[idx];
                    }
                }

                // You can implement your custom logic here
                let cleaned_target = target.toLowerCase();
                cleaned_target = cleaned_target.replace(/'/g, "");
                cleaned_target = cleaned_target.replace(/ /g, "-");
                term.writeln(`Navigating to ${cleaned_target}...`);
                setTimeout(() => {
                    term.write(".");
                }, 150);
                setTimeout(() => {
                    term.write(".");
                }, 300);
                setTimeout(() => {
                    term.write(".\r\n"); // finish with newline
                    // then actually navigate to the new tab
                    window.location.href = `/blog/${cleaned_target}`;
                }, 500);
                // e.g. trigger navigation in your app:
                // window.location.href = `/blog/${target}`;
                } catch (e) {
                term.writeln(`Unknown target: ${target}`);
                prompt();
                };
            }
        } else {
            term.writeln("Usage: goto page <page> or goto blog <blog>");
            prompt();
            return;
        }

        break;


        case "echo":
        term.writeln([subcmd, ...args].join(" "));
        break;

        default:
        term.writeln(`${cmd}: command not found. Try 'help' for more info.`);
    }
    prompt();
};

// refit on resize
addEventListener("resize", () => fit.fit());

document.addEventListener("DOMContentLoaded", () => {
  const terminalWrapper = document.querySelector(".terminal-wrapper");
  const btnMin = terminalWrapper.querySelector(".btn-min");
  const btnMax = terminalWrapper.querySelector(".btn-max");
  // const btnClose = terminalWrapper.querySelector(".btn-close");

  btnMin.addEventListener("click", () => {
    terminalWrapper.classList.add("collapsed");
  });

  btnMax.addEventListener("click", () => {
    terminalWrapper.classList.remove("collapsed");
  });

  btnClose.addEventListener("click", () => {
    // Example: completely hide it
    terminalWrapper.style.display = "none";
  });
});