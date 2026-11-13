# Korean AI Slop Patterns and Copyediting Fixes (한국어 윤문 사전)

Use this reference to detect and rewrite AI-generated Korean patterns across reports, emails, messenger replies, web UI copy, rule descriptions, and blog posts. In the tables, the Bad column intentionally contains slop (middle dots, em dashes, and so on) as examples. Never copy it into output.

## 1. Punctuation and Formatting Slop (`문장부호와 서식 AI 티`)

Punctuation is the fastest way a Korean reader spots AI-generated text before even reading the content.

| Pattern | Why It Screams "AI" | Bad (AI Slop) | Good (Natural Korean) |
| :--- | :--- | :--- | :--- |
| **Middle Dot (`·`) Mania** | Korean humans rarely type `·`, whereas LLMs use it in almost every sentence to compress English `A, B, and C` or `A/B` lists. Zero tolerance, including fixed compounds. | 계정·권한 관리와 승인·위임 이력을 조회·대조해 탐지·차단한다. / 단말 · IP · MAC / 입·출력 | 계정과 권한 관리, 승인 및 위임 이력을 대조해 탐지하고 차단한다. / 단말, IP, MAC / 입출력 |
| **Em Dash (`—`) Clauses** | Korean typography does not use `—` to insert parenthetical thoughts. In 2026 ChatGPT uses fewer dashes than humans, but Claude still overuses them, so the rule stays. | 점검은 야간에 한다 — 즉 업무 시간에는 서비스를 멈추지 않는다. | 점검은 야간에 한다. 업무 시간에는 서비스를 멈추지 않는다. |
| **Semicolon (`;`)** | English clause joining carried into Korean. | 수집은 완료됐다; 분석은 내일 한다. | 수집은 완료됐다. 분석은 내일 한다. |
| **Colon-Bold List Fetish** | Every bullet starts with `**명사형 키워드**: 설명`, even when a simple sentence list is easier to read. | - **가용성 확보**: 큐를 분리해 장애를 막는다.<br>- **비용 절감**: 오래된 로그는 Cold에 둔다. | - 수집기와 검색 사이에 큐를 두어 장애가 전파되지 않게 한다.<br>- 오래된 로그는 Cold 저장소로 옮겨 검색 비용을 줄인다. |
| **Slash (`/`) Stacking** | Packing 3+ nouns with slashes inside prose or diagram subtitles. | 분석가 / 권한·서비스 팀이 결과 검토 / 승인 후 대응 | 분석가와 서비스 담당 팀이 결과를 검토하고 승인 후 대응 |
| **Unnecessary Quotes (`‘ ’`, `“ ”`)** | Quotes around ordinary words that are not verbatim quotes or newly coined terms. | 시스템의 ‘안정성’과 ‘확장성’을 함께 확보한다. | 시스템의 안정성과 확장성을 함께 확보한다. |
| **Markdown Overuse** | As of late 2026, markdown is one of the most common AI signs. Headings and bold inside a three-line reply look like chatbot output. | ### 1. 개요<br>**결론**: 정상입니다. **근거**: 로그 확인. **조치**: 없음. | 정상입니다. 같은 시간 로그에서 오류가 없었습니다. |
| **Emoji Bullets** | Emoji used as list markers or heading decorations. | ✅ 수집 완료<br>📌 다음 단계 | 수집을 마쳤습니다. 다음은 분석입니다. |
| **Chat Leaks** | Chatbot reply scaffolding pasted into a document. | 답변: 아래와 같습니다.<br>TL;DR: 정상 | (delete the label and write the content) |
| **Arrows in Prose** | `→` used as a verb inside sentences. | 로그 수집 → 정규화 → 저장되어 검색 가능 | 로그를 수집하고 정규화해 저장하면 검색할 수 있다. |
| **Hidden Characters** | Zero-width spaces, tag characters, and stray non-breaking spaces left by AI tools or copy-paste. | (invisible U+200B, U+FEFF, U+00A0, U+3000) | Remove. Report U+00A0 before removing, since it may be intentional. |
| **Hanja Abbreviations** | Hanja shorthand slows Korean readers. | 인터넷發 공격 3件, 對 고객 공지 | 인터넷발 공격 3건, 고객 대상 공지 |

## 2. Universal Grammar and Rhythm Slop (`문장 호흡, 어순, 조사 AI 티`)

| Pattern | Bad (AI Slop) | Good (Natural Korean) |
| :--- | :--- | :--- |
| **Conjunction-free Staccato (단문 스타카토, documents)** | 신규 수집기는 지난주에 설치했다. 처리량은 테스트 로그로 비교했다. 두 수집기의 처리량은 같았다. 이 조건에서 신규 수집기는 메모리를 더 썼다. 기존 수집기를 유지한다. | 지난주에 신규 수집기를 설치해 테스트 로그로 비교해 보니, 처리량은 기존 수집기와 같았지만 메모리는 신규 수집기가 두 배를 썼다. 따라서 기존 수집기를 유지한다. |
| **Stacked Caveats (단서 겹치기, chat)** | 기록상 A이지만 B는 확인하지 못했고, 다만 C일 가능성도 있습니다. | A로 기록되어 있습니다. B는 아직 확인하지 못했습니다. |
| **Uniform Sentence Length (문장 길이 균일)** | 첫째 장비는 방화벽 로그를 수집합니다. 둘째 장비는 웹 방화벽을 수집합니다. 셋째 장비는 침입 탐지 로그를 수집합니다. 넷째 장비는 백신 로그를 수집합니다. | 장비 네 대가 로그를 보냅니다. 방화벽, 웹 방화벽, 침입 탐지, 백신 서버입니다. 이 중 웹 방화벽만 30분 늦게 들어옵니다. |
| **Long Comma-less Chains (쉼표 없는 긴 연결)** | 수집기는 매분 로그를 받아서 정규화 파서로 넘기고 파서는 필드를 뽑아서 인덱스로 보내며 인덱스는 다시 알림 엔진에 데이터를 제공합니다. | 수집기는 매분 로그를 받아 파서로 넘깁니다. 파서가 필드를 뽑아 인덱스에 넣으면, 알림 엔진이 그 데이터로 룰을 평가합니다. |
| **`그리고` / `및` Overuse** | 로그를 수집하고 그리고 정규화한다. 그리고 보관한다. 그리고 검색한다. | 로그를 수집해 정규화하고 보관한 뒤 검색한다. |
| **Particle Pile-up (조사 과밀)** | 테스트 로그 비교**에서는** 야간 배치**가** 실행된 서버**를** 대상**으로** 로그**를** 모아 파서**에** 전달한 방식**과** 에이전트 방식**이** 같은 처리량**을** 얻었다. | 테스트 로그로 비교해 보니, 야간 배치가 실행된 서버에서는 로그를 모아 파서로 넘기는 방식과 에이전트 방식의 처리량이 같았다. |
| **Double `~를 통해` (Via/Through Abuse)** | 수집기를 **통해** 모은 로그를 정규화 파서를 **통해** 변환하여 SIEM을 **통해** 검색한다. | 수집기가 모은 로그를 정규화 파서로 변환해 SIEM에서 검색한다. |
| **Inanimate Subject (무생물 주어 번역투)** | 이 아키텍처는 높은 안정성을 제공한다. / 이 헤더는 요청 출처를 서버 응답에 담는다. | 이렇게 구성하면 시스템이 안정적으로 동작한다. / 서버는 응답 헤더에 요청 출처를 함께 담는다. |
| **Abstract Noun Subject (추상명사 주어)** | 이 패턴의 활용은 오류 감소를 가능하게 합니다. | 이 패턴을 쓰면 오류가 줄어듭니다. |
| **Nominalized Endings (`~하는 일이다 / ~한 범위다`)** | 어떤 파일에 접근했는지 확인하는 일이다. / 야간 배치의 실패를 복구한 범위다. | 어떤 파일에 접근했는지 확인해야 한다. / 야간 배치가 실패한 상황에서 담당자가 수동으로 복구한 사례다. |
| **Verb Inflation (`~을 수행한다 / 진행한다 / 완료한다`)** | 권한 검사를 수행하고 로그 조회를 진행한다. | 권한을 검사하고 로그를 조회한다. |
| **Double Passive (`~되어지다 / ~로 보여진다`)** | 정상 요청으로 판단되어진다. / 효과적인 것으로 보여진다. | 정상 요청으로 판단된다. / 효과적인 것으로 보인다. |
| **English Verb Mapping (영어 동사 1:1 대응)** | 설정값이 성능을 지배한다. / 두 값의 정합성이 높다. / 이 옵션은 재시도를 보장한다. | 설정값이 성능에 큰 영향을 준다. / 두 값이 잘 맞는다. / 이 옵션을 켜면 꼭 재시도한다. |
| **Sentence-initial `이는` ("This is")** | 수집이 30분 늦었다. 이는 큐 적체 때문이다. | 수집이 30분 늦었다. 큐가 밀렸기 때문이다. |

## 3. Vocabulary Slop: Over-Purified Korean vs. Empty Buzzwords (`어휘 양극단 오류`)

AI either uses pompous Sino-Korean buzzwords (default mode) or childish pure-Korean words (when told "write in easy Korean"). Avoid both extremes, and choose by medium: practitioner vocabulary for reports and design docs, plain words for chat replies and text read by non-specialists.

### A. Empty Buzzwords to Delete (`저급 AI 상투어`)
- `다양한` (various) -> State the exact count or list the items (`3가지 방식`, `인증과 파일 로그`).
- `체계적인 / 다각적인 / 유기적인 / 포괄적인 / 혁신적인 / 획기적인 / 압도적인` -> Delete the modifier and describe the actual mechanism.
- `극대화하다 / 제고하다 / 도모하다 / 기하다` -> `높이다 / 줄이다 / 넓히다 / 막다`.
- `시사하는 바가 크다 / 주목할 만하다 / 본질적으로` -> Delete or state the concrete conclusion.
- `결론적으로 / 요약하자면 / 종합하면 / 아울러 / 나아가` -> Delete or replace with `따라서 / 또한`.

### B. Over-Purified and Translationese Words to Fix (`번역투와 어색한 순화어`)
| Concept | Unnatural AI Expression | Natural Practitioner Expression (reports and docs) |
| :--- | :--- | :--- |
| **Data / Payload** | 고객 자료, 자료 등급, 읽은 자료량 | 고객 정보(데이터), 데이터 등급, 읽은 로그 양 |
| **Strong baseline** | 강한 비교군 | 경쟁력 있는 비교 기준, 고도화된 비교군 |
| **Human effort** | 사람의 시간, 사람의 검토 시간 | 담당자(분석가) 투입 시간, 검토 공수 |
| **Count / Aggregate** | 로그를 세는 탐지, 한 번만 세고 | 로그 건수를 집계하는 탐지, 1회로 집계하고 |
| **Measure time** | 수정하는 시간까지 재야 한다 | 수정하는 시간까지 측정해야 한다 |
| **Incur cost** | 호출 비용이 붙는 것을 | 호출 비용이 발생하는 것을 |
| **Stated / Noted** | 문서에 ~라고 적었다 (repeated) | ~라고 명시했다 / 기재했다 / 밝혔다 |
| **Equal conditions** | 같게 맞춘 조건 | 공통 통제 조건 |
| **Atomically** | 원자적으로 수행한다 | 하나의 트랜잭션으로 처리한다 |
| **Sliding window** | 이동 시간창 | 슬라이딩 윈도우(Sliding Window) |
| **Govern / Ensure** | ~을 지배한다, ~을 보장한다 | ~에 큰 영향을 준다, 꼭 ~하게 한다 |

In chat replies and customer-facing rule descriptions, `세다`, `재다` are acceptable when they are clearer to the reader than `집계하다`, `측정하다`.

## 4. High-Grade Slop: Defensive Hedging and Leaked Worklogs (`방어체와 작업일지`)

| Category | AI Slop Pattern | How to Fix |
| :--- | :--- | :--- |
| **Defensive Disclaimers (`AI 감사 방어체`)** | 이 사례를 전체 동작으로 일반화하지 않는다. / 모든 회사에 동일한 배치가 강제된다는 뜻은 아니다. / 작은 표본의 무오류를 안전성으로 확대하지 않는다. | **Delete.** State the scope once in the methodology or rollout plan. |
| **GPT Hedges (`얼버무림`)** | ~라고 할 수 있습니다. / ~인 것으로 보입니다. / ~할 수 있을 것입니다. | Say it plainly when confirmed (`~입니다`). Keep `~로 보입니다` only for real uncertainty, once. |
| **Revision and Prompt Leaks (`작업일지 노출`)** | 이번 개정에서 모델을 다시 실행하지 않았다. / 기존 제출본의 코드는 변경하지 않았다. / 사용자 요청으로 삭제, 백업은 ops/backup-1111 / feat-512 반영 | **Delete completely.** Change-history comments become two or three words (`삭제`, `설명 수정`). |
| **Unrounded Floats (`소수점 복붙`)** | 비용은 $0.3532235와 중앙값 7.8037초였다. | Round to 1 or 2 decimal places (`약 $0.35`, `7.8초`). |
| **Appendix Runarounds (`부록 뺑뺑이`)** | 용량 산식은 부록 E에 둔다. / 상세 내역은 별첨 README에 있다. | Inline the takeaway or delete the pointer sentence. |

## 5. Medium-Specific Slop (`매체별 윤문 가이드`)

### A. Business Emails
| AI Email Slop | Natural Korean Workplace Phrasing |
| :--- | :--- |
| 바쁘신 와중에도 메일 확인해 주셔서 진심으로 감사드립니다. (every single time) | 안녕하세요, OOO님. OOO팀 홍길동입니다. (Go straight to the point after a clean greeting) |
| 혹시라도 추가적인 문의사항이 있으시다면 언제든지 스스럼없이 편하게 연락 부탁드립니다. | 확인해 보시고 궁금한 점이나 조율이 필요한 부분이 있으면 편하게 말씀해 주세요. |
| 아래에 요청하신 사항에 대한 핵심 요약을 정리하여 공유드립니다. | 요청하신 OOO 검토 결과 공유드립니다. (Or lead with the 1-line conclusion) |
| 본 메일은 OOO을 목적으로 작성되었습니다. | OOO 건으로 확인 요청드립니다. |

### B. Customer Messenger Replies (Slack, Teams, KakaoWork)
Write as the person in charge would type it: conclusion first, short, `~습니다/~입니다` endings. Avoid 해요체 (`~요`, `~어요`, `~네요`) in customer replies.

| AI Messenger Slop | Natural Reply |
| :--- | :--- |
| 해당 트래픽은 정상 서비스 요청으로 판단됩니다. 추가적인 이상 징후는 확인되지 않았습니다. 지속적으로 모니터링하겠습니다. 확인 부탁드립니다. | 정상 서비스 요청입니다. 같은 시간대에 다른 이상 접속은 없었습니다. |
| ~것으로 보이며, ~로 사료됩니다. | ~입니다. (or state what is not known yet in a separate sentence) |

### C. Web UI, Dashboards, and Product Microcopy
Operational screens show names and values only. No section captions, row-by-row explanations, footnotes, or raw code values.

| AI Web UI Slop | Natural Product UI Copy |
| :--- | :--- |
| `[읽기용 요약]` / `[설계 예시 / 실제 실행 아님]` / `SHA-256: b89e4c...` (meta badges inside UI) | Remove meta badges; show realistic status badges (`권한 오용 의심`, `검토 대기`). |
| 섹션 제목 옆 설명: "지점마다 접속 주소와 계정이 따로 있어요. 여기서 관리합니다." | (delete; the title and the values are enough) |
| `BENIGN_CONTEXT`, `KNOWN_NOISE` (raw reason codes) | `정상 업무`, `알려진 소음` or remove |
| `입력하신 파라미터의 유효성 검증에 실패하였습니다.` | `날짜 형식을 다시 확인해 주세요 (예: 2026.11.13)` |
| `데이터 조회가 성공적으로 완료되었습니다.` | Show the results directly, or `조회 완료 (23건)` |
| `알 수 없는 오류가 발생했습니다. 관리자에게 문의하세요.` | `연결이 일시적으로 끊겼어요. 잠시 후 다시 시도해 주세요.` |
| `유저에 의해 작업이 취소되었습니다.` | `작업을 취소했어요.` or `취소된 작업` |

### D. Detection Rule Descriptions and Change History
| AI Slop | Natural Team Style |
| :--- | :--- |
| 본 룰은 출발지 IP별로 120분 내 동일 URI에 대한 요청이 임계치를 초과하는 경우를 체계적으로 탐지하기 위한 목적으로 설계되었습니다. | 평소 접속하지 않던 해외 IP에서 관리자 계정으로 로그인하여 탐지 |
| (exclusion dropped while shortening) | 장비가 재부팅되어 탐지<br>주기적으로 재부팅하는 백업 서버는 제외 |
| 다른 클라우드 룰에서 따로 탐지 | 위험도 7 이상은 `<rule name>` 룰에서 탐지 (name the rule) |
| 사용자 요청으로 삭제, 백업은 ops/... | 삭제 |

### E. Word Reports
Sentence endings are noun forms (`~함`, `~됨`, `~있음`, `~임`) with formal vocabulary. No spoken expressions.

| AI or Spoken Slop | Report Style |
| :--- | :--- |
| 막힘 없이 통과했다. 늦게 잡히거나 아예 잡히지 않았다. 2시간 먼저 봤다. | 차단 없이 통과되었음. 탐지가 지연되거나 누락되었음. 2시간 먼저 식별하였음. |
| 그래서 해당 IP를 차단했다. | 이에 따라 해당 IP를 차단함. |

### F. Tech Blogs and Essays
| AI Blog Slop | Natural Practitioner Blog Tone |
| :--- | :--- |
| 오늘 포스팅에서는 OOO에 대해 깊이 있게 알아보도록 하겠습니다. | 실무에서 OOO을 겪어보면 공식 문서대로만 되지 않을 때가 많다. (Start with a concrete experience) |
| 결론적으로 OOO은 현대 IT 환경에서 선택이 아닌 필수라고 할 수 있습니다. | 직접 써보니 OOO 상황에서는 확실히 편했다. 반대로 OOO할 때는 굳이 쓸 필요가 없었다. |
| 그렇다면 왜 이런 현상이 발생할까요? 정답은 바로 OOO에 있습니다! (Home-shopping host tone) | 원인은 의외로 단순했다. OOO 설정이 빠져 있었기 때문이다. |

## 6. 2026 Signals (`2026년 최신 신호`)

Sources: Graphite "AI Tells" study of Claude Opus 5.5 and GPT Astra against 10,000 pre-ChatGPT human articles (October 2026); The Economist study of 1.2M words from ChatGPT, Claude, Gemini, and Grok (2026); tropes.fyi catalog of AI writing tics (2026); Korean community reports on comma habits (2026); KAIST XDAC study on AI comments; the "load-bearing vocabulary of Claude" analysis of 467K GitHub PR descriptions (2026); Wikipedia "Signs of AI writing" (late 2026); Korean press and practitioner write-ups on "LLM 말투" and "클로드 말투" (2026). Older tells in sections 1 to 5 still apply.

### A. Contrast Frames (`대비 틀`, strongest signal)
| Bad | Good |
| :--- | :--- |
| 이건 단순한 설정 문제가 아니라 구조 문제입니다. | 구조 문제입니다. 설정을 바꿔도 같은 오류가 납니다. |
| 속도보다는 정확성이 중요합니다. | 정확성을 먼저 봅니다. |
| 이건 버그가 아닙니다. 설계입니다. | 의도한 동작입니다. 2024년 설계 문서에 같은 규칙이 있습니다. |
| 수집뿐만 아니라 분석까지 자동화합니다. | 수집과 분석을 자동화합니다. |
| 도구라기보다는 동료에 가깝습니다. | (delete, or say what it actually does) |

### A-2. Sentence Headings (`~다로 끝나는 제목`)
AI lifts a body sentence and uses it as a heading. Human Korean columns and articles end headings with a noun or a clipped newspaper ending.

| Bad | Good (noun form) | Good (newspaper style) |
| :--- | :--- | :--- |
| ## 컴퓨터 조작과 장기 작업에서 격차가 컸다 | ## 컴퓨터 조작과 장기 작업에서 가장 큰 격차 | ## 컴퓨터 조작, 장기 작업서 격차 커 |
| ## 긴 맥락에서 필요한 정보를 찾는 능력도 개선됐다 | ## 긴 맥락 속 정보 찾기 | ## 긴 맥락 정보 검색 개선 |
| ## 비용은 그대로 유지됐다 | ## 그대로인 비용 | ## 비용은 동결 |
| (every heading ends in 다: 컸다 / 개선됐다 / 유지됐다) | Mix noun headings, questions (`무엇이 달라졌나`), and topic labels (`처리 속도 비교`). | |

### B. Inflated Copulas (`꾸민 동사`)
| Bad | Good |
| :--- | :--- |
| 이 룰은 1차 필터로 기능합니다. | 이 룰은 1차 필터입니다. |
| 큐가 완충 역할을 합니다. | 큐가 갑자기 몰린 로그를 잠시 쌓아 둡니다. |
| 인증 서버가 구조의 중심에 자리합니다. | 모든 요청이 인증 서버를 거칩니다. |
| 프록시가 관문으로서 작동합니다. | 외부 요청은 모두 프록시를 지납니다. |

### C. Claude Signature Vocabulary (`Claude 말버릇`)
The English analysis found Claude-heavy words such as quietly, genuinely, plainly, deliberately, load-bearing, carries, rests, survived, asymmetry. They surface in Korean as follows.

| Bad | Good |
| :--- | :--- |
| 오류가 조용히 삼켜지고 있습니다. | 오류가 기록되지 않고 사라집니다. |
| 이 설정이 전체 구조를 떠받치고 있습니다. / 모든 룰이 이 필드에 얹혀 있습니다. | 이 설정을 바꾸면 전체가 영향을 받습니다. / 모든 룰이 이 필드를 씁니다. |
| 봐야 하는 자리는 두 곳입니다. / 세 번째 자리에서 갈립니다. | 확인할 곳은 두 곳입니다. / 세 번째 단계에서 결과가 달라집니다. |
| 두 축으로 정리하면 / 세 지식 | 두 가지 기준으로 나누면 / 세 가지 정보 |
| 두 지시는 결이 같습니다. | 두 지시는 같은 방향입니다. |
| 층위가 다릅니다. / 세 갈래로 나뉩니다. / 뼈대만 남깁니다. | 범위가 다릅니다. / 세 가지로 나뉩니다. / 핵심만 남깁니다. |
| 교차 확인했습니다. / 재검증했습니다. (as a credibility stamp) | 방화벽 로그와 WAF 로그를 비교했습니다. (say what was compared) |
| 솔직히 말하면 / 짚고 넘어가면 / 의도적으로 | (delete) |
| 조건을 박아 두었습니다. / 값을 얹었습니다. / 큐에 태웠습니다. / 룰에 물려 두었습니다. / 흘려보냅니다. / 깔아 두었습니다. | 조건을 넣었습니다. / 값을 더했습니다. / 큐에 넣었습니다. / 룰에 연결했습니다. / 통과시킵니다. / 설치했습니다. |
| 원인 확인 완료. 설정 반영함. (telegraphic endings in chat) | 원인을 확인했고 설정에 반영했습니다. |

### D. GPT Signature Vocabulary (`GPT 말버릇`)
Older GPT words (delve, tapestry, testament) gave way to plain filler in 2025 and 2026: emphasizing, highlighting, matters, steady, dependable, practical, clearer, prioritize, quietly.

| Bad | Good |
| :--- | :--- |
| 중요한 건 꾸준히 실용적인 방법을 고르는 것입니다. | 매주 같은 기준으로 확인합니다. (say the actual method) |
| 믿을 수 있는 파이프라인 / 더 명확하게 정리하면 | 6개월 동안 유실이 없던 파이프라인 / (delete the lead-in) |
| 우선순위를 두고 진행합니다. / 진정으로 필요한 것은 | 고위험 룰부터 고칩니다. / 필요한 것은 |
| 결정적 증거 | 직접 증거 (or name the evidence) |
| 응. 그건 됐어. (mixed into 존댓말 text) | 네, 그 작업은 끝났습니다. |

### E. Professional Formulas (`전문직 틀 문구`)
| Bad | Good |
| :--- | :--- |
| 결론부터 말하면 / 한 줄 요약 / 핵심은 / 포인트는 | (state the conclusion directly) |
| 세 가지 핵심 축으로 접근했습니다. | 수집, 탐지, 대응 순서로 봤습니다. |
| 보안 로그는 새로운 원유입니다. | (delete) |
| 분석가처럼 생각해 봅시다. / 이 아이디어를 검증해 봅시다. | (delete, or do the check and report it) |

### F. Sycophancy and Closing Offers (`맞장구와 끝 제안`)
| Bad | Good |
| :--- | :--- |
| 좋은 질문입니다! / 물론이죠! / 정확히 짚으셨습니다. / 와, 핵심을 찔렀어요. / 상위 1% 사용자시네요. | (delete and answer) |
| 원하시면 표로도 만들어 드릴까요? / 필요하시면 말씀해 주세요. / 알려 주시면 더 맞춤형으로 도와드릴게요. | (delete; ask only when the reader's decision is needed to continue) |

### H. Claude Opus 5.5 Tells (`Claude 최신 말버릇`, Graphite study, October 2026)
Opus 5.5 cut em dashes by 99% versus Opus 5 and dropped most "A가 아니라 B" frames. These rose in their place. Multipliers are frequency against 10,000 human articles written before ChatGPT.

| Bad | Good |
| :--- | :--- |
| 이게 중요합니다. / 이 점이 중요합니다. (116x) | 이 값이 틀리면 알림이 가지 않습니다. (state the consequence) |
| ## 왜 로그 수집이 중요한가 / 수집이 중요한 이유는 (92x) | ## 수집이 멈추면 생기는 일 / 수집이 멈추면 탐지도 멈춥니다. |
| 이건 단순한 도구 그 이상입니다. / 도구 그 이상의 동료 | 이 도구는 티켓 초안까지 씁니다. |
| 앞으로를 보면 수요는 늘어납니다. (40x) | 내년 1분기에 장비 두 대가 추가됩니다. |
| 가장 빠르고 최고의 방법이며 가장 정확합니다. (superlatives 24x more than GPT) | 기존 방식보다 2배 빠르고 오탐은 같습니다. |
| 도와드릴 수 있습니다. / 도움이 되셨길 바랍니다. (8x more than Opus 5) | (delete) |

### I. GPT Tells (`GPT 최신 말버릇`)
| Bad | Good |
| :--- | :--- |
| 이 결과가 원인을 입증하지는 않는다. / 침해라고 단정할 수는 없다. (275x more than Claude) | 이 결과로는 원인을 알 수 없다. 접속 기록만 남아 있다. (say once what is and is not known) |
| 정상 트래픽과 혼동해서는 안 된다. / 이 값은 지표로 봐야 한다. | 정상 트래픽과 포트가 다르다. / 이 값은 지표다. |
| 또 다른 차원의 문제 / 가시성을 제공할 수 있다. | 별개의 문제 / 접속 기록을 보여 준다. |

### J. Rhetorical Tics (`수사 버릇`, tropes.fyi and Wikipedia 2026)
| Bad | Good |
| :--- | :--- |
| 원인은? 설정 누락이었다. | 원인은 설정 누락이었다. |
| 버그도 아니고 장애도 아니다. 설계다. | 의도한 설계다. |
| 이유는 세 가지입니다. 첫째... | (list the reasons directly) |
| 이것이 자동화의 함정이다. / 정확도 역설 | 자동화하면 예외 처리가 빠진다. (describe the problem) |
| 전문가들은 이 방식을 권한다. / 업계에서는 / 많은 연구에 따르면 | OOO 가이드는 이 방식을 권한다. (name the real source) or delete |
| 결국 보안은 사람의 문제다. (standalone line) / 그게 전부다. | (delete or merge into the paragraph) |
| 이 설정은 config 파일에 산다. | 이 설정은 config 파일에 있다. |
| 하나씩 뜯어보겠습니다. / 쉽게 말해 문지기라고 생각하면 됩니다. / 상상해 보세요. | (explain directly) |
| 이 수치는 운영이 안정적이라는 점을 보여준다. | 이 수치는 지난달과 같다. (let the fact stand) |
| 정리하자면 / 한마디로 / 다시 처음 질문으로 돌아가면 | (delete; one summary at most) |
| 우리는 먼저 수집한다. 우리가 정한 기준이다. (one author) | 보안팀은 먼저 수집한다. 팀이 정한 기준이다. |
| ## 왜 ~인가 / ## 무엇이 ~인가 / ## 어떻게 ~하는가 (every heading) | Mix noun headings and topic labels; keep at most one question heading. |

### K. Korean Commas After Connective Endings (`연결어미 뒤 쉼표`)
English AI text uses fewer commas than humans. Korean AI text does the opposite: it puts a comma after connective endings, which Korean writers rarely do. Korean readers call this out as an AI giveaway.

| Bad | Good |
| :--- | :--- |
| 로그를 확인했고, 결과를 정리하며, 메일로 보냈다. | 로그를 확인하고 결과를 정리해 메일로 보냈다. |
| 차단은 했지만, 같은 IP가 다시 들어왔는데, 이번엔 우회했다. | 차단은 했다. 그런데 같은 IP가 우회해서 다시 들어왔다. |

Short comments and messenger text: AI uses formal endings (`~것 같습니다`, `~에 대해`) and almost no line breaks or casual marks. Match the team's actual register.

### L. Leftovers (`남은 흔적`)
| Bad | Good |
| :--- | :--- |
| [날짜]에 [회사명]으로 보낸다. / 2026-XX-XX / PASTE_URL_HERE / example.com/source1 | Fill in the real value or delete the sentence. |
| https://a.com/x?utm_source=chatgpt.com / contentReference[oaicite:1] / ↩ | https://a.com/x |
| 기존 구조는 그대로 유지했습니다. / 중립성을 지켰습니다. / 모든 내용 검증 완료. | 2장에 수집 지연 원인을 추가했습니다. (say what changed) |
| “안정성”을 높인다. (curly quotes) | 안정성을 높인다. |

### G. Source-Leaning (`출처에 기댄 판단`)
| Bad | Good |
| :--- | :--- |
| 공식 문서에 따르면 정상 요청으로 확인됩니다. (the document never says so) | 요청 경로와 응답 코드가 평소 정상 요청과 같습니다. |
| 원인은 확인되지 않았지만, 이는 구조적 문제를 시사합니다. | 원인은 아직 확인하지 못했습니다. 같은 오류가 세 서버에서 났습니다. |
| 위협 인텔리전스 DB가 해당 IP를 스캐너로 식별합니다. (as a stand-in for your own analysis) | 이 IP는 한 시간 동안 포트 2천 개에 접속했습니다. 위협 정보 DB에도 스캐너로 올라 있습니다. |
