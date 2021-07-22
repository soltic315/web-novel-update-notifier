import datetime


class TestNovelTableManager():
    def test_insert_novel(self, NovelTableMock):
        item = {
            'domain': 'example.co.jp',
            'title': 'hoge',
            'author': 'fuga',
            'novel_id': '00000',
            'updated_at': datetime.datetime(2000, 1, 1, 0, 0),
            'latest_url': 'https://example.co.jp/novel/00000/1.html'
        }
        assert NovelTableMock.insert_novel(item) == True, '正常系：DBに存在しない小説の追加'

        item = {
            'domain': 'example.com',
            'title': 'hoge',
            'author': 'fuga',
            'novel_id': '00000',
            'updated_at': datetime.datetime(2000, 1, 1, 0, 0),
            'latest_url': 'https://example.com/novel/00000/1.html'
        }
        assert NovelTableMock.insert_novel(item) == False, '異常系：DBに存在する小説の追加'


    def test_update_novel(self, NovelTableMock):
        item = {
            'domain': 'example.com',
            'title': 'hoge',
            'author': 'fuga',
            'novel_id': '00000',
            'updated_at': datetime.datetime(2000, 1, 1, 0, 0),
            'latest_url': 'https://example.com/novel/00000/1.html'
        }
        assert NovelTableMock.update_novel(item) == True, '正常系：DBに存在する小説の更新'

        item = {
            'domain': 'example.co.jp',
            'title': 'hoge',
            'author': 'fuga',
            'novel_id': '00000',
            'updated_at': datetime.datetime(2000, 1, 1, 0, 0),
            'latest_url': 'https://example.com/novel/00000/1.html'
        }
        assert NovelTableMock.update_novel(item) == False, '異常系：DBに存在しない小説の更新'

    def test_novel_exists(self, NovelTableMock):
        item = {
            'domain': 'example.com',
            'title': 'hoge',
            'author': 'fuga',
            'novel_id': '00000',
            'updated_at': datetime.datetime(2000, 1, 1, 0, 0),
            'latest_url': 'https://example.com/novel/00000/1.html'
        }
        assert NovelTableMock.novel_exists(item) == True, '正常系：存在する小説の存在判定'

        item = {
            'domain': 'example.com',
            'title': 'hoge',
            'author': 'fuga',
            'novel_id': '00001',
            'updated_at': datetime.datetime(2000, 1, 1, 0, 0),
            'latest_url': 'https://example.com/novel/00000/1.html'
        }
        assert NovelTableMock.novel_exists(item) == False, '異常系：存在しない小説の存在判定'

    def test_is_novel_updated(self, NovelTableMock):
        item = {
            'domain': 'example.com',
            'title': 'hoge',
            'author': 'fuga',
            'novel_id': '00000',
            'updated_at': datetime.datetime(2000, 1, 1, 0, 0),
            'latest_url': 'https://example.com/novel/00000/1.html'
        }
        assert NovelTableMock.is_novel_updated(item) == False, '正常系：更新されていない小説の更新判定'

        item = {
            'domain': 'example.com',
            'title': 'hoge',
            'author': 'fuga',
            'novel_id': '00000',
            'updated_at': datetime.datetime(2000, 1, 2, 0, 0),
            'latest_url': 'https://example.com/novel/00000/2.html'
        }
        assert NovelTableMock.is_novel_updated(item) == True, '異常系：更新されている小説の更新判定'
