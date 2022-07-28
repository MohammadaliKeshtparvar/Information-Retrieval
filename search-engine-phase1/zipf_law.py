import pickle
import math
import matplotlib.pyplot as plt

inverted_index = pickle.load(open("../inverted-index-with-stopwords.dat", "rb"))
inverted_index = {k: v for k, v in sorted(inverted_index.items(), key=lambda item: item[1].allFrequency, reverse=True)}
key_list = list(inverted_index.keys())
all_frequency_list = [x.allFrequency for x in inverted_index.values()]
max_frequency = all_frequency_list[0]

cf_real = [math.log10(i) for i in all_frequency_list]
rank = [math.log10(i + 1) for i in range(len(key_list))]
cf_expected = [math.log10(max_frequency / (i + 1)) for i in range(len(key_list))]

plt.title('with stopwords')
plt.plot(rank, cf_expected)
plt.plot(rank, cf_real)
plt.legend(["expected", "real"])
plt.xlabel("log10 Rank")
plt.ylabel("log10 cf")
plt.show()
