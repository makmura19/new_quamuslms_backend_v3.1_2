from .concat import handle_concat
from .date_to_string import handle_date_to_string
from .round import handle_round
from .sum import handle_sum
from .multiply import handle_multiply
from .rename_field import handle_rename_field
from .age import handle_age
from .handle_mask import handle_mask

registry = {
    "CONCAT": handle_concat,
    "DATE_TO_STRING": handle_date_to_string,
    "ROUND": handle_round,
    "SUM": handle_sum,
    "MULTIPLY": handle_multiply,
    "RENAME_FIELD": handle_rename_field,
    "AGE": handle_age,
    "HANDLE_MASK": handle_mask,
}
