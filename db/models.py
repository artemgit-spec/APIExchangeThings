import uuid
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Admin(Base):
    __tablename__ = "admin_table"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String)


class User(Base):
    __tablename__ = "user_table"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String)

    my_thing = relationship("Thing", back_populates="user")
    sent_deal = relationship(
        "Deal", foreign_keys="[Deal.sender_id]", back_populates="sender"
    )  # сделки, созданные мной
    received_deals = relationship(
        "Deal", foreign_keys="[Deal.receiver_id]", back_populates="receiver"
    )  # сделки, направленые мне


class Thing(Base):
    __tablename__ = "thing_table"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    date_added = Column(DateTime, nullable=False)
    identifier = Column(String, unique=True, default=lambda: str(uuid.uuid4()))

    user_id = Column(Integer, ForeignKey("user_table.id"))
    user = relationship("User", back_populates="my_thing")


class Deal(Base):
    __tablename__ = "deal_table"

    id = Column(Integer, primary_key=True)

    id_my_thing = Column(Integer, ForeignKey("thing_table.id"), nullable=False)
    id_thing_exchange = Column(Integer, ForeignKey("thing_table.id"), nullable=False)

    answer_user = Column(Boolean)
    begin_exchange = Column(DateTime)
    end_exchange = Column(DateTime)

    my_thing = relationship("Thing", foreign_keys=[id_my_thing])
    exchange_thing = relationship("Thing", foreign_keys=[id_thing_exchange])

    sender_id = Column(
        Integer, ForeignKey("user_table.id"), nullable=False
    )  # кто предложил
    receiver_id = Column(
        Integer, ForeignKey("user_table.id"), nullable=False
    )  # кому предложили

    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_deal")
    receiver = relationship(
        "User", foreign_keys=[receiver_id], back_populates="received_deals"
    )
