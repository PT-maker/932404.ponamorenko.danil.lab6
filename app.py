import math
import os

import uvicorn
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PUBLIC_DIR = os.path.join(BASE_DIR, "public")

app = FastAPI(title="Список фильмов с рейтингом", description="Лабораторная №6, вариант 15")


class Movie(BaseModel):
    title: str
    year: int
    rating: float


class Error(BaseModel):
    error: str


# Данные: список фильмов (title, year, rating)
MOVIES = [
    {"title": "Побег из Шоушенка", "year": 1994, "rating": 9.3},
    {"title": "Крёстный отец", "year": 1972, "rating": 9.2},
    {"title": "Тёмный рыцарь", "year": 2008, "rating": 9.0},
    {"title": "Криминальное чтиво", "year": 1994, "rating": 8.9},
    {"title": "Форрест Гамп", "year": 1994, "rating": 8.8},
    {"title": "Начало", "year": 2010, "rating": 8.8},
    {"title": "Матрица", "year": 1999, "rating": 8.7},
    {"title": "Интерстеллар", "year": 2014, "rating": 8.7},
    {"title": "Гладиатор", "year": 2000, "rating": 8.5},
    {"title": "Субстанция", "year": 2024, "rating": 7.3},
    {"title": "Тор: Любовь и гром", "year": 2022, "rating": 6.2},
    {"title": "Мег 2: Бездна", "year": 2023, "rating": 5.0},
]


@app.get("/", include_in_schema=False)
def index():
    return FileResponse(os.path.join(PUBLIC_DIR, "index.html"))


@app.get("/about", include_in_schema=False)
def about():
    return FileResponse(os.path.join(PUBLIC_DIR, "about.html"))


@app.get("/api/status")
def status():
    return {"status": "ok"}


def parse_min_rating(values):
    """Возвращает число или None, если значение невалидно."""
    if len(values) != 1:  # повтор параметра (?minRating=1&minRating=2)
        return None
    raw = values[0].strip()
    if raw == "":
        return None
    try:
        value = float(raw)
    except ValueError:
        return None
    if not math.isfinite(value) or not 0 <= value <= 10:
        return None
    return value


@app.get(
    "/api/movies",
    response_model=list[Movie],
    responses={400: {"model": Error, "description": "Невалидный minRating"}},
)
def get_movies(
    minRating: list[str] | None = Query(
        default=None, description="Минимальный рейтинг, число от 0 до 10"
    ),
):
    result = list(MOVIES)

    if minRating is not None:
        min_rating = parse_min_rating(minRating)
        if min_rating is None:
            return JSONResponse(
                status_code=400,
                content={"error": "minRating должен быть числом от 0 до 10"},
            )
        result = [m for m in result if m["rating"] >= min_rating]

    result.sort(key=lambda m: m["rating"], reverse=True)  # по убыванию рейтинга
    return result


# Статика (CSS, JS, manifest.json, sw.js, иконки) — в самом конце, после всех маршрутов
app.mount("/", StaticFiles(directory=PUBLIC_DIR), name="static")


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=int(os.environ.get("PORT", 3000)), reload=True)