#!/usr/bin/env python3
"""Check argument forwarding without touching any real preferences."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='dotfiles macos ') as temporary:
    root = Path(temporary)
    folder = root / 'configuration with spaces'
    shutil.copytree(ROOT / 'macos', folder)
    tools = root / 'bin'
    tools.mkdir()
    cli = tools / 'mac-setup'
    cli.write_text('#!/usr/bin/env python3\nimport json,os,sys\nopen(os.environ["ARGUMENT_RECORD"],"w").write(json.dumps(sys.argv[1:]))\n')
    cli.chmod(0o755)
    record = root / 'arguments.json'
    env = dict(os.environ, PATH=str(tools)+os.pathsep+os.environ['PATH'], ARGUMENT_RECORD=str(record))
    for arguments in [[], ['plan'], ['off', '--dry-run'], ['apply', '--yes']]:
        subprocess.run(['bash', str(folder / 'apply.sh'), *arguments], env=env, check=True)
        assert json.loads(record.read_text()) == ['macos', *(arguments or ['apply']), '--config', str(folder / 'preferences.json')]
print('macOS wrapper forwards subcommands, flags and paths without applying preferences')
