import subprocess
import re
import os
import getpass
import yaml
import sys

# mount_status checks if the device already mounted.
def mount_status(mount_point):
    if not os.path.ismount(mount_point):
        return False
    return True
        
# find_and_extract_block_alias extracts block alias ex: sdb1 that used to mount the harddrive
def find_and_extract_block_alias(drive_name):
    found = False
    block_data = ''

    try:
        result = subprocess.run(['lsblk', '-l', '-f'], stdout=subprocess.PIPE, text=True)
        list = result.stdout.strip().split('\n')
    except Exception as e:
        print(f"Error occurred: {e}")

    pattern = rf'\b{drive_name}\b'
    for row in list:
        match = re.search(pattern, row)
        if match:
            found = True
            block_data = row
    
    if not found:
        return None, False

    # find the specific block alias.
    pattern = r'\bsd[a-z]\d+\b'
    match = re.search(pattern, row)

    return match[0], True

# load_config loads the config file.
def load_config():
    try: 
        yaml_file_path = yaml.safe_load('/home/prince/.config/hdd_mounter/config.yaml')
    except yaml.YAMLError as e:
        print(f'failed to load env file: {e}')

    # check if the file exist
    if os.path.isfile(yaml_file_path):
        with open(yaml_file_path, 'r') as file:
            data = file.read()
    else:
        sys.exit(f"file not found at location: {yaml_file_path}")

    with open(yaml_file_path, 'r') as file:
        data = yaml.safe_load(file)
        return data

if __name__ == "__main__":
    config = load_config()
    # load config
    mount_directory = config['mount_directory']
    hdd_name = config['hdd_name']
    mount_point = mount_directory + hdd_name

    is_mounted = mount_status(mount_point)
    if is_mounted:
        quit('nothing to do, device is already mounted') 

    blk_alias, is_found = find_and_extract_block_alias(hdd_name)
    if not is_found:
        quit('could not find the device')

    try:
        subprocess.run(['udisksctl', 'mount', '-b', '/dev/'+blk_alias], check=True)
        print(f'successfully mounted')
    except subprocess.CalledProcessError as e:
        print(f'error mounting the device: {e}')



