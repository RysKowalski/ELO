class EloCalc:
    def calculate_elo(
        self, rating1: float, rating2: float, game_result: float, k: float = 50
    ) -> tuple[float, float]:
        expected1: float = 1.0 / (1.0 + 10 ** ((rating2 - rating1) / 400.0))

        expected2: float = 1.0 / (1.0 + 10 ** ((rating1 - rating2) / 400.0))

        new_rating1: float = self._calculate_rating(rating1, game_result, expected1, k)

        new_rating2: float = self._calculate_rating(
            rating2, self._flip_game_result(game_result), expected2, k
        )

        return new_rating1, new_rating2

    def _calculate_rating(
        self,
        current_rating: float,
        actual_score: float,
        expected_score: float,
        k: float,
    ) -> float:
        return current_rating + k * (actual_score - expected_score)

    @staticmethod
    def _flip_game_result(game_result: float) -> float:
        return 1.0 - game_result
