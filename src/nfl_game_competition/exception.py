# custom exceptions for the nfl_game_competition package without logging
import sys
# no logging here
# error messages fuction
def error_message_detail(error, error_detail: sys):
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    error_message = f"Error occurred in script: {file_name} at line number: {line_number} with message: {str(error)}"
    return error_message  


# class for custom exception
class NFLGameCompetitionException(Exception):
    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail)

    def __str__(self):
        return self.error_message
    
# Example usage of the custom exception
if __name__ == "__main__":
    try:
        # Simulate an error
        1 / 0
    except Exception as e:
        raise NFLGameCompetitionException(e, sys)