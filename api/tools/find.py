#  olly-tools-api | find.py
#  Last modified: 06/07/2022, 21:07
#  Copyright (c) 2022 Olly (https://olly.ml/). All rights reserved.

from fastapi import APIRouter, Response, Request, Form

router = APIRouter(
    prefix="/find",
    tags=["find"],
)


@router.get("/fib", summary="Find the nth digit of the fibonacci sequence")
def fibonacci(response: Response, n: int):
    if n < 0:
        response.status_code = 400
        return {"error": "n must be greater than or equal to 0"}
    elif n > 100:
        response.status_code = 400
        return {"error": "n must be less than or equal to 100"}
    else:
        def fib(n):
            if n < 2:
                return n
            return fib(n - 1) + fib(n - 2)
        nth_term = fib(n)
        return {"value": nth_term}


@router.get("/prime-factors", summary="Find all prime factors of a given number")
def prime_factors(response: Response, n: int):
    if n < 0:
        response.status_code = 400
        return {"error": "n must be greater than or equal to 0"}
    elif n > 1000:
        response.status_code = 400
        return {"error": "n must be less than or equal to 1000"}
    else:
        prime = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101,
                 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199,
                 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317,
                 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443,
                 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577,
                 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701,
                 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839,
                 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983,
                 991, 997]
        complete = False
        factors = []

        while not complete:
            if n == 1:
                complete = True
            for num in prime:
                if n % num == 0:
                    factors.append(num)
                    n = n / num
                    break

        return {"factors": factors}


@router.post("/char-count", summary="Count the number of characters in a string")
def count_char(response: Response, text: str = Form(None)):
    return {"count": len(text)}


@router.post("/words-count", summary="Count the number of words in a given string")
def count_words(response: Response, text: str = Form(None)):
    words = text.split()
    return {"count": len(words)}


@router.post("/sentences-count", summary="Count the number of sentences in a given string")
def count_sentences(response: Response, text: str = Form(None)):
    sentences = text.split(".")
    return {"count": len(sentences)}


@router.get("/reverse", summary="Reverse a string")
def reverse(response: Response, text: str):
    return {"text": text[::-1]}


@router.get("/palindrome", summary="Check if a string is a palindrome")
def palindrome(response: Response, text: str):
    return {"palindrome": text == text[::-1]}
