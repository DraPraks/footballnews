from django.test import TestCase, Client
from .models import News
from django.contrib.auth.models import User


class MainTest(TestCase):
  def test_main_url_is_exist(self):
    # Without login, should redirect to login due to @login_required
    response = Client().get('')
    self.assertIn(response.status_code, (302, 301))

  def test_main_using_main_template(self):
    # Login first
    User.objects.create_user(username='tester', password='pass12345')
    c = Client()
    c.login(username='tester', password='pass12345')
    response = c.get('')
    self.assertTemplateUsed(response, 'main.html')

  def test_nonexistent_page(self):
    response = Client().get('/burhan_always_exists/')
    self.assertEqual(response.status_code, 404)

  def test_news_creation(self):
    news = News.objects.create(
      title="BURHAN FC WINS",
      content="BURHAN FC 1-0 PANDA BC",
      category="match",
      news_views=1001,
      is_featured=True,
    )
    self.assertTrue(news.is_news_hot)
    self.assertEqual(news.category, "match")
    self.assertTrue(news.is_featured)

  def test_news_default_values(self):
    news = News.objects.create(
      title="Test News",
      content="Test content",
    )
    self.assertEqual(news.category, "update")
    self.assertEqual(news.news_views, 0)
    self.assertFalse(news.is_featured)
    self.assertFalse(news.is_news_hot)

  def test_increment_views(self):
    news = News.objects.create(
      title="Test News",
      content="Test content",
    )
    initial_views = news.news_views
    news.increment_views()
    self.assertEqual(news.news_views, initial_views + 1)

  def test_is_news_hot_threshold(self):
    # Test news with exactly 20 views (should not be hot)
    news_20 = News.objects.create(
      title="News with 20 views",
      content="Test content",
      news_views=20,
    )
    self.assertFalse(news_20.is_news_hot)

    # Test news with 21 views (should be hot)
    news_21 = News.objects.create(
      title="News with 21 views",
      content="Test content",
      news_views=21,
    )
    self.assertTrue(news_21.is_news_hot)