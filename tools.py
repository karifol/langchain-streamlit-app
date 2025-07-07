from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
import json

@tool
def search_web(query: str) -> str:
    """
    DuckDuckGoでウェブ検索を行い、BoothのHPから衣装の情報を取得します。
    Args:
        query (str): 検索クエリ 衣装を探したいアバターの名前
    Returns:
        str: 検索結果の要約
    Description:
        このツールは、DuckDuckGoを使用してウェブ検索を行い、指定されたクエリに関連する情報を取得します。
        取得先は以下のBoothのHPです。
        https://booth.pm/ja
    """
    search_tool = DuckDuckGoSearchRun()
    results = search_tool.run(query)
    return f"検索結果: {results[:500]}..."  # 最初の500文字だけ返す