from django.test import TestCase
from .models import BookRecommendation
from .services.book_scraper import BookScraper
from django.utils.timezone import now as timezone_now
from django.core.exceptions import ValidationError
from unittest.mock import patch, MagicMock

class BookScraperTest(TestCase):
    
    def setUp(self):
        self.book_recommendation = BookRecommendation.objects.create(
            author="Test Author",
            date=timezone_now(),
            content="Test Content",
            url="https://testurl.com",
            created_at=timezone_now()
        )

    def test_book_recommendation_fields(self):
        invalid_book = BookRecommendation(author="", date=None, content="", url="")
        with self.assertRaises(ValidationError):
            invalid_book.full_clean()

    def test_book_recommendation_creation(self):
        book = BookRecommendation.objects.get(author="Test Author")
        self.assertEqual(book.author, "Test Author")
        self.assertEqual(book.content, "Test Content")
        self.assertEqual(book.url, "https://testurl.com")
        self.assertIsNotNone(book.created_at)

    def test_book_recommendation_str(self):
        book = BookRecommendation.objects.get(author="Test Author")
        expected_str = "Test Author - Test Content..."
        self.assertEqual(str(book), expected_str)


#Test scraper:

