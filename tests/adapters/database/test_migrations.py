from alembic.command import upgrade
from alembic.config import Config as AlembicConfig
from alembic.script import ScriptDirectory
from sqlalchemy.ext.asyncio import AsyncEngine

from mrfixit.adapters.database.tables import BaseTable
from tests.utils import get_diff_db_metadata


async def test_migrations_up_to_date(engine: AsyncEngine) -> None:
    async with engine.connect() as connection:
        diff = await connection.run_sync(
            get_diff_db_metadata,
            metadata=(BaseTable.metadata,),
        )
    assert not diff


def test_migrations_apply_step_by_step(
    alembic_config: AlembicConfig,
    engine: AsyncEngine,
) -> None:
    script = ScriptDirectory.from_config(alembic_config)
    revisions = list(script.walk_revisions(base="base", head="heads"))
    revisions.reverse()
    for revision in revisions:
        upgrade(alembic_config, revision.revision)
    assert True
