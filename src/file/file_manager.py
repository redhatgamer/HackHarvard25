"""
File Manager
Handles safe file operations for code generation and editing
"""

import os
import shutil
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import json

class FileManager:
    """Manages file operations with safety features"""
    
    def __init__(self, workspace_root: Optional[str] = None):
        self.logger = logging.getLogger(__name__)
        self.workspace_root = Path(workspace_root) if workspace_root else Path.cwd()
        self.backup_dir = self.workspace_root / ".pet_backups"
        self.backup_dir.mkdir(exist_ok=True)
        
        # Safety settings
        self.allowed_extensions = {
            '.py', '.js', '.ts', '.java', '.cpp', '.c', '.cs', '.go', '.rs',
            '.php', '.rb', '.swift', '.kt', '.html', '.css', '.sql', '.sh',
            '.ps1', '.json', '.xml', '.yaml', '.yml', '.md', '.txt', '.cfg',
            '.ini', '.toml', '.env'
        }
        
        # Directories to avoid
        self.forbidden_dirs = {
            'node_modules', '__pycache__', '.git', '.venv', 'venv',
            'build', 'dist', '.pytest_cache', 'target'
        }
    
    def is_safe_file(self, file_path: str) -> bool:
        """Check if file is safe to edit"""
        try:
            path = Path(file_path).resolve()
            
            # Check if within workspace
            if not str(path).startswith(str(self.workspace_root.resolve())):
                self.logger.warning(f"File outside workspace: {path}")
                return False
            
            # Check extension
            if path.suffix.lower() not in self.allowed_extensions:
                self.logger.warning(f"Unsafe file extension: {path.suffix}")
                return False
            
            # Check forbidden directories
            for part in path.parts:
                if part in self.forbidden_dirs:
                    self.logger.warning(f"File in forbidden directory: {part}")
                    return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error checking file safety: {e}")
            return False
    
    def create_backup(self, file_path: str) -> Optional[str]:
        """Create backup of existing file"""
        try:
            source = Path(file_path)
            if not source.exists():
                return None
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{source.stem}_{timestamp}{source.suffix}"
            backup_path = self.backup_dir / backup_name
            
            shutil.copy2(source, backup_path)
            self.logger.info(f"Created backup: {backup_path}")
            return str(backup_path)
            
        except Exception as e:
            self.logger.error(f"Failed to create backup: {e}")
            return None
    
    def read_file(self, file_path: str) -> Dict[str, Any]:
        """Safely read file content"""
        try:
            if not self.is_safe_file(file_path):
                return {
                    'success': False,
                    'error': 'File is not safe to read'
                }
            
            path = Path(file_path)
            if not path.exists():
                return {
                    'success': False,
                    'error': 'File does not exist'
                }
            
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return {
                'success': True,
                'content': content,
                'size': len(content),
                'lines': content.count('\n') + 1,
                'extension': path.suffix,
                'modified': datetime.fromtimestamp(path.stat().st_mtime)
            }
            
        except Exception as e:
            self.logger.error(f"Error reading file {file_path}: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def write_file(self, file_path: str, content: str, create_backup: bool = True) -> Dict[str, Any]:
        """Safely write content to file"""
        try:
            if not self.is_safe_file(file_path):
                return {
                    'success': False,
                    'error': 'File is not safe to write'
                }
            
            path = Path(file_path)
            backup_path = None
            
            # Create backup if file exists
            if path.exists() and create_backup:
                backup_path = self.create_backup(file_path)
            
            # Ensure directory exists
            path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write content
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.logger.info(f"Successfully wrote file: {path}")
            
            return {
                'success': True,
                'path': str(path),
                'size': len(content),
                'backup': backup_path,
                'created': not path.existed_before if hasattr(path, 'existed_before') else False
            }
            
        except Exception as e:
            self.logger.error(f"Error writing file {file_path}: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def create_new_file(self, filename: str, content: str, directory: str = "") -> Dict[str, Any]:
        """Create a new file with generated content"""
        try:
            if directory:
                file_path = Path(directory) / filename
            else:
                file_path = self.workspace_root / filename
            
            # Check if file already exists
            if file_path.exists():
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                stem = file_path.stem
                suffix = file_path.suffix
                file_path = file_path.parent / f"{stem}_{timestamp}{suffix}"
            
            result = self.write_file(str(file_path), content, create_backup=False)
            
            if result['success']:
                result['message'] = f"Created new file: {file_path.name}"
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error creating new file: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def analyze_project_structure(self) -> Dict[str, Any]:
        """Analyze current project structure"""
        try:
            structure = {
                'files': [],
                'directories': [],
                'languages': set(),
                'frameworks': [],
                'config_files': []
            }
            
            for item in self.workspace_root.rglob('*'):
                if item.is_file() and self.is_safe_file(str(item)):
                    rel_path = item.relative_to(self.workspace_root)
                    
                    file_info = {
                        'path': str(rel_path),
                        'name': item.name,
                        'extension': item.suffix,
                        'size': item.stat().st_size,
                        'modified': datetime.fromtimestamp(item.stat().st_mtime)
                    }
                    
                    structure['files'].append(file_info)
                    
                    # Detect language
                    ext = item.suffix.lower()
                    if ext in ['.py']: structure['languages'].add('Python')
                    elif ext in ['.js', '.jsx']: structure['languages'].add('JavaScript')
                    elif ext in ['.ts', '.tsx']: structure['languages'].add('TypeScript')
                    elif ext in ['.java']: structure['languages'].add('Java')
                    elif ext in ['.cpp', '.c']: structure['languages'].add('C/C++')
                    elif ext in ['.cs']: structure['languages'].add('C#')
                    elif ext in ['.go']: structure['languages'].add('Go')
                    elif ext in ['.rs']: structure['languages'].add('Rust')
                    elif ext in ['.php']: structure['languages'].add('PHP')
                    elif ext in ['.rb']: structure['languages'].add('Ruby')
                    
                    # Detect config files
                    if item.name in ['package.json', 'requirements.txt', 'Cargo.toml', 'pom.xml', 'build.gradle']:
                        structure['config_files'].append(str(rel_path))
            
            # Detect frameworks
            if 'package.json' in [f['name'] for f in structure['files']]:
                structure['frameworks'].append('Node.js')
            if 'requirements.txt' in [f['name'] for f in structure['files']]:
                structure['frameworks'].append('Python')
            if any('react' in f['path'].lower() for f in structure['files']):
                structure['frameworks'].append('React')
            
            structure['languages'] = list(structure['languages'])
            
            return {
                'success': True,
                'structure': structure,
                'total_files': len(structure['files']),
                'primary_language': structure['languages'][0] if structure['languages'] else 'Unknown'
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing project structure: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_recent_files(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recently modified files"""
        try:
            files = []
            
            for item in self.workspace_root.rglob('*'):
                if item.is_file() and self.is_safe_file(str(item)):
                    files.append({
                        'path': str(item.relative_to(self.workspace_root)),
                        'name': item.name,
                        'modified': datetime.fromtimestamp(item.stat().st_mtime),
                        'size': item.stat().st_size
                    })
            
            # Sort by modification time (newest first)
            files.sort(key=lambda x: x['modified'], reverse=True)
            
            return files[:limit]
            
        except Exception as e:
            self.logger.error(f"Error getting recent files: {e}")
            return []
    
    def suggest_filename(self, description: str, language: str = "python") -> str:
        """Suggest appropriate filename based on description"""
        try:
            # Clean description for filename
            import re
            clean_desc = re.sub(r'[^\w\s-]', '', description.lower())
            clean_desc = re.sub(r'[-\s]+', '_', clean_desc)
            
            # Get extension
            ext_map = {
                'python': 'py',
                'javascript': 'js',
                'typescript': 'ts',
                'java': 'java',
                'cpp': 'cpp',
                'c': 'c',
                'csharp': 'cs',
                'html': 'html',
                'css': 'css'
            }
            
            ext = ext_map.get(language.lower(), 'txt')
            
            # Limit length
            if len(clean_desc) > 50:
                clean_desc = clean_desc[:50]
            
            return f"{clean_desc}.{ext}"
            
        except Exception as e:
            self.logger.error(f"Error suggesting filename: {e}")
            return f"generated_code.{ext_map.get(language.lower(), 'txt')}"
    
    def list_backups(self) -> List[Dict[str, Any]]:
        """List all available backups"""
        try:
            backups = []
            
            if not self.backup_dir.exists():
                return backups
            
            for backup_file in self.backup_dir.iterdir():
                if backup_file.is_file():
                    backups.append({
                        'name': backup_file.name,
                        'path': str(backup_file),
                        'size': backup_file.stat().st_size,
                        'created': datetime.fromtimestamp(backup_file.stat().st_ctime)
                    })
            
            # Sort by creation time (newest first)
            backups.sort(key=lambda x: x['created'], reverse=True)
            
            return backups
            
        except Exception as e:
            self.logger.error(f"Error listing backups: {e}")
            return []
    
    def restore_backup(self, backup_name: str, target_path: str) -> Dict[str, Any]:
        """Restore file from backup"""
        try:
            backup_path = self.backup_dir / backup_name
            
            if not backup_path.exists():
                return {
                    'success': False,
                    'error': 'Backup file not found'
                }
            
            if not self.is_safe_file(target_path):
                return {
                    'success': False,
                    'error': 'Target path is not safe'
                }
            
            # Create backup of current file before restore
            current_backup = self.create_backup(target_path)
            
            # Restore from backup
            shutil.copy2(backup_path, target_path)
            
            return {
                'success': True,
                'restored_from': str(backup_path),
                'restored_to': target_path,
                'current_backup': current_backup
            }
            
        except Exception as e:
            self.logger.error(f"Error restoring backup: {e}")
            return {
                'success': False,
                'error': str(e)
            }