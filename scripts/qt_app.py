#!/usr/bin/env python
"""Qt desktop app for Help Your Gaeltacht."""

import os
import sys
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from help_your_gaeltacht.data_loader import load_custom_town_list
from help_your_gaeltacht.glossary import generate_glossary
from help_your_gaeltacht.heritage import query_heritage_assets
from help_your_gaeltacht.nearest_towns import find_nearest_towns
from help_your_gaeltacht.nlp_agent import (
    configure_client,
    process_natural_language_query,
    search_info,
)
from help_your_gaeltacht.poi import find_pubs_near_location


class SearchWorker:
    def __init__(self, features, user_input, api_key):
        self.features = features
        self.user_input = user_input
        self.api_key = api_key

    def build_result_text(self):
        configure_client(self.api_key)
        params = process_natural_language_query(self.user_input)

        if "error" in params:
            return f"Agent: Error - {params['error']}"

        if "search_query" in params:
            search_result = search_info(params["search_query"])
            return f"Search results for '{params['search_query']}':\n\n{search_result}"

        nearest = find_nearest_towns(
            self.features,
            (params["lat"], params["lon"]),
            limit=params["limit"],
        )
        if not nearest:
            return f"Agent: No Gaeltacht towns found near {params['county']}."

        lines = [f"Found {len(nearest)} Gaeltacht town(s) near {params['county']}:", ""]
        for town in nearest:
            lines.append(f"- {town['name']} ({town['distance_km']} km)")

            if params["find_pubs"]:
                try:
                    pubs = find_pubs_near_location(
                        town["latitude"],
                        town["longitude"],
                        radius_m=params["pub_radius"],
                        limit=params["pub_limit"],
                    )
                    if pubs:
                        lines.append("  Pubs:")
                        for pub in pubs:
                            lines.append(f"    - {pub['name']} ({pub['distance_km']} km)")
                    else:
                        lines.append("  No pubs found nearby")
                except Exception as exc:
                    lines.append(f"  Pub search failed: {exc}")

            if params["find_heritage"]:
                try:
                    heritage = query_heritage_assets(
                        town["latitude"],
                        town["longitude"],
                        radius_km=params["heritage_radius"],
                        limit=params["heritage_limit"],
                    )
                    if heritage:
                        lines.append("  Heritage sites:")
                        for site in heritage:
                            lines.append(f"    - {site['name']} ({site['distance_km']} km)")
                    else:
                        lines.append("  No heritage sites found nearby")
                except Exception as exc:
                    lines.append(f"  Heritage search failed: {exc}")

        glossary = generate_glossary(nearest)
        if glossary.get("terms"):
            lines.extend(["", "Irish words from these place names:"])
            for irish, english in glossary["terms"]:
                lines.append(f"- {irish}: {english}")

        if glossary.get("expressions"):
            lines.extend(["", "Useful Irish expressions:"])
            for irish, english in glossary["expressions"]:
                lines.append(f"- {irish}: {english}")

        return "\n".join(lines)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Help Your Gaeltacht")
        self.resize(900, 700)

        dataset_path = ROOT / "datasets" / "gael_towns.geojson"
        self.features = load_custom_town_list(dataset_path)
        self.search_in_progress = False

        container = QWidget()
        layout = QVBoxLayout(container)

        title = QLabel("Help Your Gaeltacht")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        subtitle = QLabel(
            "Search for Gaeltacht towns, pubs, heritage sites, volunteering opportunities, and Irish expressions."
        )
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)

        key_row = QHBoxLayout()
        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("Enter your Gemini API key")
        self.api_key_input.setEchoMode(QLineEdit.Password)
        existing_key = os.getenv("GEMINI_API_KEY", "").strip()
        if existing_key:
            self.api_key_input.setText(existing_key)
        self.connect_button = QPushButton("Set API Key")
        self.connect_button.clicked.connect(self.set_api_key)
        key_row.addWidget(self.api_key_input)
        key_row.addWidget(self.connect_button)
        layout.addLayout(key_row)

        self.query_input = QLineEdit()
        self.query_input.setPlaceholderText("Try: heritage sites in Galway")
        layout.addWidget(self.query_input)

        options = QHBoxLayout()
        self.pubs_checkbox = QCheckBox("Include pubs")
        self.heritage_checkbox = QCheckBox("Include heritage")
        self.volunteer_checkbox = QCheckBox("Include volunteers")
        options.addWidget(self.pubs_checkbox)
        options.addWidget(self.heritage_checkbox)
        options.addWidget(self.volunteer_checkbox)
        options.addStretch()
        layout.addLayout(options)

        actions = QHBoxLayout()
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.run_search)
        actions.addWidget(self.search_button)
        actions.addStretch()
        layout.addLayout(actions)

        self.results = QTextEdit()
        self.results.setReadOnly(True)
        layout.addWidget(self.results)

        self.setCentralWidget(container)

    def set_api_key(self):
        api_key = self.api_key_input.text().strip()
        if not api_key:
            QMessageBox.warning(self, "Missing API key", "Enter your Gemini API key first.")
            return

        try:
            os.environ["GEMINI_API_KEY"] = api_key
            configure_client(api_key)
        except Exception as exc:
            QMessageBox.critical(self, "API key error", f"Could not configure Gemini:\n\n{exc}")
            return

        QMessageBox.information(self, "API key set", "Gemini API key configured for this session.")

    def run_search(self):
        if self.search_in_progress:
            QMessageBox.information(self, "Search running", "Please wait for the current search to finish.")
            return

        query = self.query_input.text().strip()
        if not query:
            QMessageBox.warning(self, "Missing query", "Enter a county or natural language question.")
            return

        api_key = self.api_key_input.text().strip()
        if not api_key:
            QMessageBox.warning(self, "Missing API key", "Set your Gemini API key before searching.")
            return

        decorated_query = query
        extras = []
        if self.pubs_checkbox.isChecked():
            extras.append("with pubs nearby")
        if self.heritage_checkbox.isChecked():
            extras.append("with heritage sites")
        if self.volunteer_checkbox.isChecked():
            extras.append("with volunteer opportunities")
        if extras and query.lower() not in ("quit", "exit"):
            decorated_query = f"{query} {' '.join(extras)}"

        self.search_button.setEnabled(False)
        self.results.setPlainText("Searching...")
        QApplication.processEvents()
        self.search_in_progress = True

        try:
            worker = SearchWorker(self.features, decorated_query, api_key)
            text = worker.build_result_text()
            self.results.setPlainText(text)
        except Exception as exc:
            self.results.setPlainText(f"Search failed:\n\n{exc}")
        finally:
            self.search_button.setEnabled(True)
            self.search_in_progress = False


def prompt_for_api_key():
    return True


def main():
    app = QApplication(sys.argv)
    prompt_for_api_key()

    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
