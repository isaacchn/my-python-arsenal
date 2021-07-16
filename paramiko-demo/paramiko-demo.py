import paramiko
from paramiko import SSHClient

"""
Paramiko示例程序
"""


def paramiko_connect(hostname, port, username, password):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=hostname,
                       port=port,
                       username=username,
                       password=password)
    return ssh_client


def ssh_exec(ssh_client: SSHClient, command):
    stdin, stdout, stderr = ssh_client.exec_command(command)
    while True:
        if stdout.channel.recv_ready():
            line_stdout = stdout.readline()
            print(line_stdout, end='')
        if stderr.channel.recv_stderr_ready():
            line_stderr = stderr.readline()
            print(line_stderr, end='')
        if stdout.channel.exit_status_ready() and stderr.channel.exit_status_ready():
            print('退出')
            break

# 另一种写法
# def ssh_exec(ssh_client: SSHClient, command):
#     trans = ssh_client.get_transport()
#     channel = trans.open_session()
#     channel.set_combine_stderr(False)
#     f_stdout = channel.makefile()
#     f_stderr = channel.makefile_stderr()
#     channel.exec_command(command)
#     while True:
#         if channel.recv_ready():
#             line_stdout = f_stdout.readline()
#             print(line_stdout, end='')
#         if channel.recv_stderr_ready():
#             line_stderr = f_stderr.readline()
#             print(line_stderr, end='')
#         if channel.exit_status_ready():
#             break


if __name__ == '__main__':
    ssh = paramiko_connect('hostname', 22, 'username', 'password')
    cmd1 = 'echo STDOUT1 >& 1; sleep 2; echo STDERR1 >& 2; sleep 2; echo STDOUT2 >& 1; sleep 2; echo STDERR2 >& 2;'
    cmd2 = 'echo STDOUT1 >& 1; sleep 2; echo STDOUT2 >& 1; sleep 2; echo STDOUT3 >& 1; sleep 2; echo STDOUT4 >& 1;'
    ssh_exec(ssh, cmd1)
    ssh_exec(ssh, cmd2)
    ssh.close()
