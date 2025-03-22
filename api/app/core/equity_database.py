import pandas as pd
import json, re
from Levenshtein import ratio
class EquityDatabase:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.df = pd.read_csv(data_path)
        self.df = self.df.replace([float("inf"), float("-inf")], value=0)
        self.df = self.df.fillna(0)  # Replace NaN values with 0

    @staticmethod
    def _test(index_value, test_str, ignore_distance=False) -> bool:
        index_value = str(index_value)
        pattern = re.compile(rf"^{re.escape(test_str)}", re.IGNORECASE)
        matches = pattern.findall(index_value)
        if ignore_distance:
            return bool(matches)
        
        if matches:
            distance = ratio(index_value.lower(), test_str.lower())
            if distance < 0.5:
                    return False
        return bool(matches)
    
    
    def search_equities(self, ticker): 
        equities=self.df.loc[self.df['symbol'].map(lambda x: self._test(x, ticker))]
        if len(equities) == 0:
            print('No equities found')
            return json.dumps([])
        else:
            if len(equities) >= 8:
                equities = equities.iloc[:8]
            pd.set_option('display.max_columns', None)
            print(equities)
            equities = equities.to_json(orient="records")
            return equities
        
    def get_all_equities(self):
        equities = self.df.to_json(orient="records")
        return equities
        
