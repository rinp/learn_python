from uuid import UUID, uuid1

from sqlalchemy import ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .author import Author
from .base import Base
from .constants import BOOK_TITLE_MAX_LENGTH


class Book(Base):
    """書籍を表す ORM モデル

    Attributes:
        id (UUID): 書籍の一意な識別子
        title (str): 書籍タイトル
        author_id (UUID): 著者の ID（外部キー）
        author (Author): 著者オブジェクト（リレーション）
    """

    __tablename__ = "Books"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid1)
    title: Mapped[str] = mapped_column(String(BOOK_TITLE_MAX_LENGTH), nullable=False)
    # 現状で著者の削除を想定しない、また書籍登録時には必ず著者を含めるため、
    # 実情に合わせてNOT NULL制約は付与
    author_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("Authors.id"), index=True, nullable=False
    )

    author: Mapped[Author] = relationship(
        "Author", back_populates="books", lazy="joined"
    )
