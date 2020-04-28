# turned out I wasn't normalizing by input size
      results[i]['scores']['lda']['input']['anger'] *= (1487 / len(results[i]['question'].split()))
      results[i]['scores']['lda']['input']['sadness'] *= (1302 / len(results[i]['question'].split()))
      results[i]['scores']['lda']['input']['fear'] *= (1772 / len(results[i]['question'].split()))
      results[i]['scores']['lda']['input']['joy'] *= (1269 / len(results[i]['question'].split()))

I must fix this in the input score model