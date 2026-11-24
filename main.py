
import json
import random
from dataclasses import asdict, dataclass
from pathlib import Path


# JSON 데이터 저장 경로
STATE_FILE = Path(__file__).resolve().parent / "state.json"


# ==========================================
# 1. Quiz 클래스
# ==========================================

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

                print(
                    "정답입니다!"
                    if correct
                    else f"오답입니다. 정답: {self.answer}번"
                )

                return correct

            print("1~4 사이의 번호를 입력하세요.")


# ==========================================
# 2. 기본 퀴즈 데이터
# ==========================================

DEFAULT_QUIZZES = [
    Quiz(
        "Python에서 리스트를 만드는 기호는?",
        ["{}", "[]", "()", "< >"],
        2,
    ),
    Quiz(
        "Python에서 함수를 정의하는 키워드는?",
        ["func", "function", "def", "make"],
        3,
    ),
    Quiz(
        "JSON 데이터를 Python 객체로 읽는 함수는?",
        [
            "json.loads()",
            "json.save()",
            "json.print()",
            "json.push()",
        ],
        1,
    ),
    Quiz(
        "HTTP API에서 데이터를 조회할 때 주로 사용하는 메서드는?",
        ["POST", "DELETE", "PATCH", "GET"],
        4,
    ),
    Quiz(
        "Git에서 변경 내용을 기록하는 명령어는?",
        ["git commit", "git open", "git start", "git show-all"],
        1,
    ),
    Quiz(
        "AI에서 LLM은 무엇의 약자인가?",
        [
            "Local Logic Machine",
            "Large Language Model",
            "Long Learning Method",
            "Linked List Model",
        ],
        2,
    ),
]


# ==========================================
# 3. QuizGame 클래스
# ==========================================

class QuizGame:

    def __init__(self) -> None:
        self.quizzes = list(DEFAULT_QUIZZES)
        self.high_score = 0
        self.last_score = 0

        self.load_state()

    # ======================================
    # 3-1. JSON 파일 불러오기
    # ======================================

    def load_state(self) -> None:

        # JSON 파일이 없으면 기본 데이터 생성
        if not STATE_FILE.exists():
            self.save_state()
            return

        try:
            with STATE_FILE.open(
                "r", encoding="utf-8"
            ) as file:
                data = json.load(file)

            # ① JSON 최상위 자료형 검사
            if not isinstance(data, dict):
                raise ValueError(
                    "JSON 최상위 데이터는 dict여야 합니다."
                )

            # ② quizzes 키 존재 여부 검사
            if "quizzes" not in data:
                raise ValueError(
                    "quizzes 데이터가 없습니다."
                )

            # ③ quizzes 자료형 검사
            if not isinstance(data["quizzes"], list):
                raise ValueError(
                    "quizzes 데이터는 list여야 합니다."
                )

            # ④ 개별 퀴즈 데이터 검사
            for item in data["quizzes"]:

                if not isinstance(item, dict):
                    raise ValueError(
                        "각 퀴즈는 dict 형식이어야 합니다."
                    )

                question = item.get("question")
                options = item.get("options")
                answer = item.get("answer")

                # 문제 내용 검사
                if (
                    not isinstance(question, str)
                    or not question.strip()
                ):
                    raise ValueError(
                        "문제는 비어 있지 않은 문자열이어야 합니다."
                    )

                # 선택지 개수 검사
                if (
                    not isinstance(options, list)
                    or len(options) != 4
                ):
                    raise ValueError(
                        "선택지는 4개의 리스트 항목이어야 합니다."
                    )

                # 선택지 내용 검사
                if not all(
                    isinstance(option, str)
                    and option.strip()
                    for option in options
                ):
                    raise ValueError(
                        "모든 선택지는 비어 있지 않은 문자열이어야 합니다."
                    )

                # 정답 번호 검사
                if (
                    type(answer) is not int
                    or not 1 <= answer <= 4
                ):
                    raise ValueError(
                        "정답은 1~4 사이의 정수여야 합니다."
                    )

            # ⑤ 검증된 데이터를 Quiz 객체로 변환
            quizzes = [
                Quiz(**item)
                for item in data["quizzes"]
            ]

            # ⑥ 점수 데이터 불러오기
            # 점수 데이터 불러오기
            high_score = data.get("high_score", 0)
            last_score = data.get("last_score", 0)

            # 점수 자료형 검증
            if type(high_score) is not int:
                raise ValueError("최고 점수는 정수여야 합니다.")

            if type(last_score) is not int:
                raise ValueError("최근 점수는 정수여야 합니다.")

            # 점수 범위 검증
            if not 0 <= high_score <= 100:
                raise ValueError("최고 점수는 0~100 사이여야 합니다.")

            if not 0 <= last_score <= 100:
                raise ValueError("최근 점수는 0~100 사이여야 합니다.")

            # 점수 일관성 검증
            if last_score > high_score:
                raise ValueError(
                    "최근 점수는 최고 점수보다 클 수 없습니다."
                )

            # ⑦ 정상 데이터 적용
            self.quizzes = quizzes
            self.high_score = high_score
            self.last_score = last_score

        except (
            OSError,
            ValueError,
            TypeError,
            KeyError,
            json.JSONDecodeError,
        ) as error:

            print(
                f"저장 파일을 읽지 못했습니다: {error}"
            )
            print(
                "기본 문제로 시작합니다. "
                "기존 파일은 다음 저장 시 "
                "덮어써질 수 있습니다."
            )

    # ======================================
    # 3-2. JSON 파일 저장하기
    # ======================================

    def save_state(self) -> bool:
        data = {
        "quizzes": [asdict(quiz) for quiz in self.quizzes],
        "high_score": self.high_score,
        "last_score": self.last_score,
    }

        temp_file = STATE_FILE.with_suffix(".json.tmp")

        try:
            with temp_file.open("w", encoding="utf-8") as file:
                json.dump(
                    data,
                    file,
                    ensure_ascii=False,
                    indent=2,
                )

            temp_file.replace(STATE_FILE)
            return True

        except (OSError, TypeError, ValueError) as error:
            print(f"JSON 저장 실패: {error}")

            try:
                temp_file.unlink(missing_ok=True)
            except OSError:
                pass

            return False

    # ======================================
    # 3-3. 퀴즈 풀기
    # ======================================

    def play(self) -> None:

        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        questions = random.sample(
            self.quizzes,
            k=min(5, len(self.quizzes)),
        )

        correct_count = 0

        for index, quiz in enumerate(
            questions, start=1
        ):
            print(
                f"\n[문제 {index}/{len(questions)}]"
            )

            correct_count += int(quiz.ask())

        score = round(
            correct_count / len(questions) * 100
        )

        self.last_score = score
        self.high_score = max(
            self.high_score, score
        )

        if self.save_state():
            print("퀴즈 점수가 JSON 파일에 저장되었습니다.")
        else:
            print("주의: 퀴즈 점수를 파일에 저장하지 못했습니다.")

        print(
            f"\n게임 종료! "
            f"{correct_count}/{len(questions)}문제 정답, "
            f"점수: {score}점"
        )

        print(
            f"최고 점수: {self.high_score}점"
        )

    # ======================================
    # 3-4. 퀴즈 추가
    # ======================================

    def add_quiz(self) -> None:

        question = input(
            "문제 내용을 입력하세요: "
        ).strip()

        if not question:
            print("문제를 비워 둘 수 없습니다.")
            return

        options = []

        for index in range(1, 5):
            option = input(
                f"보기 {index}: "
            ).strip()

            if not option:
                print(
                    "보기를 비워 둘 수 없습니다. "
                    "등록을 취소합니다."
                )
                return

            options.append(option)

        while True:
            answer = input(
                "정답 번호 (1~4): "
            ).strip()

            if answer in {"1", "2", "3", "4"}:
                break

            print(
                "1~4 사이의 번호를 입력하세요."
            )

        self.quizzes.append(
            Quiz(
                question,
                options,
                int(answer),
            )
        )

        # 퀴즈 추가 즉시 JSON에 저장
        if self.save_state():
            print("퀴즈가 등록되고 저장되었습니다.")
        else:
            print("퀴즈는 메모리에 추가되었지만 파일 저장에 실패했습니다.")

    # ======================================
    # 3-5. 퀴즈 목록
    # ======================================

    def list_quizzes(self) -> None:

        print(
            f"\n총 {len(self.quizzes)}개 퀴즈"
        )

        for index, quiz in enumerate(
            self.quizzes, start=1
        ):

            print(
                f"{index}. {quiz.question}"
            )

            for option_index, option in enumerate(
                quiz.options, start=1
            ):
                print(
                    f"   {option_index}) {option}"
                )

            print(
                f"   정답: {quiz.answer}번"
            )

    # ======================================
    # 3-6. 점수 확인
    # ======================================

    def show_scores(self) -> None:

        print(
            f"\n최근 점수: {self.last_score}점"
        )

        print(
            f"최고 점수: {self.high_score}점"
        )

    # ======================================
    # 3-7. 메인 메뉴
    # ======================================

    def run(self) -> None:

        actions = {
            "1": self.play,
            "2": self.add_quiz,
            "3": self.list_quizzes,
            "4": self.show_scores,
        }

        while True:

            print(
                "\n=== AI & Python Quiz Challenge ==="
            )
            print("1. 퀴즈 풀기")
            print("2. 퀴즈 추가")
            print("3. 퀴즈 목록")
            print("4. 점수 확인")
            print("5. 종료")

            choice = input(
                "메뉴 번호 선택: "
            ).strip()

            if choice == "5":
                if self.save_state():
                    print("저장 완료. 프로그램을 종료합니다.")
                else:
                    print("저장에 실패했습니다. 프로그램을 종료합니다.")
                break

            action = actions.get(choice)

            if action:
                action()
            else:
                print(
                    "1~5 사이의 메뉴 번호를 선택하세요."
                )


# ==========================================
# 4. 프로그램 실행 진입점
# ==========================================

if __name__ == "__main__":

    game = QuizGame()

    try:
        game.run()

    except EOFError:
        if game.save_state():
             print("\n입력이 종료되어 데이터를 저장하고 종료합니다.")
        else:
             print("\n입력이 종료되었지만 데이터 저장에 실패했습니다.")

    except KeyboardInterrupt:
        if game.save_state():
            print("\n사용자가 중단하여 데이터를 저장하고 종료합니다.")
        else:
            print("\n사용자가 중단했지만 데이터 저장에 실패했습니다.")