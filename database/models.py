from sqlalchemy import BigInteger, VARCHAR, Integer, BOOLEAN, ARRAY, DATE, TIME
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


###TEMPLATE###
#class Nane(Base):
#   __tablename__ = "test"





class Test(Base):
    __tablename__ = "test"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True)
    username: Mapped[str] = mapped_column(VARCHAR(100), nullable=True)

class Users(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True,  nullable=False)
    first_name: Mapped[str] = mapped_column(VARCHAR(25))
    last_name: Mapped[str] = mapped_column(VARCHAR(25))
    username: Mapped[str] = mapped_column(VARCHAR(25))
    language_code: Mapped[str] = mapped_column(VARCHAR(5))
    is_bot: Mapped[bool] = mapped_column(BOOLEAN)
    is_premium: Mapped[bool] = mapped_column(BOOLEAN)
    chat_id: Mapped[int] = mapped_column(Integer, nullable=False)
    chat_type: Mapped[str] = mapped_column(VARCHAR(15))


class MasterTemplates(Base):
    __tablename__ = "master_templates"

    id_template: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    master_id: Mapped[int] = mapped_column(Integer, nullable=False)
    name_template: Mapped[str] = mapped_column(VARCHAR(25), nullable=False)
    is_main: Mapped[bool] = mapped_column(BOOLEAN, default=False)
    callback_key: Mapped[str] = mapped_column(VARCHAR(20), default="edit_template_")
    time_template: Mapped[list[str]] = mapped_column(ARRAY(VARCHAR(5)), nullable=False)


class OpenSign(Base):
    __tablename__ = "open_sign"

    id_sign: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    master_id: Mapped[int] = mapped_column(Integer, nullable=False)
    date: Mapped[str] = mapped_column(DATE, nullable=False)
    time: Mapped[str] = mapped_column(TIME, nullable=False)

    def toDict(self):
        pass