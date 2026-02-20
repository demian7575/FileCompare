import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from dataclasses import dataclass
from pathlib import Path


@dataclass
class OperationRow:
    op_type: str
    source: str
    target: str
    reason: str
    conflict: str


class FileCompareApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("FileCompare - Preview-first File Organizer")
        self.geometry("1200x700")

        self.selected_folder: Path | None = None
        self.status_var = tk.StringVar(value="Ready: 폴더를 선택하고 미리보기를 생성하세요.")

        self._build_toolbar()
        self._build_table()
        self._build_footer()

    def _build_toolbar(self) -> None:
        toolbar = ttk.Frame(self, padding=10)
        toolbar.pack(fill=tk.X)

        ttk.Button(toolbar, text="폴더 선택", command=self.select_folder).pack(side=tk.LEFT, padx=4)
        ttk.Button(toolbar, text="미리보기 생성", command=self.generate_preview).pack(side=tk.LEFT, padx=4)
        ttk.Button(toolbar, text="실행", command=self.apply_plan).pack(side=tk.LEFT, padx=4)

        ttk.Label(
            toolbar,
            text="기본 정책: Preview -> Confirm -> Apply",
            foreground="#444",
        ).pack(side=tk.RIGHT, padx=8)

    def _build_table(self) -> None:
        frame = ttk.Frame(self, padding=(10, 0, 10, 0))
        frame.pack(fill=tk.BOTH, expand=True)

        columns = ("type", "source", "target", "reason", "conflict")
        self.table = ttk.Treeview(frame, columns=columns, show="headings")
        self.table.heading("type", text="Type")
        self.table.heading("source", text="Source")
        self.table.heading("target", text="Target")
        self.table.heading("reason", text="Reason")
        self.table.heading("conflict", text="Conflict")

        self.table.column("type", width=110, anchor=tk.W)
        self.table.column("source", width=340, anchor=tk.W)
        self.table.column("target", width=340, anchor=tk.W)
        self.table.column("reason", width=270, anchor=tk.W)
        self.table.column("conflict", width=120, anchor=tk.W)

        y_scroll = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.table.yview)
        self.table.configure(yscrollcommand=y_scroll.set)

        self.table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    def _build_footer(self) -> None:
        footer = ttk.Frame(self, padding=10)
        footer.pack(fill=tk.X)
        ttk.Label(footer, textvariable=self.status_var).pack(side=tk.LEFT)

    def select_folder(self) -> None:
        selected = filedialog.askdirectory(title="분석할 폴더를 선택하세요")
        if not selected:
            return
        self.selected_folder = Path(selected)
        self.status_var.set(f"선택된 폴더: {self.selected_folder}")

    def generate_preview(self) -> None:
        self.table.delete(*self.table.get_children())

        if self.selected_folder is None:
            messagebox.showinfo("알림", "먼저 폴더를 선택하세요.")
            return

        rows = self._sample_rows(self.selected_folder)
        for row in rows:
            self.table.insert("", tk.END, values=(row.op_type, row.source, row.target, row.reason, row.conflict))

        self.status_var.set(f"미리보기 생성 완료: {len(rows)}건")

    def apply_plan(self) -> None:
        count = len(self.table.get_children())
        if count == 0:
            messagebox.showwarning("실행 불가", "실행할 미리보기 항목이 없습니다.")
            return

        messagebox.showinfo(
            "안전 모드",
            "현재 버전은 미리보기 중심 MVP입니다.\n실제 파일 변경은 아직 비활성화되어 있습니다.",
        )
        self.status_var.set("안전 모드: 현재는 미리보기만 제공됩니다.")

    @staticmethod
    def _sample_rows(base: Path) -> list[OperationRow]:
        downloads = str(base)
        return [
            OperationRow(
                "MOVE",
                f"{downloads}/receipt_2025_11.pdf",
                f"{downloads}/Documents/receipt_2025_11.pdf",
                "Rule: ext=pdf -> Documents",
                "NONE",
            ),
            OperationRow(
                "RENAME",
                f"{downloads}/IMG_0001.JPG",
                f"{downloads}/2026-02-20_IMG_0001.JPG",
                "Rule: camera files normalize",
                "NONE",
            ),
            OperationRow(
                "DELETE",
                f"{downloads}/copy_movie.mkv",
                "(Recycle Bin)",
                "Duplicate hash match group #14",
                "PROTECTED",
            ),
        ]


if __name__ == "__main__":
    app = FileCompareApp()
    app.mainloop()
