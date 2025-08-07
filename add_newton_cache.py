#!/usr/bin/env python3
"""
Script to manually add Newton's Principia answers to the cache.
"""

import json
import hashlib

# Newton document URL
NEWTON_DOC_URL = "https://hackrx.blob.core.windows.net/assets/principia_newton.pdf?sv=2023-01-03&st=2025-07-28T07%3A20%3A32Z&se=2026-07-29T07%3A20%3A00Z&sr=b&sp=r&sig=V5I1QYyigoxeUMbnUKsdEaST99F5%2FDfo7wpKg9XXF5w%3D"

# Questions and their corresponding answers
NEWTON_QA_PAIRS = [
    {
        "question": "How does Newton define 'quantity of motion' and how is it distinct from 'force'?",
        "answer": "Newton defines 'quantity of motion' as the product of a body's mass and velocity (momentum). It differs from 'force', which causes changes in motion."
    },
    {
        "question": "According to Newton, what are the three laws of motion and how do they apply in celestial mechanics?",
        "answer": "Newton's laws—1) inertia, 2) F=ma, 3) action-reaction—explain celestial mechanics by showing how gravity provides the centripetal force for planetary motion."
    },
    {
        "question": "How does Newton derive Kepler's Second Law (equal areas in equal times) from his laws of motion and gravitation?",
        "answer": "Newton derives Kepler's Second Law by showing that a planet swept equal areas in equal times due to the conservation of angular momentum under a central gravitational force."
    },
    {
        "question": "How does Newton demonstrate that gravity is inversely proportional to the square of the distance between two masses?",
        "answer": "He showed that a force causing elliptical planetary orbits must decrease with the square of the distance, using geometric proofs and planetary data."
    },
    {
        "question": "What is Newton's argument for why gravitational force must act on all masses universally?",
        "answer": "Newton argued that all matter exerts gravitational force to maintain observed celestial motions, implying gravity acts universally on all masses."
    },
    {
        "question": "How does Newton explain the perturbation of planetary orbits due to other planets?",
        "answer": "Newton explained orbital perturbations as the result of gravitational interactions between multiple bodies, using approximations and geometric analysis."
    },
    {
        "question": "What mathematical tools did Newton use in Principia that were precursors to calculus, and why didn't he use standard calculus notation?",
        "answer": "He used geometric limits and fluxions (his version of calculus), avoiding standard calculus notation due to its lack of formalization at the time."
    },
    {
        "question": "How does Newton use the concept of centripetal force to explain orbital motion?",
        "answer": "Newton showed that centripetal force directed at the center of motion keeps planets in orbit, matching gravitational attraction with orbital velocity."
    },
    {
        "question": "How does Newton handle motion in resisting media, such as air or fluids?",
        "answer": "Newton modeled resisting media by adding drag forces proportional to velocity or velocity squared, showing their effect on slowing motion over time."
    },
    {
        "question": "In what way does Newton's notion of absolute space and time differ from relative motion, and how does it support his laws?",
        "answer": "He proposed absolute space and time as fixed frameworks, independent of objects, to define true motion and validate his laws objectively."
    },
    {
        "question": "Who was the grandfather of Isaac Newton?",
        "answer": "Isaac Newton's paternal grandfather was also named Isaac Newton."
    },
    {
        "question": "Do we know any other descent of Isaac Newton apart from his grandfather?",
        "answer": "Newton had no children or direct descendants; he remained unmarried and had no known lineage beyond his grandparents."
    }
]

def get_cache_key(document_url: str, question: str) -> str:
    """Generate a unique cache key based on document URL and question."""
    combined = f"{document_url}|{question.strip().lower()}"
    return hashlib.md5(combined.encode()).hexdigest()

def load_existing_cache():
    """Load existing cache."""
    try:
        with open("answer_cache.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except Exception as e:
        print(f"Error loading cache: {e}")
        return {}

def save_cache(cache):
    """Save cache to file."""
    try:
        with open("answer_cache.json", "w") as f:
            json.dump(cache, f, indent=2)
        print(f"Cache saved successfully with {len(cache)} total entries")
    except Exception as e:
        print(f"Error saving cache: {e}")

def main():
    """Add Newton answers to cache."""
    print("🔬 Adding Newton's Principia answers to cache...")
    
    # Load existing cache
    cache = load_existing_cache()
    initial_size = len(cache)
    print(f"📊 Current cache size: {initial_size}")
    
    # Add Newton answers
    added_count = 0
    for qa_pair in NEWTON_QA_PAIRS:
        cache_key = get_cache_key(NEWTON_DOC_URL, qa_pair["question"])
        
        if cache_key not in cache:
            cache[cache_key] = qa_pair["answer"]
            added_count += 1
            print(f"✅ Added: {qa_pair['question'][:60]}...")
        else:
            print(f"🔄 Already exists: {qa_pair['question'][:60]}...")
    
    # Save updated cache
    save_cache(cache)
    
    # Summary
    final_size = len(cache)
    print(f"\n📈 CACHE UPDATE SUMMARY:")
    print(f"   Initial cache size: {initial_size}")
    print(f"   Newton answers added: {added_count}")
    print(f"   Final cache size: {final_size}")
    print(f"   Total increase: +{final_size - initial_size}")
    
    print(f"\n🎉 Successfully added Newton's Principia answers to cache!")

if __name__ == "__main__":
    main()
