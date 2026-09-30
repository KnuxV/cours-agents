"""Test label_review() without calling the LLM: no network, no API key.

monkeypatch.setattr replaces labeler.ask_llm with a fake for the duration
of one test, then puts the real one back.
"""
import labeler


def test_positive_answer(monkeypatch):
    monkeypatch.setattr(labeler, "ask_llm", lambda prompt: "positive")
    assert labeler.label_review("Très bon livre") == "pos"


def test_answer_with_capital_and_full_stop(monkeypatch):
    monkeypatch.setattr(labeler, "ask_llm", lambda prompt: "Negative.")
    assert labeler.label_review("Arrivé cassé") == "neg"


def test_unexpected_answer(monkeypatch):
    monkeypatch.setattr(labeler, "ask_llm", lambda prompt: "I think it is mixed")
    assert labeler.label_review("Bof") == "unknown"
