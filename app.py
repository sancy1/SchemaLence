
# import tkinter as tk
import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog

import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.widgets.scrolled import ScrolledFrame

import psycopg2
from psycopg2.extras import RealDictCursor

import pandas as pd
import json


class SchemaLence(tb.Window):

    def __init__(self):
        super().__init__(
            themename="cyborg",
            title="SchemaLence - Database Architect",
            resizable=(True, True)
        )

        # =========================================================
        # DYNAMIC LOGO / ICON LOADER
        # =========================================================
        import os
        import sys

        # Get the absolute path to the folder where the script is running
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_path, "logo.ico")
        png_path = os.path.join(base_path, "logo.png")

        try:
            if os.path.exists(icon_path):
                # Standard Windows .ico method
                self.iconbitmap(icon_path)
            elif os.path.exists(png_path):
                # Fallback for .png or Linux/Mac
                img = tk.PhotoImage(file=png_path)
                self.iconphoto(True, img)
        except Exception as e:
            print(f"Icon could not be loaded: {e}")

        # State initialization
        self.conn = None
        self.current_table = None
        self.df_cache = None
        self.sidebar_buttons = {}

        self.state('zoomed')
        self.setup_styles()
        self.create_landing_page()

    # =========================================================
    # STYLES (Updated for Left Alignment)
    # =========================================================
    def setup_styles(self):
        style = tb.Style()

        # Added anchor='w' to force left alignment for all sidebar buttons
        style.configure(
            'Active.Link.TButton',
            font=('Segoe UI', 10, 'bold'),
            foreground='#00d4ff',
            anchor="w"  # Forces text to the left
        )

        style.configure(
            'Inactive.Link.TButton',
            font=('Segoe UI', 10),
            foreground='#ffffff',
            anchor="w"  # Forces text to the left
        )

        # Specific style for the "VIEW ALL" button to ensure left alignment
        style.configure('Left.TButton', anchor="w")

        style.configure(
            'Neon.TButton',
            font=('Segoe UI', 10, 'bold'),
            foreground='#00d4ff',
            background='#060606',
            borderwidth=1,
            bordercolor='#00d4ff'
        )

    # =========================================================
    # HELPERS
    # =========================================================
    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()


    # =========================================================
    # DISCONNECT LOGIC
    # =========================================================
    def disconnect_database(self):
        if self.conn:
            try:
                self.conn.close()
            except:
                pass
        
        # Reset state
        self.conn = None
        self.current_table = None
        self.df_cache = None
        self.sidebar_buttons = {}
        
        # Go back to landing page
        self.create_landing_page()

    # =========================================================
    # LANDING PAGE
    # =========================================================
    def create_landing_page(self):

        self.clear_window()

        main_container = tb.Frame(self, padding=50)
        main_container.pack(fill=BOTH, expand=YES)

        tb.Label(
            main_container,
            text="SCHEMALENCE",
            font=("Orbitron", 40, "bold"),
            foreground="#00d4ff"
        ).pack(pady=(0, 10))

        tb.Label(
            main_container,
            text="Automated Schema Architect & Data Intelligence",
            font=("Segoe UI", 12)
        ).pack(pady=(0, 40))

        cols = tb.Frame(main_container)
        cols.pack(fill=BOTH, expand=YES)

        # =====================================================
        # OPTION A
        # =====================================================
        opt_a = tb.Labelframe(
            cols,
            text=" Option A: Connection String ",
            padding=20,
            bootstyle="info"
        )

        opt_a.pack(
            side=LEFT,
            fill=BOTH,
            expand=YES,
            padx=10
        )

        self.conn_str_var = tk.StringVar()

        tb.Entry(
            opt_a,
            textvariable=self.conn_str_var,
            font=("Consolas", 10)
        ).pack(fill=X, pady=20)

        tb.Button(
            opt_a,
            text="CONNECT VIA STRING",
            style="Neon.TButton",
            command=self.handle_string_connect
        ).pack(fill=X)

        # =====================================================
        # OPTION B
        # =====================================================
        opt_b = tb.Labelframe(
            cols,
            text=" Option B: Form Fields ",
            padding=20,
            bootstyle="primary"
        )

        opt_b.pack(
            side=LEFT,
            fill=BOTH,
            expand=YES,
            padx=10
        )

        self.form_data = {
            "host": tb.Entry(opt_b),
            "port": tb.Entry(opt_b),
            "database": tb.Entry(opt_b),
            "user": tb.Entry(opt_b),
            "password": tb.Entry(opt_b, show="*")
        }

        for label, entry in self.form_data.items():

            tb.Label(
                opt_b,
                text=label.upper()
            ).pack(anchor=W)

            entry.pack(fill=X, pady=(0, 5))

            if label == "port":
                entry.insert(0, "5432")

        tb.Button(
            opt_b,
            text="TEST & CONNECT",
            bootstyle="success-outline",
            command=self.handle_form_connect
        ).pack(fill=X, pady=10)

    # =========================================================
    # DATABASE CONNECTIONS
    # =========================================================
    def handle_string_connect(self):

        s = (
            self.conn_str_var.get()
            .strip()
            .replace('“', '')
            .replace('”', '')
            .replace('"', '')
        )

        try:
            self.conn = psycopg2.connect(
                s,
                connect_timeout=10
            )

            self.show_dashboard()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def handle_form_connect(self):

        try:
            p = {
                k: v.get().strip()
                .replace('“', '')
                .replace('”', '')
                .replace('"', '')
                for k, v in self.form_data.items()
            }

            p['sslmode'] = 'require'

            self.conn = psycopg2.connect(
                **p,
                connect_timeout=10
            )

            self.show_dashboard()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # =========================================================
    # DASHBOARD (Updated Label Alignment)
    # =========================================================
    def show_dashboard(self):
        self.clear_window()
        sidebar = tb.Frame(self, width=300, bootstyle="secondary")
        sidebar.pack(side=LEFT, fill=Y)

        tb.Label(
            sidebar,
            text="📂 SCHEMA BROWSER",
            font=("Segoe UI", 12, "bold"),
            foreground="#00d4ff",
            padding=15,
            anchor=W 
        ).pack(fill=X) 

        # ONLY KEEP THIS ONE BLOCK:
        self.table_list_frame = ScrolledFrame(sidebar, autohide=True)
        self.table_list_frame.pack(fill=BOTH, expand=YES)

        # self.table_list_frame = ScrolledFrame(sidebar, autohide=True)
        # self.table_list_frame.pack(fill=BOTH, expand=YES)

        # self.table_list_frame = ScrolledFrame(
        #     sidebar,
        #     autohide=True
        # )

        # self.table_list_frame.pack(
        #     fill=BOTH,
        #     expand=YES
        # )

        # =====================================================
        # CONTENT AREA
        # =====================================================
        self.content_area = tb.Notebook(
            self,
            bootstyle="info"
        )

        self.content_area.pack(
            side=RIGHT,
            fill=BOTH,
            expand=YES,
            padx=10,
            pady=10
        )

        self.tab_schema = tb.Frame(self.content_area)
        self.tab_data = tb.Frame(self.content_area)

        self.content_area.add(
            self.tab_schema,
            text="  SCHEMA VIEW  "
        )

        self.content_area.add(
            self.tab_data,
            text="  DATA GRID  "
        )

        self.refresh_tables()

    # =========================================================
    # LOAD TABLES
    # =========================================================
    def refresh_tables(self):

        cursor = self.conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)

        tables = cursor.fetchall()

        tb.Button(
            self.table_list_frame,
            text="⚡ VIEW ALL SCHEMAS",
            bootstyle="info-outline",
            command=self.display_all_schemas
        ).pack(fill=X, padx=10, pady=10)

        for t in tables:

            name = t['table_name']

            # btn = tb.Button(
            #     self.table_list_frame,
            #     text=f"  {name}",
            #     style="Inactive.Link.TButton",
            #     command=lambda n=name: self.load_table_context(n)
            # )

            btn = tb.Button(
                self.table_list_frame,
                text=f"  {name}",
                style="Inactive.Link.TButton",
                compound=LEFT,
                padding=(15, 5),
                command=lambda n=name: self.load_table_context(n)
            )

            # btn.pack(fill=X, padx=15, pady=2)
            btn.pack(fill=X, padx=5, pady=2)

            self.sidebar_buttons[name] = btn

    def update_sidebar_highlight(self, active_name):

        for name, btn in self.sidebar_buttons.items():

            btn.configure(
                style="Active.Link.TButton"
                if name == active_name
                else "Inactive.Link.TButton"
            )

    def load_table_context(self, table_name):

        self.current_table = table_name

        self.update_sidebar_highlight(table_name)

        self.display_single_schema(table_name)
        self.display_table_data(table_name)

   
    # =========================================================
    # UPDATED SCHEMA ENGINE (Comprehensive Intelligence)
    # =========================================================
    def get_schema_text(self, table_name):
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)

        # 1. TABLE DESCRIPTION
        cursor.execute("SELECT obj_description(%s::regclass, 'pg_class')", (table_name,))
        desc_res = cursor.fetchone()
        description = desc_res['obj_description'] if desc_res and desc_res['obj_description'] else "No metadata description found."

        # 2. FOREIGN KEYS
        cursor.execute("""
            SELECT kcu.column_name, ccu.table_name AS foreign_table, ccu.column_name AS foreign_column
            FROM information_schema.table_constraints AS tc
            JOIN information_schema.key_column_usage AS kcu ON tc.constraint_name = kcu.constraint_name
            JOIN information_schema.constraint_column_usage AS ccu ON ccu.constraint_name = tc.constraint_name
            WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_name = %s
        """, (table_name,))
        fks = cursor.fetchall()

        # 3. COLUMNS
        cursor.execute("""
            SELECT column_name, udt_name, data_type, is_nullable, column_default, character_maximum_length
            FROM information_schema.columns WHERE table_name = %s ORDER BY ordinal_position
        """, (table_name,))
        cols = cursor.fetchall()

        # 4. ALLOWED VALUES (Check Constraints)
        cursor.execute("""
            SELECT column_name, check_clause 
            FROM information_schema.check_constraints cc
            JOIN information_schema.constraint_column_usage ccu ON cc.constraint_name = ccu.constraint_name
            WHERE ccu.table_name = %s
        """, (table_name,))
        checks = cursor.fetchall()

        # 5. UNIQUE CONSTRAINTS (New Feature)
        cursor.execute("""
            SELECT tc.constraint_name, kcu.column_name
            FROM information_schema.table_constraints AS tc
            JOIN information_schema.key_column_usage AS kcu ON tc.constraint_name = kcu.constraint_name
            WHERE tc.constraint_type = 'UNIQUE' AND tc.table_name = %s
        """, (table_name,))
        uniques = cursor.fetchall()

        # 6. ENUM TYPES (New Feature - Native Allowed Values)
        cursor.execute("""
            SELECT t.column_name, e.enumlabel as value
            FROM pg_enum e
            JOIN pg_type ty ON e.enumtypid = ty.oid
            JOIN (SELECT column_name, udt_name FROM information_schema.columns WHERE table_name = %s) t 
              ON t.udt_name = ty.typname
        """, (table_name,))
        enums = cursor.fetchall()

        # 7. TRIGGERS (New Feature - Auto-Logic)
        cursor.execute("""
            SELECT trigger_name, action_timing, event_manipulation 
            FROM information_schema.triggers 
            WHERE event_object_table = %s
        """, (table_name,))
        triggers = cursor.fetchall()

        # 8. INDEXES & PK
        cursor.execute("SELECT indexname FROM pg_indexes WHERE tablename = %s", (table_name,))
        idxs = cursor.fetchall()
        cursor.execute("""
            SELECT a.attname FROM pg_index i JOIN pg_attribute a ON a.attrelid = i.indrelid 
            AND a.attnum = ANY(i.indkey) WHERE i.indrelid = %s::regclass AND i.indisprimary
        """, (table_name,))
        pk = cursor.fetchone()

        # 9. ROW COUNT & SAMPLE
        cursor.execute(f'SELECT COUNT(*) FROM "{table_name}"')
        row_count = cursor.fetchone()['count']
        example_json = "{}"
        if row_count > 0:
            cursor.execute(f'SELECT * FROM "{table_name}" LIMIT 1')
            example_json = json.dumps(dict(cursor.fetchone()), indent=2, default=str)

        # --- FORMATTING OUTPUT ---
        o = "──────────────────────────────────────────────\n"
        o += f"📋 TABLE: {table_name}\n"
        o += "──────────────────────────────────────────────\n\n"
        o += f"📝 Description:\n{description}\n\n"

        o += "🔄 Relationships:\n"
        if fks:
            for fk in fks:
                o += f"- {table_name}.{fk['column_name']} → {fk['foreign_table']}.{fk['foreign_column']}\n"
        else:
            o += "- No explicit foreign relationships found.\n"

        o += f"\n{'Column':<30}{'Type':<28}{'Nullable':<12}{'Default':<22}Description\n"
        o += "─" * 130 + "\n"
        for c in cols:
            ctype = f"{c['data_type']}({c['character_maximum_length']})" if c['character_maximum_length'] else c['data_type']
            o += f"{c['column_name']:<30}{ctype[:28]:<28}{c['is_nullable']:<12}{str(c['column_default'] or '')[:20]:<22}—\n"

        o += "\n🛡️ Integrity & Uniqueness:\n"
        o += f"🔑 PK : {pk['attname'] if pk else 'N/A'}\n"
        if uniques:
            for u in uniques: o += f"💎 UNIQUE: {u['column_name']} ({u['constraint_name']})\n"
        for fk in fks:
            o += f"🔗 FK : {fk['column_name']} → {fk['foreign_table']}.{fk['foreign_column']}\n"

        o += "\n⚡ Triggers (Auto-Logic):\n"
        if triggers:
            for tr in triggers: o += f"⚙️ {tr['trigger_name']} ({tr['action_timing']} {tr['event_manipulation']})\n"
        else:
            o += "- No triggers defined.\n"

        o += "\n── Indexes ──────────────────────────────────\n"
        for i in idxs: o += f"📇 {i['indexname']}\n"

        o += "\n🎛 Allowed Values:\n"
        found_allowed = False
        if checks:
            found_allowed = True
            for chk in checks:
                clean_clause = chk['check_clause'].replace('::text', '').replace('ARRAY[', '').replace(']', '').replace('(', '').replace(')', '')
                o += f"{chk['column_name']} (CHECK):\n"
                if 'ANY' in chk['check_clause'] or 'IN' in chk['check_clause']:
                    values = [v.strip().replace("'", "") for v in clean_clause.split('ANY')[1].split(',') if v.strip()] if 'ANY' in clean_clause else []
                    for val in values: o += f"  - {val}\n"
                else: o += f"  - {clean_clause}\n"
        
        if enums:
            found_allowed = True
            # Group enums by column name
            from collections import defaultdict
            en_map = defaultdict(list)
            for e in enums: en_map[e['column_name']].append(e['value'])
            for col, vals in en_map.items():
                o += f"{col} (ENUM):\n"
                for v in vals: o += f"  - {v}\n"

        if not found_allowed:
            o += "- No specific value constraints (CHECK/ENUM) defined.\n"

        o += f"\n📄 Example Row:\n{example_json}\n"
        o += f"\n📊 Row Count: {row_count}\n"

        return o


    # =========================================================
    # SCHEMA TAB (Themed Scrollbar Fix)
    # =========================================================
    # def display_single_schema(self, table_name):
    #     for widget in self.tab_schema.winfo_children():
    #         widget.destroy()

    #     # 1. Create a container frame for the text and scrollbar
    #     container = tb.Frame(self.tab_schema)
    #     container.pack(fill=BOTH, expand=YES, padx=10, pady=10)

    #     # 2. Create the Text widget (Standard tk.Text for better color control)
    #     # We use the 'cyborg' background color #060606
    #     txt = tk.Text(
    #         container,
    #         font=("Consolas", 11),
    #         bg="#060606",
    #         fg="#00d4ff",
    #         borderwidth=0,
    #         padx=10,
    #         pady=10,
    #         insertbackground="white" # Cursor color
    #     )

    #     # 3. Create a themed Scrollbar
    #     # 'info' bootstyle gives it a nice blue/cyan handle to match your neon theme
    #     scrollbar = tb.Scrollbar(
    #         container, 
    #         orient=VERTICAL, 
    #         command=txt.yview, 
    #         bootstyle="info-round" 
    #     )
        
    #     # 4. Link them together
    #     txt.configure(yscrollcommand=scrollbar.set)

    #     # 5. Pack them (Scrollbar on the right, Text filling the rest)
    #     scrollbar.pack(side=RIGHT, fill=Y)
    #     txt.pack(side=LEFT, fill=BOTH, expand=YES)

    #     # Insert content
    #     content = self.get_schema_text(table_name)
    #     txt.insert(END, content)
    #     txt.config(state=DISABLED) # Make it read-only

    #     # Copy button at the bottom
    #     tb.Button(
    #         self.tab_schema,
    #         text="COPY SCHEMA TO CLIPBOARD",
    #         style="Neon.TButton",
    #         command=lambda: self.copy_to_clip(content)
    #     ).pack(pady=(0, 10))


    def display_single_schema(self, table_name):
        for widget in self.tab_schema.winfo_children():
            widget.destroy()

        container = tb.Frame(self.tab_schema)
        container.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        txt = tk.Text(container, font=("Consolas", 11), bg="#060606", fg="#00d4ff", borderwidth=0, padx=10, pady=10, insertbackground="white")
        scrollbar = tb.Scrollbar(container, orient=VERTICAL, command=txt.yview, bootstyle="info-round")
        txt.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)
        txt.pack(side=LEFT, fill=BOTH, expand=YES)

        content = self.get_schema_text(table_name)
        txt.insert(END, content)
        txt.config(state=DISABLED)

        # BUTTON CONTAINER
        btn_frame = tb.Frame(self.tab_schema)
        btn_frame.pack(pady=(0, 10))

        tb.Button(
            btn_frame,
            text="📋 COPY SCHEMA TO CLIPBOARD",
            style="Neon.TButton",
            command=lambda: self.copy_to_clip(content)
        ).pack(side=LEFT, padx=5)

        tb.Button(
            btn_frame,
            text="🔌 DISCONNECT",
            bootstyle="danger-outline",
            command=self.disconnect_database
        ).pack(side=LEFT, padx=5)

    # =========================================================
    # DATA GRID
    # =========================================================
    def display_table_data(self, table_name):
        for widget in self.tab_data.winfo_children():
            widget.destroy()
        try:
            self.df_cache = pd.read_sql(f'SELECT * FROM "{table_name}" LIMIT 500', self.conn)
            action_bar = tb.Frame(self.tab_data, padding=5)
            action_bar.pack(fill=X)

            # --- RIGHT SIDE BUTTONS (Packed first to sit on far right) ---
            # Disconnect sits at the very edge
            tb.Button(
                action_bar, 
                text="🔌 DISCONNECT", 
                bootstyle="danger-outline", 
                command=self.disconnect_database
            ).pack(side=RIGHT, padx=5)

            # Export next to Disconnect
            tb.Button(
                action_bar, 
                text="📥 EXPORT CSV", 
                bootstyle="success-outline", 
                command=self.export_to_csv
            ).pack(side=RIGHT, padx=5)

            # Copy next to Export
            tb.Button(
                action_bar, 
                text="📋 COPY ALL VISIBLE", 
                bootstyle="info-outline", 
                command=self.copy_all_rows
            ).pack(side=RIGHT, padx=5)

            # --- LEFT SIDE LABEL ---
            tb.Label(
                action_bar,
                text=f"📊 Table View: {table_name}",
                font=("Segoe UI", 10, "bold"),
                foreground="#00d4ff"
            ).pack(side=LEFT, padx=10)

            # --- DATA TREEVIEW ---
            tree = tb.Treeview(self.tab_data, columns=list(self.df_cache.columns), show="headings", bootstyle="info")
            vsb = tb.Scrollbar(self.tab_data, orient="vertical", command=tree.yview)
            hsb = tb.Scrollbar(self.tab_data, orient="horizontal", command=tree.xview)
            tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
            
            vsb.pack(side=RIGHT, fill=Y)
            hsb.pack(side=BOTTOM, fill=X)
            tree.pack(fill=BOTH, expand=YES)

            for col in self.df_cache.columns: 
                tree.heading(col, text=col.upper())
                tree.column(col, width=150)
                
            for _, row in self.df_cache.iterrows(): 
                tree.insert("", END, values=[str(v) if v is not None else "NULL" for v in row])

        except Exception as e:
            tb.Label(self.tab_data, text=f"Error loading data: {e}", foreground="red").pack(pady=20)
            tb.Button(self.tab_data, text="🔌 DISCONNECT", bootstyle="danger", command=self.disconnect_database).pack()

    # =========================================================
    # ACTIONS
    # =========================================================
    def copy_all_rows(self):

        if self.df_cache is not None:

            self.copy_to_clip(
                self.df_cache.to_csv(
                    sep='\t',
                    index=False
                )
            )

    def export_to_csv(self):

        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")]
        )

        if path:

            self.df_cache.to_csv(
                path,
                index=False
            )

            messagebox.showinfo(
                "Success",
                f"Data exported to {path}"
            )

    def copy_to_clip(self, text):

        self.clipboard_clear()
        self.clipboard_append(text)

        messagebox.showinfo(
            "Clipboard",
            "Data copied successfully!"
        )

    # =========================================================
    # VIEW ALL SCHEMAS
    # =========================================================
    def display_all_schemas(self):

        for widget in self.tab_schema.winfo_children():
            widget.destroy()

        txt = scrolledtext.ScrolledText(
            self.tab_schema,
            font=("Consolas", 11),
            bg="#060606",
            fg="#00d4ff"
        )

        txt.pack(
            fill=BOTH,
            expand=YES,
            padx=10,
            pady=10
        )

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)

        full_text = "\n".join([
            self.get_schema_text(t[0])
            + "\n"
            + "=" * 70
            + "\n"
            for t in cursor.fetchall()
        ])

        txt.insert(END, full_text)

        tb.Button(
            self.tab_schema,
            text="COPY ALL SCHEMAS",
            style="Neon.TButton",
            command=lambda: self.copy_to_clip(full_text)
        ).pack(pady=10)


# =============================================================
# APP START
# =============================================================
if __name__ == "__main__":

    app = SchemaLence()
    app.mainloop()