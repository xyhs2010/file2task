import os
import sys
import subprocess
import shutil


def main_cli():
    assert(len(sys.argv) > 1)
    task_file = sys.argv[1]

    if not (os.path.isfile(task_file) and os.path.getsize(task_file) > 0):
        # 无效
        print(f"Error: File {task_file} not valid.")
        return

    shutil.copy(task_file, task_file + ".bak")


    out_fd = open(task_file + ".out", "w")
    err_fd = open(task_file + ".err", "w")
    while True:
        line_gene = (_.strip() for _ in open(task_file).readlines())
        lines = [_ for _ in line_gene if len(_) > 0]
        if len(lines) == 0:
            return

        command = lines[0]
        open(task_file, "w").writelines((_ + "\n" for _ in lines[1:]))
        
        out_fd.write("\n\n" + "#" * 8 + command + "#" * 8 + "\n")
        out_fd.flush()
        err_fd.write("\n\n" + "#" * 8 + command + "#" * 8 + "\n")
        err_fd.flush()
        subprocess.run(command.split(" "), stdout=out_fd, stderr=err_fd)
        if os.path.getsize(task_file) == 0:
            break
    
    out_fd.close()
    err_fd.close()
