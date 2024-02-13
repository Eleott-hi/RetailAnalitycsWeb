import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import create_engine, Column, Integer, String, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)


engine_sync = create_engine('sqlite:///example_sync.db', echo=False)
SessionSync = sessionmaker(bind=engine_sync)

engine_async = create_async_engine(
    'sqlite+aiosqlite:///example_async.db', echo=False)
async_session = sessionmaker(
    engine_async, class_=AsyncSession, expire_on_commit=False)


time_sync = 0
time_async = 0
N = 10000


def init_sync():
    data = []

    for i in range(N):
        data += [User(name='Alice'), User(name='Bob'), User(name='Charlie')]

    Base.metadata.create_all(engine_sync)

    with SessionSync() as session:
        session.add_all(data)
        session.commit()


async def init_async():
    data = []

    for i in range(N):
        data += [User(name='Alice'), User(name='Bob'), User(name='Charlie')]

    async with engine_async.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        async with session.begin():
            session.add_all(data)
        await session.commit()


def main_sync():
    global time_sync

    start_time = time.time()

    with SessionSync() as session:
        users = session.execute(select(User)).scalars().all()
        # print("Users:")
        # for user in users:
            # print(user.id, user.name)

    time_sync += time.time() - start_time


async def main_async():
    global time_async

    start_time = time.time()

    async with async_session() as session:
        async with session.begin():
            stmt = select(User)
            result = await session.execute(stmt)
            users = result.scalars().all()
            # print("Users:")
            # for user in users:
                # print(user.id, user.name)

    time_async += time.time() - start_time


async def run_async(r: int):
    for i in range(r):
        await main_async()


def main():
    R = 10

    init_sync()
    asyncio.run(init_async())

    for i in range(R):
        main_sync()

    asyncio.run(asyncio.gather(*[main_async() for i in range(R)]))

    print(f"\nTime sync: {time_sync}\nTime async: {time_async}")


main()