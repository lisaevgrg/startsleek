import os
import subprocess
import sys
import ctypes
from pathlib import Path

class StartSleek:
    def __init__(self):
        self.startup_folder = Path(os.getenv('APPDATA')) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
        self.services_to_disable = []

    def list_startup_programs(self):
        """Lists all programs in the startup folder."""
        return list(self.startup_folder.iterdir())

    def disable_startup_program(self, program_name):
        """Disables a specific startup program by removing its shortcut."""
        program_path = self.startup_folder / program_name
        if program_path.exists():
            program_path.unlink()
            print(f"{program_name} has been disabled from startup.")
        else:
            print(f"{program_name} not found in startup.")

    def list_services(self):
        """Lists all services currently set to start automatically."""
        result = subprocess.run(['sc', 'query', 'type=', 'service', 'state=', 'all'], capture_output=True, text=True)
        services = result.stdout.splitlines()
        return [line.strip() for line in services if 'SERVICE_NAME' in line]

    def disable_service(self, service_name):
        """Disables a specific service from starting automatically."""
        if service_name:
            subprocess.run(['sc', 'config', service_name, 'start=', 'disabled'])
            print(f"Service {service_name} has been disabled.")
        else:
            print(f"Service {service_name} not found.")

    def optimize_boot(self):
        """Optimizes boot by disabling unnecessary startup programs and services."""
        for program in self.list_startup_programs():
            self.disable_startup_program(program.name)
        
        for service in self.services_to_disable:
            self.disable_service(service)

    def is_admin(self):
        """Checks if the script is running with administrative privileges."""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def main(self):
        """Main execution method."""
        if not self.is_admin():
            print("Please run this script as an administrator.")
            sys.exit(1)

        print("Starting optimization...")
        self.optimize_boot()
        print("Optimization complete. Your system should boot faster now.")

if __name__ == "__main__":
    sleek = StartSleek()
    sleek.main()