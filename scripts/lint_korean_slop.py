#!/usr/bin/env python3
"""Static linter for Korean AI slop patterns in Markdown, text, and UI files.

Usage:
    python lint_korean_slop.py FILE [FILE ...] [--medium report|chat|ui] [--json]
    (Windows: py -I lint_korean_slop.py ...)

--medium report (default): every check is on.
--medium chat: staccato check is off (short sentences are fine in chat replies).
--medium ui:   staccato, uniform-length and long-sentence checks are off.

No signal is dropped because it is old. Older signals (em dash, middle dot,
buzzwords) are still checked, and 2026 signals are checked on top of them.
A hit is an editing hint, not proof that AI wrote the text.

Line checks
  Punctuation and formatting:
    MIDDLE_DOT, MIDDLE_DOT_CHAIN, EM_DASH_SLOP, SEMICOLON_IN_PROSE,
    BOLD_COLON_BULLET, BOLD_OVERUSE, CHAT_LEAK, EMOJI, ARROW_IN_PROSE,
    HIDDEN_CHAR, HANJA
  2026 structure and vocabulary:
    NOT_A_BUT_B, NOT_ONLY_BUT_ALSO, ELABORATE_COPULA, CLAUDE_VOCAB,
    CLAUDE_PLACE_METAPHOR, METAPHOR_VERB, GPT_RECENT_VOCAB, PRO_FORMULA,
    SYCOPHANCY, SOURCE_LEANING, CLOSING_OFFER
  Late 2026 (Claude Opus 5.5, GPT, rhetorical structure, leftovers):
    MATTERS_FRAME, MORE_THAN_FRAME, LOOKING_AHEAD, HELPFUL_PLEASANTRY,
    DOES_NOT_ESTABLISH, CORRECTIVE_FRAMING, GPT_HEDGE_PHRASE, SELF_QA,
    TRIPLE_NEGATION, COUNT_FIRST, INVENTED_LABEL, VAGUE_ATTRIBUTION,
    QUOTABLE_LINE, LIVES_IN, TEACHER_MODE, MEANING_TAIL, TIE_BACK,
    COMMA_AFTER_CONNECTIVE, PLACEHOLDER, TRACKING_LEFTOVER,
    PRESERVED_REPORT, CURLY_QUOTES
  Classic slop:
    DEFENSIVE_HEDGING, KOREAN_HEDGE, AGENT_WORKLOG, UNROUNDED_FLOAT,
    TRANSLATIONESE_VOCAB, TRANSLATIONESE_PATTERN, DOUBLE_TONGHAE,
    VERB_INFLATION, AI_BUZZWORDS, APPENDIX_RUNAROUND, CUSTOM_FAKE_URI
Heading checks (Markdown # headings and bold-only lines)
    HEADING_SENTENCE, HEADING_UNIFORM_ENDING, HEADING_LEANS_ON_PREVIOUS,
    HEADING_WH_DEFAULT
Paragraph and file checks
    STACCATO_PARAGRAPH, UNIFORM_SENTENCE_LENGTH, LONG_SENTENCE_FEW_COMMAS,
    AND_OVERUSE, SUPERLATIVE_OVERUSE, SHORT_FRAGMENT, MIXED_POLITENESS,
    WE_OVERUSE
"""

import argparse
import json
import re
import statistics
from collections import Counter
from pathlib import Path

W = r"[가-힣A-Za-z0-9]"

RULES = [
    # ---------- Punctuation and formatting ----------
    (
        "EM_DASH_SLOP",
        "엠대시(—) 또는 가로줄(―) 사용",
        re.compile(r"\s*[—―]\s*"),
    ),
    (
        "SEMICOLON_IN_PROSE",
        "한국어 문장 사이 세미콜론(;)",
        re.compile(r"[가-힣]\s*;\s*[가-힣]"),
    ),
    (
        "BOLD_COLON_BULLET",
        "굵은 글씨 + 콜론으로 시작하는 목록 (**항목**: 설명)",
        re.compile(r"^\s*([-*+]|\d+\.)\s*\*\*[^*\n]+\*\*\s*[:：]"),
    ),
    (
        "BOLD_OVERUSE",
        "한 줄에 굵은 글씨 3회 이상",
        re.compile(r"\*\*[^*\n]+\*\*.*?\*\*[^*\n]+\*\*.*?\*\*[^*\n]+\*\*"),
    ),
    (
        "CHAT_LEAK",
        "대화형 머리말 노출 (답변:, 요약:, 결론:, TL;DR)",
        re.compile(r"^\s*(\*\*)?(답변|요약|결론|요지|TL;DR|한\s*줄\s*요약)(\*\*)?\s*[:：]"),
    ),
    (
        "EMOJI",
        "이모지 사용 (✅, 📌, 🚀 등)",
        re.compile(r"[\U0001F300-\U0001FAFF☀-⛿✀-➿⭐⭕]"),
    ),
    (
        "ARROW_IN_PROSE",
        "본문 화살표(→, ⇒) 사용",
        re.compile(r"[→⇒]"),
    ),
    (
        "HIDDEN_CHAR",
        "보이지 않는 문자 (제로폭, 줄바꿈 없는 공백, 태그 문자)",
        re.compile(r"[\u200b-\u200f\u2060-\u2064\ufeff\xa0\u202f\u3000\U000E0000-\U000E007F]"),
    ),
    (
        "HANJA",
        "한자 표기 (發, 對, 件 등)",
        re.compile(r"[㐀-䶿一-鿿]+"),
    ),
    # ---------- 2026 structure and vocabulary ----------
    (
        "NOT_A_BUT_B",
        "'A가 아니라 B', 'A보다는 B' 대비 틀",
        re.compile(
            r"(" + W + r"+\s*(이|가)\s*아니라\s|"
            r"라기보다(는)?\s|"
            r"보다는\s|"
            r"아닙니다\.\s*[^.\n]{1,40}입니다|"
            r"아니다\.\s*[^.\n]{1,40}다\.)"
        ),
    ),
    (
        "NOT_ONLY_BUT_ALSO",
        "'A뿐만 아니라 B' 틀",
        re.compile(r"뿐(만)?\s*아니라"),
    ),
    (
        "ELABORATE_COPULA",
        "'~이다' 대신 꾸민 동사 (기능한다, 역할을 한다, 자리한다)",
        re.compile(
            r"((으)?로서\s*(기능|작동|자리)|"
            r"역할을\s*(한|하|합|수행|담당)|"
            r"에\s*자리(한|하|합|잡)|"
            r"(으)?로\s*기능(한|하|합))"
        ),
    ),
    (
        "CLAUDE_VOCAB",
        "Claude 특유 어휘 (조용히, 떠받친다, 축, 결, 교차 확인 등)",
        re.compile(
            r"(조용히|떠받치|떠받쳐|얹혀|내력벽|하중을|교차\s*확인|재검증|"
            r"의도적으로|정직하게\s*말하면|솔직히\s*말하면|짚고\s*넘어가|"
            r"결이\s*(같|다르|맞)|[두세네]\s*축(으로|이|을|에|의)|층위|갈래로|뼈대|"
            r"비대칭|삼켜(지|진|졌|집)|살아남(는|은|았))"
        ),
    ),
    (
        "CLAUDE_PLACE_METAPHOR",
        "Claude 특유 '자리' 은유 (봐야 하는 자리, 세 번째 자리)",
        re.compile(
            r"(봐야\s*하는|어느|첫|두\s*번째|세\s*번째|확인할|고칠|바꿀|들어갈|"
            r"[가-힣]+(하는|되는|갈리는))\s*자리(는|를|에서|가|별|입니다|이다)"
        ),
    ),
    (
        "METAPHOR_VERB",
        "비유 동사 (박다, 얹다, 태우다, 물리다, 흘려보내다, 깔다)",
        re.compile(
            r"(박아\s*(두|넣|놓)|박는|박았|얹(어|는|었|고)|태워\s*(보내|서)|"
            r"물려\s*(두|놓)|흘려\s*보내|깔아\s*(두|놓))"
        ),
    ),
    (
        "GPT_RECENT_VOCAB",
        "GPT 최신 상투어 (중요한 건, 꾸준히, 실용적인, 더 명확하게, 진정으로)",
        re.compile(
            r"(중요한\s*(건|것은|점은)|꾸준(히|한)|믿을\s*수\s*있는|실용적(인|으로)|"
            r"더\s*명확(하게|한|해)|우선순위를\s*(두|정)|진정으로|"
            r"결정적(인)?\s*(증거|역할|차이))"
        ),
    ),
    (
        "PRO_FORMULA",
        "전문직 틀 문구 (결론부터 말하면, 핵심은, 세 가지 핵심 축, X는 새로운 Y다)",
        re.compile(
            r"(결론부터\s*말(하면|씀드리면)|한\s*줄\s*요약|핵심은|포인트는|"
            r"[두세네]\s*가지\s*핵심|핵심\s*축|"
            r"(은|는)\s*새로운\s*[가-힣A-Za-z]+(이다|다|입니다)|"
            r"분석가처럼|검증해\s*(보자|봅시다))"
        ),
    ),
    (
        "SYCOPHANCY",
        "칭찬과 맞장구 (좋은 질문, 핵심을 찔렀어, 상위 1%)",
        re.compile(
            r"(좋은\s*질문|핵심을\s*찔렀|정확히\s*짚(으셨|었)|"
            r"날카로운\s*(지적|질문|관찰)|상위\s*[\d.]+\s*%|물론이죠|"
            r"훌륭한\s*(질문|생각|관찰|지적)|완전\s*잘\s*하고)"
        ),
    ),
    (
        "SOURCE_LEANING",
        "출처에 기댄 판단, 단서 뒤 의미 부여",
        re.compile(
            r"((에|에서)\s*따르면[^.\n]{0,40}(확인된다|확인됩니다|확인할\s*수\s*있|명시되어|식별)|"
            r"(확인되지\s*않았|확인하지\s*못했|알\s*수\s*없)[^.\n]{0,50}"
            r"(시사|의미가|보여준다|보여줍니다|중요하다|중요합니다))"
        ),
    ),
    (
        "CLOSING_OFFER",
        "끝 제안 문구 (원하시면, ~드릴까요?)",
        re.compile(r"(원하시면|필요하시면|원하신다면|[가-힣]+\s*드릴까요\s*\?|알려\s*주시면\s*더)"),
    ),
    # ---------- Late 2026: Claude Opus 5.5 ----------
    (
        "MATTERS_FRAME",
        "'이게 중요합니다', '왜 ~가 중요한가' (Opus 5.5에서 사람보다 92~116배)",
        re.compile(
            r"((이게|이것이|이\s*점이|그게|그\s*점이)\s*중요(합니다|하다|해요|한\s*이유)|"
            r"왜\s*[^.?!\n]{1,30}\s*중요한가|중요한\s*이유(는|가|입니다|다))"
        ),
    ),
    (
        "MORE_THAN_FRAME",
        "'단순한 A 그 이상이다' 틀 ('A가 아니라 B'를 대신한 새 틀)",
        re.compile(r"((단순한|단순히)\s*[^.\n]{0,25}이상(이다|입니다|의|이에요)|[가-힣]+\s+그\s+이상(이다|입니다|의|이에요))"),
    ),
    (
        "LOOKING_AHEAD",
        "'앞으로를 보면' 식 서두 (Opus 5.5에서 40배)",
        re.compile(r"(앞으로를\s*보면|앞을\s*내다보(면|며)|미래를\s*내다보(면|며)|향후를\s*내다보(면|며))"),
    ),
    (
        "HELPFUL_PLEASANTRY",
        "친절 상투 문구 (도와드릴 수 있습니다, 도움이 되셨길 바랍니다)",
        re.compile(r"(도와드릴\s*수\s*있(습니다|어요)|도움이\s*되(셨|었)(길|으면)|도움이\s*되길\s*바랍니다)"),
    ),
    # ---------- Late 2026: GPT ----------
    (
        "DOES_NOT_ESTABLISH",
        "'~를 입증하지는 않는다', '단정할 수 없다' 선긋기 (GPT, Claude보다 275배)",
        re.compile(
            r"(입증하지\s*(는\s*)?(않|못)|단정(할|하기)\s*(수는?\s*없|어렵)|"
            r"뒷받침하지\s*(는\s*)?않|확립(하지|되지)\s*(는\s*)?않)"
        ),
    ),
    (
        "CORRECTIVE_FRAMING",
        "바로잡는 말투 (~와 혼동해서는 안 된다, ~로 봐야 한다)",
        re.compile(r"(혼동해서는\s*안|혼동하면\s*안|(으)?로\s*봐야\s*(한다|합니다)|(으)?로\s*다뤄야\s*(한다|합니다))"),
    ),
    (
        "GPT_HEDGE_PHRASE",
        "GPT 상투 표현 (또 다른 차원, ~을 제공할 수 있다)",
        re.compile(r"(또\s*다른\s*차원|(을|를)\s*제공할\s*수\s*있)"),
    ),
    # ---------- Late 2026: rhetorical structure ----------
    (
        "SELF_QA",
        "혼자 묻고 바로 답하기 (원인은? 설정 누락이었다.)",
        re.compile(r"[가-힣]+\?\s+[가-힣][^?.\n]{0,40}?(다|요)\."),
    ),
    (
        "TRIPLE_NEGATION",
        "부정을 겹친 뒤 답 내놓기 (A도 아니고 B도 아니다. C다.)",
        re.compile(r"(도\s*아니고[^.\n]{0,30}도\s*아니|아닙니다\.\s*[^.\n]{0,30}아닙니다\.|아니다\.\s*[^.\n]{0,30}아니다\.)"),
    ),
    (
        "COUNT_FIRST",
        "개수부터 말하기 (이유는 세 가지입니다)",
        re.compile(r"(두|세|네|다섯|여섯|[2-9])\s*가지(입니다|이다|예요|가\s*있|로\s*(정리|나눌|요약|나뉩|나뉜))"),
    ),
    (
        "INVENTED_LABEL",
        "정의 없이 지어낸 개념 이름 (자동화의 함정, 정확도 역설)",
        re.compile(r"[가-힣]+의\s*(함정|역설|딜레마|저주|패러독스)"),
    ),
    (
        "VAGUE_ATTRIBUTION",
        "흐린 출처 (전문가들은, 업계에서는, 많은 연구에 따르면)",
        re.compile(
            r"(전문가들(은|에\s*따르면|이)|업계에서는|업계\s*관계자들은|많은\s*연구(에서|는|가|에\s*따르면)|"
            r"여러\s*연구(에서|는|가)|일각에서는|많은\s*사람들이)"
        ),
    ),
    (
        "QUOTABLE_LINE",
        "명언 같은 한 줄 (결국 보안은 사람의 문제다)",
        re.compile(r"^\s*(결국|결국은|모든\s*것은|답은|본질은)\s*[^.\n]{2,30}(이다|다|입니다)\.\s*$"),
    ),
    (
        "LIVES_IN",
        "위치를 '산다'로 말하기 (이 설정은 config 파일에 산다)",
        re.compile(r"(에|에서)\s*(산다|삽니다|살고\s*(있다|있습니다|있어요))"),
    ),
    (
        "TEACHER_MODE",
        "선생님 말투 (하나씩 뜯어보겠습니다, 쉽게 말해 ~라고 생각하면 됩니다)",
        re.compile(
            r"(하나씩\s*(뜯어|살펴|짚어)\s*(보겠|보자|봅시다|볼게)|차근차근\s*살펴|쉽게\s*말해|쉽게\s*말하면|"
            r"라고\s*생각하면\s*(됩니다|된다|쉽습니다)|비유하자면|상상해\s*(보세요|보십시오|보자))"
        ),
    ),
    (
        "MEANING_TAIL",
        "사실 뒤 의미 부여 꼬리 (~라는 점을 보여준다)",
        re.compile(r"(라는\s*점을\s*(보여준다|보여줍니다|시사한다|시사합니다|방증한다|드러낸다|드러냅니다)|(을|를)\s*방증(한다|합니다))"),
    ),
    (
        "TIE_BACK",
        "결론 되풀이, 요약 예고 (다시 처음 질문으로, 정리하자면, 한마디로)",
        re.compile(r"(처음\s*질문으로\s*돌아|다시\s*처음으로\s*돌아|정리하자면|다시\s*말해|요컨대|한마디로)"),
    ),
    (
        "COMMA_AFTER_CONNECTIVE",
        "연결어미 뒤 쉼표 (확인했고, 정리하며, 보내지만,)",
        re.compile(r"[가-힣](고|며|면서|지만|는데|은데|아서|어서|해서|하여|으며|이며|므로),\s"),
    ),
    # ---------- Leftovers ----------
    (
        "PLACEHOLDER",
        "채우지 않은 빈칸 템플릿 ([날짜], 2026-XX-XX, PASTE_URL, example.com)",
        re.compile(
            r"(\[(날짜|이름|회사명|회사|고객사|담당자|연도|년도|URL|링크|금액|숫자|내용|제목|[A-Z][A-Z _]{2,})\]|"
            r"\d{4}-XX-XX|(PASTE|INSERT)_[A-Z_]+|example\.(com|org)/)"
        ),
    ),
    (
        "TRACKING_LEFTOVER",
        "AI 도구 흔적 (utm_source=chatgpt.com, oaicite, ↩)",
        re.compile(r"(utm_source=(chatgpt\.com|openai|copilot\.com|claude\.ai|perplexity)|referrer=grok\.com|oaicite|contentReference\[|↩)"),
    ),
    (
        "PRESERVED_REPORT",
        "'유지했습니다', '피했습니다' 식 작업 보고 (모든 내용 검증 완료)",
        re.compile(
            r"(기존\s*[가-힣]+(은|는|을|를)?\s*(그대로\s*)?(유지|보존)(했|하였|함)|(을|를)\s*피했(습니다|다)|"
            r"중립성을\s*(지켰|유지)|모든\s*(내용|주장)(을)?\s*(검증|확인)\s*(완료|했))"
        ),
    ),
    (
        "CURLY_QUOTES",
        "키보드로 치지 않는 둥근 따옴표 (‘ ’ “ ”)",
        re.compile(r"[‘’“”]"),
    ),
    # ---------- Classic slop ----------
    (
        "DEFENSIVE_HEDGING",
        "AI 감사 방어체 (불필요한 부정, 면책 종결)",
        re.compile(
            r"(라는 뜻은 아니다|로 해석하지[는]? 않는다|고 가정하지[는]? 않는다|"
            r"전체 동작으로 일반화하지 않는다|안전성으로 확대하지 않는다|"
            r"대표 업무로 삼지 않는다|성능으로 간주하지 않는다|"
            r"내부 사고\s*과정을 저장|내부 사고\s*과정은 포함하지)"
        ),
    ),
    (
        "KOREAN_HEDGE",
        "얼버무림 (~라고 할 수 있습니다, ~것으로 보입니다)",
        re.compile(
            r"(라고\s*할\s*수\s*있(다|습니다|어요)|"
            r"것(으)?로\s*보(인다|입니다|여집니다|여진다)|"
            r"(할|될)\s*수\s*있을\s*것)"
        ),
    ),
    (
        "AGENT_WORKLOG",
        "에이전트 작업일지, 버전 관리 노출",
        re.compile(
            r"(이번 개정에서|기존 제출본|보존한 기존 부록|수동 재전송|수동으로 재전송|"
            r"이번 초안에서 실행 완료로|허용 오차를 적용했다|데모 응답과의 매핑은|"
            r"feat-\d+|사용자\s*요청(으로|에\s*따라)|백업(은|:)\s*\S+/)"
        ),
    ),
    (
        "UNROUNDED_FLOAT",
        "반올림되지 않은 소수점(4자리 이상) 노출",
        re.compile(r"\$?\d+\.\d{4,}"),
    ),
    (
        "TRANSLATIONESE_VOCAB",
        "어색한 번역투, 순우리말 조어",
        re.compile(
            r"(강한 비교군|강한 자동 수집 비교군|사람의 시간|고객 자료|자료 등급|"
            r"이동 시간창|작은 이상징후|합성 시험|합성 평가|계정 영역|"
            r"모델 호출 비용이 붙는|시간까지 재야 한다|로그를 세는|시작을 세는|"
            r"무오류 결과도 확인한 표본|같게 맞춘 조건)"
        ),
    ),
    (
        "TRANSLATIONESE_PATTERN",
        "번역투 문형 (지배한다, 보장한다, ~에 의해 ~된다, 되어지다, 이는)",
        re.compile(
            r"((을|를)\s*지배(한다|합니다)|정합성이\s*(높|낮)|(을|를)\s*보장(한다|합니다)|"
            r"에\s*의해\s*[가-힣]*(된다|됩니다|되었|됐)|되어(지|진|집|졌)|보여진다|보여집니다|"
            r"에\s*있어서|에\s*대해서?\s|(^|[.!?]\s+)이는\s)"
        ),
    ),
    (
        "DOUBLE_TONGHAE",
        "한 문장 내 '~를 통해' 중복 사용 (번역투)",
        re.compile(r"(을|를)\s*통해.*?(을|를)\s*통해"),
    ),
    (
        "VERB_INFLATION",
        "동사 부풀리기 (~을 수행한다, ~를 진행한다)",
        re.compile(r"(을|를)\s*(수행|진행|완료|실시)(한다|합니다|했다|했습니다|하였)"),
    ),
    (
        "AI_BUZZWORDS",
        "저급 AI 상투어, 추상어",
        re.compile(
            r"(다양한|체계적인|효과적인|효율적인|다각적인|유기적인|포괄적인|혁신적인|"
            r"획기적|압도적|극대화(하|한|합|했)|제고(하|한|합|했)|도모(하|한|합|했)|시사하는\s*바|주목할\s*만|"
            r"본질적으로|결론적으로|요약하자면|종합하면|아울러|나아가|"
            r"스스럼없이|평안하신지요|유효성 검증에 실패|\[읽기용 요약\])"
        ),
    ),
    (
        "APPENDIX_RUNAROUND",
        "부록, 별첨 뺑뺑이 포인터 문장",
        re.compile(
            r"(부록\s*[A-Z0-9-]+에\s*(둔다|있다|정리했다|명시한다)|"
            r"부록\s*[A-Z0-9-]+(을|를)\s*참고한다|"
            r"별첨\s*`?README`?에\s*(있다|기록했다)|"
            r"세부 원장은 별첨에 있다)"
        ),
    ),
    (
        "CUSTOM_FAKE_URI",
        "가상 커스텀 URI 스키마 사용",
        re.compile(r"(evidence|coverage|usage)://[a-zA-Z0-9_-]+"),
    ),
]

MIDDLE_DOT = re.compile(W + r"+(?:\s*[·ㆍ]\s*" + W + r"+)+")

CONNECTORS = re.compile(
    r"(하지만|그러나|반면|따라서|이에 따라|특히|예를 들어|가령|다만|또한|즉|한편|"
    r"기 때문에|하므로|으므로|지만|하되|하며|면서)"
)
CHAIN_ENDINGS = re.compile(r"(고|며|면서|해서|하여|이고|지만)\s")
POLITE_END = re.compile(r"(습니다|세요|어요|아요|해요|예요|이에요|죠)[.!?]")
BANMAL_END = re.compile(r"(^|\s)(응|그래|했어|봤어|됐어|있어|없어|할게|줄게|거야|맞아|알겠어)[.!?]")
SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")


def strip_code(text: str) -> list:
    """Return (line_number, line_text) with fenced code blocks blanked and inline code removed."""
    result = []
    in_fence = False
    for idx, line in enumerate(text.splitlines(), start=1):
        if re.match(r"^\s*(```|~~~)", line):
            in_fence = not in_fence
            result.append((idx, ""))
            continue
        result.append((idx, "" if in_fence else re.sub(r"`[^`\n]*`", "``", line)))
    return result


def paragraphs(lines):
    para, start = [], 1
    for line_no, text in lines:
        if not text.strip():
            if para:
                yield start, para
            para = []
        else:
            if not para:
                start = line_no
            para.append(text.strip())
    if para:
        yield start, para


def is_prose(first_line: str) -> bool:
    return not first_line.startswith(("#", "-", "*", "|", "!", ">", "+")) and not re.match(r"^\d+\.", first_line)


def check_paragraphs(lines, medium: str) -> list:
    findings = []
    for start, para_lines in paragraphs(lines):
        if not is_prose(para_lines[0]):
            continue
        para = " ".join(para_lines)
        sentences = [s.strip() for s in SENT_SPLIT.split(para) if s.strip()]
        snippet = para[:120] + ("..." if len(para) > 120 else "")

        if medium == "report" and len(sentences) >= 4 and not CONNECTORS.search(para):
            findings.append({"line": start, "rule": "STACCATO_PARAGRAPH",
                             "label": f"접속사, 연결어미 없는 단문 {len(sentences)}연속 (스타카토 호흡)",
                             "snippet": snippet})

        if medium != "ui" and len(sentences) >= 5:
            lengths = [len(s) for s in sentences]
            mean = statistics.mean(lengths)
            if mean >= 15 and statistics.pstdev(lengths) / mean < 0.2:
                findings.append({"line": start, "rule": "UNIFORM_SENTENCE_LENGTH",
                                 "label": f"문장 길이가 고르게 같음 (평균 {mean:.0f}자, 문장 {len(sentences)}개)",
                                 "snippet": snippet})

        if medium != "ui":
            for s in sentences:
                if len(s) >= 90 and "," not in s and len(CHAIN_ENDINGS.findall(s)) >= 2:
                    findings.append({"line": start, "rule": "LONG_SENTENCE_FEW_COMMAS",
                                     "label": f"쉼표 없이 연결어미로 길게 이은 문장 ({len(s)}자)",
                                     "snippet": s[:120] + ("..." if len(s) > 120 else "")})

        if para.count("그리고") >= 3 or para.count("및") >= 4:
            findings.append({"line": start, "rule": "AND_OVERUSE",
                             "label": "한 문단에 '그리고' 3회 이상 또는 '및' 4회 이상",
                             "snippet": snippet})

        if len(SUPERLATIVES.findall(para)) >= 3:
            findings.append({"line": start, "rule": "SUPERLATIVE_OVERUSE",
                             "label": "한 문단에 최상급(가장, 최고의, 최적의) 3회 이상",
                             "snippet": snippet})

        if medium != "ui" and len(sentences) == 1 and len(para) <= 15 and re.search(r"[가-힣]", para):
            findings.append({"line": start, "rule": "SHORT_FRAGMENT",
                             "label": "강조용 한 줄 단편 문단 (그게 전부다. 끝.)",
                             "snippet": snippet})
    return findings


SUPERLATIVES = re.compile(r"(가장\s|최고의|최상의|최적의|궁극적|최대한)")
WE_WORD = re.compile(r"우리(는|가|의|를|도|에게)")


def check_we(lines) -> list:
    hits = [(n, t) for n, t in lines if WE_WORD.search(t)]
    if sum(len(WE_WORD.findall(t)) for _, t in hits) < 3:
        return []
    return [{"line": n, "rule": "WE_OVERUSE", "label": "'우리' 남용 (혼자 쓴 글인데 '우리는 ~해야 합니다')",
             "match": WE_WORD.search(t).group(0), "snippet": t.strip()} for n, t in hits]


HEADING = re.compile(r"^\s*(#{1,6}\s+(?P<h>.+?)|\*\*(?P<b>[^*]+)\*\*)\s*#*\s*$")
HEADING_DA = re.compile(r"[가-힣]*다$")
DO_WORD = re.compile(r"([가-힣]+)도\s")
WH_START = re.compile(r"^(\d+[.)]\s*)?(왜|무엇|어떻게|어디|언제|누가|무슨)")
# Nouns that simply end in 도 (degree, system, etc.), not the particle 도
DO_NOUN_ENDINGS = (
    "온도", "속도", "정도", "강도", "각도", "제도", "태도", "빈도", "밀도", "용도", "의도", "한도",
    "고도", "습도", "농도", "이도", "확도", "뢰도", "험도", "요도", "족도", "지도", "여도", "성도",
    "감도", "시도", "인도", "보도", "전도", "주도", "수도", "년도", "연도", "가도", "반도", "포도",
)


def check_headings(lines) -> list:
    findings = []
    all_headings = []  # Hangul headings: (line_no, text)
    run = []  # consecutive headings: (line_no, text, last_syllable)

    def flush_run():
        if len(run) >= 3 and len({r[2] for r in run}) == 1:
            findings.append({"line": run[0][0], "rule": "HEADING_UNIFORM_ENDING",
                             "label": f"제목 {len(run)}개가 같은 글자('{run[0][2]}')로 끝남",
                             "snippet": " / ".join(r[1] for r in run)[:160]})

    for line_no, text in lines:
        m = HEADING.match(text)
        if not m:
            continue  # body text between headings does not break the run
        h = (m.group("h") or m.group("b") or "").strip().rstrip(".!?。 ")
        if not re.search(r"[가-힣]$", h):
            flush_run()
            run = []
            continue
        if HEADING_DA.search(h):
            findings.append({"line": line_no, "rule": "HEADING_SENTENCE",
                             "label": "제목이 '~다' 완결 문장으로 끝남 (명사형이나 신문식으로)",
                             "match": h[-6:], "snippet": text.strip()})
        for dm in DO_WORD.finditer(h + " "):
            word = dm.group(1) + "도"
            if not word.endswith(DO_NOUN_ENDINGS) and dm.end() < len(h):
                findings.append({"line": line_no, "rule": "HEADING_LEANS_ON_PREVIOUS",
                                 "label": "제목이 '~도'로 앞 제목에 기댐", "match": word,
                                 "snippet": text.strip()})
                break
        all_headings.append((line_no, h))
        run.append((line_no, h, h[-1]))
        if len(run) >= 2 and run[-1][2] != run[-2][2]:
            last = run.pop()
            flush_run()
            run = [last]
    flush_run()

    wh = [(n, h) for n, h in all_headings if WH_START.match(h)]
    if len(wh) >= 3 and len(wh) * 2 >= len(all_headings):
        for n, h in wh:
            findings.append({"line": n, "rule": "HEADING_WH_DEFAULT",
                             "label": f"제목 {len(all_headings)}개 중 {len(wh)}개가 왜, 무엇, 어떻게로 시작",
                             "match": h[:20], "snippet": h})
    return findings


def check_politeness(lines) -> list:
    polite = sum(len(POLITE_END.findall(t)) for _, t in lines)
    if polite < 3:
        return []
    findings = []
    for line_no, text in lines:
        m = BANMAL_END.search(text)
        if m:
            findings.append({"line": line_no, "rule": "MIXED_POLITENESS",
                             "label": "높임말 글에 반말 종결이 섞임", "match": m.group(0).strip(),
                             "snippet": text.strip()})
    return findings


def lint_file(path: Path, medium: str) -> list:
    raw = path.read_text(encoding="utf-8-sig")
    lines = strip_code(raw)
    findings = []
    for line_no, line in lines:
        if not line.strip():
            continue
        for match in MIDDLE_DOT.finditer(line):
            dots = match.group(0).count("·") + match.group(0).count("ㆍ")
            rule, label = (("MIDDLE_DOT_CHAIN", "가운데점(·)으로 셋 이상 묶음") if dots >= 2
                           else ("MIDDLE_DOT", "가운데점(·) 사용 (고정 복합어 포함 0건이 기준)"))
            findings.append({"line": line_no, "rule": rule, "label": label,
                             "match": match.group(0), "snippet": line.strip()})
        for rule_id, label, pattern in RULES:
            for match in pattern.finditer(line):
                shown = match.group(0).strip() or match.group(0)
                if rule_id == "HIDDEN_CHAR":
                    shown = f"U+{ord(match.group(0)):04X}"
                findings.append({"line": line_no, "rule": rule_id, "label": label,
                                 "match": shown, "snippet": line.strip()})
    findings.extend(check_headings(lines))
    findings.extend(check_paragraphs(lines, medium))
    findings.extend(check_politeness(lines))
    findings.extend(check_we(lines))
    findings.sort(key=lambda x: x["line"])
    return findings


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("files", nargs="+", type=Path, help="Markdown, text, or UI files to lint")
    parser.add_argument("--medium", choices=["report", "chat", "ui"], default="report",
                        help="report (default), chat, or ui")
    parser.add_argument("--json", action="store_true", help="Output JSON report")
    args = parser.parse_args()

    all_reports = {}
    total = 0
    counts = Counter()
    for f in args.files:
        issues = lint_file(f, args.medium)
        all_reports[str(f)] = issues
        total += len(issues)
        counts.update(i["rule"] for i in issues)

    if args.json:
        print(json.dumps({"total_issues": total, "by_rule": dict(counts), "files": all_reports},
                         ensure_ascii=False, indent=2))
        return
    for fname, issues in all_reports.items():
        print(f"=== {fname} ({len(issues)} issues) ===")
        for item in issues:
            matched = f" [{item['match']}]" if "match" in item else ""
            print(f"  L{item['line']} [{item['rule']}] {item['label']}{matched}")
            print(f"    -> {item['snippet']}")
    print(f"\nTotal issues found: {total}")
    for rule, n in counts.most_common():
        print(f"  {rule}: {n}")


if __name__ == "__main__":
    main()
