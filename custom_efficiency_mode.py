#!/usr/bin/env python3
"""
Efficiency Mode Module
Based on Matt_the_ok's solution from Microsoft Q&A
Set any Windows process to efficiency mode with green leaf indicator
"""

import argparse
import msvcrt
import wmi
import re
import ctypes
import psutil
from ctypes import wintypes, windll

class PROCESS_pPState(ctypes.Structure):
    """Windows API structure for process power throttling state"""
    _fields_ = [
        ('Version', wintypes.ULONG),
        ('ControlMask', wintypes.ULONG),
        ('StateMask', wintypes.ULONG)
    ]

def set_process_efficiency_mode(pid, process_name=None):
    """
    Set a specific process to efficiency mode by PID
    
    Args:
        pid (int): Process ID
        process_name (str, optional): Process name for logging
    
    Returns:
        bool: True if successful, False otherwise
    """
    if process_name is None:
        try:
            process = psutil.Process(pid)
            process_name = process.name()
        except:
            process_name = f"PID_{pid}"
    
    # Windows API constants
    PROCESS_POWER_THROTTLING_EXECUTION_SPEED = 0x1
    PROCESS_POWER_THROTTLING_CURRENT_VERSION = 1
    ProcessPowerThrottling = 4
    PROCESS_QUERY_INFORMATION = 0x0400
    PROCESS_SET_INFORMATION = 0x0200
    IDLE_PRIORITY_CLASS = 0x00000040  # Base Priority 4 (required for green leaf)
    
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    GetLastError = windll.kernel32.GetLastError
    SetPriorityClass = kernel32.SetPriorityClass
    OpenProcess = windll.kernel32.OpenProcess
    CloseHandle = kernel32.CloseHandle
    
    # Setup Windows API function signatures
    SetProcessInformation = windll.kernel32.SetProcessInformation
    SetProcessInformation.argtypes = (wintypes.HANDLE, wintypes.DWORD, wintypes.LPVOID, wintypes.DWORD)
    SetProcessInformation.restype = wintypes.BOOL
    
    OpenProcess.argtypes = (wintypes.DWORD, wintypes.BOOL, wintypes.DWORD)
    OpenProcess.restype = wintypes.HANDLE
    
    # Open process handle
    hProcess = OpenProcess(
        PROCESS_QUERY_INFORMATION | PROCESS_SET_INFORMATION,
        False,
        pid
    )
    
    if hProcess == 0:
        error_code = GetLastError()
        print(f"❌ Could not open process {process_name} (PID: {pid}). Error: {error_code}")
        return False
    
    try:
        # Step 1: Set process priority to IDLE_PRIORITY_CLASS (required for green leaf)
        priority_result = SetPriorityClass(hProcess, IDLE_PRIORITY_CLASS)
        if not priority_result:
            error_code = GetLastError()
            print(f"⚠️  Failed to set priority for {process_name}. Error: {error_code}")
            return False
        
        # Step 2: Setup power throttling state
        pPState = PROCESS_pPState()
        pPState.Version = PROCESS_POWER_THROTTLING_CURRENT_VERSION
        pPState.ControlMask = PROCESS_POWER_THROTTLING_EXECUTION_SPEED
        pPState.StateMask = PROCESS_POWER_THROTTLING_EXECUTION_SPEED
        
        # Step 3: Enable power throttling (efficiency mode)
        throttling_result = SetProcessInformation(
            hProcess,
            ProcessPowerThrottling,
            ctypes.byref(pPState),
            ctypes.sizeof(pPState),
        )
        
        if throttling_result:
            print(f"✅ Efficiency Mode enabled for {process_name} (PID: {pid})")
            return True
        else:
            error_code = GetLastError()
            print(f"❌ Failed to enable Efficiency Mode for {process_name}. Error: {error_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exception setting efficiency mode for {process_name}: {e}")
        return False
    finally:
        CloseHandle(hProcess)

def set_processes_efficiency_mode(process_names):
    """
    Set multiple processes to efficiency mode by name
    
    Args:
        process_names (list): List of process names (e.g., ['steam.exe', 'notepad.exe'])
    
    Returns:
        dict: Results for each process name
    """
    results = {}
    
    for process_name in process_names:
        results[process_name] = []
        
        # Find all processes with this name
        matching_processes = []
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'].lower() == process_name.lower():
                    matching_processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        if not matching_processes:
            print(f"🔍 No processes found for: {process_name}")
            results[process_name] = []
            continue
        
        print(f"🎯 Found {len(matching_processes)} process(es) for: {process_name}")
        
        for proc_info in matching_processes:
            success = set_process_efficiency_mode(proc_info['pid'], proc_info['name'])
            results[process_name].append({
                'pid': proc_info['pid'],
                'success': success
            })
    
    return results

def main(input_processes):
    expression_of_desired_processes = re.compile(input_processes, re.ASCII | re.IGNORECASE)
    list_of_desired_processes = []

    if parsed_arguments.fast == False: get_running_processes()

    for each_process in the_running_processes:
        if ((expression_of_desired_processes.match(each_process.name) != None) and (".exe" in each_process.name)):
            if (each_process.name not in list_of_desired_processes): list_of_desired_processes.append(each_process.name)
    
    print("🎮 Setting processes to efficiency mode...")
    results = set_processes_efficiency_mode(list_of_desired_processes)
    
    # Count successful operations
    total_success = 0
    total_processes = 0

    for process_name, process_results in results.items():
        for result in process_results:
            total_processes += 1
            if result['success']:
                total_success += 1
    
    if total_processes > 0: print(f"🏁 Successfully set {total_success}/{total_processes} processes to efficiency mode")
    else: print("🔍 No such processes found running")

def get_running_processes():
    global the_running_processes
    # Initialize constructor and -
    system_interface_contruct = wmi.WMI()
    # - load list of running processes into memory.
    the_running_processes = system_interface_contruct.Win32_Process()

the_running_processes = []

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--process", "--processes", 
                     help="What your process(es) (.exe only) are generally called",
                     nargs='+', # means this arg takes multiple inputs
                     default='',
                     type=str)
    parser.add_argument("-f", "--fast",
                        help="Get process list only once, earlier in execution instead of getting process" \
                             " list again & again every time an argument is processed. This may lead to higher" \
                             " chance of missing processes/subprocesses especially just after bootup" \
                             " for instance.",
                        action=argparse.BooleanOptionalAction, # makes arg true if -f is present on the cli (no inputs)
                        default=False,
                        type=bool
                        )
    parsed_arguments = parser.parse_args()

    print("🍃 Efficiency Mode Module")
    print("=" * 30)
    
    # Check admin status
    try:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        if not is_admin:
            print("⚠️  Warning: Not running as administrator")
            print("Processes may not be able to be set to efficiency mode without admin privileges.")
    except: pass

    desired_processes = None
    if parsed_arguments.process: desired_processes = parsed_arguments.process
    else: desired_processes = input("Enter what your processes (.exe only) are generally called: ")

    if desired_processes == None: quit()
    if (len(desired_processes) == 0): print("No input, exiting."); quit()

    if parsed_arguments.fast: get_running_processes()

    if type(desired_processes) == list:
        for each_process_argument in desired_processes: main(each_process_argument)
    else: 
        main(desired_processes)
        print("Press any key to exit... ")
        msvcrt.getch()