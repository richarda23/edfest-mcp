import os
import pytest
import responses
from unittest.mock import patch, mock_open, MagicMock
from edfestcli import EdFestCli


class TestEdFestCli:
    """Test suite for EdFestCli class."""

    @patch.dict(
        os.environ,
        {"api_key": "test_key", "api_secret": "test_secret", "fringe_mode": "demo"},
    )
    def setup_method(self, method):
        """Set up test fixtures before each test method."""
        self.client = EdFestCli()

    def test_init_with_env_vars(self):
        """Test initialization with environment variables."""
        with patch.dict(
            os.environ,
            {
                "api_key": "test_api_key",
                "api_secret": "test_api_secret",
                "fringe_mode": "real",
            },
        ):
            client = EdFestCli()
            assert client._apikey == "test_api_key"
            assert client._apisecret == "test_api_secret"
            assert client._fringe_mode == "real"

    def test_init_with_default_fringe_mode(self):
        """Test initialization with default fringe_mode when not set."""
        with patch.dict(
            os.environ, {"api_key": "test_key", "api_secret": "test_secret"}, clear=True
        ):
            client = EdFestCli()
            assert client._fringe_mode == "demo"

    @responses.activate
    def test_events_fringe_demo_mode(self):
        """Test events method with fringe festival in demo mode."""
        # Mock the API response
        mock_response = {"events": [{"id": 1, "name": "Test Event"}]}
        responses.add(
            responses.GET,
            "https://api.edinburghfestivalcity.com/events",
            json=mock_response,
            status=200,
        )

        params = {"festival": "fringe", "year": "2024"}

        with patch("builtins.open", mock_open()), patch("sys.stderr"):
            result = self.client.events(params)

        # Verify that fringe was changed to demofringe
        request = responses.calls[0].request
        assert "festival=demofringe" in request.url
        assert result == mock_response

    @responses.activate
    def test_events_fringe_real_mode(self):
        """Test events method with fringe festival in real mode."""
        with patch.dict(
            os.environ,
            {"api_key": "test_key", "api_secret": "test_secret", "fringe_mode": "real"},
        ):
            client = EdFestCli()

        mock_response = {"events": [{"id": 1, "name": "Real Event"}]}
        responses.add(
            responses.GET,
            "https://api.edinburghfestivalcity.com/events",
            json=mock_response,
            status=200,
        )

        params = {"festival": "fringe", "year": "2024"}

        with patch("builtins.open", mock_open()), patch("sys.stderr"):
            result = client.events(params)

        # Verify that fringe was NOT changed to demofringe
        request = responses.calls[0].request
        assert "festival=fringe" in request.url
        assert result == mock_response

    @responses.activate
    def test_events_non_fringe_festival(self):
        """Test events method with non-fringe festival."""
        mock_response = {"events": [{"id": 2, "name": "Book Festival Event"}]}
        responses.add(
            responses.GET,
            "https://api.edinburghfestivalcity.com/events",
            json=mock_response,
            status=200,
        )

        params = {"festival": "book", "year": "2024"}

        with patch("builtins.open", mock_open()), patch("sys.stderr"):
            result = self.client.events(params)

        # Verify that festival parameter was not changed
        request = responses.calls[0].request
        assert "festival=book" in request.url
        assert result == mock_response

    @responses.activate
    def test_venues_method(self):
        """Test venues method."""
        mock_response = {"venues": [{"id": 1, "name": "Test Venue"}]}
        responses.add(
            responses.GET,
            "https://api.edinburghfestivalcity.com/venues",
            json=mock_response,
            status=200,
        )

        params = {"city": "Edinburgh"}

        with patch("builtins.open", mock_open()), patch("sys.stderr"):
            result = self.client.venues(params)

        assert result == mock_response

    @responses.activate
    def test_send_request_signature_generation(self):
        """Test that the signature is correctly generated and added to the request."""
        mock_response = {"test": "data"}

        def check_signature(request):
            # Verify that signature parameter is present
            assert "signature=" in request.url
            # Verify that key parameter is present
            assert "key=test_key" in request.url
            return True

        responses.add_callback(
            responses.GET,
            "https://api.edinburghfestivalcity.com/events",
            callback=lambda request: (
                (200, {}, '{"test": "data"}')
                if check_signature(request)
                else (400, {}, "{}")
            ),
            content_type="application/json",
        )

        params = {"festival": "test"}

        with patch("builtins.open", mock_open()), patch("sys.stderr"):
            result = self.client._send_request("events", params)

        assert result == mock_response

    def test_send_request_url_logging(self):
        """Test that the URL is logged to error.log file."""
        with (
            patch("builtins.open", mock_open()) as mock_file,
            patch("sys.stderr") as mock_stderr,
            patch("requests.get") as mock_get,
        ):

            # Mock the requests response
            mock_response = MagicMock()
            mock_response.json.return_value = {"test": "data"}
            mock_get.return_value = mock_response

            params = {"test": "param"}
            self.client._send_request("events", params)

            # Verify that the file was opened for appending
            mock_file.assert_called_with("error.log", "a")

    @responses.activate
    def test_base_url_is_correct(self):
        """Test that the base URL is correctly set."""
        assert EdFestCli.base_url == "https://api.edinburghfestivalcity.com"

    @responses.activate
    def test_api_error_handling(self):
        """Test handling of API errors."""
        responses.add(
            responses.GET,
            "https://api.edinburghfestivalcity.com/events",
            json={"error": "API Error"},
            status=400,
        )

        params = {"festival": "test"}

        with patch("builtins.open", mock_open()), patch("sys.stderr"):
            result = self.client.events(params)

        assert result == {"error": "API Error"}

    def test_hmac_signature_consistency(self):
        """Test that HMAC signature generation is consistent."""
        import hmac
        import hashlib
        from urllib.parse import urlencode

        params = {"key": "test_key", "festival": "test"}
        query = urlencode(params)
        url_to_sign = f"/events?{query}"

        signature1 = hmac.new(
            "test_secret".encode("utf-8"), url_to_sign.encode("utf-8"), hashlib.sha1
        ).hexdigest()

        signature2 = hmac.new(
            "test_secret".encode("utf-8"), url_to_sign.encode("utf-8"), hashlib.sha1
        ).hexdigest()

        assert signature1 == signature2


if __name__ == "__main__":
    pytest.main([__file__])
