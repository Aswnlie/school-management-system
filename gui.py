# =============================================================
# gui.py
# GUI for the School Management System.
# Built with customtkinter (pip install customtkinter).
# Run this instead of main.py when you want the graphical interface.
# =============================================================
 
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
 
from database import Database
from student import Student
from teacher import Teacher
from course import Course
from registration import Registration
 
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")
 
# ── Palette ──────────────────────────────────────────────────
BG      = "#f5f6f8"
PANEL   = "#ffffff"
CARD    = "#eef1f4"
ACCENT  = "#2f5d8c"
ACCENT2 = "#23496f"
SUCCESS = "#3a7d44"
DANGER  = "#b23b3b"
TEXT    = "#20242a"
SUBTEXT = "#6c737f"
BORDER  = "#d7dce2"
 
 
# =============================================================
# Reusable dialog for Add / Edit forms
# =============================================================
 
class FormDialog(ctk.CTkToplevel):
    """Generic modal dialog for data entry forms."""
 
    def __init__(self, parent, title, fields):
        super().__init__(parent)
        self.title(title)
        self.resizable(False, False)
        self.grab_set()
        self.configure(fg_color=PANEL)
        self.result = None
        self._entries = {}
 
        ctk.CTkLabel(self, text=title,
                     font=("Segoe UI", 18, "bold"),
                     text_color=ACCENT).pack(pady=(24, 4), padx=30)
        ctk.CTkLabel(self, text="Enter the details below",
                     font=("Segoe UI", 11),
                     text_color=SUBTEXT).pack(pady=(0, 16))
 
        form = ctk.CTkFrame(self, fg_color=CARD, corner_radius=8)
        form.pack(padx=30, pady=8, fill="both")
 
        for i, f in enumerate(fields):
            ctk.CTkLabel(form, text=f["label"],
                         font=("Segoe UI", 11),
                         text_color=SUBTEXT, anchor="w").grid(
                row=i * 2, column=0, padx=20, pady=(14, 2), sticky="w")
 
            if "options" in f:
                var = ctk.StringVar(value=f.get("default", f["options"][0]))
                widget = ctk.CTkOptionMenu(
                    form, values=f["options"], variable=var,
                    fg_color=BG, button_color=ACCENT,
                    font=("Segoe UI", 11), width=340)
                widget.grid(row=i * 2 + 1, column=0,
                            padx=20, pady=(0, 4), sticky="ew")
                self._entries[f["key"]] = var
            else:
                entry = ctk.CTkEntry(
                    form, width=340,
                    placeholder_text=f.get("placeholder", ""),
                    fg_color=BG, border_color=BORDER,
                    font=("Segoe UI", 11))
                if f.get("default"):
                    entry.insert(0, f["default"])
                entry.grid(row=i * 2 + 1, column=0,
                           padx=20, pady=(0, 4), sticky="ew")
                self._entries[f["key"]] = entry
 
        form.columnconfigure(0, weight=1)
 
        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.pack(pady=20, padx=30, fill="x")
 
        ctk.CTkButton(btn_row, text="Cancel", fg_color=CARD,
                      hover_color=DANGER, text_color=TEXT,
                      font=("Segoe UI", 12, "bold"),
                      corner_radius=8,
                      command=self.destroy).pack(
            side="left", expand=True, padx=(0, 8), fill="x")
        ctk.CTkButton(btn_row, text="Save", fg_color=ACCENT,
                      hover_color=ACCENT2, text_color="white",
                      font=("Segoe UI", 12, "bold"),
                      corner_radius=8,
                      command=self._save).pack(
            side="right", expand=True, padx=(8, 0), fill="x")
 
        self._fields = fields
        # Delay so window fully renders before grabbing focus.
        # Without this on Windows, CTkToplevel can appear behind
        # the main window making the edit dialog seem to not open.
        self.after(100, self._show)
 
    def _show(self):
        self.update_idletasks()
        w = self.winfo_width()
        h = self.winfo_height()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        self.geometry(f"+{(sw - w) // 2}+{(sh - h) // 2}")
        self.lift()
        self.focus_force()
        self.grab_set()
 
    def _save(self):
        import re
        data = {}
        for f in self._fields:
            widget = self._entries[f["key"]]
            val = widget.get().strip() if isinstance(widget, ctk.CTkEntry) \
                else widget.get()
 
            # Required field check
            if f.get("required") and not val:
                messagebox.showerror("Validation",
                                     f"'{f['label']}' is required.",
                                     parent=self)
                return
 
            # DOB must be YYYY-MM-DD or empty
            if f["key"] == "dob" and val:
                if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", val):
                    messagebox.showerror(
                        "Invalid Date",
                        "Date of Birth must be in YYYY-MM-DD format.\n"
                        "Example: 2003-04-15",
                        parent=self)
                    return
 
            data[f["key"]] = val or None
        self.result = data
        self.destroy()
 
 
# =============================================================
# Base tab
# =============================================================
 
class BaseTab(ctk.CTkFrame):
    HEADERS = []
 
    def __init__(self, parent, db):
        super().__init__(parent, fg_color=BG)
        self.db = db
        self._build_ui()
        self.refresh()
 
    def _build_ui(self):
        # Toolbar
        top = ctk.CTkFrame(self, fg_color=PANEL, corner_radius=8)
        top.pack(fill="x", padx=20, pady=(20, 8))
 
        self._search_var = ctk.StringVar()
        self._search_var.trace_add("write", lambda *_: self._on_search())
 
        ctk.CTkEntry(top, textvariable=self._search_var,
                     placeholder_text="Search...",
                     width=280, fg_color=BG, border_color=BORDER,
                     font=("Segoe UI", 11)).pack(
            side="left", padx=16, pady=12)
 
        btn_cfg = dict(font=("Segoe UI", 12, "bold"),
                       corner_radius=8, height=36)
 
        ctk.CTkButton(top, text="Add new", fg_color=SUCCESS,
                      hover_color="#27ae60", text_color="white",
                      command=self._add, **btn_cfg).pack(
            side="right", padx=(4, 16), pady=12)
        ctk.CTkButton(top, text="Edit", fg_color=ACCENT,
                      hover_color=ACCENT2, text_color="white",
                      command=self._edit, **btn_cfg).pack(
            side="right", padx=4, pady=12)
        ctk.CTkButton(top, text="Delete", fg_color=DANGER,
                      hover_color="#c0392b", text_color="white",
                      command=self._delete, **btn_cfg).pack(
            side="right", padx=4, pady=12)
        ctk.CTkButton(top, text="Refresh", fg_color=CARD,
                      hover_color=BORDER, text_color=TEXT,
                      command=self.refresh, **btn_cfg).pack(
            side="right", padx=4, pady=12)
 
        # Table
        frame = ctk.CTkFrame(self, fg_color=PANEL, corner_radius=8)
        frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
 
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("School.Treeview",
                        background=CARD, foreground=TEXT,
                        fieldbackground=CARD, rowheight=32,
                        font=("Segoe UI", 11), borderwidth=0)
        style.configure("School.Treeview.Heading",
                        background=BG, foreground=ACCENT,
                        font=("Segoe UI", 11, "bold"), relief="flat")
        style.map("School.Treeview",
                  background=[("selected", ACCENT)],
                  foreground=[("selected", "white")])
 
        self._tree = ttk.Treeview(frame, columns=self.HEADERS,
                                  show="headings",
                                  style="School.Treeview",
                                  selectmode="browse")
        for h in self.HEADERS:
            self._tree.heading(h, text=h)
            self._tree.column(h, minwidth=80, width=140, anchor="w")
 
        sb = ctk.CTkScrollbar(frame, command=self._tree.yview,
                               fg_color=PANEL, button_color=BORDER)
        self._tree.configure(yscrollcommand=sb.set)
        self._tree.pack(side="left", fill="both", expand=True,
                        padx=(12, 0), pady=12)
        sb.pack(side="right", fill="y", pady=12, padx=(0, 8))
 
        self._status = ctk.CTkLabel(self, text="",
                                    font=("Segoe UI", 11),
                                    text_color=SUBTEXT, anchor="w")
        self._status.pack(fill="x", padx=28, pady=(0, 8))
 
    def _populate(self, rows):
        self._tree.delete(*self._tree.get_children())
        for row in rows:
            self._tree.insert("", "end", values=row)
        self._status.configure(text=f"{len(rows)} record(s) found",
                                text_color=SUBTEXT)
 
    def refresh(self):
        try:
            rows = self.load_rows()
            self._populate(rows)
            self._search_var.set("")
        except Exception as e:
            messagebox.showerror("Error", str(e))
 
    def _on_search(self):
        term = self._search_var.get().strip()
        if not term:
            self.refresh()
            return
        try:
            rows = self.search_rows(term)
            self._populate(rows)
        except Exception as e:
            messagebox.showerror("Error", str(e))
 
    def _selected_id(self):
        sel = self._tree.selection()
        if not sel:
            messagebox.showwarning("No selection",
                                   "Please select a record first.")
            return None
        return self._tree.item(sel[0])["values"][0]
 
    def _selected_row(self):
        sel = self._tree.selection()
        if not sel:
            messagebox.showwarning("No selection",
                                   "Please select a record first.")
            return None
        return self._tree.item(sel[0])["values"]
 
    def load_rows(self):        raise NotImplementedError
    def search_rows(self, term): raise NotImplementedError
    def _add(self):             raise NotImplementedError
    def _edit(self):            raise NotImplementedError
    def _delete(self):          raise NotImplementedError
 
 
# =============================================================
# STUDENT TAB
# =============================================================
 
class StudentTab(BaseTab):
    HEADERS = ["ID", "First Name", "Last Name",
               "Email", "Phone", "DOB", "Status"]
 
    def load_rows(self):
        return Student.sort_by_name(Student.get_all(self.db))
 
    def search_rows(self, term):
        return Student.search(term, self.db)
 
    def _add(self):
        dlg = FormDialog(self, "Add Student", [
            {"label": "First Name",  "key": "first",
             "required": True},
            {"label": "Last Name",   "key": "last",
             "required": True},
            {"label": "Email",       "key": "email",
             "required": True},
            {"label": "Phone",       "key": "phone",
             "required": False, "placeholder": "e.g. 555-1001"},
            {"label": "Date of Birth", "key": "dob",
             "required": False, "placeholder": "YYYY-MM-DD"},
        ])
        self.wait_window(dlg)
        if dlg.result:
            try:
                d = dlg.result
                Student(d["first"], d["last"], d["email"],
                        d["phone"], d["dob"]).add(self.db)
                self.refresh()
                self._status.configure(
                    text="Student added successfully.", text_color=SUCCESS)
            except Exception as e:
                messagebox.showerror("Error", str(e))
 
    def _edit(self):
        row = self._selected_row()
        if row is None:
            return
        sid, first, last, email, phone, dob, status = \
            row[0], row[1], row[2], row[3], row[4], row[5], row[6]
        dlg = FormDialog(self, "Edit Student", [
            {"label": "First Name",  "key": "first",
             "required": True,  "default": first},
            {"label": "Last Name",   "key": "last",
             "required": True,  "default": last},
            {"label": "Email",       "key": "email",
             "required": True,  "default": email},
            {"label": "Phone",       "key": "phone",
             "required": False, "default": phone or ""},
            {"label": "Date of Birth (YYYY-MM-DD)", "key": "dob",
             "required": False, "default": str(dob) if dob else ""},
            {"label": "Status",      "key": "status",
             "required": True,
             "options": ["Active", "Inactive", "Graduated"],
             "default": status},
        ])
        self.wait_window(dlg)
        if dlg.result:
            try:
                d = dlg.result
                Student(d["first"], d["last"], d["email"], d["phone"],
                        date_of_birth=d["dob"] or None,
                        student_id=sid,
                        status=d["status"]).update(self.db)
                self.refresh()
                self._status.configure(
                    text="Student updated successfully.", text_color=SUCCESS)
            except Exception as e:
                messagebox.showerror("Error", str(e))
 
    def _delete(self):
        sid = self._selected_id()
        if sid is None:
            return
        if messagebox.askyesno("Confirm",
                               f"Delete student ID {sid}?"):
            try:
                Student.delete_by_id(sid, self.db)
                self.refresh()
                self._status.configure(
                    text="Student deleted.", text_color=DANGER)
            except Exception as e:
                messagebox.showerror("Error", str(e))
 
 
# =============================================================
# TEACHER TAB
# =============================================================
 
class TeacherTab(BaseTab):
    HEADERS = ["ID", "First Name", "Last Name",
               "Email", "Phone", "Department"]
 
    def load_rows(self):
        return Teacher.sort_by_name(Teacher.get_all(self.db))
 
    def search_rows(self, term):
        return Teacher.search(term, self.db)
 
    def _add(self):
        dlg = FormDialog(self, "Add Teacher", [
            {"label": "First Name",  "key": "first",  "required": True},
            {"label": "Last Name",   "key": "last",   "required": True},
            {"label": "Email",       "key": "email",  "required": True},
            {"label": "Phone",       "key": "phone",  "required": False},
            {"label": "Department",  "key": "dept",   "required": True},
        ])
        self.wait_window(dlg)
        if dlg.result:
            try:
                d = dlg.result
                Teacher(d["first"], d["last"], d["email"],
                        d["phone"], d["dept"]).add(self.db)
                self.refresh()
                self._status.configure(
                    text="Teacher added successfully.", text_color=SUCCESS)
            except Exception as e:
                messagebox.showerror("Error", str(e))
 
    def _edit(self):
        row = self._selected_row()
        if row is None:
            return
        tid, first, last, email, phone, dept = row
        dlg = FormDialog(self, "Edit Teacher", [
            {"label": "First Name",  "key": "first",
             "required": True,  "default": first},
            {"label": "Last Name",   "key": "last",
             "required": True,  "default": last},
            {"label": "Email",       "key": "email",
             "required": True,  "default": email},
            {"label": "Phone",       "key": "phone",
             "required": False, "default": phone or ""},
            {"label": "Department",  "key": "dept",
             "required": True,  "default": dept},
        ])
        self.wait_window(dlg)
        if dlg.result:
            try:
                d = dlg.result
                Teacher(d["first"], d["last"], d["email"],
                        d["phone"], d["dept"],
                        teacher_id=tid).update(self.db)
                self.refresh()
                self._status.configure(
                    text="Teacher updated successfully.", text_color=SUCCESS)
            except Exception as e:
                messagebox.showerror("Error", str(e))
 
    def _delete(self):
        tid = self._selected_id()
        if tid is None:
            return
        if messagebox.askyesno("Confirm", f"Delete teacher ID {tid}?"):
            try:
                Teacher.delete_by_id(tid, self.db)
                self.refresh()
                self._status.configure(
                    text="Teacher deleted.", text_color=DANGER)
            except Exception as e:
                messagebox.showerror("Error", str(e))
 
 
# =============================================================
# COURSE TAB
# =============================================================
 
class CourseTab(BaseTab):
    HEADERS = ["ID", "Course Name", "Description", "Credits", "Teacher"]
 
    def load_rows(self):
        return Course.sort_by_name(Course.get_all(self.db))
 
    def search_rows(self, term):
        return Course.search(term, self.db)
 
    def _teacher_options(self):
        rows = Teacher.get_all(self.db)
        return [f"{r[0]} - {r[1]} {r[2]}" for r in rows]
 
    def _add(self):
        opts = self._teacher_options()
        if not opts:
            messagebox.showwarning(
                "No Teachers",
                "Add at least one teacher before adding a course.")
            return
        dlg = FormDialog(self, "Add Course", [
            {"label": "Course Name",  "key": "name",
             "required": True},
            {"label": "Description",  "key": "desc",
             "required": False},
            {"label": "Credits",      "key": "credits",
             "required": True, "placeholder": "e.g. 3"},
            {"label": "Teacher",      "key": "teacher",
             "required": True, "options": opts},
        ])
        self.wait_window(dlg)
        if dlg.result:
            try:
                d = dlg.result
                tid = int(d["teacher"].split("-")[0].strip())
                Course(d["name"], d["desc"],
                       int(d["credits"]), tid).add(self.db)
                self.refresh()
                self._status.configure(
                    text="Course added successfully.", text_color=SUCCESS)
            except Exception as e:
                messagebox.showerror("Error", str(e))
 
    def _edit(self):
        row = self._selected_row()
        if row is None:
            return
        cid, name, desc, credits, teacher_name = row
        opts = self._teacher_options()
        default_teacher = opts[0] if opts else None
        for o in opts:
            if teacher_name and teacher_name in o:
                default_teacher = o
                break
        dlg = FormDialog(self, "Edit Course", [
            {"label": "Course Name",  "key": "name",
             "required": True,  "default": name},
            {"label": "Description",  "key": "desc",
             "required": False, "default": desc or ""},
            {"label": "Credits",      "key": "credits",
             "required": True,  "default": str(credits)},
            {"label": "Teacher",      "key": "teacher",
             "required": True,
             "options": opts, "default": default_teacher},
        ])
        self.wait_window(dlg)
        if dlg.result:
            try:
                d = dlg.result
                tid = int(d["teacher"].split("-")[0].strip())
                Course(d["name"], d["desc"], int(d["credits"]),
                       tid, course_id=cid).update(self.db)
                self.refresh()
                self._status.configure(
                    text="Course updated successfully.", text_color=SUCCESS)
            except Exception as e:
                messagebox.showerror("Error", str(e))
 
    def _delete(self):
        cid = self._selected_id()
        if cid is None:
            return
        if messagebox.askyesno("Confirm", f"Delete course ID {cid}?"):
            try:
                Course.delete_by_id(cid, self.db)
                self.refresh()
                self._status.configure(
                    text="Course deleted.", text_color=DANGER)
            except Exception as e:
                messagebox.showerror("Error", str(e))
 
 
# =============================================================
# REGISTRATION TAB
# =============================================================
 
# =============================================================
# REGISTRATION TAB
# =============================================================


class RegistrationTab(BaseTab):
    HEADERS = ["ID", "Student", "Course", "Date", "Status"]

    def load_rows(self):
        return Registration.sort_by_date(Registration.get_all(self.db))

    def search_rows(self, term):
        return Registration.search(term, self.db)

    def _student_options(self):
        rows = Student.get_all(self.db)
        return [f"{r[0]} - {r[1]} {r[2]}" for r in rows]

    def _course_options(self):
        rows = Course.get_all(self.db)
        return [f"{r[0]} - {r[1]}" for r in rows]

    def _add(self):
        s_opts = self._student_options()
        c_opts = self._course_options()

        if not s_opts or not c_opts:
            messagebox.showwarning(
                "Missing data",
                "At least one student and one course are required."
            )
            return

        dlg = FormDialog(self, "Add Registration", [
            {"label": "Student", "key": "student",
             "required": True, "options": s_opts},
            {"label": "Course", "key": "course",
             "required": True, "options": c_opts},
        ])

        self.wait_window(dlg)

        if dlg.result:
            try:
                sid = int(dlg.result["student"].split("-")[0].strip())
                cid = int(dlg.result["course"].split("-")[0].strip())

                Registration(sid, cid).add(self.db)

                self.refresh()

            except Exception as e:
                messagebox.showerror("Error", str(e))

    def _edit(self):
        rid = self._selected_id()
        if rid is None:
            return

        row = self._selected_row()

        s_opts = self._student_options()
        c_opts = self._course_options()

        dlg = FormDialog(self, "Edit Registration", [
            {"label": "Student", "key": "student",
             "required": True, "options": s_opts},
            {"label": "Course", "key": "course",
             "required": True, "options": c_opts},
            {"label": "Date (YYYY-MM-DD)", "key": "date",
             "required": False,
             "default": str(row[3]) if row[3] else ""},
            {"label": "Status", "key": "status",
             "required": True,
             "options": ["Enrolled", "Completed", "Dropped"],
             "default": row[4]}
        ])

        self.wait_window(dlg)

        if dlg.result:
            try:
                student_id = int(dlg.result["student"].split("-")[0].strip())
                course_id = int(dlg.result["course"].split("-")[0].strip())

                Registration(
                    student_id,
                    course_id,
                    registration_id=rid,
                    registration_date=dlg.result["date"] or None,
                    status=dlg.result["status"]
                ).update(self.db)

                self.refresh()

            except Exception as e:
                messagebox.showerror("Error", str(e))

    def _delete(self):
        rid = self._selected_id()
        if rid is None:
            return

        if messagebox.askyesno("Confirm", f"Delete registration ID {rid}?"):
            try:
                Registration.delete_by_id(rid, self.db)
                self.refresh()

            except Exception as e:
                messagebox.showerror("Error", str(e))


 
# =============================================================
# MAIN WINDOW
# =============================================================
 
class App(ctk.CTk):
 
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.title("School Records Manager")
        self.geometry("1120x680")
        self.minsize(900, 560)
        self.configure(fg_color=BG)
        self._build_ui()
 
    def _build_ui(self):
        # Sidebar
        sidebar = ctk.CTkFrame(self, width=210, fg_color=PANEL,
                               corner_radius=0)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
 
        logo = ctk.CTkFrame(sidebar, fg_color=CARD, corner_radius=8)
        logo.pack(fill="x", padx=16, pady=(24, 8))
        ctk.CTkLabel(logo, text="School DB",
                     font=("Segoe UI", 20, "bold"),
                     text_color=ACCENT).pack(pady=12)
        ctk.CTkLabel(logo, text="Records manager",
                     font=("Segoe UI", 10),
                     text_color=SUBTEXT,
                     justify="center").pack(pady=(0, 12))
 
        self._nav_buttons = {}
        nav_items = [
            ("Students",      "students"),
            ("Teachers",      "teachers"),
            ("Courses",       "courses"),
            ("Registrations", "registrations"),
        ]
        for label, key in nav_items:
            btn = ctk.CTkButton(
                sidebar, text=label, anchor="w",
                fg_color="transparent", hover_color=CARD,
                text_color=TEXT,
                font=("Segoe UI", 12, "bold"),
                height=40, corner_radius=8,
                command=lambda k=key: self._switch_tab(k))
            btn.pack(fill="x", padx=12, pady=3)
            self._nav_buttons[key] = btn
 
        ctk.CTkLabel(sidebar, text="Database connected",
                     font=("Segoe UI", 10),
                     text_color=SUCCESS).pack(side="bottom", pady=16)
 
        # Content area
        self._content = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        self._content.pack(side="right", fill="both", expand=True)
 
        header = ctk.CTkFrame(self._content, fg_color=PANEL,
                              corner_radius=0, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        self._title_label = ctk.CTkLabel(
            header, text="Students",
            font=("Segoe UI", 18, "bold"),
            text_color=TEXT, anchor="w")
        self._title_label.pack(side="left", padx=28, pady=12)
 
        self._tabs = {
            "students":      StudentTab(self._content, self.db),
            "teachers":      TeacherTab(self._content, self.db),
            "courses":       CourseTab(self._content, self.db),
            "registrations": RegistrationTab(self._content, self.db),
        }
        self._active = None
        self._switch_tab("students")
 
    def _switch_tab(self, key):
        if self._active:
            self._tabs[self._active].pack_forget()
            self._nav_buttons[self._active].configure(
                fg_color="transparent")
        self._active = key
        self._tabs[key].pack(fill="both", expand=True)
        self._nav_buttons[key].configure(fg_color=CARD)
        self._title_label.configure(text=key.capitalize())
 
    def on_close(self):
        self.db.close()
        self.destroy()
 
 
# =============================================================
# ENTRY POINT
# =============================================================
 
if __name__ == "__main__":
    import traceback
    try:
        db = Database()
        app = App(db)
        app.protocol("WM_DELETE_WINDOW", app.on_close)
        app.mainloop()
    except Exception as e:
        print("CRASH:", e)
        traceback.print_exc()
        input("Press Enter to close...")
