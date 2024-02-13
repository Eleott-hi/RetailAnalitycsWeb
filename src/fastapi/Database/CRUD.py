from Database.Database import get_db


def base_filter(q): return q


def all(cls: type, filter: callable = base_filter) -> list[any]:
    with get_db() as session:
        return filter(session.query(cls)).all()


def get(cls: type, filter: callable = base_filter) -> any:
    with get_db() as session:
        item = filter(session.query(cls)).first()
        return item


def create(cls: type, **kwargs) -> any:
    with get_db() as session:
        item = cls(**kwargs)
        session.add(item)
        session.commit()
        session.refresh(item)
        return item


def update(cls: type, filter: callable = base_filter, **kwargs) -> any:
    with get_db() as session:
        item = filter(session.query(cls)).first()

        for key, value in kwargs.items():
            setattr(item, key, value)

        session.commit()
        session.refresh(item)

        return item


def delete(cls: type, filter: callable = base_filter) -> str:
    with get_db() as session:
        item = filter(session.query(cls)).first()
        item.delete()
        session.commit()
        return "Deleted !"
