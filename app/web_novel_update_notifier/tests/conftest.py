import datetime
import os
import tempfile
import pytest
from web_novel_update_notifier.lib.novel_table import NovelTable

@pytest.fixture(scope='function', autouse=True)
def NovelTableMock():
    _, tmpfile = tempfile.mkstemp()

    novel_table_mock = NovelTable(file_path=tmpfile)

    item = {
        'domain': 'example.com',
        'title': 'hoge',
        'author': 'fuga',
        'novel_id': '00000',
        'updated_at': datetime.datetime(2000, 1, 1, 0, 0),
        'latest_url': 'https://example.com/novel/00000/1.html'
    }

    novel_table_mock.insert_novel(item)

    yield NovelTable(file_path=tmpfile)

    os.remove(tmpfile)
