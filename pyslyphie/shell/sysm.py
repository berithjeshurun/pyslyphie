import os
import json
import time
from typing import Dict, Union


class SimpleEncryptor:
    def __init__(self, key: str):
        self.key = key.encode()

    def encrypt(self, data: str) -> str:
        data_bytes = data.encode()
        enc = bytes([b ^ self.key[i % len(self.key)] for i, b in enumerate(data_bytes)])
        return enc.hex()
    
    def decrypt(self, hex_str: str) -> str:
        data_bytes = bytes.fromhex(hex_str)
        dec = bytes([b ^ self.key[i % len(self.key)] for i, b in enumerate(data_bytes)])
        return dec.decode(errors="ignore")



class VirtualDisk:
    def __init__(self, path: str, size_gb: float):
        self.path = path
        self.size_bytes = int(size_gb * 1024 * 1024 * 1024)
        if not os.path.exists(path):
            print(f"[+] Creating virtual disk: {path} ({size_gb} GB)")
            with open(path, 'wb') as f:
                f.truncate(self.size_bytes)
        else:
            print(f"[~] Using existing disk: {path}")
        self.file = open(path, 'r+b')

    def write_data(self, offset: int, data: bytes):
        self.file.seek(offset)
        self.file.write(data)

    def read_data(self, offset: int, size: int) -> bytes:
        self.file.seek(offset)
        return self.file.read(size)

    def close(self):
        self.file.close()



class VirtualFileSystem:
    def __init__(self, disk: VirtualDisk, encryption_key: str = "default_key"):
        self.disk = disk
        self.fs_tree: Dict[str, Union[dict, str]] = {"type": "dir", "children": {}}
        self.meta_offset = 0
        self.data_offset = 4096
        self.encryptor = SimpleEncryptor(encryption_key)
        self.load_filesystem()

    def load_filesystem(self):
        self.disk.file.seek(self.meta_offset)
        raw = self.disk.file.read(8192).strip(b"\x00")
        if raw:
            try:
                self.fs_tree = json.loads(raw.decode())
                print("[~] Loaded existing filesystem tree.")
            except Exception:
                print("[!] Corrupted FS tree, resetting.")
        else:
            print("[+] New filesystem initialized.")
            self.save_filesystem()

    def save_filesystem(self):
        data = json.dumps(self.fs_tree).encode()
        if len(data) > 8192:
            raise ValueError("FS metadata too large!")
        self.disk.write_data(self.meta_offset, data.ljust(8192, b"\x00"))

    def _get_node(self, path: str):
        parts = [p for p in path.strip("/").split("/") if p]
        node = self.fs_tree
        for part in parts:
            if part not in node["children"]:
                raise FileNotFoundError(path)
            node = node["children"][part]
        return node

    def _update_timestamp(self, node: dict, mode="modified"):
        node["timestamps"][mode] = time.time()

    def mkdir(self, path: str, permissions: str = "rwxr-xr-x"):
        parts = [p for p in path.strip("/").split("/") if p]
        node = self.fs_tree
        for part in parts:
            if part not in node["children"]:
                node["children"][part] = {
                    "type": "dir",
                    "children": {},
                    "permissions": permissions,
                    "timestamps": {
                        "created": time.time(),
                        "modified": time.time(),
                        "accessed": time.time()
                    }
                }
            node = node["children"][part]
        self.save_filesystem()
        print(f"[+] Directory created: {path}")

    def write_file(self, path: str, data: str, permissions: str = "rw-r--r--"):
        parts = [p for p in path.strip("/").split("/") if p]
        filename = parts[-1]
        node = self.fs_tree
        for part in parts[:-1]:
            node = node["children"].setdefault(part, {
                "type": "dir",
                "children": {},
                "permissions": "rwxr-xr-x",
                "timestamps": {
                    "created": time.time(),
                    "modified": time.time(),
                    "accessed": time.time()
                }
            })
        enc_data = self.encryptor.encrypt(data)
        node["children"][filename] = {
            "type": "file",
            "data": enc_data,
            "permissions": permissions,
            "timestamps": {
                "created": time.time(),
                "modified": time.time(),
                "accessed": time.time()
            }
        }
        self.save_filesystem()
        print(f"[+] File written (encrypted): {path}")

    def read_file(self, path: str) -> str:
        node = self._get_node(path)
        if node["type"] != "file":
            raise IsADirectoryError(path)
        node["timestamps"]["accessed"] = time.time()
        dec_data = self.encryptor.decrypt(node["data"])
        self.save_filesystem()
        return dec_data

    def list_dir(self, path: str = "/"):
        node = self._get_node(path) if path != "/" else self.fs_tree
        if node["type"] != "dir":
            raise NotADirectoryError(path)
        return list(node["children"].keys())

    def delete(self, path: str):
        parts = [p for p in path.strip("/").split("/") if p]
        node = self.fs_tree
        for part in parts[:-1]:
            node = node["children"].get(part)
            if not node:
                raise FileNotFoundError(path)
        node["children"].pop(parts[-1], None)
        self.save_filesystem()
        print(f"[-] Deleted: {path}")

    def change_metadata(self, path: str, permissions: str = None, timestamps: Dict[str, float] = None):
        node = self._get_node(path)
        if permissions:
            node["permissions"] = permissions
        if timestamps:
            node["timestamps"].update(timestamps)
        self.save_filesystem()
        print(f"[~] Metadata updated for {path}")