
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import main


class TestQuizState(unittest.TestCase):

    def test_save_and_load_state(self):
        # 실제 state.json 대신 임시 파일 사용
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / "state.json"

            with patch.object(main, "STATE_FILE", test_file):
                # 테스트용 게임 생성
                game = main.QuizGame()

                # 테스트 점수 설정
                game.high_score = 100
                game.last_score = 80

                # JSON 저장 확인
                self.assertTrue(game.save_state())
                self.assertTrue(test_file.exists())

                # 새로운 게임 객체에서 다시 읽기
                reloaded_game = main.QuizGame()

                # 저장된 데이터 비교
                self.assertEqual(reloaded_game.high_score, 100)
                self.assertEqual(reloaded_game.last_score, 80)
                self.assertEqual(
                    len(reloaded_game.quizzes),
                    len(game.quizzes)
                )

    def test_invalid_json_syntax(self):
        """JSON 문법 오류 발생 시 기본 퀴즈로 복구"""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / "state.json"

            test_file.write_text(
                "{invalid json",
                encoding="utf-8"
            )

            with patch.object(main, "STATE_FILE", test_file):
                game = main.QuizGame()

                self.assertEqual(
                    len(game.quizzes),
                    len(main.DEFAULT_QUIZZES)
                )

                self.assertEqual(game.high_score, 0)
                self.assertEqual(game.last_score, 0)

    def test_invalid_quizzes_structure(self):
        """quizzes 자료형이 잘못된 경우 기본 퀴즈로 복구"""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / "state.json"

            test_file.write_text(
                '{"quizzes": "잘못된 데이터", '
                '"high_score": 100, "last_score": 100}',
                encoding="utf-8"
            )

            with patch.object(main, "STATE_FILE", test_file):
                game = main.QuizGame()

                self.assertEqual(
                    len(game.quizzes),
                    len(main.DEFAULT_QUIZZES)
                )

                self.assertEqual(game.high_score, 0)
                self.assertEqual(game.last_score, 0)


if __name__ == "__main__":
    unittest.main()
