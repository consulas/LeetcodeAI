from collections import Counter
from typing import List

class Solution:
    def find_special_interests(self, boards: List[List[int]]) -> List[int]:
        special_interests = []
        
        for board in boards:
            interest_count = Counter(board)
            special_interests.append(interest_count.most_common()[1][0])
        
        return special_interests