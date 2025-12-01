import traceback
import sys


class DebugExceptionMiddleware:
    """Middleware para logar todas as exceções não tratadas."""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception as e:
            print("=" * 80, file=sys.stderr)
            print(f"EXCEPTION IN REQUEST: {request.path}", file=sys.stderr)
            print(f"Exception type: {type(e).__name__}", file=sys.stderr)
            print(f"Exception message: {str(e)}", file=sys.stderr)
            print("Traceback:", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            print("=" * 80, file=sys.stderr)
            raise
    
    def process_exception(self, request, exception):
        print("=" * 80, file=sys.stderr)
        print(f"PROCESS_EXCEPTION: {request.path}", file=sys.stderr)
        print(f"Exception type: {type(exception).__name__}", file=sys.stderr)
        print(f"Exception message: {str(exception)}", file=sys.stderr)
        print("Traceback:", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        print("=" * 80, file=sys.stderr)
        return None
