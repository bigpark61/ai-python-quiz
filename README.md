# AI & Python Quiz Challenge

## 프로젝트 개요

Python 콘솔에서 실행하는 **4지선다형 퀴즈 게임**입니다. 퀴즈 풀기·추가·목록 조회, 최근/최고 점수 확인, JSON 파일 저장 및 재실행 후 데이터 유지를 지원합니다.

- GitHub: https://github.com/bigpark61/ai-python-quiz
- 소스코드: `main.py` / 자동 테스트: `test_quiz.py` / 저장 데이터: `state.json`

## 퀴즈 주제 선정 이유

Python, API, Git, AI의 핵심 개념을 퀴즈로 복습하면서 객체지향 프로그래밍, 파일 입출력, 예외 처리 및 Git 협업을 연습하기 위해 선정했습니다. 저장소의 `state.json`에는 현재 **8개 문제**가 있으며, `main.py`의 기본 문제는 6개입니다.

## 개발 환경

| 항목 | 내용 |
|---|---|
| 운영체제/터미널 | Windows / PowerShell |
| Python | 3.10 이상 권장 (실습 환경: 3.15.2) |
| 데이터 저장 | JSON (`state.json`) |
| 테스트 | Python 내장 `unittest`, `tempfile`, `unittest.mock` |
| 형상관리 | Git / GitHub |

별도의 외부 Python 라이브러리를 설치할 필요는 없습니다.

## 실행 방법

처음 내려받는 경우:

```powershell
git clone https://github.com/bigpark61/ai-python-quiz.git
cd ai-python-quiz
python main.py
```

기존에 내려받은 경우 프로젝트 폴더에서 `python main.py`를 실행합니다. 명령이 인식되지 않으면 Python 설치 및 PATH 설정을 확인하세요.

## 메뉴 출력 예시

```text
=== AI & Python Quiz Challenge ===
1. 퀴즈 풀기
2. 퀴즈 추가
3. 퀴즈 목록
4. 점수 확인
5. 종료
메뉴 번호 선택:
```

## 기능 목록

| 메뉴 | 기능 | 구현 내용 |
|---|---|---|
| 1 | 퀴즈 풀기 | 전체 문제에서 최대 5개를 무작위 출제, 4지선다 정답 판정, 100점 만점 채점 |
| 2 | 퀴즈 추가 | 문제·보기 4개·정답 번호 입력 후 JSON 즉시 저장 |
| 3 | 퀴즈 목록 | 저장된 문제·선택지·정답 조회 |
| 4 | 점수 확인 | `last_score`(최근 점수) 및 `high_score`(최고 점수) 표시 |
| 5 | 종료 | 현재 상태 저장을 시도하고 결과 메시지 출력 후 종료 |

점수는 `맞힌 문제 수 ÷ 출제 문제 수 × 100`으로 계산하고 반올림하여 표시합니다.

## 클래스 구성

- **`Quiz`**: 문제, 선택지, 정답을 보관하는 데이터 클래스이며 `ask()`로 문제 출제 및 정답 판정을 수행합니다.
- **`QuizGame`**: `run()`(메뉴), `play()`(출제·채점), `add_quiz()`(문제 추가), `list_quizzes()`(조회), `show_scores()`(점수), `save_state()`/`load_state()`(JSON 저장·불러오기)를 담당합니다.

## 파일 구조

```text
ai-python-quiz/
├── main.py        # 퀴즈 게임 프로그램
├── test_quiz.py   # unittest 자동 테스트 4개
├── state.json     # 등록 퀴즈 8개 및 점수 데이터 (Git 추적)
├── README.md      # 프로젝트 설명 및 수행 증빙
└── .gitignore     # 캐시·로컬 백업·임시 파일 제외
```

## 데이터 파일 저장 및 동기화

`state.json`은 `quizzes`, `high_score`, `last_score`를 저장하며, 각 퀴즈는 `question`, `options`(4개), `answer`(1~4)를 포함합니다.

- **불러오기**: 프로그램 시작 시 `load_state()` 호출. 파일이 없다면 기본 퀴즈 6개와 점수 0으로 새로운 파일을 생성합니다.
- **저장 시점**: 퀴즈 추가 직후, 퀴즈 완료 직후, 메뉴 5번 종료 및 Ctrl+C/EOFError에 따른 종료 시 저장을 시도합니다.
- **안전 저장**: `save_state()`는 `state.json.tmp`에 먼저 쓰고 `state.json`으로 교체합니다. 성공 여부를 `True`/`False`로 반환하며, 파일 저장 실패 시 오류 메시지를 출력합니다. 이는 자동 백업을 생성하는 기능은 아닙니다.
- **데이터 검증**: JSON 최상위 구조, 퀴즈 목록의 자료형, 질문·선택지·정답의 유효성, 점수의 정수형·0~100 범위·최고/최근 점수 관계를 검사합니다.
- **손상 파일 처리**: 문법 또는 구조가 잘못된 경우 오류를 출력하고 기본 퀴즈로 시작합니다. 이 상태로 다음 저장이 실행되면 원래 파일이 덮어써질 수 있으므로 필요한 데이터는 사전에 별도 백업하세요.
- **인코딩**: UTF-8을 사용합니다. BOM 포함 UTF-8은 현재 읽기 코드에서 오류가 발생할 수 있으므로 BOM 없는 UTF-8을 권장합니다.

`state.json`은 Git 추적 대상입니다. 다른 버전을 Pull하면 데이터가 달라지거나 충돌할 수 있으니 로컬 기록이 중요하면 별도 복사본을 보관하세요.

### 데이터 영속성 실습 결과

| 검증 항목 | 확인 결과 |
|---|---|
| 저장된 퀴즈 | 8개 |
| 최고 점수 | 100점 |
| 최근 점수 | 100점 |
| 재실행 후 퀴즈·점수 | 유지 확인 |
| `state.json` 파일 부재 | 기본 데이터 파일 생성 확인 |
| 잘못된 JSON 문법·자료형 | 안내 출력 및 기본 퀴즈 시작 확인 |
| 최고 점수 150 | 0~100 범위 오류 감지 확인 |

## 입력 중단 및 예외 처리

- 메뉴의 잘못된 입력은 안내 메시지를 출력하고 다시 메뉴로 돌아갑니다. `strip()`으로 앞뒤 공백을 제거합니다.
- 퀴즈 답변과 정답 등록은 1~4 사이의 번호만 허용합니다.
- `Ctrl+C`는 `KeyboardInterrupt`로 처리하여 저장을 시도한 후 종료합니다.
- `EOFError` 발생 시 저장을 시도하고 종료합니다. Windows PowerShell에서 `Ctrl+Z` + Enter로 시험했습니다.
- 퀴즈 한 판이 끝나지 않은 답변 또는 등록을 완료하지 않은 퀴즈 내용은 저장되지 않습니다.

## 자동 테스트 결과

```powershell
python -m unittest test_quiz.py -v
```

| 테스트 함수 | 검증 내용 | 결과 |
|---|---|---|
| `test_save_and_load_state` | JSON 저장 및 새 게임 객체로 재로딩 | PASS |
| `test_invalid_json_syntax` | 잘못된 JSON 문법 처리 | PASS |
| `test_invalid_quizzes_structure` | `quizzes`의 잘못된 자료형 처리 | PASS |
| `test_add_quiz_persistence` | 문제 추가 후 새 게임 객체에서 유지 확인 | PASS |

**실습 결과: 4개 테스트 / 4개 PASS / 실패 0개 (2026-11-24).**

자동 테스트는 `TemporaryDirectory()`와 `patch.object(main, "STATE_FILE", ...)`를 사용하므로 실제 `state.json`을 수정하지 않습니다. 모든 가능한 오류 상황을 자동으로 검증한 것은 아닙니다.

## Git 실습 기록

| 항목 | 실행 내용 및 결과 |
|---|---|
| Clone | `git clone https://github.com/bigpark61/ai-python-quiz.git` 완료 |
| 기능 브랜치 | `feature/input-interruption-handling` 작업 이력 확인 |
| PR 병합 | PR #1, PR #2 병합 이력 확인 |
| Pull | `git pull --ff-only origin main` → `Already up to date.` |
| Push | `git push origin main` → `Everything up-to-date` |
| 동기화 | `git status -sb` → `## main...origin/main`, 원격 SHA `b2e2cc8` |
| Commit | README 최종 수정 이전 **11개** 확인 (10개 이상 요구 충족) |

### 주요 Commit

| SHA | 내용 |
|---|---|
| `d1bbfd0` | JSON 유효성 검사 및 안전 저장 개선 |
| `827abca` | 딕셔너리 퀴즈 및 점수 기록 변경 |
| `d667199` | JSON 저장·재로딩 자동 테스트 |
| `bad7f50` | 잘못된 JSON 문법·구조 자동 테스트 |
| `ab1e154` | 퀴즈 추가 및 영속성 자동 테스트 |
| `b2e2cc8` | README 및 수행 증빙 업데이트 |

커밋 개수와 이력은 아래 명령으로 재확인할 수 있습니다.

```powershell
git rev-list --count HEAD
git log --oneline --graph --all
git status -sb
```

## 과제 요구사항 검증 요약

| 요구사항 | 구현·증빙 위치 | 결과 |
|---|---|---|
| 퀴즈 5개 이상 | `state.json` (8개) | 완료 |
| 메뉴 5개 | `QuizGame.run()` 및 관련 메서드 | 완료 |
| 클래스 2개 이상 | `Quiz`, `QuizGame` | 완료 |
| JSON 저장·불러오기 | `save_state()`, `load_state()` | 완료 |
| 종료 후 데이터 유지 | 수동 테스트 및 `test_quiz.py` | 완료 |
| 입력 중단·데이터 오류 대응 | `main.py`, 수동 검증 및 일부 자동 테스트 | 주요 항목 확인 |
| Git Commit 10개 이상 | 11개 확인 (본 수정 이전) | 충족 |
| 기능 브랜치 및 병합 | PR #1, PR #2 | 확인 |
| Clone, Pull, Push | PowerShell 실행 결과 | 확인 |
| 실행 스크린샷 별도 제출 | 저장소 내 해당 증빙 경로는 확인되지 않음 | 필요 시 보완 |

> 이 문서는 저장소의 실제 소스코드·데이터와 대화 중 제공된 실행 결과를 기준으로 작성했습니다. 별도의 제출용 스크린샷 및 과제 PDF 원문 평가표 전체와의 최종 대조는 별도 확인이 필요합니다.
