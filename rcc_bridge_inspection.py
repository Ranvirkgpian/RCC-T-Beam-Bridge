import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import date
import csv
import math

# ============================================================
# RCC T-BEAM BRIDGE - VISUAL INSPECTION APPLICATION
# Tutorial-1: Vibe Coding Assignment
# ============================================================

COMPONENTS = [
    "Deck Slab", "Longitudinal T-Beam Girder", "Cross Girder / Diaphragm",
    "Cantilever Portion", "Kerb / Parapet", "Bearing", "Expansion Joint",
    "Pier Cap", "Pier", "Abutment", "Drainage Arrangement"
]

DEFECTS = [
    "No Significant Defect", "Cracking", "Spalling", "Exposed Reinforcement",
    "Corrosion Staining", "Leakage / Dampness", "Water Accumulation",
    "Honeycombing", "Bearing Deterioration", "Expansion Joint Damage",
    "Surface Deterioration", "Other Visible Distress"
]

SEVERITY_SCORE = {
    "Good": 1,
    "Minor": 2,
    "Moderate": 3,
    "Severe": 4
}

ACTIONS = {
    "Good": "Routine observation / continue periodic inspection",
    "Minor": "Routine maintenance and monitoring",
    "Moderate": "Detailed inspection and timely corrective action",
    "Severe": "Urgent detailed investigation; consider NDT/material testing"
}


class BridgeInspectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RCC T-Beam Bridge | Visual Inspection")
        self.root.geometry("1180x760")
        self.root.minsize(1050, 680)

        self.records = []
        self.photo_path = ""

        self.build_ui()

    def build_ui(self):
        # Header
        header = tk.Frame(self.root, bg="#18324a", padx=20, pady=15)
        header.pack(fill="x")

        tk.Label(
            header, text="RCC T-BEAM BRIDGE",
            font=("Segoe UI", 22, "bold"), fg="white", bg="#18324a"
        ).pack(anchor="w")

        tk.Label(
            header, text="Visual Inspection & Condition Documentation System",
            font=("Segoe UI", 11), fg="#dce8f2", bg="#18324a"
        ).pack(anchor="w", pady=(3, 0))

        # Structure information
        info = ttk.LabelFrame(self.root, text="1. Inspection Information", padding=12)
        info.pack(fill="x", padx=15, pady=10)

        self.structure_var = tk.StringVar(value="RCC T-Beam Bridge")
        self.inspector_var = tk.StringVar()
        self.date_var = tk.StringVar(value=str(date.today()))
        self.weather_var = tk.StringVar(value="Normal")
        self.bridge_id_var = tk.StringVar()

        self.field(info, "Bridge ID", self.bridge_id_var, 0, 0)
        self.field(info, "Inspector", self.inspector_var, 0, 2)
        self.field(info, "Inspection Date", self.date_var, 1, 0)
        self.field(info, "Weather / Site", self.weather_var, 1, 2)

        # Observation entry
        entry = ttk.LabelFrame(self.root, text="2. Record Observation", padding=12)
        entry.pack(fill="x", padx=15, pady=5)

        self.span_var = tk.StringVar()
        self.component_var = tk.StringVar(value=COMPONENTS[0])
        self.location_var = tk.StringVar()
        self.defect_var = tk.StringVar(value=DEFECTS[0])
        self.severity_var = tk.StringVar(value="Good")
        self.remarks_var = tk.StringVar()

        self.field(entry, "Span / Chainage", self.span_var, 0, 0)
        self.combo(entry, "Component", self.component_var, COMPONENTS, 0, 2)
        self.field(entry, "Specific Location", self.location_var, 1, 0)
        self.combo(entry, "Observed Defect", self.defect_var, DEFECTS, 1, 2)
        self.combo(entry, "Severity / Condition", self.severity_var,
                   list(SEVERITY_SCORE.keys()), 2, 0)

        ttk.Label(entry, text="Remarks / Observation").grid(
            row=2, column=2, sticky="w", padx=6, pady=5
        )
        ttk.Entry(entry, textvariable=self.remarks_var, width=55).grid(
            row=2, column=3, sticky="ew", padx=6, pady=5
        )

        ttk.Label(entry, text="Inspection Photograph").grid(
            row=3, column=0, sticky="w", padx=6, pady=5
        )
        self.photo_label = ttk.Label(entry, text="No photo selected")
        self.photo_label.grid(row=3, column=1, columnspan=2, sticky="w", padx=6)
        ttk.Button(entry, text="Choose Photo", command=self.choose_photo).grid(
            row=3, column=3, sticky="e", padx=6
        )

        ttk.Button(
            entry, text="＋ Add Observation",
            command=self.add_observation
        ).grid(row=4, column=3, sticky="e", padx=6, pady=(8, 2))

        for col in range(4):
            entry.columnconfigure(col, weight=1)

        # Records table
        table_frame = ttk.LabelFrame(self.root, text="3. Recorded Observations", padding=8)
        table_frame.pack(fill="both", expand=True, padx=15, pady=8)

        columns = ("#", "Span", "Component", "Location", "Defect", "Severity", "Score", "Priority")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

        widths = {
            "#": 40, "Span": 100, "Component": 190, "Location": 150,
            "Defect": 190, "Severity": 90, "Score": 60, "Priority": 100
        }

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=widths[col], anchor="center")

        scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        # Bottom controls
        bottom = tk.Frame(self.root, padx=15, pady=8)
        bottom.pack(fill="x")

        ttk.Button(bottom, text="Delete Selected",
                   command=self.delete_selected).pack(side="left", padx=4)
        ttk.Button(bottom, text="Clear All",
                   command=self.clear_all).pack(side="left", padx=4)
        ttk.Button(bottom, text="Export CSV",
                   command=self.export_csv).pack(side="left", padx=4)
        ttk.Button(bottom, text="Inspection Dashboard",
                   command=self.show_dashboard).pack(side="right", padx=4)
        ttk.Button(bottom, text="Inspection Summary",
                   command=self.show_summary).pack(side="right", padx=4)

        self.status = tk.StringVar(value="Ready — enter an observation.")
        ttk.Label(bottom, textvariable=self.status).pack(side="right", padx=15)

    def field(self, parent, label, variable, row, col):
        ttk.Label(parent, text=label).grid(
            row=row, column=col, sticky="w", padx=6, pady=5
        )
        ttk.Entry(parent, textvariable=variable, width=30).grid(
            row=row, column=col + 1, sticky="ew", padx=6, pady=5
        )

    def combo(self, parent, label, variable, values, row, col):
        ttk.Label(parent, text=label).grid(
            row=row, column=col, sticky="w", padx=6, pady=5
        )
        box = ttk.Combobox(
            parent, textvariable=variable, values=values,
            state="readonly", width=28
        )
        box.grid(row=row, column=col + 1, sticky="ew", padx=6, pady=5)

    def choose_photo(self):
        path = filedialog.askopenfilename(
            title="Select Inspection Photograph",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.webp"),
                ("All files", "*.*")
            ]
        )
        if path:
            self.photo_path = path
            self.photo_label.config(text=Path(path).name)

    def add_observation(self):
        if not self.bridge_id_var.get().strip():
            messagebox.showwarning("Missing Information", "Enter a Bridge ID.")
            return

        if not self.span_var.get().strip():
            messagebox.showwarning("Missing Information", "Enter span / chainage.")
            return

        if not self.location_var.get().strip():
            messagebox.showwarning("Missing Information", "Enter the observation location.")
            return

        severity = self.severity_var.get()
        score = SEVERITY_SCORE[severity]

        if severity == "Severe":
            priority = "URGENT"
        elif severity == "Moderate":
            priority = "HIGH"
        elif severity == "Minor":
            priority = "ROUTINE"
        else:
            priority = "NONE"

        record = {
            "bridge_id": self.bridge_id_var.get().strip(),
            "inspection_date": self.date_var.get().strip(),
            "inspector": self.inspector_var.get().strip(),
            "weather": self.weather_var.get().strip(),
            "span": self.span_var.get().strip(),
            "component": self.component_var.get(),
            "location": self.location_var.get().strip(),
            "defect": self.defect_var.get(),
            "severity": severity,
            "score": score,
            "priority": priority,
            "remarks": self.remarks_var.get().strip(),
            "photo": self.photo_path
        }

        self.records.append(record)
        self.refresh_table()

        # Reset observation-only fields
        self.span_var.set("")
        self.location_var.set("")
        self.remarks_var.set("")
        self.photo_path = ""
        self.photo_label.config(text="No photo selected")
        self.severity_var.set("Good")
        self.status.set(f"Observation {len(self.records)} added successfully.")

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for i, r in enumerate(self.records, 1):
            self.tree.insert(
                "", "end",
                values=(
                    i, r["span"], r["component"], r["location"],
                    r["defect"], r["severity"], r["score"], r["priority"]
                )
            )

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Delete", "Select an observation first.")
            return

        indexes = sorted(
            [self.tree.index(item) for item in selected], reverse=True
        )
        for idx in indexes:
            del self.records[idx]

        self.refresh_table()
        self.status.set("Selected observation(s) deleted.")

    def clear_all(self):
        if not self.records:
            return

        if messagebox.askyesno(
            "Clear All", "Delete all recorded observations?"
        ):
            self.records.clear()
            self.refresh_table()
            self.status.set("All observations cleared.")

    def export_csv(self):
        if not self.records:
            messagebox.showinfo("Export", "No observations to export.")
            return

        path = filedialog.asksaveasfilename(
            title="Save Inspection Records",
            defaultextension=".csv",
            filetypes=[("CSV file", "*.csv")]
        )
        if not path:
            return

        fields = [
            "bridge_id", "inspection_date", "inspector", "weather",
            "span", "component", "location", "defect", "severity",
            "score", "priority", "remarks", "photo"
        ]

        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(self.records)

        messagebox.showinfo("Export Complete", f"Records exported to:\n{path}")

    def show_dashboard(self):
        if not self.records:
            messagebox.showinfo("Dashboard", "No observations have been recorded.")
            return

        dashboard = tk.Toplevel(self.root)
        dashboard.title("RCC Bridge Condition Dashboard")
        dashboard.geometry("1050x720")

        ttk.Label(
            dashboard, text="RCC T-BEAM BRIDGE — CONDITION DASHBOARD",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=(15, 3))

        ttk.Label(
            dashboard,
            text=f"Bridge: {self.bridge_id_var.get()}   |   Inspection: {self.date_var.get()}",
            font=("Segoe UI", 10)
        ).pack(pady=(0, 12))

        # KPI cards
        kpi = tk.Frame(dashboard)
        kpi.pack(fill="x", padx=20)

        total = len(self.records)
        avg = sum(r["score"] for r in self.records) / total
        urgent = sum(1 for r in self.records if r["priority"] == "URGENT")
        high = sum(1 for r in self.records if r["priority"] == "HIGH")

        cards = [
            ("TOTAL OBSERVATIONS", str(total)),
            ("AVERAGE SCORE", f"{avg:.2f}/4"),
            ("HIGH PRIORITY", str(high)),
            ("URGENT", str(urgent)),
        ]

        for title, value in cards:
            frame = ttk.LabelFrame(kpi, text=title, padding=12)
            frame.pack(side="left", fill="both", expand=True, padx=5)
            ttk.Label(
                frame, text=value, font=("Segoe UI", 20, "bold")
            ).pack()

        # Dashboard body
        body = tk.Frame(dashboard)
        body.pack(fill="both", expand=True, padx=20, pady=15)

        # Condition distribution
        left = ttk.LabelFrame(body, text="Condition Distribution", padding=12)
        left.pack(side="left", fill="both", expand=True, padx=(0, 8))

        counts = {s: 0 for s in SEVERITY_SCORE}
        for r in self.records:
            counts[r["severity"]] += 1

        max_count = max(counts.values()) if counts else 1

        for severity, count in counts.items():
            row = tk.Frame(left)
            row.pack(fill="x", pady=8)

            ttk.Label(row, text=severity, width=12).pack(side="left")

            bar = tk.Canvas(row, height=24, highlightthickness=0)
            bar.pack(side="left", fill="x", expand=True, padx=5)

            # Draw a simple horizontal bar without hard-coded colors.
            width = max(1, int(280 * count / max_count))
            bar.create_rectangle(2, 2, width, 22)
            bar.create_text(
                width + 18, 12, text=str(count),
                anchor="w", font=("Segoe UI", 10, "bold")
            )

        # Component condition
        right = ttk.LabelFrame(body, text="Component-wise Condition", padding=12)
        right.pack(side="right", fill="both", expand=True, padx=(8, 0))

        component_data = {}
        for r in self.records:
            component_data.setdefault(r["component"], []).append(r["score"])

        columns = ("Component", "Observations", "Avg Score", "Status")
        comp_tree = ttk.Treeview(right, columns=columns, show="headings", height=13)

        for c in columns:
            comp_tree.heading(c, text=c)

        comp_tree.column("Component", width=220)
        comp_tree.column("Observations", width=90, anchor="center")
        comp_tree.column("Avg Score", width=90, anchor="center")
        comp_tree.column("Status", width=120, anchor="center")

        for component, scores in sorted(component_data.items()):
            component_avg = sum(scores) / len(scores)
            if component_avg <= 1.5:
                status = "GOOD"
            elif component_avg <= 2.5:
                status = "MINOR"
            elif component_avg <= 3.5:
                status = "MODERATE"
            else:
                status = "SEVERE"

            comp_tree.insert(
                "", "end",
                values=(component, len(scores), f"{component_avg:.2f}", status)
            )

        comp_tree.pack(fill="both", expand=True)

        # Bridge schematic
        schematic = ttk.LabelFrame(dashboard, text="Bridge Defect Location Schematic", padding=8)
        schematic.pack(fill="x", padx=20, pady=(0, 12))

        canvas = tk.Canvas(schematic, height=145, highlightthickness=0)
        canvas.pack(fill="x")

        w = 960
        x0, x1 = 60, 900
        y_deck = 38
        y_base = 110

        # Deck and girders
        canvas.create_line(x0, y_deck, x1, y_deck, width=5)
        for x in [160, 360, 560, 760]:
            canvas.create_line(x, y_deck, x, y_base, width=4)
            canvas.create_line(x - 18, y_base, x + 18, y_base, width=5)

        # Span labels
        spans = [("S1", 110), ("S2", 260), ("S3", 460), ("S4", 660), ("S5", 830)]
        for label, x in spans:
            canvas.create_text(x, 72, text=label, font=("Segoe UI", 9, "bold"))

        # Plot observation markers along spans according to severity.
        for i, r in enumerate(self.records):
            span_text = r["span"].lower()
            number = 1
            for token in span_text.replace("-", " ").split():
                digits = "".join(ch for ch in token if ch.isdigit())
                if digits:
                    number = max(1, min(5, int(digits)))
                    break

            x = spans[number - 1][1]
            offset = (i % 4) * 14
            y = 20 + offset

            canvas.create_oval(
                x - 6, y - 6, x + 6, y + 6,
                outline="black", width=2
            )
            canvas.create_text(
                x + 12, y, text=str(i + 1),
                anchor="w", font=("Segoe UI", 8, "bold")
            )

        ttk.Label(
            schematic,
            text="Numbered markers correspond to observations in the recorded-observations table."
        ).pack(anchor="w", padx=5)

        ttk.Label(
            dashboard,
            text="Engineering note: this dashboard documents observed condition; it does not establish structural safety.",
            font=("Segoe UI", 9, "italic")
        ).pack(pady=(0, 12))

    def show_summary(self):
        if not self.records:
            messagebox.showinfo("Summary", "No observations have been recorded.")
            return

        total = len(self.records)
        total_score = sum(r["score"] for r in self.records)
        avg_score = total_score / total

        counts = {s: 0 for s in SEVERITY_SCORE}
        for r in self.records:
            counts[r["severity"]] += 1

        severe_components = [
            r["component"] for r in self.records if r["severity"] == "Severe"
        ]
        moderate_components = [
            r["component"] for r in self.records if r["severity"] == "Moderate"
        ]

        if avg_score <= 1.5:
            overall = "GOOD"
        elif avg_score <= 2.5:
            overall = "MINOR"
        elif avg_score <= 3.5:
            overall = "MODERATE"
        else:
            overall = "SEVERE"

        summary = tk.Toplevel(self.root)
        summary.title("Bridge Inspection Summary")
        summary.geometry("720x600")

        tk.Label(
            summary, text="INSPECTION SUMMARY",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=(15, 5))

        info_text = (
            f"Bridge ID: {self.bridge_id_var.get()}\n"
            f"Inspection Date: {self.date_var.get()}\n"
            f"Total Observations: {total}\n"
            f"Average Condition Score: {avg_score:.2f} / 4\n"
            f"Overall Observed Condition: {overall}"
        )

        tk.Label(
            summary, text=info_text, justify="left",
            font=("Segoe UI", 11)
        ).pack(anchor="w", padx=30, pady=12)

        counts_frame = ttk.LabelFrame(summary, text="Condition Distribution", padding=12)
        counts_frame.pack(fill="x", padx=25, pady=8)

        for severity, count in counts.items():
            ttk.Label(
                counts_frame,
                text=f"{severity}: {count} observation(s)"
            ).pack(anchor="w", pady=2)

        priority_frame = ttk.LabelFrame(
            summary, text="Engineering Interpretation", padding=12
        )
        priority_frame.pack(fill="both", expand=True, padx=25, pady=8)

        if severe_components:
            recommendation = (
                "URGENT ATTENTION:\n"
                + ", ".join(dict.fromkeys(severe_components))
                + "\n\n"
                "Recommend detailed investigation. NDT/material testing or "
                "structural assessment may be considered as appropriate."
            )
        elif moderate_components:
            recommendation = (
                "PRIORITY ATTENTION:\n"
                + ", ".join(dict.fromkeys(moderate_components))
                + "\n\n"
                "Recommend detailed inspection and timely corrective action."
            )
        else:
            recommendation = (
                "No severe or moderate observations recorded.\n\n"
                "Continue routine maintenance, monitoring and periodic inspection."
            )

        tk.Label(
            priority_frame, text=recommendation,
            justify="left", wraplength=620,
            font=("Segoe UI", 11)
        ).pack(anchor="w")

        tk.Label(
            summary,
            text="Note: Visual inspection alone does not establish structural safety.",
            font=("Segoe UI", 9, "italic")
        ).pack(pady=12)


if __name__ == "__main__":
    root = tk.Tk()
    try:
        style = ttk.Style()
        if "vista" in style.theme_names():
            style.theme_use("vista")
    except Exception:
        pass
    app = BridgeInspectionApp(root)
    root.mainloop()
