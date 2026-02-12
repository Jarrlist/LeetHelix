import pytest
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock
from leet_helix.main import select_smart_challenge

def test_select_smart_challenge_never_attempted(monkeypatch):
    challenges = [
        {"id": "c1", "title": "C1"},
        {"id": "c2", "title": "C2"},
    ]
    
    # Mock database returning no attempts
    monkeypatch.setattr("leet_helix.main.get_attempts", lambda: [])
        
    selected = select_smart_challenge(challenges)
    assert selected in challenges

def test_select_smart_challenge_prioritize_failed(monkeypatch):
    challenges = [
        {"id": "c1", "title": "C1"}, # Attempted and passed
        {"id": "c2", "title": "C2"}, # Attempted and failed
    ]
    
    # Mock attempts
    c1_attempt = MagicMock()
    c1_attempt.challenge_id = "c1"
    c1_attempt.is_correct = True
    c1_attempt.timestamp = datetime.now(timezone.utc)
    
    c2_attempt = MagicMock()
    c2_attempt.challenge_id = "c2"
    c2_attempt.is_correct = False
    c2_attempt.timestamp = datetime.now(timezone.utc)
    
    attempts = [c1_attempt, c2_attempt]
    
    monkeypatch.setattr("leet_helix.main.get_attempts", lambda: attempts)
    
    # Should pick c2 because it was failed
    selected = select_smart_challenge(challenges)
    assert selected["id"] == "c2"

def test_select_smart_challenge_prioritize_oldest_solved(monkeypatch):
    challenges = [
        {"id": "c1", "title": "C1"}, # Solved long ago
        {"id": "c2", "title": "C2"}, # Solved recently
    ]
    
    now = datetime.now(timezone.utc)
    old = now - timedelta(days=10)
    recent = now - timedelta(days=1)
    
    # Mock attempts
    c1_attempt = MagicMock()
    c1_attempt.challenge_id = "c1"
    c1_attempt.is_correct = True
    c1_attempt.timestamp = old
    
    c2_attempt = MagicMock()
    c2_attempt.challenge_id = "c2"
    c2_attempt.is_correct = True
    c2_attempt.timestamp = recent
    
    attempts = [c1_attempt, c2_attempt]
    
    monkeypatch.setattr("leet_helix.main.get_attempts", lambda: attempts)
    
    # Should pick c1 because it was solved longest ago
    selected = select_smart_challenge(challenges)
    assert selected["id"] == "c1"
