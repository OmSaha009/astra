import subprocess, os, tempfile, sys

def run(code: str, timeout_sec: int = 15) -> str:
    if not code.startswith('# coding') and not code.startswith('# -*- coding'):
        try:
            code.encode('ascii')
        except UnicodeEncodeError:
            code = '# -*- coding: utf-8 -*-\n' + code
    path = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(code)
            path = f.name
            f.flush()

            result = subprocess.run(
                [sys.executable, path],
                text=True,
                capture_output=True,
                timeout=timeout_sec,
                encoding='utf-8',
            )
            print(f"DEBUG stdout: {repr(result.stdout)}")
            print(f"DEBUG stderr: {repr(result.stderr)}")
            print(f"RETURN CODE: {result.returncode}")
            return result.stdout if result.stdout else ("Error" + str(result.stderr))
    except subprocess.TimeoutExpired:
        return "Error: Timeout (>5s)"
    except Exception as e:
        return f"Error: {e}"
    
    finally:
        if os.path.exists(path):
            os.remove(path)