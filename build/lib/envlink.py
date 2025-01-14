#!/usr/bin/env python3

import os
import sys
import argparse
import shutil
import re

CENTRAL_ENV_DIR = os.path.expanduser("~/env")

def ensure_project_env_dir(project_name):
    project_env_dir = os.path.join(CENTRAL_ENV_DIR, project_name)
    if not os.path.exists(project_env_dir):
        os.makedirs(project_env_dir)
    return project_env_dir

def check_env_variable_exists(env_file_path, env_name):
    if not os.path.exists(env_file_path):
        return False
    with open(env_file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith(env_name + "="):
                return True
    return False

def update_central_env_file(project_env_dir, env_name, env_value):
    env_file_path = os.path.join(project_env_dir, '.env')
    
    env_exists = check_env_variable_exists(env_file_path, env_name)
    
    if env_exists:
        user_choice = input(f"The environment variable {env_name} already exists. Do you want to update the value? (yes/no): ").strip().lower()
        if user_choice not in ['yes', 'y']:
            print("Exiting without making changes.")
            sys.exit(0)
    
    with open(env_file_path, 'r') as file:
        lines = file.readlines()
    
    with open(env_file_path, 'w') as file:
        updated = False
        for line in lines:
            if line.startswith(env_name + "="):
                file.write(f'{env_name}="{env_value}"\n')
                updated = True
            else:
                file.write(line)
        if not updated:
            file.write(f'{env_name}="{env_value}"\n')

def create_symlink(project_root, project_env_dir, env_file_name):
    env_file_path = os.path.join(project_env_dir, env_file_name)
    symlink_path = os.path.join(project_root, env_file_name)
    
    if os.path.islink(symlink_path):
        os.remove(symlink_path)
    elif os.path.exists(symlink_path):
        print(f"Error: {symlink_path} already exists and is not a symlink.")
        sys.exit(1)
    
    os.symlink(env_file_path, symlink_path)
    print(f"Symlink created: {symlink_path} -> {env_file_path}")

def move_file_and_create_symlink(source_path, target_path, project_root, project_env_dir, env_file):
    if os.path.exists(target_path):
        print(f"Skipping {env_file} as it already exists in the central env directory.")
    else:
        shutil.move(source_path, target_path)
        print(f"Moved {env_file} to {target_path}")
    create_symlink(project_root, project_env_dir, env_file)

def is_valid_env_file(env_file):
    return bool(re.match(r'^\.env(\..+)?$', env_file))

def move_and_symlink_env_files(project_root, project_env_dir):
    env_files = [f for f in os.listdir(project_root) if is_valid_env_file(f)]
    for env_file in env_files:
        source_path = os.path.join(project_root, env_file)
        target_path = os.path.join(project_env_dir, env_file)
        move_file_and_create_symlink(source_path, target_path, project_root, project_env_dir, env_file)

def sync_env_files(project_root, project_env_dir):
    # Sync files from central env directory to project directory
    for env_file in os.listdir(project_env_dir):
        if is_valid_env_file(env_file):
            env_file_path = os.path.join(project_env_dir, env_file)
            symlink_path = os.path.join(project_root, env_file)
            if not os.path.exists(symlink_path):
                create_symlink(project_root, project_env_dir, env_file)

    # Sync files from project directory to central env directory
    for env_file in os.listdir(project_root):
        if is_valid_env_file(env_file):
            source_path = os.path.join(project_root, env_file)
            target_path = os.path.join(project_env_dir, env_file)
            if not os.path.exists(target_path):
                move_file_and_create_symlink(source_path, target_path, project_root, project_env_dir, env_file)

def main():
    parser = argparse.ArgumentParser(description="Manage environment variables, move .env files, sync env files, and create symlinks for projects.")
    parser.add_argument('project_name', type=str, help='The name of the project')
    parser.add_argument('--move', '--mv', action='store_true', help='Move .env files to central directory and create symlinks')
    parser.add_argument('--key', '-k', type=str, help='The name of the environment variable')
    parser.add_argument('--value', '-v', type=str, help='The value of the environment variable')
    parser.add_argument('--sync', action='store_true', help='Sync .env files between central directory and project directory')
    
    args = parser.parse_args()

    project_name = args.project_name
    project_root = os.getcwd()
    project_env_dir = ensure_project_env_dir(project_name)
    
    print(f"Current directory: {project_root}")
    
    if args.move:
        move_and_symlink_env_files(project_root, project_env_dir)
    elif args.sync:
        sync_env_files(project_root, project_env_dir)
    elif args.key and args.value:
        update_central_env_file(project_env_dir, args.key, args.value)
        create_symlink(project_root, project_env_dir, '.env')
    else:
        print("Error: You must specify either --move to move .env files, --sync to sync .env files, or both --key and --value to update an environment variable.")
        sys.exit(1)

if __name__ == "__main__":
    main()
