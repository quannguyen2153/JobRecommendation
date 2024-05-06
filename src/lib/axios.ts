import axios from 'axios';

const config = {
  baseURL: process.env.NEXT_PUBLIC_SITE_URL,
  headers: {
    Accept: 'application/json',
    'Content-Type': 'application/json',
  },
};

const axiosClient = axios.create(config);

axiosClient.interceptors.response.use(
  (res: any) => Promise.resolve(res.data),
  async (err: any) => {
    // const originalRequest = err.config;
    // console.log('err.response.status', err.response.status, err.config.__isRetryRequest);

    if (
      err &&
      err.response &&
      err.response.status === 401 &&
      !err.config.__isRetryRequest
    ) {
      // const { setKeySite } = useKey();
      // const refreshToken = getKey(KEY_CONTEXT.REFRESH_TOKEN);
      // const salt = encryptRSA(`${getCurrentTS()}`);
      // const params = JSON.stringify({
      //   ...REFRESH_TOKEN_ACT,
      //   data: [{ refreshToken }],
      // }).replace(/\\n/g, '');
      // return axios
      //   .post(`${import.meta.env.REACT_APP_BASE_URI}${import.meta.env.REACT_APP_GETWAY}`, {
      //     headers: config.headers,
      //   })
      //   .then(async (response: any) => {
      //     const authToken = response.data.result.data.token;
      //     const rfTK = response.data.result.data.refreshToken;
      //     originalRequest.headers = {
      //       ...originalRequest.headers,
      //       authorization: `Bearer ${authToken}`,
      //     };
      //     const key: IKeyAuth = {
      //       authToken,
      //       refreshToken: rfTK,
      //     };
      //     originalRequest.__isRetryRequest = true;
      //     setKeySite(key);
      //     return axiosClient(originalRequest);
      //   })
      //   .catch(() => {
      //     // logoutRequest();
      //   });
      // return store.dispatch(logoutRequest());
    }
    return Promise.reject(((err || {}).response || {}).data);
  }
);

export default axiosClient;
