from unittest import TestCase
from unittest import mock

from django.test import override_settings as override_django_settings

from collectfasta.tests.utils import clean_static_dir
from collectfasta.tests.utils import create_static_file
from collectfasta.tests.utils import live_test
from collectfasta.tests.utils import make_test
from collectfasta.tests.utils import override_setting

from .utils import call_collectstatic


@make_test
@override_django_settings(
    STORAGES={
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    },
)
def test_disable_collectfasta_with_default_storage(case: TestCase) -> None:
    clean_static_dir()
    create_static_file()
    case.assertIn("1 static file copied", call_collectstatic(disable_collectfasta=True))


@make_test
@live_test
def test_disable_collectfasta(case: TestCase) -> None:
    clean_static_dir()
    create_static_file()
    case.assertIn(
        "1 static file copied.", call_collectstatic(disable_collectfasta=True)
    )


@override_setting("enabled", False)
@mock.patch("collectfasta.management.commands.collectstatic.Command._load_strategy")
def test_no_load_with_disable_setting(mocked_load_strategy: mock.MagicMock) -> None:
    clean_static_dir()
    call_collectstatic()
    mocked_load_strategy.assert_not_called()


@mock.patch("collectfasta.management.commands.collectstatic.Command._load_strategy")
def test_no_load_with_disable_flag(mocked_load_strategy: mock.MagicMock) -> None:
    clean_static_dir()
    call_collectstatic(disable_collectfasta=True)
    mocked_load_strategy.assert_not_called()