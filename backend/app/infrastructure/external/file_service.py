"""
МОК сервиса для работы с файлами (скачивание, парсинг).

⚠️ ВНИМАНИЕ: ЭТО МОК (ЗАГЛУШКА) ⚠️

Реальная реализация скачивания и парсинга файлов будет подключена другим разработчиком.
Этот класс возвращает тестовые данные для разработки API endpoints.

Для подключения реальной реализации:
1. Замените методы download_pdf(), download_tex() на реальное скачивание файлов
2. Замените методы parse_tex(), parse_pdf() на реальный парсинг
3. Замените методы extract_images_from_pdf(), extract_images_from_tex() на реальное извлечение изображений
4. Обновите dependency injection в app/presentation/dependencies.py
"""
from pathlib import Path
from typing import Optional, List


class FileService:
    """
    МОК сервиса для скачивания и работы с файлами статей.
    
    ⚠️ МОК-РЕАЛИЗАЦИЯ ⚠️
    Реальная реализация будет подключена другим разработчиком.
    """
    
    def __init__(self, downloads_dir: str = "./downloads"):
        """
        Инициализация сервиса.
        
        Args:
            downloads_dir: Директория для сохранения файлов
        """
        self.downloads_dir = Path(downloads_dir)
        self.downloads_dir.mkdir(parents=True, exist_ok=True)
    
    async def download_pdf(self, url: str, arxiv_id: str) -> Optional[str]:
        """
        МОК: Скачать PDF файл статьи.
        
        ⚠️ ВНИМАНИЕ: Это заглушка! Реальная реализация будет подключена другим разработчиком.
        
        Args:
            url: URL PDF файла
            arxiv_id: arXiv ID статьи
        
        Returns:
            Путь к сохраненному файлу (тестовый путь)
        
        TODO: Заменить на реальное скачивание PDF файла
        """
        # МОК: Возвращаем тестовый путь
        file_path = self.downloads_dir / f"{arxiv_id}.pdf"
        return str(file_path)
    
    async def download_tex(self, url: str, arxiv_id: str) -> Optional[str]:
        """
        МОК: Скачать TeX файл статьи.
        
        ⚠️ ВНИМАНИЕ: Это заглушка! Реальная реализация будет подключена другим разработчиком.
        
        Args:
            url: URL TeX файла
            arxiv_id: arXiv ID статьи
        
        Returns:
            Путь к сохраненному файлу (тестовый путь)
        
        TODO: Заменить на реальное скачивание TeX файла
        """
        # МОК: Возвращаем тестовый путь
        file_path = self.downloads_dir / f"{arxiv_id}.tex"
        return str(file_path)
    
    async def parse_tex(self, file_path: str) -> Optional[str]:
        """
        МОК: Парсинг TeX файла и извлечение текста.
        
        ⚠️ ВНИМАНИЕ: Это заглушка! Реальная реализация будет подключена другим разработчиком.
        
        Args:
            file_path: Путь к TeX файлу
        
        Returns:
            Извлеченный текст (тестовый текст)
        
        TODO: Заменить на реальный парсинг TeX файла
        """
        # МОК: Возвращаем тестовый текст
        return f"[MOCK] Parsed TeX content from {file_path}. This is a placeholder that will be replaced with real TeX parsing."
    
    async def parse_pdf(self, file_path: str) -> Optional[str]:
        """
        МОК: Парсинг PDF файла и извлечение текста.
        
        ⚠️ ВНИМАНИЕ: Это заглушка! Реальная реализация будет подключена другим разработчиком.
        
        Args:
            file_path: Путь к PDF файлу
        
        Returns:
            Извлеченный текст (тестовый текст)
        
        TODO: Заменить на реальный парсинг PDF файла
        """
        # МОК: Возвращаем тестовый текст
        return f"[MOCK] Parsed PDF content from {file_path}. This is a placeholder that will be replaced with real PDF parsing."
    
    async def extract_images_from_pdf(self, file_path: str) -> List[str]:
        """
        МОК: Извлечь изображения из PDF файла.
        
        ⚠️ ВНИМАНИЕ: Это заглушка! Реальная реализация будет подключена другим разработчиком.
        
        Args:
            file_path: Путь к PDF файлу
        
        Returns:
            Список путей к извлеченным изображениям (тестовые пути)
        
        TODO: Заменить на реальное извлечение изображений из PDF
        """
        # МОК: Возвращаем тестовые пути
        images_dir = self.downloads_dir / "images"
        return [
            str(images_dir / f"image_{i}.png")
            for i in range(3)  # Возвращаем 3 тестовых изображения
        ]
    
    async def extract_images_from_tex(self, file_path: str) -> List[str]:
        """
        МОК: Извлечь пути к изображениям из TeX файла.
        
        ⚠️ ВНИМАНИЕ: Это заглушка! Реальная реализация будет подключена другим разработчиком.
        
        Args:
            file_path: Путь к TeX файлу
        
        Returns:
            Список путей к изображениям (тестовые пути)
        
        TODO: Заменить на реальное извлечение путей к изображениям из TeX
        """
        # МОК: Возвращаем тестовые пути
        return [
            f"figures/figure_{i}.png"
            for i in range(2)  # Возвращаем 2 тестовых пути
        ]
