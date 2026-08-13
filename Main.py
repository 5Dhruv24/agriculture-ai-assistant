"""
🌾 AI Crop Companion Prototype
--------------------------------
A beginner-friendly desktop app built with pure Python (tkinter/ttk).

How to run:
1. Copy this entire file into Python IDLE (or save it as a .py file).
2. Press F5 (or run: python ai_crop_companion.py)
3. No extra installs needed — only the Python standard library is used.
"""

import tkinter as tk
from tkinter import ttk


# ---------------------------------------------------------------------------
# MOCK DATA
# ---------------------------------------------------------------------------

CROP_DATA = {
    "Wheat": {
        "temperature": "10°C - 25°C",
        "water": "450 - 650 mm per season",
        "soil": "Well-drained loamy soil",
        "duration": "110 - 130 days",
        "stages": ["Sowing", "Germination", "Tillering / Vegetative", "Flowering", "Harvest"],
    },
    "Rice": {
        "temperature": "20°C - 35°C",
        "water": "900 - 1200 mm per season (needs standing water)",
        "soil": "Clayey soil that retains water well",
        "duration": "100 - 150 days",
        "stages": ["Sowing / Transplanting", "Germination", "Vegetative", "Flowering", "Harvest"],
    },
    "Maize": {
        "temperature": "18°C - 27°C",
        "water": "500 - 800 mm per season",
        "soil": "Well-drained sandy loam soil",
        "duration": "90 - 120 days",
        "stages": ["Sowing", "Germination", "Vegetative", "Tasseling / Silking", "Harvest"],
    },
}

# Mock weather data keyed by location (falls back to a default if not found)
WEATHER_DATA = {
    "Delhi": {"temp": "28°C", "condition": "Partly Cloudy", "humidity": "65%", "rain_prob": 70},
    "Mumbai": {"temp": "31°C", "condition": "Light Rain", "humidity": "80%", "rain_prob": 85},
    "Bengaluru": {"temp": "24°C", "condition": "Clear Sky", "humidity": "55%", "rain_prob": 20},
    "Chennai": {"temp": "33°C", "condition": "Humid & Sunny", "humidity": "70%", "rain_prob": 40},
    "Kolkata": {"temp": "30°C", "condition": "Thunderstorms", "humidity": "78%", "rain_prob": 75},
}

DEFAULT_WEATHER = {"temp": "27°C", "condition": "Mostly Sunny", "humidity": "60%", "rain_prob": 30}


# ---------------------------------------------------------------------------
# COLOR / STYLE CONSTANTS
# ---------------------------------------------------------------------------

BG_COLOR = "#F4F7F2"
CARD_COLOR = "#FFFFFF"
PRIMARY_COLOR = "#2E7D32"       # deep green
PRIMARY_DARK = "#1B5E20"
ACCENT_COLOR = "#F9A825"        # warm yellow accent
TEXT_COLOR = "#263238"
SUBTEXT_COLOR = "#607D8B"
BORDER_COLOR = "#C8D6C0"

FONT_TITLE = ("Segoe UI", 20, "bold")
FONT_HEADER = ("Segoe UI", 15, "bold")
FONT_LABEL = ("Segoe UI", 11)
FONT_LABEL_BOLD = ("Segoe UI", 11, "bold")
FONT_BUTTON = ("Segoe UI", 11, "bold")
FONT_SMALL = ("Segoe UI", 9)


# ---------------------------------------------------------------------------
# MAIN APPLICATION
# ---------------------------------------------------------------------------

class CropCompanionApp(tk.Tk):
    """Main application window that manages screen switching."""

    def __init__(self):
        super().__init__()

        self.title("🌾 AI Crop Companion Prototype")
        self.geometry("720x620")
        self.minsize(640, 560)
        self.configure(bg=BG_COLOR)

        # Shared application state (read by all screens)
        self.selected_crop = tk.StringVar(value="Wheat")
        self.selected_location = tk.StringVar(value="Delhi")

        self._setup_styles()

        # Container that holds every screen (frame), stacked on top of each other
        container = tk.Frame(self, bg=BG_COLOR)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for ScreenClass in (HomeScreen, CropInfoScreen, WeatherScreen, AskAIScreen):
            frame = ScreenClass(parent=container, controller=self)
            self.frames[ScreenClass.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_screen("HomeScreen")

    def _setup_styles(self):
        style = ttk.Style(self)
        # 'clam' theme allows more custom color control across platforms
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("TCombobox", padding=4, font=FONT_LABEL)
        style.configure(
            "Nav.TButton",
            font=FONT_BUTTON,
            padding=10,
            background=PRIMARY_COLOR,
            foreground="white",
        )
        style.map(
            "Nav.TButton",
            background=[("active", PRIMARY_DARK)],
            foreground=[("active", "white")],
        )

        style.configure(

            "Back.TButton",
            font=FONT_LABEL_BOLD,
            padding=6,
            background=SUBTEXT_COLOR,
            foreground="white",

        )
        style.map("Back.TButton", background=[("active", "#455A64")])

        style.configure(
            "Send.TButton",
            font=FONT_BUTTON,
            padding=8,
            background=ACCENT_COLOR,
            foreground=TEXT_COLOR,
        )
        style.map("Send.TButton", background=[("active", "#F57F17")])

    def show_screen(self, screen_name):
        """Raise the requested screen to the top and refresh its data."""
        frame = self.frames[screen_name]
        if hasattr(frame, "refresh"):
            frame.refresh()
        frame.tkraise()


# ---------------------------------------------------------------------------
# REUSABLE UI HELPERS
# ---------------------------------------------------------------------------

def make_card(parent, **pack_kwargs):
    """Creates a white 'card' frame with a subtle border, ready to pack."""
    outer = tk.Frame(parent, bg=BORDER_COLOR, padx=1, pady=1)
    inner = tk.Frame(outer, bg=CARD_COLOR, padx=18, pady=16)
    inner.pack(fill="both", expand=True)
    outer.pack(**pack_kwargs)
    return inner


def make_back_button(parent, controller):
    bar = tk.Frame(parent, bg=BG_COLOR)
    bar.pack(fill="x", padx=20, pady=(16, 6))
    back_btn = ttk.Button(
        bar,
        text="⬅ Back to Home",
        style="Back.TButton",
        command=lambda: controller.show_screen("HomeScreen"),
    )
    back_btn.pack(side="left")
    return bar


def section_title(parent, text):
    lbl = tk.Label(parent, text=text, font=FONT_HEADER, bg=CARD_COLOR, fg=PRIMARY_DARK)
    lbl.pack(anchor="w", pady=(0, 10))
    return lbl


def info_row(parent, emoji_label, value_text):
    row = tk.Frame(parent, bg=CARD_COLOR)
    row.pack(fill="x", pady=4)
    tk.Label(
        row, text=emoji_label, font=FONT_LABEL_BOLD, bg=CARD_COLOR, fg=TEXT_COLOR, anchor="w"
    ).pack(side="left")
    tk.Label(
        row, text=value_text, font=FONT_LABEL, bg=CARD_COLOR, fg=SUBTEXT_COLOR,
        anchor="w", wraplength=380, justify="left"
    ).pack(side="left", padx=(6, 0))
    return row


# ---------------------------------------------------------------------------
# SCREEN 1: HOME
# ---------------------------------------------------------------------------

class HomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller

        # ---- Header ----
        header = tk.Label(
            self,
            text="🌾 AI Crop Companion Prototype",
            font=FONT_TITLE,
            bg=BG_COLOR,
            fg=PRIMARY_DARK,
            pady=20,
        )
        header.pack(fill="x")

        subtitle = tk.Label(
            self,
            text="Smart insights for your crop, weather, and farming questions.",
            font=FONT_LABEL,
            bg=BG_COLOR,
            fg=SUBTEXT_COLOR,
        )
        subtitle.pack(pady=(0, 20))

        # ---- Input Card ----
        card = make_card(self, pady=10, padx=40, fill="x")

        section_title(card, "📋 Your Farm Details")

        # Crop dropdown
        crop_row = tk.Frame(card, bg=CARD_COLOR)
        crop_row.pack(fill="x", pady=8)
        tk.Label(
            crop_row, text="Select Crop:", font=FONT_LABEL_BOLD, bg=CARD_COLOR, fg=TEXT_COLOR, width=16, anchor="w"
        ).pack(side="left")
        crop_dropdown = ttk.Combobox(
            crop_row,
            textvariable=controller.selected_crop,
            values=["Wheat", "Rice", "Maize"],
            state="readonly",
            font=FONT_LABEL,
            width=25,
        )
        crop_dropdown.pack(side="left", fill="x", expand=True)

        # Location field (editable dropdown with common cities + free typing)
        loc_row = tk.Frame(card, bg=CARD_COLOR)
        loc_row.pack(fill="x", pady=8)
        tk.Label(
            loc_row, text="Location:", font=FONT_LABEL_BOLD, bg=CARD_COLOR, fg=TEXT_COLOR, width=16, anchor="w"
        ).pack(side="left")
        location_entry = ttk.Combobox(
            loc_row,
            textvariable=controller.selected_location,
            values=["Delhi", "Mumbai", "Bengaluru", "Chennai", "Kolkata"],
            font=FONT_LABEL,
            width=25,
        )
        location_entry.pack(side="left", fill="x", expand=True)

        # ---- Navigation Buttons ----
        nav_card = tk.Frame(self, bg=BG_COLOR)
        nav_card.pack(pady=30, padx=40, fill="x")

        btn1 = ttk.Button(
            nav_card, text="🌱 Crop Information", style="Nav.TButton",
            command=lambda: controller.show_screen("CropInfoScreen"),
        )
        btn1.pack(fill="x", pady=6)

        btn2 = ttk.Button(
            nav_card, text="🌦️ Weather", style="Nav.TButton",
            command=lambda: controller.show_screen("WeatherScreen"),
        )
        btn2.pack(fill="x", pady=6)

        btn3 = ttk.Button(
            nav_card, text="🤖 Ask AI", style="Nav.TButton",
            command=lambda: controller.show_screen("AskAIScreen"),
        )
        btn3.pack(fill="x", pady=6)

        footer = tk.Label(
            self,
            text="Prototype for educational/demo purposes • Data shown is mock/sample data",
            font=FONT_SMALL,
            bg=BG_COLOR,
            fg=SUBTEXT_COLOR,
        )
        footer.pack(side="bottom", pady=12)


# ---------------------------------------------------------------------------
# SCREEN 2: CROP INFORMATION
# ---------------------------------------------------------------------------

class CropInfoScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller

        make_back_button(self, controller)

        self.title_label = tk.Label(
            self, text="", font=FONT_TITLE, bg=BG_COLOR, fg=PRIMARY_DARK
        )
        self.title_label.pack(pady=(0, 16))

        self.card = make_card(self, padx=40, pady=10, fill="both", expand=True)

    def refresh(self):
        """Redraw the crop details based on the currently selected crop."""
        for widget in self.card.winfo_children():
            widget.destroy()

        crop = self.controller.selected_crop.get()
        data = CROP_DATA.get(crop, CROP_DATA["Wheat"])

        self.title_label.config(text=f"🌱 Crop Information — {crop}")

        section_title(self.card, "📊 Key Requirements")
        info_row(self.card, "🌡️ Ideal Temperature:", data["temperature"])
        info_row(self.card, "💧 Water Requirement:", data["water"])
        info_row(self.card, "🌱 Ideal Soil Type:", data["soil"])
        info_row(self.card, "📅 Growth Duration:", data["duration"])

        tk.Frame(self.card, bg=BORDER_COLOR, height=1).pack(fill="x", pady=14)

        section_title(self.card, "🌿 Growth Stages")
        stages_text = "  →  ".join(data["stages"])
        tk.Label(
            self.card,
            text=stages_text,
            font=FONT_LABEL_BOLD,
            bg=CARD_COLOR,
            fg=PRIMARY_COLOR,
            wraplength=560,
            justify="left",
        ).pack(anchor="w", pady=4)

        # Numbered stage list for extra clarity
        stage_list_frame = tk.Frame(self.card, bg=CARD_COLOR)
        stage_list_frame.pack(fill="x", pady=(10, 0), anchor="w")
        for i, stage in enumerate(data["stages"], start=1):
            tk.Label(
                stage_list_frame,
                text=f"{i}. {stage}",
                font=FONT_LABEL,
                bg=CARD_COLOR,
                fg=SUBTEXT_COLOR,
                anchor="w",
            ).pack(anchor="w", pady=2)


# ---------------------------------------------------------------------------
# SCREEN 3: WEATHER + ADVICE
# ---------------------------------------------------------------------------

class WeatherScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller

        make_back_button(self, controller)

        self.title_label = tk.Label(
            self, text="", font=FONT_TITLE, bg=BG_COLOR, fg=PRIMARY_DARK
        )
        self.title_label.pack(pady=(0, 16))

        self.card = make_card(self, padx=40, pady=10, fill="x")

        self.suggestion_outer = tk.Frame(self, bg=ACCENT_COLOR, padx=1, pady=1)
        self.suggestion_inner = tk.Frame(self.suggestion_outer, bg="#FFF8E1", padx=20, pady=16)
        self.suggestion_inner.pack(fill="both", expand=True)
        self.suggestion_outer.pack(padx=40, pady=20, fill="x")

    def refresh(self):
        for widget in self.card.winfo_children():
            widget.destroy()
        for widget in self.suggestion_inner.winfo_children():
            widget.destroy()

        location = self.controller.selected_location.get().strip() or "Delhi"
        weather = WEATHER_DATA.get(location, DEFAULT_WEATHER)

        self.title_label.config(text=f" Weather — {location}")

        section_title(self.card, " Current Conditions")
        info_row(self.card, "Temperature:", weather["temp"])
        info_row(self.card, " Condition:", weather["condition"])
        info_row(self.card, " Humidity:", weather["humidity"])
        info_row(self.card, " Rain Probability:", f"{weather['rain_prob']}%")

        # Dynamic advice logic
        rain_prob = weather["rain_prob"]
        if rain_prob > 50:
            advice = "🌧️ Rain is expected today, so irrigation may not be necessary."
        else:
            advice = "☀️ Weather is clear. Normal irrigation recommended."

        tk.Label(
            self.suggestion_inner,
            text="💡 Today's Suggestion",
            font=FONT_HEADER,
            bg="#FFF8E1",
            fg="#E65100",
        ).pack(anchor="w", pady=(0, 8))

        tk.Label(
            self.suggestion_inner,
            text=advice,
            font=FONT_LABEL_BOLD,
            bg="#FFF8E1",
            fg=TEXT_COLOR,
            wraplength=560,
            justify="left",
        ).pack(anchor="w")


# ---------------------------------------------------------------------------
# SCREEN 4: ASK AI
# ---------------------------------------------------------------------------

class AskAIScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller

        make_back_button(self, controller)

        self.title_label = tk.Label(
            self, text="🤖 Ask AI", font=FONT_TITLE, bg=BG_COLOR, fg=PRIMARY_DARK
        )
        self.title_label.pack(pady=(0, 16))

        # Chat output area
        chat_outer = tk.Frame(self, bg=BORDER_COLOR, padx=1, pady=1)
        chat_outer.pack(padx=40, pady=(0, 10), fill="both", expand=True)

        chat_frame = tk.Frame(chat_outer, bg=CARD_COLOR)
        chat_frame.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(chat_frame)
        scrollbar.pack(side="right", fill="y")

        self.chat_box = tk.Text(
            chat_frame,
            wrap="word",
            font=FONT_LABEL,
            bg=CARD_COLOR,
            fg=TEXT_COLOR,
            relief="flat",
            padx=12,
            pady=10,
            state="disabled",
            yscrollcommand=scrollbar.set,
        )
        self.chat_box.pack(fill="both", expand=True)
        scrollbar.config(command=self.chat_box.yview)

        # Text tags for styling chat bubbles
        self.chat_box.tag_configure("user", foreground=PRIMARY_DARK, font=FONT_LABEL_BOLD, spacing1=6)
        self.chat_box.tag_configure("ai", foreground=SUBTEXT_COLOR, font=FONT_LABEL, spacing3=10)

        # Input area
        input_row = tk.Frame(self, bg=BG_COLOR)
        input_row.pack(fill="x", padx=40, pady=(0, 20))

        tk.Label(
            input_row, text="Ask anything about your crop...", font=FONT_LABEL,
            bg=BG_COLOR, fg=SUBTEXT_COLOR
        ).pack(anchor="w", pady=(0, 6))

        entry_row = tk.Frame(input_row, bg=BG_COLOR)
        entry_row.pack(fill="x")

        self.question_entry = ttk.Entry(entry_row, font=FONT_LABEL)
        self.question_entry.pack(side="left", fill="x", expand=True, ipady=4)
        self.question_entry.bind("<Return>", lambda event: self.send_question())

        send_btn = ttk.Button(
            entry_row, text="Send ➤", style="Send.TButton", command=self.send_question
        )
        send_btn.pack(side="left", padx=(8, 0))

    def refresh(self):
        # Welcome message only shown once (if chat is empty)
        self.chat_box.config(state="normal")
        if self.chat_box.get("1.0", "end").strip() == "":
            crop = self.controller.selected_crop.get()
            self._append_message(
                "ai",
                f"🤖 AI: Hello! I'm ready to help with your {crop} crop. "
                f"Ask me about soil, water, temperature, or growth stages!",
            )
        self.chat_box.config(state="disabled")

    def send_question(self):
        question = self.question_entry.get().strip()
        if not question:
            return

        self._append_message("user", f"🧑 You: {question}")
        answer = self._generate_mock_answer(question)
        self._append_message("ai", f"🤖 AI: {answer}")

        self.question_entry.delete(0, "end")

    def _generate_mock_answer(self, question):
        crop = self.controller.selected_crop.get()
        data = CROP_DATA.get(crop, CROP_DATA["Wheat"])
        q = question.lower()

        if "soil" in q:
            return f"For {crop}, the ideal soil type is: {data['soil']}."
        elif "water" in q:
            return f"For {crop}, the water requirement is approximately {data['water']}."
        elif "temperature" in q or "temp" in q:
            return f"For {crop}, the ideal temperature range is {data['temperature']}."
        elif "growth" in q or "stage" in q:
            stages = " → ".join(data["stages"])
            return f"The growth stages for {crop} are: {stages}."
        else:
            return (
                f"Regarding {crop}: Ensure proper nutrient management and "
                f"soil moisture during this stage."
            )

    def _append_message(self, tag, text):
        self.chat_box.config(state="normal")
        self.chat_box.insert("end", text + "\n", tag)
        self.chat_box.config(state="disabled")
        self.chat_box.see("end")


# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app = CropCompanionApp()
    app.mainloop()