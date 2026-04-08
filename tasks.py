class Task:
    def __init__(self, name, description):
        self.name = name
        self.description = description


# Define tasks
EASY_TASK = Task(
    name="easy",
    description="Remove duplicates and missing customers"
)

MEDIUM_TASK = Task(
    name="medium",
    description="Fix negative amounts and clean data"
)

HARD_TASK = Task(
    name="hard",
    description="Prepare fully clean dataset for analysis"
)