"""
Tests for the GET / endpoint (root redirect).

These tests verify that the root endpoint properly redirects to the static index.html page.
"""

import pytest


class TestRootEndpoint:
    """Tests for the root endpoint."""

    def test_root_redirects_to_static_index(self, test_client):
        """Test that GET / redirects to /static/index.html."""
        response = test_client.get("/", follow_redirects=False)
        
        assert response.status_code == 307  # Temporary redirect
        assert response.headers["location"] == "/static/index.html"

    def test_root_redirect_follows_to_index(self, test_client):
        """Test that following the redirect reaches the static index page."""
        response = test_client.get("/", follow_redirects=True)
        
        # After following redirect, we get the static HTML file
        assert response.status_code == 200
        # Response should be HTML content from index.html
        assert "text/html" in response.headers.get("content-type", "").lower() or \
               len(response.text) > 0  # May be HTML or plain text depending on StaticFiles serving

    def test_root_returns_redirect_response_type(self, test_client):
        """Test that root endpoint returns a redirect response."""
        response = test_client.get("/", follow_redirects=False)
        
        # Check it's a redirect status code
        assert 300 <= response.status_code < 400, "Should return a redirect status code"

    def test_root_without_follow_redirects_shows_location_header(self, test_client):
        """Test that redirect response includes the Location header."""
        response = test_client.get("/", follow_redirects=False)
        
        assert "location" in response.headers
        location = response.headers["location"]
        assert location == "/static/index.html"
