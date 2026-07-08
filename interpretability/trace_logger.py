from datetime import datetime

class TraceLogger:
    def __init__(self):
        self.steps = []
        self.start_time = datetime.now()
    
    def log(self, message: str):
        elapsed = (datetime.now() - self.start_time).total_seconds()
        self.steps.append({
            "step": len(self.steps) + 1,
            "message": message,
            "elapsed_ms": round(elapsed * 1000, 1)
        })
    
    def get_log(self):
        return {
            "steps": self.steps,
            "total_steps": len(self.steps),
            "total_time_ms": round((datetime.now() - self.start_time).total_seconds() * 1000, 1)
        }