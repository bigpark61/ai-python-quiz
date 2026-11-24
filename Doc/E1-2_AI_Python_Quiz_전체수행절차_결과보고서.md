# AI & Python Quiz Challenge — E1-2 과제 전체 수행 기록 및 실행 증빙

> **수행 일자:** 2026-11-23 ~ 2026-11-24  
> **환경:** Windows / PowerShell / Python 3.15.2 / Git / GitHub  
> **저장소:** https://github.com/bigpark61/ai-python-quiz  
> **문서 구성:** 과제 수행 배경 → 준비 → 실행 → 오류 → 수정 → 검증 → Git 제출 → 최종 확인 → 증빙 이미지 목록  
> **기준:** 현재 대화에 남은 실행 결과, 첨부 스크린샷, GitHub에 반영된 코드/README 확인 내용

**문서 읽기 안내:** 이 문서는 대화를 원문 그대로 출력한 전사본이 아니라, 수행 중 안내·질문·응답·오류·검증 사항을 **실제 작업 순서대로 재구성한 통합 수행 보고서**입니다. 일부 중간 메시지는 현재 열람 가능한 기록에 없어 요약형으로 기술했습니다. 실행하지 않은 명령을 수행했다고 쓰지 않았고, 증빙에서 확인할 수 없는 결과는 별도로 표시했습니다. `images/`의 캡처 파일은 제공된 원본 이미지를 그대로 복사했습니다.

## 1. 최종 결과 요약

| 구분 | 최종 확인 내용 | 근거 |
|---|---|---|
| 프로그램 | 콘솔 4지선다 퀴즈, 메뉴 5개 | `main.py`, 실행 화면 |
| 주요 클래스 | `Quiz`, `QuizGame` | `main.py` |
| 퀴즈 데이터 | 8문제 | `state.json` 및 PowerShell 확인 |
| 최근/최고 점수 | 100점 / 100점 | `state.json` 확인 |
| 데이터 영속성 | 저장·재실행 후 불러오기 정상 | 수동 시험 + `unittest` |
| 오류 처리 | Ctrl+C, EOFError, JSON 문법·구조 오류, 점수 검증 | 실행 화면 |
| 자동 테스트 | **4개 수행, 4개 PASS** | `python -m unittest test_quiz.py -v` |
| Git 이력 | **11개 Commit** (최종 README 파일의 별도 추가 Commit 전) | `git rev-list --count HEAD` |
| 브랜치 협업 | PR #1 / PR #2 병합 이력 | `git log --graph --all` |
| Git Clone/Pull/Push | 실습 및 동기화 확인 | PowerShell 기록 |
| GitHub 최종 동기화 | 원격 SHA `b2e2cc8`, `main...origin/main` | 2026-11-24 화면 |
| 별도 최종 README 업데이트 | ChatGPT가 파일 작성·제공, GitHub 직접 쓰기는 403 권한 오류 | 이후 대화 기록; 원격 반영 확인 전 |

## 2. 진행 흐름 한눈에 보기

1. 저장소 Clone 및 Python 설치/경로 문제 해결
2. `state.json` 백업 후 프로그램 실행 및 메뉴·퀴즈 풀이 검증
3. 퀴즈 추가/목록/점수/파일 저장 및 재시작 검증
4. 잘못된 메뉴 입력, Ctrl+C, EOFError 종료 검증
5. `state.json` 부재·손상·구조 오류 테스트 후 데이터 복원
6. JSON 항목별 유효성 및 점수 범위 검증 코드 보완
7. 임시 파일 기반 안전한 JSON 저장 기능 보완, 메서드 들여쓰기 오류 해결
8. Git 제외 규칙과 버전 이력/데이터 변경 Commit 정리
9. `unittest` 4개 작성·실행·Commit, Git 총 10개 달성
10. README 업데이트 후 Commit 11개, Pull/Push/원격 동기화 검증
11. 최신 README의 과거 상태 문구 정리 필요 사항 확인 및 별도 README 최종본 제작

---


## 3. STEP 01 — 저장소 복제 및 개발 환경 확인

**요청/지시:** GitHub 저장소에서 코드를 Clone하고 PowerShell에서 실행 준비를 진행했다. 기존 폴더가 없는 상태에서 Clone하여 `main.py`, `README.md`, `.gitignore`, `state.json` 파일과 원격 주소를 확인했다. Git 작업 상태는 `main` 및 `working tree clean`이었다.

```powershell
cd C:\Temp
Test-Path .\ai-python-quiz
git clone https://github.com/bigpark61/ai-python-quiz.git
cd ai-python-quiz
Get-ChildItem
git remote -v
git status
```


### Python 실행 문제 및 해결

처음에는 `python --version`이 실제 버전을 출력하지 않고 `Python`만 표시되거나, `py --version`이 `CommandNotFoundException`을 발생시켰다. `where.exe python`으로 조회한 경로는 WindowsApps의 실행 별칭이었다. 이후 Python 3.15.2 설치/설정이 정상화되어 퀴즈를 실행할 수 있었다. `Python 3.13.x`를 명령처럼 입력하는 착오도 있었으며, 버전은 `python --version`으로 확인해야 한다.

![Python 명령에 버전이 표시되지 않음](images/image(20261123-134726).png)

> **증빙:** Python 명령에 버전이 표시되지 않음 (`images/image(20261123-134726).png`)


![py 명령 실행 실패](images/image(20261123-134834).png)

> **증빙:** py 명령 실행 실패 (`images/image(20261123-134834).png`)


![WindowsApps Python 별칭 경로 확인](images/image(20261123-135002).png)

> **증빙:** WindowsApps Python 별칭 경로 확인 (`images/image(20261123-135002).png`)


![Python 설치 후 3.15.2 확인](images/image(20261123-135428).png)

> **증빙:** Python 설치 후 3.15.2 확인 (`images/image(20261123-135428).png`)


## 4. STEP 02 — 데이터 백업과 최초 실행

**지시:** 기존 문제와 점수 기록의 손실을 방지하기 위해 `state.json`을 복사해 백업하고, `python main.py`를 실행한다. 초기 저장소에는 기본 메뉴가 구현되어 있었다.

```powershell
Copy-Item state.json state.backup.json
Get-ChildItem state*.json
python main.py
```


![state.json 백업 파일 생성](images/image(20261123-135635).png)

> **증빙:** state.json 백업 파일 생성 (`images/image(20261123-135635).png`)


![퀴즈 게임 메인 메뉴 출력](images/image(20261123-135804).png)

> **증빙:** 퀴즈 게임 메인 메뉴 출력 (`images/image(20261123-135804).png`)

**확인:** 1. 퀴즈 풀기 / 2. 퀴즈 추가 / 3. 퀴즈 목록 / 4. 점수 확인 / 5. 종료 메뉴가 표시되었다.

## 5. STEP 03 — 퀴즈 풀기·점수·추가·저장 검증

**실행:** 메뉴 1에서 최대 5개의 무작위 문제를 풀고 정답·오답 및 100점 만점 점수를 확인했다. 메뉴 3은 전체 문제를 보여주며, 메뉴 4는 최근/최고 점수를 출력한다. 메뉴 5는 종료하며 JSON을 저장한다.

![퀴즈 문제와 정답 목록 확인](images/image(20261123-135919).png)

> **증빙:** 퀴즈 문제와 정답 목록 확인 (`images/image(20261123-135919).png`)


![퀴즈 문제 풀이 과정](images/image(20261123-140133).png)

> **증빙:** 퀴즈 문제 풀이 과정 (`images/image(20261123-140133).png`)


![퀴즈 풀이 후 점수 계산 및 메뉴 복귀](images/image(20261123-140522).png)

> **증빙:** 퀴즈 풀이 후 점수 계산 및 메뉴 복귀 (`images/image(20261123-140522).png`)


![퀴즈 점수 확인 및 종료 처리](images/image(20261123-141207).png)

> **증빙:** 퀴즈 점수 확인 및 종료 처리 (`images/image(20261123-141207).png`)

**수행 결과:** 5문제를 모두 맞혀 100점이 출력되었으며, 종료 후 JSON의 `high_score`와 `last_score`에 100이 기록된 화면을 확인했다. 이후 추가 문제 등록과 파일 반영을 확인했다.

![추가 문제 및 저장 확인](images/image(20261123-141418).png)

> **증빙:** 추가 문제 및 저장 확인 (`images/image(20261123-141418).png`)


![입력과 퀴즈 데이터 관리 화면](images/image(20261123-141553).png)

> **증빙:** 입력과 퀴즈 데이터 관리 화면 (`images/image(20261123-141553).png`)


![퀴즈 추가 및 저장 결과 확인](images/image(20261123-141752).png)

> **증빙:** 퀴즈 추가 및 저장 결과 확인 (`images/image(20261123-141752).png`)


![추가된 퀴즈 조회 및 저장된 데이터 수 확인](images/image(20261123-143723).png)

> **증빙:** 추가된 퀴즈 조회 및 저장된 데이터 수 확인 (`images/image(20261123-143723).png`)


### 추가된 8번째 문제

```json
{
  "question": "Python에서 딕셔너리 자료형을 만드는 기호는?",
  "options": ["[]", "{}", "()", "<>"],
  "answer": 2
}
```
문제 수는 최종 8개로 확인되었으며, `state.json`을 Git에서 비교한 결과 새 문제와 최근 점수 변경 외에 불필요한 변경은 발견되지 않았다.

## 6. STEP 04 — 잘못된 메뉴 입력 및 사용자 중단 처리

**검증 의도:** 빈 입력이나 범위 밖 메뉴 번호(0, 7)에서 안내문을 출력하고 다시 메뉴를 보여주는지 확인했다. Ctrl+C를 누르면 `KeyboardInterrupt`를 처리해 저장 후 종료하는지, Windows에서 Ctrl+Z 후 Enter로 EOFError를 발생시키면 정상 종료하는지 시험했다.

![잘못된 메뉴 번호 처리 후 반복 표시](images/image(20261123-143947).png)

> **증빙:** 잘못된 메뉴 번호 처리 후 반복 표시 (`images/image(20261123-143947).png`)


![Ctrl+C 또는 EOF 종료와 저장 상태 확인](images/image(20261123-144811).png)

> **증빙:** Ctrl+C 또는 EOF 종료와 저장 상태 확인 (`images/image(20261123-144811).png`)

**검증 결과:** `Traceback` 없이 PowerShell로 돌아오고, 기존 최고/최근 100점은 유지되었다. 오류 메시지 또는 종료 안내는 실제 캡처에 표시된 그대로 정상적으로 나타났다.

## 7. STEP 05 — JSON 파일이 없을 때 자동 생성

기존 8개 문제를 지키기 위해 `state.json`을 `state.saved.json`으로 이름 변경한 후 퀴즈 프로그램을 실행했다. 파일이 없으면 기본 6문제로 시작하는지를 확인했다. 종료 후 새 `state.json`이 생성되었으며, 다시 백업 파일로 복원했다.

```powershell
Rename-Item state.json state.saved.json
python main.py
# 메뉴 3에서 기본 문제 목록 확인, 메뉴 5로 종료
(Get-Content state.json -Raw -Encoding UTF8 | ConvertFrom-Json).quizzes.Count
(Get-Content state.saved.json -Raw -Encoding UTF8 | ConvertFrom-Json).quizzes.Count
Copy-Item state.saved.json state.json -Force
```


![JSON 파일 없는 상태에서 기본 퀴즈 표시](images/image(20261124-123527).png)

> **증빙:** JSON 파일 없는 상태에서 기본 퀴즈 표시 (`images/image(20261124-123527).png`)


![기본 6문제와 백업 8문제 확인](images/image(20261124-123909).png)

> **증빙:** 기본 6문제와 백업 8문제 확인 (`images/image(20261124-123909).png`)


![백업으로 8문제·최고/최근 100점 복원](images/image(20261124-124127).png)

> **증빙:** 백업으로 8문제·최고/최근 100점 복원 (`images/image(20261124-124127).png`)

**결과:** 파일 자동 생성 6문제, 원본 8문제·100/100점 복원 성공. 새 파일을 보존할 필요가 없을 때만 원본을 되돌렸다.

## 8. STEP 06 — JSON 문법 오류·구조 오류 테스트

**문법 오류:** `state.json`을 일시적으로 `{invalid json`으로 변경해 프로그램이 기본 문제로 시작하는지 확인했다. **구조 오류:** 문법상 유효하지만 `"quizzes": "잘못된 데이터"`로 기록된 파일을 통해 리스트 자료형 검증을 시험했다. 매 실험 전에 백업을 만들고 종료 후 원본을 복원했다.

### 주요 오류와 해결: 들여쓰기와 BOM

`load_state()`에 검증 코드를 넣을 때 `for item in data["quizzes"]:`의 들여쓰기 오류로 `SyntaxError: expected except or finally block`이 발생했다. 해당 반복문을 `try:` 블록 내부 12칸 들여쓰기로 수정했다.

![load_state 검증 코드 들여쓰기 SyntaxError](images/image(20261123-145802).png)

> **증빙:** load_state 검증 코드 들여쓰기 SyntaxError (`images/image(20261123-145802).png`)

PowerShell의 `Set-Content -Encoding utf8`에 의해 JSON 앞에 UTF-8 BOM이 포함된 경우 `Unexpected UTF-8 BOM` 오류가 발생하여, 구조 검증 전에 파싱이 중단되었다. `System.Text.UTF8Encoding($false)`로 BOM 없이 테스트용 JSON을 작성하여 해결했다.

```powershell
$json = @'
{
  "quizzes": "잘못된 데이터",
  "high_score": 100,
  "last_score": 100
}
'@
[System.IO.File]::WriteAllText(
    (Join-Path (Get-Location) "state.json"),
    $json,
    (New-Object System.Text.UTF8Encoding($false))
)
python main.py
```


![최고 점수 범위 검증 예제의 오류 안내](images/image(20261124-132417).png)

> **증빙:** 최고 점수 범위 검증 예제의 오류 안내 (`images/image(20261124-132417).png`)

**검증 결과:** 문법 오류 또는 `quizzes` 구조 오류 시 오류 안내가 출력되고 기본 문제로 진행했다. 각 검증 이후 기존 파일 8문제·100/100점이 복구되었음을 PowerShell에서 재확인했다.

## 9. STEP 07 — load_state 개별 필드 및 점수 검증 보완

**수정 지시:** `main.py`의 `load_state()`에서 JSON 전체가 dict인지, `quizzes`가 list인지, 문제 항목이 dict인지, 질문이 빈 문자열이 아닌지, 선택지 4개가 각각 문자열인지, 정답이 1~4의 정수인지 검사하도록 했다. 점수에는 정수형·0~100 범위·`last_score <= high_score` 일관성 검사를 추가했다.
```python
if not isinstance(data, dict):
    raise ValueError("JSON 최상위 데이터는 dict여야 합니다.")
if not isinstance(data.get("quizzes"), list):
    raise ValueError("quizzes 데이터는 list여야 합니다.")
# 개별 퀴즈 검증 후
if type(high_score) is not int or not 0 <= high_score <= 100:
    raise ValueError("최고 점수는 0~100 사이여야 합니다.")
if last_score > high_score:
    raise ValueError("최근 점수는 최고 점수보다 클 수 없습니다.")
```
기존 데이터 전체를 덮어쓰기 전에 별도 백업 파일을 확인하고, `python -m py_compile main.py`로 문법 오류를 확인했다. 구조 오류 시험은 `quizzes`를 문자열로 만들고 에러 안내가 나오는지 확인했다. 점수 시험에서는 최고 점수 150을 넣어 제한 범위 메시지가 출력되었다.

![수정 main.py 문법 검사와 정상 실행](images/image(20261124-125208).png)

> **증빙:** 수정 main.py 문법 검사와 정상 실행 (`images/image(20261124-125208).png`)


![최고 점수 150에 대한 0~100 범위 오류 감지](images/image(20261124-132417).png)

> **증빙:** 최고 점수 150에 대한 0~100 범위 오류 감지 (`images/image(20261124-132417).png`)


![구조 오류 시험 후 기본 문제 확인 화면](images/image(20261124-123909).png)

> **증빙:** 구조 오류 시험 후 기본 문제 확인 화면 (`images/image(20261124-123909).png`)


## 10. STEP 08 — JSON 저장 안정성 및 메서드 위치 오류 해결

**수정:** `save_state()`가 직접 원본에 쓰지 않고 `state.json.tmp`에 먼저 기록 후 `replace()`로 교체하고 성공 시 True, 실패 시 False를 반환하도록 변경했다. `play()`, `add_quiz()`, 종료 메뉴, Ctrl+C/EOFError에서 저장 결과에 따라 메시지를 분기하도록 보완했다.
```python
def save_state(self) -> bool:
    data = {"quizzes": [asdict(q) for q in self.quizzes],
            "high_score": self.high_score,
            "last_score": self.last_score}
    temp_file = STATE_FILE.with_suffix(".json.tmp")
    try:
        with temp_file.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        temp_file.replace(STATE_FILE)
        return True
    except (OSError, TypeError, ValueError) as error:
        print(f"JSON 저장 실패: {error}")
        try:
            temp_file.unlink(missing_ok=True)
        except OSError:
            pass
        return False
```
**실제 오류:** 수정 직후 `AttributeError: QuizGame object has no attribute save_state`가 발생했다. `save_state()` 메서드의 배치/들여쓰기를 재검토했고, 이어서 `hasattr(QuizGame, "save_state")` 결과 True를 확인했다.

![save_state 속성 오류 Traceback](images/image(20261124-125816).png)

> **증빙:** save_state 속성 오류 Traceback (`images/image(20261124-125816).png`)


![save_state 메서드 정의 확인: hasattr=True](images/image(20261124-130557).png)

> **증빙:** save_state 메서드 정의 확인: hasattr=True (`images/image(20261124-130557).png`)


![저장/종료 성공, 퀴즈 8개·점수 100·임시파일 없음](images/image(20261124-130757).png)

> **증빙:** 저장/종료 성공, 퀴즈 8개·점수 100·임시파일 없음 (`images/image(20261124-130757).png`)

**확인:** 종료 시 저장 완료 안내, `state.json`의 문제 8개·점수 100/100, `Test-Path state.json.tmp` → False.

## 11. STEP 09 — Git 백업 파일 제외 및 Commit 준비

과제 중 만든 로컬 백업은 GitHub 제출 대상이 아니므로 `.gitignore`를 수정했다. Windows에서 복사한 파일에 추가된 `:Zone.Identifier` 스트림 문제와 백업 파일 목록 노출도 처리했다. `.gitignore`의 LF/CRLF 안내는 파일 줄바꿈 변환에 관한 경고로 판단했다.

```powershell
git status --short
# .gitignore에 다음 패턴을 추가
# state.*backup*.json
# state.saved.json
# state.before-corrupt-test.json
# main.backup.py
# *.json.tmp
# README.backup.md
git add main.py .gitignore
git diff --cached --stat
```


![main.py 및 백업 파일의 Git 상태](images/image(20261124-133102).png)

> **증빙:** main.py 및 백업 파일의 Git 상태 (`images/image(20261124-133102).png`)


![git add 중 LF/CRLF 경고](images/image(20261124-133213).png)

> **증빙:** git add 중 LF/CRLF 경고 (`images/image(20261124-133213).png`)


![main.py/.gitignore 스테이징 및 state.json 분리](images/image(20261124-133330).png)

> **증빙:** main.py/.gitignore 스테이징 및 state.json 분리 (`images/image(20261124-133330).png`)


![이미 Commit된 변경사항과 중복 Commit 안내](images/image(20261124-133518).png)

> **증빙:** 이미 Commit된 변경사항과 중복 Commit 안내 (`images/image(20261124-133518).png`)


## 12. STEP 10 — Commit 이력과 state.json 변경 추적

`git log`와 `git rev-list --count HEAD`로 Commit 수와 PR 병합 이력을 확인했다. 초기에는 HEAD에 도달 가능한 Commit 6개였으며, 이후 JSON 데이터 변경과 자동 테스트 및 문서 작업을 각각 의미 있는 Commit으로 추가했다.

![기존 Git 이력 6개 및 PR 병합 그래프](images/image(20261124-133721).png)

> **증빙:** 기존 Git 이력 6개 및 PR 병합 그래프 (`images/image(20261124-133721).png`)


![state.json diff: 딕셔너리 8번째 문제와 최근 점수 변경](images/image(20261124-133855).png)

> **증빙:** state.json diff: 딕셔너리 8번째 문제와 최근 점수 변경 (`images/image(20261124-133855).png`)


![데이터 Commit 관련 로컬 상태](images/image(20261124-134226).png)

> **증빙:** 데이터 Commit 관련 로컬 상태 (`images/image(20261124-134226).png`)


![총 7개 Commit, 원격보다 앞선 2개 확인](images/image(20261124-134327).png)

> **증빙:** 총 7개 Commit, 원격보다 앞선 2개 확인 (`images/image(20261124-134327).png`)

대표 Commit: `d1bbfd0` JSON 유효성·안전 저장, `827abca` 새 퀴즈·점수 이력.

## 13. STEP 11 — unittest 자동 테스트 4개 작성

**설계:** 원본 `state.json`을 변형하지 않기 위해 임시 디렉터리의 `state.json` 경로로 `main.STATE_FILE`을 모의 변경했다. `test_quiz.py`는 아래 4개 테스트를 실행한다.
| 번호 | 테스트 | 목적 |
|---|---|---|
| TC-01 | `test_save_and_load_state` | 저장 뒤 새 객체에서 문제 수·점수 동일 확인 |
| TC-02 | `test_invalid_json_syntax` | JSON 문법 오류에서 기본 문제로 복구 |
| TC-03 | `test_invalid_quizzes_structure` | `quizzes`가 문자열이면 기본 문제로 복구 |
| TC-04 | `test_add_quiz_persistence` | 입력을 모의로 넣어 퀴즈 추가 후 새 객체에서 영속성 확인 |


```powershell
python -m unittest test_quiz.py -v
```


![첫 unittest: 저장·불러오기 1/1 PASS](images/image(20261124-134543).png)

> **증빙:** 첫 unittest: 저장·불러오기 1/1 PASS (`images/image(20261124-134543).png`)


![문법/구조 오류 자동 테스트 포함 3/3 PASS](images/image(20261124-135046).png)

> **증빙:** 문법/구조 오류 자동 테스트 포함 3/3 PASS (`images/image(20261124-135046).png`)


![추가 테스트 Commit 직전 스테이징 누락](images/image(20261124-135203).png)

> **증빙:** 추가 테스트 Commit 직전 스테이징 누락 (`images/image(20261124-135203).png`)


![3개 테스트 Commit 생성, 총 9개](images/image(20261124-135338).png)

> **증빙:** 3개 테스트 Commit 생성, 총 9개 (`images/image(20261124-135338).png`)


![퀴즈 영속성 테스트 포함 4/4 PASS](images/image(20261124-135604).png)

> **증빙:** 퀴즈 영속성 테스트 포함 4/4 PASS (`images/image(20261124-135604).png`)


![자동 테스트 4/4 재실행 PASS](images/image(20261124-135800).png)

> **증빙:** 자동 테스트 4/4 재실행 PASS (`images/image(20261124-135800).png`)


![10번째 Commit ab1e154 생성](images/image(20261124-135939).png)

> **증빙:** 10번째 Commit ab1e154 생성 (`images/image(20261124-135939).png`)

**최종 시험 화면:** `Ran 4 tests in 0.014s`, `OK`. 테스트 중 오류 안내가 출력되는 것은 의도적인 잘못된 JSON의 예외 처리 확인이며 테스트 실패가 아니다.

## 14. STEP 12 — README 보완, Git Commit 11개, Push 준비

기존 README의 목차(프로젝트 개요, 실행 방법, 메뉴 예시, 기능 목록, 예외 처리, 파일 구조, JSON 동기화, 클래스, Git 실습)를 확인하고 문서를 백업했다. 신규 수행 결과를 README에 반영했고 `.gitignore`에서 `README.backup.md`를 제외했다.

![README 목차 확인 및 README.backup.md 생성](images/image(20261124-140105).png)

> **증빙:** README 목차 확인 및 README.backup.md 생성 (`images/image(20261124-140105).png`)


![Git 브랜치 확인, README 백업 제외, ahead 상태](images/image(20261124-140401).png)

> **증빙:** Git 브랜치 확인, README 백업 제외, ahead 상태 (`images/image(20261124-140401).png`)


![Commit 이력과 PR #1/#2 병합 그래프](images/image(20261124-140558).png)

> **증빙:** Commit 이력과 PR #1/#2 병합 그래프 (`images/image(20261124-140558).png`)

`git pull --ff-only origin main` 결과 `Already up to date.`를 확인했다. README에 98줄이 추가되었고 `.gitignore`가 수정되어, 두 파일을 Commit했다.

![Git Pull 성공 및 README/.gitignore diff](images/image(20261124-141402).png)

> **증빙:** Git Pull 성공 및 README/.gitignore diff (`images/image(20261124-141402).png`)


![README Commit b2e2cc8, 총 11개, ahead 6](images/image(20261124-141603).png)

> **증빙:** README Commit b2e2cc8, 총 11개, ahead 6 (`images/image(20261124-141603).png`)


## 15. STEP 13 — GitHub 동기화 및 최종 제출 확인

`git push origin main`은 `Everything up-to-date`가 출력되었다. `git status -sb`는 `## main...origin/main`으로 동기화 상태를 나타냈고 `git rev-parse --short origin/main`은 `b2e2cc8`이었다.

```powershell
git push origin main
git status -sb
git rev-parse --short origin/main
```


![GitHub Push 확인 및 원격 HEAD b2e2cc8](images/image(20261124-142324).png)

> **증빙:** GitHub Push 확인 및 원격 HEAD b2e2cc8 (`images/image(20261124-142324).png`)

**최종 판정(해당 시점):** GitHub의 기본 브랜치와 로컬이 동기화되었고, 총 11개 Commit이 기록되었다. 다만 수행 후 별도 제작한 README 최종본은 GitHub 연동 권한에서 403으로 직접 갱신되지 않았으며, 사용자가 다운로드해 로컬에서 Commit/Push해야 반영된다. 이 보고서 자체는 그 별도 README의 원격 반영을 완료로 표기하지 않는다.

## 16. 발생 오류 및 해결 방법 총괄

| 발생 상황 | 증상 | 원인/조치 | 결과 |
|---|---|---|---|
| Python 초기 실행 | `python --version`에 버전 미표시, `py` 인식 불가 | WindowsApps 별칭·설치 환경 확인 후 Python 설치/경로 해결 | Python 3.15.2 실행 |
| `code main.py` | `code` 명령 없음 | VSCode 실행 명령 PATH 미등록 가능; 직접 편집기 열기/메모장 사용 | 파일 편집 진행 |
| JSON 구조 검증 추가 | `expected except or finally block` | `try` 내부 들여쓰기 오류 수정 | 컴파일 정상 |
| UTF-8 테스트 파일 | `Unexpected UTF-8 BOM` | BOM 없는 UTF8 파일 생성 | 실제 구조 검증 진행 |
| 잘못된 JSON 구조 | `quizzes 데이터는 list여야` | 유효성 검사 예외 처리 | 기본 데이터로 안전 진입 |
| 최고 점수 150 | `최고 점수는 0~100 사이` | 점수 범위 검증 | 예외 처리 성공 |
| `save_state` 호출 | `AttributeError` | 함수 정의/들여쓰기 수정 후 메서드 존재 확인 | 정상 저장 |
| Git Commit | `nothing to commit` | Staging 누락 또는 이미 Commit됨; Git 상태 확인 후 선택적 add | 중복 방지 |
| Git 줄바꿈 | LF → CRLF 경고 | Windows 줄바꿈 안내 | 오류 아님 |
| README 원격 직접 수정 | GitHub API 403 | 연결 앱의 쓰기 권한 제한 | 수정된 README 다운로드 제공, 로컬 Push 필요 |


## 17. 최종 검증표 — 과제 요구사항 / 구현 위치 / 완료 여부

| 과제/검증 항목 | 구현 또는 증빙 위치 | 확인 상태 |
|---|---|---|
| 콘솔 퀴즈 게임 | `main.py` / 메뉴 화면 | 완료 |
| 메뉴 5개 | `QuizGame.run()` | 완료 |
| 퀴즈 5개 이상 | `state.json` 8개 | 완료 |
| Quiz / QuizGame 클래스 | `main.py` | 완료 |
| 문제 입력 및 정답 판정 | `Quiz.ask()` | 완료 |
| 무작위 5문제·점수 계산 | `QuizGame.play()` | 완료 |
| 퀴즈 추가 및 즉시 저장 | `QuizGame.add_quiz()` | 완료 |
| JSON 영속성 | `load_state()` / `save_state()` | 완료 |
| 빈 파일·문법/구조 오류 예외 처리 | 코드 + 수동/자동 테스트 | 확인 |
| 메뉴 입력 예외 및 Ctrl+C·EOF | 코드 + PowerShell 화면 | 확인 |
| 안전한 임시 파일 저장 | `state.json.tmp` → `state.json` | 확인 |
| 자동 테스트 4개 | `test_quiz.py` | 4/4 PASS |
| Git Clone | PowerShell 화면 | 완료 |
| Git 브랜치·PR 병합 | Git 로그 | 확인 |
| Git Commit 10개 이상 | `git rev-list --count HEAD` | 11개 확인 |
| Git Pull | `Already up to date.` | 완료 |
| Git Push | `Everything up-to-date` / 원격 HEAD | 완료 |
| README 최신 문구 정비 | 별도 최종 README 제공 | GitHub 반영 재확인 필요 |
| 별도 제출 형식·스크린샷 업로드 규정 | 과제 원문 전수 대조가 아닌 대화 기록 기준 | 최종 제출 규정 재확인 권장 |


## 18. 원격 저장소 및 최종 파일 참고

- GitHub: https://github.com/bigpark61/ai-python-quiz
- `main.py`: 4지선다 게임, 데이터 검증 및 저장
- `test_quiz.py`: 자동 테스트 4개
- `state.json`: 퀴즈 8개 및 점수
- `README.md`: 실행 안내 및 Git 실습 기록(2026-11-24 최종 별도 다운로드본은 추가 적용 필요)
- `.gitignore`: Python 캐시, 임시·백업 파일 제외

### 주요 Git Commit

| SHA | 기록 내용 |
|---|---|
| `d1bbfd0` | JSON 유효성 및 안전한 저장 개선 |
| `827abca` | 딕셔너리 퀴즈 추가 및 점수 갱신 |
| `d667199` | JSON 저장/불러오기 테스트 |
| `bad7f50` | 잘못된 JSON 문법·구조 테스트 |
| `ab1e154` | 퀴즈 추가 후 영속성 테스트 |
| `b2e2cc8` | README 및 과제 증빙 업데이트 |

### 재현에 필요한 명령어

```powershell
cd C:\Temp\ai-python-quiz
python --version
python main.py
python -m unittest test_quiz.py -v
git log --oneline --graph --all
git rev-list --count HEAD
git status -sb
```


## 19. 캡처 전체 목록 (images 폴더)

해당 과제의 제공된 실행 캡처 **총 47개**를 원본 파일명 그대로 보관했습니다. 본문에서 연결하지 않은 캡처도 아래에 모두 링크했습니다. 이미지 파일명에는 대화의 실제 사용 시각과 다른 환경의 파일 저장 시각이 포함될 수 있으므로, 정확한 작업 일시는 대화 흐름을 기준으로 해석해야 합니다.

01. [원본 캡처 — image(20261123-134726).png](images/image(20261123-134726).png)
02. [원본 캡처 — image(20261123-134834).png](images/image(20261123-134834).png)
03. [원본 캡처 — image(20261123-135002).png](images/image(20261123-135002).png)
04. [원본 캡처 — image(20261123-135428).png](images/image(20261123-135428).png)
05. [원본 캡처 — image(20261123-135635).png](images/image(20261123-135635).png)
06. [원본 캡처 — image(20261123-135804).png](images/image(20261123-135804).png)
07. [원본 캡처 — image(20261123-135919).png](images/image(20261123-135919).png)
08. [원본 캡처 — image(20261123-140133).png](images/image(20261123-140133).png)
09. [원본 캡처 — image(20261123-140522).png](images/image(20261123-140522).png)
10. [원본 캡처 — image(20261123-141207).png](images/image(20261123-141207).png)
11. [원본 캡처 — image(20261123-141418).png](images/image(20261123-141418).png)
12. [원본 캡처 — image(20261123-141553).png](images/image(20261123-141553).png)
13. [원본 캡처 — image(20261123-141752).png](images/image(20261123-141752).png)
14. [원본 캡처 — image(20261123-143723).png](images/image(20261123-143723).png)
15. [원본 캡처 — image(20261123-143947).png](images/image(20261123-143947).png)
16. [원본 캡처 — image(20261123-144811).png](images/image(20261123-144811).png)
17. [원본 캡처 — image(20261123-144936).png](images/image(20261123-144936).png)
18. [원본 캡처 — image(20261123-145802).png](images/image(20261123-145802).png)
19. [원본 캡처 — image(20261124-123527).png](images/image(20261124-123527).png)
20. [원본 캡처 — image(20261124-123909).png](images/image(20261124-123909).png)
21. [원본 캡처 — image(20261124-124127).png](images/image(20261124-124127).png)
22. [원본 캡처 — image(20261124-125208).png](images/image(20261124-125208).png)
23. [원본 캡처 — image(20261124-125816).png](images/image(20261124-125816).png)
24. [원본 캡처 — image(20261124-130557).png](images/image(20261124-130557).png)
25. [원본 캡처 — image(20261124-130757).png](images/image(20261124-130757).png)
26. [원본 캡처 — image(20261124-132417).png](images/image(20261124-132417).png)
27. [원본 캡처 — image(20261124-133102).png](images/image(20261124-133102).png)
28. [원본 캡처 — image(20261124-133213).png](images/image(20261124-133213).png)
29. [원본 캡처 — image(20261124-133330).png](images/image(20261124-133330).png)
30. [원본 캡처 — image(20261124-133518).png](images/image(20261124-133518).png)
31. [원본 캡처 — image(20261124-133721).png](images/image(20261124-133721).png)
32. [원본 캡처 — image(20261124-133855).png](images/image(20261124-133855).png)
33. [원본 캡처 — image(20261124-134226).png](images/image(20261124-134226).png)
34. [원본 캡처 — image(20261124-134327).png](images/image(20261124-134327).png)
35. [원본 캡처 — image(20261124-134543).png](images/image(20261124-134543).png)
36. [원본 캡처 — image(20261124-135046).png](images/image(20261124-135046).png)
37. [원본 캡처 — image(20261124-135203).png](images/image(20261124-135203).png)
38. [원본 캡처 — image(20261124-135338).png](images/image(20261124-135338).png)
39. [원본 캡처 — image(20261124-135604).png](images/image(20261124-135604).png)
40. [원본 캡처 — image(20261124-135800).png](images/image(20261124-135800).png)
41. [원본 캡처 — image(20261124-135939).png](images/image(20261124-135939).png)
42. [원본 캡처 — image(20261124-140105).png](images/image(20261124-140105).png)
43. [원본 캡처 — image(20261124-140401).png](images/image(20261124-140401).png)
44. [원본 캡처 — image(20261124-140558).png](images/image(20261124-140558).png)
45. [원본 캡처 — image(20261124-141402).png](images/image(20261124-141402).png)
46. [원본 캡처 — image(20261124-141603).png](images/image(20261124-141603).png)
47. [원본 캡처 — image(20261124-142324).png](images/image(20261124-142324).png)

---

**작성 원칙:** 실제 확인된 출력만 완료로 표기하였고, 작업 지시·예상 출력과 실측 결과를 구분했습니다. 본문에 삽입한 코드 조각은 이해를 위한 핵심 발췌이며 실제 저장소의 전체 코드는 GitHub 파일을 기준으로 확인해야 합니다.

