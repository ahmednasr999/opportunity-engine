#!/usr/bin/env python3
"""
2nd Brain - Semantic search across all documents, CVs, job postings
"""

import json
import os
import re
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import hashlib

@dataclass
class Document:
    """A document in the 2nd Brain"""
    id: str
    title: str
    content: str
    doc_type: str  # cv, job_posting, linkedin_post, note, email, etc.
    source: str  # file path or URL
    tags: List[str]
    created_at: str
    updated_at: str
    metadata: Dict

@dataclass
class SearchResult:
    """Search result with relevance score"""
    document: Document
    score: float
    matched_terms: List[str]
    excerpt: str


class SimpleVectorStore:
    """Simple keyword-based vector store (semantic-lite)"""
    
    def __init__(self):
        self.documents: Dict[str, Document] = {}
        self.inverted_index: Dict[str, List[str]] = {}  # term -> doc_ids
        self.doc_term_freq: Dict[str, Dict[str, int]] = {}  # doc_id -> {term: freq}
    
    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into terms"""
        # Simple tokenization
        text = text.lower()
        # Remove special chars, keep alphanumeric and spaces
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        # Split and filter
        terms = [t.strip() for t in text.split() if len(t.strip()) > 2]
        return terms
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from text"""
        terms = self._tokenize(text)
        
        # Common stop words to filter
        stop_words = {
            'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was',
            'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'its', 'may', 'new',
            'now', 'old', 'see', 'two', 'who', 'boy', 'did', 'she', 'use', 'her', 'way', 'many',
            'oil', 'sit', 'set', 'run', 'eat', 'far', 'sea', 'eye', 'ago', 'off', 'too', 'any',
            'say', 'man', 'try', 'ask', 'end', 'why', 'let', 'put', 'say', 'she', 'try', 'way',
            'own', 'say', 'too', 'old', 'tell', 'very', 'when', 'come', 'here', 'just', 'like',
            'long', 'make', 'over', 'such', 'take', 'than', 'them', 'well', 'were', 'with',
            'this', 'that', 'have', 'from', 'they', 'know', 'want', 'been', 'good', 'much',
            'some', 'time', 'very', 'what', 'would', 'there', 'their', 'said', 'each',
            'which', 'will', 'about', 'if', 'out', 'many', 'then', 'them', 'these', 'so',
            'some', 'her', 'would', 'make', 'like', 'into', 'him', 'time', 'has', 'two',
            'more', 'go', 'no', 'way', 'could', 'my', 'than', 'first', 'water', 'been',
            'call', 'who', 'its', 'now', 'find', 'long', 'down', 'day', 'did', 'get',
            'come', 'made', 'may', 'part', 'over', 'also', 'after', 'back', 'other',
            'many', 'than', 'them', 'these', 'well', 'were', 'your', 'said', 'each',
            'she', 'which', 'do', 'how', 'their', 'if', 'up', 'out', 'many', 'then',
            'them', 'would', 'there', 'into', 'school', 'more', 'land', 'only', 'most'
        }
        
        # Filter stop words and return unique terms
        keywords = list(set([t for t in terms if t not in stop_words]))
        return keywords
    
    def add_document(self, doc: Document):
        """Add a document to the store"""
        self.documents[doc.id] = doc
        
        # Extract terms
        terms = self._extract_keywords(doc.content + " " + doc.title)
        
        # Update inverted index
        for term in terms:
            if term not in self.inverted_index:
                self.inverted_index[term] = []
            if doc.id not in self.inverted_index[term]:
                self.inverted_index[term].append(doc.id)
        
        # Store term frequencies
        term_freq = {}
        for term in terms:
            term_freq[term] = term_freq.get(term, 0) + 1
        self.doc_term_freq[doc.id] = term_freq
    
    def search(self, query: str, top_k: int = 10) -> List[SearchResult]:
        """Search for documents matching query"""
        query_terms = self._extract_keywords(query)
        
        if not query_terms:
            return []
        
        # Find candidate documents
        candidate_scores: Dict[str, float] = {}
        matched_terms: Dict[str, List[str]] = {}
        
        for term in query_terms:
            for doc_id in self.inverted_index.get(term, []):
                if doc_id not in candidate_scores:
                    candidate_scores[doc_id] = 0
                    matched_terms[doc_id] = []
                
                # Simple TF scoring
                tf = self.doc_term_freq[doc_id].get(term, 0)
                candidate_scores[doc_id] += tf
                matched_terms[doc_id].append(term)
        
        # Normalize by document length
        for doc_id in candidate_scores:
            doc_len = sum(self.doc_term_freq[doc_id].values())
            if doc_len > 0:
                candidate_scores[doc_id] /= doc_len
        
        # Sort by score
        sorted_results = sorted(candidate_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Build search results
        results = []
        for doc_id, score in sorted_results[:top_k]:
            doc = self.documents[doc_id]
            
            # Generate excerpt around matched terms
            excerpt = self._generate_excerpt(doc.content, matched_terms[doc_id])
            
            results.append(SearchResult(
                document=doc,
                score=score,
                matched_terms=matched_terms[doc_id],
                excerpt=excerpt
            ))
        
        return results
    
    def _generate_excerpt(self, content: str, matched_terms: List[str], max_length: int = 200) -> str:
        """Generate excerpt highlighting matched terms"""
        content_lower = content.lower()
        
        # Find first occurrence of any matched term
        best_pos = -1
        for term in matched_terms:
            pos = content_lower.find(term)
            if pos != -1 and (best_pos == -1 or pos < best_pos):
                best_pos = pos
        
        if best_pos == -1:
            return content[:max_length] + "..." if len(content) > max_length else content
        
        # Extract surrounding text
        start = max(0, best_pos - 50)
        end = min(len(content), best_pos + max_length)
        excerpt = content[start:end]
        
        if start > 0:
            excerpt = "..." + excerpt
        if end < len(content):
            excerpt = excerpt + "..."
        
        return excerpt


class SecondBrain:
    """Personal knowledge management system"""
    
    def __init__(self, data_dir: str = "/root/.openclaw/workspace/tools/cv-optimizer/data"):
        self.data_dir = Path(data_dir)
        self.brain_file = self.data_dir / "second_brain.json"
        self.vector_store = SimpleVectorStore()
        self.load()
    
    def load(self):
        """Load brain from disk"""
        if self.brain_file.exists():
            with open(self.brain_file, 'r') as f:
                data = json.load(f)
                for doc_data in data.get('documents', []):
                    doc = Document(**doc_data)
                    self.vector_store.add_document(doc)
    
    def save(self):
        """Save brain to disk"""
        data = {
            'documents': [asdict(doc) for doc in self.vector_store.documents.values()],
            'updated_at': datetime.now().isoformat()
        }
        with open(self.brain_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def ingest_cv(self, cv_text: str, title: str = "CV"):
        """Ingest a CV document"""
        doc_id = hashlib.md5(cv_text.encode()).hexdigest()[:8]
        
        doc = Document(
            id=doc_id,
            title=title,
            content=cv_text,
            doc_type="cv",
            source="user_upload",
            tags=["cv", "profile", "experience"],
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            metadata={"version": "1.0"}
        )
        
        self.vector_store.add_document(doc)
        self.save()
        return doc_id
    
    def ingest_job_posting(self, job_text: str, company: str, title: str):
        """Ingest a job posting"""
        doc_id = hashlib.md5((company + title).encode()).hexdigest()[:8]
        
        doc = Document(
            id=doc_id,
            title=f"{title} at {company}",
            content=job_text,
            doc_type="job_posting",
            source="user_input",
            tags=["job", "opportunity", company.lower().replace(" ", "_")],
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            metadata={"company": company, "title": title}
        )
        
        self.vector_store.add_document(doc)
        self.save()
        return doc_id
    
    def ingest_note(self, content: str, title: str, tags: List[str] = None):
        """Ingest a personal note"""
        doc_id = hashlib.md5((title + content[:100]).encode()).hexdigest()[:8]
        
        doc = Document(
            id=doc_id,
            title=title,
            content=content,
            doc_type="note",
            source="user_input",
            tags=tags or ["note"],
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            metadata={}
        )
        
        self.vector_store.add_document(doc)
        self.save()
        return doc_id
    
    def search(self, query: str, doc_type: str = None, top_k: int = 10) -> List[SearchResult]:
        """Search the brain"""
        results = self.vector_store.search(query, top_k=top_k * 2)  # Get extra for filtering
        
        if doc_type:
            results = [r for r in results if r.document.doc_type == doc_type]
        
        return results[:top_k]
    
    def get_by_type(self, doc_type: str) -> List[Document]:
        """Get all documents of a type"""
        return [doc for doc in self.vector_store.documents.values() if doc.doc_type == doc_type]
    
    def get_stats(self) -> Dict:
        """Get brain statistics"""
        docs = list(self.vector_store.documents.values())
        
        by_type = {}
        for doc in docs:
            by_type[doc.doc_type] = by_type.get(doc.doc_type, 0) + 1
        
        return {
            "total_documents": len(docs),
            "by_type": by_type,
            "unique_terms": len(self.vector_store.inverted_index),
            "last_updated": datetime.now().isoformat()
        }
    
    def find_similar_jobs(self, cv_doc_id: str, top_k: int = 5) -> List[SearchResult]:
        """Find job postings similar to a CV"""
        cv_doc = self.vector_store.documents.get(cv_doc_id)
        if not cv_doc:
            return []
        
        # Use CV content as query
        results = self.vector_store.search(cv_doc.content, top_k=top_k * 2)
        
        # Filter to job postings only
        job_results = [r for r in results if r.document.doc_type == "job_posting"]
        
        return job_results[:top_k]
    
    def export_knowledge_base(self, filepath: str = None):
        """Export entire knowledge base"""
        if filepath is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"/root/.openclaw/workspace/tools/cv-optimizer/output/second_brain_export_{timestamp}.json"
        
        data = {
            'export_date': datetime.now().isoformat(),
            'stats': self.get_stats(),
            'documents': [asdict(doc) for doc in self.vector_store.documents.values()]
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        return filepath


def main():
    """CLI interface"""
    import sys
    
    brain = SecondBrain()
    
    if len(sys.argv) < 2:
        print("2nd Brain - Personal Knowledge Management")
        print()
        print("Usage:")
        print("  python second_brain.py search <query> [doc_type]")
        print("  python second_brain.py stats")
        print("  python second_brain.py ingest <type> <file>")
        print("  python second_brain.py similar <cv_id>")
        print()
        print("Examples:")
        print("  python second_brain.py search 'AI healthcare'")
        print("  python second_brain.py search 'project management' job_posting")
        print("  python second_brain.py stats")
        return
    
    command = sys.argv[1]
    
    if command == "search":
        if len(sys.argv) < 3:
            print("Usage: python second_brain.py search <query> [doc_type]")
            return
        
        query = sys.argv[2]
        doc_type = sys.argv[3] if len(sys.argv) > 3 else None
        
        results = brain.search(query, doc_type, top_k=10)
        
        print(f"\n🔍 Search results for: '{query}'")
        if doc_type:
            print(f"   Filtered by type: {doc_type}")
        print("=" * 60)
        
        if not results:
            print("No results found.")
            return
        
        for i, result in enumerate(results, 1):
            doc = result.document
            print(f"\n{i}. {doc.title}")
            print(f"   Type: {doc.doc_type} | Score: {result.score:.3f}")
            print(f"   Matched: {', '.join(result.matched_terms[:5])}")
            print(f"   {result.excerpt[:150]}...")
    
    elif command == "stats":
        stats = brain.get_stats()
        print("\n📊 2nd Brain Statistics")
        print("=" * 40)
        print(f"Total Documents: {stats['total_documents']}")
        print(f"Unique Terms: {stats['unique_terms']}")
        print()
        print("By Type:")
        for doc_type, count in stats['by_type'].items():
            print(f"  {doc_type}: {count}")
    
    elif command == "ingest":
        if len(sys.argv) < 4:
            print("Usage: python second_brain.py ingest <type> <file>")
            return
        
        doc_type = sys.argv[2]
        filepath = sys.argv[3]
        
        with open(filepath, 'r') as f:
            content = f.read()
        
        if doc_type == "cv":
            doc_id = brain.ingest_cv(content, Path(filepath).stem)
        elif doc_type == "job":
            doc_id = brain.ingest_job_posting(content, "Unknown", "Unknown Position")
        else:
            doc_id = brain.ingest_note(content, Path(filepath).stem)
        
        print(f"✅ Ingested {doc_type}: {doc_id}")
    
    elif command == "similar":
        if len(sys.argv) < 3:
            print("Usage: python second_brain.py similar <cv_id>")
            return
        
        cv_id = sys.argv[2]
        results = brain.find_similar_jobs(cv_id)
        
        print(f"\n🎯 Jobs similar to CV {cv_id}")
        print("=" * 60)
        
        for result in results:
            doc = result.document
            print(f"\n• {doc.title}")
            print(f"  Score: {result.score:.3f}")
            print(f"  {result.excerpt[:100]}...")
    
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
