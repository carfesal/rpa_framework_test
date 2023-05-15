from RPA.Robocorp.WorkItems import WorkItems
from src.util.logging import logger

def get_work_item_variables() -> dict:
    """Get the input data from the work item variables."""
    library = WorkItems()
    library.get_input_work_item()
    
    variables = library.get_work_item_variables()
    for variable, value in variables.items():
        logger.info("%s = %s", variable, value)
    
    return variables