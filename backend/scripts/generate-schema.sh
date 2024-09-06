SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
python -c "import sys; sys.path.append('$SCRIPT_DIR/..'); import src.app, json, pathlib; pathlib.Path('openapi.json').write_text(json.dumps(src.app.app.openapi()))"
