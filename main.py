import json
import random
from dataclasses import asdict, dataclass
from pathlib import Path

STATE_FILE = Path(__file__).resolve().parent / "state.json"


@dataclass
class Quiz:
    question: str
    options: list[str]
    answer: int

    def ask(self) -> bool:
        print(f"\n{self.question}")
        for index, option in enumerate(self.options, start=1):
            print(f"  {index}. {option}")
        while True:
            choice = input("정답 번호 (1~4): ").strip()
            if choice in {"1", "2", "3", "4"}:
                correct = int(choice) == self.answer
                print("정답입니다!" if correct else f"오답입니다. 정답: {self.answer}번")
                return correct
            print("1~4 사이의 번호를 입력하세요.")


DEFAULT_QUIZZES = [
    Quiz("Python에서 리스트를 만드는 기호는?", ["{}", "[]", "()", "< >"], 2),
    Quiz("Python에서 함수를 정의하는 키워드는?", ["func", "function", "def", "make"], 3),
    Quiz("JSON 데이터를 Python 객체로 읽는 함수는?", ["json.loads()", "json.save()", "json.print()", "json.push()"], 1),
    Quiz("HTTP API에서 데이터를 조회할 때 주로 사용하는 메서드는?", ["POST", "DELETE", "PATCH", "GET"], 4),
    Quiz("Git에서 변경 내용을 기록하는 명령어는?", ["git commit", "git open", "git start", "git show-all"], 1),
    Quiz("AI에서 LLM은 무엇의 약자인가?", ["Local Logic Machine", "Large Language Model", "Long Learning Method", "Linked List Model"], 2),
]


class QuizGame:
    def __init__(self) -> None:
        self.quizzes = list(DEFAULT_QUIZZES)
        self.high_score = 0
        self.last_score = 0
        self.load_state()

    def load_state(self) -> None:
        if not STATE_FILE.exists():
            self.save_state()
            return
        try:
            with STATE_FILE.open("r", encoding="utf-8") as file:
                data = json.load(file)
            quizzes = [Quiz(**item) for item in data["quizzes"]]
            if not all(len(q.options) == 4 and 1 <= q.answer <= 4 for q in quizzes):
                raise ValueError("잘못된 퀴즈 데이터")
            self.quizzes = quizzes
            self.high_score = int(data.get("high_score", 0))
            self.last_score = int(data.get("last_score", 0))
        except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as error:
            print(f"저장 파일을 읽지 못했습니다: {error}")
            print("기본 문제로 시작합니다. 기존 파일은 다음 저장 시 덮어써질 수 있습니다.")

    def save_state(self) -> None:
        data = {
            "quizzes": [asdict(quiz) for quiz in self.quizzes],
            "high_score": self.high_score,
            "last_score": self.last_score,
        }
        with STATE_FILE.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    def play(self) -> None:
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return
        questions = random.sample(self.quizzes, k=min(5, len(self.quizzes)))
        correct_count = 0
        for index, quiz in enumerate(questions, start=1):
            print(f"\n[문제 {index}/{len(questions)}]")
            correct_count += int(quiz.ask())
        score = round(correct_count / len(questions) * 100)
        self.last_score = score
        self.high_score = max(self.high_score, score)
        self.save_state()
        print(f"\n게임 종료! {correct_count}/{len(questions)}문제 정답, 점수: {score}점")
        print(f"최고 점수: {self.high_score}점")

    def add_quiz(self) -> None:
        question = input("문제 내용을 입력하세요: ").strip()
        if not question:
            print("문제를 비워 둘 수 없습니다.")
            return
        options = []
        for index in range(1, 5):
            option = input(f"보기 {index}: ").strip()
            if not option:
                print("보기를 비워 둘 수 없습니다. 등록을 취소합니다.")
                return
            options.append(option)
        while True:
            answer = input("정답 번호 (1~4): ").strip()
            if answer in {"1", "2", "3", "4"}:
                break
            print("1~4 사이의 번호를 입력하세요.")
        self.quizzes.append(Quiz(question, options, int(answer)))
        self.save_state()
        print("퀴즈가 등록되고 저장되었습니다.")

    def list_quizzes(self) -> None:
        print(f"\n총 {len(self.quizzes)}개 퀴즈")
        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"{index}. {quiz.question}")
            for option_index, option in enumerate(quiz.options, start=1):
                print(f"   {option_index}) {option}")
            print(f"   정답: {quiz.answer}번")

    def show_scores(self) -> None:
        print(f"\n최근 점수: {self.last_score}점")
        print(f"최고 점수: {self.high_score}점")

    def run(self) -> None:
        actions = {
            "1": self.play,
            "2": self.add_quiz,
            "3": self.list_quizzes,
            "4": self.show_scores,
        }
        while True:
            print("\n=== AI & Python Quiz Challenge ===")
            print("1. 퀴즈 풀기")
            print("2. 퀴즈 추가")
            print("3. 퀴즈 목록")
            print("4. 점수 확인")
            print("5. 종료")
            choice = input("메뉴 번호 선택: ").strip()
            if choice == "5":
                self.save_state()
                print("저장 완료. 프로그램을 종료합니다.")
                break
            action = actions.get(choice)
            if action:
                action()
            else:
                print("1~5 사이의 메뉴 번호를 선택하세요.")


if __name__ == "__main__":
    game = QuizGame()
    try:
        game.run()
    except EOFError:
        game.save_state()
        print("\n입력이 종료되어 프로그램을 마칩니다.")
    except KeyboardInterrupt:
        game.save_state()
        print("\n사용자가 중단하여 프로그램을 종료합니다.")
