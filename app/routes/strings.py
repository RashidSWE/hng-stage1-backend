from fastapi import APIRouter, HTTPException, status, Query
from ..utils.helper import length, is_palindrome, unique_characters, word_count, sha256_hash, character_frequency_map
from ..models.model import Strings, Analyze_string
from ..config.config import string_collection
from typing import Optional
import re


router = APIRouter()

@router.post("/strings", response_model=Analyze_string, status_code=status.HTTP_201_CREATED)
async def strings(string: Strings):

    if not string.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid request body or missing value field",
        )
    if not isinstance(string.value, str):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid data type for value(must be string)"
        )

    computed_hash = sha256_hash(string.value)
    stored_strings = string_collection.find_one({"id": computed_hash})

    if stored_strings:
        raise HTTPException(status_code=409, detail="String already exists in the system")
    

    properties = {
        "length": length(string.value),
        "is_palindrome": is_palindrome(string.value),
        "unique_characters": unique_characters(string.value),
        "word_count": word_count(string.value),
        "sha256_hash": computed_hash,
        "character_frequency_map": character_frequency_map(string.value)
    }

    document = {
        "id": computed_hash,
        "value": string.value,
        "properties": properties,
    }

    string_collection.insert_one(document)

    return document


@router.get("/strings", status_code=status.HTTP_200_OK)
async def filter_strings(
    is_palindrome: Optional[bool] = Query(None, description="Filter by palindrome status"),
    min_length: Optional[int] = Query(None, ge=1, description="Minimum string length"),
    max_length: Optional[int] = Query(None, ge=1, description="Maximum string length" ),
    word_count: Optional[int] = Query(None, description="exact word count"),
    contains_character: Optional[str] = Query(None, description="single character to search for"),
):
    query = {}

    if is_palindrome is not None:
        query["properties.is_palindrome"] = is_palindrome
    
    if min_length is not None or max_length is not None:
        query["properties.length"] = {}

        if min_length is not None:
            query["properties.length"]["$gte"] = min_length
        
        if max_length is not None:
            query["properties.length"]["$lte"] = max_length
        
    if word_count is not None:
        query["properties.word_count"] = word_count
    
    if contains_character:
        query["value"] = {"$regex": contains_character, "$options": "i"}
    

    results = list(string_collection.find(query, {"_id": 0}))


    if not results:
        raise HTTPException(status_code=404, detail="Invalid query parameter values or types")
    
    filters_applied = {
        "is_palindrome": is_palindrome,
        "min_length": min_length,
        "max_length": max_length,
        "word_count": word_count,
        "contains_character": contains_character
    }
    
    return {"data": results, "count": len(results), "filters_applied": filters_applied }

@router.get("/strings/filter-by-natural-language")
async def filter_by_natural_language(
    query: str = Query(..., description="Natural Language Filtering")
):
    """ Normalize text """
    print(f"Incoming query param: {query!r}")

    q_lower = query.lower().strip()
    mongo_query = {}
    parsed_filters = {}

    """---Palindrome Query---"""
    if "palindrome" in q_lower or "palindromic" in q_lower:
        mongo_query["properties.is_palindrome"] = True
        parsed_filters["is_palindrome"] = True
    elif "not palindrome" in q_lower:
        mongo_query["properties.is_palindrome"] = False
        parsed_filters["is_palindrome"] = False
    
    """ Word count (e.g "qingle word", "one word")"""
    if "single word" in q_lower or "one word" in q_lower:
        mongo_query["properties.word_count"] = 1
        parsed_filters["word_count"] = 1
    else:
        match_word = re.search(r"(\d+)\s+word", q_lower)
        if match_word:
            mongo_query["properties.word_count"] = int(match_word.group(1))
            parsed_filters["word_count"] = int(match_word.group(1))
    
    # --- Length Detection ----
    # longer/greater/above 10 characters
    match_longer = re.search(r"(?:longer|greater|above|more than)\s+(?:than\s+)?(\d+)", q_lower)

    # shorter/less than 10 characters
    match_shorter = re.search(r"(?:shorter|less than|under)\s+(?:than\s+)?(\d+)", q_lower)

    if match_longer or match_shorter:
        mongo_query["properties.length"] = {}

        if match_longer:
            val = int(match_longer.group(1))
            mongo_query["properties.length"]["$gte"] = val + 1
            parsed_filters["min_length"] = val + 1
        if match_shorter:
            val = int(match_shorter.group(1))
            mongo_query["properties.length"]["$lte"] = val - 1
            parsed_filters["max_length"] = val - 1
        
    
    # --- CHARACTER CONTAINS ----
    match_char = re.search(r"contain(?:s|ing)?(?: the letter)? (\w)", q_lower)

    if match_char:
        char = match_char.group(1)
        mongo_query["value"] = {"$regex": char, "$options": "i"}
        parsed_filters["contains_character"] = char
    
    # ---Handle first vower or vowel keywords
    if "first vowel" in q_lower or "vowel" in q_lower:
        mongo_query.setdefault("value", {"$regex": "[aeiou]", "$options": "i"})
        parsed_filters["contains_character"] = "a (any vowel)"


    if "min_length" in parsed_filters and "max_length" in parsed_filters:
        if parsed_filters["min_length"] > parsed_filters["max_length"]:
            raise HTTPException(
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Query parsed but resulted in conflicting filters"
            )
        
    if not parsed_filters:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to parse natural language query"
        )

    results = list(string_collection.find(mongo_query, {"_id": 0}))


    if not results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No strings matched query"
        )
    
    
    return {
        "data": results,
        "count": len(results),
        "interpreted_query": {
            "original": query,
            "parsed_filters": parsed_filters
        }
    }


@router.get("/strings/{string_value}", response_model=Analyze_string, status_code=status.HTTP_200_OK)
async def get_string(string_value: str):
    compute_hash = sha256_hash(string_value)
    string_doc = string_collection.find_one({"id": compute_hash})

    if not string_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="string does not exist in the system"
        )
    return {
        "id": string_doc.get("id"),
        "value": string_doc.get("value"),
        "properties": string_doc.get("properties")
    }

@router.delete("/strings/{string_value}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_string(string_value: str):
    compute_hash = sha256_hash(string_value)
    stored_string = string_collection.find_one({"id": compute_hash})

    if not stored_string:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="String does not exist in the system"
        )
    
    """ Delete the string """
    string_collection.delete_one({"id": compute_hash})

    return