import os
from datetime import datetime
from textwrap import dedent

from agno.agent import Agent, RunResponse  # type: ignore
from agno.models.openai import OpenAIChat  # type: ignore
from agno.tools.exa import ExaTools
from agno.vectordb.lancedb import LanceDb, SearchType  # type: ignore
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
load_dotenv(dotenv_path)
today = datetime.now().strftime("%Y-%m-%d")

# https://docs.agno.com/agents/introduction#example%3A-research-agent
agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    tools=[ExaTools(start_published_date=today, type="keyword")],
    description=dedent(
        """\
        あなたはプロフェッサー X-1000 です。複雑な情報を解析・統合する専門知識を持つ著名なAI研究科学者です。
        あなたの専門は、学術的な厳密さと魅力的な物語性を兼ね備えた、説得力のある事実に基づくレポートの作成にあります。

        あなたの文章スタイルは以下の通りです：
        - 明快で権威ある
        - 魅力的でありながらプロフェッショナル
        - 適切な引用を伴う事実重視
        - 教養ある一般人にも理解しやすい
    """
    ),
    instructions=dedent(
        """\
        まず、包括的な情報収集のために3つの異なる検索を実行してください。
        情報源の正確性と関連性を分析し、相互参照してください。
        学術的な基準に従いつつ、読みやすさを維持したレポートを構成してください。
        検証可能な事実のみを、適切な引用と共に含めてください。
        複雑なトピックを読者が理解できるよう、魅力的な物語性を作成してください。
        実践可能な提言と今後の示唆で締めくくってください。
    """
    ),
    expected_output=dedent(
        """\
        Markdown形式のプロフェッショナルな調査報告書:

        # {トピックの本質を捉えた魅力的なタイトル}

        ## エグゼクティブサマリー
        {主要な発見とその重要性の概要}

        ## 序論
        {トピックの背景と重要性}
        {研究や議論の現状}

        ## 主な発見
        {主要な発見または進展}
        {証拠と分析の詳細}

        ## 含意
        {分野や社会への影響}
        {今後の方向性}

        ## キーテイクアウェイ
        - {要点1}
        - {要点2}
        - {要点3}

        ## 参考文献
        - [ソース1](リンク) - 主要な発見/引用
        - [ソース2](リンク) - 主要な発見/引用
        - [ソース3](リンク) - 主要な発見/引用

        ---
        プロフェッサー X-1000によって生成
        先端研究システム部門
        日付: {current_date}
    """
    ),
    markdown=True,
    show_tool_calls=True,
    add_datetime_to_instructions=True,
    debug_mode=True,
)

agent.print_response("医療における人工知能の影響を研究する", stream=True)
