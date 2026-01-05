"""テスト用の PyTest 設定とフィクスチャを提供するモジュール"""

import pytest

from app.database import engine
from app.models.base import Base


@pytest.fixture(scope="module")
def setup_database():
    """DBの初期化(全体)
    setup_database で テーブルを担う fixture
    """
    # 前処理：全テーブルを作成
    Base.metadata.create_all(bind=engine)

    yield

    # 後処理：テーブルを全て削除
    Base.metadata.drop_all(bind=engine)
