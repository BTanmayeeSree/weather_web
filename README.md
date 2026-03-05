# Weather Forecast (FastAPI)

Minimal FastAPI project that fetches hourly temperature forecasts from Open-Meteo.

Quickstart (Windows):

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\uvicorn app.main:app --reload
```

Run tests:

```powershell
.venv\Scripts\python -m pytest -q
```

A GitHub Actions workflow (`.github/workflows/ci.yml`) is included to run the same tests on every push or pull request.

Endpoint:
- `GET /forecast?lat={latitude}&lon={longitude}` — returns hourly temperature for the next day.

Static frontend available at `/static/index.html` (root redirects there). Start the server and visit http://localhost:8000 to try it.

### Quick start scripts

A helper batch/shell script will prepare the venv and launch the server automatically:

- **Windows:** run `run.bat`
- **macOS/Linux:** run `./run.sh` (make executable with `chmod +x run.sh`)

### VS Code Task

Open the Command Palette (Ctrl+Shift+P) and execute **Tasks: Run Task → Start FastAPI server** to run the application inside the editor.


## Next steps

- Add caching or improved error handling in `app/weather.py` to reduce external API calls and handle failures gracefully.
- Enhance the frontend with graphs, location search, or responsive styling.
- Containerize the application with Docker for easier deployment.
- Integrate with a real user interface or mobile client.
- Push to GitHub to trigger the CI workflow.

Feel free to pick any of these enhancements or extend the project further!
