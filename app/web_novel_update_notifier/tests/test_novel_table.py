import datetime


class TestNovelTable():
    def test_novel_exists(self, NovelTableMock):
        item = {
            'domain': 'example.com',
            'title': 'hoge',
            'author': 'fuga',
            'novel_id': '00000',
            'updated_at': datetime.datetime(2000, 1, 1, 0, 0),
            'latest_url': 'https://example.com/novel/00000/1.html'
        }
        assert NovelTableMock.novel_exists(item) == True

        item = {
            'domain': 'example.com',
            'title': 'hoge',
            'author': 'fuga',
            'novel_id': '00001',
            'updated_at': datetime.datetime(2000, 1, 1, 0, 0),
            'latest_url': 'https://example.com/novel/00000/1.html'
        }
        assert NovelTableMock.novel_exists(item) == False

    def test_is_novel_updated(self, NovelTableMock):
        item = {
            'domain': 'example.com',
            'title': 'hoge',
            'author': 'fuga',
            'novel_id': '00000',
            'updated_at': datetime.datetime(2000, 1, 1, 0, 0),
            'latest_url': 'https://example.com/novel/00000/1.html'
        }
        assert NovelTableMock.is_novel_updated(item) == False

        item = {
            'domain': 'example.com',
            'title': 'hoge',
            'author': 'fuga',
            'novel_id': '00000',
            'updated_at': datetime.datetime(2000, 1, 2, 0, 0),
            'latest_url': 'https://example.com/novel/00000/2.html'
        }
        assert NovelTableMock.is_novel_updated(item) == True
