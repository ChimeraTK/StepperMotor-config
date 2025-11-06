##mako
#! /usr/bin/python3
import os

"""
Generate hardlinks to req-file with motor-specific names, so autosave
can generate save files for all motors, as the name of the savefile is
derived from the req-file name.
"""
# Get file-descriptor for the current directory
# NOTE: with-environment doesn't work, because os.getcwd() does not provide an __enter__-method
cwd_fd = os.open(os.getcwd(), os.O_RDONLY)
# Generate hardlinks
for n_motor in range(${motor_cfg.number_motors}):
    try:
        os.link('steppermotorserver-motor.req', f'steppermotorserver-motor{n_motor + 1}.req', src_dir_fd=cwd_fd, dst_dir_fd=cwd_fd)
    except FileExistsError:
        print(f'make_motor_links.py: steppermotorserver-motor{n_motor + 1}.req already exists! Skip.')
        continue
os.close(cwd_fd)
