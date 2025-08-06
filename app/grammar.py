import logging
from typing import List
from .ollama_client import query_ollama
from .models import GrammarIssue
from .exceptions import GrammarCheckError

logger = logging.getLogger(__name__)

async def check_grammar(text: str) -> List[GrammarIssue]:
    if not text or not text.strip():
        return []
    
    try:
        issues_data = await query_ollama(text)
        
        if not issues_data:
            return []
        
        issues = []
        for issue in issues_data:
            try:
                grammar_issue = GrammarIssue(
                    wrong=issue.get("wrong", ""),
                    corrected=issue.get("corrected", ""),
                    error_type=issue.get("error_type", "unknown")
                )
                issues.append(grammar_issue)
            except Exception as e:
                logger.warning(f"Skipping invalid issue: {e}")
                continue
        
        return issues
        
    except GrammarCheckError:
        raise
    except Exception as e:
        raise GrammarCheckError(f"Grammar check failed: {e}")

