
from ninja.responses import Response



class XResponse:
    
    def __init__(self, message:str, status_code:int, data:object, status:bool):
        self.message = message
        self.status_code = status_code
        self.data =  data
        self.status = status
    
    
    @property
    def response(self):
        data =  {
            "message": self.message,
            "status_code": self.status_code,
            "data": self.data,
            "status": self.status
        }
        
        return Response(
            data=data,
            status=self.status_code
        )
        