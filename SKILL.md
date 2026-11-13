---
name: korean-anti-slop-writing
description: Audit, edit, and polish any Korean text (reports, architecture docs, work emails, customer messenger replies, Slack/Teams messages, web UI microcopy, detection rule descriptions, dashboards, and blog posts) to eliminate AI-generated writing patterns (AI slop). Covers 2026 signals ("A가 아니라 B" contrast frames, inflated copulas like 기능한다 and 역할을 한다, Claude vocabulary like 조용히, 떠받친다, 자리, 축, GPT vocabulary like 중요한 건, 꾸준히, sycophancy, source-leaning hedges, closing offers, markdown and emoji overuse, hidden Unicode characters, uniform sentence rhythm, column and article headings written as full sentences ending in ~다, Claude Opus 5.5 tells like 이게 중요합니다 and 단순한 A 그 이상, GPT tells like 입증하지는 않는다, self Q&A, count-first, invented labels, vague attribution, teacher mode, commas after connective endings, placeholders and tracking leftovers) and classic signals (middle dots, em dashes, Hanja, translationese, defensive hedging, staccato sentences, buzzwords, unnatural vocabulary). Use whenever the user asks for Korean copyediting (윤문), removing AI tone (AI 티 제거), checking for AI slop, or making Korean text read naturally like a human wrote it.
---
# Korean Anti-Slop Writing (한국어 윤문과 AI Slop 제거)

Eliminate AI-generated writing patterns ("AI slop") across all Korean writing formats (reports, design docs, work emails, messenger replies, web UI copy, rule descriptions, and blog posts) so every sentence reads naturally as if written by a sharp Korean human writer.

## Core Principle: Keep Every Signal

AI tells shift as models change. In 2026 the em dash and words like "delve" became weaker signals, while contrast frames, inflated copulas, and model-specific vocabulary became stronger ones. When labs remove a known tell, a new one appears (Claude Opus 5.5 cut em dashes by 99% but now says "this matters" 116 times more than humans). **Do not drop a rule because it is old.** Old signals are still fixed; new signals are added on top. No single signal proves AI authorship, so use these rules to edit text, never to accuse a writer.

## Summary

AI-generated or AI-edited Korean text leaves mechanical fingerprints in seven families:

1. **Punctuation and formatting slop (`문장부호와 서식 AI 티`)**: middle dots (`·`, e.g., `설계·구현·검증`), em dashes (`—`), semicolons, bold-colon bullets (`**항목**: 설명`), bold and heading overuse in short replies, emoji bullets (✅ 📌 🚀), chat leaks (`답변:`, `요약:`), arrows in prose, hidden Unicode characters, and Hanja (`發`, `對`, `件`).
2. **2026 structural tells (`2026년 구조 신호`)**: headings and subheadings written as full sentences ending in `~다` (`격차가 컸다`, `능력도 개선됐다`), "A가 아니라 B" and "A보다는 B" contrast frames, "A뿐만 아니라 B", inflated copulas (`~로 기능한다`, `~의 역할을 한다`, `~에 자리한다`), uniform sentence length, long comma-less chained sentences, and `그리고` or `및` overuse.
3. **Model signature vocabulary (`모델별 말버릇`)**: Claude words (`조용히`, `떠받친다`, `얹혀 있다`, `자리` metaphors, `두 축으로`, `결이 같다`, `교차 확인했습니다`), metaphor verbs (`박아 두다`, `얹다`, `태우다`, `물리다`), GPT words (`중요한 건`, `꾸준히`, `실용적인`, `더 명확하게`, `진정으로`), and professional formulas (`결론부터 말하면`, `핵심은`, `세 가지 핵심 축`, `X는 새로운 Y다`).
4. **Low-grade slop (`저급 상투어와 번역투`)**: empty buzzwords (`다양한`, `체계적인`, `효과적인`, `극대화`, `~를 통해`), translationese (`~을 지배한다`, `정합성이 높다`, `~에 의해 ~된다`, `되어진다`, sentence-initial `이는`), verb inflation (`~를 수행한다`), and GPT hedges (`~라고 할 수 있습니다`, `~것으로 보입니다`).
5. **High-grade slop (`프롬프트 부작용과 교정 티`)**: side effects of strict prompting such as staccato sentences in documents, defensive disclaimers (`~라는 뜻은 아니다`), awkward pure-Korean verbs in professional documents (`건수를 세는`), leaked agent worklogs, source-leaning claims (`공식 문서에 따르면 ~로 확인됩니다`), sycophancy (`좋은 질문입니다`, `핵심을 찔렀어요`), closing offers (`원하시면 ~해 드릴까요?`), and mixed politeness.
6. **Late 2026 tells (`2026년 하반기 신호`)**: Claude Opus 5.5 (`이게 중요합니다`, `왜 ~가 중요한가`, `단순한 A 그 이상`, `앞으로를 보면`, superlatives, `도와드릴 수 있습니다`), GPT (`~를 입증하지는 않는다`, `~와 혼동해서는 안 된다`, `또 다른 차원`), rhetorical tics (self Q&A, stacked negation, count-first, invented labels, vague attribution, quotable one-liners, `~에 산다`, teacher mode, meaning tails, tie-backs, `우리` overuse, wh-headings), Korean commas after connective endings, and leftovers (placeholders, `utm_source=chatgpt.com`, `유지했습니다` reports, curly quotes).
7. **Medium-specific slop (`매체별 어색한 문구`)**: fake-polite email clichés (`스스럼없이 말씀해 주세요`), report-style endings pasted into messenger replies (`~로 판단됩니다`), developer error messages or meta-badges in UI (`[읽기용 요약]`, `유효성 검증 실패`), and appendix runarounds in reports.

This skill provides a copyediting workflow, a replacement dictionary (`references/slop-patterns-and-fixes.md`), a multi-format checklist (`references/korean-editing-checklist.md`), and a static linter (`scripts/lint_korean_slop.py`).

## When to Use

- The user asks to polish, copyedit (윤문), or rewrite any Korean text (report, RFC/ADR, email, messenger reply, web UI copy, rule description, blog post, or essay).
- The user asks to check for or remove "AI slop" or "AI 티".
- You are generating a Korean document, email draft, message, or web app UI and need a final quality check before delivery.

## Steps

### Step 1: Run the Linter (When Inspecting Files)

If the target text is in a `.md`, `.txt`, `.html`, `.jsx`, or `.tsx` file, run the bundled linter first. The script lives in this skill's own `scripts/` folder; resolve the path from where the skill is installed.

```bash
python <this-skill-folder>/scripts/lint_korean_slop.py <file> [--medium report|chat|ui] [--json]
# Windows: py -I <this-skill-folder>\scripts\lint_korean_slop.py <file>
```

- `--medium report` (default): every check is on.
- `--medium chat`: staccato check is off, because short sentences are fine in chat replies and messenger messages.
- `--medium ui`: staccato, uniform-length, and long-sentence checks are off.

For text pasted into the conversation, save it to a temporary file and lint it, or apply the rules below by reading.

### Step 2: Apply the 21 Copyediting Rules

Read the text aloud from start to finish and fix these patterns (see `references/slop-patterns-and-fixes.md` for before/after examples).

1. **Purge AI punctuation habits (`가운데점과 대시 제거`)**:
   - **Middle dots (`·`, `ㆍ`)**: zero tolerance. Unpack with particles (`수집과 정규화, 보관`), `및`, commas, parentheses, or separate table rows. Fixed compounds are rewritten too (`입·출력` -> `입출력`, `온·오프라인` -> `온오프라인`). Header separators use parentheses, not dots.
   - **Em dashes (`—`, `―`) and semicolons (`;`)**: Korean prose does not join clauses with them. Replace with commas, parentheses, colons, or separate sentences. Claude still overuses em dashes in 2026, so this rule stays.
   - **Bold-colon bullets**: do not start every bullet with `**명사구**: 설명`. Use sentence bullets or a table.

2. **Cut defensive hedging and audit-defense disclaimers (`AI 방어체 제거`)**:
   - Remove negative disclaimers tacked onto paragraphs (`~라는 뜻은 아니다`, `~로 해석하지 않는다`, `~를 보장하지는 않는다`, `전체로 일반화하지 않는다`).
   - State scope and limitations once in the appropriate section.
   - Remove GPT hedges where a plain statement is possible (`~라고 할 수 있습니다` -> `~입니다`, `~것으로 보입니다` -> `~입니다` when confirmed).

3. **Fix over-purified verbs and translationese, by medium (`어색한 순우리말과 번역투 교정`)**:
   - In reports, design docs, and proposals, replace childish pure-Korean verbs with practitioner verbs: `건수를 세는` -> `건수를 집계하는`, `시간을 재야 한다` -> `시간을 측정해야 한다`, `비용이 붙는` -> `비용이 발생하는`, `문서에 ~라고 적었다` -> `~라고 명시했다`.
   - In chat replies, customer-facing rule descriptions, and UI text read by non-specialists, keep the plain word if it is clearer (`세다`, `재다` are fine there). The goal is the reader's understanding, not formality.
   - Replace calques everywhere: `고객 자료` -> `고객 정보(데이터)`, `강한 비교군` -> `경쟁력 있는 비교 기준`, `사람의 시간` -> `담당자 투입 시간(공수)`, `~을 지배한다` -> `~에 큰 영향을 준다`, `정합성이 높다` -> `잘 맞는다`, `~을 보장한다` -> `꼭 ~하게 한다`, `~에 의해 ~된다` -> active voice, `되어진다` -> `된다`, sentence-initial `이는` -> name the subject or merge.
   - `~를 통해` repeated in one sentence -> `~로`, `~를 사용해`, or an active verb.

4. **Restore human breathing room (`단문 병합과 조사 과밀 해소`)**:
   - **Staccato merge (documents)**: in reports and docs, when 4+ short sentences appear in a row with zero connectors, link related pairs with `하지만`, `반면`, `따라서`, `이에 따라` or connective endings (`~하며`, `~하되`, `~지만`).
   - **Chat replies**: short sentences are fine and often preferred. Instead, keep one point per sentence and never stack caveats in one sentence (`기록상 A이지만 B는 확인하지 못했고, 다만 C일 수 있습니다` -> `A로 기록되어 있습니다. B는 아직 확인하지 못했습니다.`).
   - **Particle pile-up**: if one sentence has 7+ particles, break the noun chain into an active verb clause.

5. **Eliminate buzzwords and verb inflation (`추상 한자어와 상투어 제거`)**:
   - Strip zero-information modifiers: `다양한`, `체계적인`, `효율적인`, `다각적인`, `유기적인`, `획기적`, `압도적`, `극대화하다`, `도모하다`, `제고하다`, `시사하는 바가 크다`, `주목할 만하다`, `본질적으로`, `결론적으로`, `종합하면`, `아울러`, `나아가`.
   - Shrink inflated noun+verb pairs (`검사를 수행한다` -> `검사한다`, `조사를 진행한다` -> `조사한다`).

6. **Purge agent worklogs and meta-commentary (`작업일지와 메타 문구 삭제`)**:
   - Delete sentences that expose prompt history or tooling (`이번 개정에서 모델을 다시 실행하지 않았다`, `기존 코드는 변경하지 않았다`, `허용 오차를 적용했다`).
   - Delete ticket numbers (`feat-123`), `사용자 요청으로`, backup paths, and local file paths from text a reader or customer sees. Change-history comments are two or three words (`신규 등록`, `설명 수정`).
   - Round raw floats in prose and UI (`$0.3532235` -> `약 $0.35`).

7. **Enforce forward-only order and no runarounds (`선출현 금지와 부록 뺑뺑이 금지`)**:
   - Never drop undefined codes (`A3`, `v3`) or future section numbers before explaining them.
   - Delete standalone appendix pointer sentences. Inline the key takeaway.

8. **Break contrast frames (`A가 아니라 B 대비 틀 해체`)**: the strongest 2026 tell, overused by both ChatGPT and Claude.
   - `이건 단순한 설정 문제가 아니라 구조 문제입니다` -> `구조 문제입니다. 설정을 바꿔도 같은 오류가 납니다.` (state B and the evidence).
   - `속도보다는 정확성이 중요합니다` -> `정확성을 먼저 봅니다.`
   - `A가 아닙니다. B입니다.` two-sentence form and `A뿐만 아니라 B` get the same treatment.
   - Keep one contrast only when the contrast itself is the point and the reader actually believed A.

9. **Use plain copulas (`꾸민 동사를 ~이다로`)**: `~로 기능합니다`, `~의 역할을 합니다`, `~에 자리합니다`, `~로서 작동합니다` -> `~입니다` or a concrete verb (`이 룰은 1차 필터로 기능합니다` -> `이 룰은 1차 필터입니다`).

10. **Remove model signature vocabulary (`모델별 말버릇 제거`)**: see the full lists in `references/slop-patterns-and-fixes.md` section 6.
    - Claude: `조용히` (for silent failures), `떠받친다`, `얹혀 있다`, `내력벽`, `삼켜진다`, `자리` metaphors (`봐야 하는 자리`, `세 번째 자리`), compressed nouns (`두 축으로`, `세 지식`), `결이 같다`, `층위`, `갈래`, `뼈대`, `비대칭`, `의도적으로`, `교차 확인했습니다`, `재검증했습니다`, `솔직히 말하면`, `짚고 넘어가면`, and metaphor verbs (`박아 두다`, `얹다`, `태우다`, `물리다`, `흘려보내다`, `깔아 두다`).
    - GPT: `중요한 건`, `꾸준히`, `믿을 수 있는`, `실용적인`, `더 명확하게`, `우선순위를 두다`, `진정으로`, `결정적 증거`, and mixed politeness (`응.`, `됐어.` inside 존댓말 text).
    - Professional formulas: `결론부터 말하면`, `한 줄 요약`, `핵심은`, `포인트는`, `세 가지 핵심 축`, `X는 새로운 Y다`, `분석가처럼`, `검증해 봅시다`.
    - These words are fine when literal (`조용히 재부팅한다` about a silent reboot is fine). Replace only the metaphorical or filler use.

11. **Drop sycophancy and closing offers (`맞장구와 끝 제안 제거`)**:
    - Delete openers like `좋은 질문입니다`, `물론이죠`, `정확히 짚으셨습니다`, `핵심을 찔렀어요`, `상위 1% 사용자`.
    - Delete reflexive closers like `원하시면 ~도 만들어 드릴까요?`, `필요하시면 말씀해 주세요`, `알려 주시면 더 맞춤형으로`. Keep a question only when you truly need the reader's decision to continue.

12. **Stop leaning on sources (`출처에 기댄 판단 제거`)**:
    - `공식 문서에 따르면 정상 요청으로 확인됩니다` when the document never said so -> state your own judgment and its basis (`요청 경로와 응답 코드가 정상 패턴과 같습니다`).
    - Do not pair a missing-evidence caveat with a meaning claim (`원인은 확인되지 않았지만 이는 구조 문제를 시사합니다`). Report what is known and what is not, in separate sentences, without inflating it.

13. **Vary rhythm (`문장 길이와 호흡 조절`)**:
    - Uniform sentence length across a paragraph is a 2026 tell. Mix one short sentence and one longer sentence per paragraph.
    - Long sentences chained with `~하고`, `~하며`, `~해서` and no commas are a tell too. Split them into separate sentences first; do not fix them by sprinkling commas after every connective ending (see rule 20).
    - Cut `그리고` when it appears 3+ times in a paragraph and `및` when it appears 4+ times.

14. **Strip formatting and hidden characters (`서식과 숨은 문자 정리`)**:
    - No emoji bullets, no chat leaks (`답변:`, `요약:`, `결론:`, `TL;DR`), no headings or bold in short replies and messages, no more than two bold spans per paragraph.
    - Arrows (`→`, `⇒`) belong in diagrams and before/after examples, not in prose sentences.
    - Remove zero-width characters, tag characters, and stray non-breaking spaces (`U+200B`, `U+FEFF`, `U+00A0`, `U+3000`). Report a non-breaking space before removing it, since it may be intentional.

15. **Write Hanja in Hangul (`한자 표기 금지`)**: `인터넷發` -> `인터넷발`, `對 고객` -> `고객 대상`, `3件` -> `3건`. Sino-Korean words written in Hangul are fine.

16. **Headings are not sentences (`제목은 ~다로 끝내지 않는다`)**: a strong tell in columns, articles, reports, and blog posts. AI lifts a body sentence and uses it as the heading, so every heading ends in a past-tense `~다`.
    - `컴퓨터 조작과 장기 작업에서 격차가 컸다` -> noun form `컴퓨터 조작과 장기 작업에서 가장 큰 격차` or newspaper style `컴퓨터 조작, 장기 작업서 격차 커`.
    - `긴 맥락에서 필요한 정보를 찾는 능력도 개선됐다` -> `긴 맥락 속 정보 찾기`. Do not lean on the previous heading with `~도`; each heading must stand alone.
    - Keep the conclusion in the heading, but drop the sentence ending. Do not end three or more headings in a row with the same syllable.
    - One question heading (`무엇이 달라졌나`) and topic labels (`처리 속도 비교`) are fine. But when most headings start with `왜`, `무엇이`, `어떻게` by default, that is a tell too (`왜 ~가 중요한가` is a top Claude pattern). Mix forms.

17. **Remove Claude Opus 5.5 tells (`Claude 최신 말버릇`)**: measured against 10,000 human articles in a 2026 study.
    - `이게 중요합니다`, `이 점이 중요합니다` (116x), `왜 ~가 중요한가`, `~가 중요한 이유` (92x) -> state the consequence (`이 값이 틀리면 알림이 안 갑니다`).
    - `단순한 A 그 이상입니다`, `A 그 이상의 B` (the replacement for "A가 아니라 B") -> say what it does.
    - `앞으로를 보면`, `미래를 내다보면` openers (40x) -> delete or give the concrete plan with a date.
    - Superlatives (`가장`, `최고의`, `최적의`) three or more times in a paragraph -> keep one with a number behind it.
    - Helpful pleasantries (`도와드릴 수 있습니다`, `도움이 되셨길 바랍니다`) -> delete.

18. **Remove GPT tells (`GPT 최신 말버릇`)**:
    - `~를 입증하지는 않는다`, `~라고 단정할 수는 없다`, `~를 뒷받침하지 않는다` (275x more than Claude) -> say what the evidence does show, once.
    - `~와 혼동해서는 안 된다`, `~로 봐야 한다` corrective framing -> state the fact directly.
    - `또 다른 차원`, `~을 제공할 수 있다` -> concrete noun and a definite verb.

19. **Remove rhetorical tics (`수사 버릇`)**:
    - Self Q&A (`원인은? 설정 누락이었다.`) -> `원인은 설정 누락이었다.`
    - Stacked negation (`버그도 아니고 장애도 아니다. 설계다.`) -> `의도한 설계다.`
    - Count-first (`이유는 세 가지입니다.`) -> list the reasons; the reader can count.
    - Invented labels without definition (`자동화의 함정`, `정확도 역설`) -> describe the actual problem.
    - Vague attribution (`전문가들은`, `업계에서는`, `많은 연구에 따르면`) -> name the source or delete.
    - Quotable one-liners (`결국 보안은 사람의 문제다.`) and one-line fragment paragraphs (`그게 전부다.`) -> delete or merge.
    - `~에 산다` for location (`이 설정은 config 파일에 산다`) -> `config 파일에 있다`.
    - Teacher mode (`하나씩 뜯어보겠습니다`, `쉽게 말해 ~라고 생각하면 됩니다`, `상상해 보세요`) -> just explain.
    - Meaning tails (`~라는 점을 보여준다`, `~를 방증한다`) after a fact -> let the fact stand or state the conclusion with its basis.
    - Tie-backs and fractal summaries (`정리하자면`, `한마디로`, `다시 처음 질문으로 돌아가면`, a summary after every section) -> one summary at most.
    - `우리` overuse in text written by one person -> name the actor (`보안팀은`, `저는`) or drop the subject.

20. **Do not put commas after connective endings (`연결어미 뒤 쉼표 금지`)**: Korean AI text puts commas where Korean writers do not (`확인했고, 정리하며, 보냈지만,`). Korean readers spot this quickly. Remove the comma, or split the sentence. (English AI text has the opposite habit of too few commas; in Korean the extra comma is the tell.)
    - For short comments and messenger text, AI sounds too formal (`~것 같습니다`, `~에 대해`) and too tidy. Match the medium's casual register when the team writes that way.

21. **Clean leftovers (`남은 흔적 정리`)**:
    - Unfilled placeholders: `[날짜]`, `[회사명]`, `2026-XX-XX`, `PASTE_URL_HERE`, `example.com/` links.
    - Tool traces in links: `utm_source=chatgpt.com`, `utm_source=openai`, `oaicite`, `contentReference[`, `↩`.
    - Process reports: `기존 구조는 그대로 유지했습니다`, `~를 피했습니다`, `중립성을 지켰습니다`, `모든 내용 검증 완료` -> describe what changed, not what was preserved.
    - Curly quotes (`‘ ’ “ ”`) that a Korean keyboard does not produce -> straight quotes, or drop the quotes.

### Step 3: Apply Medium Rules and Verify Against the Checklist

Apply the medium-specific rules in `references/korean-editing-checklist.md` (Parts 2 to 6), then run through the whole checklist to confirm zero remaining slop. Rerun the linter on the edited file.

## Gotchas

- **Preserve facts**: never change numbers, dates, names, quotes, IPs, field names, or code while editing style.
- **Match the medium's politeness and endings**: `~습니다` for customer messenger replies, `~합니다/해요` for emails, blogs, and UI as the team uses them, `~한다` for technical specs, and noun endings (`~함`, `~됨`, `~있음`) for Word reports. Do not turn stiffness into chatty slang.
- **Middle dots are zero tolerance**: including fixed compounds. Check with a search for `·` and `ㆍ` before delivery.
- **Literal use is fine**: `조용히`, `자리`, `축`, `꾸준히` are normal words. Remove them when they are metaphors or filler, not when they describe the literal thing.
- **Do not over-edit**: if the original is already natural, leave it. A clean sentence rewritten for no reason is its own kind of slop.
