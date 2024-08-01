#!/usr/bin/env python3

import os
import sys
import argparse

CENTRAL_ENV_DIR = os.path.expanduser("~/env")

def ensure_central_env_dir():
    if not os.path.exists(CENTRAL_ENV_DIR):
        os.makedirs(CENTRAL_ENV_DIR)

def update_central_env_file(project_name, env_name, env_value):
    env_file_path = os.path.join(CENTRAL_ENV_DIR, f"{project_name}/.env")
    
    if not os.path.exists(env_file_path):
        open(env_file_path, 'a').close()
    
    with open(env_file_path, 'r') as file:
        lines = file.readlines()
    
    with open(env_file_path, 'w') as file:
        updated = False
        for line in lines:
            if line.startswith(env_name):
                file.write(f"{env_name}={env_value}\n")
                updated = True
            else:
                file.write(line)
        if not updated:
            file.write(f"{env_name}={env_value}\n")

def create_symlink(project_root, project_name):
    env_file_path = os.path.join(CENTRAL_ENV_DIR, f"{project_name}/.env")
    symlink_path = os.path.join(project_root, ".env")
    
    if os.path.islink(symlink_path):
        os.remove(symlink_path)
    elif os.path.exists(symlink_path):
        print(f"Error: {symlink_path} already exists and is not a symlink.")
        sys.exit(1)
    
    os.symlink(env_file_path, symlink_path)
    print(f"Symlink created: {symlink_path} -> {env_file_path}")

def main():
    parser = argparse.ArgumentParser(description="Manage environment variables and create symlinks for projects.")
    parser.add_argument('project_name', type=str, help='The name of the project')
    parser.add_argument('env_name', type=str, help='The name of the environment variable')
    parser.add_argument('env_value', type=str, help='The value of the environment variable')
    
    args = parser.parse_args()

    project_name = args.project_name
    env_name = args.env_name
    env_value = args.env_value

    project_root = os.getcwd()
    
    print(f"Current directory: {project_root}")
    
    ensure_central_env_dir()
    update_central_env_file(project_name, env_name, env_value)
    create_symlink(project_root, project_name)

if __name__ == "__main__":
    main()
