#!/usr/bin/env python3
from collections import Counter, defaultdict, OrderedDict
from datetime import datetime
import re
import os
import requests
from bs4 import BeautifulSoup
import os
import pytest


class Movies:
    def __init__(self, path_movies):
        self.path_movies = path_movies
        if not os.path.exists(self.path_movies):
            raise Exception("File does not exist")
        self.data = []
        self.file_csv_reader()

    def split_correct_csv_line(self, line):
        result_parts = []
        current_value = []
        inside = False
        i = 0
        while i < len(line):
            char = line[i]
            if char == '"':
                if inside and i + 1 < len(line) and line[i + 1] == '"':
                    current_value.append('"')
                    i += 2
                    continue
                inside = not inside
            elif char == "," and not inside:
                result_parts.append("".join(current_value))
                current_value = []
            else:
                current_value.append(char)
            i += 1
        result_parts.append("".join(current_value))
        return result_parts

    def file_csv_reader(self):
        with open(self.path_movies, "r", encoding="utf-8") as f:
            first_line = f.readline().strip()
            expected_header = "movieId,title,genres"
            if first_line != expected_header:
                raise Exception(
                    f"This file isn't file with movies. His format(header) is different."
                )
            lines = f.read().splitlines()
        for line in lines[:1000]:
            parts = self.split_correct_csv_line(line)
            if len(parts) != 3:
                raise Exception("movies.csv has invalid structure")
            title = parts[1]
            m = re.search(r"\((\d{4})\)", title)
            year = int(m.group(1)) if m else None
            genres = parts[2].split("|") if parts[2] else []
            self.data.append(
                {
                    "movieId": int(parts[0]),
                    "title": title,
                    "genres": genres,
                    "year": year,
                }
            )

    def dist_by_release(self):
        years = [dicts["year"] for dicts in self.data if dicts["year"] is not None]
        release_years = dict(Counter(years).most_common())
        return release_years

    def dist_by_genres(self):
        genres = [genre for d in self.data for genre in d["genres"]]
        genres_counts = dict(Counter(genres).most_common())
        return genres_counts

    def most_genres(self, n):
        if not isinstance(n, int):
            raise Exception("n must be integer")
        if n < 0:
            raise Exception("n must be non-negative")
        movies_genres_counts = [(d["title"], len(d["genres"])) for d in self.data]
        movies_genres_top = sorted(movies_genres_counts, key=lambda v: (-v[1], v[0]))[
            :n
        ]
        return dict(movies_genres_top)


class Ratings:
    def __init__(self, path_to_movies, path_to_ratings):
        self.path_to_movies = path_to_movies
        if not os.path.exists(self.path_to_movies):
            raise Exception("File does not exist")
        self.path_to_ratings = path_to_ratings
        if not os.path.exists(self.path_to_ratings):
            raise Exception("File does not exist")
        self.ratings = []
        self.movies = []
        self.data = []
        self.read_ratings_1000()
        self.read_movies_1000()
        self.join_ratings_with_movies()
        self.class_movies = self.Movies(self)
        self.class_users = self.Users(self)

    def read_ratings_1000(self):
        with open(self.path_to_ratings, "r", encoding="utf-8") as f:
            first_line = f.readline().strip()
            expected_header = "userId,movieId,rating,timestamp"
            if first_line != expected_header:
                raise Exception(
                    f"This file isn't file with ratings. His format(header) is different."
                )
            for line in f:
                if len(self.ratings) == 1000:
                    break
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                if len(parts) != 4:
                    raise Exception("ratings.csv has invalid structure")
                self.ratings.append(
                    {
                        "userId": int(parts[0]),
                        "movieId": int(parts[1]),
                        "rating": float(parts[2]),
                        "timestamp": int(parts[3]),
                    }
                )

    def split_correct_csv_line(self, line):
        result_parts = []
        current_value = []
        inside = False
        i = 0
        while i < len(line):
            char = line[i]
            if char == '"':
                if inside and i + 1 < len(line) and line[i + 1] == '"':
                    current_value.append('"')
                    i += 2
                    continue
                inside = not inside
            elif char == "," and not inside:
                result_parts.append("".join(current_value))
                current_value = []
            else:
                current_value.append(char)
            i += 1
        result_parts.append("".join(current_value))
        return result_parts

    def read_movies_1000(self):
        with open(self.path_to_movies, "r", encoding="utf-8") as f:
            first_line = f.readline().strip()
            expected_header = "movieId,title,genres"
            if first_line != expected_header:
                raise Exception(
                    f"This file isn't file with movies. His format(header) is different."
                )
            for line in f:
                if len(self.movies) == 1000:
                    break
                line = line.rstrip("\n")

                parts = self.split_correct_csv_line(line)
                if len(parts) != 3:
                    raise Exception("movies.csv has invalid structure")

                title = parts[1]
                m = re.search(r"\((\d{4})\)", title)
                year = int(m.group(1)) if m else None
                genres = parts[2].split("|") if parts[2] else []

                self.movies.append(
                    {
                        "movieId": int(parts[0]),
                        "title": title,
                        "year": year,
                        "genres": genres,
                    }
                )

    def join_ratings_with_movies(self):
        movie_dict = {i["movieId"]: i for i in self.movies}
        self.data = []
        for i in self.ratings:
            movie = movie_dict.get(i["movieId"])
            if movie is None:
                continue
            joined = dict(i)
            joined["title"] = movie["title"]
            joined["year"] = movie["year"]
            joined["genres"] = movie["genres"]
            self.data.append(joined)

    class Movies:
        def __init__(self, ratings_parent):
            self.ratings = ratings_parent

        def dist_by_year(self):
            years = [
                datetime.fromtimestamp(i["timestamp"]).year
                for i in self.ratings.ratings
            ]
            ratings_by_year = dict(sorted(Counter(years).items()))
            return ratings_by_year

        def dist_by_rating(self):
            ratings_distribution = dict(
                sorted(Counter([i["rating"] for i in self.ratings.ratings]).items())
            )
            return ratings_distribution

        def top_by_num_of_ratings(self, n):
            if not isinstance(n, int) or n < 0:
                raise Exception("n must be non-negative integer")
            all_movies = Counter([i["title"] for i in self.ratings.data])
            top_movies = dict(all_movies.most_common(n))
            return top_movies

        def __median(self, data):
            data = sorted(data)
            center = len(data) // 2

            if len(data) % 2 == 1:
                return data[center]
            else:
                return (data[center] + data[center - 1]) / 2

        def top_by_ratings(self, n, metric="average"):
            if not isinstance(n, int) or n < 0:
                raise Exception("n must be non-negative integer")
            if metric == "average":
                d = defaultdict(lambda: [0, 0])
                for i in self.ratings.data:
                    d[i["title"]][0] += i["rating"]
                    d[i["title"]][1] += 1
                top_movies = {
                    title: round(counts[0] / counts[1], 2)
                    for title, counts in d.items()
                }
            elif metric == "median":
                d = defaultdict(list)
                for i in self.ratings.data:
                    d[i["title"]].append(i["rating"])
                top_movies = {
                    title: round(self.__median(ratings), 2)
                    for title, ratings in d.items()
                }
            else:
                raise ValueError("metric must be average or median")
            top_movies = dict(
                sorted(top_movies.items(), key=lambda x: (-x[1], x[0]))[:n]
            )
            return top_movies

        def top_controversial(self, n):
            if not isinstance(n, int) or n < 0:
                raise Exception("n must be non-negative integer")
            d = defaultdict(lambda: [0, 0, []])
            for i in self.ratings.data:
                d[i["title"]][0] += i["rating"]
                d[i["title"]][1] += 1
                d[i["title"]][2].append(i["rating"])

            before_top_movies = {
                title: round(
                    sum(map(lambda x: (x - total / count) ** 2, mas)) / count, 2
                )
                for title, (total, count, mas) in d.items()
            }
            top_movies = dict(
                sorted(before_top_movies.items(), key=lambda x: (-x[1], x[0]))[:n]
            )
            return top_movies

    class Users(Movies):
        def __init__(self, ratings_parent):
            self.ratings = ratings_parent

        def dist_by_num_of_ratings(self):
            per_user = Counter(i["userId"] for i in self.ratings.ratings)
            dist = Counter(per_user.values())
            return dict(sorted(dist.items()))

        def __median(self, data):
            data = sorted(data)
            c = len(data) // 2
            if len(data) % 2 == 1:
                return data[c]
            return (data[c] + data[c - 1]) / 2

        def dist_by_ratings(self, metric="average"):
            if metric == "average":
                d = defaultdict(lambda: [0.0, 0])
                for i in self.ratings.ratings:
                    d[i["userId"]][0] += i["rating"]
                    d[i["userId"]][1] += 1
                vals = [round(total / cnt, 2) for total, cnt in d.values()]

            elif metric == "median":
                d = defaultdict(list)
                for i in self.ratings.ratings:
                    d[i["userId"]].append(i["rating"])
                vals = [round(self.__median(rs), 2) for rs in d.values()]

            else:
                raise ValueError("metric must be average or median")

            return dict(sorted(Counter(vals).items()))

        def top_controversial(self, n):
            if not isinstance(n, int) or n < 0:
                raise Exception("n must be non-negative integer")

            d = defaultdict(list)
            for i in self.ratings.ratings:
                d[i["userId"]].append(i["rating"])

            var = {}
            for user_id, rs in d.items():
                mean = sum(rs) / len(rs)
                v = sum((x - mean) ** 2 for x in rs) / len(rs)
                var[user_id] = round(v, 2)

            return dict(sorted(var.items(), key=lambda x: (-x[1], x[0]))[:n])


class Tags:
    def __init__(self, path_to_the_file):
        self.path = path_to_the_file
        if not os.path.exists(self.path):
            raise Exception("File does not exist")
        self.tags = []
        self._read_tags_1000()

    def _read_tags_1000(self):
        with open(self.path, "r", encoding="utf-8") as f:
            header = f.readline().strip()
            if header != "userId,movieId,tag,timestamp":
                raise Exception("tags.csv has invalid header")
            for line in f:
                if len(self.tags) == 1000:
                    break
                line = line.rstrip("\n")
                if not line:
                    continue
                first = line.find(",")
                second = line.find(",", first + 1)
                last = line.rfind(",")
                if (
                    first == -1
                    or second == -1
                    or last == -1
                    or not (first < second < last)
                ):
                    raise Exception("tags.csv has invalid structure")
                tag = line[second + 1 : last].strip()
                if len(tag) >= 2 and tag[0] == '"' and tag[-1] == '"':
                    tag = tag[1:-1].replace('""', '"')
                self.tags.append(
                    {
                        "userId": int(line[:first]),
                        "movieId": int(line[first + 1 : second]),
                        "tag": tag,
                        "timestamp": int(line[last + 1 :]),
                    }
                )

    def most_words(self, n):
        if not isinstance(n, int) or n < 0:
            raise Exception("n must be non-negative integer")
        unique_tags = {i["tag"] for i in self.tags}
        sorted_tags = sorted(unique_tags, key=lambda x: (-len(x.split()), x))[:n]
        big_tags = {}
        for i in sorted_tags:
            big_tags[i] = len(i.split())
        return big_tags

    def longest(self, n):
        if not isinstance(n, int) or n < 0:
            raise Exception("n must be non-negative integer")
        unique_tags = list({i["tag"] for i in self.tags})
        big_tags = sorted(unique_tags, key=lambda x: (-len(x), x))[:n]
        return big_tags

    def most_words_and_longest(self, n):
        if not isinstance(n, int) or n < 0:
            raise Exception("n must be non-negative integer")
        most_words = set(self.most_words(n).keys())
        longest_tags = set(self.longest(n))
        big_tags = list(most_words & longest_tags)
        return sorted(big_tags)

    def most_popular(self, n):
        if not isinstance(n, int) or n < 0:
            raise Exception("n must be non-negative integer")
        all_tags = Counter(i["tag"] for i in self.tags)
        popular_tags = dict(all_tags.most_common(n))
        return popular_tags

    def tags_with(self, word):
        if not isinstance(word, str):
            raise Exception("word must be string")
        tags_with_word = sorted(
            {i["tag"] for i in self.tags if word.lower() in i["tag"].lower()}
        )
        return tags_with_word
    
class Links:
    def __init__(self, path_to_links_csv, n=1000):
        self.path = path_to_links_csv
        if not os.path.exists(self.path):
            raise Exception("File does not exist")

        if not isinstance(n, int):
            raise Exception("n must be integer")
        if n < 0:
            raise Exception("n must be non-negative")

        self.data = []        
        self.imdb_cache = {}   
        self._read_links(n)

    def _read_links(self, n):
        with open(self.path, "r", encoding="utf-8") as f:
            header = f.readline().strip()
            expected = "movieId,imdbId,tmdbId"
            if header != expected:
                raise Exception("links.csv has invalid header")

            for line in f:
                if len(self.data) == n:
                    break
                line = line.strip()
                if not line:
                    continue

                parts = line.split(",")
                if len(parts) != 3:
                    raise Exception("links.csv has invalid structure")

                movie_id = int(parts[0])
                imdb_id = parts[1].strip()
                tmdb_id = parts[2].strip()

                self.data.append(
                    {"movieId": movie_id, "imdbId": imdb_id, "tmdbId": tmdb_id}
                )

    @staticmethod
    def get_number(str_number):
        if not str_number or str_number == "Unknown field":
            return None
        digits = re.findall(r"\d+", str_number)
        if not digits:
            return None
        return int("".join(digits))

    @staticmethod
    def get_time(str_time):
        if not str_time or str_time == "Unknown field":
            return None
        match = re.search(r"\((\d+)\s*min\)", str_time)
        if not match:
            match = re.search(r"(\d+)\s*m", str_time)
        return int(match.group(1)) if match else None

    def _movieid_to_imdbid(self):
        mp = {}
        for row in self.data:
            mid = row["movieId"]
            iid = row["imdbId"]
            if iid:
                mp[mid] = iid
        return mp

    @staticmethod
    def _safe_get(url, headers, timeout=30):
        try:
            resp = requests.get(url, headers=headers, timeout=timeout)
            if not (200 <= resp.status_code < 300):
                return None
            return resp.text
        except requests.RequestException:
            return None

    @staticmethod
    def _parse_imdb_page(html, fields):
        soup = BeautifulSoup(html, "html.parser")
        out = {f: "Unknown field" for f in fields}

        if "title" in fields:
            title_tag = soup.select_one("span[data-testid='hero__primary-text']")
            if title_tag and title_tag.text.strip():
                out["title"] = f"\"{title_tag.text.strip()}\""

        if "runtime" in fields:
            text = soup.get_text(" ", strip=True)
            m = re.search(r"\((\d+)\s*min\)", text)
            if m:
                out["runtime"] = f"({m.group(1)} min)"

        metadata_items = soup.select("li.ipc-metadata-list__item")
        for item in metadata_items:
            label = item.select_one(".ipc-metadata-list-item__label")
            value = item.select_one(
                ".ipc-metadata-list-item__content-container, .ipc-metadata-list-item__content"
            )
            if not (label and value):
                continue
            key = label.text.strip().lower()
            if key in fields and out.get(key, "Unknown field") == "Unknown field":
                v = value.text.strip()
                if v:
                    out[key] = v

        if "gross" in fields and out.get("gross", "Unknown field") == "Unknown field":
            text = soup.get_text(" ", strip=True)
            gross_patterns = [
                r"Cumulative Worldwide Gross[:\s]+([$€£]?\s*\d+[,\d]*)",
                r"Worldwide[:\s]+([$€£]?\s*\d+[,\d]*)",
                r"Box office[:\s]+([$€£]?\s*\d+[,\d]*)",
            ]
            for pattern in gross_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    out["gross"] = match.group(1).strip()
                    break

        return out

    def get_imdb(self, list_of_movie_ids, list_of_fields):
        if not isinstance(list_of_movie_ids, list) or not all(
            isinstance(x, int) for x in list_of_movie_ids
        ):
            raise Exception("list_of_movie_ids must be list[int]")

        lower_fields = [f.lower() for f in list_of_fields]
        fields = lower_fields  

        movie_to_imdb = self._movieid_to_imdbid()

        headers = {
             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml',
            'Accept-Language': 'en-US,en;q=0.9',
        }

        rows = []
        for movie_id in list_of_movie_ids:
            imdb_id = movie_to_imdb.get(movie_id)
            if not imdb_id:
                row = [movie_id] + ["Unknown field"] * len(fields)
                rows.append(row)
                continue

            url = f"https://www.imdb.com/title/tt{imdb_id}/"
            html = self._safe_get(url, headers=headers, timeout=30)

            if not html:
                row = [movie_id] + ["Unknown field"] * len(fields)
                rows.append(row)
                continue

            parsed = self._parse_imdb_page(html, set(fields))
            self.imdb_cache[movie_id] = parsed

            row = [movie_id] + [parsed.get(f, "Unknown field") for f in fields]
            rows.append(row)

        return sorted(rows, key=lambda r: r[0], reverse=True)

    @staticmethod
    def _validate_n(n):
        if not isinstance(n, int):
            raise Exception("n must be integer")
        if n < 0:
            raise Exception("n must be non-negative")
        return n

    def _ensure_imdb_loaded(self, required_fields, n_movies=100):
        have_valid = any(
            isinstance(v, dict) and any(
                k in v and v.get(k, "Unknown field") != "Unknown field" 
                for k in required_fields
            )
            for v in self.imdb_cache.values()
        )
        if have_valid:
            return

        max_movies = min(len(self.data), max(n_movies, 100))
        movie_ids = [row["movieId"] for row in self.data][:max_movies]
        self.get_imdb(movie_ids, list(required_fields))

    def top_directors(self, n):
        n = self._validate_n(n)
        if n == 0:
            return dict()

        self._ensure_imdb_loaded({"director"}, n_movies=min(200, len(self.data)))
        directors = []
        for info in self.imdb_cache.values():
            d = info.get("director", "Unknown field")
            if d != "Unknown field":
                directors.append(d)

        if not directors and len(self.imdb_cache) < len(self.data):
            additional_ids = [row["movieId"] for row in self.data[len(self.imdb_cache):len(self.imdb_cache)+100]]
            self.get_imdb(additional_ids, ["director"])
            for info in self.imdb_cache.values():
                d = info.get("director", "Unknown field")
                if d != "Unknown field":
                    directors.append(d)

        c = Counter(directors)
        return dict(c.most_common(n))

    def most_expensive(self, n):
        n = self._validate_n(n)
        if n == 0:
            return dict()

        self._ensure_imdb_loaded({"title", "budget"}, n_movies=min(200, len(self.data)))
        items = []
        for mid, info in self.imdb_cache.items():
            title = info.get("title", "Unknown field")
            budget_raw = info.get("budget", "Unknown field")
            b = Links.get_number(budget_raw)
            if title != "Unknown field" and b is not None:
                items.append((title, str(b)))

        if not items and len(self.imdb_cache) < len(self.data):
            additional_ids = [row["movieId"] for row in self.data[len(self.imdb_cache):len(self.imdb_cache)+100]]
            self.get_imdb(additional_ids, ["title", "budget"])
            for mid, info in self.imdb_cache.items():
                title = info.get("title", "Unknown field")
                budget_raw = info.get("budget", "Unknown field")
                b = Links.get_number(budget_raw)
                if title != "Unknown field" and b is not None:
                    items.append((title, str(b)))

        items.sort(key=lambda x: int(x[1]), reverse=True)
        return dict(items[:n])

    def most_profitable(self, n):
        n = self._validate_n(n)
        if n == 0:
            return dict()

        self._ensure_imdb_loaded({"title", "budget", "gross"}, n_movies=min(200, len(self.data)))
        items = []
        for mid, info in self.imdb_cache.items():
            title = info.get("title", "Unknown field")
            budget = Links.get_number(info.get("budget", "Unknown field"))
            gross = Links.get_number(info.get("gross", "Unknown field"))
            if title != "Unknown field" and budget is not None and gross is not None:
                items.append((title, gross - budget))

        if not items and len(self.imdb_cache) < len(self.data):
            additional_ids = [row["movieId"] for row in self.data[len(self.imdb_cache):len(self.imdb_cache)+100]]
            self.get_imdb(additional_ids, ["title", "budget", "gross"])
            for mid, info in self.imdb_cache.items():
                title = info.get("title", "Unknown field")
                budget = Links.get_number(info.get("budget", "Unknown field"))
                gross = Links.get_number(info.get("gross", "Unknown field"))
                if title != "Unknown field" and budget is not None and gross is not None:
                    items.append((title, gross - budget))

        items.sort(key=lambda x: x[1], reverse=True)
        return dict(items[:n])

    def longest(self, n):
        n = self._validate_n(n)
        if n == 0:
            return OrderedDict()

        max_attempts = 3
        items = []
        for attempt in range(max_attempts):
            if attempt == 0:
                self._ensure_imdb_loaded({"title", "runtime"}, n_movies=min(200, len(self.data)))
            else:
                start_idx = len(self.imdb_cache)
                end_idx = min(start_idx + 100, len(self.data))
                if start_idx >= end_idx:
                    break
                additional_ids = [row["movieId"] for row in self.data[start_idx:end_idx]]
                self.get_imdb(additional_ids, ["title", "runtime"])
            
            items = []
            for mid, info in self.imdb_cache.items():
                title = info.get("title", "Unknown field")
                runtime_raw = info.get("runtime", "Unknown field")
                minutes = Links.get_time(runtime_raw)
                if title != "Unknown field" and minutes is not None:
                    items.append((title, runtime_raw))
            
            if items:
                break

        items.sort(key=lambda x: Links.get_time(x[1]) or 0, reverse=True)
        return dict(items[:n])

    def top_cost_per_minute(self, n):
        n = self._validate_n(n)
        if n == 0:
            return dict()

        max_attempts = 3
        items = []
        for attempt in range(max_attempts):
            if attempt == 0:
                self._ensure_imdb_loaded({"title", "budget", "runtime"}, n_movies=min(200, len(self.data)))
            else:
                start_idx = len(self.imdb_cache)
                end_idx = min(start_idx + 100, len(self.data))
                if start_idx >= end_idx:
                    break
                additional_ids = [row["movieId"] for row in self.data[start_idx:end_idx]]
                self.get_imdb(additional_ids, ["title", "budget", "runtime"])
            
            items = []
            for mid, info in self.imdb_cache.items():
                title = info.get("title", "Unknown field")
                budget = Links.get_number(info.get("budget", "Unknown field"))
                runtime = Links.get_time(info.get("runtime", "Unknown field"))
                if title != "Unknown field" and budget is not None and runtime not in (None, 0):
                    items.append((title, round(budget / runtime, 2)))
            
            if items:
                break

        items.sort(key=lambda x: x[1], reverse=True)
        return dict(items[:n])
    
class TestAll:
    # RATINGS
    def test_init_ratings(self):
        obj = Ratings("movies.csv", "ratings.csv")

        assert hasattr(obj, "ratings")
        assert hasattr(obj, "movies")
        assert hasattr(obj, "data")
        assert hasattr(obj, "class_movies")
        assert hasattr(obj, "class_users")

        assert isinstance(obj.ratings, list)
        assert isinstance(obj.movies, list)
        assert isinstance(obj.data, list)

        assert len(obj.ratings) == 1000
        assert len(obj.movies) == 1000
        assert len(obj.data) <= len(obj.ratings)

        if obj.data:
            row = obj.data[0]
            for k in (
                "userId",
                "movieId",
                "rating",
                "timestamp",
                "title",
                "year",
                "genres",
            ):
                assert k in row

            assert isinstance(row["userId"], int)
            assert isinstance(row["movieId"], int)
            assert isinstance(row["rating"], float)
            assert isinstance(row["timestamp"], int)
            assert isinstance(row["title"], str)
            assert (row["year"] is None) or isinstance(row["year"], int)
            assert isinstance(row["genres"], list)
            assert all(isinstance(g, str) for g in row["genres"])

    def test_init_movies_inner(self):
        obj = Ratings("movies.csv", "ratings.csv")
        assert isinstance(obj.class_movies, obj.Movies)
        assert obj.class_movies.ratings is obj

    def test_dist_by_year(self):
        rating = Ratings("movies.csv", "ratings.csv")
        result = rating.class_movies.dist_by_year()

        assert isinstance(result, dict)
        keys = list(result.keys())
        assert keys == sorted(keys)
        assert all(isinstance(k, int) for k in keys)
        assert all(isinstance(v, int) for v in result.values())

    def test_dist_by_rating(self):
        rating = Ratings("movies.csv", "ratings.csv")
        result = rating.class_movies.dist_by_rating()

        assert isinstance(result, dict)
        keys = list(result.keys())
        assert keys == sorted(keys)
        assert all(isinstance(k, float) for k in keys)
        assert all(isinstance(v, int) for v in result.values())

    def test_top_by_num_of_ratings(self):
        n = 3
        rating = Ratings("movies.csv", "ratings.csv")
        result = rating.class_movies.top_by_num_of_ratings(n)

        assert isinstance(result, dict)
        assert len(result) <= n
        assert all(isinstance(k, str) for k in result.keys())
        assert all(isinstance(v, int) for v in result.values())

        vals = list(result.values())
        assert vals == sorted(vals, reverse=True)

    def test_top_by_ratings_average(self):
        n = 3
        rating = Ratings("movies.csv", "ratings.csv")
        result = rating.class_movies.top_by_ratings(n)

        assert isinstance(result, dict)
        assert len(result) <= n
        assert all(isinstance(k, str) for k in result.keys())
        for val in result.values():
            assert isinstance(val, float)
            assert round(val, 2) == val

        vals = list(result.values())
        assert vals == sorted(vals, reverse=True)

    def test_top_by_ratings_median(self):
        n = 3
        rating = Ratings("movies.csv", "ratings.csv")
        result = rating.class_movies.top_by_ratings(n, "median")

        assert isinstance(result, dict)
        assert len(result) <= n
        for val in result.values():
            assert isinstance(val, float)
            assert round(val, 2) == val

        vals = list(result.values())
        assert vals == sorted(vals, reverse=True)

    def test_top_controversial(self):
        n = 3
        rating = Ratings("movies.csv", "ratings.csv")
        result = rating.class_movies.top_controversial(n)

        assert isinstance(result, dict)
        assert len(result) <= n
        assert all(isinstance(k, str) for k in result.keys())
        for val in result.values():
            assert isinstance(val, float)
            assert round(val, 2) == val

        vals = list(result.values())
        assert vals == sorted(vals, reverse=True)

    # USERS (Ratings.Users)
    def test_init_users_inner(self):
        obj = Ratings("movies.csv", "ratings.csv")
        assert isinstance(obj.class_users, obj.Users)
        assert obj.class_users.ratings is obj

    def test_users_dist_by_num_of_ratings(self):
        rating = Ratings("movies.csv", "ratings.csv")
        result = rating.class_users.dist_by_num_of_ratings()

        assert isinstance(result, dict)
        keys = list(result.keys())
        assert keys == sorted(keys)
        assert all(isinstance(k, int) for k in keys)
        assert all(isinstance(v, int) for v in result.values())

    def test_users_dist_by_ratings_average(self):
        rating = Ratings("movies.csv", "ratings.csv")
        result = rating.class_users.dist_by_ratings()

        assert isinstance(result, dict)
        keys = list(result.keys())
        assert keys == sorted(keys)
        assert all(isinstance(k, float) for k in keys)
        assert all(round(k, 2) == k for k in keys)
        assert all(isinstance(v, int) for v in result.values())

    def test_users_dist_by_ratings_median(self):
        rating = Ratings("movies.csv", "ratings.csv")
        result = rating.class_users.dist_by_ratings("median")

        assert isinstance(result, dict)
        keys = list(result.keys())
        assert keys == sorted(keys)
        assert all(isinstance(k, float) for k in keys)
        assert all(round(k, 2) == k for k in keys)

    def test_users_top_controversial(self):
        n = 3
        rating = Ratings("movies.csv", "ratings.csv")
        result = rating.class_users.top_controversial(n)

        assert isinstance(result, dict)
        assert len(result) <= n
        assert all(isinstance(k, int) for k in result.keys())
        for val in result.values():
            assert isinstance(val, float)
            assert round(val, 2) == val

        vals = list(result.values())
        assert vals == sorted(vals, reverse=True)

    # TAGS
    def test_init_tags(self):
        obj = Tags("tags.csv")
        assert hasattr(obj, "tags")
        assert isinstance(obj.tags, list)
        assert len(obj.tags) == 1000

        if obj.tags:
            row = obj.tags[0]
            for k in ("userId", "movieId", "tag", "timestamp"):
                assert k in row
            assert isinstance(row["userId"], int)
            assert isinstance(row["movieId"], int)
            assert isinstance(row["tag"], str)
            assert isinstance(row["timestamp"], int)

    def test_most_words(self):
        n = 5
        tags = Tags("tags.csv")
        result = tags.most_words(n)

        assert isinstance(result, dict)
        assert len(result) <= n
        for word_count in result.values():
            assert isinstance(word_count, int) and word_count > 0

        vals = list(result.values())
        assert vals == sorted(vals, reverse=True)

    def test_longest(self):
        n = 5
        tags = Tags("tags.csv")
        result = tags.longest(n)

        assert isinstance(result, list)
        assert len(result) <= n
        assert all(isinstance(tag, str) for tag in result)

        lengths = [len(tag) for tag in result]
        assert lengths == sorted(lengths, reverse=True)

    def test_most_words_and_longest(self):
        n = 5
        tags = Tags("tags.csv")
        result = tags.most_words_and_longest(n)

        assert isinstance(result, list)
        mw_set = set(tags.most_words(n).keys())
        long_set = set(tags.longest(n))
        assert set(result).issubset(mw_set & long_set)
        assert len(result) == len(set(result))

    def test_most_popular(self):
        n = 5
        tags = Tags("tags.csv")
        result = tags.most_popular(n)

        assert isinstance(result, dict)
        assert len(result) <= n
        for count in result.values():
            assert isinstance(count, int) and count > 0

        vals = list(result.values())
        assert vals == sorted(vals, reverse=True)

    def test_tags_with(self):
        word = "comedy"
        tags = Tags("tags.csv")
        result = tags.tags_with(word)

        assert isinstance(result, list)
        assert all(isinstance(tag, str) for tag in result)
        for tag in result:
            assert word.lower() in tag.lower()

        assert result == sorted(result)
        assert len(result) == len(set(result))

    # MOVIES
    def test_init_movies(self):
        obj = Movies("movies.csv")

        assert hasattr(obj, "data")
        assert isinstance(obj.data, list)
        assert len(obj.data) == 1000

        row = obj.data[0]
        for k in ("movieId", "title", "genres", "year"):
            assert k in row

        assert isinstance(row["movieId"], int)
        assert isinstance(row["title"], str)
        assert isinstance(row["genres"], list)
        assert (row["year"] is None) or isinstance(row["year"], int)

        if row["genres"]:
            assert all(isinstance(g, str) for g in row["genres"])

    def test_dist_by_release(self):
        obj = Movies("movies.csv")
        result = obj.dist_by_release()

        assert isinstance(result, dict)
        assert all(isinstance(k, int) for k in result.keys())
        assert all(isinstance(v, int) for v in result.values())

        vals = list(result.values())
        assert vals == sorted(vals, reverse=True)

    def test_dist_by_genres(self):
        obj = Movies("movies.csv")
        result = obj.dist_by_genres()

        assert isinstance(result, dict)
        assert all(isinstance(k, str) for k in result.keys())
        assert all(isinstance(v, int) for v in result.values())

        vals = list(result.values())
        assert vals == sorted(vals, reverse=True)

    def test_most_genres(self):
        obj = Movies("movies.csv")
        n = 5
        result = obj.most_genres(n)

        assert isinstance(result, dict)
        assert len(result) <= n
        assert all(isinstance(k, str) for k in result.keys())
        assert all(isinstance(v, int) for v in result.values())

        items = list(result.items())
        assert items == sorted(items, key=lambda x: (-x[1], x[0]))

    def test_most_genres_bad_n(self):
        obj = Movies("movies.csv")
        with pytest.raises(Exception):
            obj.most_genres(-1)
        with pytest.raises(Exception):
            obj.most_genres("5")

    # LINKS
    def test_links_init(self):
        obj = Links("links.csv")

        assert hasattr(obj, "path")
        assert hasattr(obj, "data")
        assert hasattr(obj, "imdb_cache")

        assert isinstance(obj.path, str)
        assert isinstance(obj.data, list)
        assert isinstance(obj.imdb_cache, dict)

        assert len(obj.data) == 1000

        row = obj.data[0]
        assert isinstance(row, dict)

        for k in ("movieId", "imdbId", "tmdbId"):
            assert k in row

        assert isinstance(row["movieId"], int)

        assert isinstance(row["imdbId"], str)
        assert row["imdbId"] == "" or row["imdbId"].isdigit()

        assert isinstance(row["tmdbId"], str)

    def test_links_init_wrong_path(self):
        with pytest.raises(Exception):
            Links("./no_such_file.csv")

    def test_get_imdb_structure_and_sorting(self):
        link = Links("links.csv")

        ids = [
            link.data[0]["movieId"],
            link.data[1]["movieId"],
            link.data[2]["movieId"],
        ]
        fields = ["title", "director", "runtime"]

        res = link.get_imdb(ids, fields)

        assert isinstance(res, list)
        assert len(res) == len(ids)

        out_ids = [row[0] for row in res]
        assert out_ids == sorted(out_ids, reverse=True)

        for row in res:
            assert isinstance(row, list)
            assert len(row) == 1 + len(fields)
            assert isinstance(row[0], int)

            for val in row[1:]:
                assert isinstance(val, str)
                assert len(val) > 0

    def test_get_imdb_unknown_movieid_does_not_crash(self):
        link = Links("links.csv")

        bad_id = 10**9
        fields = ["title", "runtime"]

        res = link.get_imdb([bad_id], fields)

        assert isinstance(res, list)
        assert len(res) == 1
        assert res[0][0] == bad_id
        assert len(res[0]) == 1 + len(fields)
        assert all(isinstance(x, str) for x in res[0][1:])

    def test_top_directors(self):
        link = Links("links.csv")
        res = link.top_directors(3)

        assert isinstance(res, dict)
        assert len(res) <= 3
        assert all(isinstance(k, str) for k in res.keys())
        assert all(isinstance(v, int) and v > 0 for v in res.values())

        if res:
            vals = list(res.values())
            assert vals == sorted(vals, reverse=True)

    def test_most_expensive(self):
        link = Links("links.csv")
        res = link.most_expensive(3)

        assert isinstance(res, dict)
        assert len(res) <= 3
        assert all(isinstance(k, str) for k in res.keys())
        assert all(isinstance(v, str) for v in res.values())

        if res:
            assert all(v.isdigit() for v in res.values())
            vals = [int(v) for v in res.values()]
            assert vals == sorted(vals, reverse=True)

    def test_most_profitable(self):
        link = Links("links.csv")
        res = link.most_profitable(3)

        assert isinstance(res, dict)
        assert len(res) <= 3
        assert all(isinstance(k, str) for k in res.keys())
        assert all(isinstance(v, int) for v in res.values())

        if res:
            vals = list(res.values())
            assert vals == sorted(vals, reverse=True)

    def test_longest_for_links(self):
        link = Links("links.csv")
        res = link.longest(3)

        assert isinstance(res, dict)
        assert len(res) <= 3
        assert all(isinstance(k, str) for k in res.keys())
        assert all(isinstance(v, str) for v in res.values())

        if res:
            mins = []
            for s in res.values():
                m = re.search(r"\((\d+)\s*min\)", s)
                assert m is not None
                mins.append(int(m.group(1)))
            assert mins == sorted(mins, reverse=True)

    def test_top_cost_per_minute(self):
        link = Links("links.csv")
        res = link.top_cost_per_minute(3)

        assert isinstance(res, dict)
        assert len(res) <= 3
        assert all(isinstance(k, str) for k in res.keys())
        assert all(isinstance(v, float) for v in res.values())

        if res:
            assert all(round(v, 2) == v for v in res.values())
            vals = list(res.values())
            assert vals == sorted(vals, reverse=True)

    def test_links_n_edge_cases(self):
        link = Links("links.csv")

        assert len(link.top_directors(0)) == 0
        assert len(link.most_expensive(0)) == 0
        assert len(link.most_profitable(0)) == 0
        assert len(link.longest(0)) == 0
        assert len(link.top_cost_per_minute(0)) == 0

        with pytest.raises(Exception):
            link.top_directors(-1)
        with pytest.raises(Exception):
            link.most_expensive(-1)
        with pytest.raises(Exception):
            link.most_profitable(-1)
        with pytest.raises(Exception):
            link.longest(-1)
        with pytest.raises(Exception):
            link.top_cost_per_minute(-1)

    def test_get_number_and_get_time(self):
        assert Links.get_number("$65,000,000 (estimated)") == 65000000
        assert Links.get_number("Unknown field") is None

        assert Links.get_time("(104 min)") == 104
        assert Links.get_time("104m") == 104
        assert Links.get_time("Unknown field") is None


if __name__ == "__main__":
    pass


