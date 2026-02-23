'''
AI was used to make this GUI annotator based on prompts explaining all windows

HARDWARE: TPUv3
HOURS USED: 10 (overestimated to account for training and chip difference on calculator)
PROVIDER: Google Cloud Platform
REGION: northamerica-northeast-1
TOTAL EMISSIONS: 0.08 kg CO2
TOTAL OFFSET BY GOOGLE: 0.08 kg CO2
'''

import tkinter as tk
from pathlib import Path
from tkinter import messagebox, scrolledtext, ttk

import pandas as pd

# --- STYLING CONSTANTS ---
BG_MAIN = "#121212"
BG_CARD = "#1e1e1e"
ACCENT_BLUE = "#00a2ed"
SUCCESS_GREEN = "#1e7e34"
DANGER_RED = "#bd2130"
TEXT_MAIN = "#e0e0e0"
TEXT_DIM = "#b0b0b0"
BORDER = "#333333"


class PhishAnnotator:
    def __init__(self, root):
        self.root = root
        self.root.title("PhishGuard Pro")
        self.root.geometry("450x450")
        self.root.configure(bg=BG_MAIN)

        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')  # 'clam' allows for better color customization

        # Frame styles
        style.configure("TFrame", background=BG_MAIN)
        style.configure("Card.TFrame", background=BG_CARD, relief="flat")

        # Label styles
        style.configure("TLabel", background=BG_MAIN, foreground=TEXT_MAIN, font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"), foreground=TEXT_MAIN)

        # Input styles
        style.configure("TEntry", fieldbackground=BG_CARD, foreground=TEXT_MAIN, insertcolor="white")

        # Button styles
        style.configure("TButton", font=("Segoe UI", 10), background=BG_MAIN, foreground=TEXT_MAIN)
        style.configure("Action.TButton", foreground="white", background=ACCENT_BLUE)
        style.map("Action.TButton", background=[('active', '#0078d4')])

    def create_widgets(self):
        main_container = ttk.Frame(self.root, padding="30")
        main_container.pack(fill="both", expand=True)

        ttk.Label(main_container, text="Data Annotation Suite", style="Header.TLabel").pack(pady=(0, 20))

        # Path Section
        ttk.Label(main_container, text="CSV File Path").pack(anchor="w")
        self.path_entry = ttk.Entry(main_container, width=50)
        self.path_entry.pack(fill="x", pady=(5, 15))

        # Range Section
        range_frame = ttk.Frame(main_container)
        range_frame.pack(fill="x", pady=5)

        ttk.Label(range_frame, text="From Row:").grid(row=0, column=0, sticky="w")
        self.from_entry = ttk.Entry(range_frame, width=10)
        self.from_entry.insert(0, "1")
        self.from_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(range_frame, text="To Row:").grid(row=0, column=2, sticky="w")
        self.to_entry = ttk.Entry(range_frame, width=10)
        self.to_entry.grid(row=0, column=3, padx=5, pady=5)

        # Buttons
        ttk.Separator(main_container, orient="horizontal").pack(fill="x", pady=20)

        ttk.Button(main_container, text="Start First Annotation", style="Action.TButton",
                   command=lambda: self.launch_annotator("annotation1")).pack(fill="x", pady=5)
        ttk.Button(main_container, text="Start Second Annotation", style="Action.TButton",
                   command=lambda: self.launch_annotator("annotation2")).pack(fill="x", pady=5)
        ttk.Button(main_container, text="Calculate Agreement Stats",
                   command=self.show_stats).pack(fill="x", pady=(15, 0))

    def get_validated_df(self):
        path_str = self.path_entry.get().strip()
        if not path_str:
            messagebox.showerror("Error", "Input path is empty.")
            return None, None

        path = Path(path_str)
        if not path.exists():
            messagebox.showerror("Error", f"File not found at:\n{path}")
            return None, None

        try:
            df = pd.read_csv(path)
            for col in ['annotation1', 'annotation2']:
                if col not in df.columns:
                    df[col] = pd.NA

                df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

            return df, path
        except Exception as e:
            messagebox.showerror("Error", f"Pandas failed to read CSV:\n{e}")
            return None, None

    def launch_annotator(self, target_col):
        df, path = self.get_validated_df()
        if df is None: return

        try:
            start_idx = int(self.from_entry.get()) - 1
            end_val = self.to_entry.get().strip()
            end_idx = int(end_val) if end_val else len(df)
            AnnotationWindow(self.root, df, path, target_col, start_idx, end_idx)
        except ValueError:
            messagebox.showerror("Error", "Row indices must be integers.")

    def show_stats(self):
        df, _ = self.get_validated_df()
        if df is None: return

        overlap = df[df['annotation1'].notna() & df['annotation2'].notna()].copy()
        if len(overlap) < 2:
            messagebox.showwarning("Incomplete", "Not enough double-labeled data for statistics.")
            return

        y1 = pd.to_numeric(overlap['annotation1']).astype('Int64')
        y2 = pd.to_numeric(overlap['annotation2']).astype('Int64')
        total = len(y1)
        po = (y1 == y2).sum() / total
        p1_phish = (y1 == 1).sum() / total
        p2_phish = (y2 == 1).sum() / total
        pe = (p1_phish * p2_phish) + ((1 - p1_phish) * (1 - p2_phish))
        kappa = (po - pe) / (1 - pe) if pe < 1 else 1.0

        stats_win = tk.Toplevel(self.root)
        stats_win.title("Results")
        stats_win.geometry("350x300")
        stats_win.configure(bg=BG_CARD)

        content = f"Samples: {total}\nRaw Agreement: {po * 100:.1f}%\n\nCohen's Kappa: {kappa:.3f}"
        tk.Label(stats_win, text="Agreement Analysis", font=("Segoe UI", 12, "bold"), bg=BG_CARD,
                 fg=TEXT_MAIN).pack(pady=20)
        tk.Label(stats_win, text=content, font=("Courier New", 11), bg=BG_CARD, justify="left",
                 fg=TEXT_MAIN).pack(pady=10)

        # Interpretation image-like logic
        interp = "Interpretation: " + ("Good" if 0.6 <= kappa <= 0.8 else "Excellent" if kappa > 0.8 else "Fair/Poor")
        tk.Label(stats_win, text=interp, font=("Segoe UI", 10, "italic"), bg=BG_CARD, fg=TEXT_MAIN).pack(pady=5)


class AnnotationWindow:
    def __init__(self, parent, df, path, col, start, end):
        self.win = tk.Toplevel(parent)
        self.win.title(f"Annotating: {col}")
        self.win.protocol("WM_DELETE_WINDOW", self.save_exit)
        self.win.geometry("900x700")
        self.win.configure(bg=BG_MAIN)

        self.df, self.path, self.col = df, path, col
        self.indices = list(range(max(0, start), min(end, len(df))))
        self.pointer = 0

        self.setup_ui()
        self.update_view()
        self.bind_keys()

    def setup_ui(self):
        # Progress Bar
        self.progress = ttk.Progressbar(self.win, orient="horizontal", mode="determinate")
        self.progress.pack(fill="x")

        header = ttk.Frame(self.win, padding=15)
        header.pack(fill="x")
        self.info_lbl = ttk.Label(header, text="", font=("Segoe UI", 10, "bold"))
        self.info_lbl.pack(side="left")

        # Email Card
        card = tk.Frame(self.win, bg=BG_CARD, padx=20, pady=20, relief="solid", borderwidth=1,
                        highlightbackground=BORDER)
        card.pack(fill="both", expand=True, padx=40, pady=10)

        self.meta_lbl = tk.Label(card, justify="left", anchor="w", bg=BG_CARD, font=("Segoe UI", 10), fg=TEXT_DIM)
        self.meta_lbl.pack(fill="x")

        tk.Frame(card, height=1, bg="#edebe9").pack(fill="x", pady=15)

        self.body_text = scrolledtext.ScrolledText(
            card,
            font=("Segoe UI", 11),
            wrap="word",
            relief="flat",
            bg=BG_CARD,
            fg=TEXT_MAIN,
            insertbackground="white",
        )
        self.body_text.pack(fill="both", expand=True)

        # Footer Controls
        footer = ttk.Frame(self.win, padding=20)
        footer.pack(fill="x")

        # Labeling Buttons with Colors (using standard tk for background support)
        tk.Button(footer, text="LEGIT (f)", bg=SUCCESS_GREEN, fg="white", width=15, font=("Segoe UI", 10, "bold"),
                  command=lambda: self.label(0)).pack(side="left", padx=5)
        tk.Button(footer, text="SPAM (d)", bg=DANGER_RED, fg="white", width=15, font=("Segoe UI", 10, "bold"),
                  command=lambda: self.label(1)).pack(side="left", padx=5)

        ttk.Button(footer, text="Next >", command=lambda: self.nav(1)).pack(side="right", padx=5)
        ttk.Button(footer, text="< Prev", command=lambda: self.nav(-1)).pack(side="right", padx=5)

        # Jump Section
        jump_frame = ttk.Frame(footer)
        jump_frame.pack(side="right", padx=40)
        self.goto_entry = ttk.Entry(jump_frame, width=8)
        self.goto_entry.pack(side="left", padx=5)
        ttk.Button(jump_frame, text="Jump", command=self.jump).pack(side="left")

    def update_view(self):
        real_idx = self.indices[self.pointer]
        row = self.df.iloc[real_idx]

        # Update progress
        pct = ((self.pointer + 1) / len(self.indices)) * 100
        self.progress['value'] = pct

        status = "NOT LABELED" if pd.isna(row[self.col]) else f"CURRENT: {'SPAM' if row[self.col] == 1 else 'LEGIT'}"
        self.info_lbl.config(text=f"ROW {real_idx + 1} | {status} ({self.pointer + 1}/{len(self.indices)})")

        meta = f"FROM: {row['sender']}\nTO: {row['receiver']}\nDATE: {row['date']}\nSUBJECT: {row['subject']}"
        self.meta_lbl.config(text=meta)

        self.body_text.config(state="normal")
        self.body_text.delete('1.0', tk.END)
        self.body_text.insert(tk.END, str(row['body']))
        self.body_text.config(state="disabled")

    def label(self, val):
        if self.win.focus_get() == self.goto_entry: return
        self.df.at[self.indices[self.pointer], self.col] = val
        self.nav(1)

    def nav(self, step):
        if self.win.focus_get() == self.goto_entry: return
        new_ptr = self.pointer + step
        if 0 <= new_ptr < len(self.indices):
            self.pointer = new_ptr

        self.update_view()

    def jump(self):
        try:
            target = int(self.goto_entry.get()) - 1
            if target in self.indices:
                self.pointer = self.indices.index(target)
                self.update_view()
            else:
                messagebox.showinfo("Limit", "That row is outside the current range.")
        except ValueError:
            pass

    def bind_keys(self):
        self.win.bind("<Escape>", lambda e: self.save_exit())
        self.win.bind("<Left>", lambda e: self.nav(-1))
        self.win.bind("<Right>", lambda e: self.nav(1))
        self.win.bind("d", lambda e: self.label(1))
        self.win.bind("f", lambda e: self.label(0))

    def save_exit(self):
        self.df.to_csv(self.path, index=False)
        self.win.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = PhishAnnotator(root)
    root.mainloop()
