import subprocess


def test_server_starts():
    try:
        server = subprocess.run(
            ["uvicorn", "server.api:app", "--host", "0.0.0.0"],
            timeout=2,
            check=True,
            text=True,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
        )
    except subprocess.TimeoutExpired as e:
        # This is expected/desired behaviour
        assert "Application startup complete." in str(e.stdout)
    except subprocess.CalledProcessError as e:
        print("Process output:")
        print("".join(e.stdout))
        assert e.returncode == 0
    else:
        assert "Application startup complete." in str(server.stdout)
