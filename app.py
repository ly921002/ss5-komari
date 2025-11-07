#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import time
import urllib.request
import urllib.error
from pathlib import Path
import shlex
# ==================================================
# 环境变量配置（可在运行容器时通过环境变量覆盖）
# ==================================================

def setup_environment():
    """设置环境变量"""
    # 必需的环境变量
    os.environ.setdefault('AGENT_ENDPOINT', 'https://gcp.240713.xyz')
    os.environ.setdefault('AGENT_TOKEN', '9bj4FIzMqDLa5yH5JzJ0LC')
    os.environ.setdefault('SOPT', '8888')
    os.environ.setdefault('UUID', '0000')
    return (os.environ.get('AGENT_ENDPOINT'), 
            os.environ.get('AGENT_TOKEN'), 
            os.environ.get('SOPT'), 
            os.environ.get('UUID'))

# ==================================================
# 辅助函数
# ==================================================

def run_command(cmd, shell=False):
    """执行命令并返回结果"""
    try:
        if shell:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        else:
            result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, "", str(e)

# ==================================================
# 文件下载
# ==================================================

def download_agent():
    """下载agent程序"""
    url = "https://raw.githubusercontent.com/ly921002/gcp/refs/heads/main/komari-agent-linux-amd64"
    local_filename = "komari-agent"
    
    try:
        print(f"Downloading agent from {url}...")
        urllib.request.urlretrieve(url, local_filename)
        
        # 验证文件是否下载成功
        if Path(local_filename).stat().st_size == 0:
            print("ERROR: Downloaded agent file is empty")
            return False
            
        # 设置文件权限为755
        Path(local_filename).chmod(0o755)
        print(f"Agent downloaded successfully: {local_filename}")
        return True
    except urllib.error.URLError as e:
        print(f"ERROR: Failed to download agent - {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"ERROR: Unexpected error during download - {e}", file=sys.stderr)
        return False

def download_argosbx():
    """下载argosbx程序"""
    url = "https://raw.githubusercontent.com/yonggekkk/argosbx/main/argosbx.sh"
    local_filename = "argosbx.sh"
    
    try:
        print(f"Downloading argosbx from {url}...")
        urllib.request.urlretrieve(url, local_filename)
        
        # 验证文件是否下载成功
        if Path(local_filename).stat().st_size == 0:
            print("ERROR: Downloaded argosbx file is empty")
            return False
            
        # 设置文件权限为755
        Path(local_filename).chmod(0o755)
        print(f"Argosbx downloaded successfully: {local_filename}")
        return True
    except urllib.error.URLError as e:
        print(f"ERROR: Failed to download argosbx - {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"ERROR: Unexpected error during download - {e}", file=sys.stderr)
        return False

# ==================================================
# 主程序执行
# ==================================================

def run_argosbx(sopt, uuid):
    """运行argosbx脚本"""
    if not download_argosbx():
        return False
    
    try:
        # 使用shell命令方式，设置环境变量并运行脚本
        safe_sopt = shlex.quote(sopt)
        safe_uuid = shlex.quote(uuid)
        command = f"sopt={safe_sopt} uuid={safe_uuid} bash argosbx.sh"
        
        print(f"Running argosbx with command: {command}")
        
        with open("argosbx.log", "w") as log_file:
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=log_file,
                stderr=subprocess.STDOUT
            )
        
        # 等待脚本完成或超时
        try:
            returncode = process.wait(timeout=300)  # 5分钟超时
            if returncode == 0:
                print("Argosbx script completed successfully")
                return True
            else:
                print(f"Argosbx script exited with code: {returncode}")
                return False
        except subprocess.TimeoutExpired:
            print("Argosbx script timed out")
            process.kill()
            return False
            
    except Exception as e:
        print(f"ERROR: Failed to run argosbx - {e}", file=sys.stderr)
        return False

def run_agent(endpoint, token):
    """运行agent程序"""
    try:
        # 显示配置信息
        print("=" * 50)
        print("Starting komari-agent with configuration:")
        print(f"  - ENDPOINT:      {endpoint}")
        print(f"  - TOKEN:         {token[:4]}****{token[-4:]}")
        print("=" * 50)
        
        # 检查agent文件是否存在
        if not Path("komari-agent").exists():
            print("ERROR: komari-agent file not found", file=sys.stderr)
            return None
        
        # 使用nohup方式运行agent（后台进程）
        with open("komari-agent.log", "w") as log_file:
            process = subprocess.Popen(
                ["./komari-agent", "-e", endpoint, "-t", token],
                stdout=log_file,
                stderr=subprocess.STDOUT
            )
        
        print("Application started in background")
        print("Logs are being written to: komari-agent.log")
        
        return process
        
    except FileNotFoundError:
        print("ERROR: komari-agent executable not found", file=sys.stderr)
        return None
    except Exception as e:
        print(f"ERROR: Failed to start agent - {e}", file=sys.stderr)
        return None

# ==================================================
# 健康检查函数
# ==================================================

def check_agent_health(process, log_path="komari-agent.log"):
    """检查agent进程的健康状态"""
    try:
        # 检查进程是否在运行
        if process.poll() is not None:
            return False, f"Agent process exited with code: {process.returncode}"
        
        # 检查日志文件大小
        if Path(log_path).exists():
            size = Path(log_path).stat().st_size
            if size > 10 * 1024 * 1024:  # 如果日志文件大于10MB
                print(f"Log file size: {size} bytes")
        
        return True, "Agent is running normally"
        
    except Exception as e:
        return False, f"Health check error: {e}"

# ==================================================
# 主函数
# ==================================================

def main():
    """主函数"""
    # 设置环境变量
    endpoint, token, sopt, uuid = setup_environment()
    
    # 验证必需的环境变量
    if not all([endpoint, token, sopt, uuid]):
        print("ERROR: Missing required environment variables")
        sys.exit(1)
    
    # 下载agent
    if not download_agent():
        print("Failed to download agent. Exiting.")
        sys.exit(1)
    
    # 运行argosbx脚本
    argosbx_success = run_argosbx(sopt, uuid)
    if not argosbx_success:
        print("Argosbx script had issues, but continuing...")
    
    # 运行agent
    process = run_agent(endpoint, token)
    if process is None:
        print("Failed to start agent. Exiting.")
        sys.exit(1)
    
    # 保持容器运行
    print("Container is running. Press Ctrl+C to stop.")
    try:
        # 检查进程状态并保持运行
        while True:
            is_healthy, health_msg = check_agent_health(process)
            
            if not is_healthy:
                print(f"Agent health check failed: {health_msg}")
                break
                
            time.sleep(5)
    
    except KeyboardInterrupt:
        print("\nReceived interrupt signal. Shutting down...")
        process.terminate()
        try:
            process.wait(timeout=10)
            print("Agent stopped gracefully.")
        except subprocess.TimeoutExpired:
            print("Agent did not stop in time, forcing kill...")
            process.kill()
            print("Agent killed.")
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        process.terminate()
        process.wait(timeout=5)
    
    finally:
        # 确保进程被终止
        if process.poll() is None:
            process.kill()
        print("Container shutdown complete.")

if __name__ == "__main__":
    main()
