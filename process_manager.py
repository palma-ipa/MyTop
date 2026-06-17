import psutil


class ProcessManager:
    """Manages system processes using psutil library."""

    def __init__(self):
        self._initialized = False

    def _init_cpu_monitoring(self):
        """Initialize CPU monitoring baseline for all processes."""
        if not self._initialized:
            for proc in psutil.process_iter(['pid']):
                try:
                    proc.cpu_percent(interval=None)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            self._initialized = True

    def get_processes(self):
        """
        Fetch all running processes with PID, Name, CPU%, Memory%, and User.
        Returns a list of dictionaries sorted by CPU usage descending.
        Non-blocking: uses interval=None for cpu_percent.
        """
        processes = []

        for proc in psutil.process_iter(['pid', 'name', 'username']):
            try:
                pid = proc.info['pid']
                try:
                    cpu_percent = proc.cpu_percent(interval=None)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    cpu_percent = 0.0

                try:
                    mem_percent = proc.memory_percent()
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    mem_percent = 0.0

                processes.append({
                    'pid': pid,
                    'name': proc.info['name'],
                    'cpu_percent': cpu_percent,
                    'memory_percent': mem_percent,
                    'username': proc.info['username']
                })

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        processes.sort(key=lambda p: p['cpu_percent'], reverse=True)
        return processes

    def kill_process(self, pid):
        """
        Terminate a process by PID.
        First tries SIGTERM, falls back to SIGKILL on timeout.
        Returns tuple: (True, "Success message") or (False, "Error message")
        """
        try:
            proc = psutil.Process(pid)
            proc.terminate()
            try:
                proc.wait(timeout=3)
                return (True, f"Process {pid} terminated successfully")
            except psutil.TimeoutExpired:
                proc.kill()
                return (True, f"Process {pid} killed after termination timeout")

        except psutil.NoSuchProcess:
            return (False, f"No such process with PID {pid}")
        except psutil.AccessDenied:
            return (False, f"Access denied to terminate process {pid}")