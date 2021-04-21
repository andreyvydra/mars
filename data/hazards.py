import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Hazards(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'hazards'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    jobs = orm.relation('Jobs', back_populates='hazards')

