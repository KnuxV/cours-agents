"""Test label_review() without calling the LLM: no network, no API key.

monkeypatch.setattr replaces labeler.ask_llm with a fake for the duration
of one test, then puts the real one back.
"""
import pytest

import labeler


def test_positive_answer(monkeypatch: pytest.MonkeyPatch) -> None:
    # on remplace ask_llm par une fausse fonction qui répond toujours "positive"
    monkeypatch.setattr(labeler, "ask_llm", lambda prompt: "positive")
    # label_review doit traduire cette réponse en "pos"
    assert labeler.label_review("Très bon livre") == "pos"


def test_answer_with_capital_and_full_stop(monkeypatch: pytest.MonkeyPatch) -> None:
    # le faux modèle répond avec une majuscule et un point : le nettoyage doit les enlever
    monkeypatch.setattr(labeler, "ask_llm", lambda prompt: "Negative.")
    assert labeler.label_review("Arrivé cassé") == "neg"


def test_unexpected_answer(monkeypatch: pytest.MonkeyPatch) -> None:
    # le faux modèle répond par une phrase : ni positif ni négatif, donc "unknown"
    monkeypatch.setattr(labeler, "ask_llm", lambda prompt: "I think it is mixed")
    assert labeler.label_review("Bof") == "unknown"
