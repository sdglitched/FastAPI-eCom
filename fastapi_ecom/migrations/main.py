from typing import List, Set

from alembic import command, config, runtime, script

from fastapi_ecom.database import get_database_url, migrpath


class AlembicMigration:
    """
    A class to manage Alembic-based database migrations.

    This class provides methods to create new migration scripts, retrieve the current database
    version, and upgrade or downgrade the database schema.

    :ivar _config: The Alembic configuration object, initialized lazily.
    """

    @property
    def config(self) -> config.Config:
        """
        Lazy-loaded Alembic configuration object.

        :return: The Alembic configuration with migration paths and database URL set.
        """
        if not hasattr(self, "_config"):
            self._config = config.Config()
            self._config.set_main_option("script_location", migrpath)
            self._config.set_main_option("sqlalchemy.url", get_database_url().render_as_string(hide_password=False))
        return self._config

    def create(self, comment: str, autogenerate: bool) -> None:
        """
        Create a new migration script.

        :param comment: A descriptive comment for the migration script.
        :param autogenerate: Whether to automatically generate the schema changes.

        :return: None
        """
        command.revision(config=self.config, message=comment, autogenerate=autogenerate)

    def _get_current(self) -> Set[str]:
        """
        Retrieve the current database revision(s).

        :return: A set of current database revision(s).
        """
        scrtobjc = script.ScriptDirectory.from_config(self.config)

        curtrevs = set()

        def _get_rev_current(rev: str, context: object) -> List:
            """
            Callback function to retrieve the current revision(s) during the migration check.

            :param rev: The revision identifier being processed.
            :param context: The context in which the script is being run (usually an Alembic
                            environment). By specifying type as object, the function signature is
                            flexible enough to accept any type as it not directly used here.

            :return: An empty list as required by the Alembic environment context callback.
            """
            curtrevs.update(
                _rev.cmd_format(verbose=False) for _rev in scrtobjc.get_all_current(rev)
            )
            return []

        with runtime.environment.EnvironmentContext(
            self.config, scrtobjc, fn=_get_rev_current, dont_mutate=True
        ):
            scrtobjc.run_env()

        return curtrevs

    def db_version(self) -> None:
        """
        Print the current database version(s).

        This method retrieves and displays the current database revision(s).

        :return: None
        """
        print(self._get_current())

    def upgrade(self, version: str) -> None:
        """
        Upgrade the database to a specified revision.

        :param version: The target database revision, e.g., "head" or a specific revision ID.

        :return: None
        """
        pre_revs = self._get_current()
        command.upgrade(self.config, version)
        post_revs = self._get_current()
        if pre_revs == post_revs:
            print("There is nothing to upgrade.")
        else:
            print("Upgraded to: ", post_revs)

    def downgrade(self, version: str) -> None:
        """
        Downgrade the database to a specified revision.

        :param version: The target database revision, e.g., "base" or a specific revision ID.

        :return: None
        """
        pre_revs = self._get_current()
        command.downgrade(self.config, version)
        post_revs = self._get_current()
        if pre_revs == post_revs:
            print("There is nothing to downgrade.")
        else:
            print("Downgraded to:", post_revs if post_revs else '<base>')


# Instantiate the AlembicMigration class for use in managing migrations.
alembic_migration = AlembicMigration()
