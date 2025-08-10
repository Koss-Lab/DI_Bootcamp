# page_timer.py

import time
import statistics
from typing import Iterable, Tuple, Dict, Any

import requests


def measure_load_time(
    url: str,
    method: str = "GET",
    timeout: float = 10.0,
    allow_redirects: bool = True,
    verify_ssl: bool = True,
    force_download: bool = True,
    session: requests.Session | None = None,
) -> Tuple[float | None, Dict[str, Any]]:
    """
    Measure the time to obtain a complete HTTP response for a URL.

    Returns:
        (elapsed_seconds or None on failure, info dict)
    """
    sess = session or requests.Session()
    sess.headers.update(
        {
            "User-Agent": "PageTimer/1.0 (+https://example.local) requests",
            "Accept": "*/*",
        }
    )

    method = method.upper()
    if method not in {"GET", "HEAD"}:
        raise ValueError("method must be 'GET' or 'HEAD'")

    try:
        start = time.perf_counter()
        resp = sess.request(
            method,
            url,
            timeout=timeout,
            allow_redirects=allow_redirects,
            verify=verify_ssl,
            stream=True,  # we'll control body consumption
        )

        # Consume the response body so timing includes content transfer.
        # For HEAD, there is usually no body, but we keep the logic unified.
        if force_download and method == "GET":
            for _ in resp.iter_content(chunk_size=64 * 1024):
                pass
        else:
            # Touch content anyway to ensure headers are fully processed
            _ = resp.content if method == "GET" else None

        elapsed = time.perf_counter() - start
        info = {
            "status_code": resp.status_code,
            "url_final": resp.url,
            "content_length": int(resp.headers.get("Content-Length") or -1),
            "ok": resp.ok,
        }
        return elapsed, info

    except requests.exceptions.RequestException as e:
        return None, {"error": type(e).__name__, "message": str(e)}


def benchmark_sites(
    urls: Iterable[str],
    runs: int = 3,
    **kwargs,
) -> Dict[str, Dict[str, float | str | Dict[str, Any]]]:
    """
    Run multiple measurements per URL and summarize results.
    Returns a dict mapping url -> summary.
    """
    results: Dict[str, Dict[str, float | str | Dict[str, Any]]] = {}
    with requests.Session() as sess:
        for url in urls:
            times = []
            last_info: Dict[str, Any] = {}
            for _ in range(runs):
                t, info = measure_load_time(url, session=sess, **kwargs)
                last_info = info
                if t is not None:
                    times.append(t)
            if times:
                results[url] = {
                    "runs": runs,
                    "successes": len(times),
                    "min_s": min(times),
                    "avg_s": statistics.fmean(times),
                    "max_s": max(times),
                    "last_info": last_info,
                }
            else:
                results[url] = {
                    "runs": runs,
                    "successes": 0,
                    "error": last_info.get("error", "UnknownError"),
                    "message": last_info.get("message", ""),
                }
    return results


if __name__ == "__main__":
    test_urls = [
        "https://www.google.com",
        "https://www.ynet.co.il",
        "https://www.imdb.com",
    ]

    # Tip: if your network does SSL inspection or blocks traffic,
    # you can try verify_ssl=False (not recommended in production)
    summary = benchmark_sites(
        test_urls,
        runs=3,
        method="GET",
        timeout=10.0,
        allow_redirects=True,
        verify_ssl=True,       # set to False only if you must bypass SSL verification
        force_download=True,   # True measures full body download time
    )

    # Pretty print
    for url, data in summary.items():
        print(f"\n=== {url} ===")
        if data.get("successes", 0) > 0:
            print(f"Runs        : {data['runs']} (successes: {data['successes']})")
            print(f"Min         : {data['min_s']:.3f}s")
            print(f"Average     : {data['avg_s']:.3f}s")
            print(f"Max         : {data['max_s']:.3f}s")
            info = data.get("last_info", {})
            print(f"Status Code : {info.get('status_code')}")
            print(f"Final URL   : {info.get('url_final')}")
            print(f"Content-Len : {info.get('content_length')}")
        else:
            print("All attempts failed.")
            print(f"Error       : {data.get('error')}")
            print(f"Message     : {data.get('message')}")
