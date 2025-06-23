# ╔═══════════════════════════════════════════════════════════════════╗
# ║                               BoxGen                              ║
# ╟───────────────────────────────────────────────────────────────────╢
# ║  Author     :  Ratbag (Dove)                                      ║
# ║                                                                   ║
# ║  Github     :  https://github.com/DeadDove13                      ║
# ║                                                                   ║
# ║  Description:  Generates formatted comment blocks for code.       ║
# ║                                                                   ║
# ║  Notes      :  Requires Python 3.x                                ║
# ║                 Uses built-in tkinter (no external dependencies)  ║
# ║                                                                   ║
# ╚═══════════════════════════════════════════════════════════════════╝
#------------- IMPORTS -------------
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText

#------------- SECTION CLASS -------------
# One section = 1 title + 1 content block
class Section:
    def __init__(self, parent, index, on_update):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self.index = index
        self.on_update = on_update

        self.title_var = tk.StringVar()
        self.title_entry = ttk.Entry(self.frame, textvariable=self.title_var)
        self.title_entry.grid(row=0, column=0, sticky='ew', padx=5, pady=2)
        self.title_var.trace_add("write", lambda *args: self.on_update())

        self.text = ScrolledText(self.frame, height=6, wrap='none')
        self.text.grid(row=1, column=0, sticky='nsew', padx=5)
        self.text.bind('<KeyRelease>', lambda e: self.on_update())

        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)

        # up/down/remove buttons
        self.controls = ttk.Frame(self.frame)
        self.controls.grid(row=2, column=0, sticky='ew', padx=5, pady=(2, 5))

        ttk.Button(self.controls, text="↑", width=3, command=self.move_up).pack(side='left')
        ttk.Button(self.controls, text="↓", width=3, command=self.move_down).pack(side='left')

        self.remove_btn = ttk.Button(self.controls, text="Remove", command=self.remove)
        self.remove_btn.pack(side='right')

    def move_up(self):
        self.on_update(move_index=(self.index, self.index - 1))

    def move_down(self):
        self.on_update(move_index=(self.index, self.index + 1))

    def remove(self):
        self.on_update(remove_index=self.index)

    def get_data(self):
        return self.title_var.get(), self.text.get('1.0', 'end').strip()

    def pack(self):
        self.frame.pack(fill='both', expand=True, pady=5, padx=2)

    def forget(self):
        self.frame.pack_forget()

#------------- MAIN APP -------------
class BoxGen:
    def __init__(self, root):
        self.root = root
        self.root.title("Comment Box Generator")
        self.sections = []

        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill='both', expand=True)

        # left panel = inputs
        self.settings = ttk.Frame(self.main_frame)
        self.settings.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=2)
        self.main_frame.rowconfigure(0, weight=1)

        # box title input
        ttk.Label(self.settings, text="Box Title:").pack(anchor='w')
        self.title_var = tk.StringVar()
        self.title_var.trace_add("write", lambda *args: self.generate_preview())
        ttk.Entry(self.settings, textvariable=self.title_var).pack(fill='x')

        # comment style dropdown
        ttk.Label(self.settings, text="Comment Style:").pack(anchor='w')
        self.comment_style = ttk.Combobox(self.settings, state='readonly')
        self.comment_style['values'] = [
            'none', 'hash', 'slash', 'html', 'sql', 'ini',
            'apostrophe', 'ocaml', 'fortran', 'matlab', 'rem'
        ]
        self.comment_style.current(0)
        self.comment_style.pack(fill='x')
        self.comment_style.bind('<<ComboboxSelected>>', lambda e: self.generate_preview())

        # layout type dropdown
        ttk.Label(self.settings, text="Content Layout:").pack(anchor='w')
        self.content_mode = ttk.Combobox(self.settings, state='readonly')
        self.content_mode['values'] = ['newline', 'inline']
        self.content_mode.current(0)
        self.content_mode.pack(fill='x')
        self.content_mode.bind('<<ComboboxSelected>>', lambda e: self.generate_preview())

        #------------- SCROLLABLE SECTION CONTAINER -------------
        section_container_frame = ttk.Frame(self.settings)
        section_container_frame.pack(fill='both', expand=True)
        section_container_frame.config(height=400)

        self.section_canvas = tk.Canvas(section_container_frame)
        self.section_scrollbar = ttk.Scrollbar(section_container_frame, orient="vertical", command=self.section_canvas.yview)
        self.section_scrollable = ttk.Frame(self.section_canvas)

        self.section_window = self.section_canvas.create_window((0, 0), window=self.section_scrollable, anchor="nw")

        self.section_canvas.bind(
            "<Configure>",
            lambda e: self.section_canvas.itemconfig(self.section_window, width=e.width)
        )

        self.section_scrollable.bind(
            "<Configure>",
            lambda e: self.section_canvas.configure(
                scrollregion=self.section_canvas.bbox("all")
            )
        )

        self.section_canvas.configure(yscrollcommand=self.section_scrollbar.set)
        self.section_canvas.pack(side="left", fill="both", expand=True)
        self.section_scrollbar.pack(side="right", fill="y")

        self.section_canvas.bind_all("<MouseWheel>", lambda e: self.section_canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        self.section_frame = self.section_scrollable

        ttk.Button(self.settings, text="Add Section", command=self.add_section).pack(pady=(5, 0))

        #------------- RIGHT SIDE: PREVIEW OUTPUT -------------
        right_frame = ttk.Frame(self.main_frame)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)
        right_frame.rowconfigure(1, weight=1)

        ttk.Label(right_frame, text="Preview:").pack(anchor='w')
        self.preview = ScrolledText(right_frame, height=20, wrap='none')
        self.preview.pack(fill='both', expand=True)

        ttk.Button(right_frame, text="Copy to Clipboard", command=self.copy_to_clipboard).pack()

        self.add_section()

    #------------- SECTION MANIPULATION -------------
    def add_section(self):
        index = len(self.sections)
        section = Section(self.section_frame, index, self.on_update)
        self.sections.append(section)
        self.repack_sections()

    def repack_sections(self):
        for idx, sec in enumerate(self.sections):
            sec.index = idx
            sec.forget()
            sec.pack()
        self.generate_preview()

    def on_update(self, move_index=None, remove_index=None):
        if move_index:
            i, j = move_index
            if 0 <= j < len(self.sections):
                self.sections[i], self.sections[j] = self.sections[j], self.sections[i]
        if remove_index is not None:
            self.sections[remove_index].frame.destroy()
            del self.sections[remove_index]
        self.repack_sections()

    #------------- PREVIEW GENERATION -------------
    def generate_preview(self):
        title = self.title_var.get().strip()
        mode = self.content_mode.get()
        lang = self.comment_style.get()

        raw_lines = []
        data = [s.get_data() for s in self.sections]
        longest = max((len(t.strip().rstrip(':')) for t, _ in data), default=0)

        for i, (t, c) in enumerate(data):
            t = t.strip().rstrip(':')
            content_lines = c.splitlines()
            if mode == 'inline':
                label = t.ljust(longest)
                if content_lines:
                    raw_lines.append(f"{label}:  {content_lines[0]}")
                    raw_lines.extend(" " * (longest + 4) + l for l in content_lines[1:])
                else:
                    raw_lines.append(f"{label}:")
            else:
                if t:
                    raw_lines.append("  " + t + ":")
                raw_lines.extend("    " + l for l in content_lines)
            if i < len(data) - 1:
                raw_lines.append("")

        max_len = max((len(l) for l in raw_lines), default=0)
        buffer = 2 if mode == 'inline' else 4
        inner_width = max_len + buffer + 2

        box = ["╔" + "═" * inner_width + "╗"]
        if title:
            box.append("║" + title.center(inner_width) + "║")
            box.append("╟" + "─" * inner_width + "╢")

        for line in raw_lines:
            box.append("║" + " " * buffer + line.ljust(inner_width - buffer) + "║")

        box.append("║" + " " * inner_width + "║")
        box.append("╚" + "═" * inner_width + "╝")

        # format by language
        if lang == 'hash':
            result = "\n".join("# " + l for l in box)
        elif lang == 'slash':
            result = "/*\n" + "\n".join(" * " + l for l in box) + "\n */"
        elif lang == 'html':
            result = "<!--\n" + "\n".join(box) + "\n-->"
        elif lang == 'sql':
            result = "\n".join("-- " + l for l in box)
        elif lang == 'ini':
            result = "\n".join("; " + l for l in box)
        elif lang == 'apostrophe':
            result = "\n".join("' " + l for l in box)
        elif lang == 'ocaml':
            result = "(*\n" + "\n".join(box) + "\n*)"
        elif lang == 'fortran':
            result = "\n".join("! " + l for l in box)
        elif lang == 'matlab':
            result = "\n".join("%% " + l for l in box)
        elif lang == 'rem':
            result = "\n".join("REM " + l for l in box)
        else:
            result = "\n".join(box)

        self.preview.delete('1.0', 'end')
        self.preview.insert('1.0', result)

    #------------- CLIPBOARD EXPORT -------------
    def copy_to_clipboard(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.preview.get('1.0', 'end').strip())
        self.root.update()
        messagebox.showinfo("Copied", "Preview copied to clipboard.")

#------------- RUN -------------
if __name__ == '__main__':
    root = tk.Tk()
    app = BoxGen(root)
    root.mainloop()


