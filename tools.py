from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

@tool
def search_web(query: str) -> str:
    """ウェブ検索を行います。"""
    search_tool = DuckDuckGoSearchRun()
    results = search_tool.run(query)
    return f"検索結果: {results[:500]}..."  # 最初の500文字だけ返す