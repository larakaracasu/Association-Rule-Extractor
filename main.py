import sys
import csv
import itertools
from operator import itemgetter


def frequent_itemsets_1(data, min_support, item_sets):
    # generates frequent itemsets of size 1
    itemsets_1 = dict()
    num_rows = len(data)

    for row in data:  # parsing the input data here
        row = set(row) - {"UNKNOWN", "(null)", "U"}
        for item in row:
            tup = (item,)
            if tup in itemsets_1:
                itemsets_1[tup] += 1
            else:
                itemsets_1[tup] = 1

    # assigning support values and calculating frequent itemsets of size 1
    item_sets[1] = itemsets_1
    freq_itemsets_1 = dict()
    min_support_count = int(float(min_support) * num_rows)

    for item, sup_value in itemsets_1.items():
        if min_support_count <= sup_value:
            freq_itemsets_1[item] = sup_value

    return freq_itemsets_1


def get_candidate_itemsets(previous_frequent_itemsets):
    # we generate candidate itemsets of size k from frequent itemsets of size k-1
    current_candidates, new_candidates = list(), list()
    temp_length = 0

    # generating all combinations of the freq. itemsets
    for set1, set2 in itertools.combinations(previous_frequent_itemsets, 2):
        if set1[:-1] == set2[:-1]:
            combined_items = [set1[-1], set2[-1]]
            new_set = set1[:-1] + tuple(combined_items)
            current_candidates.append(new_set)
            temp_length = len(new_set)

    for itemset in current_candidates:  # filtering out invalid itemsets
        is_valid = True
        for subset in itertools.combinations(itemset, temp_length - 1):
            if subset not in previous_frequent_itemsets:
                is_valid = False
                break

        if is_valid:
            new_candidates.append(itemset)

    return new_candidates


def apriori_algorithm(data, minSup, item_sets, freq_items):
    freq_items[1] = frequent_itemsets_1(data, minSup, item_sets)
    prev_lk = list(freq_items[1].keys())

    # generating freq. itemsets of size k > 1
    for k in range(2, len(prev_lk)):
        cur_ck = get_candidate_itemsets(prev_lk)
        k_item_sets = dict()
        for row in data:
            ct = list(cur_ck)
            new_Ct = list()
            for itemset in ct:
                is_subset = True
                for item in itemset:
                    if item not in set(row):
                        is_subset = False
                        break
                if is_subset:
                    new_Ct.append(itemset)
            ct = new_Ct
            for candidate_ct in ct:
                if set(candidate_ct).issubset(set(row)):
                    if candidate_ct in k_item_sets:
                        k_item_sets[candidate_ct] += 1
                    else:
                        k_item_sets[candidate_ct] = 1

        item_sets[k] = k_item_sets
        k_freq_itemsets, cur_lk = dict(), list()

        for item, support in k_item_sets.items():
            if support >= float(minSup) * len(data):
                k_freq_itemsets[item] = support
                cur_lk.append(item)
        freq_items[k] = k_freq_itemsets
        prev_lk = cur_lk


def get_rules(data, rules):
    for rhs in freq_items[1].keys():
        for value in freq_items.values():
            for lhs, lhs_support in value.items():
                if not set(lhs).intersection(rhs):
                    for row in data:
                        if set(lhs).issubset(row) and set(rhs).issubset(row):
                            rule = "[" + ",".join(lhs) + "] ==> [" + rhs[0] + "]"
                            if rule in rules:
                                rules[rule][0] += 1
                            else:
                                rules[rule] = [1, lhs_support]


def sort_rules(rules):
    rules = sorted(
        rules.items(),
        key=lambda val: (float(val[1][0]) / float(val[1][1]), val[1][1]),
        reverse=True,
    )
    rules = dict(rules)
    return rules  # returns the sorted rules by confidence value


def write_output(output_filename, data, rules, min_support, min_confidence, length):
    with open(output_filename, "wt") as output:
        output.write(
            "==Frequent itemsets (min_sup=" + str(float(min_support) * 100) + "%)\n\n"
        )

        for tup in data:
            if (float(min_support)) * length > tup[1]:
                continue
            confidence = float(tup[1]) / float(length) * 100
            output.write("[" + ",".join(list(tup[0])) + "], " + str(confidence) + "%\n")

        output.write(
            "\n==High-confidence association rules (min_conf="
            + str(float(min_confidence) * 100)
            + "%)\n"
        )

        for tup in rules:
            confidence = float(rules[tup][0]) / float(rules[tup][1])
            support = float(rules[tup][1]) / float(length) * 100
            if (
                confidence >= float(min_confidence)
                and support > float(min_support) * 100
            ):
                output.write(
                    str(tup)
                    + " (Conf: "
                    + str(confidence * 100)
                    + "%, Supp: "
                    + str(support)
                    + "%)\n"
                )


if __name__ == "__main__":
    filename, min_support, min_confidence = sys.argv[1], sys.argv[2], sys.argv[3]
    item_sets, freq_items, rules = dict(), dict(), dict()
    output_filename = "output.txt"

    with open(filename, newline="") as csvfile:
        csv_data = [tuple(line) for line in csv.reader(csvfile)]
        apriori_algorithm(csv_data, min_support, item_sets, freq_items)
        get_rules(csv_data, rules)

        final_data = list()
        for x in freq_items.keys():
            for y in freq_items[x].keys():
                final_data.append([y, freq_items[x][y]])

        final_data = sorted(final_data, key=itemgetter(1), reverse=True)
        rules = sort_rules(rules)

        write_output(
            output_filename,
            final_data,
            rules,
            min_support,
            min_confidence,
            len(csv_data),
        )
