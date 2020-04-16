import { reactive } from "@vue/composition-api"

function useFetch({ url, method, body, cb }) {
  return fetch(
    url,
    {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    }
  ).then(response => {
    let res = response.json()
    cb(response)
    return res
  }).catch((error) => {
    console.error('Error:', error)
  })
}

function useModel({ endpoint }) {
  const responseState = reactive({
    error: false,
    result: {},
    loading: false,
    resultExists: false,
  })

  function postData(body, queryparam="") {
    responseState.loading = true
    console.log("Getting something :3")
    let prod = true;
    if(process.env.NODE_ENV == "dev") prod = false;
    let url = `http://localhost:5000/${endpoint}/${queryparam}`;
    if(prod) url = `https://sproj.model.colehollant.com/${endpoint}/${queryparam}`;
    let code = -1
    useFetch({
      url,
      method: 'POST',
      body,
      cb: (response) => { code = response.status }
    })
    .then((response) => {
      if(code !== 200) {
        responseState.error = true;
        responseState.result = response;
        responseState.loading = false;
        responseState.resultExists = false;
        console.log("FAILED")
        return
      }
      responseState.error = false;
      responseState.result = response.data;
      responseState.loading = false;
      responseState.resultExists = true;
    }); 
  }

  return { responseState, postData }
}

export function useControlModel() {
  return useModel({ endpoint: 'control' })
}

export function useRawScoreModel() {
  return useModel({ endpoint: 'score' })
}

export function useLdaModel() {
  return useModel({ endpoint: 'lda' })
}

export function useAlterTargetModel() {
  return useModel({ endpoint: 'make-affect' })
}