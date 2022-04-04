import sys

class SystemException(Exception):
    def __init__(self, message):
        
        frame = sys._getframe(1)
        function = frame.f_code
        file_name = function.co_filename
        prev_frame = frame.f_back
        prev = prev_frame.f_code
        
        out = f"""
        {prev.co_filename}:{prev_frame.f_lineno} {prev.co_name} -> 
          {file_name}: {function.co_firstlineno} -> 
            {function.co_name}{function.co_varnames}:
              {file_name}: {frame.f_lineno} -> [{message}]
        """
      
        super().__init__(out)
        


