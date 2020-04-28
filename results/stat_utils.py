import math
from random import random
from datetime import datetime
from scipy.special import erf
from scipy.stats import ttest_ind
from scipy.stats import t
import numpy as np
import json

def confidence_intervals(sample_mean, sd, num_samples, one_tailed=True):
  sampling_error = sd / math.sqrt(num_samples)
  def ci(p):
    df = num_samples - 1
    t_crit = t.ppf(p, df)
    moe = t_crit * sampling_error
    upper = sample_mean + moe
    lower = sample_mean - moe
    return t_crit, moe, upper, lower
  res = {'0.95': {}, '0.99': {}}
  res['0.95']['tcrit'], res['0.95']['moe'], res['0.95']['upper'], res['0.95']['lower'] = ci(0.95 if one_tailed else 0.975)
  res['0.99']['tcrit'], res['0.99']['moe'], res['0.99']['upper'], res['0.99']['lower'] = ci(0.99 if one_tailed else 0.995)
  return res

def t_stat(sample_mean, num_samples, sd, pop_mean, one_sided=True, alpha=0.05):
  df = num_samples - 1
  sems = sd / np.sqrt(num_samples)
  t = (sample_mean - pop_mean) / sems
  d = (sample_mean - pop_mean) / sd
  effect_size = ['small', 'medium', 'large'][np.argmin([abs(d - x) for x in [0.2, 0.5, 0.8]])]
  res = {
    'df': df,
    'SEM_s': sems,
    't': t,
    'd': d,
    'effect_size': effect_size
  }
  return res

def t_stat2(sample_mean, num_samples, stddev, one_sided=True, alpha=0.05):
  samples1 = [1.752, 1.818, 1.597, 1.697, 1.644,  1.593]
  samples2 = [1.878, 1.648, 1.819, 1.794, 1.745,  1.827]
  tStat, twoTailProb = ttest_ind(samples1, samples2)
  # Result is: -2.072, 0.0650

  tStat, twoTailProb = ttest_ind(samples1, samples2, equal_var=False)
  # Result is: # t-statistic-2.072, p-value:0.0654 

def calc_z(x, mean, sd):
  return (x - mean) / sd

def z_significance(sample_mean, num_samples, pop_mean, stddev, one_sided=True, alpha=0.05):
  """
  Write code in Python that 
      computes the z-score, 
      determines statistical significance, 
      effect size 
  """
  z_score, p_value = z_test_mean(sample_mean, num_samples, pop_mean, stddev, one_sided)
  reject_null = p_value < alpha
  d = (sample_mean - pop_mean) / stddev
  effect_size = ['small', 'medium', 'large'][np.argmin([abs(d - x) for x in [0.2, 0.5, 0.8]])]
  res = {
    'z_score': z_score,
    'p_value': p_value,
    'reject_null': reject_null,
    'd': d,
    'effect_size': effect_size
  }
  return res

def z_test_mean(sample_mean, num_samples, pop_mean, stddev, one_sided=True):
  semp = stddev / math.sqrt(num_samples)
  z_score = (sample_mean - pop_mean) / semp
  p_value = 1 - erf(z_score/math.sqrt(2))
  if one_sided:
    p_value *= 0.5
  return z_score, p_value

def countFreq(arr):
  """
  params: 
  - arr: array of objects that may convert to ints
  returns:
  - frequency table
  """
  unique = {}
  for val in arr:
    unique[val] = unique.get(val, 0) + 1
  convertToInts = lambda strlist: [int(el) for el in strlist] 
  return convertToInts(list(unique.keys())), list(unique.values())

def definitional_population(data):
  """
  definitional formula for sum of deviation scores
  params:
  - data: array of data
  
  returns:
  - ss: sum of squares
  - var: variance
  - std_dev: standard deviation
  """
  keys, freqs = countFreq(data)
  n = sum(freqs)
  mean = sum(data)/n
  dev_squared_by_freq = []
  for key, freq in zip(keys, freqs):
    dev_squared_by_freq.append((key - mean)**2 * freq)
  ss = sum(dev_squared_by_freq)
  var = ss/n
  std_dev = math.sqrt(var)
  return ss, var, std_dev

def computational_population(data):
  """
  computational formula for sum of deviation scores
  params:
  - data: array of data
  
  returns:
  - ss: sum of squares
  - var: variance
  - std_dev: standard deviation
  """
  _, freqs = countFreq(data)
  n = sum(freqs)
  ss = sum([x**2 for x in data]) - ((sum(data) ** 2)/n)
  var = ss/n
  std_dev = math.sqrt(var)
  return ss, var, std_dev

def definitional_sample(data):
  """
  definitional formula for sum of deviation scores
  params:
  - data: array of data
  
  returns:
  - ss: sum of squares
  - var: variance
  - std_dev: standard deviation
  """
  keys, freqs = countFreq(data)
  n = sum(freqs)
  mean = sum(data)/n
  dev_squared_by_freq = []
  for key, freq in zip(keys, freqs):
    dev_squared_by_freq.append((key - mean)**2 * freq)
  ss = sum(dev_squared_by_freq)
  var = ss/(n - 1)
  std_dev = math.sqrt(var)
  return ss, var, std_dev

def computational_sample(data):
  """
  computational formula for sum of deviation scores
  params:
  - data: array of data
  
  returns:
  - ss: sum of squares
  - var: variance
  - std_dev: standard deviation
  """
  _, freqs = countFreq(data)
  n = sum(freqs)
  ss = sum([x**2 for x in data]) - ((sum(data) ** 2)/n)
  var = ss/(n - 1)
  std_dev = math.sqrt(var)
  return ss, var, std_dev

def coef_of_variance(data):
  """
  computes coefficient of variance
  params: 
  - data: array of data
  returns:
  - coefficient of variance
  """
  mean = sum(data)/len(data)
  _, _, stddev = definitional_population(data)
  return stddev/mean if mean != 0 else float('nan')

def random_name():
  """
  if there's no outfile, make something absurd!
  return arbitrary png fname
  """
  replaceDot = lambda x: str(x).replace('.', '-')
  return f"{replaceDot(datetime.now().timestamp())}-{replaceDot(random())}.png"
  
def mean(data):
  """
  computes mean of data
  params: 
  - data: array of data
  returns:
  - mean of data
  """
  return sum(data)/len(data)

def median(data):
  """
  computes median of data
  params: 
  - data: array of data
  returns:
  - median of data
  """
  data = sorted(data)
  middle = math.floor(len(data)/2)
  if len(data) % 2 == 1:
    return data[middle]
  else:
    return (data[middle] + data[middle+1])/2

def mode(data):
  """
  computes mode of data
  params: 
  - data: array of data
  returns:
  - mode of data
  """
  nums, freqs = countFreq(data)
  return nums[freqs.index(max(freqs))]

def labeled_stats_two_samples(sample1, sample2, labels=["sample1", "sample2"]):
  """
  A function that displays statistics (mean, N, std. dev., and std. error) 
  for 2 samples (similar to Figure 9.4, top section on page 287). 
  Test using dataset from Figure 9.1/9.2 – you should get the same answer as the text.
  """
  def compute(data):
    res = {}
    res["mean"] = mean(data)
    _, _, res["stddev"] = computational_sample(data)
    res["N"] = len(data)
    res["stderr"] = res["stddev"] / math.sqrt(res["N"])
    return res

  res = {}
  res[labels[0]] = compute(sample1)
  res[labels[1]] = compute(sample2)
  return res

def labeled_stats_paired_samples(sample1, sample2, labels=["sample1", "sample2"]):
  """
  A function that displays statistics for a Paired Samples T-Test 
  (Mean difference, std. dev of difference, std. error of mean diff., 
    95% confidence intervals, t-value, df, and sign. (2-tailed)).  
  (Similar to Figure 9.4, bottom section on page 287). 
  Test using dataset from Figure 9.1/9.2 – you should get the same answer as the text.
  """
  res = {}
  diffs = []
  for x, y in zip(sample1, sample2):
    diffs.append(x-y)
  meandiff = sum(diffs) / len(diffs)
  sd = abs(sum([diff ** 2 for diff in diffs]) - ((sum(diffs) ** 2) / len(diffs)))
  stddevdiff = math.sqrt( sd / (len(diffs) - 1))
  semdiff = stddevdiff / math.sqrt(len(diffs))
  res["mean_diff"] = meandiff
  res["stddev_diff"] = stddevdiff
  res["sem_diff"] = semdiff
  res["confidence_intervals"] = confidence_intervals(meandiff, stddevdiff, len(diffs), one_tailed=False)["0.95"]
  res["t_value"] = meandiff / semdiff
  res["df"] = len(diffs) - 1
  res["sig"] =  (1 - t.cdf(res["t_value"], df=res["df"])) * 2
  d = meandiff / stddevdiff
  res["effect_size"] = {
    "d": d,
    "description": ['small', 'medium', 'large'][np.argmin([abs(d - x) for x in [0.2, 0.5, 0.8]])]
  }
  return res

def labeled_stats_independent_samples(sample1, sample2, labels=["sample1", "sample2"]):
  """
  A function that displays statistics for an Independent Samples T-Test 
  (Mean difference, std. dev of difference, std. error of mean diff., 
    95% confidence intervals, t-value, df, and sign. (2-tailed)) 
  assuming equal variance. 
  (Similar to Figure 10.7, bottom section on page 334). 
  Test using dataset from Figure 10.4/10.5 – you should get the same answer as the text.
  """
  res = {}
  mean1 = mean(sample1)
  mean2 = mean(sample2)
  _, _, stddev1 = computational_sample(sample1)
  _, _, stddev2 = computational_sample(sample2)
  meandiff = mean1 - mean2
  num = (len(sample1) - 1) + (len(sample2) - 1)
  stddevind = (((len(sample1) - 1) * (stddev1 ** 2)) + ((len(sample2) - 1) * (stddev2 ** 2))) / num
  semind = math.sqrt((stddevind / len(sample1)) + (stddevind / len(sample2)))
  res["mean_ind"] = meandiff
  res["stddev_ind"] = stddevind
  res["sem_ind"] = semind
  res["t_value"] = meandiff / semind
  res["condidence_intervals"] = {
    "upper": meandiff + res["t_value"],
    "lower": meandiff - res["t_value"],
  }
  res["df"] = num
  res["sig"] =  (1 - t.cdf(res["t_value"], df=res["df"])) * 2
  sdpooled = math.sqrt(((stddev1 ** 2) + (stddev2 ** 2)) / 2)
  d = meandiff / sdpooled
  res["effect_size"] = {
    "d": d,
    "description": ['small', 'medium', 'large'][np.argmin([abs(d - x) for x in [0.2, 0.5, 0.8]])]
  }
  return res


def labeled_stats(data, sample=False):
  """
  computes a few basic stats for a given array of data
  params:
  - data: array of data
  - sample (default False): whether to do sample stats instead of population
  results:
  - res: dictionary with computational and definitional ss, var, stddev, as well as mean, median, mode
  """
  res = {}
  computational = computational_population
  definitional = definitional_population
  if sample:
    computational = computational_sample
    definitional = definitional_sample

  ss, var, std_dev = computational(data)
  res["computational"] = {
    "ss": ss,
    "var": var,
    "std_dev": std_dev
  }
  ss, var, std_dev = definitional(data)
  res["definitional"] = {
    "ss": ss,
    "var": var,
    "std_dev": std_dev
  }
  res["tendencies"] = {
    "mean": mean(data),
    "median": median(data),
    "mode": mode(data)
  }
  res["other"] = {
    "min": min(data),
    "max": max(data),
    "cov": coef_of_variance(data)
  }
  return res

def pretty_print(structure, tabspace=4, indent=4, offset=0):
  """
  pretty printer
  prints formatted objects!
  could use pprint, but don't want to add any dependencies, and this was pretty fun
  """
  spaces = ' '.join(['' for x in range(offset)])
  print(spaces + pretty_print_helper(structure, indent=indent, tabspace=tabspace, offset=offset, trail=False, lead=False))

def pretty_print_helper(structure, indent=0, tabspace=4, offset=0, trail=False, lead=False):
  """
  recurse through list/dicts!
  """
  spaces = ' '.join(['' for x in range(indent + offset)])
  bracket_space = ' '.join(['' for x in range(indent + offset - tabspace)])
  if type(structure) == dict:
    current_string = bracket_space + "{\n"
    if not lead:
      current_string = "{\n"
    for i, (key, val) in enumerate(structure.items()):
      current_string += spaces + f'"{key}": '
      if type(val) in [list, dict]:
        current_string += pretty_print_helper(val, indent=indent+tabspace, tabspace=tabspace, offset=offset, trail=(i!=len(structure.items())), lead=False)
      else:
        if i==len(structure.items())-1:
          current_string += str(val) + "\n"
        else:
          current_string += str(val) + ",\n"
    if trail:
      current_string += bracket_space + "},\n"
    else:
      current_string += bracket_space + "}\n"
  elif type(structure) == list:
    current_string = bracket_space + "[\n" 
    if not lead:
      current_string = "[\n" 
    for i, item in enumerate(structure):
      if type(item) in [list, dict]:
        current_string += pretty_print_helper(item, indent=indent+tabspace, tabspace=tabspace, offset=offset, trail=(i!=len(structure)), lead=True)
      else:
        if i==len(structure)-1:
          current_string += spaces + str(item) + "\n"
        else:
          current_string += spaces + str(item) + ",\n"
    if trail:
      current_string += bracket_space + "],\n"
    else:
      current_string += bracket_space + "]\n"
  else:
    current_string = spaces + str(structure)
  return current_string


def print_header(category):
  print("\n**{}**\n".format(category))
  print("| question | p value | mean difference | upper limit CI | lower limit CI | df | effect size (d) | effect size (desctiption) |")
  print("| --- | --- | --- | --- | --- | --- | --- | --- |")

def print_row(question, p, meandiff, upper, lower, df, cohen_d, effect_size_desc):
  # | question | p value | mean difference | upper limit CI | lower limit CI | df | effect size (d) | effect size (desctiption) |
  print("|", " | ".join([str(question), str(round(p, 5)), str(round(meandiff, 5)), str(round(upper, 5)), str(round(lower, 5)), str(df), str(round(cohen_d, 5)), str(effect_size_desc)]), "|")

if __name__ == "__main__":
  with open('res-a.json', 'r') as f:
    a_data = json.load(f)
  with open('res-b.json', 'r') as f:
    b_data = json.load(f)

  # category = 'count_fear' # 'count_natural' 'count_angry' 'count_sad' 'count_joy' 'count_fear'
  for category in ['count_natural', 'count_angry', 'count_sad', 'count_joy', 'count_fear']:
    print_header(category)
    for i in range(12):
      _, p = ttest_ind(a_data[i]['scores']['data'][category], b_data[i]['scores']['data'][category])
      res = labeled_stats_independent_samples(
        a_data[i]['scores']['data'][category], 
        b_data[i]['scores']['data'][category])
      print_row(a_data[i]['question'].strip(), p, res['mean_ind'], res['condidence_intervals']['upper'], res['condidence_intervals']['lower'], res['df'], res['effect_size']['d'], res['effect_size']['description'])