"""Test cases for the __main__ module."""
import pytest
import unittest
from typer.testing import CliRunner

from mqsense.__main__ import app, get_connection_details


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


@pytest.fixture
def test_case() -> unittest.TestCase:
    return unittest.TestCase()


def test_main_succeeds(runner: CliRunner, test_case: unittest.TestCase) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(app, ["--version"])
    test_case.assertEqual(result.exit_code, 0)


def test_get_random_clientid(test_case: unittest.TestCase) -> None:
    det1 = get_connection_details("host", "user", "password")
    det2 = get_connection_details("host", "user", "password")
    test_case.assertNotEqual(det1.clientId, det2.clientId)
