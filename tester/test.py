import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from Client.Client import Client

# Helper to check success
def assert_success(response):
    assert response.status_code == 200

# Helper to check failure (anything other than 200)
def assert_failure(response):
    assert response.status_code != 200

# --- Successful tests ---

def test_bulk_upload_and_list():
    resp = Client("upload --file sample_data_1.csv").run()
    assert_success(resp)
    for _ in range(5):
        resp = Client("upload --file sample_data_2.csv").run()
        assert_success(resp)
    for _ in range(5):
        resp = Client("list").run()
        assert_success(resp)

def test_export_loop():
    for i in range(1, 5):
        resp = Client(f"export {i}").run()
        assert_success(resp)

def test_stats_loop():
    for i in range(1, 5):
        resp = Client(f"stats {i}").run()
        assert_success(resp)

def test_plot_loop():
    for i in range(1, 5):
        resp = Client(f"plot {i}").run()
        assert_success(resp)

def test_delete_loop():
    for i in range(1, 5):
        resp = Client(f"delete {i}").run()
        assert_success(resp)


# --- Tests expected to fail (bad commands or inputs) ---

def test_invalid_command():
    import argparse
    with pytest.raises(SystemExit):
        Client("invalidcommand").run()

def test_upload_missing_file():
    with pytest.raises(FileNotFoundError):
        Client("upload --file non_existent_file.csv").run()

def test_export_invalid_id():
    resp = Client("export 99999").run()
    assert_failure(resp)

def test_delete_invalid_id():
    resp = Client("delete 99999").run()
    assert_failure(resp)

def test_stats_invalid_arg():
    resp = Client("stats invalid_arg").run()
    assert_failure(resp)


# --- Rate limiting tests (limit=15 per endpoint) ---

def test_rate_limiter_upload():
    for _ in range(9):
        resp = Client("upload --file sample_data_1.csv").run()
        assert_success(resp)
    resp = Client("upload --file sample_data_1.csv").run()
    assert resp.status_code == 429  # rate limited

def test_rate_limiter_list():
    for i in range(10):
        resp = Client("list").run()
        assert_success(resp)
    resp = Client("list").run()
    assert resp.status_code == 429  # rate limited
