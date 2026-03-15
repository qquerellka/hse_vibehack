"""Сервис для скачивания и парсинга файлов статей."""
import asyncio
import io
import tarfile
from pathlib import Path
from typing import List, Optional

import fitz
import pymupdf4llm
import requests

from app.infrastructure.config.settings import settings


class FileService:
    """Сервис для скачивания и работы с файлами статей."""

    def __init__(
        self,
        downloads_dir: str = settings.DOWNLOADS_DIR,
        extracted_images_dir: str = settings.EXTRACTED_IMAGES_DIR,
    ) -> None:
        self.downloads_dir = Path(downloads_dir)
        self.downloads_dir.mkdir(parents=True, exist_ok=True)
        self.extracted_images_dir = Path(extracted_images_dir)
        self.extracted_images_dir.mkdir(parents=True, exist_ok=True)

    async def download_pdf(self, url: str, arxiv_id: str) -> Optional[str]:
        """Скачать PDF файл статьи."""
        file_path = self.downloads_dir / f"{arxiv_id}.pdf"

        def _download() -> str:
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            file_path.write_bytes(response.content)
            return str(file_path.absolute())

        return await asyncio.to_thread(_download)

    async def download_tex(self, url: str, arxiv_id: str) -> Optional[str]:
        """Скачать и распаковать TeX-исходники статьи."""
        target_dir = self.downloads_dir / f"{arxiv_id}_tex"
        target_dir.mkdir(parents=True, exist_ok=True)

        def _download() -> Optional[str]:
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            try:
                with tarfile.open(fileobj=io.BytesIO(response.content), mode="r:*") as archive:
                    archive.extractall(path=target_dir)
            except tarfile.ReadError:
                return None
            return str(target_dir.absolute())

        return await asyncio.to_thread(_download)

    async def parse_tex(self, file_path: str) -> Optional[str]:
        """Парсинг TeX файлов и извлечение текста."""
        def _parse() -> Optional[str]:
            path = Path(file_path)
            tex_files = [path] if path.is_file() and path.suffix.lower() == ".tex" else list(path.glob("**/*.tex"))
            if not tex_files:
                return None

            main_tex = None
            for tex_file in tex_files:
                preview = tex_file.read_text(encoding="utf-8", errors="ignore")[:2000].lower()
                if "\\documentclass" in preview or "\\begin{document}" in preview:
                    main_tex = tex_file
                    break

            chunks: List[str] = []
            for tex_file in ([main_tex] if main_tex else tex_files):
                if tex_file is None:
                    continue
                content = tex_file.read_text(encoding="utf-8", errors="ignore")
                if "\\begin{document}" in content:
                    content = content[content.find("\\begin{document}"):]
                chunks.append(f"\n\n%%% FILE: {tex_file.name} %%%\n{content}")

            parsed = "\n".join(chunks).strip()
            return parsed or None

        return await asyncio.to_thread(_parse)

    async def parse_pdf(self, file_path: str) -> Optional[str]:
        """Парсинг PDF файла и извлечение текста."""
        return await asyncio.to_thread(pymupdf4llm.to_markdown, file_path)

    async def extract_images_from_pdf(self, file_path: str) -> List[str]:
        """Извлечь изображения из PDF файла."""
        def _extract() -> List[str]:
            source = Path(file_path)
            target_dir = self.extracted_images_dir / source.stem
            target_dir.mkdir(parents=True, exist_ok=True)

            saved_images: List[str] = []
            image_counter = 0
            doc = fitz.open(str(source))
            try:
                for page_num in range(len(doc)):
                    for image_info in doc[page_num].get_images(full=True):
                        xref = image_info[0]
                        try:
                            pix = fitz.Pixmap(doc, xref)
                            if pix.n - pix.alpha > 3:
                                pix = fitz.Pixmap(fitz.csRGB, pix)
                            image_counter += 1
                            image_path = target_dir / f"{source.stem}_page{page_num + 1}_img{image_counter}.png"
                            pix.save(str(image_path))
                            saved_images.append(str(image_path.absolute()))
                        except Exception:
                            continue
            finally:
                doc.close()
            return saved_images

        return await asyncio.to_thread(_extract)

    async def extract_images_from_tex(self, file_path: str) -> List[str]:
        """Найти изображения в директории с TeX-исходниками."""
        def _extract() -> List[str]:
            path = Path(file_path)
            root = path if path.is_dir() else path.parent
            images: List[str] = []
            for ext in (".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".pdf"):
                images.extend(str(candidate.absolute()) for candidate in root.glob(f"**/*{ext}"))
            return images

        return await asyncio.to_thread(_extract)
