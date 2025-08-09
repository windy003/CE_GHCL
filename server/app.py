#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os
import shutil
import uuid
import tempfile
from datetime import datetime
import logging

app = Flask(__name__)
CORS(app)

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 支持的编程语言文件扩展名
SUPPORTED_EXTENSIONS = {
    '.js': 'JavaScript',
    '.jsx': 'JavaScript React',
    '.ts': 'TypeScript',
    '.tsx': 'TypeScript React',
    '.py': 'Python',
    '.pyx': 'Cython',
    '.pyi': 'Python Interface',
    '.java': 'Java',
    '.cpp': 'C++',
    '.cxx': 'C++',
    '.cc': 'C++',
    '.c': 'C',
    '.h': 'C Header',
    '.hpp': 'C++ Header',
    '.hxx': 'C++ Header',
    '.cs': 'C#',
    '.php': 'PHP',
    '.rb': 'Ruby',
    '.go': 'Go',
    '.rs': 'Rust',
    '.swift': 'Swift',
    '.kt': 'Kotlin',
    '.kts': 'Kotlin Script',
    '.scala': 'Scala',
    '.sh': 'Shell',
    '.bash': 'Bash',
    '.zsh': 'Zsh',
    '.fish': 'Fish',
    '.ps1': 'PowerShell',
    '.bat': 'Batch',
    '.cmd': 'Command',
    '.html': 'HTML',
    '.htm': 'HTML',
    '.xml': 'XML',
    '.xhtml': 'XHTML',
    '.css': 'CSS',
    '.scss': 'SCSS',
    '.sass': 'Sass',
    '.less': 'LESS',
    '.styl': 'Stylus',
    '.vue': 'Vue',
    '.svelte': 'Svelte',
    '.dart': 'Dart',
    '.r': 'R',
    '.R': 'R',
    '.m': 'Objective-C/MATLAB',
    '.mm': 'Objective-C++',
    '.pl': 'Perl',
    '.pm': 'Perl Module',
    '.lua': 'Lua',
    '.sql': 'SQL',
    '.json': 'JSON',
    '.yaml': 'YAML',
    '.yml': 'YAML',
    '.toml': 'TOML',
    '.ini': 'INI',
    '.cfg': 'Config',
    '.conf': 'Config',
    '.md': 'Markdown',
    '.rst': 'reStructuredText',
    '.tex': 'LaTeX',
    '.vim': 'Vim Script',
    '.el': 'Emacs Lisp',
    '.clj': 'Clojure',
    '.cljs': 'ClojureScript',
    '.hs': 'Haskell',
    '.elm': 'Elm',
    '.ex': 'Elixir',
    '.exs': 'Elixir Script',
    '.erl': 'Erlang',
    '.hrl': 'Erlang Header',
    '.ml': 'OCaml',
    '.mli': 'OCaml Interface',
    '.fs': 'F#',
    '.fsx': 'F# Script',
    '.jl': 'Julia',
    '.nim': 'Nim',
    '.cr': 'Crystal',
    '.zig': 'Zig',
    '.v': 'V/Verilog',
    '.sv': 'SystemVerilog',
    '.vhd': 'VHDL',
    '.vhdl': 'VHDL',
    '.dockerfile': 'Dockerfile',
    '.makefile': 'Makefile',
    '.cmake': 'CMake',
    '.gradle': 'Gradle',
    '.sbt': 'SBT'
}

def execute_command(command, cwd=None):
    """执行系统命令"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd,
            capture_output=True, 
            text=True,
            timeout=300  # 5分钟超时
        )
        if result.returncode != 0:
            raise Exception(f"Command failed: {result.stderr}")
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        raise Exception("Command timeout")
    except Exception as e:
        raise Exception(f"Command execution error: {str(e)}")

def count_code_lines(directory):
    """统计代码行数"""
    total_lines = 0
    file_stats = {}
    
    # 特殊文件名（无扩展名但需要统计的文件）
    SPECIAL_FILES = {
        'dockerfile': 'Dockerfile',
        'makefile': 'Makefile', 
        'rakefile': 'Rakefile',
        'gemfile': 'Gemfile',
        'podfile': 'Podfile',
        'vagrantfile': 'Vagrantfile',
        'jenkinsfile': 'Jenkinsfile',
        'fastfile': 'Fastfile',
        'appfile': 'Appfile'
    }
    
    for root, dirs, files in os.walk(directory):
        # 跳过常见的非代码目录，但减少过滤
        dirs[:] = [d for d in dirs if d not in [
            'node_modules', '__pycache__', '.git', 'dist', 'build', 'target', 
            'bin', 'obj', '.gradle', '.idea', '.vscode', '.vs'
        ]]
        
        for file in files:
            file_path = os.path.join(root, file)
            file_lower = file.lower()
            _, ext = os.path.splitext(file_lower)
            
            # 跳过二进制文件和特定文件
            if any(file_lower.endswith(suffix) for suffix in [
                '.exe', '.dll', '.so', '.dylib', '.a', '.o', '.obj',
                '.png', '.jpg', '.jpeg', '.gif', '.ico', '.svg', '.webp',
                '.mp4', '.avi', '.mov', '.wmv', '.mp3', '.wav', '.ogg',
                '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2',
                '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
                '.lock', '.log', '.tmp', '.cache', '.pid'
            ]):
                continue
                
            # 检查特殊文件名
            is_special_file = False
            for special_name, lang in SPECIAL_FILES.items():
                if file_lower == special_name or file_lower.endswith('/' + special_name):
                    ext = f'.{special_name}'
                    if ext not in SUPPORTED_EXTENSIONS:
                        SUPPORTED_EXTENSIONS[ext] = lang
                    is_special_file = True
                    break
            
            # 统计代码文件
            if ext in SUPPORTED_EXTENSIONS or is_special_file:
                try:
                    # 尝试多种编码
                    content = None
                    for encoding in ['utf-8', 'utf-16', 'iso-8859-1', 'cp1252']:
                        try:
                            with open(file_path, 'r', encoding=encoding) as f:
                                content = f.read()
                            break
                        except UnicodeDecodeError:
                            continue
                    
                    if content is not None:
                        lines = len(content.splitlines())
                        total_lines += lines
                        
                        if ext not in file_stats:
                            file_stats[ext] = {
                                'language': SUPPORTED_EXTENSIONS.get(ext, 'Unknown'),
                                'files': 0,
                                'lines': 0
                            }
                        
                        file_stats[ext]['files'] += 1
                        file_stats[ext]['lines'] += lines
                        
                except Exception as e:
                    logger.warning(f"Error reading file {file_path}: {str(e)}")
                    continue
    
    return total_lines, file_stats

@app.route('/health', methods=['GET'])
def health_check():
    """健康检查端点"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'service': 'GitHub Code Counter'
    })

@app.route('/analyze', methods=['POST'])
def analyze_repository():
    """分析GitHub仓库"""
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'No JSON data provided'
        }), 400
    
    repo_url = data.get('repoUrl')
    clone_url = data.get('cloneUrl')
    owner = data.get('owner')
    repo = data.get('repo')
    
    if not clone_url:
        return jsonify({
            'success': False,
            'error': 'Repository clone URL is required'
        }), 400
    
    # 生成唯一的会话ID
    session_id = str(uuid.uuid4())
    temp_dir = None
    
    try:
        logger.info(f"Starting analysis for {repo_url}")
        
        # 创建临时目录
        temp_dir = os.path.join(tempfile.gettempdir(), f"github_analysis_{session_id}")
        os.makedirs(temp_dir, exist_ok=True)
        
        # 克隆仓库
        logger.info("Cloning repository...")
        clone_command = f"git clone --depth 1 {clone_url} repo"
        execute_command(clone_command, cwd=temp_dir)
        
        repo_dir = os.path.join(temp_dir, 'repo')
        
        if not os.path.exists(repo_dir):
            raise Exception("Repository clone failed")
        
        # 统计代码行数
        logger.info("Counting code lines...")
        total_lines, file_stats = count_code_lines(repo_dir)
        
        # 清理临时文件
        shutil.rmtree(temp_dir)
        temp_dir = None
        
        logger.info(f"Analysis completed. Total lines: {total_lines}")
        
        return jsonify({
            'success': True,
            'repoUrl': repo_url,
            'owner': owner,
            'repo': repo,
            'lines': total_lines,
            'fileStats': file_stats,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        
        # 清理临时文件
        if temp_dir and os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
            except Exception as cleanup_error:
                logger.error(f"Cleanup error: {str(cleanup_error)}")
        
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/stats', methods=['GET'])
def get_stats():
    """获取服务器统计信息"""
    return jsonify({
        'supported_languages': len(SUPPORTED_EXTENSIONS),
        'extensions': list(SUPPORTED_EXTENSIONS.keys()),
        'languages': list(set(SUPPORTED_EXTENSIONS.values()))
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5003))
    debug = os.environ.get('DEBUG', 'false').lower() == 'true'
    
    print(f"GitHub Code Counter Server starting...")
    print(f"Port: {port}")
    print(f"Debug mode: {debug}")
    print(f"Health check: http://localhost:{port}/health")
    print(f"Analysis endpoint: http://localhost:{port}/analyze")
    print(f"Stats endpoint: http://localhost:{port}/stats")
    
    app.run(host='0.0.0.0', port=port, debug=debug)