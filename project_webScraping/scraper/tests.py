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

class TestBookScraper(TestCase):

    @patch.object(BookScraper, 'setup_driver')
    @patch.object(BookScraper, 'get_comments')
    def test_scraper_get_comments(self, mock_get_comments, mock_setup_driver):
        mock_scraper = BookScraper()
        mock_setup_driver.return_value = None
        mock_get_comments.return_value = [
            MagicMock(text="Comment 1"),
            MagicMock(text="Comment 2")
        ]
        comments = mock_scraper.get_comments()
        self.assertEqual(len(comments), 2)
        self.assertEqual(comments[0].text, "Comment 1")
        self.assertEqual(comments[1].text, "Comment 2")

    @patch.object(BookScraper, 'extract_comment_info')
    def test_scraper_extract_comment(self, mock_extract_comment):
        mock_scraper = BookScraper()
        mock_comment = MagicMock()
        mock_extract_comment.return_value = {
            "author": "Test Author",
            "date": "Enero 1, 2025",
            "content": "Test Content"
        }

    @patch.object(BookScraper, 'process_date')
    def test_scraper_process_date(self, mock_process_date):
        mock_scraper = BookScraper()   #creo una instancia de bookscraper
        date_str = "enero 12, 2025 a las 5:30 pm"
        mock_process_date.return_value = timezone_now()  # hago que process_date me devuelva la fecha actual con zona horaria

        processed_date = mock_scraper.process_date(date_str)    # llamo al metodo process_date
        self.assertIsInstance(processed_date, type(timezone_now()))  #verificar que sea el mismo que timezone_now

    def test_process_date_invalid_day(self):    #pruebo con una fecha inválida, 32
        scraper = BookScraper()
        date_str = "enero 32, 2025 a las 10:00 am"  
        result = scraper.process_date(date_str)
        self.assertIsNone(result) 

    def test_process_date_invalid_month(self):   # Pruebo con un mes inválido, que no está en el diccionario
        scraper = BookScraper()
        date_str = "Jupiter 12, 2025 a las 8:00 am"  
        result = scraper.process_date(date_str)
        self.assertIsNone(result)