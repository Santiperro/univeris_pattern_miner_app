from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
from common_imports import *


def mine_patterns(transactions_matrix: pd.DataFrame, 
                  min_supp: float, 
                  min_lift: float, 
                  min_conf: float, 
                  max_left_elements: int, 
                  max_right_elements: int) -> pd.DataFrame:
    """
    Function to search for patterns in the transaction matrix.

    Args:
        transactions_matrix (DataFrame): The transaction matrix.
        min_supp (float): Minimum support value.
        min_lift (float): Minimum lift value.
        min_conf (float): Minimum confidence value.
        max_left_elements (int): Maximum number of elements in antecedents.
        max_right_elements (int): Maximum number of elements in consequents.

    Returns:
        DataFrame: DataFrame containing the found associative rules.
    """
    def cell_to_string(cell):
        if not isinstance(cell, str):
            try:
                iter(cell)
                string = ""
                for item in cell:
                    string += f"({item}), "
                string = string[:-2]
                return string
            except TypeError:
                pass
        return cell

    # Поиск частых наборов с параметром минимальной поддержки
    freaquent_itemsets = apriori(transactions_matrix, 
                                 min_support=min_supp, 
                                 use_colnames=True)

    # Поиск ассоциативных правил с заданной метрикой и её минимальным значением
    rules = association_rules(freaquent_itemsets, 
                              metric='lift', 
                              min_threshold=min_lift)

    # Редактирование столбцов
    rules.drop('antecedent support', axis=1, inplace=True)
    rules.drop('consequent support', axis=1, inplace=True)
    rules.drop('leverage', axis=1, inplace=True)
    rules.drop('conviction', axis=1, inplace=True)
    if "zhangs_metric" in rules.columns:
        rules.drop('zhangs_metric', axis=1, inplace=True)
    rules["support"] = rules["support"].round(4)
    rules["confidence"] = rules["confidence"].round(4)
    rules["lift"] = rules["lift"].round(4)

    if min_conf:
        rules = rules[rules["confidence"] >= min_conf]
        
    rules["antecedents"] = rules["antecedents"].apply(lambda x: x if len(x) <= max_left_elements else None)
    rules["consequents"] = rules["consequents"].apply(lambda x: x if len(x) <= max_right_elements else None)
    rules["antecedents"] = rules["antecedents"].apply(lambda x: cell_to_string(x))
    rules["consequents"] = rules["consequents"].apply(lambda x: cell_to_string(x))

    return rules.dropna()