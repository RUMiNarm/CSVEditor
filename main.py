import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd

class CSVEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Editor")
        
        self.csv_files = {
            "hu.csv": "hu.csv",
            "tensuu.csv": "tensuu.csv",
            "teyaku.csv": "teyaku.csv"
        }
        
        self.selected_file = tk.StringVar(value="")
        self.df = None
        
        self.create_main_screen()
    
    def create_main_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        tk.Label(self.root, text="編集するCSVファイルを選択してください").pack(pady=10)
        
        for name in self.csv_files.keys():
            tk.Radiobutton(self.root, text=name, variable=self.selected_file, value=name).pack(anchor='w')
        
        tk.Button(self.root, text="選択", command=self.load_csv).pack(pady=20)
    
    def load_csv(self):
        file_key = self.selected_file.get()
        if not file_key:
            messagebox.showerror("エラー", "ファイルを選択してください")
            return
        
        file_path = self.csv_files[file_key]
        try:
            headers = {
            "hu.csv": ["アガり方", "鳴き/メンゼン", "ピンフ", "符数"],
            "tensuu.csv": ["翻数", "符数", "親/子", "アガり方","点数"],
            "teyaku.csv": ["翻数", "役名"]
        }
            self.df = pd.read_csv(file_path, header=None)
            if file_key in headers:
                self.df.columns = headers[file_key]
                self.create_edit_screen()
        except Exception as e:
            messagebox.showerror("エラー", f"CSVの読み込みに失敗しました: {e}")
    
    def create_edit_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True)
        
        self.tree = ttk.Treeview(frame, columns=list(self.df.columns), show='headings')
        for col in self.df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        for i, row in self.df.iterrows():
            self.tree.insert("", "end", values=list(row))
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="編集", command=self.edit_row).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="追加", command=self.add_row).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="削除", command=self.delete_row).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="戻る", command=self.create_main_screen).pack(side=tk.LEFT, padx=5)
    
    def edit_row(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("エラー", "編集する行を選択してください")
            return
        
        values = self.tree.item(selected_item, "values")
        self.open_edit_window(selected_item, values)
    
    def open_edit_window(self, item, values):
        edit_win = tk.Toplevel(self.root)
        edit_win.title("編集")
        
        entries = []
        for i, col in enumerate(self.df.columns):
            tk.Label(edit_win, text=col).grid(row=i, column=0, padx=10, pady=5)
            entry = tk.Entry(edit_win)
            entry.insert(0, values[i])
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries.append(entry)
        
        def apply_changes():
            new_values = [e.get() for e in entries]
            self.tree.item(item, values=new_values)
            self.update_dataframe()
            edit_win.destroy()
        
        tk.Button(edit_win, text="適用", command=apply_changes).grid(row=len(self.df.columns), columnspan=2, pady=10)
    
    def add_row(self):
        new_data = ["" for _ in self.df.columns]
        item = self.tree.insert("", "end", values=new_data)
        self.open_edit_window(item, new_data)
    
    def delete_row(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("エラー", "削除する行を選択してください")
            return
        
        self.tree.delete(selected_item)
        self.update_dataframe()
    
    def update_dataframe(self):
        new_data = []
        for item in self.tree.get_children():
            new_data.append(self.tree.item(item, "values"))
        
        self.df = pd.DataFrame(new_data, columns=self.df.columns)
        file_path = self.csv_files[self.selected_file.get()]
        self.df.to_csv(file_path, index=False)
        messagebox.showinfo("保存", "変更が保存されました")

if __name__ == "__main__":
    root = tk.Tk()
    app = CSVEditorApp(root)
    root.mainloop()
