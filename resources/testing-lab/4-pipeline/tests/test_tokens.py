import pandas as pd
import pytest

from pipeline import add_n_tokens


@pytest.mark.parametrize(
    "text, expected",
    [
        ("le chat dort", 3),
        ("un   deux", 2),
        ("Super !", 2),  # a choice we made: "!" counts as a token
    ],
)
def test_add_n_tokens(text: str, expected: int) -> None:
    # un tableau d'une seule ligne, qui contient le texte à tester
    reviews = pd.DataFrame({"text": [text]})
    # la colonne n_tokens doit contenir le nombre de mots attendu
    assert add_n_tokens(reviews)["n_tokens"].tolist() == [expected]
