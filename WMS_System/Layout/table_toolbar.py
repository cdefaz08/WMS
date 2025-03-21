from PyQt5.QtWidgets import QToolBar, QAction, QMessageBox

class TableToolbar(QToolBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Store references to the table and functions
        self.tableWidget = None
        self.save_callback = None
        self.reset_callback = None

        # Add New Record
        self.action_add = QAction("Add New", self)
        self.action_add.triggered.connect(self.add_new_record)
        self.addAction(self.action_add)

        # Delete Record
        self.action_delete = QAction("Delete", self)
        self.action_delete.triggered.connect(self.delete_selected_records)
        self.addAction(self.action_delete)

        # Discard Changes
        self.action_discard = QAction("Discard Changes", self)
        self.action_discard.triggered.connect(self.discard_changes)
        self.addAction(self.action_discard)

        # Save Changes
        self.action_save = QAction("Save", self)
        self.action_save.triggered.connect(self.save_changes)
        self.addAction(self.action_save)

    def set_table(self, table_widget):
        """Assign the QTableWidget to this toolbar."""
        self.tableWidget = table_widget

    def set_callbacks(self, save_callback, reset_callback):
        """Assign callbacks for save and reset functions."""
        self.save_callback = save_callback
        self.reset_callback = reset_callback

    def add_new_record(self):
        """Add a new blank row for a new record."""
        if not self.tableWidget:
            QMessageBox.warning(self, "Error", "No table assigned to the toolbar.")
            return

        row_count = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_count)

    def delete_selected_records(self):
        """Delete selected rows from the table."""
        if not self.tableWidget:
            QMessageBox.warning(self, "Error", "No table assigned to the toolbar.")
            return

        selected_rows = set(index.row() for index in self.tableWidget.selectionModel().selectedRows())
        
        if not selected_rows:
            QMessageBox.warning(self, "Error", "No rows selected for deletion.")
            return

        # Confirmation dialog
        confirm = QMessageBox.question(
            self, "Confirm Deletion", "Are you sure you want to delete the selected records?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            for row in sorted(selected_rows, reverse=True):
                self.tableWidget.removeRow(row)

    def discard_changes(self):
        """Trigger the reset callback if assigned."""
        if self.reset_callback:
            self.reset_callback()
        else:
            QMessageBox.warning(self, "Error", "No discard function assigned.")

    def save_changes(self):
        """Trigger the save callback if assigned."""
        if self.save_callback:
            self.save_callback()
        else:
            QMessageBox.warning(self, "Error", "No save function assigned.")
