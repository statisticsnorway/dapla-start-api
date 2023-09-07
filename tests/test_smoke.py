import subprocess


def test_server_starts():
    try:
        server = subprocess.run(
            ["uvicorn", "server.api:app", "--host", "0.0.0.0"],
            capture_output=True,
            timeout=2,
            check=True,
            text=True,
        )
    except subprocess.TimeoutExpired as e:
        # This is expected/desired behaviour
        assert "Application startup complete." in str(e.stderr)
    except subprocess.CalledProcessError as e:
        print("Process output:")
        print("".join(e.stderr))
        assert e.returncode == 0
    else:
        assert "Application startup complete." in str(server.stderr)
