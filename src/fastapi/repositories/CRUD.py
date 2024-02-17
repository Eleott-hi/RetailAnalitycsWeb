from database.Database import get_db
from dataclasses import dataclass, field


@dataclass
class Operations:
    selects: list = field(default_factory=list)
    filters: list = field(default_factory=list)
    orders_by: list = field(default_factory=list)
    limit: int = None
    offset: int = 0

    def perform(self, q):
        if len(self.selects) > 0:
            q = q.select(*self.selects)
        for f in self.filters:
            q = q.filter(f)

        for o in self.orders_by:
            q = q.order_by(o)

        q = q.offset(self.offset)

        if self.limit:
            q = q.limit(self.limit)

        return q


def all(cls: type, operations: Operations = Operations()) -> list[any]:
    with get_db() as session:
        return operations.perform(session.query(cls)).all()


def one(cls: type, operations: Operations = Operations()) -> any:
    with get_db() as session:
        return operations.perform(session.query(cls)).first()


def create(cls: type, **kwargs) -> any:
    with get_db() as session:
        item = cls(**kwargs)
        session.add(item)
        session.commit()
        session.refresh(item)
        return item


def update(cls: type, operations: Operations = Operations(), **kwargs) -> any:
    with get_db() as session:
        item = operations.perform(session.query(cls)).first()

        for key, value in kwargs.items():
            setattr(item, key, value)

        session.commit()
        session.refresh(item)

        return item


def delete(cls: type, operations: Operations = Operations()) -> str:
    with get_db() as session:
        item = operations.perform(session.query(cls)).first()
        item.delete()
        session.commit()
        return "Deleted !"
