"""Сервис для работы с файлами (скачивание, парсинг, извлечение изображений)."""
import re
import io
import tarfile
import asyncio
from pathlib import Path
from typing import Optional, List

import arxiv
import pymupdf4llm
import fitz
import requests

from app.infrastructure.config.settings import settings


class FileService:
    """Сервис для скачивания и работы с файлами статей."""

    def __init__(self, downloads_dir: str = None, extracted_images_dir: str = None):
        self.downloads_dir = Path(downloads_dir or settings.DOWNLOADS_DIR)
        self.downloads_dir.mkdir(parents=True, exist_ok=True)
        self.extracted_images_dir = Path(
            extracted_images_dir or settings.EXTRACTED_IMAGES_DIR
        )
        self.extracted_images_dir.mkdir(parents=True, exist_ok=True)

    # ── PDF download ────────────────────────────────────────────

    def _download_pdf_sync(self, url: str, arxiv_id: str) -> Optional[str]:
        clean_id = re.sub(r"v\d+$", "", arxiv_id.strip())
        client = arxiv.Client()
        search = arxiv.Search(id_list=[clean_id])
        try:
            paper = next(client.results(search))
        except StopIteration:
            return None
        file_name = f"{clean_id}.pdf"
        paper.download_pdf(dirpath=str(self.downloads_dir), filename=file_name)
        return str(self.downloads_dir / file_name)

    async def download_pdf(self, url: str, arxiv_id: str) -> Optional[str]:
        """Скачать PDF файл статьи."""
        return await asyncio.to_thread(self._download_pdf_sync, url, arxiv_id)

    # ── TeX download ────────────────────────────────────────────

    def _download_tex_sync(self, url: str, arxiv_id: str) -> Optional[str]:
        clean_id = re.sub(r"v\d+$", "", arxiv_id.strip())
        paper_dir = self.downloads_dir / f"{clean_id}_tex"
        paper_dir.mkdir(exist_ok=True)
        source_url = f"https://arxiv.org/e-print/{clean_id}"
        response = requests.get(source_url, stream=True, timeout=30)
        response.raise_for_status()
        try:
            with tarfile.open(fileobj=io.BytesIO(response.content), mode="r:gz") as tar:
                tar.extractall(path=paper_dir, filter="data")
        except tarfile.ReadError:
            # Not a tar — might be a single TeX file
            single_file = paper_dir / "main.tex"
            single_file.write_bytes(response.content)
        return str(paper_dir)

    async def download_tex(self, url: str, arxiv_id: str) -> Optional[str]:
        """Скачать TeX файлы статьи."""
        return await asyncio.to_thread(self._download_tex_sync, url, arxiv_id)

    # ── PDF parsing ─────────────────────────────────────────────

    def _parse_pdf_sync(self, file_path: str) -> Optional[str]:
        return pymupdf4llm.to_markdown(file_path)

    async def parse_pdf(self, file_path: str) -> Optional[str]:
        """Парсинг PDF файла и извлечение текста."""
        return await asyncio.to_thread(self._parse_pdf_sync, file_path)

    # ── TeX parsing ─────────────────────────────────────────────

    def _parse_tex_sync(self, file_path: str) -> Optional[str]:
        p = Path(file_path)
        if p.is_file():
            tex_files = [p]
        else:
            tex_files = list(p.glob("**/*.tex"))

        if not tex_files:
            return None

        # Find main .tex file
        main_tex = None
        for tf in tex_files:
            try:
                with open(tf, "r", encoding="utf-8", errors="ignore") as f:
                    preview = f.read(2000).lower()
                    if "\\documentclass" in preview or "\\begin{document}" in preview:
                        main_tex = tf
                        break
            except Exception:
                continue

        files_to_read = [main_tex] if main_tex else tex_files

        all_content = []
        for tf in files_to_read:
            try:
                with open(tf, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    if "\\begin{document}" in content:
                        content = content[content.find("\\begin{document}"):]
                    all_content.append(content)
            except Exception:
                continue

        return "\n".join(all_content) if all_content else None

    async def parse_tex(self, file_path: str) -> Optional[str]:
        """Парсинг TeX файла и извлечение текста."""
        return await asyncio.to_thread(self._parse_tex_sync, file_path)

    # ── Image extraction from PDF ───────────────────────────────

    def _extract_images_from_pdf_sync(self, file_path: str) -> List[str]:
        base_path = Path(file_path)
        pdf_name = base_path.stem
        pdf_output_folder = self.extracted_images_dir / pdf_name
        pdf_output_folder.mkdir(parents=True, exist_ok=True)

        doc = fitz.open(str(base_path))
        saved_images = []
        image_counter = 0

        for page_num in range(len(doc)):
            page = doc[page_num]
            for img_info in page.get_images(full=True):
                xref = img_info[0]
                try:
                    pix = fitz.Pixmap(doc, xref)
                    if pix.n - pix.alpha > 3:
                        pix = fitz.Pixmap(fitz.csRGB, pix)
                    image_counter += 1
                    image_filename = (
                        f"{pdf_name}_page{page_num + 1}_img{image_counter}.png"
                    )
                    save_path = pdf_output_folder / image_filename
                    pix.save(str(save_path))
                    saved_images.append(str(save_path))
                except Exception:
                    pass

        doc.close()
        return saved_images

    async def extract_images_from_pdf(self, file_path: str) -> List[str]:
        """Извлечь изображения из PDF файла."""
        return await asyncio.to_thread(self._extract_images_from_pdf_sync, file_path)

    # ── Image extraction from TeX ───────────────────────────────

    def _extract_images_from_tex_sync(self, file_path: str) -> List[str]:
        p = Path(file_path)
        image_extensions = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp"}
        image_files = []
        for ext in image_extensions:
            image_files.extend(p.glob(f"**/*{ext}"))
        return [str(img.absolute()) for img in image_files]

    async def extract_images_from_tex(self, file_path: str) -> List[str]:
        """Извлечь пути к изображениям из TeX директории."""
        return await asyncio.to_thread(self._extract_images_from_tex_sync, file_path)
