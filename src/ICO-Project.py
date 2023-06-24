from datetime import datetime


class ICOProject:
    """
    ICOProject class
    """

    def __init__(self, project_name, start_date, end_date, goal_amount):
        self.project_name = project_name
        self.start_date = start_date
        self.end_date = end_date
        self.goal_amount = goal_amount
        self.current_amount = 0
        self.backers = []

    def add_funding(self, backer, amount):
        """_summary_

        Args:
            backer (_type_): _description_
            amount (_type_): _description_
        """
        self.current_amount += amount
        self.backers.append((backer, amount))

    def is_goal_reached(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.current_amount >= self.goal_amount

    def get_remaining_days(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        remaining_days = (self.end_date - datetime.now()).days
        return max(0, remaining_days)

    def get_project_status(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        status = f"Project Name: {self.project_name}\n"
        status += f"Goal Amount: {self.goal_amount}\n"
        status += f"Current Amount: {self.current_amount}\n"
        status += f"Number of Backers: {len(self.backers)}\n"
        status += f"Goal Reached: {'Yes' if self.is_goal_reached() else 'No'}\n"
        status += f"Remaining Days: {self.get_remaining_days()}\n"
        return status
