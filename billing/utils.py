def get_previous_month_and_year(month: int, year: int) -> tuple[int, int]:
    """
    Given a month (1-12) and a year, return the previous month and adjusted year.
    """
    if month == 1:
        return 12, year - 1
    return month - 1, year
