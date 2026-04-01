프로젝트명: QuantAI Flux (macOS Desktop App)

1. 개요 (Objective)

한국투자증권 오픈 API 명세와 구글 뉴스 RSS, Gemini AI 분석 기능을 통합하여 KOSPI 200 및 KOSDAQ 100 종목의 투자 매력도를 실시간으로 산출하고, 이를 시각적인 네트워크 그래프(Mind Map) 형태로 제공하는 전문가용 주식 스캐닝 도구 개발.

2. 주요 타겟 유저 (Target Audience)

실시간 수급 및 기술적 추세를 한눈에 파악하고자 하는 퀀트 투자자.

수많은 뉴스 및 공시 데이터를 AI로 빠르게 요약 분석받고 싶은 개인 투자자.

Obsidian 스타일의 데이터 시각화를 선호하는 기술 지향적 유저.

3. 핵심 기능 (Core Features)

3.1 실시간 데이터 모니터링 (KIS API Mocking)

필드 동기화: 한국투자증권 API 명세에 따른 stck_prpr(현재가), prdy_ctrt(등락률) 등을 반영.

실시간 업데이트: 5초 간격의 폴링(Polling)을 통해 주가 및 지수 변동 반영.

3.2 기술적 추세 분석 (Trend Analysis)

주봉 기반 이평선: 주봉 5일 이동평균선(MA5)과 20일 이동평균선(MA20) 실시간 계산.

크로스 시그널: 골든크로스(MA5 상향 돌파) 및 데드크로스 발생 시 점수 가중치 부여 및 알림.

3.3 AI 센티먼트 분석 (Gemini AI Integration)

구글 RSS 피드: 종목별 검색 결과를 바탕으로 한 실시간 뉴스 수집.

감성 점수 산출: Gemini 2.5 Flash를 활용해 뉴스 및 DART 공시 내용을 -5 ~ +5 점수로 수치화.

3.4 인터랙티브 시각화 (Obsidian-style Mind Map)

포스 디렉티드 그래프: 시장 -> 섹터 -> 종목으로 이어지는 물리 기반 네트워크망 구현.

랭킹 시스템: 종합 점수 기준 실시간 순위 산출 및 상위 종목 시각적 강조(Aura 효과).

3.5 상세 정보 탭 시스템

인사이트: 점수 산정 근거 요약 요약 설명.

뉴스: 구글 뉴스 검색 결과와 연결되는 링크 리스트.

공시: DART 스타일의 공시 보고서 목록.

추세: 이평선 수치 및 기술적 해석 제공.

4. 기술 스택 (Technical Stack)

Framework: Flutter (macOS Desktop 전용)

Language: Dart

AI/Search: Google Gemini API + Google News Search Grounding

UI: Material 3 (Custom Dark Theme), CustomPainter (Graph Engine)

5. 데이터 구조 (Mocking Specification)

Stock Model: code, name, sector, stck_prpr, prdy_ctrt, ma5, ma20, totalScore.

Log Model: 고유 ID 기반의 실시간 시스템 로그 적재.
