import datetime
import platform, psutil
class GenericSystem:
    """Custom Python functions for the chatbot"""
    
    @staticmethod
    def get_current_time():
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    @staticmethod
    def get_current_date():
        return datetime.datetime.now().strftime("%A, %B %d, %Y")
    
    
    @staticmethod
    def get_system_info() -> str:
        """Get basic system information"""
        
        
        info = {
            "OS": platform.system(),
            "OS Version": platform.version(),
            "Processor": platform.processor(),
            "Memory": f"{psutil.virtual_memory().available / 1024**3:.1f} GB available",
            "Python Version": platform.python_version()
        }
        
        return "\n".join(f"{key}: {value}" for key, value in info.items())

    @staticmethod
    @property
    def total_memory(self) :
        return self.get_memory_usage().total
    
    @staticmethod
    @property
    def available_memory(self) :
        return self.get_memory_usage().available
    
    @staticmethod
    @property
    def used_memory(self) :
        return self.get_memory_usage().used
    
    @staticmethod
    @property
    def free_memory(self) :
        return self.get_memory_usage().free
    
    @staticmethod
    @property
    def total_disk(self) :
        return self.get_disk_usage().total
    
    @staticmethod
    @property
    def available_disk(self) :
        return self.get_disk_usage().available
    
    @staticmethod
    @property
    def used_disk(self) :
        return self.get_disk_usage().used
    
    @staticmethod
    @property
    def free_disk(self) :
        return self.get_disk_usage().free
    
    @staticmethod
    def get_disk_usage(self) :
        return psutil.disk_usage('/')

    @staticmethod
    def get_cpu_usage(self) :
        return psutil.cpu_percent(interval=1)
    
    @staticmethod
    def get_memory_usage(self) :
        return psutil.virtual_memory()
    
    @staticmethod
    def get_usb_devices(self) :
        return psutil.disk_partitions()