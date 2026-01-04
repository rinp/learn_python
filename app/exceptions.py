"""独自例外を定義するモジュール"""

from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True)
class NotFoundBookException(Exception):
    """書籍の取得失敗向け例外

    Attributes:
        book_id (UUID): 見つからなかった書籍の ID
    """

    book_id: UUID

    def __str__(self) -> str:
        return f"書籍が見つかりませんでした [id: {self.book_id}]"


@dataclass(slots=True)
class NotFoundAuthorException(Exception):
    """著者の取得失敗向け例外

    Attributes:
        author_id (UUID): 見つからなかった著者の ID
    """

    author_id: UUID

    def __str__(self) -> str:
        return f"著者が見つかりませんでした [id: {self.author_id}]"
