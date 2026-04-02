from enum import Enum

"""
This file contains the enums for the page types in the todo app.
 Each enum value corresponds to a specific page or filter in the application, and is used to improve code readability 
 and maintainability by providing meaningful names for these elements. 
 By using these enums, we can avoid hardcoding strings throughout the codebase
 making it easier to update and manage the application as it evolves.
"""

class PageType(Enum):
    ADD_TODO = "What needs to be done?"
    TOGGLE_TODO = "Toggle Todo"
    DELETE_BTN = "Delete"
    ALL_FILTER = "All"
    ACTIVE_FILTER = "Active"
    COMPLETED_FILTER = "Completed"
