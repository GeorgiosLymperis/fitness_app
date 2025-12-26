import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
from pathlib import Path
from typing import List


class FitnessRAG:
    def __init__(self, data_paths: List[str]):
        """
        data_paths: list of csv or txt/md files with fitness knowledge
        """
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.texts = []
        self.meta = []
        self._load_sources(data_paths)
        self._build_index()

    def _load_sources(self, paths: List[str]):
        for p in paths:
            path = Path(p)
            if not path.exists():
                continue

            if path.suffix == ".csv":
                self._load_csv(path)
            elif path.suffix in [".txt", ".md"]:
                self._load_text(path)

    def _load_csv(self, path: Path):
        df = pd.read_csv(path)

        grouped = df.groupby(["Exercise", "Area"])

        for (exercise, area), group in grouped:
            lines = []
            for _, row in group.iterrows():
                lines.append(
                f"BW {row['BW']} kg: "
                f"Beg {row['Beg.']}, Nov {row['Nov.']}, "
                f"Int {row['Int.']}, Adv {row['Adv.']}, Elite {row['Elite']}"
            )
            text = (
            f"Exercise: {exercise}. Area: {area}. "
            f"Strength standards by bodyweight: " + " | ".join(lines)
        )
            self.texts.append(text)
            self.meta.append({"type": "standards"})

    def _load_text(self, path: Path):
        content = path.read_text(encoding="utf-8")
        # simple chunking by paragraphs
        for chunk in content.split("\n\n"):
            chunk = chunk.strip()
            if len(chunk) > 20:
                self.texts.append(chunk)
                self.meta.append({"type": "rules"})

    def _build_index(self):
        if not self.texts:
            raise ValueError("No texts loaded for RAG.")

        embeddings = self.model.encode(
            self.texts, convert_to_numpy=True, show_progress_bar=True
        ).astype("float32")

        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeddings)

    def retrieve(self, query: str, k: int = 5, source: str | None = None) -> List[str]:
        query_emb = self.model.encode([query], convert_to_numpy=True).astype("float32")
        _, idx = self.index.search(query_emb, k)

        results = []
        for i in idx[0]:
            if source is not None and self.meta[i]["type"] != source:
                continue
            results.append(self.texts[i])

        return results if results else [None]
