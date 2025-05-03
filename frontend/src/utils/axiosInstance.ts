import axios from "axios"

export const axiosInstance = axios.create({
    baseURL: process.env.NEXT_PUBLIC_BACKEND_URL,
    withCredentials: true
})

axiosInstance.interceptors.request.use(function (config) {
    console.log(`${config.method} Request Send To ${config.url}\n${config.data}`)
    return config;
  }, function (error) {
    return Promise.reject(error);
  });

axiosInstance.interceptors.response.use(function (response) {
    console.log(`Incoming Response From ${response.config.url} With Data ${response.data}`)
    return response;
  }, function (error) {
    return Promise.reject(error);
  });