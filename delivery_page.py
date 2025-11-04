"""
Delivery view for delivery management
Following Single Responsibility Principle and MVC pattern
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
QPushButton, QFrame, QGridLayout, QScrollArea, QApplication, QMainWindow, QDialog,
 QMessageBox, QFileDialog, QProgressBar, QSlider, QCheckBox,
  QRadioButton, QGroupBox, QFormLayout, QTabWidget, QSplitter,
   QMenuBar, QMenu, QSizePolicy, QStatusBar, QToolBar)
from PySide6.QtGui import QAction

from PySide6.QtCore import Qt, QTimer, Signal, QObject, QPropertyAnimation, QEasingCurve, QRect
from PySide6.QtGui import QFont, QPixmap, QPalette, QColor
import json
import os
from typing import List, Dict, Any, Optional
from app.core.interfaces import IThemeManager
from app.core.base_classes import BaseView, ThemeableMixin


class DeliveryView(BaseView, ThemeableMixin):
    """Delivery view for delivery management"""
    
    def __init__(self, parent, theme_manager: IThemeManager, app_controller, image_manager=None, **kwargs):
        BaseView.__init__(self, parent, **kwargs)
        ThemeableMixin.__init__(self)
        
        # Dependencies
        self._theme_manager = theme_manager
        self._app_controller = app_controller
        self._image_manager = image_manager
        
        # UI state
        self._current_page = 0
        self._buttons_per_page = 16
        self._max_columns = 4
        self._all_buttons = []
        self._current_button = None
        self._selected_location = None
        self._goal_location = None
        self._text_status = "Select Table \n Number"
        self._location_selected = False
        self._event_mode = False
        
        # Base and return location state
        self._return_base_location = "/home/pawan/pyside_app/app/Database/event_data.json"
        self._return_base_location_list = {}
        self._r_base_name = None
        self._r_base_cord = None
        self._return_loc_status = None
        
        # Event mode data
        self._event_type = "Birthday"
        self._guest_name = ""
        
        # Initialize view
        self._setup_theme()
        self._create_ui()
        self._load_delivery_locations()
        self._load_return_locations()
    
    def _get_themed_stylesheet(self, element_type: str, state: str = "normal") -> str:
        """Generate a stylesheet string for a themed element."""
        styles = {
            "frame": {
                "normal": f"background-color: {self.get_theme_color('frame_color')}; border-radius: 10px;",
                "white": f"background-color: {self.get_theme_color('white_frame')}; border-radius: 10px;",
            },
            "button": {
                "normal": f"""
                    QPushButton {{
                        background-color: {self.get_theme_color('button_color')};
                        color: white;
                        border-radius: 12px;
                        font-family: 'Montserrat';
                        font-size: 45px;
                    }}
                    QPushButton:hover {{
                        background-color: {self.get_theme_color('button_hover')};
                    }}
                    QPushButton:disabled {{
                        background-color: #8c8c8c;
                        color: #cccccc;
                    }}
                """,
                "selected": f"""
                    QPushButton {{
                        background-color: {self.get_theme_color('changing_button_fg')};
                        color: white;
                        border-radius: 12px;
                        font-family: 'Montserrat';
                        font-size: 45px;
                    }}
                    QPushButton:hover {{
                        background-color: {self.get_theme_color('button_hover')};
                    }}
                """,
                "start_delivery": f"""
                    QPushButton {{
                        background-color: {self.get_theme_color('button_color')};
                        color: white;
                        border-radius: 12px;
                        font-family: 'Montserrat';
                        font-size: 55px;
                    }}
                    QPushButton:hover {{
                        background-color: {self.get_theme_color('button_hover')};
                    }}
                    QPushButton:disabled {{
                        background-color: #8c8c8c;
                        color: #cccccc;
                    }}
                """,
                "nav_button": f"""
                    QPushButton {{
                        background-color: {self.get_theme_color('button_color')};
                        color: white;
                        border-radius: 8px;
                        font-family: 'Montserrat';
                        font-size: 40px;
                    }}
                    QPushButton:hover {{
                        background-color: {self.get_theme_color('button_hover')};
                    }}
                """,
                "edit_button": f"""
                    QPushButton {{
                        background-color: {self.get_theme_color('button_hover')};
                        color: white;
                        border-radius: 8px;
                        font-family: 'Montserrat';
                        font-size: 25px;
                    }}
                    QPushButton:hover {{
                        background-color: {self.get_theme_color('button_color')};
                    }}
                """,
                "base_event_button": f"""
                    QPushButton {{
                        background-color: {self.get_theme_color('button_color')};
                        color: white;
                        border-radius: 20px;
                        font-family: 'Montserrat';
                        font-size: 30px;
                    }}
                    QPushButton:hover {{
                        background-color: {self.get_theme_color('button_hover')};
                    }}
                """
            },
            "label": {
                "heading": f"color: {self.get_theme_color('grey_font_color')};",
                "normal": f"color: {self.get_theme_color('text_color')};",
                "selected": f"color: white;",
            }
        }
        return styles.get(element_type, {}).get(state, "")
    
    def _setup_theme(self) -> None:
        """Set up theme colors"""
        theme_colors = self._theme_manager.get_current_theme()
        self.set_theme_colors(theme_colors)
        
        # Apply theme to main_frame and upper_frame if they exist
        if hasattr(self, 'main_frame'):
            self.main_frame.setStyleSheet(self._get_themed_stylesheet("frame", "white"))
        if hasattr(self, 'upper_frame'):
            self.upper_frame.setStyleSheet(self._get_themed_stylesheet("frame"))   
            
             
    def _create_ui(self) -> None:
        """Create the user interface"""
        # Main container
        self.main_frame = QFrame(self)
        self.main_frame.setStyleSheet(self._get_themed_stylesheet("frame", "white"))
        
        # using VBoxLayout to remove any borders from the main_frame
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)
        outer_layout.addWidget(self.main_frame)

        # Layout for the main container so child sections stack vertically
        self.main_layout = QVBoxLayout(self.main_frame)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)
        
        # Let the main frame expand to fill available space
        self.main_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Create UI sections
        self._create_upper_frame()
        
        # HORIZONTAL SPLIT - Create body layout with left and right sections
        self.body_layout = QHBoxLayout()
        self.body_layout.setSpacing(20)
        
        # Create left and right sections
        self._create_info_section()  # Left panel
        self._create_button_section()  # Right panel
        
        # Add sections to body layout with proper width ratios
        self.body_layout.addWidget(self.info_frame, 1)  # Left gets 1 part
        self.body_layout.addWidget(self.button_container_frame, 3)  # Right gets 3 parts
        
        # Add body layout to main layout
        self.main_layout.addLayout(self.body_layout, 4)  # Give body most of the space
        
        # Create lower frame (Start Delivery button)
        self._create_lower_frame()


    
    def _create_upper_frame(self) -> None:
        """Create the upper frame with title and back button"""
        self.upper_frame = QFrame(self.main_frame)
        self.upper_frame.setStyleSheet(self._get_themed_stylesheet("frame"))
        self.upper_frame.setFixedHeight(120) #fixed height of header
        # Add to main vertical layout instead of relying on geometry
        if hasattr(self, 'main_layout'):
            self.main_layout.addWidget(self.upper_frame)
         
        # Layout for header
        # main layout where button AND label will be used 
        header_layout = QHBoxLayout(self.upper_frame)
        # places a margin of 20 pixels between outer and inner part of the widgets 
        header_layout.setContentsMargins(20, 0, 20, 0) # Add horizontal margins (left, top, right, bottom)
        # sets spacing between widgets inside HBoxLayout
        # header_layout.setSpacing(100)

        # Back button (visible and large enough)
        self.back_button = QPushButton("←", self.upper_frame)
        # size of the button widget
        self.back_button.setFixedSize(60, 60)

        self.back_button.setStyleSheet(self._get_themed_stylesheet("button", "nav_button"))
        self.back_button.clicked.connect(self._on_back) # connect to the slot on_back 
        header_layout.addWidget(self.back_button)  # add button to the hboxlayout
        header_layout.addStretch(1)

        # Title label
        self.title_label = QLabel("Delivery Mode", self.upper_frame)
        self.title_label.setFont(QFont("Montserrat", 30, QFont.Bold))
        self.title_label.setStyleSheet(self._get_themed_stylesheet("label", "heading"))
        # self.title_label.setAlignment(Qt.AlignCenter) # Center the title
        self.title_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        header_layout.addWidget(self.title_label)  # add label to the hboxlayout
        
        # Spacer at end
        header_layout.addStretch(1)
    
        # Button implemented for scrolling through Location Buttons 
    def _create_button_section(self) -> None:
        """Create the button section with location buttons and navigation"""
        # Button container frame
        self.button_container_frame = QFrame(self.main_frame)
        self.button_container_frame.setStyleSheet(self._get_themed_stylesheet("frame", "white"))
        self.button_container_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Use a vertical layout inside the container
        self.button_container_layout = QVBoxLayout(self.button_container_frame)
        self.button_container_layout.setContentsMargins(20, 20, 20, 20)
        self.button_container_layout.setSpacing(0)
        
        # Button frame for location buttons
        self.button_frame = QFrame(self.button_container_frame)
        self.button_frame.setStyleSheet("background-color: transparent;")
        self.button_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Qt grid layout for location buttons
        self.button_grid_layout = QGridLayout(self.button_frame)
        self.button_grid_layout.setSpacing(20)
        self.button_grid_layout.setContentsMargins(0, 0, 0, 0)
        
        # Add the grid frame to the container layout - takes all space
        self.button_container_layout.addWidget(self.button_frame, 1)
        
        # Navigation buttons - positioned at bottom right
        nav_row = QHBoxLayout()
        nav_row.setSpacing(10)
        nav_row.addStretch()  # Push buttons to the right
        
        self.prev_page_button = QPushButton("<", self.button_container_frame)
        self.prev_page_button.setFixedSize(70, 70)
        self.prev_page_button.setStyleSheet(self._get_themed_stylesheet("button", "nav_button"))
        self.prev_page_button.clicked.connect(self._prev_page)
        nav_row.addWidget(self.prev_page_button)
        
        self.next_page_button = QPushButton(">", self.button_container_frame)
        self.next_page_button.setFixedSize(70, 70)
        self.next_page_button.setStyleSheet(self._get_themed_stylesheet("button", "nav_button"))
        self.next_page_button.clicked.connect(self._next_page)
        nav_row.addWidget(self.next_page_button)
        
        # Add navigation row with no stretch (fixed at bottom)
        self.button_container_layout.addLayout(nav_row)
    

    def _create_info_section(self) -> None:
        """Create the info section with location display and action buttons"""
        # Info frame
        self.info_frame = QFrame(self.main_frame)
        self.info_frame.setStyleSheet(self._get_themed_stylesheet("frame", "white"))
        self.info_frame.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.info_frame.setMinimumWidth(300)  # Ensure minimum width for left panel
        
        # Layout inside info frame
        self.info_layout = QVBoxLayout(self.info_frame)
        self.info_layout.setContentsMargins(20, 20, 20, 20)
        self.info_layout.setSpacing(20)
        
        # COMPONENT 1: Location display frame (Select Table Number)
        self.location_display_frame = QFrame(self.info_frame)
        self.location_display_frame.setStyleSheet(
            f"background-color: {self.get_theme_color('frame_color')}; border-radius: 20px;"
        )
        self.location_display_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Layout for location display frame
        location_display_layout = QVBoxLayout(self.location_display_frame)
        location_display_layout.setAlignment(Qt.AlignCenter)
        location_display_layout.setContentsMargins(20, 20, 20, 20)
        
        # Location label 
        self.location_label = QLabel(self._text_status, self.location_display_frame)
        self.location_label.setFont(QFont("Montserrat", 32, QFont.Bold))
        self.location_label.setStyleSheet(self._get_themed_stylesheet("label", "heading"))
        self.location_label.setAlignment(Qt.AlignCenter)
        self.location_label.setWordWrap(True)
        location_display_layout.addWidget(self.location_label)
        
        self.info_layout.addWidget(self.location_display_frame, 3)  # Give it most stretch
        
        # COMPONENT 2: Return location button (Return to Base Button)
        self._create_return_location_button()
        self.return_location_frame.setFixedHeight(80)
        self.return_location_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.info_layout.addWidget(self.return_location_frame)
        
        # COMPONENT 3: Action buttons frame (Base/Event buttons)
        self.action_buttons_frame = QFrame(self.info_frame)
        self.action_buttons_frame.setStyleSheet(
            f"background-color: {self.get_theme_color('white_frame')}; border-radius: 10px;"
        )
        self.action_buttons_frame.setFixedHeight(90)
        self.action_buttons_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        action_buttons_layout = QHBoxLayout(self.action_buttons_frame)
        action_buttons_layout.setContentsMargins(10, 10, 10, 10)
        action_buttons_layout.setSpacing(10)
        
        # Base button
        self.base_button = QPushButton("Base", self.action_buttons_frame)
        self.base_button.setFixedHeight(70)
        self.base_button.setFont(QFont("Montserrat", 28))
        self.base_button.setStyleSheet(self._get_themed_stylesheet("button", "base_event_button"))
        self.base_button.clicked.connect(self._on_base_mode)
        action_buttons_layout.addWidget(self.base_button)

        # Event button
        self.event_button = QPushButton("Event", self.action_buttons_frame)
        self.event_button.setFixedHeight(70)
        self.event_button.setFont(QFont("Montserrat", 28))
        self.event_button.setStyleSheet(self._get_themed_stylesheet("button", "base_event_button"))
        # self.event_button.clicked.connect(self._on_event_mode)
        action_buttons_layout.addWidget(self.event_button)
        
        self.info_layout.addWidget(self.action_buttons_frame)

    
    def _create_lower_frame(self) -> None:
        """Create the lower frame with start button"""
        self.lower_frame = QFrame(self.main_frame)
        self.lower_frame.setStyleSheet(
            f"background-color: {self.get_theme_color('white_frame')}; border-radius: 12px;"
        )
        self.lower_frame.setFixedHeight(100)  # Fixed height for consistency
        self.lower_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        # Add to main layout with no stretch
        self.main_layout.addWidget(self.lower_frame)
        
        lower_frame_layout = QVBoxLayout(self.lower_frame)
        lower_frame_layout.setContentsMargins(15, 15, 15, 15)
        
        self.start_button = QPushButton("Start Delivery", self.lower_frame)
        self.start_button.setFixedHeight(70)
        self.start_button.setFont(QFont("Montserrat", 48))
        self.start_button.setStyleSheet(self._get_themed_stylesheet("button", "start_delivery"))
        self.start_button.clicked.connect(self._on_start_delivery)
        self.start_button.setEnabled(False)
        self.start_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        lower_frame_layout.addWidget(self.start_button)

    
    def _create_return_location_button(self) -> None:
        """Create return location button"""
        # self.return_location_frame = QFrame(
        #     self.middle_frame,
        # )
        self.return_location_frame = QFrame(self.info_frame)
        self.return_location_frame.setStyleSheet(f"background-color: {self.get_theme_color('button_color')}; border-radius: 10px;")
        
        return_location_layout = QHBoxLayout(self.return_location_frame)
        return_location_layout.setContentsMargins(10, 5, 10, 5)
        return_location_layout.setSpacing(10)
        # return_location_layout.addStretch(3)
        
        self.return_location_button = QPushButton("Return to Base", self.return_location_frame)
        self.return_location_button.setFont(QFont("Montserrat", 28))
        self.return_location_button.setStyleSheet(f"background-color: {self.get_theme_color('button_color')}; color: white; border-radius: 0px;")
        self.return_location_button.clicked.connect(self._on_return_location)
        
        return_location_layout.addWidget(self.return_location_button, 4) # Give it more stretch
        
        # Edit button for return location
        self.return_edit_button = QPushButton("Edit", self.return_location_frame)
        self.return_edit_button.setFont(QFont("Montserrat", 25))
        self.return_edit_button.setStyleSheet(self._get_themed_stylesheet("button", "edit_button"))
        self.return_edit_button.setFixedSize(60, 40) # Smaller fixed size for edit button
        self.return_edit_button.clicked.connect(self._on_return_location)
        return_location_layout.addWidget(self.return_edit_button, 1) # Give it less stretch
        
        # Bind mouse click on the entire frame to trigger return location handler (Qt-style)
        # Note: In PySide6, you typically override mousePressEvent on the widget itself
        # or install an event filter. For simplicity, connecting button clicks is often sufficient.
        # self.return_location_frame.mousePressEvent = lambda event: self._on_return_location()
    
    def _load_delivery_locations(self) -> None:
        """Load delivery locations from file"""
        try:
            delivery_file = "/home/pawan/pyside_app/Database/delivery_location.json"
            if os.path.exists(delivery_file):
                with open(delivery_file, "r") as f:
                    data = json.load(f)
                    locations = data.get("Delivery_Location", [])
                    # 
                    self._create_location_buttons(locations)
            else:
                # Create default locations if file doesn't exist
                default_locations = [
                    {"name": "Table 1", "cordinates": [0.0, 0.0]},
                    {"name": "Table 2", "cordinates": [1.0, 0.0]},
                    {"name": "Table 3", "cordinates": [2.0, 0.0]},
                    {"name": "Table 4", "cordinates": [0.0, 1.0]},
                    {"name": "Table 5", "cordinates": [1.0, 1.0]},
                    {"name": "Table 6", "cordinates": [2.0, 1.0]}
                ]
                self._create_location_buttons(default_locations)
        except Exception as e:
            print(f"Error loading delivery locations: {e}")
            # Create fallback buttons
            self._create_location_buttons([])
    
    def _load_return_locations(self) -> None:
        """Load return/base locations from file"""
        try:
            if os.path.exists(self._return_base_location):
                with open(self._return_base_location, "r") as f:
                    self._return_base_location_list = json.load(f)
            else:
                # Create default base locations if file doesn't exist
                self._return_base_location_list = {
                    "Base_Locations": [
                        {"name": "Base 1", "cordinates": [0.0, 0.0, 0.0, 0.0, 0.0, 1.0]},
                        {"name": "Base 2", "cordinates": [1.0, 0.0, 0.0, 0.0, 0.0, 1.0]},
                        {"name": "Base 3", "cordinates": [2.0, 0.0, 0.0, 0.0, 0.0, 1.0]}
                    ],
                    "Default_Base_Loc": [
                        {"name": "Base 1", "cordinates": [0.0, 0.0, 0.0, 0.0, 0.0, 1.0]}
                    ]
                }
        except Exception as e:
            print(f"Error loading return locations: {e}")
            self._return_base_location_list = {}
        
        # Set default return location
        self._update_return_location_display()
    
    def _create_location_buttons(self, locations: List[Dict[str, Any]]) -> None:
        """Create location buttons"""
        # Clear existing buttons
        for button in self._all_buttons:
            try:
                button.setParent(None)
                button.deleteLater()
            except Exception:
                pass
        self._all_buttons.clear()
        
        # Create new buttons
        for location in locations:
            button = QPushButton(location.get("name", "Unknown"), self.button_frame)
            button.setFont(QFont("Montserrat", 45))
            button.setStyleSheet(self._get_themed_stylesheet("button"))
            button.clicked.connect(lambda loc=location: self._on_location_click(loc))
            self._all_buttons.append(button)
        
        # Display first page
        self._display_buttons_page(0)
    
    def _display_buttons_page(self, page_num: int) -> None:
        """Display buttons for the current page"""
        # Clear current widgets from grid layout
        if hasattr(self, 'button_grid_layout'):
            while self.button_grid_layout.count():
                item = self.button_grid_layout.takeAt(0)
                w = item.widget()
                if w:
                    w.hide()
        
        start_index = page_num * self._buttons_per_page
        end_index = start_index + self._buttons_per_page
        buttons_to_display = self._all_buttons[start_index:end_index]
        
        # Add buttons to the grid layout for the current page
        for i, button in enumerate(buttons_to_display):
            row = i // self._max_columns
            column = i % self._max_columns
            self.button_grid_layout.addWidget(button, row, column)
            button.show()
        
        # Update navigation button states
        self.prev_page_button.setEnabled(page_num > 0)
        self.next_page_button.setEnabled((page_num + 1) * self._buttons_per_page < len(self._all_buttons))
    
    def _prev_page(self) -> None:
        """Go to previous page"""
        if self._current_page > 0:
            self._current_page -= 1
            self._display_buttons_page(self._current_page)
    
    def _next_page(self) -> None:
        """Go to next page"""
        if (self._current_page + 1) * self._buttons_per_page < len(self._all_buttons):
            self._current_page += 1
            self._display_buttons_page(self._current_page)
    
    def _on_location_click(self, location: Dict[str, Any]) -> None:
        """Handle location button click"""
        # Reset all buttons to default color first
        for button in self._all_buttons:
            button.setStyleSheet(self._get_themed_stylesheet("button"))
        
        # Find and update the clicked button
        for button in self._all_buttons:
            if button.text() == location.get("name"):
                if button == self._current_button:
                    # Deselect if same button clicked
                    self._current_button = None
                    self._selected_location = None
                    self._location_selected = False
                    self._text_status = "Select Table \n Number"
                else:
                    # Select new button
                    button.setStyleSheet(self._get_themed_stylesheet("button", "selected"))  # Highlight color
                    self._current_button = button
                    self._selected_location = location
                    self._goal_location = location.get("cordinates")
                    self._location_selected = True
                    self._text_status = location.get("name", "Unknown")
                break
        
        # Update UI
        self._update_location_display()
        self._update_start_button()
    
    def _update_location_display(self) -> None:
        """Update location display"""
        if hasattr(self, 'location_label'):
            self.location_label.setText(self._text_status)
            
            # Update frame color based on selection
            if self._location_selected:
                self.location_display_frame.setStyleSheet(f"background-color: {self.get_theme_color('changing_button_fg')}; border-radius: 20px;")
                self.location_label.setStyleSheet(self._get_themed_stylesheet("label", "selected"))
            else:
                self.location_display_frame.setStyleSheet(f"background-color: {self.get_theme_color('frame_color')}; border-radius: 20px;")
                self.location_label.setStyleSheet(self._get_themed_stylesheet("label", "heading"))
    
    def _update_start_button(self) -> None:
        """Update start button state"""
        self.start_button.setEnabled(bool(self._location_selected))
        if self._location_selected:
            self.start_button.setStyleSheet(self._get_themed_stylesheet("button", "start_delivery").replace(self.get_theme_color('button_color'), "#1a75ff"))
        else:
            self.start_button.setStyleSheet(self._get_themed_stylesheet("button", "start_delivery"))
    
    def _on_base_mode(self) -> None:
        """Handle base mode button click"""
        self._show_base_location_selection()
    
    def _on_return_location(self) -> None:
        """Handle return location button click"""
        self._show_return_location_selection()
    
    def _on_start_delivery(self) -> None:
        """Handle start delivery button click"""
        if self._location_selected and self._selected_location:
            if self._app_controller:
                # Start delivery process
                delivery_data = {
                    "location": self._selected_location,
                    "delivery_type": "delivery",
                    "return_location": self._get_return_location()
                }
                self._app_controller.start_delivery_process(delivery_data)
        else:
            if self._app_controller:
                self._app_controller.show_message("Please select a location first", "warning")
    
    def _get_return_location(self) -> Optional[Dict[str, Any]]:
        """Get the return location"""
        if self._r_base_name and self._r_base_cord:
            return {
                "name": self._r_base_name,
                "cordinates": self._r_base_cord
            }
        return None
    
    def _on_back(self) -> None:
        """Handle back button click"""
        if self._app_controller:
            self._app_controller.show_home()
    
    def _show_base_location_selection(self) -> None:
        """Show base location selection popup"""
        self._show_location_selection_popup("Select Base Location", "Base_Locations", self._on_base_location_selected)
    
    def _show_return_location_selection(self) -> None:
        """Show return location selection popup"""
        self._show_location_selection_popup("Select Return Location", "Base_Locations", self._on_return_location_selected)
    
    def _show_location_selection_popup(self, title: str, location_key: str, callback) -> None:
        """Show location selection popup"""
        # Create popup frame
        self.location_popup = QFrame(self)
        self.location_popup.show()
        self.location_popup.setStyleSheet(self._get_themed_stylesheet("frame", "white"))
        
        # Layout for popup
        popup_layout = QVBoxLayout(self.location_popup)
        popup_layout.setContentsMargins(20, 20, 20, 20)
        popup_layout.setSpacing(15)
        
        # Back button
        self.popup_back_button = QPushButton("←", self.location_popup)
        self.popup_back_button.setFixedSize(70, 70)
        self.popup_back_button.setStyleSheet(self._get_themed_stylesheet("button", "nav_button"))
        self.popup_back_button.clicked.connect(self.location_popup.close)
        popup_layout.addWidget(self.popup_back_button, alignment=Qt.AlignLeft)
        
        # Title
        self.popup_title = QLabel(title, self.location_popup)
        self.popup_title.setFont(QFont("Montserrat", 40))
        self.popup_title.setStyleSheet(self._get_themed_stylesheet("label", "heading"))
        self.popup_title.setAlignment(Qt.AlignCenter)
        popup_layout.addWidget(self.popup_title)
        
        # Pagination info label
        self.popup_pagination_label = QLabel("", self.location_popup)
        self.popup_pagination_label.setFont(QFont("Montserrat", 20))
        self.popup_pagination_label.setStyleSheet(self._get_themed_stylesheet("label", "normal"))
        self.popup_pagination_label.setAlignment(Qt.AlignCenter)
        popup_layout.addWidget(self.popup_pagination_label)
        
        # Button container frame (similar to main page)
        self.popup_button_container_frame = QFrame(
            self.location_popup,
        )
        self.popup_button_container_frame.setStyleSheet(self._get_themed_stylesheet("frame"))
        popup_layout.addWidget(self.popup_button_container_frame)
        
        popup_button_container_layout = QVBoxLayout(self.popup_button_container_frame)
        popup_button_container_layout.setContentsMargins(10,10,10,10)
        
        # Grid frame for buttons (Qt grid layout)
        self.popup_grid_frame = QFrame(self.popup_button_container_frame)
        self.popup_grid_frame.setStyleSheet("background-color: white;")
        # self.popup_grid_frame.show() # No need to call show directly
        self.popup_grid_layout = QGridLayout(self.popup_grid_frame)
        self.popup_grid_layout.setSpacing(20)
        popup_button_container_layout.addWidget(self.popup_grid_frame)
        
        # Configure grid
        for i in range(4):
            self.popup_grid_layout.columnMinimumWidth(i, 200)
            self.popup_grid_layout.setColumnStretch(i, 1)
        for i in range(4):
            self.popup_grid_layout.rowMinimumHeight(i, 80)
            self.popup_grid_layout.setRowStretch(i, 1)
        
        # Navigation buttons (positioned relative to button container frame like main page)
        popup_nav_layout = QHBoxLayout()
        popup_nav_layout.addStretch()
        
        self.popup_prev_button = QPushButton("↑", self.popup_button_container_frame)
        self.popup_prev_button.setFixedSize(70, 80)
        self.popup_prev_button.setStyleSheet(self._get_themed_stylesheet("button", "nav_button"))
        self.popup_prev_button.clicked.connect(self._popup_prev_page)
        popup_nav_layout.addWidget(self.popup_prev_button)
        
        self.popup_next_button = QPushButton("↓", self.popup_button_container_frame)
        self.popup_next_button.setFixedSize(70, 80)
        self.popup_next_button.setStyleSheet(self._get_themed_stylesheet("button", "nav_button"))
        self.popup_next_button.clicked.connect(self._popup_next_page)
        popup_nav_layout.addWidget(self.popup_next_button)
        
        popup_button_container_layout.addLayout(popup_nav_layout)
        
        # Initialize pagination variables
        self.popup_current_page = 0
        self.popup_buttons_per_page = 16  # 4x4 grid
        self.popup_all_buttons = []
        
        # Create location buttons
        self._create_popup_location_buttons(location_key, callback)
        
        # Confirm button
        self.popup_confirm_button = QPushButton("Confirm Location", self.location_popup)
        self.popup_confirm_button.setFixedWidth(300)
        self.popup_confirm_button.setFont(QFont("Montserrat", 45))
        self.popup_confirm_button.setStyleSheet(self._get_themed_stylesheet("button", "start_delivery").replace(self.get_theme_color('button_color'), "#4DA6FF"))
        self.popup_confirm_button.clicked.connect(lambda: self._confirm_location_selection(callback))
        popup_layout.addWidget(self.popup_confirm_button, alignment=Qt.AlignCenter)
    
    def _create_popup_location_buttons(self, location_key: str, callback) -> None:
        """Create location buttons for popup with pagination"""
        self.popup_buttons = []
        self.popup_selected_location = None
        
        locations = self._return_base_location_list.get(location_key, [])
        
        # Create all buttons first
        self.popup_all_buttons = []
        for location in locations:
            button = QPushButton(location["name"], self.popup_grid_frame)
            button.setFont(QFont("Montserrat", 45))
            button.setStyleSheet(self._get_themed_stylesheet("button"))
            button.clicked.connect(lambda loc=location: self._on_popup_location_click(loc))
            self.popup_all_buttons.append(button)
        
        # Display first page
        self._display_popup_buttons_page(0)
    
    def _display_popup_buttons_page(self, page_num: int) -> None:
        """Display buttons for the specified page"""
        # Clear current items from popup grid layout
        if hasattr(self, 'popup_grid_layout'):
            while self.popup_grid_layout.count():
                item = self.popup_grid_layout.takeAt(0)
                w = item.widget()
                if w:
                    w.hide()
        
        # Calculate start and end indices
        start_index = page_num * self.popup_buttons_per_page
        end_index = start_index + self.popup_buttons_per_page
        buttons_to_display = self.popup_all_buttons[start_index:end_index]
        
        # Add buttons to layout for the current page
        for i, button in enumerate(buttons_to_display):
            row = i // 4
            column = i % 4
            self.popup_grid_layout.addWidget(button, row, column)
            button.show()
        
        # Update pagination info
        total_pages = (len(self.popup_all_buttons) + self.popup_buttons_per_page - 1) // self.popup_buttons_per_page
        self.popup_pagination_label.setText(f"Page {page_num + 1} of {total_pages} ({len(self.popup_all_buttons)} locations)")
        
        # Update navigation button states
        self.popup_prev_button.setEnabled(page_num > 0)
        self.popup_next_button.setEnabled((page_num + 1) * self.popup_buttons_per_page < len(self.popup_all_buttons))
    
    def _popup_prev_page(self) -> None:
        """Go to previous page in popup"""
        if self.popup_current_page > 0:
            self.popup_current_page -= 1
            self._display_popup_buttons_page(self.popup_current_page)
    
    def _popup_next_page(self) -> None:
        """Go to next page in popup"""
        if (self.popup_current_page + 1) * self.popup_buttons_per_page < len(self.popup_all_buttons):
            self.popup_current_page += 1
            self._display_popup_buttons_page(self.popup_current_page)
    
    def _on_popup_location_click(self, location: Dict[str, Any]) -> None:
        """Handle popup location button click"""
        # Highlight selected button
        for button in self.popup_all_buttons:
            button.setStyleSheet(self._get_themed_stylesheet("button")) # Reset others
            if button.text() == location["name"]:
                button.setStyleSheet(self._get_themed_stylesheet("button", "selected").replace(self.get_theme_color('changing_button_fg'), "#4DA6FF")) # Highlight
                self.popup_selected_location = location
                self.popup_selected_button = button # Store reference to the selected button
                break
    
    def _confirm_location_selection(self, callback) -> None:
        """Confirm location selection"""
        if self.popup_selected_location:
            callback(self.popup_selected_location)
        if hasattr(self, 'location_popup') and self.location_popup:
            self.location_popup.close()
            self.location_popup.deleteLater()
    
    def _on_base_location_selected(self, location: Dict[str, Any]) -> None:
        """Handle base location selection"""
        self._r_base_name = location["name"]
        self._r_base_cord = location["cordinates"]
        self._update_return_location_display()
        
        if self._app_controller:
            self._app_controller.show_message(f"Base location set to: {location['name']}", "info")
    
    def _on_return_location_selected(self, location: Dict[str, Any]) -> None:
        """Handle return location selection"""
        self._r_base_name = location["name"]
        self._r_base_cord = location["cordinates"]
        self._update_return_location_display()
        
        if self._app_controller:
            self._app_controller.show_message(f"Return location set to: {location['name']}", "info")
    
    def _update_return_location_display(self) -> None:
        """Update return location display"""
        # Get default location if none selected
        if not self._r_base_name:
            default_base_locs = self._return_base_location_list.get("Default_Base_Loc", [])
            if default_base_locs:
                default_loc = default_base_locs[0]
                self._r_base_name = default_loc["name"]
                self._r_base_cord = default_loc.get("cordinates") or default_loc.get("coordinates")
        
        # Update button text
        if hasattr(self, 'return_location_button'):
            self.return_location_button.setText(self._r_base_name or "Return to Base")
            # Update color if needed
            if self._r_base_name:
                self.return_location_button.setStyleSheet(f"background-color: {self.get_theme_color('button_color')}; color: white; border-radius: 0px;")
            else:
                self.return_location_button.setStyleSheet(f"background-color: {self.get_theme_color('button_color')}; color: white; border-radius: 0px;")
    
    def show(self) -> None:
        """Show the delivery view"""
        self.main_frame.show()
        super().show()
    
    def hide(self) -> None:
        """Hide the delivery view"""
        self.main_frame.hide()
        super().hide()
    
    def update_theme(self) -> None:
        """Update theme colors"""
        self._setup_theme()
        
        # Update all UI elements with new theme colors
        if hasattr(self, 'main_frame'):
            self.main_frame.setStyleSheet(self._get_themed_stylesheet("frame", "white"))
        if hasattr(self, 'upper_frame'):
            self.upper_frame.setStyleSheet(self._get_themed_stylesheet("frame"))
        if hasattr(self, 'title_label'):
            self.title_label.setStyleSheet(self._get_themed_stylesheet("label", "heading"))
        if hasattr(self, 'back_button'):
            self.back_button.setStyleSheet(self._get_themed_stylesheet("button", "nav_button"))
        
        # Update navigation buttons
        if hasattr(self, 'prev_page_button'):
            self.prev_page_button.setStyleSheet(self._get_themed_stylesheet("button", "nav_button"))
        if hasattr(self, 'next_page_button'):
            self.next_page_button.setStyleSheet(self._get_themed_stylesheet("button", "nav_button"))
        
        # Update location buttons
        for button in self._all_buttons:
            if button != self._current_button:
                button.setStyleSheet(self._get_themed_stylesheet("button"))
            else:
                button.setStyleSheet(self._get_themed_stylesheet("button", "selected"))
                
        # Update action buttons
        if hasattr(self, 'base_button'):
            self.base_button.setStyleSheet(self._get_themed_stylesheet("button", "base_event_button"))
        
        # Update return location button
        if hasattr(self, 'return_location_frame'):
            self.return_location_frame.setStyleSheet(f"background-color: {self.get_theme_color('button_color')}; border-radius: 10px;")
        if hasattr(self, 'return_location_button'):
            self.return_location_button.setStyleSheet(f"background-color: {self.get_theme_color('button_color')}; color: white; border-radius: 0px;")
        if hasattr(self, 'return_edit_button'):
            self.return_edit_button.setStyleSheet(self._get_themed_stylesheet("button", "edit_button"))
        
        # Update location display
        self._update_location_display()
        
        # Update start button
        if hasattr(self, 'start_button'):
            self._update_start_button()
            
        # Update popup elements if they exist
        if hasattr(self, 'location_popup') and self.location_popup.isVisible():
            self.location_popup.setStyleSheet(self._get_themed_stylesheet("frame", "white"))
            self.popup_back_button.setStyleSheet(self._get_themed_stylesheet("button", "nav_button"))
            self.popup_title.setStyleSheet(self._get_themed_stylesheet("label", "heading"))
            self.popup_pagination_label.setStyleSheet(self._get_themed_stylesheet("label", "normal"))
            self.popup_button_container_frame.setStyleSheet(self._get_themed_stylesheet("frame"))
            self.popup_grid_frame.setStyleSheet("background-color: white;")
            self.popup_prev_button.setStyleSheet(self._get_themed_stylesheet("button", "nav_button"))
            self.popup_next_button.setStyleSheet(self._get_themed_stylesheet("button", "nav_button"))
            self.popup_confirm_button.setStyleSheet(self._get_themed_stylesheet("button", "start_delivery").replace(self.get_theme_color('button_color'), "#4DA6FF"))
            for button in self.popup_all_buttons:
                if button != getattr(self, 'popup_selected_button', None):
                    button.setStyleSheet(self._get_themed_stylesheet("button"))
                else:
                    button.setStyleSheet(self._get_themed_stylesheet("button", "selected").replace(self.get_theme_color('changing_button_fg'), "#4DA6FF"))
                    
    def destroy(self) -> None:
        """Destroy the view"""
        try:
            # Clean up any popups
            if hasattr(self, 'location_popup') and self.location_popup:
                try:
                    self.location_popup.close()
                    self.location_popup.deleteLater()
                except Exception:
                    pass
            
            # Clean up main frame
            if hasattr(self, 'main_frame') and self.main_frame:
                try:
                    self.main_frame.deleteLater()
                except Exception:
                    pass
            
            super().destroy()
        except Exception as e:
            print(f"Error destroying delivery view: {e}") 